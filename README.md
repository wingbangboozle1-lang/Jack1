# Jack in the Box NNN property - decision brief

A privacy-first, source-linked dashboard that answers one question: **for a Jack in the Box property on a
triple-net lease in central Los Angeles, expiring somewhere between 2030 and 2035, should the owner renew or
sell?**

Live site (GitHub Pages): `https://wingbangboozle1-lang.github.io/Jack1/`

## What the brief concludes

**Renew on market terms, hold, and sell only into a priced bid or on a stated trigger.** Do not ride the lease
to expiry, and do not sell against a number nobody has supported. The reasoning, thresholds and arithmetic are on
the site; the short version:

- Remaining term is the asset's main value, and a signed extension raises it.
- The tenant's credit is weakening but intact: systemwide same-store sales -7.4% in Q4 FY2025, 86 closures in the
  year, dividend discontinued - against fiscal 2026 guidance of 2,050-2,100 restaurants, franchise-level margin of
  $275-290m and Adjusted EBITDA of $225-240m.
- The area economy is mild, not collapsing: metropolitan employment +0.5% year over year, county population -3.2%
  since 2020, Los Angeles CPI +3.7%.
- Exit friction is unusually high and has a cliff: 0.45% base city transfer tax plus a 4.0% Measure ULA surcharge
  above $5,400,000 (5.5% at $10,900,000), applied to the whole price. One dollar over the line costs about $216,000.
- At a 6.25% entry capitalisation rate, holding five years beats selling today unless the exit rate widens beyond
  about 6.83%. The model shows the whole surface.

## Pages

| Page | Contents |
|---|---|
| [`index.html`](index.html) | Executive summary, six framing metrics, path comparison, evidence counts |
| [`demographics.html`](demographics.html) | Population, households, income, poverty, housing, travel time |
| [`economy.html`](economy.html) | Employment and sector change, CPI, Treasury yield, regional outlook |
| [`schools.html`](schools.html) | Los Angeles Unified: size, staffing, spending |
| [`property.html`](property.html) | Lease and parcel fields (blank by policy), transfer tax and regulation |
| [`tenant.html`](tenant.html) | Jack in the Box results and guidance from its own filings |
| [`model.html`](model.html) | Value grid, the ULA cliff, hold-versus-sell, break-even exit rate |
| [`decision.html`](decision.html) | Recommendation, five moves, triggers, risk balance, black-swan playbook |
| [`risks.html`](risks.html) | Thirteen registered risks, hazards, insurance gap |
| [`flagged.html`](flagged.html) | Every unverified and withheld row plus eleven recorded irregularities |
| [`sources.html`](sources.html) | The 19 official sources, method, reproduction steps, limits |

## Data and verification

154 published rows: **109 verified**, **4 derived**, **33 unverified** (value blank), **8 withheld** (value blank).
Every verified row links the exact official page it was read from on 2026-11-07. Derived rows state their formula
in the row. A blank is never zero and never an estimate.

- Dataset: `scripts/site_data.py` (single source of truth)
- Build: `python3 scripts/build_site.py` (deterministic; writes all 11 pages, CSS, JS, favicon and
  `data/published-records.json`)
- Gate: `python3 scripts/validate_site.py` (2952 assertions: structure, navigation, link resolution, per-row
  official source links, official-domain allowlist, blank-value rule, no email or phone patterns)

Sources used: U.S. Census Bureau QuickFacts (city and county), BLS Economy at a Glance and the Los Angeles CPI
release, the Federal Reserve H.15 series DGS10 via FRED, SEC EDGAR (Q4/FY2025 earnings release), City of Los
Angeles Office of Finance (transfer tax and Measure ULA), Los Angeles County Assessor (Proposition 13 / 8), the
California Department of Industrial Relations (AB 1228), CAL FIRE and the Office of the State Fire Marshal, the
California Geological Survey (Alquist-Priolo), USGS (ShakeOut), NCES (Los Angeles Unified), the California School
Dashboard, the California Department of Finance, and the IRS (Section 1031).

## Privacy

No owner name, street address, parcel number, ownership entity, lease document, rent, debt, assessed value,
insurance detail or personal financial circumstance appears anywhere in this repository or on the site. Withheld
items are listed on `flagged.html` without values. The site collects nothing: no cookies, no analytics, no
third-party scripts, no forms. The validator fails the build if an email or phone pattern appears.

## Repository layout

```
index.html ... sources.html      published site (generated - do not hand-edit)
assets/                          styles.css, site.js, favicon.svg (generated)
data/published-records.json      machine-readable export of every published row (generated)
scripts/site_data.py             dataset: sources and rows
scripts/build_site.py            the site generator and the model
scripts/validate_site.py         the build gate
archive/                         every prior session's build, preserved intact
COORDINATION.md                  shared task board and session log
EXECUTIVE_SUMMARY.md, DECISION_MEMO.md, RISK_REGISTER.md, METHODOLOGY.md
```

## Licence and status

Analysis for the owner, not appraisal, legal, tax or investment advice. Point-in-time as of 2026-11-07;
re-read the linked official page before relying on a figure.
