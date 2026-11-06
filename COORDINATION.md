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
| T02 | Anonymization policy + placeholder scheme | done | ARENA-119c72a5 | `research/PRIVACY.md`, `privacy.html` | No address, APN, owner, or tenant-contact data may reach the site. Enforced by `tools/check_site.py` §privacy |
| T03 | Official-source research dossier (property, market, risk, tenant credit) | done | ARENA-119c72a5 | `research/**` | 32 sources; raw extracts in `research/raw/`; retrieval date 2026-11-06 |
| T04 | Verified data tables (every row sourced or blank+flagged) | done | ARENA-119c72a5 | `data/facts.json`, `data/sources.json`, `data/series.json` | 113 rows checked; blank+flagged where unconfirmed |
| T05 | Projection model (documented, deterministic) | done | ARENA-119c72a5 | `tools/model.py`, `data/projections.json` | All assumptions printed on `process.html` |
| T06 | Site build (landing + category subpages + dashboard UI) | done | ARENA-119c72a5 | `index.html`, `*.html`, `assets/**`, `tools/build_site.py` | 13 pages |
| T07 | Line-by-line verification pass (every table row → official link) | needs review | ARENA-119c72a5 | `research/VERIFICATION_LOG.md`, `flagged.html` | 6 transcription errors found and corrected; 12 items published on Flagged for Review |
| T08 | Link check + build check | done | ARENA-119c72a5 | `tools/check_site.py` | exit 0, 0 errors, 0 warnings |
| T09 | PR to `main`, merge, confirm Pages deploy | in progress | ARENA-119c72a5 | — | Pages source is `main` root |

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

### 2026-11-06 (later) — ARENA-119c72a5, task close-out
- No other session ever registered on this board; no claim collisions, no merge conflicts, no handoffs.
- **Sources used:** 32 total, listed in `data/sources.json` and rendered with live links on `sources.html`.
  Official: BLS via FRED (LOSA106UR, SMU/SMS06310800000000001, CAUR), Census via FRED (MHICA06037A052NCEN),
  Census QuickFacts (LA city, LA county), BLS CPI via FRED (CPIAUCSL, CUSR0000SEFV), Federal Reserve via FRED
  (DGS10, BAA, DRCRELEXFACBS), SEC EDGAR + XBRL (10-K FY2025, Revenues, NetIncomeLoss, 8-K 2026-06-23),
  California DOF projections landing page, EDD LMI, CA LegInfo (AB 1228), CA BOE (Pub 29, Prop 8, LTA 2025/010),
  City of LA Office of Finance (Measure ULA FAQ), IRS (FS-2008-18 §1031), CAL FIRE/OSFM (FHSZ),
  CA Geological Survey (Alquist-Priolo), LA County Assessor. Third-party market commentary: Net Lease Advisor,
  Solid Investments, a JIB Westwood flyer, Instone Investments — all labelled non-official.
- **Verification performed:** every fact row re-read against the issuing page during this session;
  `tools/check_site.py` enforces (a) every valued row carries a resolving source id, (b) every internal link
  resolves, (c) every source URL is https on a recognised host, (d) no address/APN/email/phone leakage,
  (e) navigation completeness. Last run: **13 pages, 0 errors, 0 warnings**.
- **Irregularities recorded (non-blocking, published on `flagged.html`):**
  F-01 exact lease terms withheld · F-02 no in-place NOI/appraisal · F-03 parcel FHSZ/seismic status
  unavailable without the APN · F-04 a broker flyer contradicts itself on lease expiry · F-05 two LA cap rates
  are not like-for-like · F-06 no official issuer credit rating · F-07 corporate vs franchisee lease unknown ·
  F-08 Census shows `X` for two city metrics · F-09 CA DOF projection attachment not parseable here ·
  F-10 no official insurance price series · F-11 FRED `LAPOP` is Louisiana, not Los Angeles (discarded) ·
  F-12 store-level sales are confidential tenant data.
- **Corrections made during verification:** FY2023 revenue corrected to $1,692,306,000; FY2023 net income
  corrected to **+$130,826,000** (it is not a loss); model normalisation bug fixed so all paths start at 1.000;
  an undefined source id (`S34`) replaced by a defined one (`S32`); stray `|` markers stripped from rendered cells.
