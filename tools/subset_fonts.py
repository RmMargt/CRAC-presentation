#!/usr/bin/env python3
"""Subset the deck's webfonts down to the glyphs it actually uses."""
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = os.path.join(ROOT, ".fontcache")
DECK = os.path.join(ROOT, "dist", "index.html")
OUT = os.path.join(ROOT, "dist", "fonts")
os.makedirs(OUT, exist_ok=True)
os.makedirs(SCRATCH, exist_ok=True)

UA = "Mozilla/5.0"
GF = "https://fonts.googleapis.com/css2?family=%s:wght@%d"


def ensure_ttf(family, weight):
    """Download the full TTF once and cache it; Google serves TTF to a plain UA."""
    path = os.path.join(SCRATCH, "%s-%d.ttf" % (family, weight))
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        return path
    import urllib.request
    css_url = GF % (family.replace("NotoSansSC", "Noto+Sans+SC"), weight)
    req = urllib.request.Request(css_url, headers={"User-Agent": UA})
    css = urllib.request.urlopen(req, timeout=30).read().decode()
    url = re.search(r"https://[^)]*\.ttf", css).group(0)
    with urllib.request.urlopen(url, timeout=120) as r, open(path, "wb") as f:
        f.write(r.read())
    return path

src = open(DECK, encoding="utf-8").read()
# Everything the deck can display: slide text, speaker notes (drawer), HUD chrome.
text = re.sub(r"<style.*?</style>", " ", src, flags=re.S)
text = re.sub(r"<(script|svg).*?</\1>", " ", text, flags=re.S)
text = re.sub(r"<[^>]+>", " ", text)
import html as _h
text = _h.unescape(text)
# Speaker notes live in a JS array; pull them back out of the raw source too.
text += "".join(re.findall(r'data-speaker-notes="([^"]*)"', src))
text += _h.unescape("".join(re.findall(r'"([^"]*)"', src.split("var NOTES")[1].split("</script>")[0]))) \
    if "var NOTES" in src else ""

chars = set(text)
chars |= set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
chars |= set(" ．，。、；：？！（）「」『』《》〈〉—…·“”‘’%+-/×÷=<>#&@*·•→←↑↓")
chars |= set(".,;:?!()[]{}'\"`~^_|\\$")
chars -= {c for c in chars if ord(c) < 0x20}
unicodes = ",".join("U+%04X" % ord(c) for c in sorted(chars))
print("unique glyphs:", len(chars))

jobs = [("NotoSansSC", w) for w in (400, 500, 700, 900)] + [("Barlow", w) for w in (500, 600, 700)]
faces = []
for fam, w in jobs:
    ttf = ensure_ttf(fam, w)
    out = os.path.join(OUT, "%s-%d.woff2" % (fam, w))
    subprocess.run([
        "pyftsubset", ttf,
        "--unicodes=%s" % unicodes,
        "--layout-features=kern,liga,calt,tnum",
        "--flavor=woff2", "--output-file=%s" % out,
        "--no-hinting", "--desubroutinize", "--drop-tables+=DSIG",
    ], check=True)
    name = "Noto Sans SC" if fam == "NotoSansSC" else "Barlow"
    faces.append((name, w, os.path.basename(out)))
    print("  %-22s %7.0f KB -> %6.1f KB" % (
        os.path.basename(out), os.path.getsize(ttf) / 1024, os.path.getsize(out) / 1024))

css = "\n".join(
    "@font-face{font-family:'%s';font-style:normal;font-weight:%d;font-display:swap;"
    "src:url(%s) format('woff2');}" % (n, w, f) for n, w, f in faces)
open(os.path.join(OUT, "fonts.css"), "w", encoding="utf-8").write(css)
print("total woff2: %.1f MB" % (sum(
    os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT) if f.endswith(".woff2")) / 1024 / 1024))
