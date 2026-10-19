"""Inline SVG icons.

UI icons are simple 24px line icons. AI assistant marks are simplified,
hand-drawn approximations used only to label which assistant the
simulator is imitating.
"""

def _line(body, size=20):
    return (f'<svg class="i" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{body}</svg>')

_UI = {
    "search": '<circle cx="11" cy="11" r="7.5"/><path d="m21 21-4.6-4.6"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13"/><path d="M3.5 6h.01M3.5 12h.01M3.5 18h.01" stroke-width="3"/>',
    "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h8M8 9h2"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "calendar": '<rect x="3" y="4.5" width="18" height="17" rx="2.5"/><path d="M16 2.5v4M8 2.5v4M3 10h18M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01"/>',
    "send": '<path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4z"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "sparkles": '<path d="M10 3.5c.6 3.6 2.9 5.9 6.5 6.5-3.6.6-5.9 2.9-6.5 6.5-.6-3.6-2.9-5.9-6.5-6.5 3.6-.6 5.9-2.9 6.5-6.5z"/><path d="M18 14c.3 1.8 1.2 2.7 3 3-1.8.3-2.7 1.2-3 3-.3-1.8-1.2-2.7-3-3 1.8-.3 2.7-1.2 3-3z"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M18 6 6 18M6 6l12 12"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "mail": '<rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><path d="m3 6 9 7 9-7"/>',
    "play": '<path d="M7 4.5v15l13-7.5z" fill="currentColor"/>',
    "copy": '<rect x="8" y="8" width="13" height="13" rx="2.5"/><path d="M16 8V5.5A2.5 2.5 0 0 0 13.5 3h-8A2.5 2.5 0 0 0 3 5.5v8A2.5 2.5 0 0 0 5.5 16H8"/>',
    "thumb": '<path d="M7 10v11M15 5.9 14 10h5.8a2 2 0 0 1 1.9 2.6l-2.3 7A2 2 0 0 1 17.5 21H4a1 1 0 0 1-1-1v-9a1 1 0 0 1 1-1h2.8a2 2 0 0 0 1.8-1.1L12 2a3 3 0 0 1 3 3.9z"/>',
    "refresh": '<path d="M21 12a9 9 0 1 1-2.6-6.4L21 8"/><path d="M21 3v5h-5"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "mic": '<rect x="9" y="2.5" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3.5"/>',
    "wave": '<path d="M4 10v4M8 7v10M12 4v16M16 7v10M20 10v4"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    # industries
    "utensils": '<path d="M4 2v7a3 3 0 0 0 3 3v10M10 2v7a3 3 0 0 1-3 3M7 2v6"/><path d="M20 15V2a5 5 0 0 0-5 5v6a2 2 0 0 0 2 2h3zm0 0v7"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>',
    "tooth": '<path d="M12 5.5C10.5 4 8.6 3 6.8 3 4.3 3 3 5.2 3 7.8c0 2.6 1.2 4.3 1.8 6.6.6 2.4.8 6.6 2.6 6.6 2 0 2-4.6 4.6-4.6s2.6 4.6 4.6 4.6c1.8 0 2-4.2 2.6-6.6.6-2.3 1.8-4 1.8-6.6C21 5.2 19.7 3 17.2 3c-1.8 0-3.7 1-5.2 2.5z"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M12 3l-1 4M12 3l1 4"/><path d="m5 7-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "heart": '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/><path d="M3.5 12h4l1.5-3 3 6 1.5-3h7"/>',
    "home": '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22v-8h6v8"/>',
    "car": '<path d="M5 17H3v-5l2-5.5A2 2 0 0 1 6.9 5h10.2a2 2 0 0 1 1.9 1.5L21 12v5h-2"/><path d="M3 12h18"/><circle cx="7.5" cy="17" r="2"/><circle cx="16.5" cy="17" r="2"/><path d="M9.5 17h5"/>',
    "corn": '<path d="M12 2.5c2.6 0 4 3 4 6.5v5c0 2-1.8 3.5-4 3.5s-4-1.5-4-3.5V9c0-3.5 1.4-6.5 4-6.5z"/><path d="M12 3v14M8.2 7h7.6M8 10.5h8M8 14h8"/><path d="M12 21.5c-3.5-1-6-4-6.5-8.5 2.5 1 5 3.5 6.5 8.5zm0 0c3.5-1 6-4 6.5-8.5-2.5 1-5 3.5-6.5 8.5z"/>',
}


def icon(name, size=20, cls=""):
    svg = _line(_UI[name], size)
    if cls:
        svg = svg.replace('class="i"', f'class="i {cls}"', 1)
    return svg


# ---------------------------------------------------------------------------
# Brand mark: corn cob in a rounded square (redrawn from the supplied logo).
# ---------------------------------------------------------------------------
def logo_mark(size=44, cls="logo-mark"):
    return f'''<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 64 64" aria-hidden="true">
<rect width="64" height="64" rx="15" fill="#34C73A"/>
<g stroke="#0E0F0C" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
<path d="M32 8.5c5.6 0 8.8 5.7 8.8 13.4V37c0 4.4-3.9 7.6-8.8 7.6s-8.8-3.2-8.8-7.6V21.9c0-7.7 3.2-13.4 8.8-13.4z" fill="#34C73A"/>
<path d="M32 9v35M28 9.8V43M36 9.8V43M23.6 16.5h16.8M23.2 22h17.6M23.2 27.5h17.6M23.2 33h17.6M23.4 38.5h17.2" stroke-width="1.7"/>
<path d="M32 55.5c-7.6-2.2-13.4-9.4-14.8-20.3 6.3 2.7 11.8 8.9 14.8 20.3z" fill="#34C73A"/>
<path d="M32 55.5c7.6-2.2 13.4-9.4 14.8-20.3-6.3 2.7-11.8 8.9-14.8 20.3z" fill="#34C73A"/>
<path d="M22.5 41.5c2.6 3.4 5.4 7.6 7.4 11.8M41.5 41.5c-2.6 3.4-5.4 7.6-7.4 11.8" stroke-width="1.5"/>
<path d="M29.4 55.4h5.2v2.8a2.6 2.6 0 0 1-5.2 0z" fill="#34C73A"/>
</g></svg>'''


# ---------------------------------------------------------------------------
# AI assistant marks (simplified).
# ---------------------------------------------------------------------------
AI_MARKS = {
    "chatgpt": '''<svg class="ai-mark" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.7">
<ellipse cx="12" cy="12" rx="8.6" ry="4.1"/><ellipse cx="12" cy="12" rx="8.6" ry="4.1" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="8.6" ry="4.1" transform="rotate(120 12 12)"/></g></svg>''',
    "gemini": '''<svg class="ai-mark" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><defs><linearGradient id="gm-g" x1="3" y1="21" x2="21" y2="3" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="#1A73E8"/><stop offset=".55" stop-color="#6C5CE7"/><stop offset="1" stop-color="#E8577E"/></linearGradient></defs>
<path fill="url(#gm-g)" d="M12 1.5c.5 5.6 4.9 10 10.5 10.5-5.6.5-10 4.9-10.5 10.5-.5-5.6-4.9-10-10.5-10.5C7.1 11.5 11.5 7.1 12 1.5z"/></svg>''',
    "perplexity": '''<svg class="ai-mark" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><g fill="none" stroke="#20808D" stroke-width="1.7" stroke-linejoin="round">
<path d="M12 2v20M4.5 3l7.5 6.5L19.5 3v6.5M4.5 3v6.5M3 9.5h18v7.5h-3M3 9.5V17h3"/><path d="M12 9.5 6 15v6l6-5.5M12 9.5l6 5.5v6l-6-5.5"/></g></svg>''',
    "claude": '''<svg class="ai-mark" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><g stroke="#D97757" stroke-width="2.3" stroke-linecap="round">
<path d="M12 12V2.8M12 12l5.6-7.4M12 12l8.8-2.6M12 12l8.4 4M12 12l4.4 8.4M12 12l-1 9.2M12 12l-6.6 6.6M12 12l-9 1.4M12 12 3.6 7.6M12 12 7.2 3.8"/></g></svg>''',
    "google": '''<svg class="ai-mark" viewBox="0 0 48 48" width="20" height="20" aria-hidden="true">
<path fill="#EA4335" d="M24 9.5c3.5 0 6.7 1.2 9.2 3.6l6.9-6.9C35.9 2.4 30.5 0 24 0 14.6 0 6.5 5.4 2.6 13.2l8 6.2C12.4 13.7 17.7 9.5 24 9.5z"/>
<path fill="#4285F4" d="M47 24.5c0-1.6-.1-3.1-.4-4.5H24v9h12.9c-.6 3-2.3 5.5-4.8 7.2l7.7 6c4.5-4.2 7.2-10.4 7.2-17.7z"/>
<path fill="#FBBC05" d="M10.5 28.6c-.5-1.5-.8-3-.8-4.6s.3-3.1.8-4.6l-8-6.2C.9 16.5 0 20.1 0 24s.9 7.5 2.6 10.8z"/>
<path fill="#34A853" d="M24 48c6.5 0 11.9-2.1 15.9-5.8l-7.7-6c-2.2 1.5-4.9 2.3-8.2 2.3-6.3 0-11.6-4.2-13.5-9.9l-8 6.2C6.5 42.6 14.6 48 24 48z"/></svg>''',
}

AIS = [
    ("chatgpt", "ChatGPT"),
    ("gemini", "Gemini"),
    ("perplexity", "Perplexity"),
    ("claude", "Claude"),
    ("google", "Google AI Overviews"),
]
