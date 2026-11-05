#!/usr/bin/env python3
import json
from pathlib import Path
from urllib.parse import quote_plus

root = Path(__file__).resolve().parents[1]
monthly = sorted((root / "catalog/monthly").glob("????-??.json"))
if not monthly:
    raise SystemExit("No monthly catalog files found")
data = json.loads(monthly[-1].read_text())
lines = [f'# YouTube Learning Lists — {data["edition"]}', '',
         'Six balanced playlists for a curious 10-year-old. Each has 12 hand-curated topics.', '',
         '> A parent should preview videos. Channels and videos can change after publication.', '']
for playlist in data["playlists"]:
    lines += [f'## {playlist["title"]}', '', playlist["description"], '']
    for topic, channel in playlist["picks"]:
        url = 'https://www.youtube.com/results?search_query=' + quote_plus(f'{topic} {channel}')
        lines.append(f'- [{topic.title()} — {channel}]({url})')
    lines.append('')
(root / "LISTS.md").write_text('\n'.join(lines))
