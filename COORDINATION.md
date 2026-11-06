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
| T2 | Research: NNN/QSR market, Jack in the Box lease comps, cap rates | in progress | d2137d88 | `site/data/market.js` |
| T3 | Research: demographics — population, income, poverty, housing, schools (LAUSD) | unclaimed | — | `site/data/demographics.js` |
| T4 | Research: economy — jobs, unemployment, sectors, major employers, development, transit, GDP | unclaimed | — | `site/data/economy.js` |
| T5 | Research: risks — wildfire, earthquake, flood, lease/market risk, black swans | unclaimed | — | `site/data/risk.js` |
| T6 | Decision analysis: sell-before-expiry vs renew/hold; projection model; executive summary | unclaimed | — | `site/data/decision.js`, `site/index.html` copy |
| T7 | Site creation: static dashboard + subpages, GitHub Pages deploy config | unclaimed | — | `site/**` |
| T8 | Verification pass: line-by-line vs official sources; every table row sourced or flagged | unclaimed | — | `site/**`, `COORDINATION.md` |
| T9 | Final integration: combine, builds clean, no broken links, PR to main, merge, Pages live, record PR + deploy | unclaimed | — | repo root, `.github/workflows` |

## Log
- 2026-11-06 — Session `d2137d88` created this board. Repo contained only `README.md` ("# Jack1"). Git history: single commit `ef1b4c6` ("Initial commit"). Privacy scan of repo: no personal information found (repo has no content beyond README). Claiming T1 (done), T2 (in progress). Will claim remaining tasks as capacity allows; this session performs the full pipeline including final integration, as no other sessions have claimed any task.

## Sources & verification log
(see per-page source links on the site; verification details recorded here as tasks complete)
