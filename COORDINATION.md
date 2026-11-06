# COORDINATION.md — Shared Task Board

**Project:** "Jack in the box" — Central Los Angeles single-tenant net-leased (NNN) investment property
**Repository:** `wingbangboozle1-lang/Jack1`
**Board last updated:** 2026-11-06T00:00Z

## Session registry

| Session ID | Role | Branch | Scope (files) |
|---|---|---|---|
| `S1-d3fdafdd` | Worker + final integration | `arena/d3fdafdd-jack1` | All files listed in the task board below (no other session has claimed any task as of the last commit) |

## Privacy rules (apply to every task)

1. **No personal information may appear in any committed file, in the site, or in the PR.** No owner name, no entity name, no APN, no street address, no loan/broker contacts, no personal financials.
2. The subject property is referenced only by the anonymized placeholder **`[PROPERTY-ID: JIB-CTLA-01]`** and the anonymized location label **`[LOCATION: Central Los Angeles trade area]`**.
3. Any personal data discovered during research stays **internal only** and is recorded here (if at all) as `[REDACTED]`.
4. All site content is aggregate, public-record, government-sourced data about a **trade area**, never about an identifiable person.

## Status legend

`unclaimed` · `in progress` · `done` · `needs review` (= published on the Flagged for Review page, non-blocking)

## Task board

| # | Task | Status | Owner | Files touched | Notes |
|---|---|---|---|---|---|
| T01 | Repo audit (line-by-line) + create COORDINATION.md | done | `S1-d3fdafdd` | `COORDINATION.md`, `docs/repo-audit.md` | Repo contained only `README.md` (7 bytes, "# Jack1") at `ef1b4c6`. No data, no site, no CI. Nothing to preserve/merge. |
| T02 | Executive summary | in progress | `S1-d3fdafdd` | `index.html`, `docs/executive-summary.md` | Depends on T03–T12. |
| T03 | Subject asset & lease fact sheet (anonymized) | in progress | `S1-d3fdafdd` | `data/asset.json`, `asset.html` | All deal-specific values are placeholders — no source documents were provided. Flagged. |
| T04 | Tenant/brand health — Jack in the Box Inc. | in progress | `S1-d3fdafdd` | `data/tenant.json`, `tenant.html` | Source: SEC EDGAR (10-K/10-Q). |
| T05 | Population & demographics | in progress | `S1-d3fdafdd` | `data/demographics.json`, `demographics.html` | Source: U.S. Census Bureau. |
| T06 | Income, households, poverty | in progress | `S1-d3fdafdd` | `data/income.json`, `income.html` | Source: U.S. Census Bureau ACS. |
| T07 | Employment & job growth | in progress | `S1-d3fdafdd` | `data/employment.json`, `employment.html` | Source: BLS, CA EDD, BEA. |
| T08 | Schools & education | in progress | `S1-d3fdafdd` | `data/schools.json`, `schools.html` | Source: CDE, NCES. |
| T09 | Geography, access, transit, development pipeline | in progress | `S1-d3fdafdd` | `data/geography.json`, `geography.html` | Source: LA Metro, City of LA, USGS/NOAA. |
| T10 | Valuation & pricing context | in progress | `S1-d3fdafdd` | `data/valuation.json`, `valuation.html` | Source: FRED/FHFA, LA County Assessor, CBOE/Treasury. |
| T11 | Natural-hazard & black-swan risk | in progress | `S1-d3fdafdd` | `data/hazards.json`, `hazards.html` | Source: CAL FIRE, FEMA, USGS, CGS, NOAA/NWS. |
| T12 | Tax, regulatory, insurance environment | in progress | `S1-d3fdafdd` | `data/regulatory.json`, `regulatory.html` | Source: LA County Assessor, CA BOE, CA CDI, City of LA. |
| T13 | Decision framework: scenarios, risk matrix, recommendation | in progress | `S1-d3fdafdd` | `data/decisions.json`, `decisions.html`, `risks.html` | Derived analysis; inputs sourced in T04–T12. |
| T14 | Projection model (documented, reproducible) | in progress | `S1-d3fdafdd` | `model/`, `projection.html` | Deterministic scenario calculator; all assumptions listed and sourced. |
| T15 | Site build: landing page + category subpages + nav | in progress | `S1-d3fdafdd` | `index.html`, `assets/`, all `*.html` | Static HTML/CSS, no build step. |
| T16 | Flagged for Review page | in progress | `S1-d3fdafdd` | `flagged.html`, `data/flags.json` | Non-blocking. |
| T17 | Integration: link check, Pages workflow, PR, merge | unclaimed | `S1-d3fdafdd` (integration role) | `.github/workflows/`, `README.md` | Runs after T01–T16. |

## Cross-session change requests

_None._ (No task requires editing a file owned by another session.)

## Conflict / handoff log

| Timestamp (UTC) | Event |
|---|---|
| 2026-11-06 | `S1-d3fdafdd` created board, claimed T01–T17 (no other active session detected), committed and pushed claim. |

## Verification policy

* Every data row on the site carries a **source link to an official (.gov / regulator / SEC) site** or is left **blank + flagged `UNVERIFIED`**.
* No value is ever inferred, estimated into a cell, or copied from a non-official aggregator.
* Items that could not be confirmed are listed on `flagged.html` and in `data/flags.json`.
* Sources and verification notes for each completed task are appended below.

## Sources & verification log

_Appended as tasks complete — see `docs/SOURCES.md` for the full citation table._
