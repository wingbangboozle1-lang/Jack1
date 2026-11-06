# Jack in the Box — Central Los Angeles NNN Executive Brief

**Live site:** GitHub Pages (see deployment below) • **Branch:** `arena/c7b3aeda-jack1` → `main`  
**Property:** Jack in the Box QSR, triple-net (NNN) lease expiring **2030–2035**, Central Los Angeles — **representative site, address withheld**  
**Purpose:** Verified, line-by-line briefing to decide **sell before expiry vs. renew** for wealth preservation + growth at manageable risk.

## What this repo contains

A premium static dashboard site (no build step) with 10 subpages organized by category, plus a full verification ledger.

- `index.html` — Executive Summary & Dashboard (bottom-line answer: prepare to market 2028–2031 while negotiating renewal)
- `pages/methodology.html` — Projection system (7-factor weighted, 3 scenarios, auditable)
- `pages/geography.html` — Official boundaries (Central City 2,161 ac), density, neighborhood proxies
- `pages/demographics.html` — City 3.87M (2025), County 9.85M, DOF vs SCAG forecast divergence flagged
- `pages/economy.html` — Income $81,939 city / $87,760 county, GDP $818.5B (BEA 2024)
- `pages/employment.html` — BLS MSA 5.3% (2025), EDD 2022–2032 healthcare-led growth
- `pages/education.html` — LAUSD 86.7% grad rate (CDE Dashboard 2024)
- `pages/real-estate.html` — Tenant JACK (SEC 10-K 2,191 units), B+ market context flagged, NNN prototype
- `pages/infrastructure.html` — Metro 300M boardings +8%, Downtown Plan capacity, transit
- `pages/risks.html` — USGS 60% M6.7/30yr, CAL FIRE +29% Very High, FEMA NRI 100.0 Very High $7.6B EAL
- `pages/decision.html` — Sell vs Renew vs Hold matrix + interactive check + 2026–2032 action plan
- `pages/sources.html` — Every row linked to official URL (Census, BEA, BLS, DOF, SCAG, USGS, CAL FIRE, FEMA, LAUSD, SEC)
- `pages/flagged.html` — Flagged for Review (unverified/market/irregularities)
- `COORDINATION.md` — Task board, session log, verification rules, final checklist
- `assets/css/style.css` — Premium dashboard design system (Inter + Fraunces)

## Privacy

Personal information is **anonymized**. No street address, APN, owner name, rent roll, or tenant sales appear on the public site. Analysis uses **anonymized placeholder** `[REDACTED]` and community-plan-area aggregation. Internal detailed records are not committed.

## Verification

- Every table row has a source link to an official `.gov`/`.edu`/agency site.  
- If a value cannot be confirmed officially, it is left **blank** and listed on **Flagged for Review**.  
- Market data (cap rates, broker comps) is flagged as *market context — unverified* and never drives the base case alone.  
- Irregularity noted: **CA DOF projects county decline to 9.73M by 2030; SCAG projects growth to 11.67M by 2045** — both official, different assumptions, disclosed and weighted as base vs bull case.

## How to run

No build. Open `index.html` locally or serve via any static host:

```bash
python -m http.server 8000
# or
npx serve .
```

GitHub Pages deploys from `main` root (with `.nojekyll`). Enable in repo Settings → Pages: Deploy from branch → `main` / root.

## For reviewers

- Start at `index.html` → `Decision` → `Methodology` → `Risks`.
- Audit any table line via its source link.
- Flagged items do **not** block merge; they are published on a dedicated page for your review.

## Suggested citation

> Jack in the Box NNN — Central Los Angeles Executive Brief. 2026-11-06. Verified sources linked inline. Branch arena/c7b3aeda-jack1 → main.

---

*Not investment, legal, or tax advice. Consult licensed appraiser/CPA/counsel for your entity.*

