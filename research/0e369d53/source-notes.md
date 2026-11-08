# Official-source research — session 0e369d53

Research date: 2026-11-08 (UTC). This file contains public aggregate data and source locations only. No owner, parcel, lease party, personal financial information, or source-page staff contact details are reproduced.

## Evidence rules

- A value is **verified** only when the official publisher displays it for the stated geography, period, unit, and adjustment basis.
- A **reported** value is a user premise, not a verified fact.
- A **derived** value is arithmetic from cited official inputs; the formula is published. It is not an official observation.
- An **official forecast** is a conditional planning projection, not a promise or a property forecast.
- An **unverified** value is blank in the public dashboard and appears on Flagged for Review. An official lookup link is not evidence that a missing value exists.
- Analysis/recommendations are labeled as judgment. They do not inherit a source's factual authority.

## Directly read official sources and findings

### Census Bureau QuickFacts, Vintage 2025

City: https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225
County: https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045225

- City population estimate July 1, 2025: 3,869,089; April 1, 2020 estimates base: 3,899,342; published change: −0.8%.
- County population estimate July 1, 2025: 9,694,934; base: 10,017,414; published change: −3.2%.
- City median household income, 2020–2024 ACS in 2024 dollars: $81,939; county: $90,112.
- City per-capita income, same ACS basis: $47,685; county: $45,792.
- City poverty: 16.5%; county: 13.3% (source estimate; do not treat as a parcel catchment).
- City median gross rent: $1,933/month; owner-occupied housing rate: 36.0%; households: 1,439,097; persons/household: 2.61. These are housing measures, not commercial rent.
- City 2022 Economic Census retail sales: 81,351,523 ($1,000); accommodation/food-services sales: 17,366,966 ($1,000). County retail sales: 213,932,785 ($1,000).
- City 2020 land area: 469.49 sq mi; population density: 8,304.2/sq mi. County land area: 4,059.28 sq mi.
- City high-school graduate or higher (age 25+): 79.6%; bachelor's or higher: 38.5%, 2020–2024 ACS.
- QuickFacts warns that sample estimates have sampling error and that vintages/methods may not be comparable.

### BLS Los Angeles Area Economic Summary, updated November 4, 2026

https://www.bls.gov/regions/west/summary/BLSSummary_LosAngeles.pdf

September 2026, not seasonally adjusted unemployment: LA city 4.5%, LA County 4.5%, LA metro area 4.4%, California 5.1%, US 4.0%. September 2025 comparators: city/county 5.9%, metro 5.5%, state 5.6%, US 4.3%.

September 2026 metro nonfarm payrolls: 6,282.1 thousand; +30.2 thousand/+0.5% year over year. Education/health services 1,340.7 thousand, +49.1 thousand/+3.8%; leisure/hospitality 782.0 thousand, +11.5 thousand/+1.5%; information 187.0 thousand, −11.4 thousand/−5.7%; manufacturing 444.8 thousand, −5.4 thousand/−1.2%; professional/business services 975.5 thousand, −5.2 thousand/−0.5%; government 734.8 thousand, −8.4 thousand/−1.1%.

September 2026 LA-area CPI-U: all items +3.7%, food +2.8%, energy +20.3% year over year. Q1 2026 LA County average weekly wage, all industries: $1,704. Geographies and adjustment bases differ by subject; do not splice them into one series.

### BLS LAUS county series and EDD September 2026 release

BLS: https://data.bls.gov/timeseries/LAUCN060370000000003?output_view=data&include_graphs=true
EDD preliminary county PDF: https://labormarketinfo.edd.ca.gov/file/lfmonth/la$pds.pdf

- BLS September 2026 preliminary NSA county: labor force 5,031,013; employment 4,806,494; unemployment 224,519; rate 4.5%.
- EDD September 2026 preliminary county SA: unemployment 4.8%; nonfarm wage/salary 4,539,800; monthly change −4,100; annual change +20,300. NSA nonfarm: 4,593,800.
- EDD NSA annual industry changes include restaurants/other eating places +7,300; accommodation/food services +8,600; leisure/hospitality +8,900.
- BLS annual city table: https://www.bls.gov/lau/city-annual-unemployment-rates.htm — LA city 2025 rate 5.8% is an 11-month average excluding October 2025 because of the federal shutdown. It is historical context, not the latest monthly headline.
- October 2025 county observations are unavailable in the BLS series. Do not impute them.

### GDP and financing context

- BEA via FRED county current-dollar GDP: https://fred.stlouisfed.org/series/GDPALL06037 — 2024: 1,002,965,029 thousand dollars; 2023: 956,211,290 thousand. Updated February 5, 2026. Derived 2024 nominal growth: 4.89%.
- BEA via FRED metro GDP: https://fred.stlouisfed.org/series/NGMP31080 — series explicitly DISCONTINUED; latest 2023: 1,295,361.403 million dollars. No 2024 observation. The canonical executive summary's $1.355T (2024) and unsupported county ranking must be removed.
- Treasury daily par yield curve, November 2026: https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202611 — November 6, 2026: 2-year 4.51%, 5-year 4.64%, 10-year 4.86%, 30-year 5.26%. These are sovereign yields, not NNN cap rates or owner discount rates.

### California DOF population projections, Baseline 2024 / Vintage 2026

Landing/method: https://dof.ca.gov/forecasting/demographics/projections/
Workbook: https://dof.ca.gov/media/docs/forecasting/Demographics/projections/P2A_County_Total.xlsx

Report P-2A, Los Angeles County row (FIPS 6037), July 1 population:
2026 9,811,358; 2027 9,778,629; 2028 9,754,806; 2029 9,733,907; 2030 9,727,305; 2031 9,723,118; 2032 9,721,552; 2033 9,720,980; 2034 9,716,390; 2035 9,708,647; 2040 9,637,524; 2045 9,536,756; 2050 9,390,823.

The workbook's About sheet identifies Vintage 2026, released March 13, 2026, with no change to Baseline 2024 assumptions. These are official projections, not Census estimates. Do not merge DOF and Census levels into a single growth series.

### SCAG Connect SoCal 2024, adopted April 4, 2024

Technical report: https://www.scag.ca.gov/sites/default/files/2024-05/23-2987-tr-demographics-growth-forecast-final-040424.pdf
Final PEIR Appendix I (updated tables): https://scag.ca.gov/sites/default/files/2024-05/appendix_i_updated_tables_508_final.pdf

Appendix I Tables 3.14-8/9/10, Los Angeles County, rounded to thousands:
- Population: 2019 10,046,000; 2030 10,214,000; 2045 10,757,000; 2050 10,793,000.
- Households: 2019 3,393,000; 2030 3,784,000; 2045 4,120,000; 2050 4,155,000.
- Employment: 2019 5,031,000; 2030 5,277,000; 2045 5,497,000; 2050 5,461,000.

Technical report Table 6, six-county SCAG region, jobs in thousands: accommodation/food service 832 (2022) → 938 (2050), published future change +12.8%; health care/social assistance 1,498 → 1,914, +27.8%; retail 842 → 844, +0.1%; transportation/warehousing 528 → 590, +11.8%. The table's manufacturing future-change cell says 153% while its endpoints 612 → 706 imply about 15.4%; flag the inconsistency and do not publish 153% as verified.

SCAG and DOF are different official planning systems/vintages. Their 2030/2050 county population paths diverge materially. Show both; do not average them, call the gap a confidence interval, or interpolate a missing SCAG 2035 value.

### Los Angeles City Planning

DTLA 2040 adoption release, December 4, 2024: https://planning.lacity.gov/odocument/92b97b24-1978-4e0e-9eae-51f22eda9e4c/Press%20Release_%20DTLA%20New%20Zoning%20Code.pdf

The release describes a seven-square-mile Downtown plan core and expectations of 100,000 new homes, 100,000 more work opportunities, and 175,000 additional residents through 2040. These are plan-area expectations, not verified outcomes and not applicable to an unidentified central-LA parcel.

Zoning search: https://planning.lacity.gov/zoning/zoning-search — ZIMAS supports parcel lookup; Chapter 1A New Zoning Code applies to the Downtown Community Plan area and subsequent plan updates. Parcel match is required before assigning zoning.

### Schools / community context

California School Dashboard, Los Angeles Unified, 2026:
https://www.caschooldashboard.org/reports/19647330000000/2026/academic-engagement
https://www.caschooldashboard.org/reports/19647330000000/2026/academic-performance

- Combined four-/five-year graduation rate: 87.6%, +1.1 percentage points; cohort students 28,831.
- Chronic absenteeism: 21.3%, declined 0.6 percentage points; TK–8 denominator 254,681.
- ELA distance from proficient: 13.2 points below, improved 4.6 points; mathematics: 40.7 points below, improved 8.2 points.
- 2025 comparators: graduation 86.5%; chronic absenteeism 21.9%; ELA −17.8; math −48.9.

District assignment, attendance boundary, school-level results, enrollment trend, and relevance to this restaurant's customer base remain unverified. District outcomes are community context, not a property rating.

### Tenant / issuer context (not the subject lease)

FY2025 10-K: https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm
Q3 FY2026 10-Q: https://www.sec.gov/Archives/edgar/data/807882/000080788226000091/jack-20260705.htm
Q3 FY2026 earnings release filed with SEC: https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm

- FY2025 Jack in the Box system: 2,136 restaurants across 22 states; California 351 (94 company, 257 franchise). Derived California share 16.4%. The 941 California figure sometimes quoted combines Jack in the Box and Del Taco and must not be labeled Jack-only.
- Q3 FY2026 (12 weeks ended July 5, 2026): Jack system same-store sales −1.1%; franchise −1.2%; company −0.9%. Systemwide sales −1.4%.
- Q3 restaurant count: 2,115 (149 company, 1,966 franchise); 4 openings, 17 closures, net −13.
- Q3 revenue $257.657M; continuing-operations net earnings $21.041M; total net earnings $20.122M after discontinued-operations loss. Adjusted EBITDA $61.2M is non-GAAP.
- July 5, 2026 balance sheet: cash $46.318M; restricted cash $25.453M; current debt maturities $44.160M; long-term debt net of current maturities $1,428.667M; stockholders' deficit $901.286M. Operating lease liabilities are separate and must not be added to debt without explanation.
- Q3 refinancing: $500M Series 2026-1 Class A-2 Notes, anticipated repayment May 2031; existing 2019-1 notes repaid. Anticipated repayment date is not a simple legal maturity.
- FY2026 guidance in the August release: approximately 2,100 Jack restaurants; about 25 openings and 50–60 closures, mostly franchise. Guidance is not an actual result.
- Del Taco sale completed December 22, 2025; its results are discontinued operations. Do not mix old combined-brand metrics with current Jack-only metrics.

The legal tenant, guarantor, rent, options, notices, repair allocation, insurance, and assignment provisions for the reported property are not in these issuer-wide sources.

### Taxes, wages, and transaction rules

- LA Finance ULA FAQ: https://finance.lacity.gov/faq/measure-ula — for transactions closing after June 30, 2026, thresholds $5,400,000 and $10,900,000; additional ULA rates 4% above the lower threshold and below the upper, 5.5% at/above upper. City base rate displayed as 0.45% (rounded from $2.25 per $500 or fraction). Applicability/exemptions and closing-date rules require review. County documentary transfer tax and allocation are separate.
- LA Assessor Proposition 13: https://assessor.lacounty.gov/real-estate-toolkit/proposition-13 — general levy limited to 1% of assessed value plus voter-approved/direct assessments; annual assessed-value increase generally capped at 2% except reassessment events. Actual bill and reassessment treatment unknown.
- FTB: https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html — California has no lower capital-gains rate for individuals; gains taxed as ordinary income. Entity/owner treatment unknown.
- IRS Publication 544: https://www.irs.gov/publications/p544 — adjusted basis, amount realized, depreciation-related gain treatment; no owner tax estimate possible.
- IRS Form 8824 instructions: https://www.irs.gov/pub/irs-pdf/i8824.pdf — deferred like-kind real-property exchange: identify replacement within 45 days; receive within 180 days or tax-return due date including extensions, whichever earlier. Boot can trigger gain; eligibility and California conformity require professional review.
- CA DIR fast-food FAQ: https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm — covered fast-food employees at least $20.00/hour effective April 1, 2024; coverage includes qualifying chains with at least 60 establishments nationwide.
- CA DIR general minimum wage: https://www.dir.ca.gov/dlse/faq_minimumwage.htm — $16.90/hour January 1, 2026, unless higher industry/local rule applies.
- LA Office of Wage Standards notice: https://wagesla.lacity.gov/sites/g/files/wph1941/files/2026-04/MWO-Notice-2026%208x11%20-%20English%20ADA260304.pdf — city general minimum $18.42/hour July 1, 2026. The higher applicable standard governs; do not add rates together.

### Hazards and insurance

FEMA NRI overview: https://www.fema.gov/flood-maps/products-tools/national-risk-index
FEMA-owned county layer metadata: https://fema.maps.arcgis.com/home/item.html?id=39485e8035d446a5bff03259508ae355
Direct official FEMA county query used:
https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0/query?where=STCOFIPS%3D%2706037%27&outFields=COUNTY,STCOFIPS,RISK_SCORE,RISK_RATNG,EAL_SCORE,EAL_VALT,EAL_VALB,SOVI_SCORE,SOVI_RATNG,RESL_SCORE,RESL_RATNG,ERQK_RISKS,ERQK_RISKR,ERQK_EALT,WFIR_RISKS,WFIR_RISKR,WFIR_EALT,IFLD_RISKS,IFLD_RISKR,IFLD_EALT&returnGeometry=false&f=json

NRI v1.20 (December 2025), Los Angeles County: composite risk score 100, Very High; total expected annual loss $7,601,846,373.16; building EAL $5,946,330,343.43; social vulnerability score 55.3753, Relatively Moderate; resilience score 13.5496, Very Low. Earthquake risk score 100/Very High, EAL $4,565,736,367.02; wildfire 99.9364/Very High, EAL $155,191,812.04; inland flooding 100/Very High, EAL $2,808,736,523.86. These resolve the prior audit's unreadable-value flags. They are county relative/model metrics, not parcel losses or annual premiums.

A second official query returned all 18 hazard ratings. Notable county ratings: heat wave Relatively High; landslide Relatively High; lightning Very High; tornado Relatively High; drought Relatively Low; tsunami Relatively Low; hurricane No Rating; ice storm/volcanic activity Not Applicable. Do not convert ratings into invented probabilities.

USGS FAQ: https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-los-angeles-area-san-francisco-bay-area — UCERF3 30-year LA-region probabilities: M≥6.7 60%, M≥7 46%, M≥7.5 31%. The FAQ does not state a start date; do not label it a fresh 2026–2056 forecast. The linked old fact-sheet PDF returned 404; use the live FAQ and flag vintage/start-date limitation.

CAL FIRE/OSFM FHSZ: https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones
Official acreage PDF linked there: https://34c031f8-c9fd-4018-8c5a-4159cdff6b0d-cdn-endpoint.azureedge.net/-/media/osfm-website/what-we-do/community-wildfire-preparedness-and-mitigation/fire_hazard_severity_zone_acres_state_and_local_responsibility_2024_2025.pdf?rev=d1f74280dd01402f841bf2da5d5fc8cd&hash=EC6CA86D1AF5094D808CB341A328C52F

LA County combined SRA/LRA acres: moderate 330,431; high 77,951; very high 769,561; total mapped 1,177,944. Derived very-high share of mapped acres 65.3%. This is not a share of all county land and not a parcel assignment. SRA effective April 1, 2024; LRA acres transmitted March/April 2025. The page also announces a 2026 SRA public-comment update; adoption/local status must be checked. Prior 26%/35% expansion claims remain unverified and withheld.

California DOI tracker: https://www.insurance.ca.gov/01-consumers/180-climate-change/Wildfire-Claims-Tracker.cfm — updated July 6, 2026: Eaton/Palisades 41,727 claims filed; 40,482 partially paid; $25.2B paid to date. Includes home, business, living expense, auto and other disaster claims; not commercial-property-only losses.

LAPD crime mapping: https://www.lapdonline.org/office-of-the-chief-of-police/office-of-special-operations/detective-bureau/crime-mapping-and-compstat/ — official page says platform feed is being updated and links bureau/area PDFs. No parcel-level crime rate inferred.

Port of Los Angeles statistics hub: https://www.portoflosangeles.org/business/statistics — official cargo/cruise/automobile/tonnage series exist; port exposure is a regional driver, not evidence of this site's customer traffic. No port volume is needed for the decision and none is inferred.

## Projection and decision method

1. Publish DOF's official annual county population path through 2035 and SCAG's official county milestone path separately. Compute only transparent changes/CAGRs/index values from those inputs.
2. Do not interpolate missing years, blend agencies, assign regional growth to the parcel, or turn population growth into rent/cap-rate growth.
3. Stress the lease with symbolic rent interruption, owner-cost leakage, re-tenanting capital, exit-value, discount-rate, and tax changes. Magnitudes/probabilities stay blank without evidence.
4. Compare verified after-tax net sale proceeds with probability-weighted, after-tax hold/renew/exit cash flows only when all required inputs have evidence. Otherwise output blank, not zero.
5. Provisional decision: prepare sale and renewal in parallel; preserve notice/option rights; avoid an irreversible choice or passive drift to expiry without a funded re-tenanting plan. No definitive property-specific verdict is supportable.

## Repository / privacy / deployment observations

- Baseline tracked inventory: 129 text files, 25,717 lines. Every tracked text file was inventoried and scanned line by line for contact patterns, parcel identifiers, conflict markers, and external domains; canonical pages were reviewed individually. Historical numerical claims are not certified merely because they exist in the repository.
- No visible email/phone matches or explicit APN values were found in the tracked baseline. Candidate street/owner regex hits were reviewed and were false positives (template prose, EDGAR query parameter `owner=include`, or placeholders). No personal information is copied into this report.
- Exact Git conflict-marker scan must anchor `<<<<<<<`/`>>>>>>>`; a naive `=======` scan falsely flags archived CSS separators. No actual conflict markers were identified in the baseline.
- Historical builds contain nonofficial citations and unsupported/invented financial assumptions. They are preserved in Git/archives but excluded from the curated public artifact.
- `scripts/verify-data.mjs` is an obsolete architecture gate (five failures against the canonical site); it is not a current data-quality signal.
- GitHub Pages API at research time: public repository, `build_type: legacy`, source `main /`, HTTPS enforced. Local integration token's PUT to `build_type=workflow` returned HTTP 403. A successful Actions upload is not proof that the legacy site serves that artifact. The workflow token's Pages permission must be tested; if unavailable, publication must still prevent uncurated legacy exposure before claiming completion.
- Live legacy root was fetched and still contained the stale executive-summary GDP contradiction. Historical root pages/archives remain reachable under legacy serving.
