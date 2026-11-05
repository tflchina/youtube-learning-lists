#!/usr/bin/env python3
"""Resolve the catalog and create/update playlists in the signed-in YouTube account."""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MONTHLY = ROOT / "catalog" / "monthly"
SCOPES = ["https://www.googleapis.com/auth/youtube"]


def execute_with_retry(request, attempts: int = 5):
    from googleapiclient.errors import HttpError

    for attempt in range(attempts):
        try:
            return request.execute()
        except HttpError as error:
            if error.resp.status not in {409, 429, 500, 502, 503, 504} or attempt == attempts - 1:
                raise
            time.sleep(2 ** attempt)


def catalog_path(edition: str | None = None) -> Path:
    if edition:
        path = MONTHLY / f"{edition}.json"
        if not path.exists():
            raise SystemExit(f"Edition not found: {path}")
        return path
    files = sorted(MONTHLY.glob("????-??.json"))
    if not files:
        raise SystemExit(f"No monthly catalogs found in {MONTHLY}")
    return files[-1]


def load_catalog(edition: str | None = None):
    return json.loads(catalog_path(edition).read_text())


def youtube_client(client_secret: Path):
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    token = ROOT / ".youtube-token.json"
    creds = Credentials.from_authorized_user_file(token, SCOPES) if token.exists() else None
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(str(client_secret), SCOPES)
        creds = flow.run_local_server(port=0)
        token.write_text(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def resolve_video(youtube, topic: str, channel: str, video_id: str | None = None) -> dict:
    if video_id:
        response = youtube.videos().list(part="snippet,status", id=video_id).execute()
        if not response.get("items"):
            raise RuntimeError(f"Pinned video is unavailable: {topic} ({video_id})")
        item = response["items"][0]
        if item.get("status", {}).get("privacyStatus") != "public":
            raise RuntimeError(f"Pinned video is not public: {topic} ({video_id})")
        return {"id": video_id, "title": item["snippet"]["title"],
                "channel": item["snippet"]["channelTitle"]}
    result = youtube.search().list(
        part="snippet", q=f'{topic} "{channel}"', type="video", maxResults=5,
        safeSearch="strict", videoEmbeddable="true", relevanceLanguage="en"
    ).execute()
    exact = [x for x in result.get("items", []) if channel.lower() in x["snippet"]["channelTitle"].lower()]
    if not exact:
        raise RuntimeError(f'No strict channel match for "{topic}" from "{channel}"')
    item = exact[0]
    return {"id": item["id"]["videoId"], "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"]}


def existing_playlists(youtube) -> dict[str, str]:
    found, token = {}, None
    while True:
        response = youtube.playlists().list(part="snippet", mine=True, maxResults=50, pageToken=token).execute()
        found.update({x["snippet"]["title"]: x["id"] for x in response.get("items", [])})
        token = response.get("nextPageToken")
        if not token:
            return found


def playlist_items(youtube, playlist_id: str) -> set[str]:
    found, token = set(), None
    while True:
        response = youtube.playlistItems().list(part="contentDetails", playlistId=playlist_id,
                                                maxResults=50, pageToken=token).execute()
        found.update(x["contentDetails"]["videoId"] for x in response.get("items", []))
        token = response.get("nextPageToken")
        if not token:
            return found


def sync(youtube, privacy: str, dry_run: bool, edition: str | None):
    catalog = load_catalog(edition)
    current = existing_playlists(youtube) if not dry_run else {}
    resolved = {"edition": catalog["edition"], "playlists": []}
    for spec in catalog["playlists"]:
        videos = [resolve_video(youtube, *pick) for pick in spec["picks"]]
        ids = [video["id"] for video in videos]
        if len(ids) != len(set(ids)):
            duplicates = sorted({video_id for video_id in ids if ids.count(video_id) > 1})
            raise RuntimeError(f'Duplicate videos in {spec["title"]}: {duplicates}')
        resolved["playlists"].append({**spec, "videos": videos})
        print(f'\n{spec["title"]} ({len(videos)} videos)')
        for video in videos:
            print(f'  - {video["title"]} — {video["channel"]} https://youtu.be/{video["id"]}')
        if dry_run:
            continue
        playlist_id = current.get(spec["title"])
        created_now = False
        if not playlist_id:
            created = youtube.playlists().insert(part="snippet,status", body={
                "snippet": {"title": spec["title"], "description": spec["description"]},
                "status": {"privacyStatus": privacy}
            }).execute()
            playlist_id = created["id"]
            created_now = True
            current[spec["title"]] = playlist_id
        # A new playlist can briefly return playlistNotFound while YouTube propagates it.
        present = set() if created_now else playlist_items(youtube, playlist_id)
        for video in videos:
            if video["id"] not in present:
                execute_with_retry(youtube.playlistItems().insert(part="snippet", body={"snippet": {
                    "playlistId": playlist_id, "resourceId": {"kind": "youtube#video", "videoId": video["id"]}
                }}))
    (ROOT / "catalog" / "resolved.json").write_text(json.dumps(resolved, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-secret", type=Path, default=Path(os.getenv("YOUTUBE_CLIENT_SECRET", "client_secret.json")))
    parser.add_argument("--privacy", choices=["private", "unlisted", "public"], default="private")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--edition", help="Monthly edition in YYYY-MM format; defaults to latest")
    args = parser.parse_args()
    sync(youtube_client(args.client_secret), args.privacy, args.dry_run, args.edition)


if __name__ == "__main__":
    main()
