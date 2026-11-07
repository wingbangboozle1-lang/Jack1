# Jack in the Box NNN property — decision brief (central Los Angeles)

A privacy-first, source-linked dashboard that answers one question: **for a Jack in the Box restaurant on a
triple-net lease in central Los Angeles, expiring between 2030 and 2035, should the owner sell before expiry,
renew, hold to expiry, or exchange?**

**Live site:** https://wingbangboozle1-lang.github.io/Jack1/

## Recommendation in one paragraph

Renew, then decide — with a pre-committed sell trigger. Los Angeles County lost 3.2% of its population between
2020 and 2025 and the California Department of Finance projects a further 1.47% decline to 2035 while the state
grows 2.23%. The tenant is contracting: same-store sales fell 4.2% in FY2025, it closed 86 units against 31
openings, it guides another 50–100 closures, it discontinued its dividend, and its own turnaround plan includes
*selling real estate*. In that environment the lease term is the only asset the owner fully controls, and a
renewed asset is worth more than the same asset sold with five years left on it. The recommendation is
conditional on the extension carrying a creditworthy guaranty at a rent no lower than today; if that cannot be
secured by a date set in advance, the asset should be sold. Full reasoning on
[`decision.html`](decision.html) and [`risks.html`](risks.html).

## Pages

| Page | Content |
|---|---|
| [`index.html`](index.html) | Executive summary, six headline indicators, the 90-day action list |
| [`market.html`](market.html) | Population, income, housing, schools, jobs and prices — each row source-linked |
| [`projections.html`](projections.html) | DOF projections to 2035, the projection system, the scenario model and every assumption |
| [`tenant.html`](tenant.html) | Jack in the Box SEC disclosures: counts, sales, closures, guidance, real-estate strategy |
| [`property.html`](property.html) | Lease and parcel fields (withheld or blank) plus catastrophe severity references |
| [`decision.html`](decision.html) | The four paths, net-proceeds arithmetic, tax and capital-market rows, the sell trigger |
| [`risks.html`](risks.html) | 16 risks: business-as-usual, black-swan and personal |
| [`flagged.html`](flagged.html) | Every unverified value, every withheld field, and every source conflict found |
| [`sources.html`](sources.html) | All 29 official sources, the verification rules, and the audit trail |

## Privacy

No owner name, street address, parcel number, ownership entity, rent figure, loan balance, cost basis or
personal financial detail is published, collected or stored in this repository. Those fields render as
`[WITHHELD]`. The site has no forms, no analytics, no cookies and no external requests.

## How the data is verified

Every published figure was read on the cited official page during the build session and reproduced in
[`verification/captures/`](verification/captures). The rules:

- **verified** — the value was displayed on the cited official page and matches. 142 rows.
- **derived** — arithmetic on verified rows; the formula is in the row's note. 4 rows.
- **unverified** — not published by an official source at that geography, so the value is **blank**. 33 rows.
- **withheld** — private by design. 10 rows.

Nothing is estimated, interpolated, carried over from a third-party aggregator, or filled with "approximately".
Where two official sources disagree, both values are published and the conflict is named.

`verification/VERIFICATION-LOG.md` records the check performed for all 189 rows.

## Build and verify locally

```sh
python3 scripts/build_site.py     # regenerate all pages and data/dataset.json from the dataset
python3 scripts/check_site.py     # hard gate: sources, blanks, links, privacy, coverage
python3 -m http.server 4173 --bind 0.0.0.0
```

`scripts/dataset.py` is the single source of truth for every table. `scripts/analysis.py` holds the risk
register, the four decision paths, the model assumptions and the scenario arithmetic. `scripts/check_site.py`
fails the build if any table row lacks an official source link, if any unverified row carries a value, if any
internal link or fragment is broken, if any dataset row is not rendered, or if a privacy pattern is present.

## Deployment

One deploy path only: `.github/workflows/pages.yml` verifies the data, re-runs the generator to prove the
committed pages are reproducible, runs the gate, and publishes to GitHub Pages on `main`. The repository's
Pages source is **GitHub Actions**; a legacy branch build running alongside it is what previously made the
Pages API report `errored`.

## Repository layout

```
index.html … sources.html   generated pages (do not edit by hand)
data/dataset.json           generated machine-readable dataset
scripts/dataset.py          canonical dataset — every table row
scripts/analysis.py         risk register, paths, assumptions, model
scripts/build_site.py       page generator
scripts/check_site.py       verification gate
verification/captures/      reproduced excerpts from each official source
verification/VERIFICATION-LOG.md   row-by-row check log
archive/                    every prior session's build, preserved verbatim
COORDINATION.md             shared task board and session log
```
