# Jack in the Box Property Decision Brief

A privacy-first, source-linked GitHub Pages dashboard for deciding whether to sell, renew, or hold a
Jack in the Box NNN-leased property described as being near central Los Angeles, with a reported lease
expiry somewhere in 2030–2035.

**Live site:** <https://wingbangboozle1-lang.github.io/Jack1/>

## The nine published pages

| Page | What it answers |
|---|---|
| [`index.html`](index.html) | Executive summary, the provisional course of action, and the sale-versus-renew test |
| [`market.html`](market.html) | Population, income, rent, employment, long-range forecast and school-lookup limits |
| [`property.html`](property.html) | Blank asset and lease fields, plus issuer-wide SEC context |
| [`decision.html`](decision.html) | Sell, renew and hold paths; after-tax worksheet; wealth-preservation tradeoffs |
| [`projection.html`](projection.html) | Projection system: official SCAG and CPI growth anchors, derivations, and a browser-only rent calculator |
| [`risks.html`](risks.html) | Parcel-dependent hazard, operational, regulatory and tail-risk register |
| [`flagged.html`](flagged.html) | Every material input that could not be verified, with the evidence still required |
| [`verification.html`](verification.html) | Line-by-line re-verification of every published figure against its official source |
| [`sources.html`](sources.html) | Source register, method and limitations |

## What was verified, and how

[`VERIFICATION.md`](VERIFICATION.md) is the audit log. Its key results at the 2026-11-07 pass:

- 29 published figures re-read at their official source: 27 matched exactly, 2 matched with a caveat.
- 0 wrong values and 0 unverified values published.
- 16 official links opened and confirmed; 14 official links **not** re-tested and listed as such rather
  than assumed to work.
- 7 irregularities found, with 5 repaired or resolved and 2 left open and published.

Two of those irregularities were defects committed to this repository and are worth naming:

1. `COORDINATION.md` had been committed with two raw git conflict blocks. Both sides are preserved
   verbatim, in order, with a dated repair note. Nothing was deleted.
2. Eight files in `archive/arena-ffc97e4e/` had been committed with conflict markers, which broke those
   archived pages. Each was resolved to that archive's own side **after** checking that 100% of the other
   side's substantive lines already exist verbatim in `archive/arena-d2137d88/`.

The two "verified with caveat" rows are the CA EDD county labour figures: the cited county profile page
now renders "Data for Los Angeles County not available", so the values were confirmed in EDD's own
December 2025 monthly release, which is now linked beside it.

## Evidence and privacy

No exact address, APN, executed lease, rent schedule, legal tenant or guarantor, debt payoff, appraisal,
condition report, insurance quote, or owner-specific tax or liquidity detail was available for independent
verification. Asset-specific values are left blank and flagged. The brief makes no parcel-level hazard
conclusion, no appraisal, and no definitive sell/renew recommendation, because each of those needs a
document that does not exist in the public record.

The site does not publish or collect owner names, exact property identifiers, ownership entities, lease
documents, or personal financial information. The projection calculator runs entirely in the reader's
browser: inputs are never sent, saved, or logged.

## Local preview and checks

```sh
python3 -m http.server 4173 --bind 0.0.0.0
python3 scripts/build_verification.py   # regenerate VERIFICATION.md + verification.html
python3 scripts/build_projection.py     # regenerate projection.html from official endpoints
python3 scripts/validate_site.py        # structural gate, exit 1 on any violation
```

`validate_site.py` is a consistency gate, not a truth gate. It enforces: all nine pages present; no git
conflict markers in any published file; every table-body row links to an allowlisted official domain;
every intentionally blank cell carries a status badge; all relative links and `#fragments` resolve;
navigation identical on every page and covering every page; no visible email or phone number; one `<h1>`
and a description per page; and `rel="noopener noreferrer"` on new-tab links.

Truth of the figures is enforced by `scripts/build_verification.py`, whose register is hand-checked
against official sources and which generates both the published page and the markdown log from one
source of truth so the two cannot drift.

## GitHub Pages deployment

`.github/workflows/pages.yml` runs on pull requests and on pushes to `main`. The validator job also
re-runs both generators and fails if a generated page no longer matches its register, so no page can be
hand-edited into disagreement with its data. The deploy job publishes only the nine pages above plus
`assets/styles.css`, `assets/site.js` and `.nojekyll`.

Repository Pages settings must use **GitHub Actions** as the build source; the deployment URL is reported
by the Pages workflow after a successful run.

## Repository contents beyond the live site

`pages/`, `site/`, `archive/`, `data/`, `research/`, `analysis/`, `risks/`, `model/`, `tools/` and the root
markdown files are earlier sessions' work, kept for traceability. They are not part of the Pages artifact.
`COORDINATION.md` is the shared task board and carries the full multi-session audit trail.
