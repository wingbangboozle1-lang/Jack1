# Jack in the Box NNN Property Decision Brief

A privacy-first, source-linked GitHub Pages dashboard for deciding whether to sell, renew, or hold a Jack in the Box NNN-leased property described as being near central Los Angeles, with a reported lease expiry between 2030 and 2035.

**Live site:** https://wingbangboozle1-lang.github.io/Jack1/

## Published dashboard (11 pages)

| # | Page | What it answers |
|---|---|---|
| 01 | [`index.html`](index.html) | Executive summary, verified indicators, the recommended course of action, the sequence to run, the decision rules, and the gate dates |
| 02 | [`market.html`](market.html) | Population, income, housing, labour, output, official forecasts, and school-lookup limits |
| 03 | [`projection.html`](projection.html) | The projection system: verified drivers, derived growth rates, scenarios, break-even and sensitivity arithmetic |
| 04 | [`property.html`](property.html) | Blank, flagged property and lease fields; issuer-wide SEC lease-structure and financial context |
| 05 | [`decision.html`](decision.html) | Sell, renew, and hold paths; the risk-balanced recommendation; risk by decision; after-tax worksheet |
| 06 | [`risks.html`](risks.html) | Hazard, contract, market, regulatory, and tail-risk register, with county-level official hazard statistics |
| 07 | [`requirements.html`](requirements.html) | Requirement-by-requirement coverage matrix for the brief as issued |
| 08 | [`repo-review.html`](repo-review.html) | Repository findings: competing builds, orphan pages, conflict markers, stale data, deploy-path fixes, privacy scan |
| 09 | [`flagged.html`](flagged.html) | Every material unverified input, with what would close it |
| 10 | [`sources.html`](sources.html) | Official source register, verification rules, and limitations |
| 11 | [`audit.html`](audit.html) | Verification ledger: each figure against its official page, corrections, and irregularities |

## What the brief recommends

Dual-track and evidence-first, with a date attached: obtain the contract and a price while term remains, ask the tenant for an extension at acceptable rent, and compare after-tax net proceeds with risk-adjusted hold value. If no qualifying extension is signed — market rent, ten-plus years beyond 2035, fixed escalations, creditworthy obligor or guaranty, capped landlord obligations, obtainable insurance — the default is to **sell with the lease in place inside the 2027–2029 window**, and never to enter the final 24 months of term with neither a signed renewal nor an active listing.

The reasoning is labelled analyst judgement and kept separate from sourced data: the renewal option belongs to the tenant, and roughly 93% of the brand's restaurants are franchise-operated, so the paying obligor may not be the public company.

## Evidence, verification and privacy

- [`verification/2026-11-08-9dce30d0.md`](verification/2026-11-08-9dce30d0.md) — 23 figure groups re-read at source on 08 Nov 2026; two published contradictions corrected; the FEMA county-declaration gap closed through OpenFEMA.
- [`verification/2026-11-08-14c28bc9.md`](verification/2026-11-08-14c28bc9.md) and [`research/verification-2026-11-08.md`](research/verification-2026-11-08.md) — independent re-verification passes by other sessions.
- [`verification/2026-11-07-aa4a9fab.md`](verification/2026-11-07-aa4a9fab.md) and [`research/verification-audit-d18e3065.md`](research/verification-audit-d18e3065.md) — earlier line-by-line audits.

Every table row in the published pages links an official source. Values that cannot be confirmed are left blank and listed on **Flagged for Review**; nothing is inferred or filled in. No exact address, APN, executed lease, rent schedule, legal tenant or guarantor, debt payoff, appraisal, condition report, insurance quote, or owner-specific tax / liquidity detail is published, collected, or requested.

## Local preview and checks

```sh
python3 -m http.server 4173 --bind 0.0.0.0
python3 scripts/validate_site.py
```

The validator checks the eleven published pages, required local paths and fragments, unique IDs, an official-source link in every evidence row, external-source host allowlisting, new-tab link protections, and visible email / phone patterns.

## Publication scope

There are two publishers, and they now emit the same set:

1. `.github/workflows/pages.yml` — validates every push and pull request, and on `main` uploads an artifact containing the eleven pages, `404.html`, `assets/styles.css`, and `assets/site.js`.
2. The repository's legacy branch build (`build_type: legacy`, source `main` `/`) — which otherwise serves **every** file in the root. `_config.yml` scopes it to the same set, and `.nojekyll` was removed so Jekyll actually runs as the filter. The nine published HTML pages carry no YAML front matter, so they are copied byte-for-byte.

A local simulation of the exclude rules returns exactly 14 files: the eleven pages, `404.html`, `assets/styles.css`, `assets/site.js`.

Material outside the published set (`archive/`, `pages/`, `site/`, `data/`, `research/`, `analysis/`, `verification/`, `tools/`, `scripts/`, and the older root drafts that still carry withdrawn figures) remains in the repository for traceability and is deliberately not published.

**Admin note:** switching Pages → Source to **GitHub Actions** would make the workflow the only publisher; the REST attempt from an integration token returns HTTP 403, so an admin must make that change. Until then `_config.yml` is what keeps superseded dashboards off the live site.
