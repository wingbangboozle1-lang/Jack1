# Jack in the Box NNN — Central Los Angeles · hold / renew / exit analysis

A single-page-per-category analytical site for one decision: **sell a single-tenant Jack in the Box net-lease asset
before its 2030–2035 expiry, or renew it?** Built entirely from official public sources; every figure links to the page
it was read on, and anything that could not be confirmed is left blank and published on a Flagged for Review page.

**Live site:** https://wingbangboozle1-lang.github.io/Jack1/

## What is here

| Path | Purpose |
|---|---|
| `index.html` | Executive summary, recommendation, KPI dashboard, build integrity |
| `market.html` | Census demographics, income, housing, DOF population projections to 2035 |
| `economy.html` | BLS employment and sector trends, CPI, Treasury yields |
| `schools.html` | NCES data for Los Angeles Unified, human capital |
| `tenant.html` | Jack in the Box FY2025 filings (SEC), lease mechanics, withheld property fields |
| `risk.html` | 16-item risk register: business-as-usual and black swans |
| `model.html` | Projection engine — hold vs. sell vs. renew-then-sell, in units of annual rent |
| `decision.html` | Recommendation, decision rules, timeline, wealth-preservation and black-swan playbooks |
| `flagged.html` | Every unverified value, every withheld field, every source irregularity |
| `sources.html` | Source registry, methodology, verification log, glossary |
| `data/*.json` | The dataset the site renders (records, risks, model scenarios) |
| `research/notes/*.md` | Evidence trail: the exact figures read from each official page |
| `scripts/build-data.mjs` | Regenerates `data/*.json` from one reviewed source of truth |
| `scripts/verify-data.mjs` | Build gate: 358 assertions (schema, blank-value rule, official-domain allowlist, internal links) |

## Rules the build enforces

1. A value may appear only if it was read on the cited official page. `scripts/verify-data.mjs` **fails the build** if an
   `unverified` row contains a number.
2. Every source must be https and on the official-domain allowlist (Census, BLS, CA DOF, CA DIR, CGS, CAL FIRE/OSFM,
   CA Department of Insurance, LA County Assessor, City of LA, NCES, SEC, FRB St. Louis).
3. Every derived percentage must state its arithmetic in the row note.
4. No personal information is published. Address, APN, owner, rent and lease dates appear only as `[WITHHELD]`.

## Run it locally

```bash
python3 -m http.server 8000     # then open http://localhost:8000
node scripts/build-data.mjs     # rebuild JSON from the reviewed data
node scripts/verify-data.mjs    # must print "ALL CHECKS PASSED"
```

Static site: no build step, no dependencies, no trackers, no cookies. GitHub Pages serves it from `main` at the repo root.

## Scope and limitations

- No parcel address was supplied, so the statistical frame is **Los Angeles city and County**, not a three-mile trade area.
- The lease, guaranty, rent, configured options and insurance policy were not available; those decisions are conditional
  and are listed as open items U-01 to U-11.
- The projection model expresses values as **multiples of one year of base rent** rather than inventing a dollar value.
- This is analytical work product, not an appraisal, not investment advice, and not tax or legal advice.

## Prior builds (preserved, not deployed as navigation)

Two earlier sessions built complete sites for this same question. Both are preserved intact for provenance and comparison:

- `archive/arena-d2137d88/` — the previous canonical 12-page site plus its 92-row `assets/js/data.js` registry
- `archive/arena-ffc97e4e/` — an independent parallel build (11 pages, port/wildfire/forecast tables)

Nothing from either was deleted. Their unique research remains in the repository; the root site is the build that carries a
per-row source link and an enforced blank-value gate.

## Coordination

`COORDINATION.md` is the shared task board (claims, scope, handoffs, merge record) used while this repository is worked on.
