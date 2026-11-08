# Jack in the Box Property Decision Brief

A privacy-first, source-linked GitHub Pages dashboard for the sell / renew / hold question on a Jack in the Box NNN-leased property described as being near central Los Angeles, with a reported lease expiry between 2030 and 2035.

**Live site:** https://wingbangboozle1-lang.github.io/Jack1/

## The published dashboard (eight pages)

| Page | What it holds |
|---|---|
| [`index.html`](index.html) | Executive summary, verified indicators, and the dated, gate-based recommendation |
| [`market.html`](market.html) | City / county population, income, labour, GDP, official forecasts, and school-lookup limits |
| [`property.html`](property.html) | Blank property and lease fields, plus issuer-wide SEC lease-structure and financial context |
| [`decision.html`](decision.html) | The recommended plan, per-path risk balance, after-tax worksheet, and wealth-preservation tradeoffs |
| [`risks.html`](risks.html) | Parcel-dependent hazards, county-level official hazard statistics, operations, regulation, and tail risk |
| [`flagged.html`](flagged.html) | Every material unverified input, with what would close it |
| [`sources.html`](sources.html) | Official-source register, method, and limitations |
| [`audit.html`](audit.html) | Verification ledger for the 07 Nov and 08 Nov 2026 passes, with defects and corrections |

## What the brief recommends

Dual-track, **sell-weighted**: prepare and price a sale while negotiating a qualifying renewal, and sign nothing until both cases are underwritten. Unless a renewal clears every evidence test on `decision.html` — market rent, ten-plus years beyond 2035, fixed escalations, creditworthy obligor or guaranty, capped landlord obligations, obtainable insurance — the recommendation is to sell with the lease in place inside the **2027–2029** window, before the final 24 months of term. The reasoning is labelled analyst judgement and kept separate from sourced data: the renewal option belongs to the tenant, and the paying obligor may be a franchisee.

## Evidence, verification and privacy

- `verification/2026-11-08-9dce30d0.md` — this session's line-by-line pass: 23 figures re-read on official pages, two published contradictions corrected, one withheld gap closed through FEMA's OpenFEMA API.
- `verification/2026-11-08-14c28bc9.md` and `verification/2026-11-07-aa4a9fab.md` — independent re-verification passes by other sessions.
- `research/verification-audit-d18e3065.md` — the original line-by-line audit.

Every table row in the published pages links an official source. Values that cannot be confirmed are left blank and listed on **Flagged for Review**; nothing is inferred or filled in. No exact address, APN, executed lease, rent schedule, legal tenant or guarantor, debt payoff, appraisal, condition report, insurance quote, or owner-specific tax / liquidity detail is published, collected, or requested.

## Local preview and checks

```sh
python3 -m http.server 4173 --bind 0.0.0.0
python3 scripts/validate_site.py
```

The validator checks the eight public pages, required local paths and fragments, unique IDs, official-source links in each table-body row, external-source host allowlisting, new-tab link protections, and visible email / phone patterns.

## Publication scope

`.github/workflows/pages.yml` validates every push and pull request and, on `main`, publishes an artifact containing only the eight pages, `404.html`, `assets/styles.css`, and `assets/site.js`. `_config.yml` applies the same scope to the repository's legacy branch build, which otherwise serves every file in the repository root — including superseded dashboards from earlier sessions that carry withdrawn figures. Both paths now publish the same clean set.

`data/`, `research/`, `archive/`, `pages/`, `site/`, `analysis/`, `verification/`, and the older root pages remain in the repository for traceability and are intentionally not published.

**Admin note:** the repository's Pages setting is still `build_type: legacy`. Switching Settings → Pages → Source to **GitHub Actions** would make the workflow the only publisher; the REST attempt from an integration token returns HTTP 403. Until an admin changes it, the legacy build runs alongside the deployed artifact, which is why `_config.yml` scoping matters.
