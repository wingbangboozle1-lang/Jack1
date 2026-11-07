# COORDINATION.md — shared task board

> **History.** The previous board (2026-11-06, seven sessions) was corrupted by unresolved merge-conflict
> markers committed to `main` (`<<<<<<< HEAD`, `=======`, `>>>>>>> origin/main` at lines 22–203). It has been
> preserved verbatim, nothing deleted, at
> [`archive/coordination-history/COORDINATION-through-2026-11-06.md`](archive/coordination-history/COORDINATION-through-2026-11-06.md).
> Read that file for the full PR ledger, the five prior builds, and their outstanding notes.

## Coordination rules (unchanged)

- One branch per session: `arena/<session-id>-jack1` (this session: `arena/22afad63-jack1`).
- Claim a task by writing your session ID and file scope here, commit and push the claim immediately.
- Never start a task another session has claimed. Keep file scopes non-overlapping.
- If a task needs a file owned by another session, log the request here instead of editing it.
- Small, frequent commits. `git pull --rebase` before every push. Resolve conflicts without discarding work.
- Record sources, verification performed, and irregularities when a task is finished, then mark it done.
- Never mark anything verified without checking it against an official source, and link that source.
- Shared outputs (table data, site index/nav) are changed only by the final integration session.

## Open work inherited from prior sessions (read-only to this session unless claimed)

| Item | What it is | State |
|---|---|---|
| PR #5, #10, #11, #14 | Four prior-session PRs still open; #11 removes the duplicate Pages workflow, #14 is `CONFLICTING` | unclaimed |
| Two deploy paths | `.github/workflows/pages.yml` (assembles 7 pages into `_site`) races the legacy branch build (`build_type: legacy`, `main` /). Pages API reported `errored` on 2026-11-06 | needs review |
| Cited-but-unchecked links | Root pages cite 52 distinct external URLs; the site validator only checks *host allowlisting*, never that a page contains the value shown | this session's main task |

## Task board — session `arena-22afad63`

| Task ID | Description | Status | Owning Session ID | Files / scope | Sources | Verification performed | Irregularities |
|---|---|---|---|---|---|---|---|
| V1 | Repo audit + repair coordination board (conflict markers) | **done** | arena-22afad63 | `COORDINATION.md`, `archive/coordination-history/` | repo history only | Conflict markers removed from the live board and archived verbatim; no content discarded | Board had been committed with unresolved merge markers |
| V2 | Line-by-line re-verification of every verified row in `data/records.json` against the cited official page | **in progress** | arena-22afad63 | `data/records.json`, `scripts/verify-live.mjs`, `verification/` | census.gov, bls.gov, dof.ca.gov, sec.gov, nces.ed.gov, fred.stlouisfed.org, fire.ca.gov, osfm.fire.ca.gov, conservation.ca.gov, usgs.gov, insurance.ca.gov, assessor.lacounty.gov, dir.ca.gov, cityattorney.lacity.gov, finance.lacity.gov | Value-by-value re-read of the live page for each row; mismatches corrected to the published figure; rows whose citation does not support the value are re-sourced or blanked | Found: Measure ULA rows (REG-01/02) cite a City Attorney *homelessness* page that does not contain the rates; several blank rows cite unrelated pages as their "lookup" |
| V3 | Decision report: sell vs. renew, full risk register, scenario model, executive summary | unclaimed | — | `DECISION_REPORT.md` (new) | as V2 | pending | — |
| V4 | Site rebuild: landing page + category subpages from one dataset, every row source-linked | unclaimed | — | `index.html`, `assets/`, new pages | as V2 | pending | — |
| V5 | Integration: single deploy path, link check, PR, merge, deploy confirmation | unclaimed | — | `.github/workflows/`, `COORDINATION.md` | — | pending | — |

## Session log

- **Session ID:** `arena-22afad63` — branch `arena/22afad63-jack1`, started 2026-11-07.
- **Claimed:** V1–V5 (self-coordinated; no other session holds a live claim — the four open PRs were checked
  and their branches are not being pushed to during this session).
- **Privacy:** no owner name, street address, APN, entity, lease document, rent, or personal financial detail
  is published. Property fields stay `[WITHHELD]` placeholders. Nothing about the owner is collected.
