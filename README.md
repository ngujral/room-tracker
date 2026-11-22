# Registered Accounts Room Tracker

Track TFSA, RRSP and FHSA contribution room for a whole household, across every bank and brokerage.
Installable on iPhone and Android as a web app (PWA). Works offline. No accounts, no server, no tracking —
all data stays in the browser on the user's device.

## Features

- **Room** — per-person room left for TFSA, RRSP and FHSA, with a breakdown by institution and over-contribution warnings
- **Contributions** — log deposits and withdrawals at any institution (with undo)
- **Where should it go?** — rules of thumb for which account suits each kind of investment
- **Key dates** — countdowns to the FHSA year-end, new TFSA room, RRSP deadline and tax filing
- **Backup** — copy / restore all data as text

## Project layout

```
index.html              the whole app (HTML, CSS, JS in one file)
manifest.webmanifest    app name, icons, colours for "Add to Home Screen"
sw.js                   service worker for offline use
_headers                Cloudflare Pages headers
icons/                  app icons (192, 512, maskable, Apple touch)
```

No build step. Open `index.html` through any static server to test locally:

```
python3 -m http.server 8080
```

## Deploy on Cloudflare Pages (free)

1. Push this repo to GitHub.
2. In Cloudflare: **Workers & Pages → Create → Pages → Connect to Git**, pick this repo.
3. Build settings: framework **None**, build command **empty**, output directory **/**.
4. Deploy. The app is live at `https://<project>.pages.dev`. Every push to `main` redeploys.
5. Optional: add a custom domain under **Custom domains**.

## Yearly update (every November/December)

When CRA announces the new limits, edit the constants at the top of the script in `index.html`:

```js
const Y=2026, TFSA_NEXT=7500, RRSP_START='2026-03-03', RRSP_END='2027-03-01', FHSA_YR=8000, FHSA_LIFE=40000;
```

Also update the limits note at the bottom of the page, the `D` (key dates) list, and bump `VERSION` in `sw.js`
so installed copies pick up the change.

> The 2027 TFSA limit (`TFSA_NEXT`) is set to the expected $7,500 — confirm once CRA announces it.

## Disclaimer

General information only, not tax advice. Contribution room should be confirmed with CRA.
