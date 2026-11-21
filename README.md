# Dain Club · Daily Newsletters
`newsletters/<YYYY-MM-DD>/{en,es}/` — 10 Instagram slides (1080x1350 PNG), an A4 PDF, a 60s feed video (`video_*`, 4:5) and a 60s Reels video (`reels_*`, 9:16) per language.
- `en`: world news for English learners · `es`: Latin America news for Spanish learners
- Issues: 2026-11-09, 2026-11-21
- Content per issue: `tools/issues/<YYYY-MM-DD>.py` (EN/ES + Korean layer `KO`).
- Rebuild newest issue: `NODE_PATH=$(npm root -g) python3 tools/build.py` · a specific one: `ISSUE=2026-11-09 NODE_PATH=$(npm root -g) python3 tools/build.py`. Logo: `assets/dain_logo.jpg`.
