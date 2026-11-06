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
| T1 | Research: market & demographic fundamentals (Census/BLS/DOF) | done | S-83526ad4 | `research/notes/market-*.md` |
| T2 | Research: tenant & lease risk (SEC EDGAR, JACK 10-K) | done | S-83526ad4 | `research/notes/tenant-*.md` |
| T3 | Research: labor-cost & regulatory risk (CA DIR, LA City, Measure ULA, Prop 13) | done | S-83526ad4 | `research/notes/regulatory-*.md` |
| T4 | Research: catastrophe & black-swan risk (CAL FIRE, CGS, USGS, CA DOI) | done | S-83526ad4 | `research/notes/hazard-*.md` |
| T5 | Research: schools & quality-of-life indicators (NCES, CDE) | done | S-83526ad4 | `research/notes/schools-*.md` |
| T6 | Research: capital markets & exit-cost inputs (Treasury, CPI) | done | S-83526ad4 | `research/notes/schools-capital.md` |
| T7 | Dataset build (`data/*.json`) + verification script | done | S-83526ad4 | `data/`, `scripts/` |
| T8 | Site build (landing + category pages + tables) | done | S-83526ad4 | `index.html`, `*.html`, `assets/` |
| T9 | Verification pass: every row -> official source link or flagged blank | done | S-83526ad4 | `data/`, `research/VERIFICATION-LOG.md` |
| T10 | Integration, PR, merge, Pages publish | in progress | S-83526ad4 | branch-wide |

## Verification performed (T9)

Build gate: `node scripts/verify-data.mjs` -> **370 assertions pass**. It enforces:
1. unique IDs and complete schema on all 130 records;
2. every non-blank value is `verified` or `derived`;
3. **every `unverified` row has an empty value** (the gate fails if a number is smuggled into a flagged row);
4. every source URL is https and on the official-domain allowlist (census.gov, bls.gov, dof.ca.gov, sec.gov,
   conservation.ca.gov, usgs.gov, fire.ca.gov, osfm.fire.ca.gov, insurance.ca.gov, assessor.lacounty.gov, lacity.gov,
   dir.ca.gov, nces.ed.gov, stlouisfed.org, cde.ca.gov);
5. every internal link and asset reference in every HTML page resolves, and every page appears in the navigation;
6. the per-category row counts declared on `sources.html` match the dataset exactly.

Render test: all 10 pages were executed against the real JSON in a headless DOM — **no JavaScript errors**, no empty table
slots, navigation present on every page, model output identical to the figures quoted in the narrative
(A 13.43x / B 13.15x / C 15.19x, break-even renewal probability 59.4%).

Row accounting: 130 records = 91 verified + 3 derived + 28 unverified (blank) + 8 placeholder (withheld).

## Irregularities logged
- **R-01** Census Vintage-2025 county population (9,694,934) vs. CA DOF Baseline-2024 projection (9,853,435): 158,501 gap
  between two official products. Both published as separate rows, never blended.
- **R-02** Jack in the Box FY2025 10-K Item 1 says 2,136 restaurants / 22 states; the same-day Q4 earnings release boilerplate
  says ~2,135 / 21 states. Site uses 2,136 and flags the conflict.
- **U-09** Measure ULA statutory rates verified (4.0% / 5.5%), but the annually indexed dollar thresholds could not be
  confirmed on an official page; third-party figures conflict by up to $300k. No threshold published beyond $5m/$10m.
- **U-10** AB 1228 $20/hour verified from 2024-04-01; no subsequent Fast Food Council figure was published on the DIR page
  retrieved, so none is stated.

## Handoffs / conflicts
None. No other session claimed, wrote to, or merged into this repository during the build; no merge conflicts occurred.
`arena/83526ad4-jack1` therefore also served as the integration branch (single-session repo, no parallel scopes to merge).

## Log

| UTC time | Session | Entry |
|---|---|---|
| 2026-11-06T00:00Z | S-83526ad4 | Repo audit: single commit `ef1b4c6`, `README.md` only (7 bytes, `# Jack1`). No prior content, no other session commits on any branch. GitHub Pages already enabled: source `main` `/`, URL https://wingbangboozle1-lang.github.io/Jack1/, status `built`. Claimed T0–T6. |
