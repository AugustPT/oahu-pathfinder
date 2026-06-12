"""Fetch CC-licensed Oahu photos from Wikimedia Commons, resize, and build credits."""
import io, json, os, re, sys
import requests
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images")
os.makedirs(OUT, exist_ok=True)

UA = {"User-Agent": "OahuPathfinder/1.0 (August@kindcodex.com)"}
API = "https://commons.wikimedia.org/w/api.php"

SUBJECTS = {
    "bg":          "Waikiki Beach Diamond Head panorama",
    "diamondhead": "Diamond Head crater Honolulu",
    "northshore":  "Waimea Bay Oahu",
    "lanikai":     "Lanikai Beach",
    "hanauma":     "Hanauma Bay",
    "food":        "Hawaiian plate lunch",
    "shaveice":    "Shave ice Hawaii",
    "hike":        "Manoa Falls trail",
    "thebus":      "TheBus Honolulu bus",
    "skyline":     "Honolulu skyline aerial",
    "pearlharbor": "USS Arizona Memorial",
    "hibiscus":    "Hibiscus flower Hawaii",
    "sunset":      "Waikiki sunset beach",
    "kailua":      "Kailua Beach Oahu",
}

def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()

def pick(pages):
    best = None
    for p in sorted(pages.values(), key=lambda x: x.get("index", 99)):
        ii = (p.get("imageinfo") or [None])[0]
        if not ii: continue
        if ii.get("mime") != "image/jpeg": continue
        w, h = ii.get("width", 0), ii.get("height", 0)
        if w < 1000 or h < 600: continue
        landscape = w > h
        if best is None or (landscape and not best[1]):
            best = (p, landscape, ii)
            if landscape: break
    return best

credits = []
for key, term in SUBJECTS.items():
    try:
        r = requests.get(API, headers=UA, timeout=30, params={
            "action": "query", "generator": "search",
            "gsrsearch": term, "gsrnamespace": 6, "gsrlimit": 10,
            "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata",
            "iiurlwidth": 1400, "format": "json",
        })
        pages = (r.json().get("query") or {}).get("pages") or {}
        choice = pick(pages)
        if not choice:
            print(f"MISS  {key}: no suitable image for '{term}'")
            continue
        p, _, ii = choice
        url = ii.get("thumburl") or ii["url"]
        img_bytes = requests.get(url, headers=UA, timeout=60).content
        im = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        if im.width > 1200:
            im = im.resize((1200, int(im.height * 1200 / im.width)), Image.LANCZOS)
        path = os.path.join(OUT, f"{key}.jpg")
        im.save(path, "JPEG", quality=72, optimize=True)
        meta = ii.get("extmetadata") or {}
        credits.append({
            "key": key,
            "file": p.get("title", ""),
            "artist": strip_tags((meta.get("Artist") or {}).get("value")),
            "license": (meta.get("LicenseShortName") or {}).get("value", ""),
            "url": ii.get("descriptionurl", ""),
        })
        print(f"OK    {key}: {p.get('title','')} [{(meta.get('LicenseShortName') or {}).get('value','')}] {os.path.getsize(path)//1024}KB")
    except Exception as e:
        print(f"ERROR {key}: {e}")

with open(os.path.join(HERE, "credits.json"), "w", encoding="utf-8") as f:
    json.dump(credits, f, indent=2, ensure_ascii=False)

# contact sheet for visual review
files = [f for f in sorted(os.listdir(OUT)) if f.endswith(".jpg")]
if files:
    cols, cell_w, cell_h, label_h = 4, 300, 200, 24
    rows = (len(files) + cols - 1) // cols
    from PIL import ImageDraw
    sheet = Image.new("RGB", (cols * cell_w, rows * (cell_h + label_h)), "white")
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        im = Image.open(os.path.join(OUT, f)).convert("RGB")
        im.thumbnail((cell_w, cell_h))
        x = (i % cols) * cell_w
        y = (i // cols) * (cell_h + label_h)
        sheet.paste(im, (x + (cell_w - im.width) // 2, y))
        d.text((x + 8, y + cell_h + 4), f, fill="black")
    sheet.save(os.path.join(HERE, "contact-sheet.jpg"), "JPEG", quality=80)
    print(f"sheet: contact-sheet.jpg ({len(files)} images)")
