# YouTube Learning Lists for Age 10

A balanced, family-oriented catalog with **6 playlists and 72 picks**, spanning science, math,
physics, culture, creativity, and downtime. See the browsable [current lists](LISTS.md).

Each edition is preserved as a separate file under [`catalog/monthly`](catalog/monthly), named
`YYYY-MM.json`. The scripts use the newest edition unless `--edition YYYY-MM` is supplied.

The source catalog stores a topic, trusted channel, and—after review—a pinned video ID for every
pick. Unpinned picks are resolved with YouTube Data API `safeSearch=strict`, and the importer writes
the exact results to
`catalog/resolved.json`, and creates private playlists by default.

## Load into a YouTube account

1. In Google Cloud, create a project, enable **YouTube Data API v3**, configure an OAuth consent
   screen, and create an **OAuth desktop app** credential.
2. Download the credential as `client_secret.json` into this folder. Never commit it.
3. Use Python 3.10+:

   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   .venv/bin/python scripts/youtube_playlists.py --dry-run
   .venv/bin/python scripts/youtube_playlists.py --privacy private
   ```

The browser login asks for permission to manage YouTube playlists. Re-running is additive: it
reuses playlists with the same title and skips videos already present. Review
`catalog/resolved.json` before the non-dry run if you want to approve every exact match.

## Monthly upkeep

Copy the latest `catalog/monthly/YYYY-MM.json` to the new month, update its `edition` and picks,
run `scripts/render_catalog.py`, then run the importer again. Never overwrite an older monthly
file. Keep 10–15 picks per list. Preview replacements for age fit, sponsorships, language, and
comments; no automated filter replaces a parent's judgment.

For the exact commands and a comparison of manual, Python, and Apps Script approaches, see
[EASY-WAYS.md](EASY-WAYS.md).

## Safety choices

- Trusted educational or official channels are named for each topic.
- Strict SafeSearch and embeddable videos are required during resolution.
- Playlists default to private; use `--privacy unlisted` or `--privacy public` deliberately.
- OAuth tokens, client secrets, and generated exact results are excluded from Git.

This is an independent community project and is not affiliated with YouTube or the channels.
See the [Disclaimer](DISCLAIMER.md), [Privacy Notice](PRIVACY.md), and [Terms of Use](TERMS.md).
