# Jack in the Box Property Decision Brief

A privacy-first, source-linked GitHub Pages dashboard for assessing sale, renewal, or hold
scenarios for a Jack in the Box NNN-leased property described as being near central Los Angeles.

Every table row links to the official publisher of the figure on that row. Where a value could
not be read from an official page, the cell is left blank and the item is listed on the
**Flagged for Review** page. Nothing is inferred, estimated, or filled in.

## The published dashboard

Fifteen pages, grouped by category in the sidebar. Each page's tables have a client-side
filter box.

| Page | Contents |
|---|---|
| [`index.html`](index.html) | Executive summary, eight verified indicator cards, decision guardrails |
| [`geography.html`](geography.html) | Land area, density, DTLA 2040 plan expectations, parcel-mismatch caveats |
| [`population.html`](population.html) | Census city and county estimates, households, SCAG population forecast |
| [`income.html`](income.html) | Income, poverty, rent, tenure, home value, retail and food-services sales |
| [`schools.html`](schools.html) | Federal Common Core of Data statistics for Los Angeles Unified |
| [`economy.html`](economy.html) | County GDP, the discontinued metro GDP series, LA-area CPI detail |
| [`jobs.html`](jobs.html) | BLS unemployment rates, Census establishment counts, SCAG employment baseline |
| [`projections.html`](projections.html) | Model inputs, six scenarios, blank outputs, private in-browser calculator |
| [`property.html`](property.html) | Lease and asset diligence checklist — every value blank |
| [`tenant.html`](tenant.html) | Issuer-level SEC figures and what they do not establish |
| [`decision.html`](decision.html) | Sell / renew / hold worksheet, trade-offs, and the risk carried by each path |
| [`risks.html`](risks.html) | Risk register, measured hazards with citations, tail-event scenarios |
| [`flagged.html`](flagged.html) | Seventeen flagged items, including seven corrections made on 08 Nov 2026 |
| [`sources.html`](sources.html) | Every official publisher, what it is used for, and its audit status |
| [`audit.html`](audit.html) | Line-by-line verification ledger and repository findings |

## Evidence and privacy

The full verification ledger for 08 November 2026 is in
[`verification/2026-11-08-81536038.md`](verification/2026-11-08-81536038.md). A prior
independent audit is in `verification/2026-11-07-aa4a9fab.md`.

No exact address, APN, executed lease, rent schedule, legal tenant or guarantor, debt payoff,
appraisal, condition report, insurance quote, or owner-specific tax or liquidity detail was
available for independent verification. Asset-specific values are left blank and flagged. The
brief does not make a parcel-level hazard conclusion, an appraisal, or a definitive sell/renew
recommendation. Public statistics retain their published City of Los Angeles, Los Angeles
County, SCAG, or planning geography.

The website intentionally does not publish or collect owner names, exact property identifiers,
ownership entities, lease documents, or personal financial information. The calculator on the
projection page runs entirely in the browser: no network request, no storage, no logging.
A link to an interactive lookup tool does not mean a property query was completed.

## Building and checking

```sh
python3 scripts/build_pages.py   # regenerate all fifteen pages
python3 scripts/validate_site.py # structural, citation, and privacy checks
python3 -m http.server 4173      # local preview
```

`scripts/build_pages.py` is the single source of truth for page content. It refuses to emit a
table row that does not carry an official-source hyperlink, and it renders blanks through a
dedicated `cell-blank` element so an empty cell can never be read as zero.

`scripts/validate_site.py` checks the fifteen public pages, required local paths and fragments,
unique IDs, an official-source link in every table-body row, an external-host allowlist,
new-tab link protections, and visible email or phone-number patterns.

## GitHub Pages deployment

`.github/workflows/pages.yml` runs the validator for pull requests and publishes the site after
changes reach `main` (or on manual dispatch). It assembles only the fifteen pages above plus
`404.html`, `assets/styles.css`, `assets/site.js`, `assets/favicon.svg`, and `.nojekyll`.
Earlier integrated material in `pages/`, `site/`, `data/`, `research/`, `archive/`, and other
root documents remains in the repository for traceability but is not part of this dashboard's
deployment artifact.

Superseded root pages from earlier builds were moved to `archive/arena-81536038/` rather than
deleted.

## Repository note

This repository has been built on by many parallel sessions and contains several complete,
overlapping site builds under `pages/`, `site/`, and `archive/`. Only the fifteen root pages
described here are deployed. See `COORDINATION.md` for the session task board.
