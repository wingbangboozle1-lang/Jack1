# COORDINATION.md — Shared Task Board

**Repo:** wingbangboozle1-lang/Jack1
**Live site:** https://wingbangboozle1-lang.github.io/Jack1/ (GitHub Pages, source = `main` branch, `/` root, legacy build)
**Project:** Jack in the Box NNN property (Central Los Angeles) — hold-to-expiry vs. sell analysis, anonymized.

> Read this file before starting any work. Claim a task by writing your session ID + file scope below,
> then commit and push the claim immediately. Never start a task another session has claimed.
> Keep scopes non-overlapping. Shared outputs (table data, index/nav) are changed only by the
> final integration session.

## Session registry

| Session ID | Branch / worktree | Role | Claimed since | Last commit |
|---|---|---|---|---|
| `ARENA-119c72a5` | `arena/119c72a5-jack1` | Research + site build + verification + integration (sole active session; no other sessions observed at start) | 2026-11-06 | see git log |

No other session had claimed anything when this board was created. This session therefore claims all tasks
sequentially and records each claim/close below. If a second session appears, it must pick unclaimed rows only.

## Task board

Status values: `unclaimed` · `in progress` · `done` · `needs review` (published on the Flagged for Review page; non-blocking)

| ID | Task | Status | Owner | File scope | Notes |
|---|---|---|---|---|---|
| T01 | Board creation + task claims | done | ARENA-119c72a5 | `COORDINATION.md` | Created 2026-11-06 |
| T02 | Anonymization policy + placeholder scheme | in progress | ARENA-119c72a5 | `research/PRIVACY.md`, `content/*.json` | No address, APN, owner, or tenant-contact data may reach the site |
| T03 | Official-source research dossier (property, market, risk, tenant credit) | in progress | ARENA-119c72a5 | `research/**` | raw extracts + retrieval dates; no derived values |
| T04 | Verified data tables (every row sourced or blank+flagged) | unclaimed | — | `data/**` | |
| T05 | Projection model (documented, deterministic) | unclaimed | — | `tools/model.py`, `data/projections.json` | |
| T06 | Site build (landing + category subpages + dashboard UI) | unclaimed | — | `index.html`, `*.html`, `assets/**`, `tools/build_site.py` | |
| T07 | Line-by-line verification pass (every table row → official link) | unclaimed | — | `research/VERIFICATION_LOG.md` | |
| T08 | Link check + build check | unclaimed | — | `tools/check_links.py` | |
| T09 | PR to `main`, merge, confirm Pages deploy | unclaimed | — | — | |

## Log

### 2026-11-06 — ARENA-119c72a5
- Inspected repo: single commit `ef1b4c6` ("Initial commit"), only `README.md` (7 bytes). No prior work, no conflicts.
- Branch in use: `arena/119c72a5-jack1` (session branch; must not be renamed). Merge target: `main`.
- GitHub Pages already enabled: `source.branch=main`, `path=/`, `build_type=legacy`, `html_url=https://wingbangboozle1-lang.github.io/Jack1/`, `https_enforced=true`.
  → Because Pages deploys from the `main` root, the generated site must live at repo root on `main`.
- Environment finding: the sandbox shell has **no outbound network**; research is performed with the harness
  web-fetch tools, and only official domains resolve through them (verified working: `fred.stlouisfed.org`,
  `sec.gov`, `census.gov`). All fetched extracts are saved verbatim under `research/raw/` with retrieval dates
  so every published row is reproducible.
- Files claimed by this session: all paths above (sole session). No handoff or conflict recorded.
