#!/usr/bin/env python3
import datetime, re
from pathlib import Path
import feedparser

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "news.html"

FEEDS = {
    "US": ["https://news.google.com/rss/headlines/section/geo/United%20States?hl=en-US&gl=US&ceid=US:en"],
    "Canada": ["https://news.google.com/rss/headlines/section/geo/Canada?hl=en-US&gl=US&ceid=US:en"],
    "Europe": ["https://news.google.com/rss/search?q=Europe&hl=en-US&gl=US&ceid=US:en"],
    "World": ["https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en"],
    "Crypto": ["https://news.google.com/rss/search?q=cryptocurrency+OR+bitcoin+OR+ethereum&hl=en-US&gl=US&ceid=US:en"],
    "Tech": ["https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en"]
}

def clean(text, limit=180):
    text = re.sub('<[^<]+?>', '', text or '')
    text = text.replace('\xa0',' ').strip()
    return (text[:limit] + '…') if len(text)>limit else text

def fetch(urls, n=6):
    items = []
    for u in urls:
        try:
            d = feedparser.parse(u)
            for e in d.entries:
                items.append({
                    "title": clean(e.get("title",""), 120),
                    "link": e.get("link",""),
                    "summary": clean(getattr(e, "summary", "") or getattr(e, "description", ""), 180),
                    "published": e.get("published","")
                })
        except Exception:
            pass
    # unique by title
    seen=set(); out=[]
    for it in items:
        t=it["title"]
        if t in seen: continue
        seen.add(t); out.append(it)
        if len(out)>=n: break
    return out

def section_html(name, items):
    cards = "\n".join([f'''
  <div class="card">
    <h3><a href="{{it["link"]}}" target="_blank" rel="noopener nofollow">{it["title"]}</a></h3>
    <div class="small">{it["published"]}</div>
    <p class="small">{it["summary"]}</p>
  </div>''' for it in items])
    return f"<h2>{name}</h2><div class='grid'>{cards}</div>"

def build():
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    parts = []
    for name, urls in FEEDS.items():
        parts.append(section_html(name, fetch(urls, 6)))
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>News — Promtmix</title>
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="bg-grid"></div>
<div class="container">
  <div class="header">
    <div class="brand">Promtmix</div>
    <nav>
      <a href="index.html">Home</a>
      <a href="converters.html">Converters</a>
      <a href="logistics.html">Logistics</a>
      <a href="nutrition.html">Nutrition</a>
      <a href="news.html">News</a>
      <a href="about.html">About</a>
      <a href="privacy.html">Privacy</a>
      <a href="terms.html">Terms</a>
    </nav>
  </div>
  <div class="hero">
    <h1>Daily News</h1>
    <p class="small">Auto‑updated from Google News RSS. Last update: {now}. Headlines link to original sources.</p>
    <div class="alert small">We only show headlines/snippets and link out. All rights belong to original publishers.</div>
    {' '.join(parts)}
  </div>
  <footer>© {datetime.datetime.utcnow().year} Promtmix — Free calculators & tools.</footer>
</div>
</body></html>"""
    OUT.write_text(html, encoding="utf-8")

if __name__ == "__main__":
    build()
