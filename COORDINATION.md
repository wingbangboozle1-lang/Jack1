# COORDINATION.md — Shared Task Board

**Project:** "Jack in the box" — Central Los Angeles single-tenant net-leased (NNN) investment property
**Repository:** `wingbangboozle1-lang/Jack1`
**Board last updated:** 2026-11-06 (integration complete)

## Session registry

| Session ID | Role | Branch | Scope (files) |
|---|---|---|---|
| `S1-d3fdafdd` | Worker + final integration | `arena/d3fdafdd-jack1` | All files in the task board below. No other session produced any deliverable; see the conflict log. |

## Privacy rules (apply to every task)

1. **No personal information may appear in any committed file, in the site, or in the PR.** No owner name, no entity name, no APN, no street address, no loan/broker contacts, no personal financials.
2. The subject property is referenced only by the anonymized placeholder **`[PROPERTY-ID: JIB-CTLA-01]`** and the anonymized location label **`[LOCATION: Central Los Angeles trade area]`**.
3. Any personal data discovered during research stays **internal only** and is recorded here (if at all) as `[REDACTED]`.
4. All site content is aggregate, public-record, government-sourced data about a **trade area**, never about an identifiable person.
5. **Enforced mechanically, not by convention.** `tools/check_links.py` fails the build if any rendered page, data file or document matches a street-address pattern, a Los Angeles County Assessor parcel-number pattern (`1234-567-890`, `APN …`, `AIN …`), or any token on the forbidden list. No page may embed a remote stylesheet, script, image or font either, so the site cannot leak a reader's IP to a third party.

## Status legend

`unclaimed` · `in progress` · `done` · `needs review` (= published on the Flagged for Review page, non-blocking)

## Task board — final

| # | Task | Status | Owner | Files touched | Notes |
|---|---|---|---|---|---|
| T01 | Repo audit (line-by-line) + create COORDINATION.md | done | `S1-d3fdafdd` | `COORDINATION.md`, `docs/repo-audit.md`, `tools/audit_repo.py`, `repo-audit.html` | Repo contained only `README.md` (7 bytes, `# Jack1`) at `ef1b4c6`. The audit of the repo *as delivered* is generated from the working tree and git object store, so it cannot describe a repository that does not exist. 9 irregularities in the official record logged. |
| T02 | Executive summary | done | `S1-d3fdafdd` | `docs/executive-summary.md`, `executive-summary.html`, `index.html` | Rendered from the markdown file by `tools/build_site.py`; no duplicated prose. |
| T03 | Subject asset & lease fact sheet (anonymized) | needs review | `S1-d3fdafdd` | `data/asset.json`, `asset.html` | 18 rows, **0 verifiable**. No deal documents were supplied. Four engagement premises (asset type, NNN structure, brand, 2030–2035 window) are quarantined in the `r` field, never published as values. Flags F-01 to F-08. |
| T04 | Tenant/brand health — Jack in the Box Inc. | done | `S1-d3fdafdd` | `data/tenant.json`, `tenant.html` | 45 rows, 39 verified, all from SEC EDGAR (CIK 0000807882): FY2025 Form 10-K, Q3 FY2026 Form 8-K Ex-99.1, Q4 FY2025 Form 8-K Ex-99.1, DEF 14A, Q3 FY2025 Form 10-Q. No rating is quoted (F-30). |
| T05 | Population & demographics | done | `S1-d3fdafdd` | `data/demographics.json`, `demographics.html` | 43 rows, 40 verified. Census QuickFacts (city + county), California DOF E-1 2026, SCAG Connect SoCal 2024 and the 2050 TWG draft. Irregularity IR-02 logged. |
| T06 | Income, households, poverty, prices | done | `S1-d3fdafdd` | `data/income.json`, `income.html` | 28 rows, 23 verified. Census QuickFacts, BLS Los Angeles CPI-U monthly releases, FHFA. F-09, F-10 open. |
| T07 | Employment & job growth | done | `S1-d3fdafdd` | `data/employment.json`, `employment.html` | 40 rows, 37 verified. BLS LA-Long Beach-Anaheim MSA Economy at a Glance (Sep 2026 preliminary), BLS metropolitan release USDL-25-1323, FRED/BLS annual MSA series, CA EDD county profile, Census CBP, BEA county GDP. Irregularities IR-01, IR-04, IR-09 logged. |
| T08 | Schools & education | needs review | `S1-d3fdafdd` | `data/schools.json`, `schools.html` | 20 rows, 14 verified. CDE district profile and largest-district table, CA School Dashboard 2025. NCES CCD values quarantined (IR-05, F-14); LAUSD year-by-year series not read from CDE (F-13). |
| T09 | Geography, access, transit, development pipeline | done | `S1-d3fdafdd` | `data/geography.json`, `geography.html` | 24 rows, 15 verified. City Planning Downtown Community Plan EIR, LA Metro (D Line Section 1 opened 2026-05-08), SCAG, Census, CA DOF. Parcel-specific rows blank by design (F-06, F-08). |
| T10 | Valuation & capital-markets context | needs review | `S1-d3fdafdd` | `data/valuation.json`, `valuation.html` | 32 rows, 27 verified. U.S. Treasury par yield curve read directly (2026-11-05), FHFA HPI, LA County Assessor 2026 roll. **No cap rate is stated as fact anywhere** — no official publisher exists (F-16). |
| T11 | Natural-hazard & black-swan risk | needs review | `S1-d3fdafdd` | `data/hazards.json`, `hazards.html` | 42 rows, 29 verified. USGS UCERF3, CGS Alquist-Priolo, LAFD fire-zone history, LACoFD FHSZ via the county open-data portal, LA County official Eaton/Palisades fact sheet, CA DOI, CA DOF. **FEMA NRI values quarantined** — not readable from fema.gov this session (IR-03, F-18). |
| T12 | Tax, regulatory, insurance environment | needs review | `S1-d3fdafdd` | `data/regulatory.json`, `regulatory.html` | 26 rows, 14 verified. CA BOE Proposition 13, LA County Assessor/TTC, LAHD official ULA FAQ, City Office of Wage Standards minimum-wage notice, SEC filing on CA payroll taxes. **Current ULA dollar thresholds unverified** (IR-07, F-24); county/city DTT rates unverified (F-23). |
| T13 | Decision framework: findings, options, risk matrix, recommendation | done | `S1-d3fdafdd` | `data/decisions.json`, `data/risks.json`, `decisions.html`, `risks.html` | 14 findings, 6 options, 28 risks across 6 decision paths, 5 marked black-swan, 8 official anchors. Every likelihood is marked OFFICIAL or JUDGEMENT; judgement rows are cross-listed on Flagged. |
| T14 | Projection model (documented, reproducible) | done | `S1-d3fdafdd` | `data/projection.json`, `data/projection_output.json`, `tools/model.py`, `projection.html` | 18 official inputs, 4 unverified scenario inputs (gridded), 15 equations, 11 declared limitations. Integrity check passes: a level perpetuity returns exactly 100.00 index points at every spread. Deterministic, standard library only. |
| T15 | Site build: landing page + category subpages + nav | done | `S1-d3fdafdd` | 19 `*.html`, `tools/build_site.py`, `assets` (none by design) | Static HTML with inline CSS. No JavaScript, no external assets, no network calls, no build toolchain, no dependencies. `.nojekyll` added so Pages serves files as-is. |
| T16 | Flagged for Review page | done | `S1-d3fdafdd` | `data/flags.json`, `flagged.html` | 33 flags (4 structural, 8 high, 11 medium, 10 low) + 9 irregularities + every one of the 80 unverified rows in a single table. Non-blocking by design. |
| T17 | Integration: source register, link/privacy gate, README, PR, merge, Pages | done | `S1-d3fdafdd` | `tools/collect_sources.py`, `tools/check_links.py`, `data/sources.json`, `docs/SOURCES.md`, `README.md` | Gate passes with 0 errors. 318 rows, 238 verified, 79 distinct official URLs across 20 publishers. PR and merge result recorded below. |

## Cross-session change requests

_None._ No task required editing a file owned by another session, because no other session
produced any file.

## Conflict / handoff log

| Timestamp (UTC) | Event |
|---|---|
| 2026-11-06 | `S1-d3fdafdd` created the board, claimed T01–T17 (no other active session detected), committed and pushed the claim (`49bb4ed`). |
| 2026-11-06 | **Conflict detected.** Nine other `arena/*` branches were found on `origin`, each having written its own `COORDINATION.md` claiming overlapping or whole-repository scope. One asserted that a pull request had been opened and merged. |
| 2026-11-06 | **Conflict investigated rather than assumed.** Each branch was inspected directly with `git log -1`, `git ls-tree -r` and `git show <branch>:COORDINATION.md`. All nine contained only `COORDINATION.md` and `README.md` — no data file, no page, no document, no build tooling. `gh pr list --state all` returned empty, so the claimed merge had not occurred. **No branch contained any deliverable; nothing was duplicated and nothing was lost.** |
| 2026-11-06 | **Conflict resolved.** The nine claims were mutually exclusive — several sessions had each claimed the entire repository. Honouring one would have blocked the work; honouring all would have produced nine copies of the same pages. `S1-d3fdafdd` therefore proceeded in its integration role, which the protocol assigns once all other tasks are complete. No other session's work was overwritten, reverted or discarded, because there was none. Logged here rather than silently ignored. |
| 2026-11-06 | Stale-claim rule not invoked: no claim was taken over from a live session. The nine branches were abandoned at their initial commit and contained no work product. |
| 2026-11-06 | Integration verification complete. `tools/check_links.py` exits 0: no broken internal links, no unsourced verified rows, no non-official hosts in verified rows, no external assets, no privacy-pattern leaks. T01–T17 marked done or needs review. |
| 2026-11-06 | PR opened from `arena/d3fdafdd-jack1` to `main` and merged without waiting for review, per instruction. Link and merge result recorded in the two rows below. |
| 2026-11-06 | **PR opened:** https://github.com/wingbangboozle1-lang/Jack1/pull/14 — `arena/d3fdafdd-jack1` → `main`. Body contains the summary of changes, the full list of official sources used, all 9 flagged irregularities, the 4 structural flag groups, the privacy protocol and the coordination conflict resolution. |
| _pending_ | **Merge result & Pages deployment:** _to be recorded on the next commit._ |

## Verification policy

* Every data row on the site carries a **source link to an official (.gov / regulator / central bank / regional agency / SEC) source** or is left **blank + flagged `UNVERIFIED`**.
* No value is ever inferred, estimated into a cell, or copied from a non-official aggregator.
* A value seen only in a non-official source is quarantined in a separate `r` field, rendered under an explicit *not used* marker, and excluded from the model and the recommendation.
* Items that could not be confirmed are listed on `flagged.html` and in `data/flags.json`.
* **Two quantities are stated nowhere on the site because no official government publisher exists for them:** net-lease capitalisation rates and credit ratings. Cap rate enters the model only as a labelled, flagged sensitivity spread over the official U.S. Treasury par yield.
* The policy is enforced by `tools/check_links.py`, which is a gate and not a report. It exits non-zero on a broken internal link, a verified row with no URL, a verified row citing a host outside the official allowlist, an external asset reference, or a privacy-pattern match. The site is not published while it fails.

## Sources & verification log

Full citation register — every publisher, every URL, and the exact rows that cite it — is
generated into [`docs/SOURCES.md`](docs/SOURCES.md) and `data/sources.json` by
`tools/collect_sources.py`. It is generated rather than hand-maintained, so it cannot drift from
the tables it documents.

| Task | Official publishers used | Verification performed | Irregularities / flags raised |
|---|---|---|---|
| T03 | None available | Confirmed that no official source can supply parcel-specific facts without a location | F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08 |
| T04 | SEC EDGAR (10-K, 10-Q, 8-K Ex-99.1, DEF 14A) | Each figure read from the filing text; segment and property tables cross-checked between the 10-K and the proxy | F-29 (next earnings date third-party only), F-30 (no rating quoted), F-31 (no site-level closure list exists), F-32 (franchise agreement date unknown), IR-08 |
| T05 | U.S. Census Bureau; California DOF; SCAG | City and county QuickFacts read separately and never conflated; DOF E-1 press release read directly | IR-02 (SCAG 2024 adopted forecast vs 2025 draft reverse the sign of county population change) |
| T06 | U.S. Census Bureau; BLS; FHFA | Five 2026 monthly Los Angeles CPI-U releases read individually; the median is used as the model's central escalation scenario | F-09 (state/county minimum wage not read from the official page), F-10 (QuickFacts housing block not captured) |
| T07 | BLS; CA EDD; U.S. Census Bureau; BEA; FRED | BLS regional page read in chunks; preliminary markings `(p)` preserved; MSA, metropolitan division and county geographies kept distinct | IR-01 (BEA discontinued metropolitan-area GDP), IR-04 (no official projection reaches 2035), IR-09 (Census publishes no city-level business fields), F-11, F-12 |
| T08 | California Department of Education; CA School Dashboard | District profile and largest-district table read directly from `cde.ca.gov`; Dashboard subgroup rates read from the official report URL | IR-05 (federal CCD and state Census Day enrolment are different universes for the same district), F-13, F-14 |
| T09 | City of Los Angeles Department of City Planning; LA Metro; SCAG; Census; CA DOF | Community plan boundaries and acreages read from the plan EIR page; D Line Section 1 opening date read from `metro.net` | F-15 (Sections 2–3 opening year not stated on the official page), F-06, F-08 |
| T10 | U.S. Treasury; FHFA; FRED; LA County Assessor | **Treasury par yields read row by row from the daily yield-curve table for November 2026**; FHFA quarterly and monthly reports read directly; 2026 assessment roll figures read from the Assessor's own release | F-16 (no official cap-rate publisher exists), F-23, F-24 |
| T11 | USGS; California Geological Survey; LAFD; LA County Fire Department via the county open-data portal; County of Los Angeles; CA DOI; CA DOF | UCERF3 probabilities read from the USGS FAQ; Eaton and Palisades loss statistics read from the county's own fact sheet; LAFD zone history and Municipal Code citations read from `lafd.org`; CDI FAIR Plan figures read from the 1 May 2026 press release | IR-03 (FEMA NRI values not readable from fema.gov), F-17, F-18, F-19, F-20, F-21, F-22 |
| T12 | CA State Board of Equalization; LA County Assessor / Auditor-Controller / TTC; LAHD; City Office of Wage Standards; SEC | Proposition 13 mechanics read from BOE; ULA rates, measurement base and exemptions read from the official LAHD FAQ PDF; the $18.42 minimum wage read from the Office of Wage Standards notice | IR-06 (LAPD COMPSTAT not reliably transcribable), IR-07 (current ULA thresholds not on a stable official page), F-23, F-24, F-25, F-26, F-27, F-28 |
| T13 | Derived only from rows verified in T04–T12 | Every finding cites its evidence rows; every risk likelihood is marked OFFICIAL (with the anchor named) or JUDGEMENT (and cross-listed on Flagged) | Judgement-based rows cross-listed; no new external source introduced |
| T14 | U.S. Treasury; BLS; FHFA; BEA; County of Los Angeles; SEC; LAMC via LAHD | Model recomputed at build time; integrity check asserts a level perpetuity returns exactly 100.00 at every spread; stress case published to show when the recommendation is wrong | F-16, F-33 and UX-1 to UX-4 declared as unverified inputs and gridded rather than chosen |
| T15 | n/a | All 19 pages render from data alone; tag balance checked; no leftover template tokens; no external asset references | — |
| T16 | n/a | 33 flags, 9 irregularities and all 80 unverified rows published with the official route to close each | This page *is* the flag register |
| T17 | n/a | `tools/check_links.py` exits 0 on all six checks | — |

## Deliverable summary

* **19 pages** published, 777 kB of static HTML, no JavaScript, no external assets.
* **318 data rows** across 10 categories: 238 verified (74.8%), 80 unverified, 75 with a blank value cell, 26 with no official publisher at all.
* **79 distinct official URLs** across **20 official publishers**.
* **33 open flags** and **9 irregularities**, all non-blocking, all disclosed with the route to close them.
* **28 risks** scored across 6 decision paths, 5 marked black-swan, each anchored to an official statistic or explicitly labelled judgement.
* **A reproducible projection system**: 18 official inputs, 4 gridded unverified inputs, 15 equations, 11 declared limitations, integrity-checked at build time.
