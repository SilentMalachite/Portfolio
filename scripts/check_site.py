"""公開ファイルのリンク・パス・メタデータを標準ライブラリだけで検査する。"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import struct
import sys

ROOT = Path(__file__).resolve().parents[1] / "site"
BASE = "https://silentmalachite.github.io/Portfolio/"
REQUIRED = ("index.html", "en/index.html", "404.html", "assets/styles.css", "assets/hero-motion.js", "assets/favicon.svg", "assets/ogp.png", "assets/ogp-en.png")
errors = []


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.refs, self.metadata, self.links = [], [], {}, []
        self.h1 = 0
        self.lang = None
        self.alternates = {}
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "script" and (a.get("src") not in {
            "./assets/hero-motion.js?v=20260911-replay2", "../assets/hero-motion.js?v=20260911-replay2"
        } or "defer" not in a):
            errors.append("Only the deferred local hero replay enhancement is allowed")
        if tag == "img" and ("alt" not in a or not a.get("width") or not a.get("height")):
            errors.append("Images require alt and explicit dimensions")
        if tag == "meta":
            self.metadata[a.get("name", a.get("property"))] = a.get("content", "")
        if tag == "link":
            self.metadata[a.get("rel")] = a.get("href", "")
            if a.get("rel") == "alternate":
                if a.get("hreflang") in self.alternates:
                    errors.append("Duplicate hreflang entry")
                self.alternates[a.get("hreflang")] = a.get("href")
        if tag == "a":
            self.links.append(a.get("href", ""))
        for key in ("href", "src"):
            if key in a:
                self.refs.append(("metadata" if tag == "link" and a.get("rel") in {"canonical", "alternate"} else tag, a[key]))


for relative in REQUIRED:
    if not (ROOT / relative).is_file():
        errors.append(f"Missing public file: {relative}")
pages = {p: Page(p.read_text()) for p in ROOT.rglob("*.html")}
for path, page in pages.items():
    expected_lang = "en" if path.parent == ROOT / "en" else "ja"
    if page.lang != expected_lang:
        errors.append(f"{path.relative_to(ROOT)}: html lang must be {expected_lang}")
    if page.h1 != 1 or len(page.ids) != len(set(page.ids)):
        errors.append(f"{path.name}: requires one h1 and unique IDs")
    for tag, ref in page.refs:
        url = urlsplit(ref)
        if not ref or ref == "#":
            errors.append(f"{path.name}: empty link")
        if url.scheme or url.netloc:
            if url.scheme != "https":
                errors.append(f"{path.name}: unexpected URL scheme: {ref}")
            if tag in ("script", "img", "link"):
                errors.append(f"{path.name}: remote runtime dependency: {ref}")
            continue
        if url.path.startswith("/"):
            errors.append(f"{path.name}: root-relative reference: {ref}")
        target = (path.parent / unquote(url.path)).resolve() if url.path else path.resolve()
        if not target.is_relative_to(ROOT.resolve()) or not target.is_file():
            errors.append(f"{path.name}: missing/escaping target: {ref}")
        if url.fragment and target.suffix == ".html":
            target_page = (pages.get(target) or Page(target.read_text())) if target.is_file() else None
            if target_page and unquote(url.fragment) not in target_page.ids:
                errors.append(f"{path.name}: missing anchor: {ref}")

for relative, locale, image_name, switch in (("index.html", "ja_JP", "ogp.png", "./en/index.html"), ("en/index.html", "en_US", "ogp-en.png", "../index.html")):
    home = pages.get(ROOT / relative)
    if not home:
        continue
    home_url = BASE if relative == "index.html" else BASE + "en/"
    for field in ("description", "viewport", "og:title", "og:description", "og:type"):
        if not home.metadata.get(field):
            errors.append(f"Missing metadata: {field}")
    for field, expected in (("canonical", home_url), ("og:url", home_url), ("og:locale", locale), ("og:image", BASE + "assets/" + image_name)):
        if home.metadata.get(field) != expected:
            errors.append(f"Incorrect metadata: {field}")
    if home.alternates != {"ja": BASE, "en": BASE + "en/", "x-default": BASE}:
        errors.append(f"{relative}: requires reciprocal hreflang metadata")
    if home.links.count(switch) < 2:
        errors.append(f"{relative}: requires header and footer language links")
    if home.links.count("https://silentmalachite.github.io/A11yLab/") < 2:
        errors.append("A11yLab requires direct project and footer links")
    for anchor in ("top", "strengths", "projects", "engineering", "approach", "recruiting"):
        if anchor not in home.ids:
            errors.append(f"Missing section: {anchor}")

not_found = pages.get(ROOT / "404.html")
if not_found and ("noindex" not in not_found.metadata.get("robots", "") or not {BASE, BASE + "en/"}.issubset(not_found.links)):
    errors.append("404 needs noindex and absolute links to both homepages")
japanese, english = pages.get(ROOT / "index.html"), pages.get(ROOT / "en/index.html")
if japanese and english:
    if set(japanese.ids) != set(english.ids):
        errors.append("Language versions must retain the same sections and project anchors")
    external_links = lambda page: {link for link in page.links if link.startswith("https://")}
    if external_links(japanese) != external_links(english):
        errors.append("Language versions must retain the same external project links")
for name in ("ogp.png", "ogp-en.png"):
    png = ROOT / "assets" / name
    if png.is_file() and struct.unpack(">II", png.read_bytes()[16:24]) != (1200, 630):
        errors.append(f"{name}: OGP must be 1200x630")
files = list(ROOT.rglob("*"))
size = sum(p.stat().st_size for p in files if p.is_file())
if size > 1_000_000:
    errors.append("Public directory exceeds conservative 1MB budget")
for p in files:
    if p.is_symlink() or (p.is_file() and p.suffix not in {".html", ".css", ".svg", ".png"} and p != ROOT / "assets/hero-motion.js"):
        errors.append(f"Unexpected public artifact: {p.relative_to(ROOT)}")
if errors:
    print("\n".join(f"FAIL: {error}" for error in errors))
    sys.exit(1)
print(f"PASS: {len(pages)} pages, local links/anchors, metadata, A11yLab links; public files {size:,} bytes")
