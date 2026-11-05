#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / "catalog/playlists.json").read_text())
assert len(data["playlists"]) >= 6
slugs = set()
for playlist in data["playlists"]:
    assert playlist["slug"] not in slugs
    slugs.add(playlist["slug"])
    assert 10 <= len(playlist["picks"]) <= 15
    assert all(len(pick) == 2 and all(pick) for pick in playlist["picks"])
print(f'OK: {len(data["playlists"])} playlists, {sum(len(x["picks"]) for x in data["playlists"])} picks')
