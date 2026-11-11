# Jack in the Box NNN decision brief — central Los Angeles area

A privacy-safe, official-source decision dashboard for a **reported** Jack in the Box NNN-leased property near central Los Angeles with an approximate **2030–2035** lease expiry. The exact parcel, legal tenant, guarantor, rent, value, debt, condition, insurance, tax basis, and owner finances are **not verified** and remain blank/flagged.

**Live dashboard:** https://wingbangboozle1-lang.github.io/Jack1/  
**Repository:** https://github.com/wingbangboozle1-lang/Jack1

## Recommendation

[Current source-linked executive summary](EXECUTIVE_SUMMARY.md) (2026-11-11) replaces contradictory historical root briefs that asserted numerical property outcomes without verified asset inputs. Older alternative builds/data remain in Git but are excluded from the published artifact. The previous full 74-source cross-check is dated 2026-11-10; the [2026-11-11 review](verification/2026-11-11-db9ded39.md) rechecked high-impact and rolling sources, not every source afresh.

Prepare sale and renewal cases in parallel. Preserve notice/option rights, verify the actual obligor and lease, and compare after-tax net sale proceeds with risk-adjusted ownership value. Do not make an irreversible sell/extend choice or drift to expiry without a funded re-tenanting alternative.

This is decision support, not legal, tax, appraisal, or brokerage advice.

## Canonical public pages

- `index.html` — landing page and executive decision
- `market.html` — geography, population, income, jobs, schools, drivers
- `property.html` — blank asset fields, tenant/issuer context, taxes, gates
- `projections.html` — official DOF/SCAG paths, derived arithmetic, gated property model
- `decision.html` — sell, renew, hold, exchange, refinance, re-tenant paths + blank-default local owner worksheet
- `risks.html` — ordinary, rare high-impact, and black-swan risks
- `requirements.html` — coverage checklist
- `flagged.html` — unconfirmed values and irregularities
- `sources.html` — official source registry
- `audit.html` — verification, privacy, deployment, and method
- `404.html` — fallback page linking only to the ten canonical pages

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
- Every published table row links to an official source or repository provenance record.
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
`_site` contains only the ten canonical HTML pages, `404.html`, and three assets.
The root `.nojekyll` marker is not published in legacy mode; it exists only in the
curated local artifact. `archive/`, `data/`, `research/`, `verification/`,
`COORDINATION.md`, alternate builds and root markdown briefs are not public pages.

Source and review records: `COORDINATION.md`,
`verification/2026-11-11-db9ded39.md`,
`verification/2026-11-11-a6ebbd99.md`,
`verification/2026-11-10-8d46ab6c.md`.
