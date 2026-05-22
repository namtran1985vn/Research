#!/usr/bin/env python3
"""
Build a Google Play Books–compatible EPUB from markdown.
Strategy:
  - Use lxml to parse and re-serialise every chapter as clean XHTML
  - Inline CSS in <head> (avoids external-CSS loading issues)
  - Generate EPUB3 with nav=linear:no AND a companion EPUB2
  - ASCII-only filenames, ISO-8601 date, dc:language=vi
"""

import re, os, textwrap
import markdown
from lxml import etree, html as lxhtml
from ebooklib import epub

# ── Paths ────────────────────────────────────────────────────────────────────
BASE    = "/Volumes/RAMDisk/Research/Youtube Chanel/book"
MD_FILE = f"{BASE}/youtube-cgm-formula.md"
OUT3    = f"{BASE}/youtube-cgm-formula.epub"          # EPUB3
OUT2    = f"{BASE}/youtube-cgm-formula-epub2.epub"    # EPUB2 (fallback)
COVER   = f"{BASE}/epub-assets/cover.jpg"

# ── CSS ──────────────────────────────────────────────────────────────────────
STYLE = textwrap.dedent("""\
    body{font-family:serif;font-size:100%;
         line-height:1.8;margin:0;padding:0.5em 1em;color:#111111}
    h1{font-family:sans-serif;font-size:1.6em;font-weight:bold;
       margin:1.4em 0 0.5em 0}
    h2{font-family:sans-serif;font-size:1.2em;font-weight:bold;
       margin:1.2em 0 0.3em 0}
    h3{font-family:sans-serif;font-size:1.05em;font-weight:bold;
       margin:0.9em 0 0.2em 0}
    p{margin:0 0 0.7em 0}
    blockquote{margin:0.7em 1em;padding:0.3em 0.8em;
               border-left:3px solid #888888;font-style:italic}
    ul,ol{margin:0.4em 0 0.7em 1.5em;padding:0}
    li{margin-bottom:0.3em}
    hr{border:none;border-top:1px solid #cccccc;margin:1em 0}
    table{border-collapse:collapse;width:100%;margin:0.7em 0;font-size:0.9em}
    th{background:#333333;color:#ffffff;padding:0.3em 0.5em;text-align:left}
    td{border:1px solid #bbbbbb;padding:0.3em 0.5em}
    code{font-family:monospace;font-size:0.85em}
""")

# ── Helpers ──────────────────────────────────────────────────────────────────
import unicodedata

def slugify(text):
    # Decompose Unicode → strip combining marks → keep ASCII
    t = unicodedata.normalize('NFD', text.lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    # đ/Đ not decomposed by NFD
    t = t.replace('đ', 'd').replace('ð', 'd')
    t = re.sub(r'[^a-z0-9]+', '-', t)
    return t.strip('-')[:48] or 'chapter'

def md_to_xhtml(md_text, title):
    """Convert markdown → clean XHTML body string via lxml."""
    raw_html = markdown.markdown(
        md_text,
        extensions=['tables', 'fenced_code', 'sane_lists']
    )
    # Parse with lxml (tolerant HTML parser), then serialise as XHTML
    frag = lxhtml.fragment_fromstring(raw_html, create_parent='div')
    # Self-closing fix: lxml serialises img/br/hr as <br/> etc. automatically
    body_inner = etree.tostring(frag, encoding='unicode', method='xml')
    # Strip the wrapping <div> tags lxml added
    body_inner = re.sub(r'^<div[^>]*>', '', body_inner)
    body_inner = re.sub(r'</div>$', '', body_inner)
    return body_inner.strip()

def make_xhtml(title, body_inner, css):
    """Wrap body content in a complete, self-contained XHTML document."""
    safe_title = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="vi" lang="vi">\n'
        '<head>\n'
        f'  <meta charset="utf-8"/>\n'
        f'  <title>{safe_title}</title>\n'
        f'  <style type="text/css">\n{css}\n  </style>\n'
        '</head>\n'
        '<body>\n'
        f'{body_inner}\n'
        '</body>\n'
        '</html>'
    )

# ── Parse markdown ────────────────────────────────────────────────────────────
with open(MD_FILE, encoding='utf-8') as f:
    raw = f.read()

raw = re.sub(r'^---.*?---\s*\n', '', raw, count=1, flags=re.DOTALL)

parts = re.split(r'^(# .+)$', raw, flags=re.MULTILINE)
chapters_raw = []
if parts[0].strip():
    chapters_raw.append(('Lời Mở Đầu', parts[0]))
i = 1
while i < len(parts) - 1:
    heading = parts[i].lstrip('#').strip()
    body    = parts[i+1] if i+1 < len(parts) else ''
    chapters_raw.append((heading, parts[i] + body))
    i += 2

print(f"Parsed {len(chapters_raw)} chapters")

# ── Build EPUB3 ───────────────────────────────────────────────────────────────
def build(version, out_path):
    book = epub.EpubBook()
    book.set_identifier(f'cgm-youtube-formula-2026-v{version}')
    book.set_title('Công Thức YouTube Triệu Đô')
    book.set_language('vi')
    book.add_author('CGM Channel Research')
    book.add_metadata('DC', 'description',
        'Hướng dẫn xây dựng kênh YouTube CGM nhắm vào người Mỹ giàu có')
    book.add_metadata('DC', 'publisher', 'CGM Research')
    book.add_metadata('DC', 'date', '2026-01-01')
    book.add_metadata('DC', 'rights', 'All rights reserved')

    # Cover
    if os.path.exists(COVER):
        with open(COVER, 'rb') as f:
            book.set_cover('cover.jpg', f.read())

    # Chapters
    epub_chaps = []
    for idx, (title, md_text) in enumerate(chapters_raw):
        slug     = slugify(title)
        filename = f'ch{idx:02d}-{slug}.xhtml'
        body     = md_to_xhtml(md_text, title)
        xhtml    = make_xhtml(title, body, STYLE)

        ch = epub.EpubHtml(title=title, file_name=filename, lang='vi')
        ch.set_content(xhtml.encode('utf-8'))
        book.add_item(ch)
        epub_chaps.append(ch)
        print(f'  [{idx+1:02d}] {title[:58]}')

    # NCX + NAV
    book.add_item(epub.EpubNcx())
    nav = epub.EpubNav()
    book.add_item(nav)

    # TOC
    book.toc = tuple(epub_chaps)

    # Spine: nav hidden, then chapters
    book.spine = [('nav', 'no')] + epub_chaps

    # EPUB guide (EPUB2 compatibility)
    book.guide = [
        {'type': 'toc',   'href': 'nav.xhtml',          'title': 'Mục Lục'},
        {'type': 'text',  'href': epub_chaps[0].file_name, 'title': 'Bắt Đầu'},
    ]

    epub.write_epub(out_path, book)
    size = os.path.getsize(out_path) / 1024
    print(f'\n✅ EPUB{version} → {out_path}')
    print(f'   {size:.1f} KB  |  {len(epub_chaps)} chapters')

# Build both versions
print('\n── Building EPUB3 ──────────────────────────────────────')
build(3, OUT3)

print('\n── Building EPUB2 (fallback) ───────────────────────────')
build(2, OUT2)
