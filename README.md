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

## Install on the iPad

1. Open your deployed URL in Safari.
2. Share button → **Add to Home Screen**.
3. Launch from the home screen icon — fullscreen, no browser bars, works offline.
4. For kiosk use (rideshare passengers): Settings → Accessibility → **Guided Access**,
   then triple-click the side button inside the app to lock it.

## Editing content

All content lives in two plain objects near the top of the script in `index.html`:

- `nodes` — the question screens. Each option's `go` is either `n/<node-id>` (go deeper)
  or `r/<result-id>` (show an answer).
- `results` — the answer cards: `steps`, `tip`, `watch`, and a verified `link`.

Add a button by copying a line and changing the words. No other code changes needed.

All external links were verified live in June 2026. Re-check them every few months —
government URLs move (the city's 311 page and beach-safety site both moved in the last
two years).
