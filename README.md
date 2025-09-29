# Promtmix — ENGINE‑30K v1

Fast, minimalist **tools portfolio**: converters, logistics calculators, and nutrition utilities.
Static site (no servers), built by GitHub Actions and deployed on GitHub Pages (or Cloudflare Pages).

## Live structure
- `/` — home
- `/converters/` — unit converters
- `/logistics/` — box volume + dimensional weight
- `/nutrition/` — BMI, BMR/TDEE, macros
- `sitemap.xml`, `robots.txt` auto-generated

## Monetization
- **AdSense** (auto ads): `client=ca-pub-6781021197640734`
- **Amazon Associates**: `tag=promtmix20-20` — we use search links so they always work
- **Sovrn Commerce**: `key=2422504` — converts outgoing links automatically (replace with your true JS key if Sovrn gives a different one).

> All affiliate/ad scripts are loaded client-side and can be toggled by editing `config.json` and rebuilding.

## How to deploy (GitHub Pages)
1. Create a public repo named `promtmix` under your GitHub account.
2. Upload **all files from this ZIP** into the repo root (drag & drop in GitHub → "Upload files"). Commit.
3. Go to **Settings → Pages** → Source: `Deploy from a branch`, Branch: `main` and **root**. Save.
4. Wait 1–2 minutes. Open: `https://levko-123.github.io/promtmix/`

## Automatic builds (no PC needed)
- GitHub Actions workflow `/.github/workflows/build.yml` runs **daily** and on each push.
- It executes `src/build.py`, regenerates `/public`, copies to root, and commits changes.
- You can change the cron in the workflow file.

## Cloudflare Pages (optional)
You can also connect this repo in Cloudflare Pages for global CDN. No server, no idle shutdown.

## Configuration
Edit `/config.json`:
```json
{
  "base_url": "https://levko-123.github.io/promtmix",
  "adsense_client": "ca-pub-6781021197640734",
  "amazon_tag": "promtmix20-20",
  "sovrn_key": "2422504"
}
```
Commit changes and the Action will rebuild.

## Notes
- **Not medical advice.** Nutrition calculators are informational only.
- **Carriers change rules.** Dimensional weight divisors are common defaults (UPS/FedEx/DHL: 139 in³/lb; USPS: 166). Always verify with your carrier.
- This is a starter; we can add thousands of programmatic pages later.
