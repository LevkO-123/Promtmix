#!/usr/bin/env python3
import datetime, re
from pathlib import Path
import feedparser

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "news.html"

FEEDS = {
    "us": ["https://news.google.com/rss/headlines/section/geo/United%20States?hl=en-US&gl=US&ceid=US:en"],
    "canada": ["https://news.google.com/rss/headlines/section/geo/Canada?hl=en-US&gl=US&ceid=US:en"],
    "europe": ["https://news.google.com/rss/search?q=Europe&hl=en-US&gl=US&ceid=US:en"],
    "world": ["https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en"],
    "crypto": ["https://news.google.com/rss/search?q=cryptocurrency+OR+bitcoin+OR+ethereum&hl=en-US&gl=US&ceid=US:en"],
    "tech": ["https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en"],
}

def clean(text, limit=140):
    text = re.sub('<[^<]+?>', '', text or '')
    text = text.replace('\xa0',' ').strip()
    return (text[:limit] + '…') if len(text)>limit else text

def fetch_items(urls, max_items=12):
    items = []
    for u in urls:
        try:
            d = feedparser.parse(u)
            for e in d.entries:
                items.append({
                    "title": clean(e.get("title","")),
                    "link": e.get("link",""),
                    "summary": clean(getattr(e, "summary", "") or getattr(e, "description", ""), 180),
                    "published": e.get("published","")
                })
        except Exception:
            pass
    # De-dup by title
    seen = set(); out=[]
    for it in items:
        t = it["title"]
        if t in seen: continue
        seen.add(t); out.append(it)
        if len(out)>=max_items: break
    return out

def render_section(name, items):
    cards = "\n".join([
        f"""
    <div class="news-item">
      <h4><a href="{it['link']}" target="_blank" rel="noopener nofollow">{it['title']}</a></h4>
      <div class="news-meta">{it['published']}</div>
      <div class="small">{it['summary']}</div>
    </div>""" for it in items
    ])
    return f"""
  <h2 id="{name.capitalize()}">{name.capitalize()}</h2>
  <div class="news-col">{cards or '<div class="small">No items</div>'}</div>"""

def build():
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    sections = []
    for key, urls in FEEDS.items():
        items = fetch_items(urls, max_items=12)
        sections.append(render_section(key, items))
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>News dashboard — Promtmix</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
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
    </nav>
  </div>
  <div class="hero">
    <h1>Daily News</h1>
    <p class="small">Auto‑updated from Google News RSS. Last update: {now}. Headlines link to original sources.</p>
    <div class="alert small">We only show headlines/snippets and link out. All rights belong to original publishers.</div>
    {''.join(sections)}
  </div>
  <footer>© {datetime.datetime.utcnow().year} Promtmix — Free calculators & tools.</footer>
</div>
</body></html>"""
    OUT.write_text(html, encoding="utf-8")

if __name__ == "__main__":
    build()
