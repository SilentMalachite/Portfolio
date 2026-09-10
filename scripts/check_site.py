"""公開ファイルのリンク・パス・メタデータを標準ライブラリだけで検査する。"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import struct
import sys

ROOT = Path(__file__).resolve().parents[1] / "site"
BASE = "https://silentmalachite.github.io/Portfolio/"
REQUIRED = ("index.html", "404.html", "assets/styles.css", "assets/favicon.svg", "assets/ogp.png")
errors = []


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.refs, self.metadata, self.links = [], [], {}, []
        self.h1 = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "html" and a.get("lang") != "ja":
            errors.append("html lang must be ja")
        if tag == "script":
            errors.append("Public pages must work without scripts")
        if tag == "img" and ("alt" not in a or not a.get("width") or not a.get("height")):
            errors.append("Images require alt and explicit dimensions")
        if tag == "meta":
            self.metadata[a.get("name", a.get("property"))] = a.get("content", "")
        if tag == "link":
            self.metadata[a.get("rel")] = a.get("href", "")
        if tag == "a":
            self.links.append(a.get("href", ""))
        for key in ("href", "src"):
            if key in a:
                self.refs.append(("canonical" if tag == "link" and a.get("rel") == "canonical" else tag, a[key]))


for relative in REQUIRED:
    if not (ROOT / relative).is_file():
        errors.append(f"Missing public file: {relative}")
pages = {p: Page(p.read_text()) for p in ROOT.glob("*.html")}
for path, page in pages.items():
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

home = pages.get(ROOT / "index.html")
if home:
    for field in ("description", "viewport", "og:title", "og:description", "og:type"):
        if not home.metadata.get(field):
            errors.append(f"Missing metadata: {field}")
    for field, expected in (("canonical", BASE), ("og:url", BASE), ("og:image", BASE + "assets/ogp.png")):
        if home.metadata.get(field) != expected:
            errors.append(f"Incorrect metadata: {field}")
    if home.links.count("https://silentmalachite.github.io/A11yLab/") < 2:
        errors.append("A11yLab requires direct project and footer links")
    for anchor in ("top", "strengths", "projects", "engineering", "approach", "recruiting"):
        if anchor not in home.ids:
            errors.append(f"Missing section: {anchor}")

not_found = pages.get(ROOT / "404.html")
if not_found and ("noindex" not in not_found.metadata.get("robots", "") or BASE not in not_found.links):
    errors.append("404 needs noindex and absolute homepage link")
png = ROOT / "assets/ogp.png"
if png.is_file() and struct.unpack(">II", png.read_bytes()[16:24]) != (1200, 630):
    errors.append("OGP must be 1200x630")
files = list(ROOT.rglob("*"))
size = sum(p.stat().st_size for p in files if p.is_file())
if size > 1_000_000:
    errors.append("Public directory exceeds conservative 1MB budget")
for p in files:
    if p.is_symlink() or (p.is_file() and p.suffix not in {".html", ".css", ".svg", ".png"}):
        errors.append(f"Unexpected public artifact: {p.relative_to(ROOT)}")
if errors:
    print("\n".join(f"FAIL: {error}" for error in errors))
    sys.exit(1)
print(f"PASS: {len(pages)} pages, local links/anchors, metadata, A11yLab links; public files {size:,} bytes")
