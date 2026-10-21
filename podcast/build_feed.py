#!/usr/bin/env python3
"""Builds podcast RSS feeds and show pages from podcast/shows.json.

    python3 podcast/build_feed.py

Audio and cover art live in podcast/public/<slug>/ (audio in audio/). This
writes each show's feed.xml (submit it to Spotify, Apple or a Shopify podcast
app) and index.html (a simple player page). podcast/public/ is deployed to
Cloudflare Pages as its own project by .github/workflows/deploy.yml.
"""
import html
import json
import subprocess
from email.utils import format_datetime
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "public"
e = html.escape


def duration_seconds(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", str(path)], capture_output=True, text=True)
    return int(float(out.stdout.strip() or 0))


def hms(sec):
    return f"{sec // 3600:02d}:{sec % 3600 // 60:02d}:{sec % 60:02d}"


def rfc822(day):
    return format_datetime(datetime.fromisoformat(day).replace(hour=12, tzinfo=timezone.utc))


def build_show(cfg, base_url):
    slug = cfg["slug"]
    dst = OUT / slug
    show_url = f"{base_url}/{slug}"
    cover = f"{show_url}/{cfg['cover']}"

    items, cards = [], []
    for ep in sorted(cfg["episodes"], key=lambda x: x["date"], reverse=True):
        audio = dst / "audio" / ep["file"]
        url = f"{show_url}/audio/{ep['file']}"
        secs = duration_seconds(audio)
        items.append(f"""<item>
<title>{e(ep['title'])}</title>
<description><![CDATA[{ep['description']}]]></description>
<itunes:summary>{e(ep['description'])}</itunes:summary>
<enclosure url="{e(url)}" length="{audio.stat().st_size}" type="audio/mpeg"/>
<guid isPermaLink="false">{e(slug + ':' + ep['id'])}</guid>
<pubDate>{rfc822(ep['date'])}</pubDate>
<itunes:duration>{hms(secs)}</itunes:duration>
<itunes:episodeType>full</itunes:episodeType>
<itunes:explicit>false</itunes:explicit>
<itunes:image href="{e(cover)}"/>
</item>""")
        cards.append(f"""<article><h2>{e(ep['title'])}</h2><p class="d">{e(ep['date'])} · {secs // 60} min</p>
<audio controls preload="none" src="{e(url)}"></audio><p>{e(ep['description'])}</p></article>""")

    owner = f"<itunes:owner><itunes:name>{e(cfg['author'])}</itunes:name><itunes:email>{e(cfg['email'])}</itunes:email></itunes:owner>" if cfg.get("email") else ""
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:podcast="https://podcastindex.org/namespace/1.0">
<channel>
<title>{e(cfg['title'])}</title>
<link>{e(cfg.get('website', show_url + '/'))}</link>
<atom:link href="{show_url}/feed.xml" rel="self" type="application/rss+xml"/>
<description><![CDATA[{cfg['description']}]]></description>
<language>{cfg.get('language', 'en-us')}</language>
<itunes:author>{e(cfg['author'])}</itunes:author>
{owner}
<itunes:image href="{e(cover)}"/>
<image><url>{e(cover)}</url><title>{e(cfg['title'])}</title><link>{e(show_url)}/</link></image>
<itunes:category text="{e(cfg['category'])}">{f'<itunes:category text="{e(cfg["subcategory"])}"/>' if cfg.get('subcategory') else ''}</itunes:category>
<itunes:explicit>false</itunes:explicit>
<itunes:type>episodic</itunes:type>
<podcast:locked>no</podcast:locked>
{''.join(items)}
</channel>
</rss>
"""
    (dst / "feed.xml").write_text(feed, encoding="utf-8")
    (dst / "index.html").write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(cfg['title'])}</title>
<meta name="description" content="{e(cfg['description'])}">
<link rel="alternate" type="application/rss+xml" title="{e(cfg['title'])}" href="feed.xml">
<style>body{{margin:0;background:#f6f5f0;color:#111;font:17px/1.6 system-ui,sans-serif}}main{{max-width:760px;margin:0 auto;padding:40px 16px}}
header{{display:flex;gap:20px;align-items:center;margin-bottom:32px}}header img{{width:140px;height:140px;border-radius:16px}}h1{{margin:0 0 6px;font-size:32px;line-height:1.1}}
article{{background:#fff;border:1px solid #e3e1d8;border-radius:18px;padding:22px;margin-bottom:16px}}h2{{margin:0;font-size:21px}}.d{{margin:4px 0 12px;color:#666;font-size:14px}}
audio{{width:100%}}a{{color:inherit}}@media(max-width:520px){{header{{flex-direction:column;align-items:flex-start}}}}</style></head>
<body><main><header><img src="{e(cfg['cover'])}" alt=""><div><h1>{e(cfg['title'])}</h1><p>{e(cfg['description'])}</p>
<p><a href="feed.xml">RSS feed</a></p></div></header>{''.join(cards)}</main></body></html>
""", encoding="utf-8")
    print(f"{slug}: {len(items)} episode(s) -> {show_url}/feed.xml")


def main():
    cfg = json.loads((HERE / "shows.json").read_text())
    for show in cfg["shows"]:
        build_show(show, cfg["base_url"].rstrip("/"))
    (OUT / "index.html").write_text("<!doctype html><title>Podcasts</title><ul>" + "".join(
        f'<li><a href="/{s["slug"]}/">{e(s["title"])}</a></li>' for s in cfg["shows"]) + "</ul>\n")


if __name__ == "__main__":
    main()
