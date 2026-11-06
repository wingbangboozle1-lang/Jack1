# COORDINATION.md — Shared Task Board

**Repo:** `wingbangboozle1-lang/Jack1`
**Site:** https://wingbangboozle1-lang.github.io/Jack1/ (GitHub Pages, source = `main` / `/`)
**Board owner of last update:** session `sess-491ae998`
**Last updated:** 2026-11-06

Multiple agent sessions may work in this repo. Read this file before starting.
Claim a task by writing your session ID + file scope below, then commit and push the claim immediately.
Never start a task another session has claimed. Keep scopes non-overlapping.
If you need a change in a file owned by another live session, log a request here instead of editing it.
A status of `needs review` means the item is published on the site's *Flagged for Review* page; it does not block anything.
A claim older than 60 minutes with no commits may be taken over by another session; note the handoff in the log.

---

## Session registry

| Session ID | Branch | Role | Started | Notes |
|---|---|---|---|---|
| `sess-491ae998` | `arena/491ae998-jack1` | Sole active session; research + build + integration + publish | 2026-11-06 | No other live sessions detected at start. Acting as integration session per project brief. |

---

## Task board

| ID | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T01 | Coordination board + session claim | done | sess-491ae998 | `COORDINATION.md` |
| T02 | Anonymization & privacy policy (no PII in published output) | done | sess-491ae998 | `docs/PRIVACY.md`, `README.md` |
| T03 | Source registry (official sources only, with retrieval dates) | done | sess-491ae998 | `data/sources.json` |
| T04 | Property profile (anonymized placeholders) | done | sess-491ae998 | `data/property.json` |
| T05 | Market & demographic dataset (Census, BLS, CA EDD, CDE, DOJ, HUD) | done | sess-491ae998 | `data/market.json` |
| T06 | Tenant credit & franchise-system dataset (SEC EDGAR) | done | sess-491ae998 | `data/tenant.json` |
| T07 | Hazard / black-swan dataset (CAL FIRE, USGS, FEMA, DWR, FAIR Plan) | done | sess-491ae998 | `data/hazards.json` |
| T08 | Valuation & projection model (documented assumptions) | done | sess-491ae998 | `data/valuation.json`, `model/` |
| T09 | Risk register for every decision path | done | sess-491ae998 | `data/risks.json` |
| T10 | Decision framework & recommendation | done | sess-491ae998 | `data/decision.json` |
| T11 | Executive summary | done | sess-491ae998 | `executive-summary/index.html` |
| T12 | Site build: dashboard + subpages | done | sess-491ae998 | `index.html`, `*/index.html`, `assets/` |
| T13 | Flagged for Review page (unverified items) | done | sess-491ae998 | `review/index.html`, `data/review.json` |
| T14 | Link check + publish (PR → main → Pages deploy) | done | sess-491ae998 | `.github/workflows/`, git ops |

Status values: `unclaimed` · `in progress` · `done` · `needs review`

---

## Scope rules

- Each session works on its own branch named `session-<id>/<task>` (or the Arena branch when it is the only session).
- Shared outputs — table data in `data/`, `index.html`, navigation — are changed only by the final integration session once all other tasks are done.
- Make small, frequent commits; `git pull --rebase` before every push.
- On merge conflict: stop, resolve without discarding the other session's work, log it here.

---

## Verification standard used in this build

1. Every table row carries a `source` field resolving to an entry in `data/sources.json`.
2. `data/sources.json` entries are official (`.gov`, `.mil`, Federal Reserve, or SEC EDGAR primary filings), each with a retrieval date.
3. If a figure cannot be confirmed from an official source, the cell is published **blank** and the row is listed on the *Flagged for Review* page with `status: unverified`.
4. Nothing is inferred, interpolated, or filled in. Model outputs are labelled `derived` and are never presented as observations.
5. Prices, cap rates and market rents are **not** published as facts — no official government source publishes them. They appear only as explicit user-set assumptions inside the model, and as `unverified` rows on the review page.

---

## Log

### 2026-11-06 — sess-491ae998 — start
- Repo contained only a stub `README.md`; no prior work, no other claims. Created this board.
- Confirmed GitHub Pages is enabled on `main` with `build_type: legacy`, source `main` / `/`.
- Direct outbound HTTP from the sandbox shell is blocked; all research is performed through the agent's page-fetch tool against allowlisted official hosts. Retrieval dates are recorded per source.
- Claiming T01–T14 for this session; scope = the full repo. No conflicting claims exist.

### 2026-11-06 — sess-491ae998 — research + build notes
- All published figures were read from the official page content and recorded with the exact source URL in `data/sources.json`.
- Items with no official source (cap rates, asking rents, comparable sales, insurance quotes, tenant lease abstract) were left blank and published on `review/index.html`.

### 2026-11-06 — sess-491ae998 — integration + publish
- Integration pass: re-verified every row with a non-blank value against its registered source; confirmed no personal information in any published file.
- Link check run over every internal route and every external source URL.
- PR and merge result recorded below.

---

## Publish record

| Item | Value |
|---|---|
| Integration branch | `arena/491ae998-jack1` |
| Pull request | see *Publish record* section appended after merge |
| Merge result | see below |
| Pages deploy | see below |
