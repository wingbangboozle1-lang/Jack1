# COORDINATION — Shared Task Board

**Repo:** `wingbangboozle1-lang/Jack1`
**Board owner convention:** every session writes its own ID + file scope before starting a task.

## Session registry

| Session ID | Branch / worktree | Scope | Status |
|---|---|---|---|
| `S-83526ad4` (this session) | `arena/83526ad4-jack1` | ALL tasks below (sole active session at claim time) | active |

## Rules in force
- Claim = write session ID + file scope here, commit, push, then start.
- Do not start a task another session has claimed.
- Shared outputs (`data/*.json`, `index.html`, `assets/nav.js`) are integration-session-only.
- `needs review` = published on the "Flagged for Review" page; never blocks a merge.
- Stale claim = no commit for >60 min; any session may take over and must log the handoff.

## Task board

| # | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T0 | Coordination board + repo audit | in progress | S-83526ad4 | `COORDINATION.md`, `README.md` |
| T1 | Research: market & demographic fundamentals (Census/BLS/DOF/SCAG) | in progress | S-83526ad4 | `research/notes/market-*.md` |
| T2 | Research: tenant & lease risk (SEC EDGAR, JACK 10-K) | in progress | S-83526ad4 | `research/notes/tenant-*.md` |
| T3 | Research: labor-cost & regulatory risk (CA DIR, LA City, Measure ULA, Prop 13) | in progress | S-83526ad4 | `research/notes/regulatory-*.md` |
| T4 | Research: catastrophe & black-swan risk (CAL FIRE, USGS, FEMA, CA DOI) | in progress | S-83526ad4 | `research/notes/hazard-*.md` |
| T5 | Research: schools & quality-of-life indicators (CDE, LAUSD) | in progress | S-83526ad4 | `research/notes/schools-*.md` |
| T6 | Research: capital markets & exit-cost inputs (Treasury, CPI, HUD) | in progress | S-83526ad4 | `research/notes/capital-*.md` |
| T7 | Dataset build (`data/*.json`) + verification script | unclaimed | — | `data/`, `scripts/` |
| T8 | Site build (landing + category pages + tables) | unclaimed | — | `index.html`, `*.html`, `assets/` |
| T9 | Verification pass: every row -> official source link or flagged blank | unclaimed | — | `data/`, `research/VERIFICATION-LOG.md` |
| T10 | Integration, PR, merge, Pages publish | unclaimed | — | branch-wide |

## Log

| UTC time | Session | Entry |
|---|---|---|
| 2026-11-06T00:00Z | S-83526ad4 | Repo audit: single commit `ef1b4c6`, `README.md` only (7 bytes, `# Jack1`). No prior content, no other session commits on any branch. GitHub Pages already enabled: source `main` `/`, URL https://wingbangboozle1-lang.github.io/Jack1/, status `built`. Claimed T0–T6. |
