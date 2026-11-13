# Jack in the Box NNN decision brief — central Los Angeles area

A privacy-safe, official-source decision dashboard for a **reported** Jack in the Box NNN-leased property near central Los Angeles with an approximate **2030–2035** lease expiry. The exact parcel, legal tenant, guarantor, rent, value, debt, condition, insurance, tax basis, and owner finances are **not verified** and remain blank/flagged.

**Live dashboard:** https://wingbangboozle1-lang.github.io/Jack1/  
**Repository:** https://github.com/wingbangboozle1-lang/Jack1

## Recommendation

[Current source-linked executive summary](EXECUTIVE_SUMMARY.md) (2026-11-13; the Nov. 13 Treasury curve is the current rate context, and the October LA CPI 12-month cell remains blank as BLS did not publish it) replaces contradictory historical root briefs that asserted numerical property outcomes without verified asset inputs. Older alternative builds/data remain in Git but are excluded from the published artifact. The full source cross-check is dated 2026-11-10; later scoped reviews re-read selected high-impact and rolling sources on Nov. 11–13. The [2026-11-13 C-1 ledger](verification/2026-11-13-c1cabdaf.md) records this targeted follow-up and its limits.

Prepare sale and renewal cases in parallel. Preserve notice/option rights, verify the actual obligor and lease, and compare after-tax net sale proceeds with risk-adjusted ownership value. Do not make an irreversible sell/extend choice or drift to expiry without a funded re-tenanting alternative.

This is decision support, not legal, tax, appraisal, or brokerage advice.

## Canonical public pages

- `index.html` — landing page and executive decision
- `market.html` — geography, population, income, jobs, schools, drivers
- `property.html` — blank asset fields, tenant/issuer context, taxes, gates
- `projections.html` — official DOF/SCAG paths, derived arithmetic, gated property model
- `decision.html` — sell, renew, hold, exchange, refinance, re-tenant paths, risk table by decision path + blank-default local owner worksheet
- `timeline.html` — dated official milestones 2026–2035 around the reported expiry window, the tenant's principal schedule, statutory clocks, and monitoring triggers; unknown dates blank (data: `data/timeline-2026-11-12-dcb5495c.json`, builder: `scripts/build_timeline.py`)
- `suggestions.html` — review-only: six property/evidence proposals, twelve site-improvement suggestions with options, and a ranked nine-step discovery sequence; nothing is implemented until chosen
- `risks.html` — ordinary, rare high-impact, and black-swan risks
- `requirements.html` — decision-question register (25 questions with verified answer or blank, acquisition route, official source) and coverage checklist
- `flagged.html` — unconfirmed values and irregularities
- `sources.html` — official source registry
- `audit.html` — verification, privacy, deployment, and method
- `404.html` — fallback page linking only to the twelve canonical pages

Historical `pages/`, `site/`, `archive/`, extra root pages, old data/model/tools, and research notes are preserved in Git but are **not** part of the curated public artifact.

## Reproduce and verify

Python 3.11+; no third-party runtime dependencies.

```bash
python3 scripts/build_public.py           # generate canonical pages, 404.html + assets/projections.json
python3 scripts/build_public.py --check   # fail if committed pages differ from dataset
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate_site.py          # structure, row sources, allowlist, links, blanks, privacy
python3 scripts/build_public.py --out _site
python3 scripts/validate_site.py --site _site --artifact
```

The verified dataset is `data/verified-2026-11-10.json` (with `data/verified-2026-11-08.json` preserved as historical baseline). Projection arithmetic is in `scripts/projection_model.py`. Missing property inputs produce `None`/blank outputs, never zero or invented assumptions, and the browser worksheet in `decision.html` starts completely blank with zero storage or network calls.

## Privacy and source policy

- No owner, parcel, lease-party, or personal financial identifiers are published.
- Every economic or legal observation row links to its official source; rows documenting repository or publication state use a clearly labeled repository-provenance source.
- Unconfirmed values are blank and appear on `flagged.html`.
- Derived values are labeled as calculations from cited official inputs.
- Official DOF and SCAG projections are kept separate; no interpolation, blending, or parcel extrapolation.

## Deployment

GitHub Pages currently runs in **legacy `main /` mode**. The repository's
`pages-build-deployment` workflow publishes on merges to `main`; our
`.github/workflows/pages.yml` validates deterministic pages, tests and curated artifact,
then leaves publication to the legacy Pages workflow. The former custom
`deploy-pages` job failed despite successful legacy publication because GitHub could
not find its `github-pages` artifact; attempting to change Pages mode with the
integration token returned HTTP 403. This custom job is disabled until an authorized
administrator switches to workflow-built Pages. Do **not** mistake an upload or a
build check for publication: verify the new revision at the live URL after every merge.

`_config.yml` excludes historical/internal files in legacy Jekyll publication;
`_site` contains only the twelve canonical HTML pages, `404.html`, and three assets.
The root `.nojekyll` marker is not published in legacy mode; it exists only in the
curated local artifact. `archive/`, `data/`, `research/`, `verification/`,
`COORDINATION.md`, alternate builds and root markdown briefs are not public pages.

Source and review records: `COORDINATION.md`,
`verification/2026-11-11-db9ded39.md`,
`verification/2026-11-11-a6ebbd99.md`,
`verification/2026-11-11-2efe9aec.md`,
`verification/2026-11-10-8d46ab6c.md`.

## 2026-11-13 re-read and irregularity log

Session `arena/d5e4c6bf-jack1` re-read 20 decision-critical figure groups (about 70 values) on 13 official primary pages. 19 matched. The 20th (debt maturities) matches its page values, but the 10-Q maturity table does not reconcile with its own repayment tranches (F-08, already flagged by session `103ff2d8`). No value changed. Four irregularities and one re-read gap were added to Flagged for Review. The privacy rescan found no personal identifiers in the artifact or dataset. Ledger: `verification/2026-11-13-d5e4c6bf.md`.

## 2026-11-12 targeted improvement

A dedicated **Suggestions review** page separates proposed actions from approved or
implemented changes. Six proposals cover privacy, lease evidence, sale/renewal tax
comparison, permissible reuse, disaster resilience, and source-refresh controls.
IRS Publication 544 contents, City Planning Zoning Search, and FEMA NRI guidance
were freshly read for this addition; this is **not** a fresh re-verification of all
historical economic observations. See `verification/2026-11-12-87c0c876.md`.

A second 2026-11-12 pass (`verification/2026-11-12-1520648f.md`) re-read ten rolling/high-impact
official sources (all matched, no value changed), added the site-improvement and discovery tables
to `suggestions.html`, and added the risk-by-decision-path table to `decision.html`.

A third 2026-11-12 pass (`verification/2026-11-12-83da931a.md`, session `arena/83da931a-jack1`) opened 40 of
the 74 registry sources and compared every row that rests on them. Three published items were corrected:
the 2027 state minimum-wage percentage (+2.97% was on neither official page; the certified figure is 2.99%
and the rate arithmetic is 2.96%), the geography of the DOF 11,260 housing-unit row (the release does not
say county or city), and a credit-loss provision labelled Q3 that the filing reports year to date. The
other 34 sources were not opened by that session and keep their earlier access dates. Additions, all from
pages read that day: ten observation rows (franchise rent trend, who holds renewal options, building
ownership split, unit volume, franchise margin, lease-payment schedule, population drivers, unemployment
and absenteeism history), two decision questions, a signal scorecard on `projections.html` that sets area
activity against tenant health, and a separate property / owner view on `decision.html`. The scorecard's
keep / sell / mixed labels are judgment on official figures and are flagged as such.

## 2026-11-13 focused C-1 follow-up

The Treasury card and financing answer now use the verified November 13 daily close; the November 10 observation remains a dated historical snapshot. FEMA’s official product page and ArcGIS item confirm the December 2025 NRI v1.20 release, and the Los Angeles County query matches the county-level values. The additional-hazard row now links to the official 18-rating query that actually contains those fields. The SEC allowance note is described as year-to-date (40 weeks), not a quarter-only result. This pass did not re-open every published row or infer parcel-specific exposure; the executed lease, parcel, obligor, property value, debt, condition, insurance and owner-specific inputs remain unverified. See `verification/2026-11-13-c1cabdaf.md` for checked URLs, arithmetic, privacy limits and the still-open debt-schedule discrepancy.
