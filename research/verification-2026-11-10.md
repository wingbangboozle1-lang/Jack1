# Verification report — independent line-by-line re-read, 2026-11-10

**Session:** `arena/f046010e-jack1`
**Scope:** every figure on the ten published pages, re-read at its own official URL on 2026-11-10.
**Method:** each published value was opened at the exact source URL recorded in
`data/verified-2026-11-08.json`, compared on geography, period, unit, and adjustment basis, and then
either confirmed, corrected, or flagged. No value was copied from a secondary or aggregator page.
Numbers that the official page does not print are left blank and remain on the Flagged for Review page.

**Result: 76 of 76 published observations match their official source exactly. 0 contradictions found.
0 values corrected. 0 values invented.** Two publication defects were found and fixed, and one repo-hygiene
issue was logged without deleting anything (see §4). Five decision-relevant rows were added from official
sources that had not previously been used.

Retrieval path note: direct `curl` from this sandbox is blocked by the egress allowlist, so official
pages were read through the platform's page-fetch tool, which returns the rendered official page and
the raw JSON/CSV payloads of official data services unchanged. Machine-readable endpoints
(`fredgraph.csv`, the FEMA ArcGIS feature service, `data.sec.gov`) were used wherever the official
publisher offers one, so the comparison is against the publisher's own data, not a summary.

---

## 1. Line-by-line re-read of every published observation

| result legend | meaning |
|---|---|
| Match | the official page prints exactly the published value for that geography and period |
| Corrected | a different value is printed officially; the page was changed |
| Flagged | the official page does not print the value, is internally inconsistent, or is silent on the period |

| # | Observation id | Published value | Geography / period | Official source(s) | Re-read result |
|---|---|---|---|---|---|
| 1 | `geo_city_area` | 469.49 sq mi | City of Los Angeles · 2020 Census geography | [U.S. Census Bureau](https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225) | Match |
| 2 | `geo_city_density` | 8,304.2 people/sq mi | City of Los Angeles · 2020 Census | [U.S. Census Bureau](https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225) | Match |
| 3 | `geo_county_area` | 4,059.28 sq mi | Los Angeles County · 2020 Census geography | [U.S. Census Bureau](https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045225) | Match |
| 4 | `pop_city_2025` | 3,869,089 | City of Los Angeles · July 1, 2025 | [U.S. Census Bureau](https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225) | Match |
| 5 | `pop_city_change` | −0.8% | City of Los Angeles · April 1, 2020 base to July 1, 2025 | [U.S. Census Bureau](https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225) | Match |
| 6 | `pop_county_2025` | 9,694,934 | Los Angeles County · July 1, 2025 | [U.S. Census Bureau](https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045225) | Match |
| 7 | `pop_county_change` | −3.2% | Los Angeles County · April 1, 2020 base to July 1, 2025 | [U.S. Census Bureau](https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045225) | Match |
| 8 | `income_city` | $81,939 | City of Los Angeles · 2020–2024 ACS, 2024 dollars | [U.S. Census Bureau](https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225) | Match |
| 9 | `income_county` | $90,112 | Los Angeles County · 2020–2024 ACS, 2024 dollars | [U.S. Census Bureau](https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045225) | Match |
| 10 | `income_pc_city` | $47,685 | City of Los Angeles · 2020–2024 ACS, 2024 dollars | [U.S. Census Bureau](https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225) | Match |
| 11 | `poverty_city` | 16.5% | City of Los Angeles · 2020–2024 ACS | [U.S. Census Bureau](https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225) | Match |
| 12 | `housing_rent` | $1,933/month | City of Los Angeles · 2020–2024 ACS | [U.S. Census Bureau](https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225) | Match |
| 13 | `housing_owner` | 36.0% | City of Los Angeles · 2020–2024 ACS | [U.S. Census Bureau](https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225) | Match |
| 14 | `housing_value` | $921,200 | City of Los Angeles · 2020–2024 ACS | [U.S. Census Bureau](https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225) | Match |
| 15 | `retail_city` | $81,351,523 thousand | City of Los Angeles · 2022 Economic Census | [U.S. Census Bureau](https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225) | Match |
| 16 | `food_sales_city` | $17,366,966 thousand | City of Los Angeles · 2022 Economic Census | [U.S. Census Bureau](https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225) | Match |
| 17 | `gdp_county_2024` | $1,002,965,029 thousand | Los Angeles County · 2024; updated February 5, 2026 | [U.S. Bureau of Economic Analysis via FRED](https://fred.stlouisfed.org/series/GDPALL06037) | Match |
| 18 | `gdp_metro_2023` | $1,295,361.403 million | Los Angeles-Long Beach-Anaheim MSA · 2023; series discontinued | [U.S. Bureau of Economic Analysis via FRED](https://fred.stlouisfed.org/series/NGMP31080) | Match |
| 19 | `unemp_sep2026` | City 4.5%; County 4.5%; Metro 4.4% | City / County / Los Angeles metro · September 2026 | [U.S. Bureau of Labor Statistics](https://www.bls.gov/regions/west/summary/BLSSummary_LosAngeles.pdf) | Match |
| 20 | `unemp_comparators` | California 5.1%; United States 4.0% | State / nation · September 2026 | [U.S. Bureau of Labor Statistics](https://www.bls.gov/regions/west/summary/BLSSummary_LosAngeles.pdf) | Match |
| 21 | `laus_sep2026` | 5,031,013 / 4,806,494 / 224,519 | Los Angeles County, NSA · September 2026 preliminary | [U.S. Bureau of Labor Statistics](https://data.bls.gov/timeseries/LAUCN060370000000003?output_view=data&include_graphs=true) | Match |
| 22 | `edd_sa_sep2026` | 4.8% | Los Angeles County, SA · September 2026 preliminary | [California Employment Development Department](https://labormarketinfo.edd.ca.gov/file/lfmonth/la$pds.pdf) | Match |
| 23 | `payrolls_metro` | 6,282.1 thousand; +30.2 thousand / +0.5% YoY | Los Angeles metro area · September 2026 | [U.S. Bureau of Labor Statistics](https://www.bls.gov/regions/west/summary/BLSSummary_LosAngeles.pdf) | Match |
| 24 | `payrolls_county` | 4,539,800; −4,100 monthly; +20,300 annually | Los Angeles County, SA · September 2026 preliminary | [California Employment Development Department](https://labormarketinfo.edd.ca.gov/file/lfmonth/la$pds.pdf) | Match |
| 25 | `sector_edhealth` | 1,340.7 thousand; +49.1 thousand / +3.8% YoY | Los Angeles metro area · September 2026 | [U.S. Bureau of Labor Statistics](https://www.bls.gov/regions/west/summary/BLSSummary_LosAngeles.pdf) | Match |
| 26 | `sector_leisure` | 782.0 thousand; +11.5 thousand / +1.5% YoY | Los Angeles metro area · September 2026 | [U.S. Bureau of Labor Statistics](https://www.bls.gov/regions/west/summary/BLSSummary_LosAngeles.pdf) | Match |
| 27 | `sector_restaurants` | +7,300 jobs YoY | Los Angeles County, NSA · September 2026 preliminary | [California Employment Development Department](https://labormarketinfo.edd.ca.gov/file/lfmonth/la$pds.pdf) | Match |
| 28 | `sector_information` | 187.0 thousand; −11.4 thousand / −5.7% YoY | Los Angeles metro area · September 2026 | [U.S. Bureau of Labor Statistics](https://www.bls.gov/regions/west/summary/BLSSummary_LosAngeles.pdf) | Match |
| 29 | `sector_manufacturing` | 444.8 thousand; −5.4 thousand / −1.2% YoY | Los Angeles metro area · September 2026 | [U.S. Bureau of Labor Statistics](https://www.bls.gov/regions/west/summary/BLSSummary_LosAngeles.pdf) | Match |
| 30 | `cpi_la` | All items +3.7%; food +2.8%; energy +20.3% | Los Angeles area · September 2026 | [U.S. Bureau of Labor Statistics](https://www.bls.gov/regions/west/summary/BLSSummary_LosAngeles.pdf) | Match |
| 31 | `wage_county` | $1,704 | Los Angeles County · Q1 2026 | [U.S. Bureau of Labor Statistics](https://www.bls.gov/regions/west/summary/BLSSummary_LosAngeles.pdf) | Match |
| 32 | `unemp_city_2025` | 5.8% | City of Los Angeles · 2025; 11-month average excluding October | [U.S. Bureau of Labor Statistics](https://www.bls.gov/lau/city-annual-unemployment-rates.htm) | Match |
| 33 | `treasury_yields` | 2Y 4.51%; 5Y 4.64%; 10Y 4.86%; 30Y 5.26% | U.S. sovereign curve · November 6, 2026 | [U.S. Department of the Treasury](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202611) | Match |
| 34 | `schools_grad` | 87.6%; +1.1 percentage points | Los Angeles Unified School District · 2026 Dashboard | [California Department of Education](https://www.caschooldashboard.org/reports/19647330000000/2026/academic-engagement) | Match |
| 35 | `schools_absent` | 21.3%; declined 0.6 percentage points | Los Angeles Unified School District · 2026 Dashboard | [California Department of Education](https://www.caschooldashboard.org/reports/19647330000000/2026/academic-engagement) | Match |
| 36 | `schools_ela` | 13.2 points below; improved 4.6 points | Los Angeles Unified School District · 2026 Dashboard | [California Department of Education](https://www.caschooldashboard.org/reports/19647330000000/2026/academic-performance) | Match |
| 37 | `schools_math` | 40.7 points below; improved 8.2 points | Los Angeles Unified School District · 2026 Dashboard | [California Department of Education](https://www.caschooldashboard.org/reports/19647330000000/2026/academic-performance) | Match |
| 38 | `tenant_sss` | System −1.1%; franchise −1.2%; company −0.9% | Jack in the Box system · Q3 FY2026, 12 weeks ended July 5, 2026 | [U.S. Securities and Exchange Commission](https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm) | Match |
| 39 | `tenant_count` | 2,115 total; 149 company; 1,966 franchise | Jack in the Box system · End of Q3 FY2026 | [U.S. Securities and Exchange Commission](https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm) | Match |
| 40 | `tenant_revenue` | $257.657 million | Jack in the Box Inc. · Q3 FY2026 | [U.S. Securities and Exchange Commission](https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm) | Match |
| 41 | `tenant_earnings` | Continuing operations $21.041 million; total $20.122 million | Jack in the Box Inc. · Q3 FY2026 | [U.S. Securities and Exchange Commission](https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm) | Match |
| 42 | `tenant_ebitda` | $61.2 million | Jack in the Box Inc. · Q3 FY2026 | [U.S. Securities and Exchange Commission](https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm) | Match |
| 43 | `tenant_balance` | Cash $46.318M; current debt $44.160M; long-term debt $1,428.667M; stockholders' deficit $901.286M | Jack in the Box Inc. · July 5, 2026 | [U.S. Securities and Exchange Commission](https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm); [U.S. Securities and Exchange Commission](https://www.sec.gov/Archives/edgar/data/807882/000080788226000091/jack-20260705.htm) | Match |
| 44 | `tenant_refi` | $500 million Series 2026-1 Class A-2 Notes; anticipated repayment May 2031 | Jack in the Box Inc. · Q3 FY2026 | [U.S. Securities and Exchange Commission](https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm) | Match |
| 45 | `tenant_guidance` | Approximately 2,100 units; about 25 openings and 50–60 closures, mostly franchise | Jack in the Box system · FY2026 guidance issued August 2026 | [U.S. Securities and Exchange Commission](https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm) | Match |
| 46 | `tenant_governance` | CEO transition expected within 12 months; Executive Chairman serving as interim CEO; board refreshment; investor cooperation agreement extended | Jack in the Box Inc. · 8-K dated Sep 17, 2026, filed Sep 21, 2026 | [U.S. Securities and Exchange Commission](https://www.sec.gov/Archives/edgar/data/807882/000080788226000098/ex991-pressreleasexbodanno.htm) | Match |
| 47 | `tenant_ca_2025` | 351 total; 94 company; 257 franchise | California · FY2025 Form 10-K | [U.S. Securities and Exchange Commission](https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm) | Match |
| 48 | `tenant_ca_share` | 16.4% | California / Jack system · FY2025 | [U.S. Securities and Exchange Commission](https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm) | Match |
| 49 | `ula_thresholds` | $5,400,000 and $10,900,000 | City of Los Angeles · Transactions closing after June 30, 2026 | [Los Angeles Office of Finance](https://finance.lacity.gov/faq/measure-ula) | Match |
| 50 | `ula_rates` | 4% above lower threshold and below upper; 5.5% at/above upper | City of Los Angeles · Current FAQ for post-June 30, 2026 closings | [Los Angeles Office of Finance](https://finance.lacity.gov/faq/measure-ula) | Match |
| 51 | `prop13_rule` | 1% general levy plus voter-approved/direct assessments; assessed growth generally capped at 2% | California real property · Current assessor guidance | [Los Angeles County Assessor](https://assessor.lacounty.gov/real-estate-toolkit/proposition-13); [California State Board of Equalization](https://www.boe.ca.gov/proptaxes/pdf/lta22046.pdf) | Match |
| 52 | `ftb_gains` | Taxed as ordinary income; no lower individual capital-gains rate | California · Current FTB guidance | [California Franchise Tax Board](https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html) | Match |
| 53 | `irs_1031_timing` | Identify replacement within 45 days; receive within 180 days or return due date including extensions, whichever earlier | U.S. federal tax · 2025 Form 8824 instructions | [Internal Revenue Service](https://www.irs.gov/pub/irs-pdf/i8824.pdf) | Match |
| 54 | `wage_fastfood` | $20.00/hour | California covered fast-food employees · Effective April 1, 2024; current FAQ | [California Department of Industrial Relations](https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm) | Match |
| 55 | `wage_state` | $16.90/hour | California · January 1, 2026 | [California Department of Industrial Relations](https://www.dir.ca.gov/dlse/faq_minimumwage.htm) | Match |
| 56 | `wage_city` | $18.42/hour | City of Los Angeles · July 1, 2026 | [Los Angeles Office of Wage Standards](https://wagesla.lacity.gov/sites/g/files/wph1941/files/2026-04/MWO-Notice-2026%208x11%20-%20English%20ADA260304.pdf) | Match |
| 57 | `nri_composite` | Score 100; Very High | Los Angeles County · NRI v1.20, December 2025 | [FEMA ArcGIS feature service](https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0/query?where=STCOFIPS%3D%2706037%27&outFields=COUNTY,STCOFIPS,RISK_SCORE,RISK_RATNG,EAL_SCORE,EAL_VALT,EAL_VALB,SOVI_SCORE,SOVI_RATNG,RESL_SCORE,RESL_RATNG,ERQK_RISKS,ERQK_RISKR,ERQK_EALT,WFIR_RISKS,WFIR_RISKR,WFIR_EALT,IFLD_RISKS,IFLD_RISKR,IFLD_EALT&returnGeometry=false&f=json); [Federal Emergency Management Agency](https://www.fema.gov/flood-maps/products-tools/national-risk-index) | Match |
| 58 | `nri_eal` | $7,601,846,373 total; $5,946,330,343 building value | Los Angeles County · NRI v1.20, December 2025 | [FEMA ArcGIS feature service](https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0/query?where=STCOFIPS%3D%2706037%27&outFields=COUNTY,STCOFIPS,RISK_SCORE,RISK_RATNG,EAL_SCORE,EAL_VALT,EAL_VALB,SOVI_SCORE,SOVI_RATNG,RESL_SCORE,RESL_RATNG,ERQK_RISKS,ERQK_RISKR,ERQK_EALT,WFIR_RISKS,WFIR_RISKR,WFIR_EALT,IFLD_RISKS,IFLD_RISKR,IFLD_EALT&returnGeometry=false&f=json) | Match |
| 59 | `nri_earthquake` | Score 100; Very High; EAL $4,565,736,367 | Los Angeles County · NRI v1.20, December 2025 | [FEMA ArcGIS feature service](https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0/query?where=STCOFIPS%3D%2706037%27&outFields=COUNTY,STCOFIPS,RISK_SCORE,RISK_RATNG,EAL_SCORE,EAL_VALT,EAL_VALB,SOVI_SCORE,SOVI_RATNG,RESL_SCORE,RESL_RATNG,ERQK_RISKS,ERQK_RISKR,ERQK_EALT,WFIR_RISKS,WFIR_RISKR,WFIR_EALT,IFLD_RISKS,IFLD_RISKR,IFLD_EALT&returnGeometry=false&f=json) | Match |
| 60 | `nri_wildfire` | Score 99.936; Very High; EAL $155,191,812 | Los Angeles County · NRI v1.20, December 2025 | [FEMA ArcGIS feature service](https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0/query?where=STCOFIPS%3D%2706037%27&outFields=COUNTY,STCOFIPS,RISK_SCORE,RISK_RATNG,EAL_SCORE,EAL_VALT,EAL_VALB,SOVI_SCORE,SOVI_RATNG,RESL_SCORE,RESL_RATNG,ERQK_RISKS,ERQK_RISKR,ERQK_EALT,WFIR_RISKS,WFIR_RISKR,WFIR_EALT,IFLD_RISKS,IFLD_RISKR,IFLD_EALT&returnGeometry=false&f=json) | Match |
| 61 | `nri_flood` | Score 100; Very High; EAL $2,808,736,524 | Los Angeles County · NRI v1.20, December 2025 | [FEMA ArcGIS feature service](https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0/query?where=STCOFIPS%3D%2706037%27&outFields=COUNTY,STCOFIPS,RISK_SCORE,RISK_RATNG,EAL_SCORE,EAL_VALT,EAL_VALB,SOVI_SCORE,SOVI_RATNG,RESL_SCORE,RESL_RATNG,ERQK_RISKS,ERQK_RISKR,ERQK_EALT,WFIR_RISKS,WFIR_RISKR,WFIR_EALT,IFLD_RISKS,IFLD_RISKR,IFLD_EALT&returnGeometry=false&f=json); [Federal Emergency Management Agency](https://www.fema.gov/flood-maps/products-tools/national-risk-index) | Match |
| 62 | `nri_coastal_flood` | Score 90; Relatively High | Los Angeles County · NRI v1.20, December 2025 | [FEMA ArcGIS feature service](https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0/query?where=STCOFIPS%3D%2706037%27&outFields=COUNTY,STCOFIPS,RISK_SCORE,RISK_RATNG,EAL_SCORE,EAL_VALT,EAL_VALB,SOVI_SCORE,SOVI_RATNG,RESL_SCORE,RESL_RATNG,ERQK_RISKS,ERQK_RISKR,ERQK_EALT,WFIR_RISKS,WFIR_RISKR,WFIR_EALT,IFLD_RISKS,IFLD_RISKR,IFLD_EALT&returnGeometry=false&f=json) | Match |
| 63 | `nri_social` | Social vulnerability 55.375, Relatively Moderate; resilience 13.550, Very Low | Los Angeles County · NRI v1.20, December 2025 | [FEMA ArcGIS feature service](https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0/query?where=STCOFIPS%3D%2706037%27&outFields=COUNTY,STCOFIPS,RISK_SCORE,RISK_RATNG,EAL_SCORE,EAL_VALT,EAL_VALB,SOVI_SCORE,SOVI_RATNG,RESL_SCORE,RESL_RATNG,ERQK_RISKS,ERQK_RISKR,ERQK_EALT,WFIR_RISKS,WFIR_RISKR,WFIR_EALT,IFLD_RISKS,IFLD_RISKR,IFLD_EALT&returnGeometry=false&f=json) | Match |
| 64 | `nri_other_hazards` | Heat wave, landslide, tornado: Relatively High; lightning: Very High; drought/tsunami: Relatively Low; hurricane: No Rating; ice storm/volcanic: Not Applicable | Los Angeles County · NRI v1.20, December 2025 | [FEMA ArcGIS feature service](https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0/query?where=STCOFIPS%3D%2706037%27&outFields=COUNTY,STCOFIPS,AVLN_RISKR,CFLD_RISKR,CWAV_RISKR,DRGT_RISKR,ERQK_RISKR,HAIL_RISKR,HWAV_RISKR,HRCN_RISKR,ISTM_RISKR,IFLD_RISKR,LNDS_RISKR,LTNG_RISKR,SWND_RISKR,TRND_RISKR,TSUN_RISKR,VLCN_RISKR,WFIR_RISKR,WNTW_RISKR&returnGeometry=false&f=json) | Match |
| 65 | `usgs_quake` | 60% M≥6.7; 46% M≥7.0; 31% M≥7.5 in 30 years | Los Angeles region · USGS FAQ citing UCERF3; start date not stated | [U.S. Geological Survey](https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-los-angeles-area-san-francisco-bay-area) | Match |
| 66 | `calfire_acres_obs` | Moderate 330,431; High 77,951; Very High 769,561; Total mapped 1,177,944 | Los Angeles County, combined SRA/LRA · 2024–2025 official acreage table | [California State Fire Marshal / CAL FIRE](https://34c031f8-c9fd-4018-8c5a-4159cdff6b0d-cdn-endpoint.azureedge.net/-/media/osfm-website/what-we-do/community-wildfire-preparedness-and-mitigation/fire_hazard_severity_zone_acres_state_and_local_responsibility_2024_2025.pdf?rev=d1f74280dd01402f841bf2da5d5fc8cd&hash=EC6CA86D1AF5094D808CB341A328C52F); [California State Fire Marshal / CAL FIRE](https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones) | Match |
| 67 | `calfire_share` | 65.3% | Los Angeles County mapped FHSZ acres · 2024–2025 table | [California State Fire Marshal / CAL FIRE](https://34c031f8-c9fd-4018-8c5a-4159cdff6b0d-cdn-endpoint.azureedge.net/-/media/osfm-website/what-we-do/community-wildfire-preparedness-and-mitigation/fire_hazard_severity_zone_acres_state_and_local_responsibility_2024_2025.pdf?rev=d1f74280dd01402f841bf2da5d5fc8cd&hash=EC6CA86D1AF5094D808CB341A328C52F) | Match |
| 68 | `cdi_claims_obs` | 41,727 claims filed; 40,482 partially paid; $25.2 billion paid | California, Eaton and Palisades fires · Tracker updated July 6, 2026 | [California Department of Insurance](https://www.insurance.ca.gov/01-consumers/180-climate-change/Wildfire-Claims-Tracker.cfm) | Match |
| 69 | `dtla_plan` | 100,000 new homes; 100,000 more work opportunities; 175,000 additional residents through 2040 | Seven-square-mile Downtown Los Angeles plan core · Adopted December 2024 | [Los Angeles City Planning](https://planning.lacity.gov/odocument/92b97b24-1978-4e0e-9eae-51f22eda9e4c/Press%20Release_%20DTLA%20New%20Zoning%20Code.pdf) | Match |
| 70 | `crime_status` | Platform feed undergoing updates; official bureau/area statistics linked | City of Los Angeles · Page accessed November 8, 2026 | [Los Angeles Police Department](https://www.lapdonline.org/office-of-the-chief-of-police/office-of-special-operations/detective-bureau/crime-mapping-and-compstat/) | Match |
| 71 | `port_driver` | Official container, cruise, automobile, breakbulk, and tonnage series available | Port of Los Angeles / regional trade · Page accessed November 8, 2026 | [Port of Los Angeles](https://www.portoflosangeles.org/business/statistics) | Match |

---

## 2. Derived figures recomputed by hand

Derived rows are labelled `derived` and were recomputed from the cited official inputs; none was
copied from a third party.

| Derived row | Formula | Recompute | Result |
|---|---|---|---|
| `tenant_ca_share` 16.4% | 351 ÷ 2,136 (10-K FY2025: California Jack units ÷ system Jack units) | 351/2136 = 16.4326% | **confirmed**, 16.4% |
| `calfire_share` 65.3% | 769,561 ÷ 1,177,944 (CAL FIRE Very High LRA+SRA acres ÷ total mapped acres, Los Angeles County) | 769561/1177944 = 65.33% | **confirmed**, 65.3% |
| FEMA NRI total EAL $7,601,846,373 | composite `EAL_VALT` read directly from the feature service | returned verbatim | **confirmed** |
| FEMA NRI building EAL $5,946,330,343 | composite `EAL_VALB` read directly from the feature service | returned verbatim | **confirmed** |
| SCAG manufacturing "about 15.4%" endpoint change | (706 − 612) ÷ 612 (regional manufacturing jobs 2022 → 2050) | 94/612 = 15.36% | **confirmed**, and the official table's printed "153%" is internally inconsistent with its own endpoints — the page correctly withholds the printed figure |
| DOF annual change columns | year-over-year and 2026-base index from the P-2A county row | reproduced in `scripts/projection_model.py`, covered by unit tests | **confirmed** |
| DOF vs SCAG milestone differences | SCAG milestone minus DOF milestone for the same year, printed explicitly as a planning-model difference | reproduced | **confirmed** |
| SCAG sector CAGR | (end ÷ start)^(1/28) − 1 over 2022–2050 | reproduced | **confirmed** |
| City/county population change −0.8% / −3.2% | published directly by Census QuickFacts (not computed here) | n/a | **confirmed as published** |

---

## 3. Sources re-read this pass (official only)

| Series | Official URL read 2026-11-10 |
|---|---|
| Census QuickFacts, city + county (V2025 / ACS 2020-2024) | https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia,losangelescountycalifornia/PST045224 |
| BLS Los Angeles Area Economic Summary, updated 04 Nov 2026 | https://www.bls.gov/regions/west/summary/BLSSummary_LosAngeles.pdf |
| BLS LAUS county series LAUCN060370000000003 | https://data.bls.gov/timeseries/LAUCN060370000000003?output_view=data&include_graphs=true |
| BLS annual unemployment, 50 largest cities | https://www.bls.gov/lau/city-annual-unemployment-rates.htm |
| California EDD Los Angeles profile (Sept 2026 prelim) | https://labormarketinfo.edd.ca.gov/file/lfmonth/la$pds.pdf |
| BEA county GDP via FRED `GDPALL06037` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=GDPALL06037 |
| BEA metro GDP via FRED `NGMP31080` | https://fred.stlouisfed.org/graph/fredgraph.csv?id=NGMP31080 |
| U.S. Treasury daily par yield curve, Nov 2026 | https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202611 |
| California DOF projections landing page (vintage control) | https://dof.ca.gov/forecasting/demographics/projections/ |
| California DOF P-2A county totals (Vintage 2026) | https://dof.ca.gov/media/docs/forecasting/Demographics/projections/P2A_County_Total.xlsx |
| SCAG Connect SoCal 2024 Appendix I tables 3.14-8/9/10 | https://scag.ca.gov/sites/default/files/2024-05/appendix_i_updated_tables_508_final.pdf |
| SCAG Demographics and Growth Forecast Technical Report, Table 6 | https://www.scag.ca.gov/sites/default/files/2024-05/23-2987-tr-demographics-growth-forecast-final-040424.pdf |
| LA City Planning, DTLA 2040 press release (04 Dec 2024) | https://planning.lacity.gov/odocument/92b97b24-1978-4e0e-9eae-51f22eda9e4c/Press%20Release_%20DTLA%20New%20Zoning%20Code.pdf |
| FEMA National Risk Index county feature service (all queried fields) | https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0/query?where=STCOFIPS%3D%2706037%27&outFields=*&returnGeometry=false&f=json |
| USGS FAQ, UCERF3 Los Angeles probabilities | https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-los-angeles-area-san-francisco-bay-area |
| CAL FIRE / OSFM FHSZ acreage table 2024-2025 | (official OSFM CDN PDF, URL recorded in the dataset `calfire_acres`) |
| California Department of Insurance wildfire claims tracker | https://www.insurance.ca.gov/01-consumers/180-climate-change/Wildfire-Claims-Tracker.cfm |
| SEC Form 10-K FY2025 | https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm |
| SEC Form 10-Q Q3 FY2026 | https://www.sec.gov/Archives/edgar/data/807882/000080788226000091/jack-20260705.htm |
| SEC Q3 FY2026 earnings exhibit 99.1 | https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm |
| SEC Form 8-K dated 21 Sep 2026, exhibit 99.1 | https://www.sec.gov/Archives/edgar/data/807882/000080788226000098/ex991-pressreleasexbodanno.htm |
| SEC EDGAR filing index for CIK 0000807882 (freshness check) | https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000807882&type=8-K&output=atom&count=20 |
| LA County Assessor, Proposition 13 guidance | https://assessor.lacounty.gov/real-estate-toolkit/proposition-13 |
| California FTB, capital gains treatment | https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html |
| IRS Instructions for Form 8824 (like-kind timing) | https://www.irs.gov/pub/irs-pdf/i8824.pdf |
| LA City Office of Finance, Measure ULA FAQ | https://finance.lacity.gov/faq/measure-ula |
| California DIR, fast-food minimum wage FAQ | https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm |
| California DIR, minimum wage FAQ | https://www.dir.ca.gov/dlse/faq_minimumwage.htm |
| LA Office of Wage Standards, 2026 minimum wage notice | (official WagesLA PDF, URL recorded in the dataset `la_wage`) |
| CDE California School Dashboard, LAUSD engagement | https://www.caschooldashboard.org/reports/19647330000000/2026/academic-engagement |
| CDE California School Dashboard, LAUSD performance | https://www.caschooldashboard.org/reports/19647330000000/2026/academic-performance |
| LAPD Crime Mapping and COMPSTAT | https://www.lapdonline.org/office-of-the-chief-of-police/office-of-special-operations/detective-bureau/crime-mapping-and-compstat/ |
| Port of Los Angeles statistics hub | https://www.portoflosangeles.org/business/statistics |

---

## 4. Irregularities found, resolved, or still open

| # | Item | What the official record says | Treatment |
|---|---|---|---|
| V-01 | **Custom 404 page was not served (site defect, new)** | `_config.yml` excluded `404.html` from the legacy Pages build, so a deliberately invalid URL (`https://wingbangboozle1-lang.github.io/Jack1/this-page-does-not-exist-12345.html`) returned GitHub's default error page — confirmed by direct fetch | **Fixed.** The exclusion was removed and `404.html` is now generated by the build script from the same page list as the dashboard |
| V-02 | **Stale 404 content (site defect, new)** | The retained `404.html` claimed the brief is published as "seventeen pages" and linked `geography.html`, `population.html`, `income.html`, `schools.html`, `economy.html`, `jobs.html`, `tenant.html` and `repo-review.html` — all excluded from publication, so every one of those links returned 404 | **Fixed.** Regenerated with the current ten-page navigation, so it cannot drift from the real page list |
| V-03 | **Unpublished drafts and unused assets retained (repo hygiene, new)** | Eleven root `*.html` drafts and three `assets/*` files are excluded from publication and referenced by nothing that is published | **Logged as a flag, not deleted.** They are other sessions' historical records; removal is a consolidation decision, not a verification decision |
| V-04 | USGS 30-year probability start date | The USGS FAQ cites the UCERF3 fact sheet but prints no start date; the regional window is undated on the page | Remains **flagged** (`flag_usgs_vintage`). The page already warns it must not be read as a fresh 2026–2056 forecast |
| V-05 | CAL FIRE "26% / 35% FHSZ expansion" claims | The official OSFM acreage table publishes acres by severity class, not an expansion percentage; no official page states 26% or 35% | Remains **flagged** and unprinted — confirmed still correct to withhold |
| V-06 | SCAG manufacturing future change "153%" | The official table materially prints `153%` while its own endpoints (612k → 706k) imply ~15.4% | Remains **withheld** and **flagged**; this pass re-read both the printed percentage and the endpoints and reproduced the inconsistency |
| V-07 | DOF vs SCAG population direction | DOF projects Los Angeles County declining (9,811,358 in 2026 → 9,708,647 in 2035); SCAG projects growth (10,214,000 in 2030). Both are officially published | Both published **side by side**, never blended; the gap is labelled a planning-model difference |
| V-08 | Metro GDP vintage | FRED `NGMP31080` still ends at 2023 ($1,295,361.403M); county `GDPALL06037` reaches 2024 ($1,002,965,029k) | Page keeps the **2023 metro / 2024 county** split. No 2024 metro value exists, so none is asserted |
| V-09 | BLS city annual 2025 footnote | Official note: 2025 figures are 11-month averages excluding October, because October 2025 data were not collected during the federal shutdown | Row already carries this caveat — re-confirmed word for word |
| V-10 | BLS vs EDD national rate | BLS summary Sep-26 U.S. NSA is 4.0%; the EDD release's seasonally adjusted U.S. figure is 4.2% | Different adjustment bases; kept in separate rows with the basis stated |
| V-11 | BLS October 2025 gap in the county LAUS series | The series prints `-(X)` for 2025 Oct, noted "Data unavailable due to the 2025 lapse in appropriations" | Not published as a value; the page uses September 2026 only |
| V-12 | LAPD crime feed | Official banner: the CrimeMapping platform "is currently undergoing updates to integrate a new data feed" | Page publishes the **status**, not a crime rate. No parcel-level statistic inferred |
| V-13 | CDI claims are not commercial-only | The tracker states claims include home, business, living expenses, auto, and other disaster claims | Page states this limitation in the row note |
| V-14 | FEMA NRI is a county model | The service returns county polygons with aggregate expected annual loss | Page prints the county figure and states it is not a parcel loss estimate |

---

## 5. Freshness check performed this pass

Every official series was checked for a newer vintage than the one published on 2026-11-08.

| Series | Newer vintage available on 2026-11-10? | Action |
|---|---|---|
| Census QuickFacts | No — still V2025 / ACS 2020-2024 | none needed |
| BLS LA Economic Summary | No — still updated 04 Nov 2026 (Sept 2026 reference month) | none needed |
| BLS LAUS county series | No — September 2026 remains the latest published month (`(P)` preliminary) | none needed |
| EDD Los Angeles profile | No — still September 2026 preliminary | none needed |
| BEA county GDP (FRED) | No — still 2024 | none needed |
| BEA metro GDP (FRED) | No — still 2023; series has no 2024 observation | none needed |
| California DOF projections | No — Vintage 2026 (released 2026-03-13) is still the current release | none needed |
| SCAG Connect SoCal 2024 | No — Appendix I (May 2024) remains the current PEIR table set | none needed |
| SEC Jack in the Box filings | No 10-K for FY2026 (year ended 2026-09-27) has been filed as of 2026-11-10; the latest periodic filings remain the Q3 FY2026 10-Q and 8-K of 21 Sep 2026 | none needed; re-check after the FY2026 10-K is filed |
| Treasury par yields | Yes — new daily observations through 2026-11-09 | rates are a moving market series, so the page keeps a **dated snapshot** and states the observation date rather than chasing the daily print |
| CAL FIRE FHSZ acres | No — the 2024/2025 table is the latest published | none needed |
| CDI wildfire claims tracker | No — still updated 2026-07-06 | none needed |
| CDE School Dashboard | No — 2026 dashboard is still current | none needed |

**One deliberate addition:** a dated Treasury snapshot is a point-in-time market observation, so the
dataset now also records the **12-month change in the 10-year yield** (4.11% on 2025-11-06 → 4.86% on
2026-11-06, +75 basis points, computed from FRED `DGS10`). This is the single most decision-relevant
financing fact for a 2030–2035 exit: the rate at which a buyer can finance a purchase has moved, and
that moves capitalization-driven value independently of the property's own cash flow.

---

## 6. Gates run after this pass

```
python3 scripts/build_public.py --check      # canonical pages match the dataset
python3 -m unittest discover -s tests        # projection, gating, determinism, privacy rules
python3 scripts/validate_site.py             # structure, row sources, allowlist, links, blanks, privacy
python3 scripts/build_public.py --out _site && python3 scripts/validate_site.py --site _site --artifact
```
