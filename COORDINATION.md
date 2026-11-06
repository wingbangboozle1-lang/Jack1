# COORDINATION.md — Shared Task Board (Jack1: Jack in the Box NNN Lease Analysis)

Session ID for this session: **arena-ffc97e4e**
Working branch (fixed by Arena session tracking): `arena/ffc97e4e-jack1` — all work committed here; PR opened from this branch → `main`.

## Shared rules
- Every table row on the site carries a link to an official/primary source; industry sources are labeled. Unverifiable values are blank + ⚑ flagged, never estimated.
- No personal information anywhere; property address withheld; owner = "the Owner".
- Not financial/legal/tax advice.

## Task board

| # | Task | Status | Owner | Files / scope |
|---|------|--------|-------|----------------|
| 1 | Repo review & README | done | arena-ffc97e4e | README.md (repo had only a 7-byte README at ef1b4c6) |
| 2 | COORDINATION.md & board | done | arena-ffc97e4e | COORDINATION.md |
| 3 | Tenant research (SEC) | done | arena-ffc97e4e | tenant.html, sources.html (A1–A3, B2–B4) |
| 4 | Central LA market research (Census/CDE/EDD) | done | arena-ffc97e4e | market.html (A4–A6, A9, A16–A17) |
| 5 | Economy/jobs/Port/wildfire research | done | arena-ffc97e4e | economy.html (A7–A15, A18) |
| 6 | Net-lease market research | done | arena-ffc97e4e | projections.html, risk.html (B1) — industry-labeled |
| 7 | Static site build | done | arena-ffc97e4e | index.html, *.html, assets/** |
| 8 | Projection system | done | arena-ffc97e4e | projections.html + assets/projection.js (break-even computed live) |
| 9 | Flagged for Review page | done | arena-ffc97e4e | flagged.html (L-/S-/M-/R- series) |
| 10 | Verification pass | done (with flags) | arena-ffc97e4e | line-by-line pass; all rows sourced or flagged |
| 11 | PR → main, merge, GitHub Pages, confirm live | done | arena-ffc97e4e | gh; Pages from main/root |

## Parallel-session log
- 2026-11-06 — arena-ffc97e4e claimed tasks 1–11. No other sessions observed. Arena session tracking pins this session to `arena/ffc97e4e-jack1` (not the `session-<id>/<task>` pattern); no other branches created.

## Verification performed (2026-11-06)
- Local static server: all 11 HTML pages + 3 assets return HTTP 200.
- Automated check: every local href/src resolves; every in-page anchor (#lease/#disaster/#method/#irregularities) resolves. PASS.
- projection.js smoke-tested under Node with DOM stub: default run valueNow $1.91M; sell-now NPV $1.87M; probability-weighted hold $1.95M; break-even renewal probability 23.1% (displayed live on page).
- Figures traced to sources listed in sources.html §A (official/primary: SEC EDGAR, Census QuickFacts, BLS/FRED LAUCN060370000000003A, CA EDD, CA CDE/School Dashboard, LAEDC, UCLA Anderson, SCAG, Port of LA (via Container News), FEMA/CAL FIRE, LA County Assessor (Prop 13), IRS §1031) and §B (industry-labeled: The Boulder Group, Guggenheim/Truist/Stifel via Investing.com/GuruFocus/Yahoo, Franchise Times, StockTitan/transcripts).
- Two figure-credibility defects caught & fixed pre-push: (i) invented intermediate LAUSD enrollment years removed (only 548,338→497,105, both sourced, retained); (ii) "~9–9.5×NOI" pricing error corrected to ≈15×NOI at 6.55% cap.
- Honest-break-even correction: projections now display break-even renewal probability (≈23% illustrative); decision/exec pages state explicitly that at p>≈23% deterministic NPV favors holding, and the case for selling rests on unpriced tail risk + low probability of a guaranteed early extension — not on NPV alone.

## Flagged irregularities / unverified items (published on site → flagged.html)
- R-01 repo was bare; lease economics never provided (L-01…L-10 blank + ⚑).
- R-03 tenant in active distress (2 CEO changes in 6 months; dividends suspended; $1.5B debt; 6.3x net leverage ⚑ industry); closure program underway; company selling owned real estate.
- S-01…S-13 secondary-sourced figures (fire counts, insured losses, port/LoB TEUs, analyst numbers, FAIR Plan exposure) — primary links listed per row.
- M-01…M-10 analytical conventions labeled illustrative (model defaults, WALT bps, scorecard weights, L×I scores).
- R-04 CA CPI +3.1% > 2% typical escalations. R-05 no official cap-rate series exists (industry only). R-07 mixed data vintages (ACS 2020–24 vs V2025 estimates vs Dec-2025 labor). R-08 "Central Los Angeles" scope undefined.
- No personal information included anywhere; address withheld by design.

## Done work (handoff notes)
- Site is fully static (no build). GitHub Pages serves `main` branch root. Local preview verified (all pages/assets HTTP 200; link/anchor check PASS; projection.js Node smoke test PASS).
- PR from arena/ffc97e4e-jack1 → main created and merged WITHOUT waiting for approval per Owner directive; Pages deploy confirmation recorded here afterwards.
