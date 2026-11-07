# Jack in the Box NNN lease decision brief

A privacy-first, source-verified decision project for an **anonymized** Jack in the Box
NNN-leased property around central Los Angeles with a reported lease expiry in the
2030–2035 window. Core question: **sell before expiry, or renew/hold?**

**Live site:** <https://wingbangboozle1-lang.github.io/Jack1/>

## What is published

A clean dashboard landing page (`index.html`) and 18 category/governance subpages:

| Group | Pages |
| --- | --- |
| Overview | `index.html`, `decision.html`, `projection.html` |
| Property & tenant | `property.html`, `tenant.html` |
| Area economy | `market.html`, `geography.html`, `demographics.html`, `income.html`, `employment.html`, `schools.html`, `economy.html` |
| Risk & rules | `hazards.html`, `regulatory.html`, `risks.html` |
| Governance | `sources.html`, `flagged.html`, `privacy.html`, `scope.html` |

`model.html` and `risk.html` are preserved aliases of `projection.html` and `risks.html`.
`404.html`, `robots.txt` and `sitemap.xml` complete the published set.

Every table row links to an official publisher. **315 line-by-line entries**: **229 verified**
values and **86 deliberately blank, flagged** values. A value that cannot be confirmed from an
official source is never inferred, estimated or filled. The clearly labelled
[`flagged.html`](flagged.html) page publishes all 86 blanks and all 17 irregularities
(IR-D1 … IR-D17). `sources.html` is the manual-review register of 59 official sources.

**Recommendation (decision rule, not a property-specific verdict):** hold and secure a longer
signed renewal now, with a hard pre-committed sell trigger; do not sell immediately and do not
wait passively to expiry. The binding risk is tenant-side contraction, not a collapsing local
economy. The address, APN, lease, rent, guarantor, debt, appraisal and owner tax profile were
withheld, so no property-specific sale/renew price can be honestly computed.

## Privacy

No owner name, ownership entity, street address, APN, lease document, rent figure, tenant legal
name, guarantor, debt, appraisal, insurance policy, personal financial figure, personal email or
phone number appears on this site, in the dataset or in the generated pages. Parcel-specific
fields are blank by design; internal notes under `research/` are not part of the published
artifact. An automated gate scans every published page for emails, phone numbers, SSN-like
patterns, APN-like identifiers, street addresses and person-name labels. See
[`privacy.html`](privacy.html).

## Verification and reproducibility

```bash
python tools/build_dataset.py          # writes data/brief_*.json from the verified source ledger
python tools/build_brief.py            # generates all HTML, robots.txt, sitemap.xml
python tools/verify_brief.py           # authoritative gate (dataset, HTML, links, PII, deploy)
python scripts/validate_site.py        # legacy CI entry point → same gate
python tools/projection.py --self-test # deterministic projection engine check
```

`tools/verify_brief.py` enforces: unique ids; every row has ≥1 official HTTPS source link on an
approved publisher domain; verified rows have values and unverified rows have empty cells plus a
`U-<row id>` flag; no broken relative links or missing fragments; `noopener noreferrer` on new-tab
links; completeness of `flagged.html` and `sources.html`; every dataset row present on its page;
every canonical page present in the deployment artifact; archived prior-session builds labelled
superseded and `noindex`; and no PII. It also runs the projection engine self-test.

Internal records: `research/REPO_AUDIT_DAC604B9.md` (line-by-line repo audit),
`research/VERIFICATION_DAC604B9.md` (official-source ledger), `COORDINATION.md` (shared board and
final PR/merge/deploy record).

### Projection system

`tools/projection.py` is a deterministic, offline NPV/break-even engine. It reads only the
official anchors in `data/brief_scenarios.json` (each traced to a verified row and its official
publisher) plus private parameters supplied locally by the owner. It makes no network calls,
contains no owner information, labels every number as an official anchor, an owner-supplied
sensitivity or a model output, and writes nothing into the website. Model outputs are
**not** official statistics and are deliberately not published. Official employment projections
end in 2033 and BEA has discontinued metropolitan-area output/income statistics, so no series is
extrapolated to 2035.

## Local preview

```bash
python3 -m http.server 4173 --bind 0.0.0.0
```

Then open `http://localhost:4173/index.html`. The site is fully static: no build tooling, no
external fonts, no analytics, no cookies, no network requests.

## Deployment

`.github/workflows/pages.yml` regenerates the site from the dataset, checks that the committed
pages match the generated output, runs both verification gates and the engine self-test, then
uploads only the canonical pages and `assets/brief.css` / `assets/brief.js` to GitHub Pages.

The repository's Pages site is currently configured for a **legacy branch build** in addition to
the Actions deployment; the integration token cannot change `build_type` (HTTP 403). Therefore all
committed files are also served by the legacy build. Prior-session HTML under `archive/`, `pages/`
and `site/` is **preserved, not deleted**; each such page is stamped with a visible "superseded"
banner, `noindex`, and is excluded by `robots.txt`. Only the pages listed above are the canonical,
verified product. See IR-D12 on `flagged.html`.

## Prior work

Earlier sessions' dashboards, datasets and prose (`archive/`, `pages/`, `site/`, `data/*.json`,
`EXECUTIVE_SUMMARY.md`, `DECISION_MEMO.md`, `METHODOLOGY.md`, `RISK_REGISTER.md`,
`analysis/`, `risks/`, `model/`, `scripts/`, `assets/styles.css`, `assets/site.js`) are retained
for audit. Verified values from this build are re-read from the publishers; nothing is imported
from a prior dataset without re-verification. Open overlapping PRs #10 and #14 were not merged.
