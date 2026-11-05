#!/usr/bin/env python3
"""Pin unpinned monthly picks to IDs from the last reviewed dry run."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
resolved_path = root / "catalog/resolved.json"
resolved = json.loads(resolved_path.read_text())
edition = resolved["edition"]
catalog_path = root / "catalog/monthly" / f"{edition}.json"
catalog = json.loads(catalog_path.read_text())
by_slug = {playlist["slug"]: playlist for playlist in resolved["playlists"]}

for playlist in catalog["playlists"]:
    old = by_slug[playlist["slug"]]
    if len(old["videos"]) != len(playlist["picks"]):
        raise SystemExit(f'Pick count changed for {playlist["slug"]}; cannot pin by position')
    playlist["picks"] = [
        pick if len(pick) == 3 else [pick[0], pick[1], old["videos"][index]["id"]]
        for index, pick in enumerate(playlist["picks"])
    ]

# The original search resolved the first two Scratch topics to the same game.
# Pin the official introductory tutorial for the first topic instead.
coding = next(item for item in catalog["playlists"] if item["slug"] == "coding-creativity")
coding["picks"][0] = ["Getting Started with Scratch", "Scratch Team", "9jTPZfhuVro"]

catalog_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")
print(f"Pinned {sum(len(p['picks']) for p in catalog['playlists'])} picks in {catalog_path}")
