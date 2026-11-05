# Easy ways to load the lists into YouTube

## Recommendation

Use the included Python importer for a full monthly edition. It is the least repetitive official
bulk method: one Google OAuth approval, a dry-run review, then one command to create or update all
six playlists. It uses the official YouTube Data API and keeps credentials on your computer.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/youtube_playlists.py --edition 2026-11 --dry-run
.venv/bin/python scripts/youtube_playlists.py --edition 2026-11 --privacy private
```

## Alternatives researched

### Manual YouTube saving

Best when adding only a few videos. Open a result from `LISTS.md`, use **Save**, and select or
create a playlist. This needs no developer setup, but repeating it for 72 picks every month is
slow and error-prone. YouTube's official help documents this workflow:
https://support.google.com/youtube/answer/57792

### YouTube Studio

Useful for editing titles, descriptions, visibility, ordering, and adding videos after a playlist
exists. It is better for final review than bulk importing a catalog:
https://support.google.com/youtube/answer/10232933

### Google Apps Script

Apps Script can manage playlists through its advanced YouTube service, but that service must be
enabled and uses the same YouTube Data API objects and quotas. It moves the code into Google but
does not remove the API/OAuth setup, so it is not simpler for this repository:
https://developers.google.com/apps-script/advanced/youtube

### Third-party playlist importers

Not recommended here. They may require broad access to a Google/YouTube account, can disappear,
and add another party's privacy and security practices. Prefer YouTube's UI or an importer whose
source and credentials remain under your control.

## Monthly file workflow

1. Copy the newest `catalog/monthly/YYYY-MM.json` to the new month's filename.
2. Change its `edition` to match the filename and refresh its picks.
3. Run `python3 scripts/validate_catalog.py` and `python3 scripts/render_catalog.py`.
4. Run the importer with `--edition YYYY-MM --dry-run` and review every resolved video.
5. Run it again without `--dry-run`, keeping playlists private until a parent has reviewed them.
