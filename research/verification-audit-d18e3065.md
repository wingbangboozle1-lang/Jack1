# Verification audit — session d18e3065 (2026-11-07 UTC)

Scope: line-by-line check of the numeric and factual claims on the seven public pages (`index`, `market`, `property`, `decision`, `risks`, `flagged`, `sources`), plus a privacy scan and a repository review. Board task: **T18**.

Method: each figure was re-read from the official page named in its row (Census QuickFacts, BLS, Los Angeles Office of Finance, SEC EDGAR, SCAG, City Planning, CAL FIRE/OSFM, California Department of Insurance, LAPD, NOAA Climate.gov, California EDD). Where a figure could not be read from the official page in this session, it is marked **not confirmed** and listed on the Flagged for Review page. No value was inferred or filled in.

Limits of this audit: the verification tools reach only a subset of the web, and some government pages are long and were read in chunks. Not every one of the roughly 50 unique external links was re-opened in this session; links not listed below were not re-checked here and keep their previous status.

## A. Figures re-verified against the official page

| # | Published figure (page) | Official source read | Result |
|---|---|---|---|
| A1 | Population 3,869,089, July 1, 2025 (index, market) | [Census QuickFacts — Los Angeles city](https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225) | Verified |
| A2 | Population change −0.8%, Apr 2020 base to Jul 2025 (index, market) | same | Verified |
| A3 | Median household income $81,939, 2020–2024, 2024 dollars (index, market) | same | Verified |
| A4 | Median gross rent $1,933 (market) | same | Verified |
| A5 | Owner-occupied housing 36.0% (market) | same | Verified |
| A6 | Density 8,304.2 per sq. mi., 2020 (market) | same | Verified |
| A7 | Retail sales $81.35 billion, 2022 (market); table value 81,351,523 thousand | same | Verified |
| A8 | Accommodation and food services $17.37 billion, 2022 (market); table value 17,366,966 thousand | same | Verified |
| A9 | Unemployment 5.8%, 2025 annual average, 11 months (index, market) | [BLS Unemployment Rates for 50 Largest Cities](https://www.bls.gov/lau/city-annual-unemployment-rates.htm) | Verified; BLS footnote excludes October 2025 as published |
| A10 | Measure ULA thresholds $5,400,000 and $10,900,000 for closings after June 30, 2026; ULA rates 4% and 5.5%; base rate 0.45% (decision, flagged, risks, sources) | [LA Office of Finance — Measure ULA FAQ](https://finance.lacity.gov/faq/measure-ula) | Verified from the effective-date note and rate table. This closes prior open item U-09 for the site's use. Irregularity noted in section C. |
| A11 | SCAG Connect SoCal 2024: LA County employment 5,031,000 (2019) → 5,461,000 (2050) (market) | [SCAG Demographics & Growth Forecast technical report](https://www.scag.ca.gov/sites/default/files/2024-05/23-2987-tr-demographics-growth-forecast-final-040424.pdf), Table 2 | Verified |
| A12 | SCAG LA County population 10,046,000 (2019) → 10,793,000 (2050) (market) | Adopted Final Program EIR, Appendix I, Tables ES-1 & 2-1 (state CEQA clearinghouse attachment, `files.ceqanet.lci.ca.gov`, not on the site's allowlist, so not linked) | Verified against the PEIR table. Table 12 of the forecast PDF could not be read in this session; the press-release conflict is listed in section C. |
| A13 | Regional job additions 2022–2050: health care +416,000; construction +148,000; accommodation and food +106,000 (market) | SCAG forecast PDF, Table 6 (2022 vs 2050 jobs, thousands: health care 1,498 → 1,914; construction 473 → 621; accommodation and food 832 → 938) | Verified (differences computed from the table) |
| A14 | DTLA 2040: 100,000 homes; 100,000 work opportunities; 175,000 additional residents through 2040 (market) | [LA City Planning press release, Dec 4, 2024](https://planning.lacity.gov/odocument/92b97b24-1978-4e0e-9eae-51f22eda9e4c/Press%20Release_%20DTLA%20New%20Zoning%20Code.pdf) | Verified (described as expectations, as on the site) |
| A15 | Jack in the Box Q3 FY2026 (12 weeks to July 5, 2026): revenue $257,657k vs $262,401k; earnings from continuing operations $21,041k vs $22,839k; YTD revenue $861,438k vs $899,196k; YTD continuing earnings $47,971k vs $74,534k (property) | [SEC Form 10-Q, quarter ended July 5, 2026](https://www.sec.gov/Archives/edgar/data/807882/000080788226000091/jack-20260705.htm), Statements of Earnings | Verified |
| A16 | Current maturities of debt $44,160k; long-term debt $1,428,667k (property) | same, Balance Sheets | Verified |
| A17 | Restaurants at July 5, 2026: 149 company-operated, 1,966 franchise-operated (property) | same, MD&A restaurant count table (total 2,115) | Verified |
| A18 | Average franchise restaurants, quarter: 1,968 (not on site; context) | same, MD&A | Noted only. Differs from the period-end count, which is the figure the site uses. |
| A19 | Tenant-credit context (added this session to risks and flagged pages): leverage ratio greater than 5.0x; senior ABS leverage greater than 5.25x; $23.3 million cash-sweep prepayments in current maturities | same, Note 7 (Indebtedness) | Verified. Issuer-level only. |
| A20 | Wildfire claims (added to risks): 41,727 claims filed; $25.2 billion paid; updated July 6, 2026; scope Eaton and Palisades fires | [CA Department of Insurance — LA County Wildfire Claims Tracker](https://www.insurance.ca.gov/01-consumers/180-climate-change/Wildfire-Claims-Tracker.cfm) | Verified. The tracker is for those two fires, not a county-wide total. |
| A21 | Fire Hazard Severity Zones: SRA map effective April 2024; LRA maps released Feb–Mar 2025 (risks) | [CAL FIRE / OSFM FHSZ](https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones) | Verified |
| A22 | LAPD crime-mapping platform "currently undergoing updates" (flagged, risks, market) | [LAPD Crime Mapping and COMPSTAT](https://www.lapdonline.org/office-of-the-chief-of-police/office-of-special-operations/detective-bureau/crime-mapping-and-compstat/) | Verified |
| A23 | Heat context: 2024 early-September heat wave; Long Beach 109°F on Sept 6 (risks, sources; not quoted as a site figure) | [NOAA Climate.gov event tracker](https://www.climate.gov/news-features/event-tracker/heat-wave-southern-california-and-southwest-early-september-2024) | Verified |

## B. Not confirmed from an official page in this session (flagged, not corrected in the table values)

| # | Item | Why not confirmed | Status on site |
|---|---|---|---|
| B1 | LA County unemployment, December 2025, not seasonally adjusted: 5.0%; labor force 5,148,900; employed 4,889,600; unemployed 259,300 (market) | The search-index copy of the [EDD county profile](https://labormarketinfo.edd.ca.gov/cgi/databrowsing/localAreaProfileQSResults.asp?selectedarea=Los+Angeles+County&selectedindex=19&state=true&geogArea=0604000037&submit1=View+Local+Area+Profile) shows these values. The live fetch did not render the table. A Los Angeles Business Journal report gives 5.6% for December 2025 as the seasonally adjusted county rate, a different series. | Values kept as published, labelled as the non-seasonally adjusted series; conflict flagged. Confirm on the live EDD page before reuse. |
| B2 | SCAG LA County 2050 population: 10.793 million vs 10.77 million in the SCAG December 2023 press release | Adopted PEIR table is later than the press release; both are SCAG. | Site uses 10,793,000; conflict flagged. |
| B3 | Los Angeles County heat-related illness data brief (`publichealth.lacounty.gov/eh/docs/about/heat-related-illness-data_brief.pdf`, http and https) | Both versions returned a page-not-found response to the verification fetch, although a search index lists the document. | Link removed from the risks and sources pages; NOAA kept as the heat source; flagged. |

## C. Irregularities flagged for review (published on the Flagged for Review page where they affect the site)

1. **EDD series conflict** (B1 above). Seasonally adjusted vs not seasonally adjusted, and a fetch that did not render the table.
2. **SCAG 2050 population conflict** (B2 above). Press release vs adopted PEIR table.
3. **Broken LA County heat link** (B3 above).
4. **Measure ULA FAQ wording.** The effective-date note gives $5,400,000 and $10,900,000 for closings after June 30, 2026, and the site uses that note. The FAQ's introductory paragraph still says "a threshold of five million dollars" and "ten million dollars". The note appears to be the controlling statement. The thresholds are indexed annually and must be checked on the closing date.
5. **Issuer-level leverage above 5.0x** (A19) is material context for the tenant-credit side of the sale-versus-renew decision. It describes the company, not the operator or guarantor of this site, which remains unverified.

## D. Privacy scan (internal)

Regex and text scan of every tracked file, including `archive/`, `data/`, `research/`, `pages/`, `site/`, and the root pages, for: email addresses, separated phone numbers, California APN patterns, street-address patterns, and owner, LLC, trust, and guarantor terms.

- Result: **no personal information found** in published or tracked content. Hits were policy statements, `[WITHHELD]` placeholders, or the public company's own corporate filings.
- The SEC 10-Q names a named individual as guarantor of the buyer of a divested brand. That is a public corporate filing fact unrelated to this property. It is not reproduced on the site.
- The site does not publish any owner, tenant, parcel, address, rent, or personal financial detail.

## E. Repository review (not published on the site)

| # | Finding | Action this session |
|---|---|---|
| R1 | `COORDINATION.md` contained six committed merge-conflict marker lines (`<<<<<<<`, `=======`, `>>>>>>>`). | Markers removed; both sides kept intact. No content deleted. |
| R2 | `scripts/verify-data.mjs` fails four assertions against the current root pages: hard-coded totals on `index.html` no longer match the 130-row dataset; `flagged.html` lead text; `property.html` and `risks.html` missing from the navigation list; one `http://` link. | Not changed. The deployed validator is `scripts/validate_site.py`, which passes. The stale gate is logged for the owner. |
| R3 | GitHub Pages build type was `legacy`, while `README.md` and the workflow expect GitHub Actions. The legacy build reported `errored` on 2026-11-06 13:17 UTC and `built` on 2026-11-07. Two deploy paths ran on each push. | Build type switched to the Actions workflow (section F). Result recorded in COORDINATION.md after deploy. |
| R4 | Open pull requests from other sessions: #5, #9, #10, #11, #14. PR #14 (`arena/d3fdafdd-jack1`, a 19-page site) is not on the board. | Not touched. Left for the owner. |
| R5 | The board's `session-<id>/<task>` branch rule conflicts with the branch Arena assigns to this session. | This session used its assigned branch only. |
| R6 | Archived builds under `archive/` and `pages/`, `site/` contain older figures (for example, 2,136 vs 2,135 restaurants in an earlier 10-K / earnings-release comparison). | Not on the public root pages. Left unchanged. |

## F. Site changes made by this session

- `risks.html`: heat rows (broken LA County link removed, NOAA kept); tenant-credit finding (A19); insurance finding (A20).
- `sources.html`: heat source row relabelled; broken link removed.
- `market.html`: EDD series note; SCAG 2050 note.
- `decision.html`: ULA verification note.
- `flagged.html`: caption date; five verification-review rows.
- `research/verification-audit-d18e3065.md`: this file.
- `COORDINATION.md`: claim, marker repair, task record.
- GitHub Pages build type: `legacy` → `workflow` (as documented in `README.md`).
