/* =====================================================================
   Jack1 — Master data registry
   Central Los Angeles Jack in the Box NNN lease decision support.
   Every figure is either (a) tied to an official source (status "official"),
   (b) a reputable secondary source (status "secondary"),
   (c) broker/market data with NO official source (status "market"), or
   (d) genuinely unverified (status "unverified") / illustrative ("illustrative").
   Status badges render on every table row. Nothing is asserted without one.
   NO PERSONAL INFORMATION IS STORED OR PUBLISHED HERE.
   ===================================================================== */

window.JACK1_SOURCES = {
  quickfacts_la_city: { label: "U.S. Census Bureau — QuickFacts: Los Angeles city, California", url: "https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia,US/PST045224", type: "official" },
  fred_lacounty_pop:  { label: "U.S. Census Bureau via FRED — LA County population, ACS 5-yr 2024 (B03002001E006037)", url: "https://fred.stlouisfed.org/series/B03002001E006037", type: "official" },
  fred_lacounty_mhi:  { label: "U.S. Census Bureau SAIPE via FRED — LA County median household income 2024 (MHICA06037A052NCEN)", url: "https://fred.stlouisfed.org/series/MHICA06037A052NCEN", type: "official" },
  fred_gdp_lacounty:  { label: "U.S. BEA via FRED — LA County GDP (current $), GDPALL06037 (2024 = $1,002.965B)", url: "https://fred.stlouisfed.org/series/GDPALL06037", type: "official" },
  bea_county_gdp_2026:{ label: "U.S. BEA — Gross Domestic Product by County, 2024 (news release, Feb 2026)", url: "https://www.bea.gov/news/2026/gross-domestic-product-county-and-personal-income-county-2024", type: "official" },
  usafacts_gdp:       { label: "USAFacts — LA County GDP 2024 (real $810.8B, +2.1%; per-capita $83,173) — secondary, citing BEA", url: "https://usafacts.org/answers/what-is-the-gross-domestic-product-gdp/county/los-angeles-county-ca/", type: "secondary" },
  fred_unemp_msa:     { label: "U.S. BLS via FRED — LA-LB-Anaheim MSA unemployment rate (LAUMT063108000000003A): 2025 avg 5.3%; Dec 2025 4.8%", url: "https://fred.stlouisfed.org/series/LAUMT063108000000003A", type: "official" },
  bls_metro_sep2026:  { label: "U.S. BLS — Metropolitan Area Employment and Unemployment (news release, 2026) — 2025 NSA rate 5.5%; labor force ≈6.73M", url: "https://www.bls.gov/news.release/pdf/metro.pdf", type: "official" },
  fred_gs10:          { label: "Board of Governors FRS via FRED — 10-Year Treasury yield, GS10: Oct 2026 = 5.13% (Jun 4.47% · Jul 4.60% · Aug 4.68% · Sep 4.99%)", url: "https://fred.stlouisfed.org/series/GS10", type: "official" },
  sec_jack10k:        { label: "SEC EDGAR — Jack in the Box Inc. Form 10-K, FY ended 2025-09-28 (CIK 807882, filed 2025-11-19, accession 0000807882-25-000072)", url: "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000807882&type=10-K", type: "official" },
  sec_jack10q_q3:     { label: "SEC EDGAR — Jack in the Box Inc. Form 10-Q, Q3 FY2025 (13 weeks ended 2025-07-06)", url: "https://www.sec.gov/Archives/edgar/data/807882/000080788225000043/jack-20250706.htm", type: "official" },
  stocktitan_10k:     { label: "StockTitan (SEC filing summary) — JACK FY2025 10-K: $1.5B revenue, $270.9M adj. EBITDA, Del Taco divestiture ~$115M, dividend discontinued", url: "https://www.stocktitan.net/sec-filings/JACK/10-k-jack-in-the-box-inc-files-annual-report-23704df3bd29.html", type: "secondary" },
  stockanalysis_jack:  { label: "StockAnalysis.com (financials aggregator) — JACK net loss FY2024 −$36.7M; FY2025 −$80.7M — secondary, not audited-source", url: "https://stockanalysis.com/stocks/jack/forecast/", type: "secondary" },
  marketscreener_10k:  { label: "MarketScreener (SEC filing reprint) — JACK FY2025 Form 10-K text", url: "https://www.marketscreener.com/news/jack-in-the-box-annual-report-for-fiscal-year-ending-september-28-2025-form-10-k-ce7d5ed9da8ef024", type: "secondary" },
  netleaseadvisor_jib: { label: "Net Lease Advisor (broker) — JIB tenant overview: avg cap 4.91% (TTM Mar 2024), avg sale $2,707,997, avg NOI $129,846, avg SF 2,500, not S&P/Moody's rated", url: "https://netleaseadvisor.com/tenant/jack-in-the-box/", type: "market" },
  solidinvestments_nnn:{ label: "Solid Investments (broker) — NNN offerings, Dec 2025: new 20-yr JIB NNN 5.0%–6.5% cap, 10%/5-yr bumps, 93% franchised", url: "https://www.solidinvestmentsfl.com/nnnproperties_forsale.htm", type: "market" },
  constantcontact_westwood:{ label: "Broker offering (Constant Contact) — JIB Westwood absolute NNN: $7.4M, 4.31% cap, expires 2031/2036 (listing text inconsistent), ±2,025 SF", url: "https://myemail.constantcontact.com/Jack-in-the-Box---55-Yr-Operating-History---Absolute-NNN---4-31--CAP---Westwood--Los-Angeles--CA.html?soid=1102006692645&aid=myxzmDI-jgw", type: "market" },
  cde_dashboard:      { label: "California School Dashboard — Los Angeles Unified (district 1964733), 2025: ELA 17.8 pts below standard (improved from 28.2 in 2024); College/Career 54.9% prepared (+3.8); EL progress 51.5%", url: "https://www.caschooldashboard.org/reports/19647330000000/2025/academic-performance", type: "official" },
  cde_cci_grid:       { label: "California Dept. of Education — 2025 College/Career Five-by-Five: LAUSD district placement = MEDIUM (Green, increased); 152 schools graded", url: "https://www6.cde.ca.gov/californiamodel/grid?indicator=cci&year=2025&cdcode=1964733&scode=&reporttype=schools", type: "official" },
  lausd_caaspp:       { label: "LA Unified (district release) — 2025 CAASPP highest ever districtwide; improvement 3.93% vs 1.76% statewide; all grades above 2019 levels", url: "https://www.lausd.org/apps/news/article/2144518?categoryId=23516", type: "official" },
  ca_dash_math:       { label: "California School Dashboard — LAUSD 2025 math points-from-standard: NOT captured in research pull (row left blank/flagged)", url: "https://www.caschooldashboard.org/reports/19647330000000/2025/academic-performance", type: "unverified" },
  finance_ula:        { label: "City of Los Angeles — Office of Finance: Measure ULA (Homelessness & Housing Solutions Tax) — 4% > $5M; 5.5% ≥ $10M; thresholds CPI-adjusted annually; LA City only", url: "https://finance.lacity.gov/faq/measure-ula", type: "official" },
  lacity_cao_ula:     { label: "City of LA CAO — Nov 2026 report: ULA thresholds currently $5.4M / $10.9M (Chained CPI-adjusted); applies to residential AND commercial; base tax 0.45% city + 0.11% county", url: "https://cityclerk.lacity.org/election/Measure_TE.pdf", type: "official" },
  la_county_fire_factsheet: { label: "LA County — Eaton & Palisades Fires anniversary fact sheet: Eaton 14,021 ac, 9,414 structures destroyed, 19 deaths; Palisades 23,448 ac, 6,837 structures, 12 deaths; $5.2–10.1B output loss; ~6,800 businesses; ~47,000 workers", url: "https://file.lacounty.gov/SDSInter/lac/1199046_Eaton_Palisades_Fires_Anniversary_Fact_Sheet.pdf", type: "official" },
  calfire_eaton:      { label: "CAL FIRE — 2025 incidents: Eaton Fire (2025-01-07, LA County Fire)", url: "https://www.fire.ca.gov/incidents/2025/1/7/eaton-fire", type: "official" },
  calfire_palisades:  { label: "CAL FIRE — 2025 incidents: Palisades Fire (2025-01-07, LA City Fire)", url: "https://www.fire.ca.gov/incidents/2025/1/7/palisades-fire", type: "official" },
  usgs_northridge:    { label: "USGS — M 6.7 Northridge earthquake, 1994-01-17 12:30:55 UTC, depth 18.2 km; est. $20B losses (USGS OFR 94-179-I)", url: "https://earthquake.usgs.gov/earthquakes/eventpage/ci3144585/executive", type: "official" },
  usgs_ofr:           { label: "USGS Open-File Report — Northridge: ~10M people shaken; most costly U.S. earthquake at the time", url: "https://www.usgs.gov/media/videos/northridge-ca-earthquake-open-file-report-94-179-i", type: "official" },
  metro_dline:        { label: "LA Metro — D Line Subway Extension: Section 1 (Wilshire/La Brea, Fairfax, La Cienega) opened 2026-05-08; Sections 2–3 (Beverly Hills, Century City, Westwood/VA) forecast 2026–2027", url: "https://www.metro.net/d-line-extension/", type: "official" },
  latimes_dline:      { label: "LA Times — D Line Extension cost ≈ $9.7B; opens to Westwood by fall 2027 — secondary", url: "https://www.latimes.com/california/story/2026-05-07/los-angeles-metro-d-line-extension", type: "secondary" },
  la28:               { label: "LA28 (official) — Olympic Games July 14–30, 2028; Paralympics Aug 15–27, 2028", url: "https://la28.org/en.html", type: "official" },
  lahsa_2025:         { label: "LAHSA — Finalized 2025 Greater LA Homeless Count: LA CoC 67,777; City of LA 43,695; countywide 72,195 (revised Oct 2025); second straight annual decline", url: "https://www.lahsa.org/news?article=1051-lahsa-releases-finalized-2025-homeless-count-results-after-hud-review", type: "official" },
  latimes_fire_map:   { label: "LA Times — Jan 2025 fires: ~40,000 acres, ~12,000+ structures (early count), est. $250B total economic loss — secondary", url: "https://www.latimes.com/california/story/2025-01-16/mapping-los-angeles-damage-from-the-eaton-and-palisades-fires-altadena-pasadena", type: "secondary" },
  commercialobserver_dtla: { label: "Commercial Observer — DTLA office vacancy ≈27.5% (Jul 2025); multifamily occupancy ≈91% (near/above pre-COVID) — secondary; other estimates cited 22%–33.3%", url: "https://commercialobserver.com/2025/07/downtown-la/", type: "secondary" },
  tolj_dtla:          { label: "TOLJ Commercial — DTLA office vacancy 33.3% Q3 2025; availability 36.8%; national avg ≈14% — secondary, unverified", url: "https://toljcommercial.com/downtown-la-office-amenities-2026/", type: "secondary" },
  bisnow_cca:         { label: "Bisnow — Central City Association study (Aug 2025): DTLA office vacancy ≈22% (record high); warns of up to $70B property-value loss — secondary", url: "https://www.bisnow.com/los-angeles/news/office/downtown-los-angeles-office-buildings-property-tax-value-loss-risk-130517", type: "secondary" },
  ca_boe_prop13:      { label: "California State Board of Equalization — Proposition 13: 1% base rate cap; assessed value +≤2%/yr until change of ownership (sale resets base year)", url: "https://www.boe.ca.gov/proptaxes/faqs.htm", type: "official" },
  la_assessor_fact:   { label: "LA County Office of the Assessor — Real Property Assessments fact sheet: base year value set at market at purchase; +≤2%/yr; change-of-ownership reassessment; 2024-25 roll > $1.997T", url: "https://assessor.lacounty.gov/", type: "official" },
  tradingecon_la_unemp_peak: { label: "TradingEconomics — LA MSA unemployment record 17.9% (May 2020) — secondary, derived from BLS", url: "https://tradingeconomics.com/united-states/unemployment-rate-in-los-angeles-long-beach-santa-ana-ca-msa-percent-m-nsa-fed-data.html", type: "secondary" },
  dir_fastfood:       { label: "California DIR / Fast Food Council — $20.00/hr minimum wage for covered fast-food restaurant employees (60+ locations nationally), effective 2024-04-01", url: "https://www.dir.ca.gov/iwc/minimum-wage-fastfood.htm", type: "official" },
  boe_prop13_overview:{ label: "CA State Board of Equalization — Proposition 13 overview (1% cap; 2% annual limit; reassessment on change of ownership)", url: "https://www.boe.ca.gov/proptaxes/prop13.htm", type: "official" },
  fema_flood:         { label: "FEMA — Flood Map Service Center (parcel-level flood status must be checked by the buyer/owner; central LA is largely Zone X but not universally)", url: "https://msc.fema.gov/portal/home", type: "official" },
  calfire_fhsz:       { label: "CAL FIRE / OSFM — Fire Hazard Severity Zone viewer (parcel-level; Central LA generally not Very High FHSZ — verify per parcel)", url: "https://egis.fire.ca.gov/fhsz/", type: "official" },
  cdog:               { label: "CA Geological Survey — Alquist-Priolo Earthquake Fault Zones (parcel-level lookup required)", url: "https://www.conservation.ca.gov/cgs/alquist-priolo", type: "official" },
  insurance_ca:       { label: "California Dept. of Insurance — property insurance market conditions post-2025 wildfires; FAIR Plan exposure rising (no audited figure republished here)", url: "https://www.insurance.ca.gov/", type: "official" }
};

/* Table row schema:
   { m: metric, v: value, g: geography/detail, p: period, s: [sourceIds], st: 'official'|'secondary'|'market'|'unverified'|'illustrative', n: notes } */
window.JACK1_DATA = {

  demographics: [
    { m:"Population estimate, July 1 2025", v:"3,869,089", g:"Los Angeles city", p:"2025-07-01", s:["quickfacts_la_city"], st:"official", n:"QuickFacts (V2025)" },
    { m:"Population change since 2020 census (base)", v:"−0.8%", g:"Los Angeles city", p:"Apr 2020 → Jul 2025", s:["quickfacts_la_city"], st:"official", n:"2020 base 3,899,342" },
    { m:"Population, ACS 5-yr estimate", v:"9,808,667", g:"Los Angeles County", p:"2024", s:["fred_lacounty_pop"], st:"official", n:"Down from 10.04M (2020)" },
    { m:"Median household income (in 2024 $)", v:"$81,939", g:"Los Angeles city", p:"2020–2024", s:["quickfacts_la_city"], st:"official", n:"US = $80,734" },
    { m:"Median household income (SAIPE)", v:"$90,757", g:"Los Angeles County", p:"2024", s:["fred_lacounty_mhi"], st:"official", n:"2023: $86,499 · 2022: $82,455" },
    { m:"Per capita income (in 2024 $)", v:"$47,685", g:"Los Angeles city", p:"2020–2024", s:["quickfacts_la_city"], st:"official", n:"US = $44,673" },
    { m:"Persons in poverty", v:"16.5%", g:"Los Angeles city", p:"2025 (SAIPE-based QuickFacts)", s:["quickfacts_la_city"], st:"official", n:"US = 10.2%" },
    { m:"Bachelor's degree or higher (25+)", v:"38.5%", g:"Los Angeles city", p:"2020–2024", s:["quickfacts_la_city"], st:"official", n:"US = 35.7%" },
    { m:"High-school graduate or higher (25+)", v:"79.6%", g:"Los Angeles city", p:"2020–2024", s:["quickfacts_la_city"], st:"official", n:"US = 89.6%" },
    { m:"Owner-occupied housing unit rate", v:"36.0%", g:"Los Angeles city", p:"2020–2024", s:["quickfacts_la_city"], st:"official", n:"US = 65.2% (mostly renters)" },
    { m:"Median value, owner-occupied housing", v:"$921,200", g:"Los Angeles city", p:"2020–2024", s:["quickfacts_la_city"], st:"official", n:"US = $332,700" },
    { m:"Median gross rent", v:"$1,933", g:"Los Angeles city", p:"2020–2024", s:["quickfacts_la_city"], st:"official", n:"US = $1,413" },
    { m:"Households / persons per household", v:"1,439,097 / 2.61", g:"Los Angeles city", p:"2020–2024", s:["quickfacts_la_city"], st:"official", n:"" },
    { m:"Foreign-born persons", v:"35.7%", g:"Los Angeles city", p:"2020–2024", s:["quickfacts_la_city"], st:"official", n:"US = 14.1%" },
    { m:"Language other than English at home (5+)", v:"56.4%", g:"Los Angeles city", p:"2020–2024", s:["quickfacts_la_city"], st:"official", n:"US = 22.3%" },
    { m:"In civilian labor force (16+)", v:"66.4%", g:"Los Angeles city", p:"2020–2024", s:["quickfacts_la_city"], st:"official", n:"Female 61.1%" },
    { m:"Mean travel time to work", v:"30.7 min", g:"Los Angeles city", p:"2020–2024", s:["quickfacts_la_city"], st:"official", n:"US = 26.4 min" },
    { m:"Same house as 1 year ago", v:"89.3%", g:"Los Angeles city", p:"2020–2024", s:["quickfacts_la_city"], st:"official", n:"High residential stability" },
    { m:"Retail sales per capita", v:"$21,281", g:"Los Angeles city", p:"2022", s:["quickfacts_la_city"], st:"official", n:"US = $20,928" },
    { m:"Total retail sales", v:"$81.35B", g:"Los Angeles city", p:"2022 (Economic Census)", s:["quickfacts_la_city"], st:"official", n:"$81,351,523 thousand" },
    { m:"Accommodation & food services sales", v:"$17.37B", g:"Los Angeles city", p:"2022 (Economic Census)", s:["quickfacts_la_city"], st:"official", n:"$17,366,966 thousand — QSR demand pool" },
    { m:"Hispanic or Latino population share", v:"47.2%", g:"Los Angeles city", p:"2020–2024", s:["quickfacts_la_city"], st:"official", n:"Core JIB customer demographic" }
  ],

  schools: [
    { m:"ELA — distance from standard (all students)", v:"17.8 pts below", g:"LAUSD district", p:"2025", s:["cde_dashboard"], st:"official", n:"Improved from 28.2 pts (2024) and 32.4 (2023)" },
    { m:"Mathematics — distance from standard (all students)", v:"—", g:"LAUSD district", p:"2025", s:["ca_dash_math"], st:"unverified", n:"Value not captured in research pull; read directly on CA School Dashboard before relying on it" },
    { m:"English Learner progress (met ELPI targets)", v:"51.5% making progress", g:"LAUSD district", p:"2025", s:["cde_dashboard"], st:"official", n:"Green level 4/5; 52,253 students" },
    { m:"College/Career readiness (grades 12)", v:"54.9% prepared", g:"LAUSD district", p:"2025", s:["cde_dashboard"], st:"official", n:"Level 4/5 green; +3.8 pts YoY; 29,408 students" },
    { m:"College/Career Five-by-Five placement", v:"MEDIUM — Green (increased)", g:"LAUSD district", p:"2025", s:["cde_cci_grid"], st:"official", n:"152 graded schools: 20 red, 27 orange, 25 yellow, 41 green, 39 blue" },
    { m:"CAASPP trajectory (districtwide)", v:"Record high; +3.93% YoY vs +1.76% state", g:"LAUSD district", p:"2025", s:["lausd_caaspp"], st:"official", n:"All grades above 2019 pre-pandemic levels (district release)" },
    { m:"Assigned school quality for the specific parcel", v:"—", g:"Subject asset (anonymized)", p:"n/a", s:["cde_dashboard"], st:"unverified", n:"Parcel anonymized for privacy — verify enrolled-school SARC and CA Dashboard for the exact address before any decision; schools are not the primary NNN driver but affect tenant traffic" }
  ],

  economy: [
    { m:"GDP (current dollars)", v:"$1,002.965B", g:"Los Angeles County", p:"2024", s:["fred_gdp_lacounty","bea_county_gdp_2026"], st:"official", n:"BEA county GDP, FRED GDPALL06037; 2023 = $956.2B" },
    { m:"Real GDP growth 2023→2024", v:"+2.1% (real $810.8B)", g:"Los Angeles County", p:"2024", s:["usafacts_gdp","bea_county_gdp_2026"], st:"secondary", n:"USAFacts citing BEA; verify against BEA release directly" },
    { m:"GDP per capita", v:"$83,173 (≈10th of 58 CA counties)", g:"Los Angeles County", p:"2024", s:["usafacts_gdp"], st:"secondary", n:"Secondary; BEA primary not directly verified — flagged" },
    { m:"Largest GDP sectors (2024)", v:"Information $134B · Prof./business services $120.3B · Real estate $105.9B", g:"Los Angeles County", p:"2024", s:["usafacts_gdp"], st:"secondary", n:"Secondary (USAFacts/BEA) — sector detail flagged" },
    { m:"County GDP rank (current $)", v:"#2 of U.S. county economies (behind NY County $1.007T)", g:"Los Angeles County", p:"2024", s:["bea_county_gdp_2026"], st:"secondary", n:"Ranking computed by secondary press from BEA table — flagged" },
    { m:"Unemployment rate — 2025 annual average", v:"5.3%", g:"LA-LB-Anaheim MSA", p:"2025", s:["fred_unemp_msa"], st:"official", n:"2024: 5.3% · 2023: 4.7% · 2022: 4.6% (SA)" },
    { m:"Unemployment — December 2025", v:"4.8%", g:"LA-LB-Anaheim MSA", p:"2025-12", s:["fred_unemp_msa"], st:"official", n:"Down from record 17.9% (May 2020)" },
    { m:"Unemployment — 2025 not-seasonally-adjusted", v:"5.5%", g:"LA-LB-Anaheim MSA", p:"2025", s:["bls_metro_sep2026"], st:"official", n:"Civilian labor force ≈ 6.73M (2025)" },
    { m:"Labor-force participation (16+)", v:"66.4% (female 61.1%)", g:"Los Angeles city", p:"2020–2024", s:["quickfacts_la_city"], st:"official", n:"" },
    { m:"Accommodation & food services sales", v:"$17.37B", g:"Los Angeles city", p:"2022", s:["quickfacts_la_city"], st:"official", n:"Economic Census — direct demand pool for QSR" },
    { m:"CA fast-food minimum wage (60+ unit chains)", v:"$20.00/hr", g:"California", p:"Effective 2024-04-01", s:["dir_fastfood"], st:"official", n:"Raises JIB franchisee labor costs — pressure on franchisee solvency" },
    { m:"10-year U.S. Treasury yield", v:"5.13%", g:"United States", p:"Oct 2026", s:["fred_gs10"], st:"official", n:"Jun 4.47% · Jul 4.60% · Aug 4.68% · Sep 4.99% — drives NNN cap rates" },
    { m:"DTLA office vacancy", v:"22% (CCA, Aug 2025) vs 27.5% (Commercial Observer) vs 33.3% (broker Q3-2025)", g:"Downtown LA", p:"2025", s:["bisnow_cca","commercialobserver_dtla","tolj_dtla"], st:"unverified", n:"Three conflicting estimates, different scopes/methodologies — none official; treat central-LA office distress as real but magnitude unconfirmed" },
    { m:"DTLA multifamily occupancy", v:"≈91% (near/above pre-COVID)", g:"Downtown LA", p:"2025", s:["commercialobserver_dtla"], st:"secondary", n:"Residential demand strong even as office struggles" },
    { m:"Homelessness (count)", v:"City of LA 43,695 · LA CoC 67,777 · county 72,195", g:"LA city / county", p:"Jan 2025 (revised Oct 2025)", s:["lahsa_2025"], st:"official", n:"Second consecutive annual decline; city −7.9% YoY" },
    { m:"D Line subway extension — Section 1 opened", v:"2026-05-08 (La Brea, Fairfax, La Cienega)", g:"Central / Westside LA", p:"2026", s:["metro_dline"], st:"official", n:"Sections 2–3 (Beverly Hills, Century City, Westwood/VA) forecast 2026–2027; cost ≈$9.7B (secondary)" },
    { m:"LA28 Olympic & Paralympic Games", v:"Jul 14–30, 2028 / Aug 15–27, 2028", g:"Los Angeles", p:"2028", s:["la28"], st:"official", n:"Expected investment/tourism catalyst for central LA" }
  ],

  market: [
    { m:"JIB — restaurants systemwide (Sept 28, 2025)", v:"2,136 (1,986 franchised = 93%)", g:"U.S. + Mexico/Guam", p:"FY2025", s:["sec_jack10k"], st:"official", n:"Del Taco: 576 units; Del Taco divested FY2025 (~$115M, secondary)" },
    { m:"JIB FY2025 total revenue", v:"$1.5B", g:"JIB Inc.", p:"FY2025", s:["stocktitan_10k","sec_jack10k"], st:"secondary", n:"10-K figure; per filing-summary reprint — verify exact number in 10-K" },
    { m:"JIB FY2025 adjusted EBITDA", v:"$270.9M", g:"JIB Inc.", p:"FY2025", s:["stocktitan_10k"], st:"secondary", n:"Turnaround plan 'JACK on Track'; dividend discontinued" },
    { m:"JIB system same-store sales growth", v:"−4.2%", g:"JIB Inc.", p:"FY2025", s:["stocktitan_10k"], st:"secondary", n:"Del Taco −3.7%; Q3-FY25 10-Q also shows declines" },
    { m:"JIB net loss", v:"FY2024 −$36.7M · FY2025 −$80.7M", g:"JIB Inc.", p:"FY2024–FY2025", s:["stockanalysis_jack"], st:"secondary", n:"Aggregator data — flagged; audited figures in 10-K" },
    { m:"JACK credit rating (S&P / Moody's)", v:"Not rated", g:"JIB Inc.", p:"as of Mar 2024 (stale)", s:["netleaseadvisor_jib"], st:"market", n:"Broker-reported; confirm with rating agencies; JACK is speculative-grade or unrated — weaker covenant for NNN buyers" },
    { m:"JIB average cap rate (TTM)", v:"4.91%", g:"JIB NNN market", p:"TTM to Mar 2024", s:["netleaseadvisor_jib"], st:"market", n:"Stale (Mar 2024) — reprice to today's 5.13% 10Y environment; expect higher caps" },
    { m:"JIB avg sale price / NOI / SF", v:"$2.708M · NOI $129,846 · $1,083/SF · 2,500 SF", g:"JIB NNN market", p:"TTM to Mar 2024", s:["netleaseadvisor_jib"], st:"market", n:"Stale; use only as order-of-magnitude anchor" },
    { m:"Asking cap — Westwood, LA absolute NNN JIB", v:"4.31% ($7.4M · ±2,025 SF · exp. 2031/2036 — listing internally inconsistent)", g:"West Los Angeles", p:"2026 offering", s:["constantcontact_westwood"], st:"market", n:"Listing text contradicts itself (2031 vs 2036) — flagged irregularity; example only, not subject asset" },
    { m:"New 20-yr JIB NNN cap-rate range", v:"5.0% – 6.5% (10%/5-yr bumps)", g:"National NNN market", p:"Dec 2025", s:["solidinvestments_nnn"], st:"market", n:"Broker offering range; used $5.5%–6.5% in sensitivity grid" },
    { m:"NNN lease structure (typical JIB)", v:"Absolute NNN · corporate or franchisee lease · 5–10% bumps / 5 yrs", g:"JIB NNN market", p:"market standard", s:["netleaseadvisor_jib","solidinvestments_nnn"], st:"market", n:"Subject lease instrument must be read — corporate vs franchisee guarantee changes risk materially" },
    { m:"Measure ULA transfer tax (LA City only)", v:"4% > $5.4M · 5.5% ≥ $10.9M (CPI-adjusted, 2026)", g:"City of Los Angeles", p:"2026", s:["lacity_cao_ula","finance_ula"], st:"official", n:"Applies to residential AND commercial; on TOP of base 0.45% city + 0.11% county; 1031 does NOT avoid ULA" },
    { m:"Base documentary transfer tax", v:"0.45% city + 0.11% county (≈0.56%)", g:"City + County of LA", p:"2026", s:["lacity_cao_ula"], st:"official", n:"On all real-property sales in LA" },
    { m:"Proposition 13 — sale consequence", v:"Buyer's assessed value resets to purchase price; +≤2%/yr thereafter", g:"California", p:"ongoing", s:["boe_prop13_overview","la_assessor_fact"], st:"official", n:"Tenant (NNN) typically pays property tax → reassessment inflates tenant's occupancy cost, suppresses supportable rent at renewal" },
    { m:"Estimated combined seller friction at $6.5M sale", v:"≈4.56% ULA + base ≈ 5.1% before capital gains", g:"City of Los Angeles", p:"2026", s:["lacity_cao_ula"], st:"illustrative", n:"Illustrative arithmetic, not tax advice — engage CPA; 4% ULA ≈ $260K + base ≈ $36K on $6.5M" }
  ],

  risk: [
    { m:"Lease expiry 2030–2035 — re-leasing / renewal risk", v:"HIGH", g:"Subject asset", p:"2030–2035", s:["sec_jack10k"], st:"official", n:"Value decays with remaining term; a dark asset single-tenant QSR loses NNN premium fast; renewal is the single biggest value lever", sev:"high" },
    { m:"Tenant credit — JIB franchisor distress", v:"HIGH", g:"JIB Inc. system", p:"FY2025–2026", s:["stocktitan_10k","stockanalysis_jack","netleaseadvisor_jib"], st:"secondary", n:"Same-store sales −4.2%; dividend discontinued; unrated; activist contested 2026 vote; 93% franchised → store-level guarantee usually a franchisee LLC, not JACK parent", sev:"high" },
    { m:"Cap-rate expansion / rate risk", v:"HIGH", g:"NNN market", p:"Oct 2026", s:["fred_gs10"], st:"official", n:"10Y at 5.13% (rising Jun→Oct 2026); every +50 bps on cap rate ≈ −7% value on a 6.9%-cap-equivalent asset", sev:"high" },
    { m:"Measure ULA transfer tax on sale", v:"MEDIUM-HIGH", g:"LA City", p:"2026", s:["lacity_cao_ula","finance_ula"], st:"official", n:"≈4% over $5.4M / 5.5% over $10.9M + 0.56% base; ~$290K+ on a $6.5M exit — large enough to change sell/hold math", sev:"med" },
    { m:"Wildfire — regional black swan", v:"LOW (central LA) / EXTREME (regional impact)", g:"LA region", p:"Jan 2025", s:["la_county_fire_factsheet","calfire_eaton","calfire_palisades"], st:"official", n:"Eaton 14,021 ac / 9,414 destroyed / 19 deaths; Palisades 23,448 ac / 6,837 / 12 deaths; $5.2–10.1B output loss; ~47,000 workers; insurance & construction-cost shock ripples citywide", sev:"med" },
    { m:"Earthquake — regional black swan", v:"MODERATE likelihood, EXTREME impact", g:"LA region", p:"historical", s:["usgs_northridge","usgs_ofr","cdog"], st:"official", n:"Northridge 1994 M6.7, 18.2 km depth, ~$20B losses; single-parcel seismic & Alquist-Priolo status MUST be checked per parcel", sev:"high" },
    { m:"Pandemic / public-health black swan", v:"LOW (repeat) / SEVERE impact", g:"LA MSA", p:"2020", s:["tradingecon_la_unemp_peak"], st:"secondary", n:"LA unemployment hit 17.9% May 2020 (secondary, from BLS); QSR proved resilient (drive-thru) but sit-down traffic collapsed — pandemic favors drive-thru JIB format", sev:"med" },
    { m:"DTLA economic distress / foot traffic", v:"MEDIUM-HIGH", g:"Central LA", p:"2023–2026", s:["commercialobserver_dtla","tolj_dtla","bisnow_cca"], st:"unverified", n:"Office vacancy 22–33.3% (conflicting sources, none official); multifamily ≈91% occupied; WFH structurally reduced central-LA daytime QSR traffic", sev:"med" },
    { m:"Homelessness / public safety perception", v:"MEDIUM", g:"Central LA", p:"Jan 2025", s:["lahsa_2025"], st:"official", n:"43,695 homeless in City of LA; encampments near QSR affect customer counts, loitering, security cost; improving trend (2nd annual decline)", sev:"med" },
    { m:"Insurance availability / cost inflation", v:"MEDIUM-HIGH", g:"California", p:"2025–2026", s:["insurance_ca"], st:"official", n:"Post-fire market stress; NNN tenant pays insurance, but coverage gaps (fire, earthquake) hit rent collectability & asset value; FAIR Plan reliance spreading", sev:"med" },
    { m:"Single-tenant concentration", v:"HIGH", g:"Subject asset", p:"ongoing", s:["netleaseadvisor_jib"], st:"market", n:"100% of income from one brand/operator; diversification requires sale or 1031 into multi-tenant replacement", sev:"high" },
    { m:"QSR labor-cost regulation ($20/hr fast food)", v:"MEDIUM", g:"California", p:"since 2024-04-01", s:["dir_fastfood"], st:"official", n:"Compresses franchisee margins → renewal rent growth must absorb it; raises default risk at weak stores", sev:"med" },
    { m:"CA Proposition 13 reassessment on sale", v:"MEDIUM", g:"California", p:"at sale", s:["boe_prop13_overview","la_assessor_fact"], st:"official", n:"Buyer's tax resets upward; NNN tenant bears the increase → reduces supportable renewal rent and buyer pricing", sev:"low" },
    { m:"Climate / heat & power grid events", v:"LOW-MEDIUM", g:"LA region", p:"ongoing", s:["calfire_fhsz"], st:"official", n:"PSPS shutoffs and heat waves disrupt QSR ops; central LA not Very-High FHSZ generally — verify parcel at CAL FIRE viewer", sev:"low" },
    { m:"Black swan — civil unrest / security event", v:"LOW likelihood / HIGH impact", g:"Central LA", p:"historical", s:["usgs_ofr"], st:"official", n:"1992 unrest precedent; downtown assets exposed to localized vandalism; insurance sub-limits apply", sev:"med" },
    { m:" Black swan — recession + rate shock combo", v:"MEDIUM likelihood", g:"National / LA", p:"forward 2030–2035", s:["fred_gs10","fred_unemp_msa"], st:"official", n:"Recession during remaining-term window → NNN values fall on BOTH cap-rate-up and NOI-down; stress-test hold NPV under 7.5% cap + flat rent", sev:"high" }
  ],

  decision: [],

  flagged: [
    { m:"All broker cap-rate comps (4.31% Westwood ask; 4.91% TTM; 5.0–6.5% new 20-yr range)", v:"No official source exists", g:"NNN market", p:"2024–2026", s:["constantcontact_westwood","netleaseadvisor_jib","solidinvestments_nnn"], st:"unverified", n:"Commercial real estate has no government cap-rate index; treat all cap data as indicative only. Commission a broker BPO/appraisal before transacting." },
    { m:"JIB credit 'not rated by S&P/Moody's'", v:"Broker-reported", g:"JIB Inc.", p:"Mar 2024", s:["netleaseadvisor_jib"], st:"market", n:"Confirm directly with S&P/Moody's; rating status may have changed" },
    { m:"JACK FY2024 −$36.7M / FY2025 −$80.7M net losses", v:"Aggregator-reported", g:"JIB Inc.", p:"FY2024–FY2025", s:["stockanalysis_jack"], st:"secondary", n:"Read the audited 10-K (SEC link in Sources) — do not rely on aggregator math" },
    { m:"JIB FY2025 revenue $1.5B; adj. EBITDA $270.9M; same-store sales −4.2%", v:"From filing-summary reprint", g:"JIB Inc.", p:"FY2025", s:["stocktitan_10k","marketscreener_10k"], st:"secondary", n:"10-K is authoritative; reprints transcribe it — confirm exact figures on EDGAR" },
    { m:"Del Taco divestiture ≈ $115M", v:"Press/filing-summary", g:"JIB Inc.", p:"FY2025", s:["stocktitan_10k"], st:"secondary", n:"Confirm closing date & proceeds in 8-K filings" },
    { m:"DTLA office vacancy — 22% vs 27.5% vs 33.3%", v:"Three conflicting estimates", g:"Downtown LA", p:"2025", s:["bisnow_cca","commercialobserver_dtla","tolj_dtla"], st:"unverified", n:"Different scopes (CBD vs broader downtown), methods, dates. No official series exists. Direction (vacancy elevated) is consistent across all three." },
    { m:"LA County GDP per-capita $83,173 & 2024 real GDP $810.8B (+2.1%)", v:"Secondary (USAFacts) citing BEA", g:"LA County", p:"2024", s:["usafacts_gdp"], st:"secondary", n:"BEA primary release confirms GDP level; per-capita figure not directly re-verified against BEA table — flagged" },
    { m:"LA County GDP '#2 behind NY County $1.007T'", v:"Ranking from secondary press of BEA data", g:"LA County", p:"2024", s:["bea_county_gdp_2026"], st:"secondary", n:"BEA release confirms $818.5B 'current dollars for large counties' sizing table — the $1.003T figure is CURRENT-dollar total from FRED; mixed measures in secondary coverage — do not mix without re-reading BEA tables" },
    { m:"Jan 2025 fires — '$250B economic loss'", v:"LA Times estimate", g:"LA region", p:"Jan 2025", s:["latimes_fire_map"], st:"secondary", n:"LA County official fact sheet cites $5.2–10.1B output loss / $2.2–4.2B labor income. Vastly different scopes. Use County figures for analysis; $250B is a broad total-loss estimate incl. property values" },
    { m:"Measure ULA exact 2026 thresholds ($5.4M / $10.9M)", v:"From LA City CAO report (Nov 2026)", g:"LA City", p:"2026", s:["lacity_cao_ula"], st:"official", n:"Thresholds are Chained-CPI adjusted annually — pull the current figure from finance.lacity.gov at the time of any LOI/escrow" },
    { m:"LAUSD 2025 math points-from-standard", v:"Not captured", g:"LAUSD", p:"2025", s:["ca_dash_math"], st:"unverified", n:"Left blank deliberately — do not fill in without reading the Dashboard directly" },
    { m:"Westwood listing internal inconsistency (2031 vs 2036 expiry)", v:"$7.4M / 4.31%", g:"West LA comp", p:"2026", s:["constantcontact_westwood"], st:"unverified", n:"Broker offering text self-contradictory — comp usable only as a soft illustration, never as a matched-pair valuation" },
    { m:"Projection model on this site", v:"All outputs illustrative", g:"n/a", p:"n/a", s:[], st:"illustrative", n:"Decision-support arithmetic only. Not an appraisal, not investment/tax/legal advice. Engage licensed appraiser, CPA, and counsel before transacting." },
    { m:"Specific parcel: school assignment, FHSZ class, Alquist-Priolo zone, FEMA flood zone, title/lease guarantee", v:"Not publicly verifiable without address", g:"Subject asset", p:"n/a", s:["calfire_fhsz","cdog","fema_flood"], st:"unverified", n:"Address deliberately withheld for privacy. Owner must verify each at the linked official viewers before closing any decision." },
    { m:"Subject asset lease terms (NOI, escalation, guarantee, expiry month)", v:"Not provided", g:"Subject asset", p:"2030–2035 window", s:[], st:"unverified", n:"Analysis framed on public market norms. The actual executed lease controls everything — pull it before any offer" }
  ]
};

window.JACK1_FLAG_COUNT = window.JACK1_DATA.flagged.length;
