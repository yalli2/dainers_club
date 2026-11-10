# Dain Club · Daily Newsletters
`newsletters/<YYYY-MM-DD>/{en,es}/` — 10 Instagram slides (1080x1350 PNG), an A4 PDF, a 60s feed video (`video_*`, 4:5) and a 60s Reels video (`reels_*`, 9:16) per language.
- `en`: world news for English learners · `es`: Latin America news for Spanish learners
- Rebuild: `NODE_PATH=$(npm root -g) python3 tools/build.py` (edit `tools/content.py` first). Logo: `assets/dain_logo.jpg`. Korean text layer: `tools/content_ko.py`.
