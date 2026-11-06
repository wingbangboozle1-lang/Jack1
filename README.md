# Jack in the Box — Central Los Angeles NNN Executive Brief

**Live site:** https://wingbangboozle1-lang.github.io/Jack1/ • **Branches integrated:** `arena/d85fba50-jack1` + `arena/c7b3aeda-jack1` → `main`  
**Property:** Jack in the Box QSR, triple-net (NNN) lease expiring **2030–2035**, Central Los Angeles — **representative site, address withheld**  
**Purpose:** Verified, line-by-line briefing to decide **sell before expiry vs. renew** for wealth preservation + growth at manageable risk.

## Two complementary builds, one repo — both preserved

This repo integrated two autonomous builds that ran in parallel on the same prompt. Both are static, dependency-free, GitHub Pages sites from `main` root — **neither was discarded**.

| Build | Style | Entry point | Strengths | Files |
|---|---|---|---|---|
| **Premium Dashboard** (arena/c7b3aeda-jack1) | Executive briefing, premium UX, premium typography (Fraunces/Inter, copper/sage/navy) | `index.html` | Polished executive summary, 7-factor weighted projection (3.1/5.0), interactive renewal calculator, 30 official sources with vintage, FEMA/USGS/CAL FIRE risk deep-dive | `index.html`, `pages/*.html` (12 pages), `assets/css/style.css`, `assets/js/main.js` |
| **Data-Verified Site** (arena/d85fba50-jack1) | Dataset-first, 358-assertion verifier, research trail | `site/index.html` | Rich JSON dataset (`data/records.json` 1958 rows), black-swan notes, projection engine in rent-multiples, `scripts/build-data.mjs` + `scripts/verify-data.mjs` | `site/*.html`, `data/*.json`, `research/notes/*.md`, `scripts/*.mjs`, `assets/app.js`, `assets/model.js`, `assets/style.css` |

**Start here:** open `index.html` (premium). Then explore `site/index.html` for the alternate dataset view. Both share the same conclusion (sell 2028–31 dual-track).

## Premium Dashboard — What is here

| Path | Purpose |
|---|---|
| `index.html` | Executive summary, bottom-line answer, KPI dashboard, verification ledger |
| `pages/methodology.html` | Projection system — 7-factor weighted, 3 scenarios (base/bull/bear), valuation guardrails |
| `pages/geography.html` | Official boundaries (Central City 2,161 ac), density 8,304/mi² |
| `pages/demographics.html` | City 3.87M (V2025), County 9.85M, DOF vs SCAG divergence flagged |
| `pages/economy.html` | Income $81,939 city / $87,760 county, GDP $818.5B (BEA 2024) |
| `pages/employment.html` | BLS 5.3% MSA (2025), EDD 2022–2032 fastest growers |
| `pages/education.html` | LAUSD 86.7% grad rate (CDE Dashboard 2024) |
| `pages/real-estate.html` | JACK SEC 10-K 2,191 units, B+ market context flagged, NNN prototype |
| `pages/infrastructure.html` | Metro 300M +8%, Downtown Plan capacity, SCAG 4.77M city 2045 |
| `pages/risks.html` | USGS 60% M6.7/30yr, CAL FIRE +29% Very High, FEMA NRI 100.0 $7.6B EAL |
| `pages/decision.html` | Sell vs Renew vs Hold matrix + calculator + 2026–32 action plan |
| `pages/sources.html` | 30 official source rows with URLs & vintage |
| `pages/flagged.html` | 5 flagged items (DOF/SCAG, market cap rates, proxies, blank parcel data) |

## Data-Verified Site (Preserved)

| Path | Purpose |
|---|---|
| `site/index.html` | Dashboard / executive summary (alternate) |
| `site/executive_summary.html`, `site/property_data.html`, `site/risk_analysis.html`, `site/projection_system.html` | Topic deep-dives |
| `data/records.json` | 1958-row dataset the site renders |
| `data/risks.json` | 16-item risk register |
| `data/scenarios.json` | Model scenarios |
| `research/notes/*.md` | Evidence trail: exact figures read from each official page |
| `research/VERIFICATION-LOG.md` | Verification ledger |
| `scripts/build-data.mjs` | Regenerates JSON from reviewed source of truth |
| `scripts/verify-data.mjs` | Build gate: 358 assertions |
| `archive/*` | Prior sub-builds preserved (d2137d88, ffc97e4e) |

## Bottom-line answer (both builds agree)

**Dual-track:** market the asset **2028–2031** (18–30 months before expiry) while negotiating a **10yr+ renewal** in parallel. Whichever yields a contract first preserves wealth. Do not hold to expiry without a signed renewal. Details: `pages/decision.html` + `site/projection_system.html` + `decision.html` (alt).

## Privacy

Personal info **anonymized**. No street address, APN, owner name, rent roll, or tenant sales on the public site. Placeholders: `[REDACTED]` / `[WITHHELD]`. Internal detailed records not committed.

## Verification (Both Builds)

- Every table row links to official `.gov`/`.edu`/agency URL with vintage.
- If a value cannot be confirmed, left **blank** and listed on **Flagged for Review** (`pages/flagged.html` + `flagged.html` / `site/flagged_review.html`).
- Market data (cap rates, broker comps) flagged as *market context — unverified*.
- Irregularity disclosed: **CA DOF projects county decline to 9.73M by 2030; SCAG projects growth to 11.67M by 2045** — both official, different assumptions.
- Premium build: local QA 200 OK; Data-verified build: `node scripts/verify-data.mjs` → `ALL CHECKS PASSED`.

## Official sources (Combined)

Census.gov QuickFacts/ACS/PEP, BEA GDP by County (Feb 5 2026), BLS LAUS/FRED, CA Dept of Finance P-2A, SCAG Connect SoCal, USGS UCERF3, CAL FIRE LRA FHSZ Mar 24 2025, FEMA NRI v1.20, CA Dept of Ed/LAUSD Dashboard, CA EDD LMID, Metro/COO, SEC 10-K Nov 21 2024, plus plainhazard.com/FEMA, EPA, CRS for risks. Full ledgers: `pages/sources.html` + `sources.html` + `research/notes/`.

## Run locally

```bash
python3 -m http.server 8000     # open http://localhost:8000/ (premium)
# then visit http://localhost:8000/site/index.html (alternate)

node scripts/build-data.mjs     # rebuild JSON (data-verified build)
node scripts/verify-data.mjs    # must print ALL CHECKS PASSED
```

Static: no dependencies, no trackers. GitHub Pages serves from `main` root.

## Scope & Limitations

- No parcel address supplied → statistical frame is Los Angeles city/county, not trade area.
- Lease, guaranty, rent, options, insurance not available → decisions conditional, listed as open items U-01 to U-11 (`flagged.html`).
- Projection models express values as multiples of annual rent rather than inventing price.
- Not appraisal, not investment/tax/legal advice.

---

*Integrated on 2026-11-06: preserved both sessions' work without discarding either; conflicts resolved and logged in COORDINATION.md.*

