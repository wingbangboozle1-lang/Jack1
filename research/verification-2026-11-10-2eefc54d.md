# Line-by-line research log — session 2eefc54d — 2026-11-10 (UTC)

This is the internal research companion to `verification/2026-11-10-2eefc54d.md`. It preserves the source trail used for manual review. No personal names, email addresses, phone numbers, APNs, or owner identifiers from official pages are reproduced here.

## A. Source groups re-read

The verification report contains all 74 active source IDs, official links, and exact re-read/reconciliation notes: 48 at-claim IDs, 25 added by `ac5b9087`, and one dedicated FEMA coastal query added in V-2. This pass closes the groups that session `c5e199ef` listed as "Not re-read this pass": SEC 10-K California table; SCAG 2030/2045 rows and sector endpoints; Q3 FY2026 10-Q balance detail; 8-K filing date / role-only governance; CAL FIRE, LAPD, Port, EPA, IRS, FTB, BOE, and Assessor/ZIMAS guidance; FEMA coastal-flood numeric score.

## B. Critical cross-checks

1. **FY2025 10-K state table.** The table has separate Del Taco and Jack in the Box column groups. California Del Taco = 94 company + 257 franchise = 351 total. California Jack in the Box = 96 company + 845 franchise = 941 total. The brand system total is 2,136 Jack in the Box restaurants (150 company + 1,986 franchise), separate from 576 Del Taco restaurants. Therefore 941 ÷ 2,136 = 44.1%, not 351 ÷ 2,136 = 16.4%. The active 2026-11-10 dataset already publishes this correction (session `ac5b9087`); this session recorded independent confirmation rather than duplicating the edit. Official link: <https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm>.
2. **FEMA NRI coastal flooding.** The generic county query returns composite, EAL, social vulnerability, resilience, earthquake, wildfire and inland-flood fields, but no `CFLD_RISKS`. The hazard-ratings query returns `CFLD_RISKR: "Relatively High"` but no numeric score. A dedicated official query returns both `CFLD_RISKS: 90` and `CFLD_RISKR: "Relatively High"`. Official link: <https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0/query?where=STCOFIPS%3D%2706037%27&outFields=COUNTY,STCOFIPS,CFLD_RISKS,CFLD_RISKR&returnGeometry=false&f=json>.
3. **SCAG 2030/2045.** Appendix I tables give LA County 2030 population 10,214,000 / households 3,784,000 / employment 5,277,000 and 2045 population 10,757,000 / households 4,120,000 / employment 5,497,000. Technical Report Table 6 gives sector endpoints and the inconsistent printed manufacturing percentage. Official links: <https://scag.ca.gov/sites/default/files/2024-05/appendix_i_updated_tables_508_final.pdf> and <https://www.scag.ca.gov/sites/default/files/2024-05/23-2987-tr-demographics-growth-forecast-final-040424.pdf>.
4. **Treasury.** Official November 2026 table has 11/06 and 11/09 rows. The dataset now uses 11/09 with its exact date; the older 11/06 row is not blended. Official link: <https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202611>.
5. **8-K.** EDGAR index shows filing date 2026-09-21 and period of report 2026-09-17. The exhibit's role-only governance wording supports the published row; personal identifiers are omitted. Official link: <https://www.sec.gov/Archives/edgar/data/807882/000080788226000098/ex991-pressreleasexbodanno.htm>.

## C. Manual-review source list

| Source ID | Official link | Publisher |
|---|---|---|
| `census_city` | <https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225> | U.S. Census Bureau |
| `census_county` | <https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045225> | U.S. Census Bureau |
| `bls_summary` | <https://www.bls.gov/regions/west/summary/BLSSummary_LosAngeles.pdf> | U.S. Bureau of Labor Statistics |
| `bls_laus` | <https://data.bls.gov/timeseries/LAUCN060370000000003?output_view=data&include_graphs=true> | U.S. Bureau of Labor Statistics |
| `bls_city_annual` | <https://www.bls.gov/lau/city-annual-unemployment-rates.htm> | U.S. Bureau of Labor Statistics |
| `edd_la` | <https://labormarketinfo.edd.ca.gov/file/lfmonth/la$pds.pdf> | California Employment Development Department |
| `fred_county_gdp` | <https://fred.stlouisfed.org/series/GDPALL06037> | U.S. Bureau of Economic Analysis via FRED |
| `fred_metro_gdp` | <https://fred.stlouisfed.org/series/NGMP31080> | U.S. Bureau of Economic Analysis via FRED |
| `treasury` | <https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202611> | U.S. Department of the Treasury |
| `dof_landing` | <https://dof.ca.gov/forecasting/demographics/projections/> | California Department of Finance |
| `dof_p2a` | <https://dof.ca.gov/media/docs/forecasting/Demographics/projections/P2A_County_Total.xlsx> | California Department of Finance |
| `scag_plan` | <https://scag.ca.gov/connect-socal> | Southern California Association of Governments |
| `scag_tr` | <https://www.scag.ca.gov/sites/default/files/2024-05/23-2987-tr-demographics-growth-forecast-final-040424.pdf> | Southern California Association of Governments |
| `scag_appendix` | <https://scag.ca.gov/sites/default/files/2024-05/appendix_i_updated_tables_508_final.pdf> | Southern California Association of Governments |
| `dtla_release` | <https://planning.lacity.gov/odocument/92b97b24-1978-4e0e-9eae-51f22eda9e4c/Press%20Release_%20DTLA%20New%20Zoning%20Code.pdf> | Los Angeles City Planning |
| `zimas` | <https://planning.lacity.gov/zoning/zoning-search> | Los Angeles City Planning |
| `assessor` | <https://portal.assessor.lacounty.gov/> | Los Angeles County Assessor |
| `prop13` | <https://assessor.lacounty.gov/real-estate-toolkit/proposition-13> | Los Angeles County Assessor |
| `boe_reassessment` | <https://www.boe.ca.gov/proptaxes/pdf/lta22046.pdf> | California State Board of Equalization |
| `ula` | <https://finance.lacity.gov/faq/measure-ula> | Los Angeles Office of Finance |
| `ftb_capgains` | <https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html> | California Franchise Tax Board |
| `irs_544` | <https://www.irs.gov/publications/p544> | Internal Revenue Service |
| `irs_8824` | <https://www.irs.gov/pub/irs-pdf/i8824.pdf> | Internal Revenue Service |
| `dir_fastfood` | <https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm> | California Department of Industrial Relations |
| `dir_minwage` | <https://www.dir.ca.gov/dlse/faq_minimumwage.htm> | California Department of Industrial Relations |
| `la_wage` | <https://wagesla.lacity.gov/sites/g/files/wph1941/files/2026-04/MWO-Notice-2026%208x11%20-%20English%20ADA260304.pdf> | Los Angeles Office of Wage Standards |
| `dashboard_engagement` | <https://www.caschooldashboard.org/reports/19647330000000/2026/academic-engagement> | California Department of Education |
| `dashboard_performance` | <https://www.caschooldashboard.org/reports/19647330000000/2026/academic-performance> | California Department of Education |
| `dashboard_faq` | <https://www.caschooldashboard.org/about/faq> | California Department of Education |
| `cde_directory` | <https://www.cde.ca.gov/schooldirectory/> | California Department of Education |
| `sec_10k` | <https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm> | U.S. Securities and Exchange Commission |
| `sec_10q` | <https://www.sec.gov/Archives/edgar/data/807882/000080788226000091/jack-20260705.htm> | U.S. Securities and Exchange Commission |
| `sec_release` | <https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm> | U.S. Securities and Exchange Commission |
| `fema_nri` | <https://www.fema.gov/flood-maps/products-tools/national-risk-index> | Federal Emergency Management Agency |
| `fema_county_item` | <https://fema.maps.arcgis.com/home/item.html?id=39485e8035d446a5bff03259508ae355> | FEMA via ArcGIS Living Atlas |
| `fema_county_query` | <https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0/query?where=STCOFIPS%3D%2706037%27&outFields=COUNTY,STCOFIPS,RISK_SCORE,RISK_RATNG,EAL_SCORE,EAL_VALT,EAL_VALB,SOVI_SCORE,SOVI_RATNG,RESL_SCORE,RESL_RATNG,ERQK_RISKS,ERQK_RISKR,ERQK_EALT,WFIR_RISKS,WFIR_RISKR,WFIR_EALT,IFLD_RISKS,IFLD_RISKR,IFLD_EALT&returnGeometry=false&f=json> | FEMA ArcGIS feature service |
| `fema_hazard_ratings` | <https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0/query?where=STCOFIPS%3D%2706037%27&outFields=COUNTY,STCOFIPS,AVLN_RISKR,CFLD_RISKR,CWAV_RISKR,DRGT_RISKR,ERQK_RISKR,HAIL_RISKR,HWAV_RISKR,HRCN_RISKR,ISTM_RISKR,IFLD_RISKR,LNDS_RISKR,LTNG_RISKR,SWND_RISKR,TRND_RISKR,TSUN_RISKR,VLCN_RISKR,WFIR_RISKR,WNTW_RISKR&returnGeometry=false&f=json> | FEMA ArcGIS feature service |
| `usgs_faq` | <https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-los-angeles-area-san-francisco-bay-area> | U.S. Geological Survey |
| `calfire_fhsz` | <https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones> | California State Fire Marshal / CAL FIRE |
| `calfire_acres` | <https://34c031f8-c9fd-4018-8c5a-4159cdff6b0d-cdn-endpoint.azureedge.net/-/media/osfm-website/what-we-do/community-wildfire-preparedness-and-mitigation/fire_hazard_severity_zone_acres_state_and_local_responsibility_2024_2025.pdf?rev=d1f74280dd01402f841bf2da5d5fc8cd&hash=EC6CA86D1AF5094D808CB341A328C52F> | California State Fire Marshal / CAL FIRE |
| `cdi_claims` | <https://www.insurance.ca.gov/01-consumers/180-climate-change/Wildfire-Claims-Tracker.cfm> | California Department of Insurance |
| `lapd` | <https://www.lapdonline.org/office-of-the-chief-of-police/office-of-special-operations/detective-bureau/crime-mapping-and-compstat/> | Los Angeles Police Department |
| `epa_brownfields` | <https://www.epa.gov/brownfields> | U.S. Environmental Protection Agency |
| `port_stats` | <https://www.portoflosangeles.org/business/statistics> | Port of Los Angeles |
| `repo` | <https://github.com/wingbangboozle1-lang/Jack1> | GitHub repository |
| `live` | <https://wingbangboozle1-lang.github.io/Jack1/> | GitHub Pages |
| `repo_line_audit` | <https://github.com/wingbangboozle1-lang/Jack1/blob/main/verification/repository-line-audit-0e369d53.tsv> | GitHub repository verification record |
| `sec_8k_sept2026` | <https://www.sec.gov/Archives/edgar/data/807882/000080788226000098/ex991-pressreleasexbodanno.htm> | U.S. Securities and Exchange Commission |
| `fema_coastal_score` | <https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0/query?where=STCOFIPS%3D%2706037%27&outFields=COUNTY,STCOFIPS,CFLD_RISKS,CFLD_RISKR&returnGeometry=false&f=json> | FEMA ArcGIS feature service |


### Additional source IDs merged from session ac5b9087 and reconciled in V-2

| Source ID | Official link | Publisher |
|---|---|---|
| `dof_e1` | <https://dof.ca.gov/media/docs/forecasting/Demographics/estimates/E-1_2026_Press_Release.pdf> | California Department of Finance |
| `dof_e5` | <https://dof.ca.gov/media/docs/forecasting/Demographics/estimates/July2025_Population_Estimates_Feb26_release.pdf> | California Department of Finance |
| `cde_sdprofile` | <https://www.cde.ca.gov/sdprofile/details.aspx?cds=19647330000000> | California Department of Education |
| `lavote_dtt` | <https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info> | LA County Registrar-Recorder / County Clerk |
| `dir_release_2027` | <https://www.dir.ca.gov/DIRNews/2026/2026-66.html> | California Department of Industrial Relations |
| `port_facts` | <https://portoflosangeles.org/business/statistics/facts-and-figures> | Port of Los Angeles |
| `port_containers` | <https://portoflosangeles.org/business/statistics/container-statistics> | Port of Los Angeles |
| `metro_dline` | <https://www.metro.net/projects/westside/> | Los Angeles County Metropolitan Transportation Authority |
| `metro_lax` | <https://www.metro.net/about/media-relations/now-boarding-metros-lax-metro-transit-center-station-officially-opens-connecting-communities-bringing-faster-easier-travel-for-angelenos-visitors/> | Los Angeles County Metropolitan Transportation Authority |
| `lapd_city` | <https://lapdonlinestrgeacc.blob.core.usgovcloudapi.net/lapdonlinemedia/cityprof.pdf> | Los Angeles Police Department |
| `lapd_central` | <https://lapdonlinestrgeacc.blob.core.usgovcloudapi.net/lapdonlinemedia/ocbprof.pdf> | Los Angeles Police Department |
| `sec_10q_debt` | <https://www.sec.gov/Archives/edgar/data/807882/000080788226000091/R14.htm> | U.S. Securities and Exchange Commission |
| `sec_10q_ar` | <https://www.sec.gov/Archives/edgar/data/807882/000080788226000091/R8.htm> | U.S. Securities and Exchange Commission |
| `sec_10q_leases` | <https://www.sec.gov/Archives/edgar/data/807882/000080788226000091/R12.htm> | U.S. Securities and Exchange Commission |
| `sec_10k_leases` | <https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/R16.htm> | U.S. Securities and Exchange Commission |
| `sec_10q_contingencies` | <https://www.sec.gov/Archives/edgar/data/807882/000080788226000091/R20.htm> | U.S. Securities and Exchange Commission |
| `openfema_la` | <https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries?%24filter=state%20eq%20%27CA%27%20and%20contains(designatedArea%2C%20%27Los%20Angeles%27)&%24inlinecount=allpages&%24top=5> | Federal Emergency Management Agency |
| `calfire_palisades` | <https://www.fire.ca.gov/incidents/2025/1/7/palisades-fire/> | CAL FIRE |
| `calfire_eaton` | <https://www.fire.ca.gov/incidents/2025/1/7/eaton-fire/> | CAL FIRE |
| `cgs_alquist_priolo` | <https://www.conservation.ca.gov/cgs/alquist-priolo> | California Geological Survey |
| `cgs_shma` | <https://www.conservation.ca.gov/cgs/shma> | California Geological Survey |
| `usgs_shakeout` | <https://www.usgs.gov/publications/shakeout-scenario-a-hypothetical-mw78-earthquake-southern-san-andreas-fault> | U.S. Geological Survey |
| `cdi_fairplan_2025` | <https://www.insurance.ca.gov/0400-news/0100-press-releases/2025/release028-2025.cfm> | California Department of Insurance |
| `cdi_catmodel_2025` | <https://www.insurance.ca.gov/0400-news/0100-press-releases/2025/release052-2025.cfm> | California Department of Insurance |
| `epa_heat` | <https://www.epa.gov/heatislands> | U.S. Environmental Protection Agency |

High-risk SEC XBRL notes `R14.htm`, `R8.htm`, `R12.htm`, `R16.htm`, and `R20.htm` were independently re-read; the remaining newly merged sources were reconciled against `verification/2026-11-10-ac5b9087.md` and `research/2026-11-10-ac5b9087/source-notes.md`, and every active URL passes the validator allowlist.

## D. Final row inventory

Canonical dataset after V-2: `74` source IDs, `90` observations, `27` flags, `13` audit entries. Generated canonical artifact: 10 pages + `404.html` + `assets/projections.json`; validator reports **324 sourced table rows**. Source IDs below resolve through the exact official URLs in section C and `verification/2026-11-10-2eefc54d.md`.

| Page | Row | Label (truncated) | Source ID(s) / host | Links |
|---|---:|---|---|---:|
| `index.html` | 1 | Course of action | sec_10k, irs_544, treasury | 3 |
| `index.html` | 2 | Property-specific inputs | assessor, zimas | 2 |
| `index.html` | 3 | Tenant 2029–2032 ARD wall | sec_10q_debt, sec_10q_ar | 2 |
| `index.html` | 4 | Official population paths | dof_e1, dof_p2a, scag_appendix | 3 |
| `index.html` | 5 | County hazard & insurance | fema_county_query, openfema_la, cdi_fairplan_2025 | 3 |
| `market.html` | 1 | Los Angeles city land areaGeography | census_city | 1 |
| `market.html` | 2 | Los Angeles city population densityGeography | census_city | 1 |
| `market.html` | 3 | Los Angeles County land areaGeography | census_county | 1 |
| `market.html` | 4 | City population estimatePopulation | census_city | 1 |
| `market.html` | 5 | City population change from estimates basePopulation | census_city | 1 |
| `market.html` | 6 | County population estimatePopulation | census_county | 1 |
| `market.html` | 7 | County population change from estimates basePopulation | census_county | 1 |
| `market.html` | 8 | DOF P-2A July 1, 2025 county level vs Census V2025 estimatePopulation | dof_p2a, dof_e1, census_county | 3 |
| `market.html` | 9 | Median household incomeIncome | census_city | 1 |
| `market.html` | 10 | Median household incomeIncome | census_county | 1 |
| `market.html` | 11 | Per-capita incomeIncome | census_city | 1 |
| `market.html` | 12 | Poverty rateIncome | census_city | 1 |
| `market.html` | 13 | Median gross rentHousing | census_city | 1 |
| `market.html` | 14 | Owner-occupied housing unit rateHousing | census_city | 1 |
| `market.html` | 15 | Median owner-occupied home valueHousing | census_city | 1 |
| `market.html` | 16 | Average weekly wage, all industriesIncome | bls_summary | 1 |
| `market.html` | 17 | DOF city population estimate (E-1)Population | dof_e1 | 1 |
| `market.html` | 18 | DOF county population estimate (E-1 & July 2025)Population | dof_e1, dof_e5 | 2 |
| `market.html` | 19 | Net housing units added (statewide-highest county total)Housing | dof_e1 | 1 |
| `market.html` | 20 | Total retail salesEconomy | census_city | 1 |
| `market.html` | 21 | Accommodation and food-services salesEconomy | census_city | 1 |
| `market.html` | 22 | County nominal GDPEconomy | fred_county_gdp | 1 |
| `market.html` | 23 | Metro nominal GDP, latest availableEconomy | fred_metro_gdp | 1 |
| `market.html` | 24 | Unemployment rate, not seasonally adjustedLabor | bls_summary | 1 |
| `market.html` | 25 | Unemployment comparators, NSALabor | bls_summary | 1 |
| `market.html` | 26 | County labor force / employment / unemployedLabor | bls_laus | 1 |
| `market.html` | 27 | County unemployment rate, seasonally adjustedLabor | edd_la | 1 |
| `market.html` | 28 | Metro nonfarm payrollsLabor | bls_summary | 1 |
| `market.html` | 29 | County nonfarm wage and salary employment, SALabor | edd_la | 1 |
| `market.html` | 30 | Education and health services payrollsLabor | bls_summary | 1 |
| `market.html` | 31 | Leisure and hospitality payrollsLabor | bls_summary | 1 |
| `market.html` | 32 | Restaurants and other eating places employment changeLabor | edd_la | 1 |
| `market.html` | 33 | Information payrollsLabor | bls_summary | 1 |
| `market.html` | 34 | Manufacturing payrollsLabor | bls_summary | 1 |
| `market.html` | 35 | LA-area CPI-U year-over-yearInflation | bls_summary | 1 |
| `market.html` | 36 | City annual unemployment rate, historicalLabor | bls_city_annual | 1 |
| `market.html` | 37 | Treasury par yieldsFinancing | treasury | 1 |
| `market.html` | 38 | Port of Los Angeles annual throughput and economic impactEconomic drivers | port_facts, port_stats | 2 |
| `market.html` | 39 | Port of Los Angeles container throughputEconomic drivers | port_containers | 1 |
| `market.html` | 40 | Regional commute mode & remote-work divergenceEconomic drivers | scag_tr, scag_appendix | 2 |
| `market.html` | 41 | LAUSD combined four-/five-year graduation rateSchools | dashboard_engagement | 1 |
| `market.html` | 42 | LAUSD chronic absenteeismSchools | dashboard_engagement | 1 |
| `market.html` | 43 | LAUSD ELA distance from proficientSchools | dashboard_performance | 1 |
| `market.html` | 44 | LAUSD mathematics distance from proficientSchools | dashboard_performance | 1 |
| `market.html` | 45 | DTLA 2040 plan expectationsPlanning | dtla_release | 1 |
| `market.html` | 46 | LAPD citywide NIBRS crime profilePublic safety | lapd_city, lapd | 2 |
| `market.html` | 47 | LA Metro D Line extension & LAX Transit CenterPlanning | metro_dline, metro_lax | 2 |
| `market.html` | 48 | LAUSD district enrollment & student compositionSchools | cde_sdprofile | 1 |
| `market.html` | 49 | LAPD Operations-Central Bureau NIBRS crime profilePublic safety | lapd_central, lapd | 2 |
| `property.html` | 1 | Street address / parcel match | zimas, assessor | 2 |
| `property.html` | 2 | Assessor parcel number | assessor | 1 |
| `property.html` | 3 | Fee owner, vesting, easements, lender liens | assessor, prop13 | 2 |
| `property.html` | 4 | Legal tenant and operating entity | sec_10q | 1 |
| `property.html` | 5 | Guarantor, scope, recourse | sec_10q | 1 |
| `property.html` | 6 | Base rent, additional rent, escalations | sec_10k | 1 |
| `property.html` | 7 | Exact lease expiration and options | sec_10k | 1 |
| `property.html` | 8 | NNN scope and landlord retained obligations | sec_10k | 1 |
| `property.html` | 9 | Current market value / broker opinion / appraisal | treasury, sec_release | 2 |
| `property.html` | 10 | Property debt, rate, maturity, prepayment | treasury | 1 |
| `property.html` | 11 | Building condition, seismic/roof/HVAC/parking capital needs | usgs_faq, fema_nri | 2 |
| `property.html` | 12 | Insurance coverage, exclusions, deductibles, premium | cdi_claims | 1 |
| `property.html` | 13 | Tax basis, depreciation, owner entity, marginal rates | irs_544, ftb_capgains | 2 |
| `property.html` | 14 | Zoning, overlays, entitlements, alternative use | zimas, dtla_release | 2 |
| `property.html` | 15 | Phase I/II environmental status | epa_brownfields | 1 |
| `property.html` | 16 | Assigned schools / attendance boundary | cde_directory, dashboard_faq | 2 |
| `property.html` | 17 | Owner liquidity, concentration, tax and estate objectives | irs_544, ftb_capgains | 2 |
| `property.html` | 18 | Identity gate | assessor, zimas | 2 |
| `property.html` | 19 | Credit gate | sec_10q, sec_release | 2 |
| `property.html` | 20 | Cash-flow gate | sec_10k, prop13 | 2 |
| `property.html` | 21 | Exit gate | treasury, ula, irs_544 | 3 |
| `property.html` | 22 | Jack in the Box system same-store salesTenant | sec_release | 1 |
| `property.html` | 23 | Jack in the Box restaurant countTenant | sec_release | 1 |
| `property.html` | 24 | Quarterly revenueTenant | sec_release | 1 |
| `property.html` | 25 | Net earningsTenant | sec_release | 1 |
| `property.html` | 26 | Adjusted EBITDATenant | sec_release | 1 |
| `property.html` | 27 | Cash and debt balancesTenant | sec_release, sec_10q | 2 |
| `property.html` | 28 | Securitized refinancingTenant | sec_10q_debt, sec_release | 2 |
| `property.html` | 29 | FY2026 restaurant guidanceTenant | sec_release | 1 |
| `property.html` | 30 | Issuer leadership transition (Form 8-K)Tenant | sec_8k_sept2026 | 1 |
| `property.html` | 31 | California Jack in the Box restaurants, FY2025Tenant | sec_10k | 1 |
| `property.html` | 32 | California share of Jack systemTenant | sec_10k | 1 |
| `property.html` | 33 | Securitized debt 2029–2032 ARD concentration (overlapping lease window)Tenant | sec_10q_debt | 1 |
| `property.html` | 34 | Franchisee accounts & notes allowance for credit lossesTenant | sec_10q_ar | 1 |
| `property.html` | 35 | Issuer lease footprint, ROU obligations & rental spreadTenant | sec_10q_leases, sec_10k_leases, sec_10k, sec_10q_contingencies | 4 |
| `property.html` | 36 | Treasury par yieldsFinancing | treasury | 1 |
| `property.html` | 37 | Los Angeles Measure ULA thresholdsTaxes | ula | 1 |
| `property.html` | 38 | Measure ULA additional ratesTaxes | ula | 1 |
| `property.html` | 39 | Proposition 13 general levy and assessed growthTaxes | prop13, boe_reassessment | 2 |
| `property.html` | 40 | California individual capital-gains treatmentTaxes | ftb_capgains | 1 |
| `property.html` | 41 | Deferred like-kind exchange timingTaxes | irs_8824 | 1 |
| `property.html` | 42 | Covered fast-food minimum wageLabor costs | dir_fastfood | 1 |
| `property.html` | 43 | California general minimum wageLabor costs | dir_minwage | 1 |
| `property.html` | 44 | Los Angeles city general minimum wageLabor costs | la_wage | 1 |
| `property.html` | 45 | LA County + LA City combined documentary transfer tax stackTaxes | lavote_dtt, ula | 2 |
| `property.html` | 46 | California general minimum wage (effective January 1, 2027)Labor costs | dir_release_2027 | 1 |
| `projections.html` | 1 | 2026 | dof_p2a | 1 |
| `projections.html` | 2 | 2027 | dof_p2a | 1 |
| `projections.html` | 3 | 2028 | dof_p2a | 1 |
| `projections.html` | 4 | 2029 | dof_p2a | 1 |
| `projections.html` | 5 | 2030 | dof_p2a | 1 |
| `projections.html` | 6 | 2031 | dof_p2a | 1 |
| `projections.html` | 7 | 2032 | dof_p2a | 1 |
| `projections.html` | 8 | 2033 | dof_p2a | 1 |
| `projections.html` | 9 | 2034 | dof_p2a | 1 |
| `projections.html` | 10 | 2035 | dof_p2a | 1 |
| `projections.html` | 11 | 2030 | dof_p2a | 1 |
| `projections.html` | 12 | 2035 | dof_p2a | 1 |
| `projections.html` | 13 | 2040 | dof_p2a | 1 |
| `projections.html` | 14 | 2045 | dof_p2a | 1 |
| `projections.html` | 15 | 2050 | dof_p2a | 1 |
| `projections.html` | 16 | 2019 | scag_appendix | 1 |
| `projections.html` | 17 | 2030 | scag_appendix | 1 |
| `projections.html` | 18 | 2045 | scag_appendix | 1 |
| `projections.html` | 19 | 2050 | scag_appendix | 1 |
| `projections.html` | 20 | 2019 | scag_appendix | 1 |
| `projections.html` | 21 | 2030 | scag_appendix | 1 |
| `projections.html` | 22 | 2045 | scag_appendix | 1 |
| `projections.html` | 23 | 2050 | scag_appendix | 1 |
| `projections.html` | 24 | 2019 | scag_appendix | 1 |
| `projections.html` | 25 | 2030 | scag_appendix | 1 |
| `projections.html` | 26 | 2045 | scag_appendix | 1 |
| `projections.html` | 27 | 2050 | scag_appendix | 1 |
| `projections.html` | 28 | 2030 | dof_p2a, scag_appendix | 2 |
| `projections.html` | 29 | 2045 | dof_p2a, scag_appendix | 2 |
| `projections.html` | 30 | 2050 | dof_p2a, scag_appendix | 2 |
| `projections.html` | 31 | Accommodation and food service | scag_tr | 1 |
| `projections.html` | 32 | Health care and social assistance | scag_tr | 1 |
| `projections.html` | 33 | Retail | scag_tr | 1 |
| `projections.html` | 34 | Transportation and warehousing | scag_tr | 1 |
| `projections.html` | 35 | Manufacturing | scag_tr | 1 |
| `projections.html` | 36 | Rent interruption | sec_release, sec_10k | 2 |
| `projections.html` | 37 | NNN cost leakage | sec_10k, prop13 | 2 |
| `projections.html` | 38 | Re-tenanting / capital shock | sec_10k, usgs_faq | 2 |
| `projections.html` | 39 | Exit valuation shock | treasury, sec_release | 2 |
| `projections.html` | 40 | Discount-rate shock | treasury, irs_544 | 2 |
| `projections.html` | 41 | Tax / transfer-cost shock | ula, irs_544, ftb_capgains | 3 |
| `projections.html` | 42 | Hazard / insurance shock | fema_county_query, cdi_claims, usgs_faq | 3 |
| `projections.html` | 43 | Net Sale Proceeds | sec_10k, irs_544, treasury | 3 |
| `projections.html` | 44 | Hold Npv | sec_10k, irs_544, treasury | 3 |
| `projections.html` | 45 | Renew Npv | sec_10k, irs_544, treasury | 3 |
| `projections.html` | 46 | Retenant Npv | sec_10k, irs_544, treasury | 3 |
| `projections.html` | 47 | Recommended Path | sec_10k, irs_544, treasury | 3 |
| `decision.html` | 1 | Sell before expiry | sec_10k, irs_544, ula, treasury | 4 |
| `decision.html` | 2 | Renew / extend with tenant | sec_release, sec_10k, treasury | 3 |
| `decision.html` | 3 | Hold without extension | sec_release, fema_county_query, cdi_claims | 3 |
| `decision.html` | 4 | Sell to user / operator / redeveloper | zimas, dtla_release, epa_brownfields | 3 |
| `decision.html` | 5 | Sale plus 1031 exchange / diversification | irs_8824, irs_544, ftb_capgains | 3 |
| `decision.html` | 6 | Refinance / recapitalize | treasury, sec_release | 2 |
| `decision.html` | 7 | Prepare re-tenanting / alternative use | sec_release, zimas, sec_10k | 3 |
| `decision.html` | 8 | Wealth preservation | irs_544, cdi_claims, fema_county_query | 3 |
| `decision.html` | 9 | Growth | sec_release, zimas, scag_appendix | 3 |
| `decision.html` | 10 | Manageable risk | sec_10k, treasury, sec_release | 3 |
| `risks.html` | 1 | Lease-term decayOrdinary lease risk | sec_10k | 1 |
| `risks.html` | 2 | Tenant / guarantor creditOrdinary tenant risk | sec_10q_debt, sec_10q_ar, sec_release | 3 |
| `risks.html` | 3 | NNN label versus actual obligationsOrdinary operating risk | sec_10k, prop13 | 2 |
| `risks.html` | 4 | Above-market rent / renewal resetOrdinary market risk | sec_release, sec_10k | 2 |
| `risks.html` | 5 | Vacancy and re-tenanting downtimeOrdinary market risk | sec_release, sec_10k | 2 |
| `risks.html` | 6 | Interest-rate / cap-rate repricingOrdinary financial risk | treasury | 1 |
| `risks.html` | 7 | Transfer taxes and closing costsOrdinary tax risk | lavote_dtt, ula | 2 |
| `risks.html` | 8 | Property-tax reassessmentOrdinary tax risk | prop13, boe_reassessment | 2 |
| `risks.html` | 9 | Capital gain / depreciation recaptureOrdinary tax risk | irs_544, ftb_capgains, irs_8824 | 3 |
| `risks.html` | 10 | Insurance availability / premium shockOrdinary insurance risk | cdi_claims, cdi_fairplan_2025, cdi_catmodel_2025 | 3 |
| `risks.html` | 11 | Labor and input-cost pressureOrdinary operating risk | dir_fastfood, la_wage, dir_release_2027, bls_summary | 4 |
| `risks.html` | 12 | Access, visibility, parking, circulationOrdinary site risk | zimas, dtla_release | 2 |
| `risks.html` | 13 | Crime / perception / operating hoursOrdinary community risk | lapd_city, lapd_central, lapd | 3 |
| `risks.html` | 14 | Contamination / historical useOrdinary environmental risk | epa_brownfields | 1 |
| `risks.html` | 15 | EarthquakeRare high-impact hazard | fema_county_query, usgs_faq, usgs_shakeout, cgs_alquist_priolo, cgs_shma | 5 |
| `risks.html` | 16 | Wildfire / smoke / insurance marketRare high-impact hazard | calfire_acres, calfire_fhsz, calfire_palisades, calfire_eaton, openfema_la | 5 |
| `risks.html` | 17 | Inland flooding / storm drainageRare high-impact hazard | fema_county_query, fema_nri | 2 |
| `risks.html` | 18 | Heat, landslide, wind, lightning, tornadoRare high-impact hazard | fema_hazard_ratings | 1 |
| `risks.html` | 19 | Tenant bankruptcy or system shockBlack-swan / severe stress | sec_release, sec_10k | 2 |
| `risks.html` | 20 | Capital-market freezeBlack-swan / severe stress | treasury, sec_release | 2 |
| `risks.html` | 21 | Regulatory / tax / zoning shockBlack-swan / severe stress | ula, dir_fastfood, zimas | 3 |
| `risks.html` | 22 | Compound disasterBlack-swan / severe stress | fema_county_query, cdi_claims, sec_release | 3 |
| `risks.html` | 23 | FEMA NRI composite riskHazards | fema_county_query, fema_nri | 2 |
| `risks.html` | 24 | FEMA NRI total expected annual lossHazards | fema_county_query | 1 |
| `risks.html` | 25 | FEMA NRI earthquake riskHazards | fema_county_query | 1 |
| `risks.html` | 26 | FEMA NRI wildfire riskHazards | fema_county_query | 1 |
| `risks.html` | 27 | FEMA NRI inland flooding riskHazards | fema_county_query, fema_nri | 2 |
| `risks.html` | 28 | FEMA NRI coastal flooding riskHazards | fema_coastal_score, fema_hazard_ratings, fema_county_query | 3 |
| `risks.html` | 29 | Social vulnerability / community resilienceHazards | fema_county_query | 1 |
| `risks.html` | 30 | Other county hazard ratingsHazards | fema_hazard_ratings | 1 |
| `risks.html` | 31 | UCERF3 regional earthquake probabilitiesHazards | usgs_faq | 1 |
| `risks.html` | 32 | CAL FIRE FHSZ mapped acres, Los Angeles CountyHazards | calfire_acres, calfire_fhsz | 2 |
| `risks.html` | 33 | Very High share of mapped FHSZ acresHazards | calfire_acres | 1 |
| `risks.html` | 34 | Eaton/Palisades wildfire claims trackerInsurance | cdi_claims | 1 |
| `risks.html` | 35 | Federal disaster declarations (OpenFEMA tally, 1969–2025)Hazards | openfema_la | 1 |
| `risks.html` | 36 | 2026 SRA FHSZ update & Jan 2025 Palisades/Eaton incident damageHazards | calfire_fhsz, calfire_palisades, calfire_eaton | 3 |
| `risks.html` | 37 | CGS Alquist-Priolo/SHMA rules & USGS M7.8 ShakeOut benchmarkHazards | cgs_alquist_priolo, cgs_shma, usgs_shakeout | 3 |
| `risks.html` | 38 | Urban heat island mitigation & cooling load contextHazards | epa_heat | 1 |
| `risks.html` | 39 | CDI FAIR Plan commercial limits & catastrophe model reformInsurance | cdi_fairplan_2025, cdi_catmodel_2025 | 2 |
| `requirements.html` | 1 | Property identity and privacy | assessor, zimas | 2 |
| `requirements.html` | 2 | Lease, tenant, guaranty, options, notices | sec_10k, sec_10q | 2 |
| `requirements.html` | 3 | Geography, population, income, housing | census_city, census_county | 2 |
| `requirements.html` | 4 | Employment, job growth, economic drivers, inflation | bls_summary, edd_la, fred_county_gdp, port_stats | 4 |
| `requirements.html` | 5 | Schools and community context | dashboard_engagement, dashboard_performance, cde_directory | 3 |
| `requirements.html` | 6 | Tenant / lease credit | sec_10k, sec_10q, sec_release | 3 |
| `requirements.html` | 7 | Value influences and taxes | treasury, ula, prop13, irs_544, ftb_capgains | 5 |
| `requirements.html` | 8 | Ordinary risks and rare high-impact events | fema_county_query, usgs_faq, calfire_acres, cdi_claims, sec_release, epa_brownfields, lapd | 7 |
| `requirements.html` | 9 | Reliable transparent projection/scenario system | dof_p2a, scag_appendix, repo | 3 |
| `requirements.html` | 10 | All decision paths and balanced recommendation | sec_10k, irs_8824, treasury, zimas | 4 |
| `requirements.html` | 11 | Every published table row links to an official source | repo | 1 |
| `requirements.html` | 12 | Unconfirmed values blank and flagged | repo | 1 |
| `requirements.html` | 13 | Coordinate parallel sessions and preserve prior work | repo | 1 |
| `requirements.html` | 14 | PR, merge, and live deployment verification | repo, live | 2 |
| `flagged.html` | 1 | Exact parcel, address, APN, title, and owner | assessor, zimas | 2 |
| `flagged.html` | 2 | Exact expiry, options, notices, rent, escalations, NNN scope | sec_10k | 1 |
| `flagged.html` | 3 | Legal tenant, franchisee, guarantor, recourse | sec_10q, sec_release | 2 |
| `flagged.html` | 4 | Market value, cap rate, debt, prepayment, owner discount rate | treasury, sec_release | 2 |
| `flagged.html` | 5 | Tax basis, depreciation, entity, marginal rates, 1031 eligibility | irs_544, ftb_capgains, irs_8824 | 3 |
| `flagged.html` | 6 | Roof, structure, seismic, HVAC, parking, capital plan | usgs_faq, fema_nri | 2 |
| `flagged.html` | 7 | Policy forms, exclusions, deductibles, premium, business interruption | cdi_claims | 1 |
| `flagged.html` | 8 | Parcel FHSZ, flood zone, fault/soil/landslide exposure | calfire_fhsz, fema_nri, usgs_faq | 3 |
| `flagged.html` | 9 | Assigned schools and attendance boundary | cde_directory, dashboard_faq | 2 |
| `flagged.html` | 10 | Current parcel-area crime statistics | lapd_city, lapd_central, lapd | 3 |
| `flagged.html` | 11 | Phase I/II environmental condition | epa_brownfields | 1 |
| `flagged.html` | 12 | Zoning, overlays, alternative use, entitlement feasibility | zimas, dtla_release | 2 |
| `flagged.html` | 13 | SCAG manufacturing future-change percentage | scag_tr | 1 |
| `flagged.html` | 14 | USGS 30-year probability start date | usgs_faq | 1 |
| `flagged.html` | 15 | Prior 26%/35% FHSZ expansion claims | calfire_fhsz, calfire_acres | 2 |
| `flagged.html` | 16 | Old executive-summary metro GDP $1.355T (2024) and county ranking | fred_metro_gdp, fred_county_gdp, repo | 3 |
| `flagged.html` | 17 | Stale December 2025 labor headline | bls_summary, edd_la, bls_city_annual | 3 |
| `flagged.html` | 18 | GitHub Pages serving path | repo, live | 2 |
| `flagged.html` | 19 | Obsolete verify-data.mjs gate | repo | 1 |
| `flagged.html` | 20 | Competing historical pages/site/archive builds | repo | 1 |
| `flagged.html` | 21 | Archived arena-ffc97e4e unresolved conflict markers | repo, repo_line_audit | 2 |
| `flagged.html` | 22 | DOF 2025 county population exceeds the Census V2025 estimate by 158,501 (+1.63%) | dof_p2a, dof_e1, census_county, dof_landing | 4 |
| `flagged.html` | 23 | Repository commit metadata (outside website content) may expose personal contact details o | repo | 1 |
| `flagged.html` | 24 | Prior 2026-11-08 California unit count (351 / 16.4%) inverted Del Taco vs Jack in the Box | sec_10k, sec_release, dir_fastfood | 3 |
| `flagged.html` | 25 | Root markdown executive briefs vs the published dashboard | repo | 1 |
| `flagged.html` | 26 | FEMA coastal-flood numeric score previously linked to a query without its score field | fema_coastal_score, fema_hazard_ratings, fema_county_query | 3 |
| `flagged.html` | 27 | Independent confirmation of the FY2025 Form 10-K California unit-column correction | sec_10k, sec_release | 2 |
| `sources.html` | 1 | QuickFacts: Los Angeles city, California; Vintage 2025census_city | census_city | 1 |
| `sources.html` | 2 | QuickFacts: Los Angeles County, California; Vintage 2025census_county | census_county | 1 |
| `sources.html` | 3 | Los Angeles Area Economic Summary, updated November 4, 2026bls_summary | bls_summary | 1 |
| `sources.html` | 4 | LAUS series LAUCN060370000000003: Los Angeles County unemployment rate, NSAbls_laus | bls_laus | 1 |
| `sources.html` | 5 | Annual unemployment rates for 50 largest cities, 2025bls_city_annual | bls_city_annual | 1 |
| `sources.html` | 6 | Los Angeles County preliminary labor force and industry employment, September 2026edd_la | edd_la | 1 |
| `sources.html` | 7 | GDPALL06037: Total Gross Domestic Product for Los Angeles County, CAfred_county_gdp | fred_county_gdp | 1 |
| `sources.html` | 8 | NGMP31080: Total Gross Domestic Product for Los Angeles-Long Beach-Anaheim, CA (MSA), disc | fred_metro_gdp | 1 |
| `sources.html` | 9 | Daily Treasury Par Yield Curve Rates, November 2026treasury | treasury | 1 |
| `sources.html` | 10 | Population Projections, Baseline 2024; Vintage 2026 release notesdof_landing | dof_landing | 1 |
| `sources.html` | 11 | P-2A: Total Population for California and Counties, Baseline 2024 / Vintage 2026dof_p2a | dof_p2a | 1 |
| `sources.html` | 12 | Connect SoCal 2024; Connect SoCal 2050 in developmentscag_plan | scag_plan | 1 |
| `sources.html` | 13 | Connect SoCal 2024 Technical Report: Demographics and Growth Forecastscag_tr | scag_tr | 1 |
| `sources.html` | 14 | Connect SoCal 2024 Final PEIR Appendix I, updated tablesscag_appendix | scag_appendix | 1 |
| `sources.html` | 15 | DTLA 2040 New Zoning Code adoption press release, December 4, 2024dtla_release | dtla_release | 1 |
| `sources.html` | 16 | Zoning Search / ZIMAS parcel lookupzimas | zimas | 1 |
| `sources.html` | 17 | Assessor parcel searchassessor | assessor | 1 |
| `sources.html` | 18 | Proposition 13 property tax overviewprop13 | prop13 | 1 |
| `sources.html` | 19 | Letter 2022/046: Change in Ownership — Base Year Value Transfers; Prop 13 current-law summ | boe_reassessment | 1 |
| `sources.html` | 20 | Measure ULA FAQula | ula | 1 |
| `sources.html` | 21 | Capital gains and lossesftb_capgains | ftb_capgains | 1 |
| `sources.html` | 22 | Publication 544: Sales and Other Dispositions of Assetsirs_544 | irs_544 | 1 |
| `sources.html` | 23 | Instructions for Form 8824 (2025): Like-Kind Exchangesirs_8824 | irs_8824 | 1 |
| `sources.html` | 24 | Fast Food Minimum Wage FAQdir_fastfood | dir_fastfood | 1 |
| `sources.html` | 25 | Minimum Wage FAQdir_minwage | dir_minwage | 1 |
| `sources.html` | 26 | 2026 Minimum Wage Ordinance notice, effective July 1, 2026la_wage | la_wage | 1 |
| `sources.html` | 27 | California School Dashboard 2026: Los Angeles Unified, Academic Engagementdashboard_engage | dashboard_engagement | 1 |
| `sources.html` | 28 | California School Dashboard 2026: Los Angeles Unified, Academic Performancedashboard_perfo | dashboard_performance | 1 |
| `sources.html` | 29 | California School Dashboard FAQdashboard_faq | dashboard_faq | 1 |
| `sources.html` | 30 | California School Directorycde_directory | cde_directory | 1 |
| `sources.html` | 31 | Jack in the Box Inc. FY2025 Form 10-Ksec_10k | sec_10k | 1 |
| `sources.html` | 32 | Jack in the Box Inc. Q3 FY2026 Form 10-Qsec_10q | sec_10q | 1 |
| `sources.html` | 33 | Jack in the Box Inc. Q3 FY2026 earnings release, Exhibit 99.1sec_release | sec_release | 1 |
| `sources.html` | 34 | National Risk Index for Natural Hazards; v1.20 December 2025fema_nri | fema_nri | 1 |
| `sources.html` | 35 | National Risk Index Counties feature layer; data updated December 16, 2025fema_county_item | fema_county_item | 1 |
| `sources.html` | 36 | NRI Counties official query: Los Angeles County risk, EAL, vulnerability, resilience, eart | fema_county_query | 1 |
| `sources.html` | 37 | NRI Counties official query: Los Angeles County 18 hazard ratingsfema_hazard_ratings | fema_hazard_ratings | 1 |
| `sources.html` | 38 | What is the probability that an earthquake will occur in the Los Angeles Area? In the San  | usgs_faq | 1 |
| `sources.html` | 39 | Fire Hazard Severity Zonescalfire_fhsz | calfire_fhsz | 1 |
| `sources.html` | 40 | Fire Hazard Severity Zone acres, state and local responsibility, 2024–2025calfire_acres | calfire_acres | 1 |
| `sources.html` | 41 | Wildfire Claims Tracker, updated July 6, 2026cdi_claims | cdi_claims | 1 |
| `sources.html` | 42 | Crime Mapping and COMPSTATlapd | lapd | 1 |
| `sources.html` | 43 | Brownfields and Land Revitalizationepa_brownfields | epa_brownfields | 1 |
| `sources.html` | 44 | Port of Los Angeles Statistics hubport_stats | port_stats | 1 |
| `sources.html` | 45 | Jack1 repository: source, verification, and coordination recordsrepo | repo | 1 |
| `sources.html` | 46 | Live GitHub Pages dashboardlive | live | 1 |
| `sources.html` | 47 | Tracked repository line-by-line audit manifest (2026-11-10)repo_line_audit | repo_line_audit | 1 |
| `sources.html` | 48 | Jack in the Box Inc. Form 8-K, Exhibit 99.1 (board refreshment; CEO transition; cooperatio | sec_8k_sept2026 | 1 |
| `sources.html` | 49 | Report E-1 Population and Housing Estimates (January 1, 2026; released May 1, 2026)dof_e1 | dof_e1 | 1 |
| `sources.html` | 50 | July 2025 Population Estimates (released February 2026)dof_e5 | dof_e5 | 1 |
| `sources.html` | 51 | LAUSD District Profile 2025-26 (CDS 19647330000000)cde_sdprofile | cde_sdprofile | 1 |
| `sources.html` | 52 | Documentary Transfer Tax — General Information (County & Special City Rates)lavote_dtt | lavote_dtt | 1 |
| `sources.html` | 53 | News Release 2026-66: California Minimum Wage Increases to $17.40 Effective Jan. 1, 2027di | dir_release_2027 | 1 |
| `sources.html` | 54 | Port of Los Angeles Facts and Figures (CY 2025)port_facts | port_facts | 1 |
| `sources.html` | 55 | Port of Los Angeles Container Statistics (Through September 2026)port_containers | port_containers | 1 |
| `sources.html` | 56 | D Line Subway Extension Project (Section 1 opened May 8, 2026; Sec. 2–3 forecast 2027)metr | metro_dline | 1 |
| `sources.html` | 57 | LAX/Metro Transit Center Station Official Openingmetro_lax | metro_lax | 1 |
| `sources.html` | 58 | LAPD COMPSTAT Citywide Profile (Through Oct 31, 2026)lapd_city | lapd_city | 1 |
| `sources.html` | 59 | LAPD COMPSTAT Operations-Central Bureau Profile (Through Oct 31, 2026)lapd_central | lapd_central | 1 |
| `sources.html` | 60 | Jack in the Box Q3 FY2026 10-Q Note 7 (Indebtedness / ARDs / Leverage)sec_10q_debt | sec_10q_debt | 1 |
| `sources.html` | 61 | Jack in the Box Q3 FY2026 10-Q Note 1 (Basis & Allowance for Credit Losses)sec_10q_ar | sec_10q_ar | 1 |
| `sources.html` | 62 | Jack in the Box Q3 FY2026 10-Q Note 5 (Leases / Rental Spread)sec_10q_leases | sec_10q_leases | 1 |
| `sources.html` | 63 | Jack in the Box FY2025 10-K Note 10 (Lease Term & Commitments)sec_10k_leases | sec_10k_leases | 1 |
| `sources.html` | 64 | Jack in the Box Q3 FY2026 10-Q Note 13 (Commitments & Contingencies)sec_10q_contingencies | sec_10q_contingencies | 1 |
| `sources.html` | 65 | OpenFEMA Disaster Declarations Summaries v2 (LA County Query)openfema_la | openfema_la | 1 |
| `sources.html` | 66 | Palisades Fire Official Incident Recordcalfire_palisades | calfire_palisades | 1 |
| `sources.html` | 67 | Eaton Fire Official Incident Recordcalfire_eaton | calfire_eaton | 1 |
| `sources.html` | 68 | Alquist-Priolo Earthquake Fault Zonescgs_alquist_priolo | cgs_alquist_priolo | 1 |
| `sources.html` | 69 | Seismic Hazard Zones (Liquefaction & Landslide)cgs_shma | cgs_shma | 1 |
| `sources.html` | 70 | The ShakeOut Scenario: Hypothetical Mw7.8 Southern San Andreas Earthquakeusgs_shakeout | usgs_shakeout | 1 |
| `sources.html` | 71 | Commissioner Approves FAIR Plan Commercial Expansion ($20M/$100M, Release 028-2025)cdi_fai | cdi_fairplan_2025 | 1 |
| `sources.html` | 72 | CDI Completes First Wildfire Catastrophe Model Review (Release 052-2025)cdi_catmodel_2025 | cdi_catmodel_2025 | 1 |
| `sources.html` | 73 | Heat Islands Overview (Updated September 30, 2026)epa_heat | epa_heat | 1 |
| `sources.html` | 74 | NRI Counties official query: Los Angeles County coastal flooding risk index score and rati | fema_coastal_score | 1 |
| `audit.html` | 1 | Repository inventory and privacy scan | repo, repo_line_audit | 2 |
| `audit.html` | 2 | Git conflict-marker scan | repo, repo_line_audit | 2 |
| `audit.html` | 3 | Baseline structural validator | repo | 1 |
| `audit.html` | 4 | Official-source re-read | census_city, bls_summary, dof_p2a, scag_appendix, sec_release, fema_county_query, repo | 7 |
| `audit.html` | 5 | Projection method | dof_p2a, scag_appendix, repo | 3 |
| `audit.html` | 6 | Decision support | sec_10k, irs_544, treasury, repo | 4 |
| `audit.html` | 7 | Public artifact boundary | repo, live | 2 |
| `audit.html` | 8 | Deployment verification | repo, live | 2 |
| `audit.html` | 9 | Independent re-verification pass (session b8188ee0, 08 Nov 2026) | census_city, sec_10q, fema_county_query | 3 |
| `audit.html` | 10 | Independent re-verification pass (session c5e199ef, 10 Nov 2026) | treasury, dof_p2a, census_county, sec_release | 4 |
| `audit.html` | 11 | Independent re-verification pass, session af77a54e (2026-11-10) | repo | 1 |
| `audit.html` | 12 | Full repo line-audit & live official re-verification (session ac5b9087, 10 Nov 2026) | repo_line_audit, sec_10q_debt, dof_e1, treasury, lavote_dtt | 5 |
| `audit.html` | 13 | Independent line-by-line official-source re-verification (session 2eefc54d, 2026-11-10) | fema_coastal_score, sec_10k, repo_line_audit | 3 |

## F. V-2 final gates

- `python3 scripts/build_public.py --check` → PASS: 12 generated files match the verified dataset.
- `python3 -m unittest discover -s tests -p 'test_*.py' -q` → 14 tests OK.
- `python3 scripts/validate_site.py` → PASS: 10 pages, 324 sourced table rows, allowlist/local links/privacy/blanks OK.
- `python3 scripts/build_public.py --out /tmp/jack1-site-2eefc54d` + `python3 scripts/validate_site.py --site ... --artifact` → PASS: 10 pages, 324 sourced table rows, strict curated artifact boundary.
- Dataset/reference integrity: zero missing source IDs; zero canonical rows without source links; zero privacy hits in canonical pages or new reports. Noncanonical legacy root HTML files are excluded from the published artifact and were not modified.


## E. Privacy and scope

Only official domains and the repository/live provenance links appear above. Personal contact metadata present on some official pages was used solely to confirm the institutional source and was not copied. Historical internal notes under `research/0e369d53/` and `verification/2026-11-08-0e369d53.md` preserve an earlier California-column misreading; they are not part of the curated public artifact and are not edited by this session. The canonical dataset and `property.html` are corrected in V-2.
