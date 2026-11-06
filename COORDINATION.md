# COORDINATION.md — Shared Task Board

**Repo:** wingbangboozle1-lang/Jack1 · **Project:** Jack in the Box NNN Lease Decision Support (Central Los Angeles)
**Participating sessions:** `d2137d88` (site build → merged to `main` via PR #1) and `arena-ffc97e4e` (parallel full build → PR #2; merged branch re-integrated).
**Branch note (both sessions):** Arena session tracking pins each session to its assigned branch (`arena/<id>-jack1`) rather than the `session-<id>/<task>` pattern; scope isolation maintained by files + this board.
**Privacy rule:** No personal information may appear in the repository, this board, or the published site. All data must be public/aggregate. Anything resembling personal info is flagged for internal review and excluded from the site.

## How to use
- Statuses: `unclaimed` · `in progress` · `done` · `needs review`
- `needs review` items are published on the site's **Flagged for Review** page and do not block anything.
- Claim by writing your session ID + file scope, then commit & push immediately. Never start a task another session claimed.
- `git pull --rebase` before every push. Merge conflicts: stop, resolve without discarding the other session's work, log it here.
- Shared outputs (site index/navigation, master data) change only via the final integration pass.
- Stale-claim takeover: claim older than 60 minutes with no commits → any session may take over and log the handoff.

## Task Board

| ID | Task | Status | Owner | Files / scope |
|----|------|--------|-------|----------------|
| T1 | Repo review & baseline | done | d2137d88 | `README.md`, this file |
| T2 | Research: NNN/QSR market, JIB lease comps, cap rates | done | d2137d88 | `assets/js/data.js` |
| T3 | Research: demographics, income, poverty, housing, schools | done | d2137d88 | `demographics.html`, `schools.html`, `assets/js/data.js` |
| T4 | Research: economy, jobs, unemployment, GDP, DTLA | done | d2137d88 | `economy.html`, `assets/js/data.js` |
| T5 | Research: risks, wildfire, earthquake, black swans | done | d2137d88 | `risk.html`, `assets/js/data.js` |
| T6 | Decision analysis, projection model, exec summary | done | d2137d88 | `index.html`, `decision.html`, `projection.html` |
| T7 | Site creation: dashboard + subpages, Pages deploy config | done | d2137d88 | site root, `.github/workflows/pages.yml`, `.nojekyll`, `404.html` |
| T8 | Verification pass: line-by-line vs official sources | done | d2137d88 | site files |
| T9 | Final integration (d2137d88 track): merge/PR, Pages live, record | done | d2137d88 | repo root; `.github/workflows` |
| T10 | Parallel build (arena-ffc97e4e): tenant deep-dive, port/wildfire/forecast tables | done → merged | arena-ffc97e4e | archived at `archive/arena-ffc97e4e/`; tenant research merged as `tenant.html` |
| T11 | Cross-session integration merge + Pages verification | done | arena-ffc97e4e | repo root; `tenant.html`; `archive/` |

## Integration log (2026-11-06, session arena-ffc97e4e)
- Session `d2137d88` reached `main` first (PR #1, merge commit c5f4214, 2026-11-06). It built and merged a complete, registry-driven static site (11 content pages + 404 + deploy workflow).
- Session `arena-ffc97e4e` independently built a near-complete parallel site (11 pages). To honor "do not discard the other session's work" and "avoid duplicate work", the merge keeps **their** site as the canonical deployment and **archives** `arena-ffc97e4e`'s version under `archive/arena-ffc97e4e/` (not deployed; preserved for review). Unique, non-duplicative research was merged forward as a new live page: `tenant.html` (Jack in the Box Inc. SEC deep-dive: FY25 10-K, FY26 8-Ks, leadership changes, JACK on Track, Del Taco sale, net leverage 6.3x).
- Navigation extended with the new Tenant page (`assets/js/app.js`). No other shared file content altered.
- COORDINATION.md and README.md unioned/kept (theirs canonical + integration notes).
- Two figure errors found in arena-ffc97e4e's draft were corrected before archival (see PR #2). One honesty fix retained in spirit: the deterministic NPV break-even (~23% renewal probability at illustrative inputs) is acknowledged — the sell case rests on unpriced tail risk, low odds of a guaranteed early extension, and optionality, not on NPV alone. d2137d88's analysis reaches a materially identical conclusion via parallel tracks (negotiate renewal; sell if not signed / credit deteriorates).
- Re-verified after integration: all root HTML pages + assets serve HTTP 200; local href/src and anchor check PASS; `node --check` on JS PASS; Pages deploy confirmed (see below).

## Correction / disclosure (2026-11-06, session d2137d88)
- While merging a docs-only update, session d2137d88 mistakenly ran `gh pr merge 2`, which merged **arena-ffc97e4e's PR #2** (their fully-resolved integration branch) instead of d2137d88's own PR #3. Disclosed for transparency and auditability.
- Impact assessment: PR #2 contained the already-resolved union (d2137d88's `main` + arena-ffc97e4e's `tenant.html` + `archive/` + nav + COORDINATION/README union) — i.e., content both sessions had already prepared and integration-logged. No work was discarded; `main` was not damaged. Post-merge, GitHub Pages rebuilt and reached status **built**, and the deployed site was API-verified live.
- Process fix: d2137d88 will not run `gh pr merge` with an assumed PR number again; always re-check `gh pr list` / the PR title before merging.
- d2137d88's own PR #3 (this board's update) was left open and is merged only after union-resolution of this file.

## Sources & verification log
- `d2137d88`: full registry in `assets/js/data.js` (92 rows, 42 source ids; official/secondary/market/unverified badges). Verification method and known irregularities recorded in the T8 notes (below) — retained.
- `arena-ffc97e4e`: official/primary sources — SEC EDGAR (JACK 10-K FY2025; 8-Ks Oct 2025–Sep 2026), U.S. Census QuickFacts (LA city 3,869,089 / LA County 9,694,934, Jul 1 2025 V2025), BLS+FRED (LA MSA / county unemployment series; 2025 avg ≈5.7% LA County per EDD; MSA 5.3% per BLS/FRED — vintages differ, both labeled), CA EDD (LA County profile; CPI 2025 352.5, +3.1%), CA CDE (LAUSD 2025–26 enrollment 497,105; graduation 86.5%), LAEDC (2025/2026 forecasts; Jan 2025 wildfire $4.6–8.9B county-GDP 5-yr impact), UCLA Anderson (Sep 2026), SCAG (Jan 2026), Port of LA 2025 (10.24M TEUs, −0.56%, 26th consecutive #1 — via Container News citing official release ⚑), FEMA/CAL FIRE (Jan 2025 fires), LA County Assessor (Prop 13), IRS (§1031). Industry-labeled ⚑: The Boulder Group (retail net-lease cap 6.55% Q4-25), Guggenheim/Truist/Stifel (JACK credit).
- **Vintage note:** LA County July-2025 population differs between V2025 QuickFacts pulls cited by the two sessions (9.81M ACS-2024-5yr/FRED vs 9,694,934 QuickFacts V2025 county figure). Different vintages/series — not contradictory; each session's figure is labeled with its source. Do not blend.

## d2137d88 — T8 verification (retained)
- All 12 HTML pages serve HTTP 200 via `python3 -m http.server`; all local href/src targets exist (automated check, PASS).
- `node --check` passes for `assets/js/data.js` and `assets/js/app.js`.
- Registry validation: 92 rows across 6 datasets; every row has metric/value, a status badge, and every referenced source id exists in the registry (42 ids) — PASS.
- Every table row carries ≥1 source link OR an explicit unverified/illustrative badge; flagged.html shows 15 items.
- Mixed-measure traps checked & labeled separately: current vs real GDP; County output-loss vs total-loss fire figures; SA vs NSA unemployment; QuickFacts SAIPE vs ACS.
- Privacy scan: no phone numbers, no emails, no street addresses, no APNs, no personal names anywhere in repo. Location described only at district level; exact parcel intentionally absent.
- Known irregularities (published on Flagged for Review, non-blocking): Westwood comp listing self-contradiction (2031 vs 2036); three conflicting DTLA vacancy estimates; GDP measure-mixing in secondary coverage; fire-loss scope spread ($5.2B–$250B); JACK financials via filing reprints not re-read on EDGAR; LAUSD math points blank; parcel-level hazard/school/zoning checks impossible without address (anonymized).
- Nothing was marked "verified" without an attached official source link; secondary/market/unverified items carry explicit badges.

## Integration-time verification & irregularities (arena-ffc97e4e, 2026-11-06)
- Archive created preserving arena-ffc97e4e's full draft for provenance (`archive/arena-ffc97e4e/`); not deployed (workflow copies root `*.html` + `assets/` only).
- New live page `tenant.html` written directly in the d2137d88 design system; tables carry official/market badges and links; no invented figures (JIB FY26 figures from SEC-filed 8-Ks as reported; analyst numbers labeled industry ⚑).
- Honesty correction carried forward: both sessions now state the recommendation as "parallel tracks — negotiate renewal NOW; sell 2026–2028 if not signed or credit deteriorates," with deterministic break-even (~23% illustrative) acknowledged.
- Irregularities: R-01…R-08 from the archived draft remain valid and are echoed on the live Flagged page by the primary site (d2137d88) — notably: lease economics not provided (L-01…), tenant guarantee unverified, cap-rate data industry-only, mixed data vintages, scope of "Central Los Angeles" undefined, port-LA TEUs secondary-sourced.
- Pages: root `*.html` + `assets/` deploy via `.github/workflows/pages.yml` on push to `main`.

## T9 integration & release record (2026-11-06, session d2137d88)
- PR #1: https://github.com/wingbangboozle1-lang/Jack1/pull/1 — merged 2026-11-06T13:01:26Z, merge commit c5f4214da9d314d6389f9823ad97322794c45a08 (--merge, no squash).
- GitHub Pages: legacy branch-based deploy from main / — status "built" at https://wingbangboozle1-lang.github.io/Jack1/ (verified via API; custom domain none; HTTPS enforced; custom 404 active).
- Both post-merge workflows finished with conclusion=success: "Deploy static site to GitHub Pages" (run 42222151401) and legacy "pages build and deployment" (run 42222151095).
- Note: repo Pages setting is build_type=legacy (main /). The Actions workflow ALSO succeeded; both paths publish the same static root, so the site is live regardless of which path serves it. Token could not switch build_type to workflow (403) — left as-is since both deploy paths work; flagged for owner attention if they want to consolidate on one mechanism.
- Site contents after integration: d2137d88's 12-page site + `tenant.html` (SEC deep-dive) from arena-ffc97e4e's work; registry of 92 sourced rows; archive of the parallel draft under `archive/` (not deployed).
- Flagged for review items published at /flagged.html (broker cap rates, JACK credit & loss figures via reprints/aggregators, conflicting DTLA vacancy, USAFacts secondary GDP figures, blank LAUSD math points, fire-loss scope spread, parcel-level hazard checks impossible without address). None marked verified; owner review requested.
- Open follow-ups for owner: (1) review Flagged for Review page; (2) provide parcel/lease docs to re-verify parcel-specific items; (3) re-pull live 10Y/ULA/cap rates at any LOI/escrow; (4) choose Pages build mechanism (legacy vs workflow); (5) review open PR #4 (see below).

## PR & deploy record (final, 2026-11-06)
- PR #1 (arena/d2137d88-jack1 → main): merged; Pages rebuilt; live at https://wingbangboozle1-lang.github.io/Jack1/ — confirmed via API (`status: built`) and post-merge workflow run 42222151401 = success.
- PR #2 (arena/ffc97e4e-jack1 → main): merge commit 60dda8f (integration: canonical d2137d88 site + tenant.html + archive/). Merged (inadvertently, see Correction above) after its threads were resolved by arena-ffc97e4e; no content lost; Pages rebuilt → `status: built` confirmed by d2137d88 via API.
- PR #3 (arena/d2137d88-jack1 → main): this board's union update; merges after conflict resolution.
- PR #4: OPEN — arena-ffc97e4e — "JACK NNN (Central LA): sourced hold / renew / exit analysis + live dashboard". Left for the authoring session; d2137d88 does not merge another session's PR.
