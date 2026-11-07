# Verification report

Generated from `python3 tools/check.py` on 2026-11-06.

```
pages: 9  |  facts: 121  |  sources: 22  |  scenarios: 9
  · checked 245 links across 9 pages
  · PII scan: 16 files, 0 hits
ALL CHECKS PASSED
```

## What every check means

| Check | Method | Result |
|---|---|---|
| Internal links | Parse every `<a href>`; verify the target page exists and the `#anchor` exists in that page | pass |
| Source coverage | Every `verified`/`derived` fact row must list ≥1 source ID that exists in the ledger; every `unverified` row must be blank or `[WITHHELD]` | pass |
| Source resolution | No fact references a source ID absent from `data/sources.json` | pass |
| PII | Regex scan for SSN, card-like numbers, separated phone numbers, email addresses, street addresses and APN patterns across site, data, assets and documents (CIK numbers from SEC URLs whitelisted by context) | 0 hits |
| HTML structure | Exactly one `<h1>` per page; balanced tags; no external `src`/`href` on assets | pass |
| Placeholders | No TODO/FIXME/lorem/XXX/PLACEHOLDER tokens | pass |
| Model sanity | Strategies A–E present in all 9 scenarios; net proceeds never exceed gross price; no negative tax | pass |

## Line-by-line spot audit performed manually

Each of these was re-opened and compared against the site's rendering:

* 10-year Treasury **4.90%** (2026-11-04) vs FRED DGS10, sourced to the Fed's H.15 release — matches.
* Fed funds **3.75–4.00%** vs the Fed's open-market-operations table, single 2026 entry 17 Sep +25bp — matches.
* CPI **+3.7%** / core +2.6% vs BLS USDL-26-1574 (September 2026) — matches.
* LA MSA unemployment **4.4%** (Sep 2026, preliminary) vs BLS Economy at a Glance — matches, and the
  preliminary flag is carried through to the site.
* LA city population **3,869,089** and −0.8% vs Census QuickFacts V2025 — matches; the −3.2% county figure
  and 2020 base are shown alongside so the base is auditable.
* Median household income **$81,939** (2024 dollars) — matches QuickFacts, and the "2024 dollars" qualifier
  is preserved.
* JACK Q3 FY2026: comps −1.1%, 2,115 restaurants, 17 closures, guidance 50–60 closures — all match the
  Exhibit 99.1 filed 2026-08-12; the quoted phrase "most of which will be franchise restaurants" is verbatim.
* Measure ULA **4% / 5.5%** at **$5.4M / $10.9M** — matches both the City of Los Angeles Office of Finance FAQ
  and the County Recorder's rate table (the latter showing the prior-year $5.3M/$10.6M, which is how the
  annual indexation was confirmed rather than assumed).
* County transfer tax **$0.55 per $500** and the $1.10 per $1,000 special-city line — matches lavote.gov.
* Prop 13 **2%** cap — verified in the text of California Constitution Article XIII A, not from a summary.
* FAIR Plan **$724bn**, **668,609** policies, **21,717** commercial, **$100M/$20M** commercial limits,
  **~5,400 claims / ~$3.5bn** — all match the Assembly Insurance Committee presentation.
* CAL FIRE 2026 YTD **6,389 fires / 339,481 acres / 177 structures** and the below-normal Southern California
  outlook through February 2027 — match the live dashboard on the access date.
* NCES **408,026 students / 784 schools / 19.20 ratio / $34,533 revenue per student** — match the district
  detail page.

## Values deliberately left blank (12)

Address, APN/assessed value, building and land area, rent/NOI, lease dates and options, tenant of record,
NNN scope, escalation clause, parcel FHSZ, FEMA flood zone, seismic/liquefaction/Alquist-Priolo, zoning,
school assignment, retail rents, cap-rate comps, the 2026 fast-food wage change, JACK's California share,
unit-level AUV, insurance premium, and the CDE enrolment figure.

Each has a note on the site stating exactly what would fill it.

## Irregularities logged

1. CDE DataQuest district-enrolment endpoint returned a generic error page; federal NCES used instead.
2. Two LA County Assessor URLs (Prop 13, Prop 19) redirected to the homepage; Prop 13 verified against the
   Constitution instead, Prop 19 not cited.
3. California Geological Survey Alquist-Priolo page returned 404; seismic site data left blank and flagged.
4. IRS Section 1031 source is marked archival by the IRS itself; flagged for CPA confirmation.
5. USGS 2023 NSHM science page returned 404 at one URL; the Earthquake Hazards Program landing page was
   verified and is what is cited.
6. Third-party school-enrolment aggregators disagreed by more than 20% for the same year; none used.
7. Fast-food minimum wage change during 2026 could not be confirmed from an official page; secondary
   commentary exists but was not adopted.
