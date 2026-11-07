# Official-source verification ledger — session `arena/dac604b9-jack1`

Verification date: 2026-11-07 (UTC). Internal research file; **not published on the website**.
The published, reviewable form of this ledger is `sources.html` plus the per-row source links in
every table. Machine-readable form: `data/brief_sources.json`, `data/brief_rows.json`,
`data/brief_flags.json`.

Rule applied: a value appears in the dataset **only** if the exact figure, its unit, its date and
its geography were read on the official publisher's page named in that row's source link. If a
value could not be confirmed, the cell is empty and the row is flagged `unverified` (`U-<row id>`)
and appears on `flagged.html`. Nothing was inferred, interpolated, estimated or copied from a
prior session's dataset without re-reading the publisher.

## 1. Publishers read line by line

| Source id | Official URL | Values verified for this build |
| --- | --- | --- |
| `CEN_CITY` | https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225 | V2025 pop `3,869,089`; 2020 base `3,899,342`; change `−0.8%`; 2020 Census `3,898,747`; 2010 `3,792,621`; under 18 `19.2%`; 65+ `14.2%`; Hispanic/Latino `47.2%`; foreign-born `35.7%`; language other than English `56.4%`; same house 1 yr `89.3%`; households `1,439,097`; persons/household `2.61`; owner-occupied `36.0%`; median value `$921,200`; median gross rent `$1,933`; owner costs w/ mortgage `$3,497`; bachelor's+ `38.5%`; HS+ `79.6%`; median HH income `$81,939`; per capita `$47,685`; poverty `16.5%`; mean travel `30.7` min; accommodation/food sales `$17,366,966k`; retail sales `$81,351,523k`; retail/capita `$21,281`; density `8,304.2`; land area `469.49`; FIPS `0644000`. City-level business fields show `[X]` (IR-D13). |
| `CEN_CTY` | https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045225 | V2025 pop `9,694,934`; 2020 base `10,017,414`; change **`−3.2%`**; 2020 Census `10,014,009`; 2010 `9,818,605`; 65+ `17.1%`; Hispanic/Latino `49.3%`; foreign-born `33.4%`; housing units `3,726,923`; building permits `22,250`; households `3,416,449`; persons/household `2.81`; owner-occupied `45.9%`; median value `$834,200`; median gross rent `$1,954`; bachelor's+ `36.0%`; median HH income `$90,112`; per capita `$45,792`; poverty `13.3%`; mean travel `30.4`; accommodation/food sales `$44,000,801k`; retail sales `$213,932,785k`; retail/capita `$22,010`; health care/social assistance receipts `$113,488,435k`; transportation/warehousing `$65,350,932k`; employer firms `251,405`; employer establishments `304,988`; employment `3,987,736`; annual payroll `$299,616,607k`; employment change `2.3%`; nonemployer establishments `1,165,040`; density `2,466.9`; land area `4,059.28`; FIPS `06037`. |
| `BLS_EAG` | https://www.bls.gov/eag/eag.ca_losangeles_msa.htm | Data extracted Nov 6 2026. Sep 2026 (preliminary) labor force `6,646.9k`, employment `6,352.9k`, unemployed `294.0k`, unemployment `4.4%` (Aug `4.8%`); total nonfarm `6,282.1k`, `+0.5%` y/y; CPI-U index `358.725` and `+3.7%` y/y. Sectors Sep 2026: education/health `1,340.7k` `+3.8%`; leisure/hospitality `782.0k` `+1.5%`; trade/transport/utilities `1,047.9k` `+0.3%`; professional/business `975.5k` `−0.5%`; information `187.0k` `−5.7%`; manufacturing `444.8k` `−1.2%`; construction `251.5k` `0.0%`; government `734.8k` `−1.1%`. |
| `BLS_CITY` | https://www.bls.gov/lau/city-annual-unemployment-rates.htm | LA city annual unemployment 2021 `9.0`, 2024 `5.9`, 2025 `5.8`; 2025 is an 11-month average excluding October (IR-D5). |
| `BLS_CPI` | https://www.bls.gov/regions/west/news-release/consumerpriceindex_losangeles.htm | Sep 2026 LA area: all items `+0.5%` month / `+3.7%` year; core `+2.6%` year; food away from home `+2.8%` year; energy `+20.3%` year; October 2025 data unavailable; next release Nov 10 2026. |
| `BEA_2024` | https://www.bea.gov/news/2026/gross-domestic-product-county-and-personal-income-county-2024 | BEA 26-08 (Feb 5 2026): 2024 LA County **personal income** `$818.5 billion`; BEA discontinued MSA/metro-division GDP and personal income statistics with the 2024 estimates (IR-D2, IR-D7). |
| `BEA_2023` | https://www.bea.gov/news/2024/gross-domestic-product-county-and-metropolitan-area-2023 | BEA 24-57 (Dec 4 2024): 2023 LA County real GDP `$802.0 billion` (chained 2017 dollars); page marked "superseded". |
| `DOF_E1` | https://dof.ca.gov/media/docs/forecasting/demographics/estimates/e-1_2026_press_release.Pdf | May 1 2026: CA population `39,593,000` (`−0.14%`); LA County `9,837,286` on Jan 1 2026 vs `9,900,914` Jan 1 2025 (`−0.6%`); City of LA `3,806,201` vs `3,839,536` (`−0.9%`); statewide housing `15,064,131` (`+115,165`); `11,160` units lost to Eaton/Palisades; LA County lost ~`64,000` persons (fire, Inland Empire migration, deportations). |
| `SCAG_DEM` | https://www.scag.ca.gov/sites/default/files/2024-05/23-2987-tr-demographics-growth-forecast-final-040424.pdf | Adopted Apr 4 2024; horizon 2050; "Slower Growth, Steady Improvement"; RHNA `1,341,827` units; regional population peak `18,966,261` (Jan 2019 DOF); 2022 employment matched 2019 peak, `447,000` jobs above 2016 base year; 2023 `51,770` new units; ages 0–17 `4.2M`→`3.8M` / `22.5%`→`18.1%`; 65+ `2.7M`→`4.5M` / `14.4%`→`21.7%`; 2050 total headship rate `44.8%`. Exact county Table 12 2050 values were **not** extracted, so none is published. |
| `EDD_LA` | https://labormarketinfo.edd.ca.gov/cgi/databrowsing/localAreaProfileQSResults.asp?selectedarea=Los+Angeles+County&selectedindex=19&state=true&geogArea=0604000037&submit1=View+Local+Area+Profile | 2023–2033 occupational projections: Nurse Practitioners `+48.8%` (`4,490`→`6,680`); Home health/personal care aides `+34.8%` (`289,930`→`390,820`); Data scientists `+33.7%`; Solar PV installers `+36.4%`; Cooks, restaurant `+32.7%` (`40,760`→`54,070`); 2025 permits `20,192` / `$4,197,975,040`. The page explicitly reports "Data for Los Angeles County not available" for unemployment, labor force and employment by industry (IR-D6). Its "Median Price of Existing Homes Sold" table is misaligned with CPI-like values — **not used**. |
| `CDE_LAUSD` | https://www.cde.ca.gov/sdprofile/details.aspx?cds=19647330000000 | LAUSD 2025–26 enrollment `497,105`; English learners `81,328` (`16.4%`); CDS `19 64733 0000000`. |
| `CDE_LARGE` | https://www.cde.ca.gov/ds/ad/ceflargesmalldist.asp | Statewide 2025–26 enrollment `5,731,260`; LAUSD largest district. |
| `CASD_2025` | https://www.caschooldashboard.org/reports/19647330000000/2025/academic-engagement | LAUSD 2025 graduation `86.5%`, 2024 `86.7%`; state 2025 `87.8%`. |
| `DIR_FF` | https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm | AB 1228 `$20.00/hr` effective Apr 1 2024; chains of ≥60 establishments; applies to brand owners, franchisees and licensees; exempt salary threshold `$83,200`; local higher **general** minimum wage may apply (IR-D3-adjacent caveat). The URL `.../Fast-Food-Minimum-Wage.htm` returned 404 — do not cite. |
| `ULA_FAQ` | https://finance.lacity.gov/faq/measure-ula | Base transfer tax `0.45%` (`$2.25/$500`); ULA `4%` / `5.5%` on top; thresholds `$5,400,000` / `$10,900,000` for conveyances after Jun 30 2026; effective Apr 1 2023; thresholds indexed annually by BLS Chained CPI; exemptions under LAMC §§21.9.14/21.9.15; prorated where only part of the property is in the City. |
| `FRED_10` | https://fred.stlouisfed.org/series/DGS10 | `4.84%` on 2026-11-05; `4.90%` 11-04; `4.95%` 11-03; updated Nov 6 2026. |
| `FRED_30` | https://fred.stlouisfed.org/series/DGS30 | `5.25%` on 2026-11-05; `5.28%` 11-04. |
| `TREASURY` | https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026 | 2026 daily par yield curve (214 entries); methodology page. The CSV endpoint returned HTTP 500 and `page=7`/`page=8` returned "No Results Found" — FRED was used for exact recent observations instead. |
| `SEC_10K` | https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm | FY2025: `2,136` Jack in the Box restaurants (`1,986` / `93%` franchised); Del Taco `576`; `Jack on Track` pillars include a restaurant closure programme, Del Taco alternatives and accelerated cash flow; discontinuing the dividend; franchise agreement generally `$50,000` fee / 20-year term / `5%` royalty+marketing; site selection uses demographics, traffic, competition, visibility, parking; CRAVED prototype ~`1,372` sq ft. |
| `SEC_Q4FY25` | https://www.sec.gov/Archives/edgar/data/807882/000080788225000070/ex991-q425earningsrelease.htm | Q4 SSS `−7.4%`; FY2025 SSS `−4.2%`; Q4 systemwide sales `−7.2%`; Q4 `15` openings / `47` closures (`38` from the `JACK on Track` block closure programme); FY2025 `31` openings / `86` closures; Q4 end count `2,136` (`150` company, `1,986` franchise); restaurant-level margin `16.1%`; franchise-level margin `38.9%`. |
| `SEC_Q3FY26` | https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm | Q3 ended Jul 5 2026: system SSS `−1.1%` (company `−0.9%`, franchise `−1.2%`), prior year `−7.1%`; systemwide sales `−1.4%`; revenue `$257.7M` vs `$262.4M`; restaurant-level margin `$17.0M` / `17.6%`; franchise-level margin `$60.3M` / `37.4%` vs `$66.2M` / `39.3%` (lower rent/royalty revenue and fewer restaurants under the closure programme); higher bad-debt expense; `4` openings / `17` closures; count `2,115` (`149` company, `1,966` franchise) vs `2,168`; net earnings `$21.0M` vs `$22.8M`; adjusted EBITDA `$61.2M` vs `$57.1M`; EPS `$1.08`; Del Taco sale completed Dec 22 2025. |
| `USGS_UCERF3` | https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-los-angeles-area-san-francisco-bay-area | LA region 30-year probabilities: M6.7 `60%`, M7 `46%`, M7.5 `31%`. Regional, not parcel-specific. |
| `USGS_NSHM` | https://www.usgs.gov/programs/earthquake-hazards/science/2023-50-state-long-term-national-seismic-hazard-model-0 | Revised 2023 50-state NSHM adopted in 2026 NEHRP provisions; probabilistic ground shaking, not a building rating. |
| `OSFM_FHSZ` | https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones | Classifications Moderate / High / Very High; hazard over 30–50 years; SRA effective Apr 1 2024; 2025 LRA rollout Feb 10 / Feb 24 / Mar 10 / Mar 24 2025; 2026 SRA public comment open. Parcel address required. |
| `LACO_FIRES` | https://file.lacounty.gov/SDSInter/lac/1199046_Eaton_Palisades_Fires_Anniversary_Fact_Sheet.pdf | Eaton `14,021` acres / `9,414` destroyed / `1,074` damaged / `19` fatalities; Palisades `23,448` acres / `6,837` destroyed / `973` damaged / `12` fatalities; combined `16,251` destroyed; economic output lost `$5.2B–$10.1B`; ~`6,800` businesses and ~`47,000` workers impacted; labor income lost `$2.2B–$4.2B`; tax revenue losses `$900M–$1.6B`. |
| `CDI_ORDER` | https://www.insurance.ca.gov/0250-insurers/0500-legal-info/0700-commissioners-orders/upload/Order-No-2025-1-Approving-the-California-FAIR-Plan-Association-s-Request-to-Issue-Assessment.pdf | As of Feb 9 2025: `3,469` Palisades + `1,325` Eaton claims; `$914M` paid; `$3.251B` reserved; total loss estimated ~`$4B`; `$1B` assessment approved Feb 11 2025. |
| `CDI_ALERT` | https://www.insurance.ca.gov/0400-news/0102-alerts/2025/Commissioner-Lara-Launches-Investigation.cfm | Nearly `$17B` in claims paid to residential and commercial policyholders impacted (as of May 12 2025); >`$40M` recovered via complaints; formal market-conduct investigation and smoke-damage task force. |
| `ASSESSOR_ROLL` | https://assessor.lacounty.gov/news-information/assessmentroll | July 13 2026 roll release memo: gross roll `$2.367 trillion`; net taxable `$2.272 trillion` (`+4.42%`, sixteenth consecutive increase); `2,399,978` taxable parcels; downtown office declines >50% on some sales; ~16,000 Prop 8 decline-in-value parcels. |
| `ASSESSOR_P13` | https://assessor.lacounty.gov/homeowners/realproperty | Prop 13 max levy `1%` of assessed value plus bonded indebtedness/direct assessments; assessed-value growth limited to `2%` annually absent change of ownership or new construction. |
| `METRO_DLINE` | https://www.metro.net/projects/westside/ | D Line Extension Section 1 opened **May 8 2026** (Wilshire/La Brea, Wilshire/Fairfax, Wilshire/La Cienega); Sections 2 and 3 in construction. The old URL `/projects/d-line-extension/` returned Page not found — replaced. |
| `IRS_544` | https://www.irs.gov/publications/p544 | General rule source for dispositions; no owner-specific tax result computed. |
| `FTB_GAINS` | https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html | CA capital-gain guidance; no owner-specific result. |
| Lookup tools | `ZIMAS`, `PLAN_ZONING`, `PLAN_DTLA`, `ASSESSOR_PORTAL`, `AUDITOR_TRA`, `TTC`, `CGS_EQZ`, `FEMA_FLOOD`, `FEMA_NRI`, `LACO_FLOOD`, `LACO_FHSZ`, `EPA_CLEANUP`, `GEOTRACKER`, `LADWP`, `LAPD`, `PH_HEAT`, `CLIMATE`, `SEC_EDGAR`, `CDE_ACCT`, `DOF_EST`, `IRS_HOME`, `FIRE_EATON`, `FIRE_PAL` | Each is an official publisher's lookup tool used as the source link for a **blank** cell. No value is asserted from them. `FEMA_NRI` is an interactive tool with no static official county figure (IR-D10). |

## 2. Dead ends and contradictions (not published as values)

- Treasury 2026 CSV → HTTP 500; paginated `TextView` pages 7/8 → "No Results Found". Used FRED
  series pages for exact observations instead.
- `https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage.htm` → 404. Correct FAQ URL used.
- `https://www.metro.net/projects/d-line-extension/` → Page not found. Correct `/projects/westside/`.
- EDD LA County profile: county unemployment/labor force/industry employment "not available"; the
  "Median Price of Existing Homes Sold" table is visibly misaligned with CPI-like numbers and a
  CAR attribution. Not used.
- SCAG PDF: exact county Table 12 2050 population/employment values were not extracted. Prior
  session's IR-02 (`+7%` adopted vs `−5%` 2025 draft) was **not** independently verified and is
  not published here.
- Prior session's NCES `408,026` LAUSD enrollment figure was not verified; only CDE `497,105` is
  published (IR-D14).
- Prior session notes flagged `2,136` vs `~2,135` press-release restaurant counts. The dated
  FY2025 10-K (`2,136` at Sep 28 2025) and Q3 FY2026 release (`2,115` at Jul 5 2026) reconcile it
  (IR-D8).
- SEC filings are issuer/brand-level. **No** filing identifies the subject property, legal tenant,
  guarantor, lease, rent, unit sales, franchise agreement expiry or closure-list membership. Those
  cells are blank and flagged.
- USGS probabilities, CAL FIRE FHSZ, FEMA/LA County hazard maps, LA County fire losses and CDI
  insurance figures are **regional/contextual**, not parcel ratings.
- BLS Oct 2025 city CPI-U missing; 2025 city unemployment is an 11-month average.
- `data.census.gov/profile?g=050XX00US06037` returns `10,014,009` / `$92,404` from a different
  vintage/universe — not blended with QuickFacts V2025.
- PR #14's `docs/SOURCES.md` reports 26 rows with no official publisher. None of those rows was
  imported.

## 3. Privacy verification

The dataset contains no street address, APN, owner name, ownership entity, tenant legal name,
guarantor name, lease document, rent figure, personal financial figure, personal email or personal
phone number. The property is described only as "an anonymized Jack in the Box NNN-leased property
around central Los Angeles" with a reported lease-expiry window of 2030–2035. All parcel-specific
fields are blank. A regex pass over the generated canonical pages checks for emails, phone numbers,
APN-like identifiers, street-address patterns and person-name labels. `privacy.html` explains the
posture publicly. Internal research files under `research/` are not part of the published artifact.

## 4. Result

`tools/build_dataset.py` produced **315 rows**: **229 verified** from the publishers above and
**86 blank/flagged** (`U-<row id>`), from **59 official sources**, plus **17 irregularities**
(IR-D1 … IR-D17). Every row has at least one official source link. `tools/verify_brief.py` enforces
that invariant on the generated HTML and on the dataset, checks links, IDs, PII and the deploy
artifact. No value with an empty cell was filled in.
