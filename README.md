# Jack1 — Project Jack-in-the-Box (NNN Lease Analysis)

Decision-support analysis for a **single-tenant, triple-net (NNN) Jack in the Box restaurant in Central Los Angeles**, lease expiry window **2030–2035**: sell before expiry vs. renew.

**Live site:** https://wingbangboozle1-lang.github.io/Jack1/ (GitHub Pages)

## What this repo contains
- A static, dependency-free dashboard site (HTML/CSS/vanilla JS) at the repo root:
  `index.html` (dashboard) + subpages: `executive-summary.html`, `property.html`, `market.html`, `economy.html`, `tenant.html`, `projections.html` (interactive NPV/cap-rate model), `risk.html`, `decision.html`, `sources.html`, `flagged.html`.
- `COORDINATION.md` — parallel-session task board and verification log.
- This README.

## Privacy
No personal information appears in this repository or the site. The owner is "the Owner"; the property address is withheld by design; all location analysis is city/county-level. Any personal information encountered in research was excluded.

## Verification standard
Every table row carries a source link (official/primary preferred; industry sources labeled). Values not confirmable from an official source are left blank and flagged (⚑) on `flagged.html` — never estimated or inferred.

## Not advice
This is an analytical work product, not financial, legal, accounting, or tax advice. Engage a licensed CA broker, CPA, attorney, and 1031 qualified intermediary before acting.

## Build / deploy
Static site — no build step. Served by GitHub Pages from the `main` branch (root). Local check: `python3 -m http.server 8080` then open `http://127.0.0.1:8080`.
