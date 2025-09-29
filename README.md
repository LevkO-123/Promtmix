# Promtmix v2 (flat) — calculators + news

**What changed vs v1**
- Flat file layout (no folders in URLs) → fewer mistakes on upload.
- Visual polish + animations.
- **News** page auto-updates daily via GitHub Actions from Google News RSS (US, Canada, Europe, World, Crypto, Tech).
- All CSS/JS at root (`style.css`, `pmx.js`).

## How to deploy
1. Open your repo `promtmix` → **Add file → Upload files**.
2. Upload EVERYTHING from this ZIP (keep the filenames as-is).
3. In **Settings → Pages**: Source `Deploy from a branch`, Branch `main`, folder `/ (root)`.
4. Visit `https://levko-123.github.io/promtmix/`

## IDs configured
- AdSense: `ca-pub-6781021197640734`
- Amazon tag: `promtmix20-20`
- Sovrn Commerce key: `2422504`

## News auto-update
- Workflow `.github/workflows/news.yml` runs daily and regenerates `news.html` using Google News RSS links.
- You can edit feeds in `news_builder.py`.
