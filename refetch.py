"""Refetch specific images with better search terms: refetch.py key 'search term' [key 'term' ...]"""
import sys, importlib.util, os
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("fi", os.path.join(HERE, "fetch_images.py"))
# reuse the helpers without rerunning everything: copy of minimal logic instead
import io, json, re
import requests
from PIL import Image

UA = {"User-Agent": "OahuPathfinder/1.0 (August@kindcodex.com)"}
API = "https://commons.wikimedia.org/w/api.php"
OUT = os.path.join(HERE, "images")

def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()

args = sys.argv[1:]
pairs = list(zip(args[::2], args[1::2]))
creds = json.load(open(os.path.join(HERE, "credits.json"), encoding="utf-8"))

for key, term in pairs:
    r = requests.get(API, headers=UA, timeout=30, params={
        "action": "query", "generator": "search",
        "gsrsearch": term, "gsrnamespace": 6, "gsrlimit": 10,
        "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": 1400, "format": "json",
    })
    pages = (r.json().get("query") or {}).get("pages") or {}
    best = None
    for p in sorted(pages.values(), key=lambda x: x.get("index", 99)):
        ii = (p.get("imageinfo") or [None])[0]
        if not ii or ii.get("mime") != "image/jpeg": continue
        w, h = ii.get("width", 0), ii.get("height", 0)
        if w < 1000 or h < 600 or w <= h: continue
        best = (p, ii); break
    if not best:
        print(f"MISS {key}: '{term}'"); continue
    p, ii = best
    img = requests.get(ii.get("thumburl") or ii["url"], headers=UA, timeout=60).content
    im = Image.open(io.BytesIO(img)).convert("RGB")
    if im.width > 1200:
        im = im.resize((1200, int(im.height * 1200 / im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, f"{key}.jpg"), "JPEG", quality=72, optimize=True)
    meta = ii.get("extmetadata") or {}
    entry = {"key": key, "file": p.get("title", ""),
             "artist": strip_tags((meta.get("Artist") or {}).get("value")),
             "license": (meta.get("LicenseShortName") or {}).get("value", ""),
             "url": ii.get("descriptionurl", "")}
    creds = [c for c in creds if c["key"] != key] + [entry]
    print(f"OK   {key}: {entry['file']} [{entry['license']}]")

json.dump(creds, open(os.path.join(HERE, "credits.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
