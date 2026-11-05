# Privacy Notice

Last updated: 2026-11-04

This command-line project uses YouTube API Services only when a user runs the importer. It asks
Google for authorization to manage that user's YouTube account so it can search for videos,
list/create playlists, inspect playlist items, and add videos to playlists.

The project has no server, analytics, advertising, user database, or developer-operated data
collection. Google OAuth credentials and tokens are stored only on the user's computer in
`client_secret.json` and `.youtube-token.json`; both are excluded from Git. The project does not
send those files to the repository owner or any third party. Exact resolved search results may be
stored locally in `catalog/resolved.json`, which is also excluded from Git.

Users can revoke access at any time in their Google Account's third-party connections page and
can delete the local token file. Removing playlists or other YouTube data must be done in the
user's YouTube account.

Use of YouTube API Services is also governed by the
[Google Privacy Policy](https://policies.google.com/privacy) and
[YouTube Terms of Service](https://www.youtube.com/t/terms).
