# Dainers Club · Daily Newsletters

**사이트:** https://yalli2.github.io/dainers_club/ — 날짜별 영어·스페인어 뉴스레터, 릴스, 카드뉴스, PDF를 한곳에서 봅니다.

`newsletters/<YYYY-MM-DD>/{en,es}/` — 10 Instagram slides (1080x1350 PNG), an A4 PDF, a 60s feed video (`video_*`, 4:5) and a 60s Reels video (`reels_*`, 9:16) per language.
- `en`: world news for English learners · `es`: Spanish-speaking world news for Spanish learners
- Rebuild: `NODE_PATH=$(npm root -g) python3 tools/build.py` (edit `tools/content.py` first). Logo: `assets/dain_logo.jpg`. Korean text layer: `tools/content_ko.py`.

## How the site updates
- **Always commit new editions to the `main` branch.** GitHub Pages serves `main`; other branches never appear on the site.
- `tools/build.py` writes `newsletters/<DATE>/meta.json` (headlines) and rebuilds `newsletters/index.json` at the end of each build (`tools/manifest.py`).
- Added a folder by hand? Run `python3 tools/manifest.py` before committing. The page also finds new date folders on `main` through the GitHub API, so a missed index update still shows up (without headlines).
