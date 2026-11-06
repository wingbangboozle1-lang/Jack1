# Jack1 — Central Los Angeles Jack in the Box NNN: Sell vs. Renew (2030–2035)

Decision-support research and a public dashboard site for one **anonymized**, single-tenant, absolute-NNN quick-service restaurant (Jack in the Box) in central Los Angeles, lease expiring 2030–2035.

**Live site:** https://wingbangboozle1-lang.github.io/Jack1/

## What's inside

- `index.html` — executive summary & dashboard
- `asset.html` — anonymized asset profile & pre-transaction checklist
- `demographics.html`, `economy.html`, `schools.html`, `market.html` — verified research tables (every row source-linked; unverifiable values flagged, never guessed)
- `risk.html` — risk register incl. black swans (wildfire, earthquake, pandemic, DTLA distress)
- `decision.html` — five options, risk-adjusted comparison, triggered action plan
- `projection.html` — interactive illustrative sell/renew/ride model
- `flagged.html` — everything unverified, published for review
- `sources.html` — master source registry + verification protocol
- `COORDINATION.md` — multi-session task board & log

## Verification & privacy

- No personal information is stored or published anywhere in this repo or on the site.
- Every table row links to its official source and carries a status badge (Official / Secondary / Market / Unverified / Illustrative).
- Claims that could not be verified are left blank or published on **Flagged for Review** with reasons.
- Nothing here is investment, tax, or legal advice.

## Deploy

Static site → GitHub Pages via `.github/workflows/pages.yml` (deploys on merge to `main`). `.nojekyll` disables Jekyll. No build step.
