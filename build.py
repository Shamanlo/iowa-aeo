#!/usr/bin/env python3
"""Static site generator for Iowa AEO.

    python3 build.py          # writes the site to docs/

Content lives in src/content.py, icons in src/icons.py, and CSS/JS/images
in static/. Everything in docs/ is generated; don't edit it by hand.
"""
import html
import json
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from content import HUBS, INDUSTRIES, SERVICES, PROCESS, SEO_VS_AEO, HOME_FAQ  # noqa: E402
from icons import icon, logo_mark, AI_MARKS, AIS  # noqa: E402

# ---------------------------------------------------------------------------
# Site settings. Fill in PHONE / BOOKING_URL / HERO_VIDEO when you have them.
# ---------------------------------------------------------------------------
SITE_URL = "https://iowaaeo.com"
NAME = "Iowa AEO"
EMAIL = "info@iowaaeo.com"
PHONE = ""            # e.g. "(515) 555-0123" - shows the phone pill in the header when set
BOOKING_URL = ""      # e.g. a Calendly link - "Book a Call" goes to the contact form until set
WEB3FORMS_KEY = "9d30dc0e-53df-46e9-8f84-d1cb44ea1039"
HERO_VIDEO = ""       # e.g. "/assets/video/hero.mp4" or a YouTube embed URL
HERO_POSTER = ""      # optional poster image for the hero video
MEDIA_VIDEOS = []     # [{"title": "...", "src": "/assets/video/x.mp4" or YouTube embed URL, "poster": ""}]

OUT = ROOT / "docs"
TODAY = date.today().isoformat()
ASSET_VER = TODAY.replace("-", "")

e = html.escape
INDUSTRY_BY_SLUG = {i["slug"]: i for i in INDUSTRIES}
ALL_TOWNS = [(hub, t) for hub in HUBS for t in hub["towns"]]


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
def hl(text):
    return f'<span class="hl">{text}</span>'


def eyebrow(text):
    return f'<p class="eyebrow">{text}</p>'


def btn(label, href, kind="primary", ico=None, attrs=""):
    i = icon(ico, 18) if ico else ""
    return f'<a class="btn btn-{kind}" href="{href}"{attrs}>{label}{i}</a>'


def book_href():
    return BOOKING_URL or "/contact/?topic=call#form"


def tel(phone):
    return "tel:+1" + "".join(c for c in phone if c.isdigit())[-10:]


def town_url(hub, town):
    return f"/locations/{hub['slug']}/{town[1]}/"


def town_label(town):
    return f"{town[0]}, {town[2]}"


def question_set(city, industries, per=1):
    out = []
    for slug in industries:
        for q in INDUSTRY_BY_SLUG[slug]["questions"][:per]:
            out.append({"q": q["q"].format(city=city), "you": q["you"],
                        "review": q["review"], "site": q["site"], "city": city})
    return out


def jsonld(obj):
    return ('<script type="application/ld+json">'
            + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>")


ORG = {
    "@type": "ProfessionalService",
    "@id": SITE_URL + "/#org",
    "name": NAME,
    "url": SITE_URL + "/",
    "email": EMAIL,
    "logo": SITE_URL + "/assets/img/logo-mark.svg",
    "image": SITE_URL + "/assets/img/og.png",
    "description": "Answer Engine Optimization (AEO) agency helping Iowa businesses get recommended by "
                   "ChatGPT, Gemini, Perplexity, Claude and Google AI Overviews.",
    "areaServed": [{"@type": "City", "name": f"{h['name']}, Iowa"} for h in HUBS]
                  + [{"@type": "State", "name": "Iowa"}],
    "address": {"@type": "PostalAddress", "addressRegion": "IA", "addressCountry": "US"},
    "knowsAbout": ["Answer Engine Optimization", "Generative Engine Optimization",
                   "AI search optimization", "Local SEO", "Structured data"],
}
if PHONE:
    ORG["telephone"] = PHONE


def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in items]}


def breadcrumb_schema(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": n + 1, "name": name, "item": SITE_URL + url}
        for n, (name, url) in enumerate(crumbs)]}


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
def nav():
    ind = "".join(
        f'<a class="dd-item" href="/industries/{i["slug"]}/"><span class="dd-ico">{icon(i["icon"], 18)}</span>{i["name"]}</a>'
        for i in INDUSTRIES)
    loc_cols = "".join(
        f'''<div class="dd-col"><a class="dd-hub" href="/locations/{h["slug"]}/">{icon("pin", 16)}{h["name"]}</a>
{"".join(f'<a class="dd-town" href="{town_url(h, t)}">{t[0]}</a>' for t in h["towns"][:6])}
<a class="dd-more" href="/locations/{h["slug"]}/#towns">All {h["name"]} areas →</a></div>'''
        for h in HUBS)
    phone = (f'<a class="btn btn-dark btn-phone" href="{tel(PHONE)}">{icon("phone", 18)}{PHONE}</a>'
             if PHONE else
             f'<a class="btn btn-dark btn-phone" href="/contact/#form">{icon("sparkles", 18)}Free AI Check</a>')
    return f'''<header class="site-header" data-header>
<div class="wrap header-in">
<a class="brand" href="/" aria-label="{NAME} home">{logo_mark(42)}<span class="brand-word">Iowa <span>AEO</span></span></a>
<nav class="main-nav" aria-label="Main">
<a href="/" data-nav="/">Home</a>
<a href="/about/" data-nav="/about/">About</a>
<div class="dd"><button class="dd-btn" aria-expanded="false" data-nav="/industries/">Industries{icon("chevron", 16)}</button>
<div class="dd-panel dd-ind"><div class="dd-grid">{ind}</div><a class="dd-all" href="/industries/">All industries →</a></div></div>
<div class="dd"><button class="dd-btn" aria-expanded="false" data-nav="/locations/">Locations{icon("chevron", 16)}</button>
<div class="dd-panel dd-loc"><div class="dd-cols">{loc_cols}</div><a class="dd-all" href="/locations/">All Iowa locations →</a></div></div>
<a href="/media-room/" data-nav="/media-room/">Media Room</a>
<a href="/contact/" data-nav="/contact/">Contact</a>
</nav>
{phone}
<button class="menu-btn" aria-label="Open menu" aria-expanded="false" data-menu>{icon("menu", 24)}</button>
</div>
<div class="mobile-nav" data-mobile-nav hidden>
<a href="/">Home</a><a href="/about/">About</a>
<details><summary>Industries{icon("chevron", 18)}</summary>{"".join(f'<a href="/industries/{i["slug"]}/">{i["name"]}</a>' for i in INDUSTRIES)}<a href="/industries/">All industries</a></details>
<details><summary>Locations{icon("chevron", 18)}</summary>{"".join(f'<a href="/locations/{h["slug"]}/">{h["name"]}</a>' for h in HUBS)}<a href="/locations/">All locations</a></details>
<a href="/media-room/">Media Room</a><a href="/contact/">Contact</a>
{btn("Get a Free AI Check", "/contact/#form", "primary", "arrow")}
</div>
</header>'''


def footer():
    hub_cols = "".join(
        f'<div><h3><a href="/locations/{h["slug"]}/">{h["name"]}</a></h3>'
        + "".join(f'<a href="{town_url(h, t)}">{t[0]}</a>' for t in h["towns"]) + "</div>"
        for h in HUBS)
    return f'''<footer class="site-footer">
<div class="wrap">
<div class="foot-top">
<div class="foot-brand">
<a class="brand" href="/">{logo_mark(42)}<span class="brand-word">Iowa <span>AEO</span></span></a>
<p>Answer Engine Optimization for Iowa businesses. We help you get recommended by ChatGPT, Gemini, Perplexity, Claude and Google AI Overviews.</p>
<a class="foot-mail" href="mailto:{EMAIL}">{icon("mail", 18)}{EMAIL}</a>
{f'<a class="foot-mail" href="{tel(PHONE)}">{icon("phone", 18)}{PHONE}</a>' if PHONE else ""}
</div>
<div class="foot-links">
<div><h3>Company</h3><a href="/about/">About</a><a href="/media-room/">Media Room</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy</a></div>
<div><h3>Industries</h3>{"".join(f'<a href="/industries/{i["slug"]}/">{i["short"]}</a>' for i in INDUSTRIES)}</div>
</div>
</div>
<div class="foot-towns">{hub_cols}</div>
<div class="foot-bottom"><span>© {date.today().year} {NAME}. All rights reserved.</span><span>AEO · GEO · AIO · AI SEO · LLM SEO</span></div>
</div>
</footer>'''


def page(path, title, desc, body, schema=None, og_title=None):
    url = SITE_URL + path
    graph = [ORG, {"@type": "WebSite", "@id": SITE_URL + "/#site", "url": SITE_URL + "/", "name": NAME,
                   "publisher": {"@id": SITE_URL + "/#org"}}]
    graph += schema or []
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#34C73A">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{e(og_title or title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=DM+Mono:wght@400;500&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_VER}">
{jsonld({"@context": "https://schema.org", "@graph": graph})}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{nav()}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/site.js?v={ASSET_VER}" defer></script>
</body>
</html>
'''
    dest = OUT / path.lstrip("/") / "index.html" if path.endswith("/") else OUT / path.lstrip("/")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding="utf-8")
    PAGES.append(path)


PAGES = []


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------
def crumbs_html(crumbs):
    parts = []
    for n, (name, url) in enumerate(crumbs):
        if n == len(crumbs) - 1:
            parts.append(f'<span aria-current="page">{name}</span>')
        else:
            parts.append(f'<a href="{url}">{name}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep">/</span>'.join(parts) + "</nav>"


def hero(title_html, sub=None, eyebrow_txt="AEO · GEO · AIO · AI SEO · LLM SEO", crumbs=None, compact=False):
    return f'''<section class="hero{' hero-compact' if compact else ''}">
<div class="wrap hero-in">
{crumbs_html(crumbs) if crumbs else ""}
{eyebrow(eyebrow_txt)}
<h1>{title_html}</h1>
{f'<p class="hero-sub">{sub}</p>' if sub else ""}
<div class="hero-ctas">
{btn("Book a Call", book_href(), "primary", "calendar")}
{btn("Submit a Form", "#form", "ghost", "send")}
</div>
</div>
</section>'''


def video_frame(title_html="Is AI recommending<br>" + hl("your competitors?")):
    tiles = [("utensils", "Restaurants"), ("wrench", "Home services"), ("tooth", "Dental"),
             ("scale", "Law"), ("corn", "Ag")]
    strip = "".join(f'<div class="vt vt-{n}"><span class="vt-ico">{icon(ic, 34)}</span><span>{lbl}</span></div>'
                    for n, (ic, lbl) in enumerate(tiles))
    if HERO_VIDEO:
        media = (f'<button class="vf-play" data-video="{e(HERO_VIDEO)}" data-poster="{e(HERO_POSTER)}" '
                 f'aria-label="Play video">{icon("play", 34)}</button>')
    else:
        media = ""
    return f'''<section class="vf-sec"><div class="wrap">
<div class="vframe" data-vframe>
<div class="vf-top"></div>
<div class="vf-head"><h2>{title_html}</h2></div>
<div class="vf-strip">{strip}<div class="vt vt-you"><span class="you-tag">Your business</span></div></div>
{media}
</div></div></section>'''


def simulator(questions, heading=None, sub=None):
    data = {"questions": questions}
    qs = "".join(
        f'<button class="sim-q{" is-on" if n == 0 else ""}" data-q="{n}" aria-pressed="{"true" if n == 0 else "false"}">{e(q["q"])}</button>'
        for n, q in enumerate(questions))
    ais = "".join(
        f'<button class="sim-ai{" is-on" if n == 0 else ""}" data-ai="{k}" aria-pressed="{"true" if n == 0 else "false"}">{AI_MARKS[k]}<span>{name}</span></button>'
        for n, (k, name) in enumerate(AIS))
    sigs = [
        ("listings", "Consistent listings", "Your name, hours and address match on Google, Bing, Apple Maps and Yelp."),
        ("reviews", "Specific reviews", "Customers describe what you do best, in their own words."),
        ("website", "Answer-ready website", "Clear pages that answer the exact questions people ask AI."),
        ("schema", "Structured data", "Schema markup tells AI your services, service area and hours."),
        ("mentions", "Trusted mentions", "Local press, guides and directories mention you by name."),
    ]
    toggles = "".join(
        f'''<label class="sim-t"><input type="checkbox" data-sig="{k}"><span class="sw" aria-hidden="true"></span>
<span class="sim-t-txt"><strong>{t}</strong><span>{d}</span></span></label>''' for k, t, d in sigs)
    return f'''<section class="sim-sec" id="try-it">
<div class="wrap">
<div class="sec-head center">
{eyebrow("Try it yourself")}
<h2>{heading or ("See How AI Picks " + hl("Who to Recommend"))}</h2>
<p>{sub or "Pick a question, choose an AI, then switch on the signals we build. Watch what happens to your business in the answer."}</p>
</div>
<div class="sim" data-sim>
<script type="application/json" class="sim-data">{json.dumps(data, ensure_ascii=False).replace("</", "<\\/")}</script>
<div class="sim-left">
<div class="card sim-card"><h3><span class="num">1</span>Ask a question</h3><div class="sim-qs">{qs}</div></div>
<div class="card sim-card"><h3><span class="num">2</span>Pick an AI</h3><div class="sim-ais">{ais}</div></div>
<div class="card sim-card"><h3><span class="num">3</span>Switch on AEO signals</h3><div class="sim-ts">{toggles}</div>
<div class="meter"><div class="meter-top"><span>AI confidence in your business</span><strong data-pct>6%</strong></div>
<div class="meter-bar"><span data-bar style="width:6%"></span></div><p class="meter-lbl" data-lvl>INVISIBLE</p></div>
<div class="sim-btns"><button class="btn btn-primary" data-all>Turn All On{icon("sparkles", 18)}</button><button class="btn btn-ghost" data-reset>Reset</button></div>
</div>
</div>
<div class="sim-right">
<div class="sim-status"><span class="pill" data-pill>Your business: <strong>Not mentioned</strong></span><span class="sim-why" data-why>AI couldn't find enough consistent information about you.</span></div>
<div class="chat" data-chat data-ai="chatgpt" aria-live="polite"></div>
</div>
</div>
<p class="sim-note">A simulated example to show how AI assistants weigh information when choosing businesses. Real answers vary by platform and change over time.</p>
</div>
</section>'''


def services_bento(place="Iowa"):
    cards = "".join(
        f'<article class="bento-card tone-{s["tone"]}"><span class="b-ico">{icon(s["icon"], 24)}</span><h3>{s["title"]}</h3><p>{s["body"]}</p></article>'
        for s in SERVICES)
    return f'''<section class="sec"><div class="wrap bento">
<article class="bento-intro">
{eyebrow("What we do")}
<h2>Get Recommended<br>{hl("by AI.")}</h2>
<p>AI assistants don't rank ten websites. They read what's written about your business across the web, decide who fits the question, and recommend a few names. If your information is thin, inconsistent or hard to read, you get skipped, even if you're the best option in {place}.</p>
<p>We fix that. AEO gives AI systems clean facts, clear answers and trusted third-party proof, so they can recommend you with confidence.</p>
{btn("Check My AI Visibility", "#form", "primary", "arrow")}
</article>
{cards}
</div></section>'''


def process_sec():
    steps = "".join(f'<li><span class="step-n">0{n + 1}</span><h3>{t}</h3><p>{d}</p></li>'
                    for n, (t, d) in enumerate(PROCESS))
    return f'''<section class="sec sec-dark"><div class="wrap">
<div class="sec-head">{eyebrow("How it works")}<h2>From invisible to {hl("recommended")}</h2>
<p>A clear, repeatable process. No tricks, no gimmicks, just making your business easy for AI to understand and trust.</p></div>
<ol class="steps">{steps}</ol>
</div></section>'''


def ais_strip():
    chips = "".join(f'<span class="ai-chip">{AI_MARKS[k]}{n}</span>' for k, n in AIS)
    return f'''<section class="ai-strip"><div class="wrap"><p>Optimizing for the assistants your customers already use</p>
<div class="ai-chips">{chips}<span class="ai-chip">{icon("sparkles", 20)}Copilot &amp; more</span></div></div></section>'''


def industries_grid(heading=None):
    cards = "".join(
        f'<a class="ind-card" href="/industries/{i["slug"]}/"><span class="ind-ico">{icon(i["icon"], 26)}</span><h3>{i["name"]}</h3><p>{i["lede"]}</p><span class="more">Learn more {icon("arrow", 16)}</span></a>'
        for i in INDUSTRIES)
    return f'''<section class="sec"><div class="wrap">
<div class="sec-head">{eyebrow("Industries")}<h2>{heading or ("Built for Iowa's " + hl("local businesses"))}</h2>
<p>Every industry gets asked different questions. We tailor the facts, pages and reviews to what your customers actually ask AI.</p></div>
<div class="ind-grid">{cards}</div>
</div></section>'''


def locations_grid():
    cards = "".join(
        f'''<article class="loc-card"><a class="loc-main" href="/locations/{h["slug"]}/"><span class="loc-reg">{h["region"]}</span><h3>{h["name"]}</h3>
<span class="more">AEO in {h["name"]} {icon("arrow", 16)}</span></a>
<div class="loc-towns">{"".join(f'<a href="{town_url(h, t)}">{t[0]}</a>' for t in h["towns"])}</div></article>'''
        for h in HUBS)
    return f'''<section class="sec sec-tint" id="locations"><div class="wrap">
<div class="sec-head">{eyebrow("Locations")}<h2>Serving businesses {hl("across Iowa")}</h2>
<p>Four home markets, plus the towns around them. We know which questions people ask AI in each one.</p></div>
<div class="loc-grid">{cards}</div>
</div></section>'''


def seo_vs_aeo():
    rows = "".join(f"<tr><th scope=\"row\">{a}</th><td>{b}</td><td>{c}</td></tr>" for a, b, c in SEO_VS_AEO)
    return f'''<section class="sec"><div class="wrap">
<div class="sec-head">{eyebrow("AEO vs SEO")}<h2>Search changed. {hl("So did the rules.")}</h2></div>
<div class="table-wrap"><table class="cmp"><thead><tr><th></th><th>Traditional SEO</th><th class="col-aeo">AEO</th></tr></thead><tbody>{rows}</tbody></table></div>
</div></section>'''


def faq_sec(items, heading=None):
    qa = "".join(f'<details class="faq"><summary>{q}<span class="faq-x">{icon("plus", 20)}</span></summary><p>{a}</p></details>'
                 for q, a in items)
    return f'''<section class="sec" id="faq"><div class="wrap faq-wrap">
<div class="sec-head">{eyebrow("FAQ")}<h2>{heading or ("Questions, " + hl("answered"))}</h2>
<p>Still curious? <a href="/contact/">Send us a question</a> and we'll get back to you.</p></div>
<div class="faqs">{qa}</div>
</div></section>'''


def city_options(selected=""):
    opts = ['<option value="">Choose your area</option>']
    for h in HUBS:
        opts.append(f'<optgroup label="{h["name"]} area">')
        for name in [h["query_city"] if h["slug"] != "quad-cities" else "Quad Cities"] + [t[0] for t in h["towns"]]:
            sel = " selected" if name == selected else ""
            opts.append(f'<option{sel}>{name}</option>')
        opts.append("</optgroup>")
    opts.append(f'<option{" selected" if selected == "Other" else ""}>Other Iowa town</option>')
    return "".join(opts)


def lead_form(city="", topic="audit", source="", heading=None, dark=True):
    where = f" in {city}" if city else ""
    return f'''<section class="sec cta-sec{' cta-dark' if dark else ''}" id="form"><div class="wrap cta-in">
<div class="cta-copy">
{eyebrow("Free AI visibility check")}
<h2>Is AI recommending you{where}? {hl("Let's find out.")}</h2>
<p>Tell us about your business. We'll ask ChatGPT, Gemini, Perplexity, Claude and Google AI Overviews the questions your customers ask, and send you what they say, plus the first fixes we'd make.</p>
<ul class="ticks"><li>{icon("check", 18)}No cost, no obligation</li><li>{icon("check", 18)}Real answers from 5 AI assistants</li><li>{icon("check", 18)}Plain-English next steps</li></ul>
<p class="cta-mail">Prefer email? <a href="mailto:{EMAIL}">{EMAIL}</a></p>
</div>
<form class="lead" action="https://api.web3forms.com/submit" method="POST" data-form>
<input type="hidden" name="access_key" value="{WEB3FORMS_KEY}">
<input type="hidden" name="subject" value="New lead from {NAME}{where}">
<input type="hidden" name="from_name" value="{NAME} Website">
<input type="hidden" name="page" value="{e(source)}">
<input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off">
<fieldset class="topic"><legend>What can we help with?</legend>
<label><input type="radio" name="topic" value="Free AI visibility check"{' checked' if topic == 'audit' else ''}><span>Free AI check</span></label>
<label><input type="radio" name="topic" value="Book a call"{' checked' if topic == 'call' else ''}><span>Book a call</span></label>
<label><input type="radio" name="topic" value="General question"{' checked' if topic == 'general' else ''}><span>Question</span></label>
</fieldset>
<div class="row2">
<label>Your name<input name="name" required autocomplete="name"></label>
<label>Business name<input name="business" required autocomplete="organization"></label>
</div>
<div class="row2">
<label>Email<input type="email" name="email" required autocomplete="email"></label>
<label>Phone<input type="tel" name="phone" autocomplete="tel"></label>
</div>
<div class="row2">
<label>Website<input name="website" placeholder="yourbusiness.com" autocomplete="url"></label>
<label>City<select name="city">{city_options(city)}</select></label>
</div>
<label>Anything we should know?<textarea name="message" rows="3" placeholder="What you do, who your customers are, questions you'd like AI to answer with your name"></textarea></label>
<button class="btn btn-primary btn-wide" type="submit">Send{icon("send", 18)}</button>
<p class="form-msg" data-msg role="status"></p>
</form>
</div></section>'''


def towns_grid(hub, current=None):
    links = "".join(
        f'<a class="town-chip{" is-cur" if current and t[1] == current[1] else ""}" href="{town_url(hub, t)}">{icon("pin", 16)}{town_label(t)}</a>'
        for t in hub["towns"])
    return links


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def build_home():
    qs = [
        question_set("Des Moines", ["restaurants"])[0],
        question_set("Cedar Rapids", ["home-services"])[0],
        question_set("Iowa City", ["dentists"])[0],
        question_set("Davenport", ["law-firms"])[0],
    ]
    body = (hero("<span class=\"hl\">Answer Engine Optimization</span><br>Agency in Iowa",
                 "Get your business recommended by ChatGPT, Gemini, Perplexity, Claude and Google AI Overviews in Des Moines, Cedar Rapids, Iowa City and the Quad Cities.")
            + video_frame() + simulator(qs) + ais_strip() + services_bento() + process_sec()
            + industries_grid() + locations_grid() + seo_vs_aeo() + faq_sec(HOME_FAQ) + lead_form(source="Home"))
    page("/", "Iowa AEO | Answer Engine Optimization Agency in Iowa",
         "Iowa AEO helps Iowa businesses get recommended by ChatGPT, Gemini, Perplexity, Claude and Google AI Overviews. Serving Des Moines, Cedar Rapids, Iowa City and the Quad Cities.",
         body, [faq_schema(HOME_FAQ)])


def hub_faq(hub):
    n = hub["name"]
    towns = ", ".join(t[0] for t in hub["towns"][:5])
    return [
        (f"Do you work with businesses in {n}?",
         f"Yes. {n} is one of our four home markets. We work with businesses across the area, including {towns} and the surrounding towns."),
        (f"What do people in {n} ask AI about local businesses?",
         f"Mostly practical questions: who's open now, who can come today, who takes my insurance, where's good for a group dinner. AI answers with a few names, and AEO is how you become one of them in {n}."),
        (f"How is AEO different from local SEO in {n}?",
         "Local SEO helps you show up in the Google map pack and search results. AEO helps you get named in AI-written answers. Both rely on accurate listings and a strong website, so we build them together."),
        ("How do I know if AI is recommending me now?",
         "Ask for a free AI visibility check. We'll ask the major AI assistants the questions your customers ask and send you exactly what they say."),
    ]


def build_hub(hub):
    n, city = hub["name"], hub["query_city"]
    qs = question_set(city, ["restaurants", "home-services", "dentists", "agriculture" if hub["slug"] == "iowa-city" else "law-firms"])
    path = f"/locations/{hub['slug']}/"
    crumbs = [("Home", "/"), ("Locations", "/locations/"), (n, path)]
    faq = hub_faq(hub)
    body = (hero(f"{hl('AEO Agency')} in<br>{n}, Iowa" if hub["slug"] != "quad-cities" else f"{hl('AEO Agency')} in the<br>Quad Cities",
                 hub["blurb"], f"{hub['region']} · AEO · AI SEO", crumbs)
            + simulator(qs, f"What does AI say about {hl(n)}?",
                        f"Real questions people in the {n} area ask AI. Switch on the signals and watch who gets recommended.")
            + f'''<section class="sec sec-tint" id="towns"><div class="wrap">
<div class="sec-head">{eyebrow("Areas we serve")}<h2>{n} {hl("and nearby")}</h2>
<p>We help businesses across the {n} area show up when customers ask AI for a recommendation in their own town.</p></div>
<div class="town-grid">{towns_grid(hub)}</div></div></section>'''
            + services_bento(n) + process_sec() + industries_grid(f"Industries we help in {hl(n)}")
            + faq_sec(faq) + lead_form(n if hub["slug"] != "quad-cities" else "Quad Cities", source=n))
    schema = [faq_schema(faq), breadcrumb_schema(crumbs),
              {"@type": "Service", "name": f"Answer Engine Optimization in {n}", "serviceType": "Answer Engine Optimization",
               "provider": {"@id": SITE_URL + "/#org"}, "areaServed": {"@type": "City", "name": f"{city}, IA"}}]
    page(path, f"AEO Agency in {n}, Iowa | {NAME}" if hub["slug"] != "quad-cities" else f"AEO Agency in the Quad Cities | {NAME}",
         f"Answer Engine Optimization in {n}. Get your business recommended by ChatGPT, Gemini, Perplexity, Claude and Google AI Overviews. {hub['blurb'][:80]}",
         body, schema)


def build_town(hub, town):
    name, slug, state, blurb = town
    label = f"{name}, {state}"
    path = town_url(hub, town)
    crumbs = [("Home", "/"), ("Locations", "/locations/"), (hub["name"], f"/locations/{hub['slug']}/"), (name, path)]
    qs = question_set(name, ["home-services", "restaurants", "dentists", "auto"])
    faq = [
        (f"Do you offer AEO in {name}?",
         f"Yes. We help businesses in {name} and across the {hub['name']} area get recommended by ChatGPT, Gemini, Perplexity, Claude and Google AI Overviews."),
        (f"Why isn't AI recommending my {name} business?",
         "Usually because the facts AI finds are thin or inconsistent: different hours on different sites, a service area that doesn't mention your town, or reviews that don't describe what you do. Those are all fixable."),
        (f"Should my website mention {name} specifically?",
         f"If you serve {name}, yes. AI matches questions like “who can fix my furnace in {name}” to businesses that clearly say they serve {name}, with real details about the work they do there."),
    ]
    nearby = [t for t in hub["towns"] if t[1] != slug]
    body = (hero(f"{hl('AEO')} in {name}, {state}",
                 f"{blurb} We help {name} businesses get named when customers ask AI for a recommendation.",
                 f"{hub['name']} area · AEO · AI SEO", crumbs, compact=True)
            + simulator(qs, f"What does AI say in {hl(name)}?",
                        f"Questions people in {name} ask AI every day. Switch on the signals and see who gets recommended.")
            + services_bento(name)
            + f'''<section class="sec sec-tint"><div class="wrap">
<div class="sec-head">{eyebrow("Nearby")}<h2>Also serving the {hl(hub["name"] + " area")}</h2></div>
<div class="town-grid"><a class="town-chip hub-chip" href="/locations/{hub["slug"]}/">{icon("pin", 16)}{hub["name"]} (all areas)</a>{"".join(f'<a class="town-chip" href="{town_url(hub, t)}">{icon("pin", 16)}{town_label(t)}</a>' for t in nearby)}</div></div></section>'''
            + faq_sec(faq) + lead_form(name, source=label))
    schema = [faq_schema(faq), breadcrumb_schema(crumbs),
              {"@type": "Service", "name": f"Answer Engine Optimization in {label}", "serviceType": "Answer Engine Optimization",
               "provider": {"@id": SITE_URL + "/#org"},
               "areaServed": {"@type": "City", "name": f"{name}, {'Iowa' if state == 'IA' else 'Illinois'}"}}]
    page(path, f"AEO in {label} | Get Recommended by AI | {NAME}",
         f"Answer Engine Optimization for {name}, {state} businesses. Get recommended by ChatGPT, Gemini, Perplexity, Claude and Google AI Overviews.",
         body, schema)


def build_locations_index():
    path = "/locations/"
    crumbs = [("Home", "/"), ("Locations", path)]
    body = (hero(f"AEO Across {hl('Iowa')}",
                 "Des Moines, Cedar Rapids, Iowa City and the Quad Cities, plus the towns around them. Pick your area to see what local customers ask AI.",
                 "Locations", crumbs, compact=True)
            + locations_grid() + lead_form(source="Locations"))
    page(path, f"Locations | AEO Across Iowa | {NAME}",
         "Iowa AEO serves Des Moines, Cedar Rapids, Iowa City, the Quad Cities and nearby towns with Answer Engine Optimization.",
         body, [breadcrumb_schema(crumbs)])


def build_industry(ind):
    path = f"/industries/{ind['slug']}/"
    crumbs = [("Home", "/"), ("Industries", "/industries/"), (ind["name"], path)]
    cities = [h["query_city"] for h in HUBS]
    qs = []
    for n, city in enumerate(cities):
        q = ind["questions"][n % len(ind["questions"])]
        qs.append({"q": q["q"].format(city=city), "you": q["you"], "review": q["review"], "site": q["site"], "city": city})
    sigs = "".join(f"<li>{icon('check', 20)}<span>{s}</span></li>" for s in ind["signals"])
    body = (hero(f"AEO for {hl(ind['name'])} in Iowa", ind["lede"], "Industries · AEO", crumbs, compact=True)
            + simulator(qs, f"What AI says about {hl(ind['short'].lower() if ind['short'] != 'Auto' else 'auto shops')}",
                        "Real questions Iowans ask AI in your industry. Switch on the signals and see who gets recommended.")
            + f'''<section class="sec"><div class="wrap split">
<div class="sec-head">{eyebrow("What AI looks for")}<h2>The signals that get {hl(ind['short'].lower() if ind['short'] != 'Auto' else 'auto shops')} recommended</h2>
<p>AI assistants compare what they can find about you against the question. These are the details that tip the answer in your favor.</p></div>
<ul class="sig-list">{sigs}</ul></div></section>'''
            + services_bento() + locations_grid() + faq_sec(ind["faq"]) + lead_form(source=ind["name"]))
    page(path, f"AEO for {ind['name']} in Iowa | {NAME}",
         f"Answer Engine Optimization for Iowa {ind['name'].lower()}. {ind['lede']}",
         body, [faq_schema(ind["faq"]), breadcrumb_schema(crumbs)])


def build_industries_index():
    path = "/industries/"
    crumbs = [("Home", "/"), ("Industries", path)]
    body = (hero(f"AEO for Every {hl('Iowa Business')}",
                 "Restaurants, contractors, dentists, law firms, clinics, agents, auto shops and ag businesses. Each gets asked different questions, so each needs a different playbook.",
                 "Industries", crumbs, compact=True)
            + industries_grid("Pick your " + hl("industry")) + lead_form(source="Industries"))
    page(path, f"Industries | AEO for Iowa Businesses | {NAME}",
         "Answer Engine Optimization for Iowa restaurants, home services, dentists, law firms, medical, real estate, auto and agriculture businesses.",
         body, [breadcrumb_schema(crumbs)])


def build_about():
    path = "/about/"
    crumbs = [("Home", "/"), ("About", path)]
    values = [
        ("search", "We test, not guess", "Every engagement starts by asking real AI assistants real customer questions, and we re-test every month so you can see what changed."),
        ("pin", "Iowa first", "We know the difference between Ankeny and Altoona, and why a Quad Cities business needs to be clear about which side of the river it's on."),
        ("doc", "Plain English", "No jargon-filled reports. You'll always know what we did, why it matters and what AI says about you now."),
        ("check", "Clean facts, no tricks", "AI rewards accurate, consistent, verifiable information. We build that, and we never use spammy shortcuts that could backfire."),
    ]
    vals = "".join(f'<article class="val"><span class="b-ico">{icon(i, 24)}</span><h3>{t}</h3><p>{d}</p></article>' for i, t, d in values)
    body = (hero(f"Helping Iowa Businesses<br>{hl('Get Recommended by AI')}",
                 "More customers start with a question to ChatGPT, Gemini or Google's AI instead of a list of links. We make sure the answer includes you.",
                 "About Iowa AEO", crumbs, compact=True)
            + f'''<section class="sec"><div class="wrap split">
<div class="sec-head">{eyebrow("Why we exist")}<h2>The way people find local businesses {hl("has changed")}</h2></div>
<div class="prose"><p>For twenty years, getting found meant ranking on Google. Now a growing share of people skip the list entirely. They ask an AI assistant a full question, like <em>“Who's a good dentist in Ankeny for kids?”</em>, and get back two or three names.</p>
<p>If your business isn't one of them, you don't get the call, no matter how good you are. Most Iowa businesses have never checked what AI says about them.</p>
<p>Iowa AEO exists to change that. We focus on the work that makes AI confident about a business: consistent listings, specific reviews, answer-ready web pages, structured data and trusted local mentions.</p></div>
</div></section>
<section class="sec sec-tint"><div class="wrap"><div class="sec-head">{eyebrow("How we work")}<h2>What you can {hl("count on")}</h2></div><div class="vals">{vals}</div></div></section>'''
            + process_sec() + locations_grid() + lead_form(source="About"))
    page(path, f"About | {NAME}",
         "Iowa AEO helps Iowa businesses get recommended by AI assistants like ChatGPT, Gemini, Perplexity, Claude and Google AI Overviews.",
         body, [breadcrumb_schema(crumbs)])


def video_embed(src, title, poster=""):
    if "youtube.com" in src or "youtu.be" in src or "vimeo.com" in src:
        return f'<iframe src="{e(src)}" title="{e(title)}" loading="lazy" allow="accelerometer; autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>'
    return f'<video src="{e(src)}" controls playsinline preload="metadata"{f" poster={chr(34)}{e(poster)}{chr(34)}" if poster else ""}></video>'


def build_media():
    path = "/media-room/"
    crumbs = [("Home", "/"), ("Media Room", path)]
    if MEDIA_VIDEOS:
        items = "".join(f'<article class="media-card"><div class="media-frame">{video_embed(v["src"], v["title"], v.get("poster", ""))}</div><h3>{e(v["title"])}</h3></article>'
                        for v in MEDIA_VIDEOS)
        grid = f'<div class="media-grid">{items}</div>'
    else:
        grid = f'''<div class="media-empty"><span class="b-ico">{icon("play", 26)}</span><h3>Videos are on the way</h3>
<p>Client spotlights, AEO explainers and before-and-after AI answers are coming soon. Want your business featured? <a href="/contact/">Get in touch</a>.</p></div>'''
    body = (hero(f"Media {hl('Room')}", "Videos, client spotlights and AEO explainers from Iowa AEO.", "Media Room", crumbs, compact=True)
            + f'<section class="sec"><div class="wrap">{grid}</div></section>' + lead_form(source="Media Room"))
    page(path, f"Media Room | {NAME}", "Videos, client spotlights and Answer Engine Optimization explainers from Iowa AEO.",
         body, [breadcrumb_schema(crumbs)])


def build_contact():
    path = "/contact/"
    crumbs = [("Home", "/"), ("Contact", path)]
    phone_card = (f'<a class="c-card" href="{tel(PHONE)}"><span class="b-ico">{icon("phone", 22)}</span><span><strong>Call</strong>{PHONE}</span></a>'
                  if PHONE else "")
    book_card = (f'<a class="c-card" href="{BOOKING_URL}"><span class="b-ico">{icon("calendar", 22)}</span><span><strong>Book a call</strong>Pick a time that works</span></a>'
                 if BOOKING_URL else "")
    body = (f'''<section class="hero hero-compact"><div class="wrap hero-in">{crumbs_html(crumbs)}{eyebrow("Contact")}
<h1>Let's Get You {hl("Recommended")}</h1>
<p class="hero-sub">Request a free AI visibility check, book a call, or just ask a question. We reply within one business day.</p>
<div class="c-cards"><a class="c-card" href="mailto:{EMAIL}"><span class="b-ico">{icon("mail", 22)}</span><span><strong>Email</strong>{EMAIL}</span></a>{phone_card}{book_card}
<span class="c-card"><span class="b-ico">{icon("pin", 22)}</span><span><strong>Serving</strong>Des Moines · Cedar Rapids · Iowa City · Quad Cities</span></span></div>
</div></section>'''
            + lead_form(source="Contact", dark=False))
    page(path, f"Contact | {NAME}", "Contact Iowa AEO for a free AI visibility check or to book a call. Email info@iowaaeo.com.",
         body, [breadcrumb_schema(crumbs)])


def build_privacy():
    path = "/privacy/"
    body = f'''<section class="hero hero-compact"><div class="wrap hero-in">{eyebrow("Legal")}<h1>Privacy {hl("Policy")}</h1>
<p class="hero-sub">Last updated {date.today().strftime("%B %-d, %Y")}</p></div></section>
<section class="sec"><div class="wrap prose narrow">
<h2>What we collect</h2><p>When you submit a form on this site we collect the details you enter: typically your name, business name, email, phone, website, city and message. We use this only to respond to you and provide the services you ask about.</p>
<h2>How forms are processed</h2><p>Form submissions are delivered to us by Web3Forms, a form-processing service. Web3Forms handles your submission only to deliver it to our inbox. See the <a href="https://web3forms.com/privacy" rel="noopener">Web3Forms privacy policy</a> for details.</p>
<h2>What we don't do</h2><p>We don't sell your information, and we don't add you to a mailing list without asking.</p>
<h2>Cookies</h2><p>This site doesn't use advertising or tracking cookies. Fonts are served by Google Fonts.</p>
<h2>Contact</h2><p>Questions about your information? Email <a href="mailto:{EMAIL}">{EMAIL}</a> and we'll help, including deleting anything you've sent us.</p>
</div></section>'''
    page(path, f"Privacy Policy | {NAME}", "How Iowa AEO handles information submitted through this website.", body)


def build_404():
    body = f'''<section class="hero"><div class="wrap hero-in">{eyebrow("404")}<h1>Even AI couldn't<br>{hl("find this page")}</h1>
<p class="hero-sub">The page you're looking for doesn't exist or has moved.</p>
<div class="hero-ctas">{btn("Go Home", "/", "primary", "arrow")}{btn("See Locations", "/locations/", "ghost", "pin")}</div></div></section>'''
    page("/404.html", f"Page not found | {NAME}", "Page not found.", body)
    PAGES.remove("/404.html")


def build_extras():
    urls = "".join(f"<url><loc>{SITE_URL}{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in PAGES)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    loc_lines = "\n".join(
        f"- [{h['name']}]({SITE_URL}/locations/{h['slug']}/): " + ", ".join(t[0] for t in h["towns"]) for h in HUBS)
    ind_lines = "\n".join(f"- [{i['name']}]({SITE_URL}/industries/{i['slug']}/): {i['lede']}" for i in INDUSTRIES)
    (OUT / "llms.txt").write_text(f"""# {NAME}

> {NAME} is an Answer Engine Optimization (AEO) agency in Iowa. We help local businesses get recommended by AI assistants including ChatGPT, Google Gemini, Google AI Overviews, Perplexity, Claude and Microsoft Copilot.

Contact: {EMAIL}{f' · {PHONE}' if PHONE else ''}
Service area: Iowa, focused on Des Moines, Cedar Rapids, Iowa City and the Quad Cities.

## Services
""" + "\n".join(f"- {s['title']}: {s['body']}" for s in SERVICES) + f"""

## Locations
{loc_lines}

## Industries
{ind_lines}

## Pages
- [Home]({SITE_URL}/)
- [About]({SITE_URL}/about/)
- [Contact]({SITE_URL}/contact/)
- [Media Room]({SITE_URL}/media-room/)
""")
    (OUT / "CNAME").write_text("iowaaeo.com\n")
    (OUT / ".nojekyll").write_text("")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "static", OUT / "assets")
    build_home()
    build_about()
    build_contact()
    build_media()
    build_privacy()
    build_industries_index()
    for ind in INDUSTRIES:
        build_industry(ind)
    build_locations_index()
    for hub in HUBS:
        build_hub(hub)
        for town in hub["towns"]:
            build_town(hub, town)
    build_404()
    build_extras()
    print(f"Built {len(PAGES)} pages into {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
