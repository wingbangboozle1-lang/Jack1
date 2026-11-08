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
- [`audit.html`](audit.html) — verification ledger: every published figure re-read against its official page on 07–08 Nov 2026, with corrections, source-by-source status, and repository findings

## Evidence and privacy

Line-by-line verification of the published figures, with the figures that could not be confirmed, is recorded in [`research/verification-audit-d18e3065.md`](research/verification-audit-d18e3065.md) and the 08 Nov 2026 follow-up pass in [`research/verification-audit-b8188ee0.md`](research/verification-audit-b8188ee0.md).

No exact address, APN, executed lease, rent schedule, legal tenant or guarantor, debt payoff, appraisal, condition report, insurance quote, or owner-specific tax / liquidity details were available for independent verification. Asset-specific values are left blank and flagged. The brief does not make a parcel-level hazard conclusion, appraisal, or definitive sell / renew recommendation. Public statistics retain their published City of Los Angeles, Los Angeles County, SCAG, or planning geography.

The website intentionally does not publish or collect owner names, exact property identifiers, ownership entities, lease documents, or personal financial information. Official links are provided for manual review; a link to an interactive lookup tool does not mean a property query was completed.

## Local preview and checks

```sh
python3 -m http.server 4173 --bind 0.0.0.0
python3 scripts/validate_site.py
```

The validator checks the eight public pages, required local paths and fragments, unique IDs, official-source links in each table-body row, external-source host allowlisting, new-tab link protections, and visible email / phone patterns.

## GitHub Pages deployment

`.github/workflows/pages.yml` runs the validator for pull requests and publishes the site after changes reach `main` (or on manual workflow dispatch). The workflow explicitly assembles only the eight pages above plus `assets/styles.css`, `assets/site.js`, and `.nojekyll`. Earlier integrated material in `pages/`, `site/`, `data/`, `research/`, and other root pages remains in the repository for traceability but is not part of this dashboard’s deployment artifact.

The workflow is ready to serve as the Pages source, but the repository's Pages setting is currently the legacy **main root** build (switching to GitHub Actions via API returns HTTP 403 with the session token; an admin can change it under Settings → Pages). Both paths publish the same canonical pages; the legacy build additionally serves archived repository files, which contain no personal information. Live site: <https://wingbangboozle1-lang.github.io/Jack1/>.
