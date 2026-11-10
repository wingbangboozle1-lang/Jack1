# Line-by-line research log — session 2eefc54d — 2026-11-10 (UTC)

This is the internal research companion to `verification/2026-11-10-2eefc54d.md`. It preserves the source trail used for manual review. No personal names, email addresses, phone numbers, APNs, or owner identifiers from official pages are reproduced here.

## A. Source groups re-read

The verification report contains all 49 source IDs, official links, and exact re-read notes. This pass closes the groups that session `c5e199ef` listed as "Not re-read this pass": SEC 10-K California table; SCAG 2030/2045 rows and sector endpoints; Q3 FY2026 10-Q balance detail; 8-K filing date / role-only governance; CAL FIRE, LAPD, Port, EPA, IRS, FTB, BOE, and Assessor/ZIMAS guidance; FEMA coastal-flood numeric score.

## B. Critical cross-checks

1. **FY2025 10-K state table.** The table has separate Del Taco and Jack in the Box column groups. California Del Taco = 94 company + 257 franchise = 351 total. California Jack in the Box = 96 company + 845 franchise = 941 total. The brand system total is 2,136 Jack in the Box restaurants (150 company + 1,986 franchise), separate from 576 Del Taco restaurants. Therefore 941 ÷ 2,136 = 44.1%, not 351 ÷ 2,136 = 16.4%. Official link: <https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm>.
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

## D. Final row inventory

The final generated-row inventory, with each row's official source link(s), is appended after V-2 regeneration so that it reflects the corrected dataset and canonical pages.

## E. Privacy and scope

Only official domains and the repository/live provenance links appear above. Personal contact metadata present on some official pages was used solely to confirm the institutional source and was not copied. Historical internal notes under `research/0e369d53/` and `verification/2026-11-08-0e369d53.md` preserve an earlier California-column misreading; they are not part of the curated public artifact and are not edited by this session. The canonical dataset and `property.html` are corrected in V-2.
