#!/usr/bin/env python3
"""
Build a Google Play Books compatible EPUB from markdown.
Uses ebooklib for proper EPUB3 structure.
"""

import re
import os
import markdown
from ebooklib import epub

# ── Config ──────────────────────────────────────────────────────────────────
MD_FILE   = "/Volumes/RAMDisk/Research/Youtube Chanel/book/youtube-cgm-formula.md"
OUT_FILE  = "/Volumes/RAMDisk/Research/Youtube Chanel/book/youtube-cgm-formula.epub"
COVER_IMG = "/Volumes/RAMDisk/Research/Youtube Chanel/book/epub-assets/cover.jpg"

# ── CSS (embedded, Play Books compatible) ────────────────────────────────────
STYLE = """
body {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 100%;
  line-height: 1.75;
  margin: 0;
  padding: 0.5em 1em;
  color: #1a1a1a;
  background: #fff;
}
h1 {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 1.7em;
  font-weight: bold;
  color: #0d1b2a;
  border-bottom: 3px solid #e63946;
  padding-bottom: 0.3em;
  margin: 1.5em 0 0.6em 0;
}
h2 {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 1.25em;
  font-weight: bold;
  color: #1d3557;
  margin: 1.3em 0 0.4em 0;
}
h3 {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 1.05em;
  font-weight: bold;
  color: #457b9d;
  margin: 1em 0 0.3em 0;
}
p {
  margin: 0 0 0.8em 0;
  text-align: justify;
}
blockquote {
  border-left: 4px solid #e63946;
  margin: 0.8em 0;
  padding: 0.4em 0.9em;
  background: #f8f9fa;
  color: #444;
  font-style: italic;
}
ul, ol {
  margin: 0.4em 0 0.8em 1.6em;
  padding: 0;
}
li {
  margin-bottom: 0.35em;
}
strong { color: #c1121f; }
em     { color: #457b9d; }
hr {
  border: none;
  border-top: 1px solid #ddd;
  margin: 1.2em 0;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 0.8em 0;
  font-size: 0.9em;
}
th {
  background: #1d3557;
  color: #fff;
  padding: 0.4em 0.6em;
  text-align: left;
}
td {
  border: 1px solid #ccc;
  padding: 0.35em 0.6em;
}
tr:nth-child(even) td { background: #f5f7f9; }
code {
  font-family: "Courier New", monospace;
  font-size: 0.88em;
  background: #f0f4f8;
  padding: 0.1em 0.3em;
  border-radius: 3px;
}
"""

# ── Helpers ──────────────────────────────────────────────────────────────────
def slugify(text):
    # Transliterate Vietnamese to ASCII
    vn_map = {
        'à':'a','á':'a','â':'a','ã':'a','ả':'a','ạ':'a',
        'ă':'a','ắ':'a','ặ':'a','ằ':'a','ẳ':'a','ẵ':'a',
        'â':'a','ấ':'a','ầ':'a','ẩ':'a','ẫ':'a','ậ':'a',
        'è':'e','é':'e','ê':'e','ẹ':'e','ẻ':'e','ẽ':'e',
        'ế':'e','ề':'e','ệ':'e','ể':'e','ễ':'e',
        'ì':'i','í':'i','ị':'i','ỉ':'i','ĩ':'i',
        'ò':'o','ó':'o','ô':'o','õ':'o','ọ':'o','ỏ':'o',
        'ố':'o','ồ':'o','ộ':'o','ổ':'o','ỗ':'o',
        'ơ':'o','ớ':'o','ờ':'o','ợ':'o','ở':'o','ỡ':'o',
        'ù':'u','ú':'u','ụ':'u','ủ':'u','ũ':'u',
        'ư':'u','ứ':'u','ừ':'u','ự':'u','ử':'u','ữ':'u',
        'ỳ':'y','ý':'y','ỵ':'y','ỷ':'y','ỹ':'y',
        'đ':'d',
        'À':'a','Á':'a','Â':'a','Ã':'a','Ả':'a','Ạ':'a',
        'Ă':'a','Ắ':'a','Ặ':'a','Ằ':'a','Ẳ':'a','Ẵ':'a',
        'È':'e','É':'e','Ê':'e','Ẹ':'e','Ẻ':'e','Ẽ':'e',
        'Ế':'e','Ề':'e','Ệ':'e','Ể':'e','Ễ':'e',
        'Ì':'i','Í':'i','Ị':'i','Ỉ':'i','Ĩ':'i',
        'Ò':'o','Ó':'o','Ô':'o','Õ':'o','Ọ':'o','Ỏ':'o',
        'Ố':'o','Ồ':'o','Ộ':'o','Ổ':'o','Ỗ':'o',
        'Ơ':'o','Ớ':'o','Ờ':'o','Ợ':'o','Ở':'o','Ỡ':'o',
        'Ù':'u','Ú':'u','Ụ':'u','Ủ':'u','Ũ':'u',
        'Ư':'u','Ứ':'u','Ừ':'u','Ự':'u','Ử':'u','Ữ':'u',
        'Ỳ':'y','Ý':'y','Ỵ':'y','Ỷ':'y','Ỹ':'y',
        'Đ':'d',
    }
    result = ''
    for ch in text.lower():
        result += vn_map.get(ch, ch)
    result = re.sub(r'[^a-z0-9\s-]', '', result)
    result = re.sub(r'[\s_-]+', '-', result)
    return result.strip('-')[:50]

def md_to_html(text):
    return markdown.markdown(
        text,
        extensions=['tables', 'fenced_code', 'nl2br', 'sane_lists']
    )

def wrap_html(title, body_html):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="vi" lang="vi">
<head>
  <meta charset="UTF-8"/>
  <title>{title}</title>
</head>
<body>
{body_html}
</body>
</html>"""

# ── Read & strip YAML front matter ───────────────────────────────────────────
with open(MD_FILE, "r", encoding="utf-8") as f:
    raw = f.read()

raw = re.sub(r'^---.*?---\n', '', raw, count=1, flags=re.DOTALL)

# ── Split into chapters on H1 (# ...) ────────────────────────────────────────
parts = re.split(r'^(# .+)$', raw, flags=re.MULTILINE)

chapters = []
if parts[0].strip():
    chapters.append(("Lời mở đầu", parts[0]))

i = 1
while i < len(parts) - 1:
    heading = parts[i].lstrip('#').strip()
    body    = parts[i+1] if i+1 < len(parts) else ""
    chapters.append((heading, parts[i] + body))
    i += 2

print(f"Found {len(chapters)} chapters")

# ── Build EPUB ────────────────────────────────────────────────────────────────
book = epub.EpubBook()

# Metadata
book.set_identifier("cgm-youtube-formula-2026")
book.set_title("Công Thức YouTube Triệu Đô")
book.set_language("vi")
book.add_author("CGM Channel Research")
book.add_metadata('DC', 'description',
    'Hướng dẫn xây dựng kênh YouTube về CGM/đường máu targeting người Mỹ giàu có')
book.add_metadata('DC', 'publisher', 'CGM Research')
book.add_metadata('DC', 'date', '2026')
book.add_metadata('DC', 'rights', 'All rights reserved')

# Cover image
if os.path.exists(COVER_IMG):
    with open(COVER_IMG, "rb") as f:
        cover_data = f.read()
    book.set_cover("cover.jpg", cover_data)
    print("Cover added")

# CSS
style = epub.EpubItem(
    uid="style",
    file_name="style/main.css",
    media_type="text/css",
    content=STYLE.encode("utf-8")
)
book.add_item(style)

# Chapters
epub_chapters = []
spine = ["nav"]

for idx, (title, md_text) in enumerate(chapters):
    slug     = slugify(title) or f"chapter-{idx}"
    filename = f"chapter-{idx:02d}-{slug}.xhtml"

    body_html = md_to_html(md_text)
    html      = wrap_html(title, body_html)

    chapter = epub.EpubHtml(
        title=title,
        file_name=filename,
        lang="vi",
        content=html.encode("utf-8")
    )
    chapter.add_item(style)
    book.add_item(chapter)
    epub_chapters.append(chapter)
    spine.append(chapter)
    print(f"  [{idx+1:02d}] {title[:60]}")

# Navigation
book.toc = tuple(epub_chapters)
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
book.spine = spine

# Write
epub.write_epub(OUT_FILE, book)
size = os.path.getsize(OUT_FILE)
print(f"\n✅ EPUB written: {OUT_FILE}")
print(f"   Size: {size/1024:.1f} KB  |  Chapters: {len(epub_chapters)}")
