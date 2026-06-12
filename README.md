# Oʻahu Pathfinder

A guided "what should I do next on Oʻahu?" app for tourists, business owners, and locals.
Single-page PWA — no build step, no framework, no backend.

## Files

| File | Purpose |
|---|---|
| `index.html` | The entire app — UI, content, and router in one file |
| `sw.js` | Service worker — makes the app work fully offline |
| `manifest.webmanifest` | PWA manifest — name, icons, fullscreen install |
| `icon-512.png`, `icon-192.png`, `apple-touch-icon.png` | App icons (regenerate with `build-icons.ps1`) |
| `build-icons.ps1` | Regenerates the icon PNGs (Windows PowerShell) |
| `images/` | Photography (Wikimedia Commons, see `CREDITS.md`) |
| `fetch_images.py`, `refetch.py`, `make_credits.py` | Tooling that downloads/refreshes the photos and credits |
| `CREDITS.md`, `credits.json` | Photo attribution (required by the CC licenses) |

## Before you ship

1. Open `index.html`, find the `CONFIG` block near the top of the `<script>`, and set
   `ownerName` (and tweak `ownerPitch`) — this appears on every screen's footer.
2. When you change `index.html`, bump the version in `sw.js` (`oahu-pathfinder-v1.0.0` →
   `v1.0.1`) so installed devices pick up the update.

## Deploy (pick one, both free)

**Netlify Drop (fastest):** go to <https://app.netlify.com/drop> and drag this whole
folder onto the page. You get an HTTPS URL immediately.

**GitHub Pages:** push this folder to a GitHub repo → Settings → Pages → deploy from
branch `main`, root folder.

HTTPS hosting is required for the service worker (offline mode) — both options above
provide it automatically.

## Kiosk mode (locked tablet / rideshare / lobby)

**Triple-tap the logo** to toggle kiosk mode on or off (it persists on the device). While ON:

- Tapping any external link or email shows a **QR code** instead of opening it — the
  passenger scans it with their own phone, and the tablet never leaves the app.
- The session **auto-resets to Home after 2 minutes idle** (saved items cleared), so the
  next passenger starts fresh. A **🔄 Start over** button also appears in the header.
- Long-press menus, text selection, and pinch-zoom are blocked.
- The app asks the screen to stay awake (works on iOS 16.4+ over HTTPS).

Tablet setup checklist for kiosk use:

1. Settings → Display & Brightness → Auto-Lock → **Never**
2. Settings → Accessibility → **Guided Access** → on, set a passcode
3. Open the app from the home screen icon, triple-tap the logo (kiosk ON)
4. Triple-click the side/top button → **Start** Guided Access

## Install on the iPad

1. Open your deployed URL in Safari.
2. Share button → **Add to Home Screen**.
3. Launch from the home screen icon — fullscreen, no browser bars, works offline.
4. For kiosk use (rideshare passengers): Settings → Accessibility → **Guided Access**,
   then triple-click the side button inside the app to lock it.

## White-label hotel editions

`hotel/` is a demo property edition — **Mauka Lani Beach Hotel** (fictional) — showing
how the engine white-labels as a hotel concierge: hotel essentials (WiFi, breakfast,
pool, checkout, parking), the hotel's partner picks with guest perks, and the full
island guide underneath. All `tel:` and partner details in it are demo data.

To spin up a new property:

1. Copy the `hotel/` folder (e.g. to `surfjack/`).
2. Edit the marked blocks at the top of its `index.html`: the `<title>`, `<h1>`,
   tagline, and the `HOTEL LAYER` sections in `nodes` and `results` (front-desk phone,
   hours, partner picks).
3. Add the new folder's files to `ASSETS` in `sw.js` and bump the cache version.
4. Push. The property lives at `/<folder>/` on the same site.

Pitch tip: make a prospect's edition *before* the meeting — it takes minutes.

### Live property editions

| Property | Path | Notes |
|---|---|---|
| Mauka Lani (fictional demo) | `/hotel/` | All data is demo placeholder |
| White Sands Hotel | `/whitesands/` | Venues verified on whitesandshotel.com |
| The Surfjack Hotel & Swim Club | `/surfjack/` | Content verified on surfjack.com |
| Marina Hawaii Vacations | `/marina/` | Buildings/phones verified on marinahawaiivacations.com |

**Confirm before launch (with each property):** hours, prices, parking rates/options,
housekeeping fees, after-hours procedures, and dog rules. White Sands specifically:
the surf school / yacht charter / Roberts Hawaii shuttle partnerships from the design
brief are NOT on their website and were left out — confirm with the hotel and add them
only if real. These pages are unsolicited pitch demos until a property signs off —
get their approval before printing QR cards or putting a tablet in their lobby.

## Editing content

All content lives in two plain objects near the top of the script in `index.html`:

- `nodes` — the question screens. Each option's `go` is either `n/<node-id>` (go deeper)
  or `r/<result-id>` (show an answer).
- `results` — the answer cards: `steps`, `tip`, `watch`, and a verified `link`.

Add a button by copying a line and changing the words. No other code changes needed.

All external links were verified live in June 2026. Re-check them every few months —
government URLs move (the city's 311 page and beach-safety site both moved in the last
two years).
