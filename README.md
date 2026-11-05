# YouTube Learning Lists for Age 10

A balanced, family-oriented catalog with **6 playlists and 72 picks**, spanning science, math,
physics, culture, creativity, and downtime. See the browsable [current lists](LISTS.md).

The source catalog stores a topic plus a trusted channel for every pick. The importer resolves
those picks with YouTube Data API `safeSearch=strict`, writes the exact results to
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

Edit `catalog/playlists.json`, change `edition`, run `scripts/render_catalog.py`, then run the
importer again. Keep 10–15 picks per list. Preview replacements for age fit, sponsorships,
language, and comments; no automated filter replaces a parent's judgment.

## Safety choices

- Trusted educational or official channels are named for each topic.
- Strict SafeSearch and embeddable videos are required during resolution.
- Playlists default to private; use `--privacy unlisted` or `--privacy public` deliberately.
- OAuth tokens, client secrets, and generated exact results are excluded from Git.

This is an independent community project and is not affiliated with YouTube or the channels.
