# Jack in the Box NNN decision brief — central Los Angeles area

A privacy-safe, official-source decision dashboard for a **reported** Jack in the Box NNN-leased property near central Los Angeles with an approximate **2030–2035** lease expiry. The exact parcel, legal tenant, guarantor, rent, value, debt, condition, insurance, tax basis, and owner finances are **not verified** and remain blank/flagged.

**Live dashboard:** https://wingbangboozle1-lang.github.io/Jack1/  
**Repository:** https://github.com/wingbangboozle1-lang/Jack1  
**Last independent re-verification:** 2026-11-10 — 76 of 76 published observations re-read at their own
official URL and matched exactly (report: `research/verification-2026-11-10.md`)

## Recommendation

Prepare sale and renewal cases in parallel. Preserve notice/option rights, verify the actual obligor and lease, and compare after-tax net sale proceeds with risk-adjusted ownership value. Do not make an irreversible sell/extend choice or drift to expiry without a funded re-tenanting alternative.

This is decision support, not legal, tax, appraisal, or brokerage advice.

## Canonical public pages

- `index.html` — landing page and executive decision
- `market.html` — geography, population, income, jobs, schools, drivers
- `property.html` — blank asset fields, tenant/issuer context, taxes, gates
- `projections.html` — official DOF/SCAG paths, derived arithmetic, gated property model
- `decision.html` — sell, renew, hold, exchange, refinance, re-tenant paths
- `risks.html` — ordinary, rare high-impact, and black-swan risks
- `requirements.html` — coverage checklist
- `flagged.html` — unconfirmed values and irregularities
- `sources.html` — official source registry
- `audit.html` — verification, privacy, deployment, and method
- `404.html` — generated from the same navigation list as the dashboard, so retired URLs still land somewhere useful

Historical `pages/`, `site/`, `archive/`, extra root pages, old data/model/tools, and research notes are preserved in Git but are **not** part of the curated public artifact.

## Reproduce and verify

Python 3.11+; no third-party runtime dependencies.

```bash
python3 scripts/build_public.py           # generate canonical pages + 404.html + assets/projections.json
python3 scripts/build_public.py --check   # fail if committed pages differ from dataset
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate_site.py          # structure, row sources, allowlist, links, blanks, privacy
python3 scripts/build_public.py --out _site
python3 scripts/validate_site.py --site _site --artifact
```

The verified dataset is `data/verified-2026-11-08.json`. The filename date is the date the canonical
build was created; the file's `meta` block records the latest re-verification (`meta.reverified`).
It keeps its original name because the build script, the tests, and the workflow all reference that
exact path. Projection arithmetic is in `scripts/projection_model.py`. Missing property inputs produce `None`/blank outputs, never zero or invented assumptions.

## Privacy and source policy

- No owner, parcel, lease-party, or personal financial identifiers are published.
- Every published table row links to an official source or repository provenance record.
- Unconfirmed values are blank and appear on `flagged.html`.
- Derived values are labeled as calculations from cited official inputs.
- Official DOF and SCAG projections are kept separate; no interpolation, blending, or parcel extrapolation.

## Deployment

`.github/workflows/pages.yml` validates on PRs and, on `main`, builds a curated `_site` artifact containing only the canonical pages/assets/generated projection data. It attempts to set GitHub Pages to workflow-built source using the workflow token.

If Pages remains in legacy `main /` mode, `_config.yml` excludes historical/internal files so the legacy fallback serves only the curated root dashboard. The former root `.nojekyll` marker is preserved under `archive/arena-0e369d53-legacy/` and is regenerated inside the workflow artifact. A successful Actions upload alone is not publication proof; the live URL and a sentinel page must be fetched after merge.

Coordination and verification records: `COORDINATION.md`, `verification/2026-11-08-0e369d53.md`, `research/0e369d53/source-notes.md`.

## What changed on 2026-11-10 (verification pass)

- **Nothing that was published was wrong.** 76 of 76 observations matched their official source
  exactly; no figure was corrected and none was invented.
- **Two publication defects were fixed.** `404.html` was excluded from publication, so a mistyped URL
  returned GitHub's default error page; the retained 404 page also described a stale "seventeen page"
  build and linked eight pages that no longer exist. It is now generated from the live navigation list
  and covered by a test.
- **Five decision-relevant rows were added** from official sources that had not previously been used:
  the 12-month and six-month range of the 10-year Treasury yield (FRED `DGS10`), a CPI cross-check
  against the BLS Los Angeles summary (FRED `CPIAUCNS`, not-seasonally-adjusted series), and two
  issuer-context rows from the FY2025 Form 10-K (lease obligations at closed locations, and the
  approximately 70% California-plus-Texas concentration the issuer itself flags alongside earthquake,
  wildfire, and severe-weather risk).
- **Site:** a per-table filter now reports how many rows match instead of hiding rows silently, and
  `/` focuses the filter. A financing-sensitivity table and an explicit sell-versus-renew decision rule
  were added, both stating what is still unverified rather than assuming a cap rate, rent, or value.
- **Process:** two arithmetic errors I introduced in this pass were caught by tests written to guard
  them (a six-month yield range and a CPI series mismatch) and corrected before publication. The
  seasonally adjusted CPI series was replaced with the not-seasonally-adjusted series, which is the
  correct basis for a September-to-September comparison.

Coordination, scope, and the full irregularity list are in `COORDINATION.md` and
`research/verification-2026-11-10.md`.
