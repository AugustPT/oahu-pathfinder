import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
creds = json.load(open(os.path.join(HERE, "credits.json"), encoding="utf-8"))
lines = [
    "# Photo Credits", "",
    "All photography via [Wikimedia Commons](https://commons.wikimedia.org). Mahalo to the photographers.", "",
    "| Image | Photographer | License | Source |", "|---|---|---|---|",
]
for c in sorted(creds, key=lambda x: x["key"]):
    name = c["file"].replace("File:", "")
    lines.append(f"| images/{c['key']}.jpg | {c['artist']} | {c['license']} | [{name}]({c['url']}) |")
open(os.path.join(HERE, "CREDITS.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("CREDITS.md written")
