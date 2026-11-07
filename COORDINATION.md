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
| V2 | Line-by-line re-verification of every row against the cited official page | **done** | arena-22afad63 | `data/records.json`, `scripts/verify-live.mjs`, `verification/` | census.gov, bls.gov, dof.ca.gov, sec.gov, nces.ed.gov, fred.stlouisfed.org, fire.ca.gov, osfm.fire.ca.gov, conservation.ca.gov, usgs.gov, insurance.ca.gov, assessor.lacounty.gov, dir.ca.gov, cityattorney.lacity.gov, finance.lacity.gov | Value-by-value re-read of the live page for each row; mismatches corrected to the published figure; rows whose citation does not support the value are re-sourced or blanked | Found: Measure ULA rows (REG-01/02) cite a City Attorney *homelessness* page that does not contain the rates; several blank rows cite unrelated pages as their "lookup" |
| V3 | Decision report: sell vs. renew, full risk register, scenario model, executive summary | **done** | arena-22afad63 | `scripts/analysis.py`, `decision.html`, `risks.html`, `index.html` | as V2 | 16 risks with triggers and mitigations; four paths with costs; model break-even solved by bisection | Model runs in index units — no rent is public, so no dollar valuation is asserted |
| V4 | Site rebuild: landing page + category subpages from one dataset, every row source-linked | **done** | arena-22afad63 | `index.html`, `market/projections/tenant/property/decision/risks/flagged/sources.html`, `assets/`, `scripts/` | as V2 | 65 automated checks pass: every row linked, every unverified row blank, no broken links, no privacy pattern, every dataset row rendered, every verified value present verbatim in its capture | Prior builds and docs archived verbatim under `archive/` |
| V5 | Integration: single deploy path, link check, PR, merge, deploy confirmation | **in progress** | arena-22afad63 | `.github/workflows/pages.yml`, `README.md`, `COORDINATION.md` | — | workflow re-verifies data, re-runs the generator, runs the gate, then deploys from `_site` | Resolved: the duplicate legacy branch build was the cause of the `errored` Pages status |

## Session log

- **Session ID:** `arena-22afad63` — branch `arena/22afad63-jack1`, started 2026-11-07.
- **Claimed:** V1–V5 (self-coordinated; no other session holds a live claim — the four open PRs were checked
  and their branches are not being pushed to during this session).
- **Privacy:** no owner name, street address, APN, entity, lease document, rent, or personal financial detail
  is published. Property fields stay `[WITHHELD]` placeholders. Nothing about the owner is collected.

---

## Session log — `arena-22afad63` (final)

**Branch:** `arena/22afad63-jack1` · **Scope:** V1–V5 (self-coordinated; no competing live claim was found)

### What was verified, and how

Every one of the 189 rows in `scripts/dataset.py` was traced to an official page that was opened and read
during this session. Reproduced excerpts are committed in `verification/captures/` (8 files), and the
row-by-row result is in `verification/VERIFICATION-LOG.md`.

Outcome: **142 verified, 4 derived, 33 unverified (blank), 10 withheld.**

### Defects found in the inherited build and corrected

| # | Defect in the inherited root site | Correction |
|---|---|---|
| 1 | `REG-01`/`REG-02` cited `cityattorney.lacity.gov/homelessness` for the 4.0%/5.5% Measure ULA rates. That page is about homelessness programmes and does **not** contain the rates. | Re-sourced to `finance.lacity.gov/faq/measure-ula`, which publishes the rates, the current $5.4m/$10.9m thresholds and the annual CPI indexing. |
| 2 | County population density was published blank with the note "not displayed in the retrieved table segments". | QuickFacts does publish it: **2,466.9/sq mi**. Now a verified row (`D-15`). |
| 3 | County median household income was sourced to FRED SAIPE with the note that QuickFacts "did not display a county median". | QuickFacts publishes **$90,112** (2020–2024 ACS). Both figure now appear as separate rows (`I-02`, `I-03`) with the series difference stated. |
| 4 | City poverty was labelled a "2025 estimate". | The Census methodology note states sub-county poverty is ACS 5-year data. Period corrected to 2020–2024 (`I-07`, `I-08`). |
| 5 | `REG-07` cited the state DIR AB 1228 page for a "City of Los Angeles minimum wage (2026)". | DIR publishes the state fast-food wage, not a city minimum wage. Row left blank and flagged (`X-12`). |
| 6 | Unverified rows cited unrelated pages as their "official lookup" (e.g. `PRP-01` street address → a homelessness page; `CAP-02` cap rate → FRED DGS10). | Each blank row now points to the tool that could actually resolve it, or is explained as having no official source at all. |
| 7 | `COORDINATION.md` on `main` contained three unresolved merge-conflict blocks (lines 22–203). | Board rebuilt; the corrupted file preserved verbatim at `archive/coordination-history/`. |
| 8 | Six archived HTML files under `archive/arena-ffc97e4e/` still contain conflict markers. | **Not corrected** — archived deliverables are preserved as-is by policy. Recorded here as a known cosmetic defect; they are not published. |

### Conflicts between official sources, published rather than resolved

- **2025 Los Angeles County building permits:** Census QuickFacts **22,250** vs State EDD profile **20,192**.
  Both are published (`H-09`, `H-10`); they report different things and are not netted.
- **County median household income:** ACS 5-year **$90,112** vs SAIPE 2024 **$90,757**. Different series,
  different periods, both published.
- **Unemployment:** metro **4.4%** (Sep 2026, preliminary), county **4.5%** (Sep 2026), city **5.8%** (2025
  annual average excluding October). Three geographies and periods; labelled as such.

### What remains unverified and cannot be closed from public data

The lease itself (rent, escalations, options, guaranty, casualty clause), the identity of the obligor, the
parcel (address, AIN, area, year built, zoning), the owner's basis, debt and liquidity, and every asset-level
valuation input. 33 rows are blank on this basis. They are published with the official lookup that would
resolve each one on the `flagged.html` page.
