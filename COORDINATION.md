# COORDINATION.md — Shared Task Board

**Repo:** wingbangboozle1-lang/Jack1 · **Project:** Jack in the Box NNN Lease Decision Support (Central Los Angeles)
**Branch note:** Per Arena session rules, this session (`d2137d88`) works on branch `arena/d2137d88-jack1` (the session's assigned integration branch) rather than a separate `session-<id>/<task>` branch. Scope isolation is maintained by file paths and by this board.
**Privacy rule:** No personal information may appear in the repository, in this board, or in the published site. All data must be public/aggregate. Anything that looks like personal information is flagged for internal review and excluded from the site.

## How to use
- Statuses: `unclaimed` · `in progress` · `done` · `needs review`
- A `needs review` item is published on the site's **Flagged for Review** page and does not block anything.
- Claim by writing your session ID + file scope, then commit & push immediately. Never start a task another session claimed.
- `git pull --rebase` before every push. Merge conflicts: stop, resolve without discarding the other session's work, log it here.
- Shared outputs (site index/navigation, master data) change only via the final integration pass.
- Stale-claim takeover: claim older than 60 minutes with no commits → any session may take over and log the handoff.

## Task Board

| ID | Task | Status | Owner | Files / scope |
|----|------|--------|-------|----------------|
| T1 | Repo review & baseline (README, git history, privacy scan) | done | d2137d88 | `README.md`, this file |
| T2 | Research: NNN/QSR market, Jack in the Box lease comps, cap rates | done | d2137d88 | `assets/js/data.js` |
| T3 | Research: demographics — population, income, poverty, housing, schools (LAUSD) | done | d2137d88 | `assets/js/data.js`, `demographics.html` |
| T4 | Research: economy — jobs, unemployment, sectors, development, transit, GDP | done | d2137d88 | `assets/js/data.js`, `economy.html` |
| T5 | Research: risks — wildfire, earthquake, lease/market risk, black swans | done | d2137d88 | `assets/js/data.js`, `risk.html` |
| T6 | Decision analysis: sell-before-expiry vs renew/hold; projection model; executive summary | done | d2137d88 | `index.html`, `decision.html`, `projection.html` |
| T7 | Site creation: static dashboard + subpages, GitHub Pages deploy config | done | d2137d88 | repo root site files, `.github/workflows/pages.yml` |
| T8 | Verification pass: line-by-line vs official sources; every table row sourced or flagged | done | d2137d88 | site files, `COORDINATION.md` |
| T9 | Final integration: combine, builds clean, no broken links, PR to main, merge, Pages live, record PR + deploy | unclaimed | — | repo root, `.github/workflows` |

## Log
- 2026-11-06 — Session `d2137d88` created this board. Repo contained only `README.md` ("# Jack1"). Git history: single commit `ef1b4c6` ("Initial commit"). Privacy scan of repo: no personal information found (repo has no content beyond README). Claiming T1 (done), T2 (in progress). Will claim remaining tasks as capacity allows; this session performs the full pipeline including final integration, as no other sessions have claimed any task.

## Sources & verification log
(see per-page source links on the site; verification details recorded here as tasks complete)

## Session `d2137d88` research completion notes (2026-11-06)
All research figures used on the site were collected from official sources (Census/QuickFacts, SAIPE, BLS, BEA, FRED, CA School Dashboard/CDE, LAUSD, LAHSA, LA County CAO/LAFD official fact sheet, Cal Fire, USGS, Metro, SEC EDGAR, LA Office of Finance, LA28) except where explicitly flagged on the site's Flagged for Review page (broker/market data, secondary economic series, and conflicting DTLA vacancy figures). Full source registry with links: `sources.html`. Verification approach: every table row on the site carries its own source link(s) and a status badge (Official-verified / Secondary / Unverified-flagged). Nothing on the site is asserted without either an attached source or an explicit "unverified" flag. No personal information appears anywhere (no owner/occupant names, no parcel address; Central Los Angeles location is described at neighborhood/district level only).

## T8 verification — what was actually checked (2026-11-06, session d2137d88)
- All 12 HTML pages serve HTTP 200 via `python3 -m http.server`; all local href/src targets exist (automated check, PASS).
- `node --check` passes for `assets/js/data.js` and `assets/js/app.js`.
- Registry validation: 92 rows across 6 datasets; every row has a non-empty metric/value, a valid status badge, and every referenced source id exists in the registry (42 source ids) — PASS.
- Every table row on the site carries ≥1 source link OR is explicitly badged unverified/illustrative (flagged.html shows all 15).
- Mixed-measure traps checked & labeled separately: current vs real GDP; County output-loss vs total-loss fire figures; SA vs NSA unemployment; QuickFacts SAIPE vs ACS.
- Privacy scan: no phone numbers, no emails, no street addresses, no APNs, no personal names anywhere in repo. Location described only at district level; exact parcel intentionally absent.
- Known irregularities (published on Flagged for Review, non-blocking): Westwood comp listing self-contradiction (2031 vs 2036); three conflicting DTLA vacancy estimates; GDP measure-mixing in secondary coverage; fire-loss scope spread ($5.2B–$250B); JACK financials via filing reprints not yet re-read on EDGAR; LAUSD math points blank; parcel-level hazard/school/zoning checks impossible without address (anonymized).
- Nothing was marked "verified" without an attached official source link; secondary/market/unverified items carry explicit badges.
