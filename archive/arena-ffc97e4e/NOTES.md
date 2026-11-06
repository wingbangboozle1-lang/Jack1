# Archive — session arena-ffc97e4e parallel build (2026-11-06)

This folder preserves, byte-for-byte, the independent full-site build produced by Arena session
`arena-ffc97e4e` while session `d2137d88`'s build was merged to `main` first (PR #1).
Per parallel-session rules, the merged `main` site (d2137d88's) is the canonical deployment.
This archive is **not deployed** (`.github/workflows/pages.yml` copies only root `*.html` + `assets/`).
Preserved so nothing is lost: pages (index, executive-summary, property, market, economy, tenant,
projections, risk, decision, sources, flagged) + assets (style.css, app.js, projection.js).
Its unique tenant research was merged forward into the live site as root `tenant.html`.
Note: `assets/projection.js` there implements a WALT-decay NPV model with a live
break-even renewal-probability readout (~23.1% at the illustrative default inputs) — see
`archive/arena-ffc97e4e/projections.html` for the formulas. Not investment advice.
