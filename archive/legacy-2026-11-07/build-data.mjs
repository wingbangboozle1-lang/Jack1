#!/usr/bin/env node
/**
 * Builds the static JSON datasets consumed by the site.
 * Every row carries a source URL and a status. Rules enforced downstream by
 * scripts/verify-data.mjs:
 *   - status "verified" | "derived"  -> must have an https source URL on an allowlisted official domain
 *   - status "unverified"            -> value MUST be empty (never inferred)
 *   - status "placeholder"           -> property-specific private data withheld by design
 */
import { writeFileSync, mkdirSync } from "node:fs";

const U = {
  censusCity: "https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225",
  censusCounty: "https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045225",
  blsEag: "https://www.bls.gov/eag/eag.ca_losangeles_msa.htm",
  blsCpi: "https://www.bls.gov/regions/west/news-release/consumerpriceindex_losangeles.htm",
  dofP2A: "https://dof.ca.gov/media/docs/forecasting/Demographics/projections/P2A_County_Total.xlsx",
  dofProj: "https://dof.ca.gov/forecasting/demographics/projections/",
  sec10K: "https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm",
  secER: "https://www.sec.gov/Archives/edgar/data/807882/000080788225000070/ex991-q425earningsrelease.htm",
  secIndex: "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000807882&type=10-K&owner=include&count=10",
  cgs: "https://www.conservation.ca.gov/cgs/alquist-priolo",
  usgs: "https://www.usgs.gov/publications/shakeout-scenario-a-hypothetical-mw78-earthquake-southern-san-andreas-fault",
  usgsReport: "https://pubs.usgs.gov/of/2008/1150/",
  calfire: "https://www.fire.ca.gov/incidents/2025/1/7/palisades-fire/",
  osfm: "https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones",
  cdi: "https://www.insurance.ca.gov/0400-news/0100-press-releases/2024/release031-2024.cfm",
  cdi2023: "https://www.insurance.ca.gov/0400-news/0100-press-releases/2023/release051-2023.cfm",
  assessor: "https://assessor.lacounty.gov/tax-relief/decline-in-value",
  assessorContest: "https://assessor.lacounty.gov/homeowners/contest-assessment",
  ula: "https://cityattorney.lacity.gov/homelessness",
  ulaCd4: "https://cd4.lacity.gov/press-releases/cd4release_measureula_022223/",
  dir: "https://www.dir.ca.gov/AB1228/AB1228.html",
  nces: "https://nces.ed.gov/ccd/districtsearch/district_detail.asp?ID2=0622710",
  fred: "https://fred.stlouisfed.org/series/DGS10",
  fredInc: "https://fred.stlouisfed.org/series/MHICA06037A052NCEN",
};

const SRC = {
  censusCity: "U.S. Census Bureau, QuickFacts — Los Angeles city, CA",
  censusCounty: "U.S. Census Bureau, QuickFacts — Los Angeles County, CA",
  blsEag: "U.S. Bureau of Labor Statistics, Economy at a Glance — LA-Long Beach-Santa Ana MSA",
  blsCpi: "U.S. Bureau of Labor Statistics, CPI Los Angeles area, Sept 2026 (26-1595-SAN)",
  dofP2A: "California Dept. of Finance, Report P-2A County Population Projections (Baseline 2024, Vintage 2026)",
  sec10K: "Jack in the Box Inc., Form 10-K FY2025 (SEC accession 0000807882-25-000072)",
  secER: "Jack in the Box Inc., Q4/FY2025 earnings release, Exhibit 99.1 (SEC)",
  cgs: "California Geological Survey, Alquist-Priolo Earthquake Fault Zones",
  usgs: "U.S. Geological Survey, The ShakeOut Scenario (M7.8)",
  calfire: "CAL FIRE incident record, Palisades Fire (LA-69 Bravo)",
  osfm: "CAL FIRE — Office of the State Fire Marshal, Fire Hazard Severity Zones",
  cdi: "California Department of Insurance, FAIR Plan modernisation (release 031-2024)",
  assessor: "Los Angeles County Assessor, Decline-in-Value / Proposition 8",
  ula: "City of Los Angeles City Attorney — Measure ULA",
  dir: "California Dept. of Industrial Relations, AB 1228 Fast Food Council",
  nces: "National Center for Education Statistics, Common Core of Data — Los Angeles Unified (0622710)",
  fred: "Federal Reserve Bank of St. Louis (FRED), 10-Year Treasury Constant Maturity (DGS10)",
  fredInc: "Federal Reserve Bank of St. Louis (FRED), Median Household Income — Los Angeles County (SAIPE)",
};

/* [id, category, metric, value, unit, period, geography, srcKey, status, note] */
const rows = [
  // ---------- DEMOGRAPHICS ----------
  ["DEM-01","Demographics","Population (city of Los Angeles)","3,869,089","persons","July 1, 2025","Los Angeles city","censusCity","verified","Census Vintage 2025 estimate."],
  ["DEM-02","Demographics","Population (Los Angeles County)","9,694,934","persons","July 1, 2025","Los Angeles County","censusCounty","verified","Census Vintage 2025 estimate."],
  ["DEM-03","Demographics","Population change since 2020 (city)","-0.8","%","Apr 1 2020 -> Jul 1 2025","Los Angeles city","censusCity","verified","As published; base 3,899,342."],
  ["DEM-04","Demographics","Population change since 2020 (county)","-3.2","%","Apr 1 2020 -> Jul 1 2025","Los Angeles County","censusCounty","verified","As published; base 10,017,414. Largest county population decline in the state over the period."],
  ["DEM-05","Demographics","Population density","8,304.2","persons per sq mi","2020","Los Angeles city","censusCity","verified","Land area 469.49 sq mi."],
  ["DEM-06","Demographics","Foreign-born share","35.7","%","2020-2024","Los Angeles city","censusCity","verified",""],
  ["DEM-07","Demographics","Households","1,439,097","households","2020-2024","Los Angeles city","censusCity","verified",""],
  ["DEM-08","Demographics","Persons per household","2.61","persons","2020-2024","Los Angeles city","censusCity","verified","Household formation supports multi-person ordering baskets."],
  ["DEM-09","Demographics","Households","3,416,449","households","2020-2024","Los Angeles County","censusCounty","verified",""],
  ["DEM-10","Demographics","Residents aged 65+","17.1","%","July 1, 2025","Los Angeles County","censusCounty","verified","Ageing base changes daypart mix (fewer late-night, more breakfast)."],
  ["DEM-11","Demographics","Population density, county","","persons per sq mi","","Los Angeles County","censusCounty","unverified","County density was not displayed in the retrieved table segments. Deliberately left blank rather than computed from an unrelated source."],
  ["DEM-12","Demographics","Population inside the 3-mile trade area","","","","Subject trade area (placeholder)","censusCity","unverified","Trade-area population requires the parcel address. U-07 on the Flagged for Review page."],

  // ---------- INCOME & POVERTY ----------
  ["INC-01","Income & Poverty","Median household income (2024 dollars)","81,939","USD / year","2020-2024","Los Angeles city","censusCity","verified",""],
  ["INC-02","Income & Poverty","Per capita income (2024 dollars)","47,685","USD / year","2020-2024","Los Angeles city","censusCity","verified",""],
  ["INC-03","Income & Poverty","Persons below poverty line","16.5","%","2025 estimate","Los Angeles city","censusCity","verified",""],
  ["INC-04","Income & Poverty","Median household income","90,757","USD / year","2024","Los Angeles County","fredInc","verified","SAIPE-based series on FRED. Census QuickFacts did not display a county median in the retrieved segments, so the value is taken from this series instead; it corroborates the figure used in the archived build."],
  ["INC-05","Income & Poverty","Civilian labour force participation (16+)","66.4","%","2020-2024","Los Angeles city","censusCity","verified",""],
  ["INC-06","Income & Poverty","Uninsured residents under 65","10.7","%","2020-2024","Los Angeles city","censusCity","verified",""],
  ["INC-07","Income & Poverty","High school graduate or higher (25+)","79.6","%","2020-2024","Los Angeles city","censusCity","verified",""],
  ["INC-08","Income & Poverty","Bachelor's degree or higher (25+)","38.5","%","2020-2024","Los Angeles city","censusCity","verified",""],
  ["INC-09","Income & Poverty","Bachelor's degree or higher (25+)","36.0","%","2020-2024","Los Angeles County","censusCounty","verified",""],

  // ---------- HOUSING ----------
  ["HOU-01","Housing","Median value, owner-occupied unit","921,200","USD","2020-2024","Los Angeles city","censusCity","verified",""],
  ["HOU-02","Housing","Median gross rent","1,933","USD / month","2020-2024","Los Angeles city","censusCity","verified",""],
  ["HOU-03","Housing","Owner-occupied rate","36.0","%","2020-2024","Los Angeles city","censusCity","verified","Very low ownership = renter-heavy trade area, higher price sensitivity."],
  ["HOU-04","Housing","Housing units","3,726,923","units","July 1, 2025","Los Angeles County","censusCounty","verified",""],
  ["HOU-05","Housing","Building permits issued","22,250","permits","2025","Los Angeles County","censusCounty","verified","Supply response matters for redevelopment optionality."],
  ["HOU-06","Housing","Median gross rent","1,954","USD / month","2020-2024","Los Angeles County","censusCounty","verified",""],

  // ---------- ECONOMY & JOBS ----------
  ["ECO-01","Economy & Jobs","Unemployment rate","4.4","%","September 2026 (preliminary)","LA-Long Beach-Santa Ana MSA","blsEag","verified","Series LAUMT063108000000003."],
  ["ECO-02","Economy & Jobs","Civilian labour force","6,646.9","thousands","September 2026 (p)","LA-Long Beach-Santa Ana MSA","blsEag","verified","Series LAUMT063108000000006."],
  ["ECO-03","Economy & Jobs","Employment","6,352.9","thousands","September 2026 (p)","LA-Long Beach-Santa Ana MSA","blsEag","verified","Series LAUMT063108000000005."],
  ["ECO-04","Economy & Jobs","Total nonfarm employment","6,282.1","thousands","September 2026 (p)","LA-Long Beach-Santa Ana MSA","blsEag","verified","Series SMU06310800000000001."],
  ["ECO-05","Economy & Jobs","Total nonfarm, 12-month change","0.5","%","to September 2026","LA-Long Beach-Santa Ana MSA","blsEag","verified","Essentially flat payroll growth."],
  ["ECO-06","Economy & Jobs","Information sector employment","187.0","thousands","September 2026 (p)","LA-Long Beach-Santa Ana MSA","blsEag","verified",""],
  ["ECO-07","Economy & Jobs","Information sector, 12-month change","-5.7","%","to September 2026","LA-Long Beach-Santa Ana MSA","blsEag","verified","Largest declining sector; entertainment/tech contraction."],
  ["ECO-08","Economy & Jobs","Manufacturing, 12-month change","-1.2","%","to September 2026","LA-Long Beach-Santa Ana MSA","blsEag","verified",""],
  ["ECO-09","Economy & Jobs","Construction, 12-month change","0.0","%","to September 2026","LA-Long Beach-Santa Ana MSA","blsEag","verified",""],
  ["ECO-10","Economy & Jobs","Trade, transportation & utilities, 12-month change","0.3","%","to September 2026","LA-Long Beach-Santa Ana MSA","blsEag","verified",""],
  ["ECO-11","Economy & Jobs","Financial activities, 12-month change","-1.7","%","to September 2026","LA-Long Beach-Santa Ana MSA","blsEag","verified",""],
  ["ECO-12","Economy & Jobs","Professional & business services, 12-month change","-0.5","%","to September 2026","LA-Long Beach-Santa Ana MSA","blsEag","verified",""],
  ["ECO-13","Economy & Jobs","Education & health services, 12-month change","3.8","%","to September 2026","LA-Long Beach-Santa Ana MSA","blsEag","verified","Only clearly growing sector, and the least exposed to discretionary food spend."],
  ["ECO-14","Economy & Jobs","Accommodation & food services sales, 2022","17,366,966","USD thousands","2022","Los Angeles city","censusCity","verified","2022 Economic Census. ~$17.37bn — the addressable food market at city scale."],
  ["ECO-15","Economy & Jobs","Retail sales, 2022","81,351,523","USD thousands","2022","Los Angeles city","censusCity","verified",""],
  ["ECO-16","Economy & Jobs","Retail sales per capita, 2022","21,281","USD","2022","Los Angeles city","censusCity","verified",""],
  ["ECO-17","Economy & Jobs","Mean travel time to work","30.7","minutes","2020-2024","Los Angeles city","censusCity","verified","Commute pattern drives drive-thru daypart demand."],
  ["ECO-18","Economy & Jobs","Office-using employment within 3 miles","","","","Subject trade area (placeholder)","blsEag","unverified","Requires geocoded parcel; BLS publishes at MSA level only. U-08."],

  // ---------- PRICES ----------
  ["PRI-01","Prices","CPI-U all items, 12-month change","3.7","%","September 2026","Los Angeles-Long Beach-Anaheim","blsCpi","verified",""],
  ["PRI-02","Prices","CPI-U core (ex food & energy), 12-month change","2.6","%","September 2026","Los Angeles-Long Beach-Anaheim","blsCpi","verified",""],
  ["PRI-03","Prices","Food, 12-month change","2.8","%","September 2026","Los Angeles-Long Beach-Anaheim","blsCpi","verified",""],
  ["PRI-04","Prices","Food away from home, 12-month change","2.8","%","September 2026","Los Angeles-Long Beach-Anaheim","blsCpi","verified","Menu-price inflation running below all-items CPI: real price compression for restaurants."],
  ["PRI-05","Prices","Shelter, 12-month change","3.7","%","September 2026","Los Angeles-Long Beach-Anaheim","blsCpi","verified",""],
  ["PRI-06","Prices","Energy, 12-month change","20.3","%","September 2026","Los Angeles-Long Beach-Anaheim","blsCpi","verified",""],
  ["PRI-07","Prices","Gasoline, 12-month change","30.8","%","September 2026","Los Angeles-Long Beach-Anaheim","blsCpi","verified","Direct headwind to drive-thru traffic and to NNN utility costs."],

  // ---------- POPULATION OUTLOOK ----------
  ["POP-01","Population Outlook","Projected population 2030","9,727,305","persons","July 1, 2030 (projection)","Los Angeles County","dofP2A","verified","DOF Baseline 2024, Vintage 2026. Projection, not an observation."],
  ["POP-02","Population Outlook","Projected population 2035","9,708,647","persons","July 1, 2035 (projection)","Los Angeles County","dofP2A","verified","Upper end of the 2030-2035 lease-expiry window."],
  ["POP-03","Population Outlook","Projected population 2040","9,637,524","persons","July 1, 2040 (projection)","Los Angeles County","dofP2A","verified",""],
  ["POP-04","Population Outlook","Projected change 2025-2030","-1.28","%","2025-2030 (projection)","Los Angeles County","dofP2A","derived","Arithmetic on two published DOF values (9,727,305 / 9,853,435)."],
  ["POP-05","Population Outlook","Projected change 2025-2035","-1.47","%","2025-2035 (projection)","Los Angeles County","dofP2A","derived","Derived: 9,708,647 / 9,853,435 - 1 (two published DOF values). Covers the full 2030-2035 expiry window."],
  ["POP-06","Population Outlook","Projected change 2030-2035","-0.19","%","2030-2035 (projection)","Los Angeles County","dofP2A","derived","Derived: 9,708,647 / 9,727,305 - 1. Near-flat: no demographic tailwind inside the decision window."],
  ["POP-07","Population Outlook","Projected California population 2035","40,410,843","persons","July 1, 2035 (projection)","California","dofP2A","verified","State grows while the county shrinks — regional share is shifting away from LA."],

  // ---------- SCHOOLS ----------
  ["SCH-01","Schools","Students enrolled","408,026","students","2024-2025","Los Angeles Unified School District","nces","verified",""],
  ["SCH-02","Schools","Schools in district","784","schools","2025-2026 directory","Los Angeles Unified School District","nces","verified",""],
  ["SCH-03","Schools","Student / teacher ratio","19.20","students per teacher","2024-2025","Los Angeles Unified School District","nces","verified","Classroom teachers 21,246.18 FTE."],
  ["SCH-04","Schools","Total revenue per student","34,533","USD","2022-2023","Los Angeles Unified School District","nces","verified","Total revenue $14.77bn; federal 19% / state 55% / local 26%."],
  ["SCH-05","Schools","Total expenditure per student","26,866","USD","2022-2023","Los Angeles Unified School District","nces","verified",""],
  ["SCH-06","Schools","Total staff","55,601.49","FTE","2024-2025","Los Angeles Unified School District","nces","verified",""],
  ["SCH-07","Schools","District graduation rate","","","","Los Angeles Unified School District","nces","unverified","CDE DataQuest / CA School Dashboard are dynamic queries that did not return stable values to automated retrieval. U-05."],
  ["SCH-08","Schools","District test scores (CAASPP, ELA & math met/exceeded)","","","","Los Angeles Unified School District","nces","unverified","Same as SCH-07. U-05."],
  ["SCH-09","Schools","School ratings for the 3-mile trade area","","","","Subject trade area (placeholder)","nces","unverified","Requires parcel geocode. U-07."],

  // ---------- TENANT ----------
  ["TEN-01","Tenant","System restaurant count (Jack in the Box)","2,136","restaurants","Sep 28, 2025","National system","sec10K","verified","Item 1: 2,136 across 22 states."],
  ["TEN-02","Tenant","Franchised restaurants","1,986","restaurants","Sep 28, 2025","National system","sec10K","verified","93% franchised."],
  ["TEN-03","Tenant","Company-operated restaurants","150","restaurants","Sep 28, 2025","National system","sec10K","verified",""],
  ["TEN-04","Tenant","System count, prior year","2,191","restaurants","Sep 29, 2024","National system","secER","verified","Net decline of 55 units in FY2025."],
  ["TEN-05","Tenant","Same-store sales, FY2025 (system)","-4.2","%","FY2025","National system","secER","verified",""],
  ["TEN-06","Tenant","Same-store sales, Q4 FY2025 (system)","-7.4","%","Q4 FY2025","National system","secER","verified","Franchise -7.6%; the deterioration is in the franchise base."],
  ["TEN-07","Tenant","Restaurant openings, FY2025","31","restaurants","FY2025","National system","secER","verified",""],
  ["TEN-08","Tenant","Restaurant closures, FY2025","86","restaurants","FY2025","National system","secER","verified","38 of the 47 Q4 closures were part of the 'JACK on Track' block closure programme."],
  ["TEN-09","Tenant","Guided restaurant count, FY2026","2,050-2,100","restaurants","FY2026 guidance","National system","secER","verified",""],
  ["TEN-10","Tenant","Guided closures, FY2026","50-100","restaurants","FY2026 guidance","National system","secER","verified","'most of which will be franchise restaurants'."],
  ["TEN-11","Tenant","Guided same-store sales, FY2026","(-1) to (+1)","%","FY2026 guidance","National system","secER","verified",""],
  ["TEN-12","Tenant","Q4 revenue","326.2","USD millions","Q4 FY2025","Jack in the Box Inc.","secER","verified","-6.6% year over year."],
  ["TEN-13","Tenant","Q4 Adjusted EBITDA","45.6","USD millions","Q4 FY2025","Jack in the Box Inc.","secER","verified","Down from $65.5m."],
  ["TEN-14","Tenant","Guided FY2026 Adjusted EBITDA","225-240","USD millions","FY2026 guidance","Jack in the Box Inc.","secER","verified",""],
  ["TEN-15","Tenant","Dividend","discontinued","","FY2025","Jack in the Box Inc.","secER","verified","Cash-preservation signal."],
  ["TEN-16","Tenant","Divestiture: Del Taco","115","USD millions","Agreement signed Oct 15, 2025","Jack in the Box Inc.","sec10K","verified","Cash purchase price, subject to adjustments. Proceeds aimed at debt paydown."],
  ["TEN-17","Tenant","Standard franchise term","20","years","Current programme","National system","sec10K","verified","Initial fee $50,000; royalty generally 5.0% of gross sales."],
  ["TEN-18","Tenant","Prototype building size","1,372","square feet","Current prototype","National system","sec10K","verified","Small footprint = high land-value share in the asset."],
  ["TEN-19","Tenant","Combined-brand employees","5,046","employees","Sep 28, 2025","Jack in the Box Inc.","sec10K","verified","Largely franchised system."],
  ["TEN-20","Tenant","Operator of the subject unit (corporate vs. franchisee)","","","","Subject property","sec10K","unverified","Determines guarantor strength. Requires the lease. U-03."],
  ["TEN-21","Tenant","Guarantor structure on the subject lease","","","","Subject property","sec10K","unverified","Requires the lease. U-03."],
  ["TEN-22","Tenant","Same-store sales of the subject trade area","","","","Subject property","sec10K","unverified","Not published by unit. U-07."],

  // ---------- PROPERTY & LEASE ----------
  ["PRP-01","Property & Lease","Property street address","[WITHHELD]","","","Subject property","ula","placeholder","Private information. Withheld by design and never published."],
  ["PRP-02","Property & Lease","Assessor parcel number (APN)","[WITHHELD]","","","Subject property","assessor","placeholder","Private information."],
  ["PRP-03","Property & Lease","Owner name / entity","[WITHHELD]","","","Subject property","assessor","placeholder","Private information."],
  ["PRP-04","Property & Lease","Lease commencement date","[WITHHELD]","","","Subject property","sec10K","placeholder","Needed to compute remaining term."],
  ["PRP-05","Property & Lease","Lease expiry (owner-stated window)","[WITHHELD]","","Owner-stated window: 2030-2035","Subject property","sec10K","placeholder","Exact date withheld. The five-year uncertainty band is itself a valuation problem: buyers price the worst case."],
  ["PRP-06","Property & Lease","Remaining base term","","years","","Subject property","sec10K","unverified","Cannot be computed without the commencement date. U-03."],
  ["PRP-07","Property & Lease","Current annual base rent","[WITHHELD]","USD","","Subject property","sec10K","placeholder","Needed for every valuation line."],
  ["PRP-08","Property & Lease","Rent escalation structure","","","","Subject property","sec10K","unverified","Fixed bumps vs. CPI-linked changes the inflation hedge completely. U-03."],
  ["PRP-09","Property & Lease","Renewal / extension options held by tenant","","","","Subject property","sec10K","unverified","Number, length and mechanism (fixed vs. fair market) of options. U-03."],
  ["PRP-10","Property & Lease","Lease type","[WITHHELD]","","Owner-stated: NNN (triple net)","Subject property","ula","placeholder","Owner-supplied characteristic; the lease document itself was not available for review. U-03."],
  ["PRP-11","Property & Lease","Land area","","sq ft","","Subject property","assessor","unverified","Requires parcel data. U-02."],
  ["PRP-12","Property & Lease","Building area","","sq ft","","Subject property","sec10K","unverified","Requires rent roll / building record. U-03."],
  ["PRP-13","Property & Lease","Assessed value (Prop 13 base)","[WITHHELD]","USD","","Subject property","assessor","placeholder","Determines property-tax pass-through and reassessment at sale."],
  ["PRP-14","Property & Lease","Year built","","year","","Subject property","assessor","unverified","Drives seismic retrofit exposure (soft-story / URM). U-02."],
  ["PRP-15","Property & Lease","Zoning / community plan designation","","","","Subject property","ula","unverified","Drives residual land value and redevelopment optionality. U-04."],

  // ---------- TAX & REGULATION ----------
  ["REG-01","Tax & Regulation","Measure ULA rate, sales above $5m","4.0","% of price","In force since Apr 1, 2023","Los Angeles city","ula","verified","Applies to the full sale price, paid by the seller."],
  ["REG-02","Tax & Regulation","Measure ULA rate, sales above $10m","5.5","% of price","In force since Apr 1, 2023","Los Angeles city","ula","verified",""],
  ["REG-03","Tax & Regulation","Current CPI-indexed ULA thresholds","","USD","2026","Los Angeles city","ula","unverified","Statutory $5m/$10m are indexed annually. No official page with the current indexed figures was located; third-party figures conflict. U-09."],
  ["REG-04","Tax & Regulation","Proposition 13 assessment growth cap","2.0","% per year","In force","Los Angeles County","assessor","verified","Unless market value falls below the trended base value."],
  ["REG-05","Tax & Regulation","Proposition 8 decline-in-value relief","Available (temporary)","","Annual, filing Jul 2 - Nov 30","Los Angeles County","assessor","verified","Applies only when the Jan 1 market value is lower than the current assessed value."],
  ["REG-06","Tax & Regulation","California fast-food minimum wage","20.00","USD / hour","From April 1, 2024","California","dir","verified","AB 1228. Subsequent Council adjustments not verified (U-10)."],
  ["REG-07","Tax & Regulation","City of Los Angeles minimum wage (2026)","","USD / hour","2026","Los Angeles city","dir","unverified","Different instrument from the state fast-food wage. U-10."],
  ["REG-08","Tax & Regulation","County documentary transfer tax + city base transfer tax","","USD per $1,000","2026","Los Angeles city","ula","unverified","Needed for total exit cost alongside ULA. U-09."],

  // ---------- CATASTROPHE ----------
  ["CAT-01","Catastrophe","Palisades Fire — area burned","23,448","acres","Jan 2025","Los Angeles County","calfire","verified","Started 01/07/2025, contained 01/31/2025. Cause: arson."],
  ["CAT-02","Catastrophe","Palisades Fire — structures destroyed","6,845","structures","Jan 2025","Los Angeles County","calfire","verified","Plus 975 damaged."],
  ["CAT-03","Catastrophe","Palisades Fire — civilian fatalities","12","persons","Jan 2025","Los Angeles County","calfire","verified","3 civilian injuries, 1 firefighter injury."],
  ["CAT-04","Catastrophe","Fire Hazard Severity Zone tiers","Moderate / High / Very High","","Current maps","California","osfm","verified","SRA maps effective April 1, 2024; LRA (city) maps released Feb-Mar 2025."],
  ["CAT-05","Catastrophe","Fire Hazard Severity Zone rating of the subject parcel","","","","Subject property","osfm","unverified","Requires address lookup in the CAL FIRE viewer. U-01."],
  ["CAT-06","Catastrophe","Alquist-Priolo surface-fault-rupture setback","50","feet (generally)","In force","California","cgs","verified","Structures for human occupancy cannot be placed over a mapped active fault."],
  ["CAT-07","Catastrophe","Alquist-Priolo status of the subject parcel","","","","Subject property","cgs","unverified","Requires CGS EQ Zapp parcel lookup. U-02."],
  ["CAT-08","Catastrophe","Seismic hazard zone (liquefaction / landslide) status","","","","Subject property","cgs","unverified","Seismic Hazards Mapping Act is a separate regime from Alquist-Priolo. U-02."],
  ["CAT-09","Catastrophe","ShakeOut scenario: modelled deaths","1,800","persons","M7.8 scenario","Southern California","usgs","verified","Scenario, not a forecast."],
  ["CAT-10","Catastrophe","ShakeOut scenario: modelled economic losses","213","USD billions","M7.8 scenario","Southern California","usgs","verified","USGS Open-File Report 2008-1150."],
  ["CAT-11","Catastrophe","FAIR Plan commercial coverage limit","20","USD millions per location","2024 agreement","California","cdi","verified","Residential limit $3m; 'insurer of last resort'."],
  ["CAT-12","Catastrophe","Insurance cost / availability at the subject property","","","","Subject property","cdi","unverified","Requires current policy declaration pages. U-11."],
  ["CAT-13","Catastrophe","Post-event business interruption cover (NNN lease)","","","","Subject property","cdi","unverified","Lease-dependent; requires the policy and the lease. U-03 / U-11."],

  // ---------- CAPITAL MARKETS ----------
  ["CAP-01","Capital Markets","10-year Treasury constant maturity","4.90","%","2026-11-04","United States","fred","verified","Peak of 5.31% on 2026-10-05 in the retrieved window. Discount-rate anchor for the model."],
  ["CAP-02","Capital Markets","QSR net-lease cap rate for this asset","","%","","Subject property","fred","unverified","No official agency publishes QSR cap rates. Treated as a model assumption, never as data. U-06."],
  ["CAP-03","Capital Markets","Local commercial vacancy rate","","%","","Central Los Angeles","fred","unverified","Commercial market statistics are published by private data vendors, not by government. U-06."],
  ["CAP-04","Capital Markets","Achievable sale price / broker opinion of value","","USD","","Subject property","fred","unverified","Requires an appraisal or BOV. Not estimated here. U-06."],
];

const records = rows.map(([id, category, metric, value, unit, period, geography, srcKey, status, note]) => ({
  id, category, metric, value, unit, period, geography,
  source: SRC[srcKey], url: U[srcKey], status,
  source_class: "official",
  note: note || "",
}));

/* ---------------- RISK REGISTER ---------------- */
/* assessment fields are analyst judgement and are labelled as such on the site */
const risks = [
  ["RSK-01","Tenant credit","Tenant bankruptcy, franchisee default or lease rejection","business-as-usual","Medium","High",
   "Rent stops if the operator fails, even in a NNN lease. NNN protects against expenses, not against vacancy.",
   "Obtain lease + guarantor; require corporate guaranty or letter of credit on renewal; monitor JACK same-store sales and closures quarterly.",
   "JACK same-store sales, closure count, credit rating, franchisee distress disclosures in 10-Q/10-K.", "secER"],
  ["RSK-02","Lease timing","Expiry risk: value decays as remaining term shortens","business-as-usual","High","High",
   "Buyers of single-tenant NNN assets need long remaining term to finance; with 1-5 years left the buyer pool collapses to land buyers.",
   "Decide before the term premium is gone. Market the asset while 5+ years remain if exit is chosen.",
   "Remaining term, comparable NNN marketing times, lender appetite.", "sec10K"],
  ["RSK-03","Occupancy cost","Rent exceeds the unit's economic capacity at renewal","business-as-usual","Medium","High",
   "Franchise margins are compressing (Q4 franchise-level margin 38.9% from 40.4%); a rent reset upward is not available if sales are falling.",
   "Model renewal at flat-to-modest growth; do not underwrite market rent growth above CPI.",
   "Franchise-level margin, same-store sales, commodity inflation.", "secER"],
  ["RSK-04","Exit cost","Measure ULA transfer tax on a City of Los Angeles sale above $5m","business-as-usual","High","Medium",
   "4.0% of the full sale price (5.5% above $10m), paid by the seller, on top of documentary transfer taxes.",
   "Size the exit cost into the sale decision now; evaluate structured/installment sale; if timing is flexible, transact when pricing offsets the tax.",
   "City of Los Angeles ordinance and annual indexed thresholds.", "ula"],
  ["RSK-05","Property tax","Reassessment to market on sale","business-as-usual","High","Low-Medium",
   "A buyer's property tax resets at sale. In a NNN lease the tenant bears it, so the reset hits the tenant's occupancy cost and thus renewal capacity.",
   "Quantify the assessed-value step before marketing; show buyers a post-sale tax estimate to avoid price churn.",
   "Assessor assessed value and Prop 13/Prop 8 mechanics.", "assessor"],
  ["RSK-06","Labour cost","Further statutory wage increases for fast-food workers","business-as-usual","Medium","High",
   "$20/hour already applies (AB 1228). Any further Council increase hits store-level margin, which is the tenant's ability to pay rent.",
   "Stress-test tenant coverage at +5% and +10% labour cost.",
   "DIR Fast Food Council actions.", "dir"],
  ["RSK-07","Demand","Continued population and employment stagnation in LA County","business-as-usual","High","Medium",
   "DOF projects county population -1.5% by 2035; total nonfarm payrolls +0.5% y/y with Information -5.7%.",
   "Do not underwrite volume growth; treat growth as rent-escalation only.",
   "DOF P-2A, BLS LAUS/CES.", "dofP2A"],
  ["RSK-08","Interest rates","Cap-rate expansion from a higher-for-longer rate environment","business-as-usual","Medium","High",
   "10-year Treasury at 4.90% (2026-11-04); every 50 bp of cap-rate expansion removes ~8% of value at a 6.0% cap.",
   "Refinance analysis before sale; consider holding through a rate peak only if cash flow covers carry.",
   "FRED DGS10, transaction cap rates.", "fred"],
  ["RSK-09","Operating cost","Energy and utility pass-through spikes","business-as-usual","Medium","Medium",
   "Energy CPI +20.3% y/y and gasoline +30.8% (Sept 2026). NNN passes cost to tenant, which further pressures rent capacity.",
   "Confirm recovery mechanics and caps in the lease; review the CAM/utility reconciliation.",
   "BLS CPI Los Angeles.", "blsCpi"],
  ["RSK-10","Insurance","Carrier withdrawal or premium shock (wildfire-concentrated market)","business-as-usual","Medium","High",
   "FAIR Plan is the insurer of last resort; commercial limit $20m/location. Premium rises hit the tenant's NNN cost load.",
   "Obtain a current declaration page and a broker quote for the renewal year; consider a lender-required insurance covenant.",
   "California Department of Insurance FAIR Plan data.", "cdi"],
  ["RSK-11","Earthquake","M6.7-M7.8 rupture causing structural damage or total loss","black swan","Low (annual) / High (over 30 yrs)","Severe",
   "USGS ShakeOut: ~1,800 deaths and $213bn regional losses. Unreinforced masonry or soft-story buildings are the exposure.",
   "Seismic retrofit assessment; confirm earthquake cover and deductibles; keep a repair reserve.",
   "USGS ShakeOut Scenario; CGS Alquist-Priolo.", "usgs"],
  ["RSK-12","Wildfire","Regional wildfire destroying utility, insurance and consumer demand even if the parcel is untouched","black swan","Low-Medium","Severe",
   "Palisades Fire: 23,448 acres, 6,845 structures destroyed, 12 deaths (Jan 2025). Second-order effects: insurance repricing, utility cost, tourism.",
   "Parcel-level FHSZ lookup; defensible-space and roof class review; insurance adequacy test.",
   "CAL FIRE incident record; OSFM FHSZ.", "calfire"],
  ["RSK-13","Civil / social","Civil unrest, curfew or prolonged disruption in the trade area","black swan","Low","High",
   "Store closure during unrest produces zero sales while rent continues; uninsured loss possible.",
   "Verify business-interruption and civil-commotion cover; maintain tenant communication plan.",
   "None located for a forward-looking probability. Treated as judgement only.", "cdi"],
  ["RSK-14","Policy","New or expanded local transfer/“mansion” taxes or rent regulation","black swan","Low-Medium","Medium",
   "LA has already imposed a 4%/5.5% transfer tax. Further levies raise exit friction for the next buyer and lower bids today.",
   "Model a +2% adverse exit-cost sensitivity; retain timing flexibility.",
   "City of Los Angeles ordinance record.", "ula"],
  ["RSK-15","Concentration","Wealth concentrated in one parcel, one tenant, one seismic zone","business-as-usual","High","High",
   "A single-asset, single-tenant position has no diversification: one vacancy or one event dominates the owner's net worth.",
   "Set a maximum share of net worth in this asset; plan a 1031 or DST diversification on exit.",
   "Portfolio construction judgement, not data.", "fred"],
  ["RSK-16","Data","Decision made on incomplete property data (lease, APN, insurance)","business-as-usual","High","Medium",
   "Fifteen property-level fields are unverified in this build. Every valuation line inherits that uncertainty.",
   "Close the U-01 to U-11 information gaps before signing anything.",
   "Flagged for Review page.", "sec10K"],
].map(([id, category, event, type, probability, impact, exposure, mitigation, indicator, srcKey]) => ({
  id, category, event, type, probability, impact, exposure, mitigation, indicator,
  basis: SRC[srcKey], basis_url: U[srcKey],
  probability_basis: "Analyst assessment — not a sourced statistical probability",
}));

/* ---------------- MODEL SCENARIOS ---------------- */
const scenarios = {
  currency_note:
    "All values are expressed as a multiple of ONE YEAR of current base rent (R0 = 1.00). No property-specific dollar amount is invented. Multiply any output by the actual annual base rent to obtain dollars.",
  inputs_placeholder: {
    annual_base_rent: "[WITHHELD] — set R0 = 1.00 as the unit of account",
    expiry_year: "2030-2035 (use 2032.5 midpoint for modelling)",
    discount_rate_anchor: { value: 4.90, source: "FRED DGS10, 2026-11-04", url: U.fred },
  },
  assumptions: [
    ["discount_rate", 7.90, "%", "10-yr Treasury 4.90% (verified) + 3.00% illiquidity/equity premium (assumption)."],
    ["rent_escalation", 2.00, "%/yr", "Fixed NNN bumps typical of QSR leases; below LA CPI of 3.7%."],
    ["years_to_expiry_midpoint", 6.0, "years", "Midpoint of the owner-stated 2030-2035 window measured from 2026."],
    ["exit_cap_rate_renewed", 6.00, "%", "Assumption: credit-tenant QSR NNN pricing. Not an official statistic (U-06)."],
    ["exit_cap_rate_short_term", 7.00, "%", "Assumption: 100 bp penalty for <3 years remaining term / renewal uncertainty."],
    ["sale_cost_pct", 6.00, "% of price", "Measure ULA 4.0% (verified, if >$5m) + ~1.0% transfer/title + ~1.0% advisory."],
    ["renewal_probability", 0.55, "probability", "Assumption informed by tenant trajectory (5 negative indicators), not a published statistic."],
    ["dark_value_multiple", 8.0, "x annual rent", "Assumption: vacant/alternative-use land+building value as a multiple of the current rent."],
    ["hold_opex_leakage", 0.5, "% of rent/yr", "Non-recoverable owner costs under NNN (legal, asset management, vacancy-period carry)."],
  ],
  strategies: [
    ["A","S ell now (2027) with the lease in place","Capitalise current rent at the renewed-asset cap, net of sale costs, then redeploy proceeds."],
    ["B","Hold to expiry (2032-2035), then renew if the tenant will, else lease or sell vacant","Collect contractual rent to expiry, then bear renewal or vacancy risk."],
    ["C","Renew early (2028-2029) on a reset rent, then sell in 2031-2032 with long term remaining","Trade near-term rent for term certainty and a tighter exit cap."],
  ],
};
scenarios.strategies[0][1] = "Sell now (2027) with the lease in place";

mkdirSync("data", { recursive: true });
writeFileSync("data/records.json", JSON.stringify({
  generated_by: "scripts/build-data.mjs",
  generated_on: "2026-11-06",
  methodology: "Every row is a single sourced metric. status=verified means the value was read on the cited official page during this session. status=derived means arithmetic on two verified values. status=unverified means the value is deliberately blank. status=placeholder means private property data withheld by design.",
  categories: [...new Set(records.map(r => r.category))],
  sources: Object.entries(U).map(([k, url]) => ({ key: k, name: SRC[k] || k, url })),
  records,
}, null, 2));

writeFileSync("data/risks.json", JSON.stringify({
  generated_by: "scripts/build-data.mjs",
  note: "Probability and impact columns are analyst assessments, not sourced statistics. The basis column links the factual anchor for each risk.",
  risks,
}, null, 2));

writeFileSync("data/scenarios.json", JSON.stringify(scenarios, null, 2));

console.log(`records: ${records.length}`);
console.log(`verified: ${records.filter(r=>r.status==="verified").length}`);
console.log(`derived:  ${records.filter(r=>r.status==="derived").length}`);
console.log(`unverified: ${records.filter(r=>r.status==="unverified").length}`);
console.log(`placeholder: ${records.filter(r=>r.status==="placeholder").length}`);
console.log(`risks: ${risks.length}`);
