# Jack in the Box NNN — Central Los Angeles · Decision Dashboard

**Live site:** https://wingbangboozle1-lang.github.io/Jack1/

An anonymized, source-verified decision dashboard for a single-tenant Jack in the Box restaurant on an
absolute-NNN lease in Central Los Angeles (lease expiry window 2030–2035).

## The question
Sell before expiry, hold to expiry, or renew the lease then decide — with the risks of each path,
including black-swan events, and a recommendation that preserves wealth while keeping optionality.

## The recommendation
**Negotiate a long renewal first, then decide whether to sell the re-rated asset or hold.** Selling now
crystallises the shortest remaining lease term and pays 4.45% city transfer tax to do it; holding to
expiry without a renewal keeps tenant-credit risk to the end and then hands you vacancy.

## Privacy
No street address, parcel number, owner identity, tenant contact or lease financials appear anywhere in
this repo's published output. Placeholders (`[PARCEL-REDACTED]`, `[OWNER-ENTITY]`, `[TENANT-ENTITY]`,
`[RENT]`) are used instead. See `privacy.html` and `research/PRIVACY.md`.

## Verification
Every factual cell on the site links to its official source. Anything that could not be confirmed is left
blank and published on `flagged.html`. Nothing is inferred or filled from memory.

## Layout
```
index.html … flagged.html      generated pages (do not hand-edit)
assets/styles.css              single stylesheet, no external fonts or trackers
data/sources.json              32 sources with live URLs
data/facts.json                the verified tables (T01–T08)
data/series.json               official series used by the model
data/risks.json                12 risks incl. black-swan events
data/decision.json             options, recommendation, stress scenarios
data/flagged.json              unverified items with resolution paths
data/projections.json          model output (generated)
tools/model.py                 deterministic projection model
tools/build_site.py            page generator
tools/check_site.py            verification gate (fails on any unlinked value)
research/                      raw extracts, privacy policy, verification log
COORDINATION.md                shared task board
```

## Rebuild
```bash
python3 tools/model.py        # regenerate projections
python3 tools/build_site.py   # regenerate HTML
python3 tools/check_site.py   # verification gate — must exit 0
```

Not an appraisal, and not legal, tax or investment advice.
