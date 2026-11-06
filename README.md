# Jack in the Box Property Decision Brief

A privacy-first, source-linked GitHub Pages dashboard for assessing sale, renewal, or hold scenarios for a Jack in the Box NNN-leased property described as being near central Los Angeles.

## Current public dashboard

- [`index.html`](index.html) — executive summary and conditional recommendation
- [`market.html`](market.html) — city / county economics, population, income, jobs, forecasts, and school lookup limits
- [`property.html`](property.html) — blank property and lease fields; issuer-wide SEC context
- [`decision.html`](decision.html) — sell, renew, and hold paths; after-tax worksheet and wealth-preservation tradeoffs
- [`risks.html`](risks.html) — parcel-dependent hazard, operational, regulatory, and tail-risk register
- [`flagged.html`](flagged.html) — explicit review list for every material unverified input
- [`sources.html`](sources.html) — official-source register, method, and limitations

## Evidence and privacy

No exact address, APN, executed lease, rent schedule, legal tenant or guarantor, debt payoff, appraisal, condition report, insurance quote, or owner-specific tax / liquidity details were available for independent verification. Asset-specific values are left blank and flagged. The brief does not make a parcel-level hazard conclusion, appraisal, or definitive sell / renew recommendation. Public statistics retain their published City of Los Angeles, Los Angeles County, SCAG, or planning geography.

The website intentionally does not publish or collect owner names, exact property identifiers, ownership entities, lease documents, or personal financial information. Official links are provided for manual review; a link to an interactive lookup tool does not mean a property query was completed.

## Local preview and checks

```sh
python3 -m http.server 4173 --bind 0.0.0.0
python3 scripts/validate_site.py
```

The validator checks the seven public pages, required local paths and fragments, unique IDs, official-source links in each table-body row, external-source host allowlisting, new-tab link protections, and visible email / phone patterns.

## GitHub Pages deployment

`.github/workflows/pages.yml` runs the validator for pull requests and publishes the site after changes reach `main` (or on manual workflow dispatch). The workflow explicitly assembles only the seven pages above plus `assets/styles.css`, `assets/site.js`, and `.nojekyll`. Earlier integrated material in `pages/`, `site/`, `data/`, `research/`, and other root pages remains in the repository for traceability but is not part of this dashboard’s deployment artifact.

Repository Pages settings must use **GitHub Actions** as the build source. The deployment URL is reported by the Pages workflow after a successful run.
