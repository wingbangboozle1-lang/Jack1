# Jack in the Box NNN Property Decision Brief

A privacy-first, source-linked GitHub Pages dashboard for deciding whether to sell, renew, or hold a Jack in the Box NNN-leased property described as being near central Los Angeles, with a reported lease expiry between 2030 and 2035.

## Published dashboard (11 pages)

| # | Page | What it answers |
|---|---|---|
| 01 | [`index.html`](index.html) | Executive summary, the recommended course of action, the sequence to run, and the decision rules |
| 02 | [`market.html`](market.html) | Population, income, housing, labour, output, prices, rates, wage floors, and planning context |
| 03 | [`projection.html`](projection.html) | The projection system: verified drivers, derived growth rates, three scenarios, break-even and sensitivity arithmetic |
| 04 | [`property.html`](property.html) | Blank, flagged property and lease fields; issuer-wide SEC context |
| 05 | [`decision.html`](decision.html) | Sell, renew, and hold paths; ranked action; risk by decision; after-tax worksheet |
| 06 | [`risks.html`](risks.html) | Hazard, contract, market, regulatory, and tail-risk register, including the January 2025 fire record |
| 07 | [`requirements.html`](requirements.html) | Requirement-by-requirement coverage matrix for the brief as issued |
| 08 | [`repo-review.html`](repo-review.html) | Repository findings: competing builds, orphan pages, conflict markers, stale data, deploy-path fixes, privacy scan |
| 09 | [`flagged.html`](flagged.html) | Every material unverified input, with the document or official link that would close it |
| 10 | [`sources.html`](sources.html) | Official source register, verification rules, and limitations |
| 11 | [`audit.html`](audit.html) | Verification ledger: each figure against its official page, corrections, and irregularities |

## Evidence and privacy

Line-by-line verification records live in [`research/verification-2026-11-08.md`](research/verification-2026-11-08.md) (current pass) and [`research/verification-audit-d18e3065.md`](research/verification-audit-d18e3065.md) (07 Nov 2026 pass). Repository integrity findings are recorded in [`research/repo-review-2026-11-08.md`](research/repo-review-2026-11-08.md).

No exact address, APN, executed lease, rent schedule, legal tenant or guarantor identity, debt payoff, appraisal, condition report, insurance quote, or owner-specific tax or liquidity detail was available for independent verification. Asset-specific values are blank and flagged. The brief does not make a parcel-level hazard conclusion, an appraisal, or a dollar-value sell/renew verdict; it does give a ranked course of action with explicit triggers.

The website does not publish or collect owner names, exact property identifiers, ownership entities, lease documents, or personal financial information. Official links are provided for manual review; a link to an interactive lookup tool does not mean a property query was completed.

## Local preview and checks

```sh
python3 -m http.server 4173 --bind 0.0.0.0
python3 scripts/validate_site.py
```

The validator checks the eleven published pages, required local paths and fragments, unique IDs, an official-source link in every evidence-row of a table body, a working link in every narrative-table row, external-host allowlisting, new-tab link protections, and visible email / phone patterns.

## GitHub Pages deployment

`.github/workflows/pages.yml` validates on pull requests and publishes exactly the eleven pages above plus `assets/styles.css`, `assets/site.js`, and `.nojekyll`.

The workflow stages a strict allowlist and publishes it on every push to `main`.

**Known open defect:** the repository's Pages source is currently the branch itself (`build_type: legacy`), so the branch build also publishes the whole repository — including archived drafts that contain unresolved merge markers — and races the workflow. Switching the source to **GitHub Actions** requires repository-admin rights and is the one-line settings change that closes the defect. It is logged as RR-04/RR-05 on the Repo Review page.

Material not in the published artifact (`archive/`, `pages/`, `site/`, `data/`, `research/`, and the five superseded root drafts) remains in the repository for traceability and is documented on the Repo Review page.
