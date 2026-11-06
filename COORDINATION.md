# COORDINATION.md — Shared Task Board

**Project:** Jack in the Box NNN property — Central Los Angeles — hold vs. renew vs. sell analysis
**Repository:** `wingbangboozle1-lang/Jack1`
**Last updated:** 2026-11-06

---

## 0. Session registry

| Session ID | Branch | Role | Status |
|---|---|---|---|
| `arena-972c721e` | `arena/972c721e-jack1` | Research + build + **final integration** | active |

### Branch policy note (important, read before claiming)

The platform that runs this session pins the whole session to one branch:
`arena/972c721e-jack1`. This session is therefore **not permitted** to create or push
`session-<id>/<task>` branches or to switch branches. The equivalent isolation is
enforced *not* by branches but by **file scopes** in the task table below
(section 3), which are non-overlapping by construction.

**This branch is the integration branch.** It is the only branch this session writes to.
Any future session must create its own branch, and only the final integration
session may change the shared outputs listed in section 4.

---

## 1. Confidentiality / privacy rules (binding on every session)

1. **No personal information in this repo or on the published site.** No owner name,
   no entity name, no address, no parcel/APN, no tenant-franchisee identity, no
   contact details, no dollar figure that is traceable back to the owner.
2. The subject property is referred to as **`SP-01`** ("Subject Property 01").
   Location is described only at the granularity that the owner supplied:
   **"Central Los Angeles"**. Sub-market analysis is presented as a *scenario
   matrix* over candidate sub-markets, never as a confirmed location.
3. Any figure that would only be known from private documents (rent, NOI, lease
   commencement, renewal option count, parcel size, building size, ownership
   basis, mortgage balance) is published as **`[WITHHELD]`** or as an explicitly
   labelled *assumption band* — never as a fact.
4. Research notes containing anything private must stay in the internal research log
   and must not be copied to `site/`. Current state: **no personal information has
   been collected, so there is nothing to redact.**

---

## 2. Working agreements

* Small, frequent commits. `git pull --rebase` before every push.
* Never mark a data point verified without an official source URL that a human can
  open and check. `id` in the data files links the row to `site/sources.html`.
* A value that cannot be confirmed from an official source is **left blank and
  flagged** (`status: "unverified"`), never estimated and never inferred.
* If a claim is supported only by a non-government source (broker report, REIT
  filing, trade press), its status is `industry` and it is displayed in a separate,
  clearly labelled table. It is never mixed into the government-verified tables.
* A claim stale by more than 24 months gets `stale: true` and a visible date pill.

---

## 3. Task board

Status values: `unclaimed` · `in progress` · `done` · `needs review` (published on
the Flagged for Review page; does not block anything).

| # | Task | Status | Owner | File scope | Notes |
|---|---|---|---|---|---|
| T01 | Repo audit + coordination board | done | `arena-972c721e` | `COORDINATION.md`, `README.md` | Repo was 1 file (`README.md`, 6 bytes). No prior work to reconcile. |
| T02 | Source ledger & verification method | done | `arena-972c721e` | `research/*.md`, `site/data/sources.json` | 40 rows, each fetched and read. |
| T03 | Macro / capital-markets data pull | done | `arena-972c721e` | `research/macro.md`, `site/data/macro.json` | Treasury, Fed, BLS CPI, BLS LA MSA. |
| T04 | Site & area data pull (pop, income, jobs, schools, retail sales) | done | `arena-972c721e` | `research/area.md`, `site/data/area.json` | Census, CA DOF, BLS, CDTFA, CDE. |
| T05 | Tenant & brand credit research (JACK) | done | `arena-972c721e` | `research/tenant.md`, `site/data/tenant.json` | SEC EDGAR only. |
| T06 | Tax / regulatory / transfer-cost research | done | `arena-972c721e` | `research/tax.md`, `site/data/tax.json` | Measure ULA, Prop 13/19, county transfer tax. |
| T07 | Catastrophe & insurance research | done | `arena-972c721e` | `research/cat.md`, `site/data/cat.json` | CAL FIRE, USGS, CDI, FEMA. |
| T08 | Valuation & projection model | done | `arena-972c721e` | `model/`, `site/data/model.json` | Deterministic Python model, no RNG, full inputs shown. |
| T09 | Site build (dashboard + subpages) | done | `arena-972c721e` | `site/**` | Static, no build step, no external JS. |
| T10 | Link + data-integrity check | done | `arena-972c721e` | `tools/check.py` | All internal links resolved; all rows have sources. |
| T11 | Final integration: verify combined data, PR → main, merge, Pages deploy | done | `arena-972c721e` | `COORDINATION.md` §6 | See section 6 for PR + deploy result. |

---

## 4. Shared outputs (integration session only)

`site/index.html` (nav/dashboard), `site/data/*.json` index files,
`site/sources.html`, `site/flagged.html`, `COORDINATION.md` §6.
No other session may edit these.

---

## 5. Request log (cross-scope change requests)

| # | Requested by | Target file | Request | Status |
|---|---|---|---|---|
| — | — | — | *empty* | — |

---

## 6. Integration record

### Build & verification

| Check | Command | Result |
|---|---|---|
| Internal link resolution | `python3 tools/check.py` | PASS — see `research/verification-report.md` |
| Every table row has a source id | `python3 tools/check.py` | PASS |
| No personal information present | `python3 tools/check.py` (PII scan: address/APN/owner patterns) | PASS |
| HTML validity (tag balance, single `<h1>`) | `python3 tools/check.py` | PASS |

### Pull request

* **PR:** https://github.com/wingbangboozle1-lang/Jack1/pull/1
* **Branch → base:** `arena/972c721e-jack1` → `main`
* **Merge commit / method:** merge commit, no approval wait
* **Merge result:** merged (see PR above; merged via `gh pr merge 1 --merge`)

### GitHub Pages

* **Source:** `main` branch, `/` root, legacy build (confirmed pre-existing config)
* **URL:** https://wingbangboozle1-lang.github.io/Jack1/
* **Deploy status:** `built` — verified by re-reading the Pages API and fetching the live URL.

### Irregularities handed to the owner

All published on `site/flagged.html` with source links. None blocked the merge.
The two that matter most:

1. **No address, no lease, no rent, no NOI were supplied.** Every property-specific
   number in this project is a labelled assumption band, not a fact. The decision
   framework is sound; the *specific* answer cannot be final until documents are read.
2. **A 2030–2035 expiry is not one decision date, it is four** (option notice
   deadlines usually precede expiry by 6–12 months, and a NNN buyer prices remaining
   term). The analysis models the notice date, not the expiry date.
