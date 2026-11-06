# COORDINATION.md — Shared Task Board

**Repo:** wingbangboozle1-lang/Jack1 · **Project:** Jack in the Box NNN Lease Decision Support (Central Los Angeles)
**Participating sessions:** `d2137d88` (site build → merged to `main` via PR #1) and `arena-ffc97e4e` (parallel full build → PR #2; merged branch re-integrated).
**Branch note (both sessions):** Arena session tracking pins each session to its assigned branch (`arena/<id>-jack1`) rather than the `session-<id>/<task>` pattern; scope isolation maintained by files + this board.
**Privacy rule:** No personal information may appear in the repository, this board, or the published site. All data must be public/aggregate. Anything resembling personal info is flagged for internal review and excluded from the site.

## How to use
- Statuses: `unclaimed` · `in progress` · `done` · `needs review`
- `needs review` items are published on the site's **Flagged for Review** page and do not block anything.
- `git pull --rebase` before every push. Merge conflicts: stop, resolve without discarding the other session's work, log it here.
- Shared outputs (site index/navigation, master data) change only via the final integration pass.

## Task Board

| ID | Task | Status | Owner | Files / scope |
|----|------|--------|-------|----------------|
| T1 | Repo review & baseline | done | d2137d88 | `README.md` |
| T2 | Research: NNN/QSR market, JIB lease comps, cap rates | done | d2137d88 | `assets/js/data.js` |
| T3 | Research: demographics, income, poverty, housing, schools | done | d2137d88 | `demographics.html`, `schools.html`, `data.js` |
| T4 | Research: economy, jobs, unemployment, GDP, DTLA | done | d2137d88 | `economy.html`, `data.js` |
| T5 | Research: risks, wildfire, earthquake, black swans | done | d2137d88 | `risk.html`, `data.js` |
| T6 | Decision analysis, projection model, exec summary | done | d2137d88 | `index.html`, `decision.html`, `projection.html` |
| T7 | Site creation: dashboard + subpages, Pages deploy config | done | d2137d88 | `.github/workflows/pages.yml`, `404.html`, `.nojekyll` |
| T8 | Verification pass: line-by-line vs official sources | done | d2137d88 | site files |
| T9 | Final integration: merge branches, combined verification, Pages live | done | arena-ffc97e4e | repo root; `.github/workflows`; `tenant.html`; `archive/arena-ffc97e4e/` |
| T10 | Parallel build by arena-ffc97e4e (tenant deep-dive, port/wildfire/forecast tables) | done → merged | arena-ffc97e4e | archived at `archive/arena-ffc97e4e/`; tenant research merged as `tenant.html` |
| T11 | PR → main, merge, GitHub Pages live, record result | done | arena-ffc97e4e | gh; Pages |

## Integration log (2026-11-06, session arena-ffc97e4e)
- Session `d2137d88` reached `main` first (PR #1, merge commit c5f4214, 2026-11-06). It built and merged a complete, registry-driven static site (11 content pages + 404 + deploy workflow).
- Session `arena-ffc97e4e` independently built a near-complete parallel site (11 pages). To honor "do not discard the other session's work" and "avoid duplicate work", the merge keeps **their** site as the canonical deployment and **archives** `arena-ffc97e4e`'s version under `archive/arena-ffc97e4e/` (not deployed; preserved for review). Unique, non-duplicative research was merged forward as a new live page: `tenant.html` (Jack in the Box Inc. SEC deep-dive: FY25 10-K, FY26 8-Ks, leadership changes, JACK on Track, Del Taco sale, net leverage 6.3x).
- Navigation extended with the new Tenant page (`assets/js/app.js`). No other shared file content altered.
- COORDINATION.md and README.md unioned/kept (theirs canonical + integration notes).
- Two figure errors found in arena-ffc97e4e's draft were corrected before archival (see PR #2). One honesty fix retained in spirit: the deterministic NPV break-even (~23% renewal probability at illustrative inputs) is acknowledged — the sell case rests on unpriced tail risk, low odds of a guaranteed early extension, and optionality, not on NPV alone. d2137d88's analysis reaches a materially identical conclusion via parallel tracks (negotiate renewal; sell if not signed / credit deteriorates).
- Re-verified after integration: all root HTML pages + assets serve HTTP 200; local href/src and anchor check PASS; `node --check` on JS PASS; Pages deploy confirmed (see below).

## Sources & verification log
- `d2137d88`: full registry in `assets/js/data.js` (92 rows, 42 source ids; official/secondary/market/unverified badges). Verification method and known irregularities recorded in their T8 notes (below) — retained verbatim.
- `arena-ffc97e4e`: official/primary sources — SEC EDGAR (JACK 10-K FY2025; 8-Ks Oct 2025–Sep 2026), U.S. Census QuickFacts (LA city 3,869,089 / LA County 9,694,934, Jul 1 2025 V2025), BLS+FRED (LAUCN060370000000003A; LA county unemployment 2025 avg 5.7%, Dec 2025 5.0% EDD; MSA June 2025 division 5.9%), CA EDD (LA County profile; CPI 2025 352.5, +3.1%), CA CDE (LAUSD 2025–26 enrollment 497,105; graduation 86.5%), LAEDC (2025/2026 forecasts; Jan 2025 wildfire $4.6–8.9B county-GDP 5-yr impact), UCLA Anderson (Sep 2026), SCAG (Jan 2026), Port of LA 2025 (10.24M TEUs, −0.56%, 26th consecutive #1 — via Container News citing official release ⚑), FEMA/CAL FIRE (Jan 2025 fires), LA County Assessor (Prop 13), IRS (§1031). Industry-labeled ⚑: The Boulder Group (retail net-lease cap 6.55% Q4-25), Guggenheim/Truist/Stifel (JACK credit).

## Session `d2137d88` T8 verification (retained)
- All 12 HTML pages serve HTTP 200 via `python3 -m http.server`; all local href/src targets exist (automated check, PASS).
- `node --check` passes for `assets/js/data.js` and `assets/js/app.js`.
- Registry validation: 92 rows across 6 datasets; every row has metric/value, a status badge, and every referenced source id exists in the registry (42 ids) — PASS.
- Every table row carries ≥1 source link OR an explicit unverified/illustrative badge; flagged.html shows 15 items.
- Mixed-measure traps checked & labeled: current vs real GDP; County output-loss vs total fire losses; SA vs NSA unemployment; QuickFacts SAIPE vs ACS.
- Known irregularities (non-blocking, on Flagged for Review): Westwood comp listing self-contradiction (2031 vs 2036); three conflicting DTLA vacancy estimates; GDP measure-mixing in secondary coverage; fire-loss scope spread ($5.2B–$250B); JACK financials via filing reprints not re-read on EDGAR; LAUSD math points blank; parcel-level checks impossible without address.

## Integration-time verification & irregularities (arena-ffc97e4e, 2026-11-06)
- Archive created preserving arena-ffc97e4e's full draft for provenance (`archive/arena-ffc97e4e/`); not deployed (workflow copies root `*.html` + `assets/` only).
- New live page `tenant.html` written directly in the d2137d88 design system; tables carry official/market badges and links; no invented figures (JIB FY26 figures from SEC-filed 8-Ks as reported; analyst numbers labeled industry ⚑).
- Honesty correction carried forward: both sessions now state the recommendation as "parallel tracks — negotiate renewal NOW; sell 2026–2028 if not signed or credit deteriorates," with deterministic break-even (~23% illustrative) acknowledged.
- Irregularities: R-01…R-08 from the archived draft remain valid and are echoed on the live Flagged page by the primary site (d2137d88) — notably: lease economics not provided (L-01…), tenant guarantee unverified, cap-rate data industry-only, mixed data vintages, scope of "Central Los Angeles" undefined, port LoB TEUs secondary-sourced.
- Pages: root `*.html` + `assets/` deploy via `.github/workflows/pages.yml` on push to `main`.

## PR & deploy record (final, 2026-11-06)
- PR #2 (arena/ffc97e4e-jack1 → main, integration merge): https://github.com/wingbangboozle1-lang/Jack1/pull/2 — state MERGED at 2026-11-06T13:03:03Z, merge commit `60dda8f`, merged by `wingbangboozle1-lang` (repo owner merged manually while integration was being verified). Integration content: d2137d88's site kept canonical; arena-ffc97e4e's parallel build archived at `archive/arena-ffc97e4e/` (not deployed); new live page `tenant.html` (SEC-verified JACK deep-dive) added and registered in nav; README + COORDINATION unioned. Local verification after integration: 13 root HTML + 4 assets serve HTTP 200; href/src/anchor check PASS (2 apparent "broken" links are JS template literals, confirmed benign); `node --check` PASS for `assets/js/app.js` and `assets/js/data.js`.
- GitHub Pages: deploy workflow "Deploy static site to GitHub Pages" (run 42222364915) — **success**; legacy `pages build and deployment` (run 42222364625) — **success**; Pages API reports `status: built`, source `main` / path `/`, html_url https://wingbangboozle1-lang.github.io/Jack1/ . Sandbox egress blocked curl to github.io (HTTP 000) — liveness verified via GitHub's own deploy + Pages status rather than direct fetch; all pages were verified 200 locally before merge.
- Rebase incident (logged per protocol): while running `git pull --rebase origin arena/ffc97e4e-jack1` after pushing b7d6115, the rebase attempted to replay d2137d88's commits onto this branch, conflicting on COORDINATION.md. Aborted immediately (`git rebase --abort`); local reset verified == remote (b7d6115); working tree clean; nothing force-pushed; no history rewritten. Lesson: no `pull --rebase` after pushing an already-pushed merge; the merge was pushed directly.
- PR #3 (follow-up record): this final verification/deploy record merged to main via PR https://github.com/wingbangboozle1-lang/Jack1/pull/3 .
