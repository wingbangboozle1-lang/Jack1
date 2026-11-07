"""Single source of truth for the Jack in the Box property decision brief.

Every value in ROWS was read from the official page named in its `src`
field during this session (2026-11-07).  Values that could not be read
from an official source are blank ("") and carry status "unverified" or
"withheld"; they are published on the Flagged for Review page.

Status vocabulary
  verified  - value read directly from the official source page today
  derived   - arithmetic on verified values; formula stated in `note`
  unverified- not confirmed from an official source; value left blank
  withheld  - exists but intentionally not published (privacy policy)
"""

ACCESSION_DATE = "2026-11-07"

SOURCES = {
    "CEN-CITY": {
        "title": "QuickFacts: Los Angeles city, California (Population estimates V2025; ACS 2020-2024)",
        "publisher": "U.S. Census Bureau",
        "url": "https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225",
        "as_of": "V2025 estimates / ACS 2020-2024",
    },
    "CEN-COUNTY": {
        "title": "QuickFacts: Los Angeles County, California (Population estimates V2025; ACS 2020-2024)",
        "publisher": "U.S. Census Bureau",
        "url": "https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045225",
        "as_of": "V2025 estimates / ACS 2020-2024",
    },
    "BLS-EAG": {
        "title": "Economy at a Glance: Los Angeles-Long Beach-Santa Ana, CA (MSA)",
        "publisher": "U.S. Bureau of Labor Statistics",
        "url": "https://www.bls.gov/eag/eag.ca_losangeles_msa.htm",
        "as_of": "September 2026 preliminary",
    },
    "BLS-CPI": {
        "title": "Consumer Price Index, Los Angeles area - September 2026 (26-1595-SAN)",
        "publisher": "U.S. Bureau of Labor Statistics, Western Information Office",
        "url": "https://www.bls.gov/regions/west/news-release/consumerpriceindex_losangeles.htm",
        "as_of": "September 2026, released 2026-10-14",
    },
    "FRED-DGS10": {
        "title": "10-Year Treasury Constant Maturity Rate (DGS10), H.15 Selected Interest Rates",
        "publisher": "Board of Governors of the Federal Reserve System via FRED",
        "url": "https://fred.stlouisfed.org/series/DGS10",
        "as_of": "2026-11-05 observation",
    },
    "SEC-Q4": {
        "title": "Form 8-K, Exhibit 99.1: Jack in the Box Inc. Reports Fourth Quarter and Full-Year 2025 Earnings",
        "publisher": "U.S. Securities and Exchange Commission (EDGAR, CIK 0000807882)",
        "url": "https://www.sec.gov/Archives/edgar/data/807882/000080788225000070/ex991-q425earningsrelease.htm",
        "as_of": "Fiscal year ended 2025-09-28; released 2025-11-19",
    },
    "LA-ULA": {
        "title": "Real Property Transfer Tax and Measure ULA FAQ",
        "publisher": "City of Los Angeles Office of Finance",
        "url": "https://finance.lacity.gov/faq/measure-ula",
        "as_of": "Threshold note effective for closings after 2026-06-30",
    },
    "LACO-ASSESSOR": {
        "title": "Decline-in-Value (Proposition 13 base-year value; Proposition 8 temporary relief)",
        "publisher": "Los Angeles County Office of the Assessor",
        "url": "https://assessor.lacounty.gov/tax-relief/decline-in-value",
        "as_of": "2026 filing cycle",
    },
    "DIR-FF": {
        "title": "Fast Food Council - AB 1228 fast food minimum wage",
        "publisher": "California Department of Industrial Relations",
        "url": "https://www.dir.ca.gov/AB1228/AB1228.html",
        "as_of": "Effective 2024-04-01",
    },
    "CALFIRE-PAL": {
        "title": "Palisades Fire incident page (Los Angeles County, January 2025)",
        "publisher": "CAL FIRE / California Department of Forestry and Fire Protection",
        "url": "https://www.fire.ca.gov/incidents/2025/1/7/palisades-fire/",
        "as_of": "Last updated 2026-04-09",
    },
    "OSFM-FHSZ": {
        "title": "Fire Hazard Severity Zones (SRA effective 2024-04-01; 2025 LRA rollout)",
        "publisher": "CAL FIRE - Office of the State Fire Marshal",
        "url": "https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones",
        "as_of": "2026 map update cycle",
    },
    "CGS-AP": {
        "title": "Alquist-Priolo Earthquake Fault Zones",
        "publisher": "California Geological Survey, Department of Conservation",
        "url": "https://www.conservation.ca.gov/cgs/alquist-priolo",
        "as_of": "Current",
    },
    "USGS-SHAKEOUT": {
        "title": "The ShakeOut scenario: a hypothetical Mw 7.8 earthquake on the southern San Andreas Fault",
        "publisher": "U.S. Geological Survey (Earthquake Spectra, 2011)",
        "url": "https://www.usgs.gov/publications/shakeout-scenario-a-hypothetical-mw78-earthquake-southern-san-andreas-fault",
        "as_of": "2011 publication (scenario, not a forecast)",
    },
    "NCES-LAUSD": {
        "title": "District Directory Information: Los Angeles Unified (NCES District ID 0622710)",
        "publisher": "National Center for Education Statistics, Common Core of Data",
        "url": "https://nces.ed.gov/ccd/districtsearch/district_detail.asp?ID2=0622710",
        "as_of": "2024-25 school year; fiscal data 2022-23",
    },
    "IRS-1031": {
        "title": "Like-Kind Exchanges Under IRC Section 1031 (FS-2008-18)",
        "publisher": "Internal Revenue Service",
        "url": "https://www.irs.gov/newsroom/like-kind-exchanges-under-irc-code-section-1031",
        "as_of": "IRS fact sheet (rules as described by IRS)",
    },
    "DOF-PROJ": {
        "title": "Population Projections (Baseline 2024), P-2 county projections",
        "publisher": "California Department of Finance, Demographic Research Unit",
        "url": "https://dof.ca.gov/forecasting/demographics/projections/",
        "as_of": "Baseline 2024 release; 2026-03-13 note",
    },
    "LA-ZIMAS": {
        "title": "Zoning Search / Property Information (ZIMAS)",
        "publisher": "City of Los Angeles Department of City Planning",
        "url": "https://planning.lacity.gov/zoning",
        "as_of": "Live lookup tool",
    },
    "LACO-ASSESSOR-HOME": {
        "title": "Los Angeles County Office of the Assessor (parcel and value lookup)",
        "publisher": "Los Angeles County Office of the Assessor",
        "url": "https://assessor.lacounty.gov/",
        "as_of": "Live lookup tool",
    },
    "CSC-DASH": {
        "title": "California School Dashboard (district and school performance reports)",
        "publisher": "California Department of Education",
        "url": "https://www.caschooldashboard.org/",
        "as_of": "Live lookup tool",
    },
}

# --------------------------------------------------------------------------
# Table rows
# --------------------------------------------------------------------------

ROWS = []


def add(id, metric, value, period, geo, status, src, note="", unit=""):
    ROWS.append(
        {
            "id": id,
            "metric": metric,
            "value": value,
            "unit": unit,
            "period": period,
            "geo": geo,
            "status": status,
            "src": src,
            "note": note,
        }
    )


# --- Demographics ---------------------------------------------------------
add("DEM-01", "Population", "3,869,089", "July 1, 2025 estimate (V2025)", "Los Angeles city", "verified", "CEN-CITY")
add("DEM-02", "Population", "9,694,934", "July 1, 2025 estimate (V2025)", "Los Angeles County", "verified", "CEN-COUNTY")
add("DEM-03", "Population change since the 2020 estimate base", "-0.8%", "Apr 1, 2020 to Jul 1, 2025", "Los Angeles city", "verified", "CEN-CITY")
add("DEM-04", "Population change since the 2020 estimate base", "-3.2%", "Apr 1, 2020 to Jul 1, 2025", "Los Angeles County", "verified", "CEN-COUNTY")
add("DEM-05", "Annualised population change", "-0.15% per year", "Apr 1, 2020 to Jul 1, 2025", "Los Angeles city", "derived", "CEN-CITY",
    "Formula: (1 - 0.008)^(1/5.25) - 1, using the city change in DEM-03 over 5.25 years. Arithmetic only.")
add("DEM-06", "Annualised population change", "-0.62% per year", "Apr 1, 2020 to Jul 1, 2025", "Los Angeles County", "derived", "CEN-COUNTY",
    "Formula: (1 - 0.032)^(1/5.25) - 1, using the county change in DEM-04. Arithmetic only.")
add("DEM-07", "Households", "1,439,097", "2020-2024 ACS", "Los Angeles city", "verified", "CEN-CITY")
add("DEM-08", "Persons per household", "2.61", "2020-2024 ACS", "Los Angeles city", "verified", "CEN-CITY")
add("DEM-09", "Households", "3,416,449", "2020-2024 ACS", "Los Angeles County", "verified", "CEN-COUNTY")
add("DEM-10", "Population density", "8,304.2 per sq mi", "2020 Census", "Los Angeles city", "verified", "CEN-CITY")
add("DEM-11", "Population density", "2,466.9 per sq mi", "2020 Census", "Los Angeles County", "verified", "CEN-COUNTY")
add("DEM-12", "Foreign-born residents", "35.7%", "2020-2024 ACS", "Los Angeles city", "verified", "CEN-CITY")
add("DEM-13", "Language other than English spoken at home", "56.4%", "2020-2024 ACS", "Los Angeles city", "verified", "CEN-CITY")
add("DEM-14", "Residents aged 65 and over", "14.2%", "July 1, 2025 estimate", "Los Angeles city", "verified", "CEN-CITY")
add("DEM-15", "Residents aged 65 and over", "17.1%", "July 1, 2025 estimate", "Los Angeles County", "verified", "CEN-COUNTY")
add("DEM-16", "Population inside a three-mile trade area", "", "Not determinable", "Subject site", "unverified", "CEN-CITY",
    "Requires the parcel location. Census QuickFacts publishes city and county totals only.")
add("DEM-17", "Households earning the income band of a typical quick-service customer", "", "Not determinable", "Subject site", "unverified", "CEN-CITY",
    "No official geocoded income ring was produced; no value is inferred.")

# --- Income, poverty, housing --------------------------------------------
add("INC-01", "Median household income (2024 dollars)", "$81,939", "2020-2024 ACS", "Los Angeles city", "verified", "CEN-CITY")
add("INC-02", "Median household income (2024 dollars)", "$90,112", "2020-2024 ACS", "Los Angeles County", "verified", "CEN-COUNTY")
add("INC-03", "Per capita income (2024 dollars)", "$47,685", "2020-2024 ACS", "Los Angeles city", "verified", "CEN-CITY")
add("INC-04", "Per capita income (2024 dollars)", "$45,792", "2020-2024 ACS", "Los Angeles County", "verified", "CEN-COUNTY")
add("INC-05", "Residents below the poverty line", "16.5%", "2025 estimate", "Los Angeles city", "verified", "CEN-CITY")
add("INC-06", "Residents below the poverty line", "13.3%", "2025 estimate", "Los Angeles County", "verified", "CEN-COUNTY")
add("INC-07", "Uninsured residents under 65", "10.7%", "2020-2024 ACS", "Los Angeles city", "verified", "CEN-CITY")
add("INC-08", "Uninsured residents under 65", "8.3%", "2020-2024 ACS", "Los Angeles County", "verified", "CEN-COUNTY")
add("INC-09", "Civilian labour force participation, age 16+", "66.4%", "2020-2024 ACS", "Los Angeles city", "verified", "CEN-CITY")
add("INC-10", "High school graduate or higher, age 25+", "79.6%", "2020-2024 ACS", "Los Angeles city", "verified", "CEN-CITY")
add("INC-11", "Bachelor's degree or higher, age 25+", "38.5%", "2020-2024 ACS", "Los Angeles city", "verified", "CEN-CITY")
add("INC-12", "Bachelor's degree or higher, age 25+", "36.0%", "2020-2024 ACS", "Los Angeles County", "verified", "CEN-COUNTY")
add("HOU-01", "Median value, owner-occupied housing units", "$921,200", "2020-2024 ACS", "Los Angeles city", "verified", "CEN-CITY")
add("HOU-02", "Median value, owner-occupied housing units", "$834,200", "2020-2024 ACS", "Los Angeles County", "verified", "CEN-COUNTY")
add("HOU-03", "Median gross rent", "$1,933 per month", "2020-2024 ACS", "Los Angeles city", "verified", "CEN-CITY")
add("HOU-04", "Median gross rent", "$1,954 per month", "2020-2024 ACS", "Los Angeles County", "verified", "CEN-COUNTY")
add("HOU-05", "Owner-occupied housing unit rate", "36.0%", "2020-2024 ACS", "Los Angeles city", "verified", "CEN-CITY")
add("HOU-06", "Owner-occupied housing unit rate", "45.9%", "2020-2024 ACS", "Los Angeles County", "verified", "CEN-COUNTY")
add("HOU-07", "Housing units", "3,726,923", "July 1, 2025 estimate", "Los Angeles County", "verified", "CEN-COUNTY")
add("HOU-08", "Building permits issued", "22,250", "2025", "Los Angeles County", "verified", "CEN-COUNTY")
add("HOU-09", "Mean travel time to work", "30.7 minutes", "2020-2024 ACS", "Los Angeles city", "verified", "CEN-CITY")
add("HOU-10", "Commercial rent for this property", "", "Not determinable", "Subject site", "unverified", "LACO-ASSESSOR-HOME",
    "Requires the executed lease or independent rent comps. No official series covers a single net-leased parcel.")

# --- Economy and jobs -----------------------------------------------------
add("ECO-01", "Unemployment rate", "4.4%", "September 2026 (preliminary)", "Los Angeles-Long Beach-Santa Ana MSA", "verified", "BLS-EAG")
add("ECO-02", "Civilian labour force", "6,646.9 thousand", "September 2026 (preliminary)", "Los Angeles-Long Beach-Santa Ana MSA", "verified", "BLS-EAG")
add("ECO-03", "Employment (household survey)", "6,352.9 thousand", "September 2026 (preliminary)", "Los Angeles-Long Beach-Santa Ana MSA", "verified", "BLS-EAG")
add("ECO-04", "Unemployed", "294.0 thousand", "September 2026 (preliminary)", "Los Angeles-Long Beach-Santa Ana MSA", "verified", "BLS-EAG")
add("ECO-05", "Total nonfarm employment", "6,282.1 thousand", "September 2026 (preliminary)", "Los Angeles-Long Beach-Santa Ana MSA", "verified", "BLS-EAG")
add("ECO-06", "Total nonfarm employment, 12-month change", "+0.5%", "12 months to September 2026", "Los Angeles-Long Beach-Santa Ana MSA", "verified", "BLS-EAG")
add("ECO-07", "Education and health services, 12-month change", "+3.8%", "12 months to September 2026", "Los Angeles-Long Beach-Santa Ana MSA", "verified", "BLS-EAG")
add("ECO-08", "Trade, transportation and utilities, 12-month change", "+0.3%", "12 months to September 2026", "Los Angeles-Long Beach-Santa Ana MSA", "verified", "BLS-EAG")
add("ECO-09", "Construction, 12-month change", "0.0%", "12 months to September 2026", "Los Angeles-Long Beach-Santa Ana MSA", "verified", "BLS-EAG")
add("ECO-10", "Professional and business services, 12-month change", "-0.5%", "12 months to September 2026", "Los Angeles-Long Beach-Santa Ana MSA", "verified", "BLS-EAG")
add("ECO-11", "Manufacturing, 12-month change", "-1.2%", "12 months to September 2026", "Los Angeles-Long Beach-Santa Ana MSA", "verified", "BLS-EAG")
add("ECO-12", "Financial activities, 12-month change", "-1.7%", "12 months to September 2026", "Los Angeles-Long Beach-Santa Ana MSA", "verified", "BLS-EAG")
add("ECO-13", "Information sector, 12-month change", "-5.7%", "12 months to September 2026", "Los Angeles-Long Beach-Santa Ana MSA", "verified", "BLS-EAG")
add("ECO-14", "Accommodation and food services sales", "$17.37 billion", "2022 Economic Census", "Los Angeles city", "verified", "CEN-CITY")
add("ECO-15", "Accommodation and food services sales", "$44.00 billion", "2022 Economic Census", "Los Angeles County", "verified", "CEN-COUNTY")
add("ECO-16", "Retail sales, all categories", "$81.35 billion", "2022 Economic Census", "Los Angeles city", "verified", "CEN-CITY")
add("ECO-17", "Retail sales, all categories", "$213.93 billion", "2022 Economic Census", "Los Angeles County", "verified", "CEN-COUNTY")
add("ECO-18", "Retail sales per capita", "$21,281", "2022 Economic Census", "Los Angeles city", "verified", "CEN-CITY")
add("ECO-19", "Employer establishments", "304,988", "2023", "Los Angeles County", "verified", "CEN-COUNTY")
add("ECO-20", "Total employment (establishment basis)", "3,987,736", "2023", "Los Angeles County", "verified", "CEN-COUNTY")
add("ECO-21", "Total employment, 2022-2023 change", "+2.3%", "2022 to 2023", "Los Angeles County", "verified", "CEN-COUNTY")
add("ECO-22", "Unemployment rate", "", "Latest county figure", "Los Angeles County", "unverified", "BLS-EAG",
    "The BLS page read covers the metropolitan statistical area, not the county. No county rate is published here.")
add("ECO-23", "Employment within three miles of the site", "", "Not determinable", "Subject site", "unverified", "BLS-EAG",
    "Requires geocoded parcel data. MSA figures are not a trade-area measure.")

# --- Prices and cost of capital ------------------------------------------
add("PRI-01", "CPI-U, all items, 12-month change", "3.7%", "September 2026", "Los Angeles-Long Beach-Anaheim, CA", "verified", "BLS-CPI")
add("PRI-02", "CPI-U, all items less food and energy, 12-month change", "2.6%", "September 2026", "Los Angeles-Long Beach-Anaheim, CA", "verified", "BLS-CPI")
add("PRI-03", "Food, 12-month change", "2.8%", "September 2026", "Los Angeles-Long Beach-Anaheim, CA", "verified", "BLS-CPI")
add("PRI-04", "Food away from home, 12-month change", "2.8%", "September 2026", "Los Angeles-Long Beach-Anaheim, CA", "verified", "BLS-CPI")
add("PRI-05", "Shelter, 12-month change", "3.7%", "September 2026", "Los Angeles-Long Beach-Anaheim, CA", "verified", "BLS-CPI")
add("PRI-06", "Energy, 12-month change", "20.3%", "September 2026", "Los Angeles-Long Beach-Anaheim, CA", "verified", "BLS-CPI")
add("PRI-07", "Gasoline, 12-month change", "30.8%", "September 2026", "Los Angeles-Long Beach-Anaheim, CA", "verified", "BLS-CPI")
add("CAP-01", "10-year Treasury constant maturity yield", "4.84%", "2026-11-05", "United States", "verified", "FRED-DGS10")
add("CAP-02", "Capitalisation rate applicable to this asset", "", "Not determinable", "Subject site", "unverified", "FRED-DGS10",
    "No official series publishes net-lease cap rates for a single quick-service parcel. Treasury yield is context only, not a cap rate.")

# --- Schools --------------------------------------------------------------
add("SCH-01", "Public school district serving central Los Angeles", "Los Angeles Unified (NCES ID 0622710)", "2025-26 directory", "Los Angeles city", "verified", "NCES-LAUSD")
add("SCH-02", "Schools in the district", "784", "2025-26 directory", "Los Angeles Unified", "verified", "NCES-LAUSD")
add("SCH-03", "Students enrolled", "408,026", "2024-25", "Los Angeles Unified", "verified", "NCES-LAUSD")
add("SCH-04", "Classroom teachers (FTE)", "21,246.18", "2024-25", "Los Angeles Unified", "verified", "NCES-LAUSD")
add("SCH-05", "Student / teacher ratio", "19.20", "2024-25", "Los Angeles Unified", "verified", "NCES-LAUSD")
add("SCH-06", "Total revenue", "$14,773,154,000 ($34,533 per student)", "Fiscal 2022-23", "Los Angeles Unified", "verified", "NCES-LAUSD")
add("SCH-07", "Total current expenditures per student", "$22,606", "Fiscal 2022-23", "Los Angeles Unified", "verified", "NCES-LAUSD")
add("SCH-08", "District locale", "City, Large (11)", "2024-25", "Los Angeles Unified", "verified", "NCES-LAUSD")
add("SCH-09", "School assigned to this parcel", "", "Not determinable", "Subject site", "unverified", "CSC-DASH",
    "Requires the street address; assignment boundaries are address-specific.")
add("SCH-10", "District academic performance indicators", "", "Not reviewed", "Los Angeles Unified", "unverified", "CSC-DASH",
    "The California School Dashboard district report was not opened in this session, so no performance number is published.")

# --- Tenant (issuer-level, anonymised subject) ----------------------------
add("TEN-01", "Restaurants at fiscal year end (Jack in the Box brand)", "2,136 (150 company-operated, 1,986 franchise)", "September 28, 2025", "National system", "verified", "SEC-Q4")
add("TEN-02", "Restaurant openings, fiscal 2025", "31", "Fiscal 2025", "National system", "verified", "SEC-Q4")
add("TEN-03", "Restaurant closures, fiscal 2025", "86", "Fiscal 2025", "National system", "verified", "SEC-Q4")
add("TEN-04", "Same-store sales, fourth quarter", "-7.4% (company -5.3%, franchise -7.6%)", "Q4 fiscal 2025", "National system", "verified", "SEC-Q4")
add("TEN-05", "Same-store sales, full year", "-4.2%", "Fiscal 2025", "National system", "verified", "SEC-Q4")
add("TEN-06", "Systemwide sales change, fourth quarter", "-7.2%", "Q4 fiscal 2025", "National system", "verified", "SEC-Q4")
add("TEN-07", "Total revenues, fourth quarter", "$326.2 million (-6.6% year over year)", "Q4 fiscal 2025", "Jack in the Box Inc.", "verified", "SEC-Q4")
add("TEN-08", "Adjusted EBITDA, fourth quarter", "$45.6 million (prior-year quarter $65.5 million)", "Q4 fiscal 2025", "Jack in the Box Inc.", "verified", "SEC-Q4")
add("TEN-09", "Net earnings, fourth quarter", "$5.8 million; diluted EPS $0.30", "Q4 fiscal 2025", "Jack in the Box Inc.", "verified", "SEC-Q4")
add("TEN-10", "Dividend", "Discontinued", "Fiscal 2025", "Jack in the Box Inc.", "verified", "SEC-Q4")
add("TEN-11", "Guidance: restaurant count", "2,050 to 2,100", "Fiscal 2026 guidance", "Jack in the Box brand", "verified", "SEC-Q4")
add("TEN-12", "Guidance: same-store sales", "-1% to +1%", "Fiscal 2026 guidance", "Jack in the Box brand", "verified", "SEC-Q4")
add("TEN-13", "Guidance: Adjusted EBITDA", "$225 million to $240 million", "Fiscal 2026 guidance", "Jack in the Box brand", "verified", "SEC-Q4")
add("TEN-14", "Guidance: franchise-level margin", "$275 million to $290 million", "Fiscal 2026 guidance", "Jack in the Box brand", "verified", "SEC-Q4")
add("TEN-15", "Guidance: capital expenditures", "$45 million to $55 million", "Fiscal 2026 guidance", "Jack in the Box brand", "verified", "SEC-Q4")
add("TEN-16", "Guidance: company-operated restaurant-level margin", "17% to 18%", "Fiscal 2026 guidance", "Jack in the Box brand", "verified", "SEC-Q4")
add("TEN-17", "Del Taco segment treatment", "Reflected in discontinued operations in fiscal 2026 following its sale", "Fiscal 2026 guidance basis", "Jack in the Box Inc.", "verified", "SEC-Q4")
add("TEN-18", "Operator of the subject unit (company or franchisee)", "", "Not determinable", "Subject property", "unverified", "SEC-Q4",
    "Issuer filings do not identify individual locations or franchisees.")
add("TEN-19", "Guarantor and guaranty scope on the subject lease", "", "Not determinable", "Subject property", "withheld", "SEC-Q4")
add("TEN-20", "Issuer credit rating", "", "Not reviewed", "Jack in the Box Inc.", "unverified", "SEC-Q4",
    "The earnings release does not state a rating; no rating-agency page was opened in this session.")

# --- Property and lease ---------------------------------------------------
add("PRP-01", "Street address", "", "Privacy policy", "Subject property", "withheld", "LA-ZIMAS")
add("PRP-02", "Assessor parcel number (APN)", "", "Privacy policy", "Subject property", "withheld", "LACO-ASSESSOR-HOME")
add("PRP-03", "Fee owner / title vesting", "", "Privacy policy", "Subject property", "withheld", "LACO-ASSESSOR-HOME")
add("PRP-04", "Lease commencement date", "", "Owner file", "Subject property", "withheld", "LACO-ASSESSOR-HOME")
add("PRP-05", "Lease expiry window (as described by the owner)", "", "Owner-stated window: 2030-2035; contract not reviewed", "Subject property", "unverified", "LACO-ASSESSOR-HOME",
    "Reported by the owner. The executed lease, amendments and any extension were not available for review in this session.")
add("PRP-06", "Remaining firm term in years", "", "Not determinable", "Subject property", "unverified", "LACO-ASSESSOR-HOME")
add("PRP-07", "Current annual base rent", "", "Privacy policy", "Subject property", "withheld", "LACO-ASSESSOR-HOME")
add("PRP-08", "Rent escalation schedule", "", "Lease not reviewed", "Subject property", "unverified", "LACO-ASSESSOR-HOME")
add("PRP-09", "Renewal / extension options held by the tenant", "", "Lease not reviewed", "Subject property", "unverified", "LACO-ASSESSOR-HOME")
add("PRP-10", "Lease structure", "", "Owner-stated triple net (NNN); contract not reviewed", "Subject property", "unverified", "LACO-ASSESSOR-HOME",
    "NNN is not treated as proof that every operating and capital item is reimbursed.")
add("PRP-11", "Building area", "", "Not determinable", "Subject property", "unverified", "LACO-ASSESSOR-HOME")
add("PRP-12", "Land area", "", "Not determinable", "Subject property", "unverified", "LACO-ASSESSOR-HOME")
add("PRP-13", "Year built", "", "Not determinable", "Subject property", "unverified", "LACO-ASSESSOR-HOME")
add("PRP-14", "Zoning / community plan designation", "", "Parcel not matched", "Subject property", "unverified", "LA-ZIMAS",
    "ZIMAS requires an address or parcel number that is deliberately not published.")
add("PRP-15", "Assessed value (Proposition 13 base)", "", "Privacy policy", "Subject property", "withheld", "LACO-ASSESSOR-HOME")
add("PRP-16", "Existing debt, loan payoff and prepayment terms", "", "Privacy policy", "Subject property", "withheld", "LACO-ASSESSOR-HOME")
add("PRP-17", "Insurance premium, deductible and exclusions", "", "Policy not reviewed", "Subject property", "unverified", "LACO-ASSESSOR-HOME")
add("PRP-18", "Environmental reports (Phase I / II)", "", "Not reviewed", "Subject property", "unverified", "LACO-ASSESSOR-HOME")
add("PRP-19", "Property condition / roof and structural survey", "", "Not reviewed", "Subject property", "unverified", "LACO-ASSESSOR-HOME")

# --- Transfer tax and regulation -----------------------------------------
add("REG-01", "City of Los Angeles base real property transfer tax", "0.45% ($2.25 per $500 of value)", "In force", "Los Angeles city", "verified", "LA-ULA")
add("REG-02", "Measure ULA surcharge, sales above $5,400,000 and below $10,900,000", "4.0%", "Closings after June 30, 2026", "Los Angeles city", "verified", "LA-ULA")
add("REG-03", "Measure ULA surcharge, sales of $10,900,000 or more", "5.5%", "Closings after June 30, 2026", "Los Angeles city", "verified", "LA-ULA")
add("REG-04", "Combined city transfer tax rate, upper tier", "5.95% (0.45% base + 5.5% ULA)", "Closings after June 30, 2026", "Los Angeles city", "verified", "LA-ULA")
add("REG-05", "ULA threshold indexation basis", "Chained Consumer Price Index, adjusted annually", "In force", "Los Angeles city", "verified", "LA-ULA")
add("REG-06", "Proposition 13 cap on assessed value growth", "2.0% per year", "In force", "Los Angeles County", "verified", "LACO-ASSESSOR")
add("REG-07", "Proposition 8 decline-in-value relief", "Temporary reduction; file application RP-87 between July 2 and November 30", "Annual cycle", "Los Angeles County", "verified", "LACO-ASSESSOR")
add("REG-08", "California fast-food minimum wage", "$20.00 per hour", "From April 1, 2024 (AB 1228)", "California", "verified", "DIR-FF")
add("REG-09", "Section 1031 like-kind exchange deadlines", "45 days to identify; 180 days to close", "In force", "United States", "verified", "IRS-1031")
add("REG-10", "City of Los Angeles general minimum wage", "", "2026 rate", "Los Angeles city", "unverified", "DIR-FF",
    "The fast-food rate is verified; the separate citywide rate was not opened on an official page in this session.")
add("REG-11", "Los Angeles County documentary transfer tax", "", "Current rate", "Los Angeles County", "unverified", "LACO-ASSESSOR-HOME")
add("REG-12", "Property tax rate applying to this parcel", "", "Not determinable", "Subject property", "unverified", "LACO-ASSESSOR-HOME")

# --- Hazard and catastrophe ----------------------------------------------
add("CAT-01", "Palisades Fire - area burned", "23,448 acres", "January 2025", "Los Angeles County", "verified", "CALFIRE-PAL")
add("CAT-02", "Palisades Fire - structures destroyed", "6,845", "January 2025", "Los Angeles County", "verified", "CALFIRE-PAL")
add("CAT-03", "Palisades Fire - structures damaged", "975", "January 2025", "Los Angeles County", "verified", "CALFIRE-PAL")
add("CAT-04", "Palisades Fire - confirmed civilian fatalities", "12 (plus 3 civilian injuries, 1 firefighter injury)", "January 2025", "Los Angeles County", "verified", "CALFIRE-PAL")
add("CAT-05", "Palisades Fire - containment and cause", "Contained 2025-01-31 after 24 days; cause recorded as arson", "January 2025", "Los Angeles County", "verified", "CALFIRE-PAL")
add("CAT-06", "Fire Hazard Severity Zone classes (State Responsibility Area)", "Moderate, High, Very High", "Maps effective 2024-04-01", "California", "verified", "OSFM-FHSZ")
add("CAT-07", "Local Responsibility Area Fire Hazard Severity Zone mapping", "Delivered to all counties during 2025; jurisdiction-specific", "2025 rollout", "California", "verified", "OSFM-FHSZ")
add("CAT-08", "Fire Hazard Severity Zone for this parcel", "", "Parcel not matched", "Subject property", "unverified", "OSFM-FHSZ",
    "The FHSZ viewer requires an address; no zone is assigned to this asset.")
add("CAT-09", "Alquist-Priolo fault-rupture setback", "Structures for human occupancy may not be placed over an active fault and generally must be at least 50 feet from it", "In force", "California", "verified", "CGS-AP")
add("CAT-10", "Definition of an active fault under the Alquist-Priolo Act", "A fault that has ruptured in the last 11,000 years", "In force", "California", "verified", "CGS-AP")
add("CAT-11", "Alquist-Priolo earthquake fault zone status of this parcel", "", "Parcel not matched", "Subject property", "unverified", "CGS-AP")
add("CAT-12", "Seismic hazard zone (liquefaction / landslide) status of this parcel", "", "Parcel not matched", "Subject property", "unverified", "CGS-AP")
add("CAT-13", "ShakeOut Mw 7.8 scenario - modelled deaths", "1,800 (plus 53,000 injuries requiring emergency care)", "Hypothetical scenario", "Southern California", "verified", "USGS-SHAKEOUT")
add("CAT-14", "ShakeOut Mw 7.8 scenario - modelled economic loss", "$191 billion total (fire $87 billion, shake damage $46 billion, water-outage business interruption $24 billion)", "Hypothetical scenario", "Southern California", "verified", "USGS-SHAKEOUT")
add("CAT-15", "ShakeOut Mw 7.8 scenario - fires ignited", "About 1,600 fires; 200 million sq ft of building stock destroyed", "Hypothetical scenario", "Southern California", "verified", "USGS-SHAKEOUT")
add("CAT-16", "Flood zone designation for this parcel", "", "Parcel not matched", "Subject property", "unverified", "LACO-ASSESSOR-HOME")
add("CAT-17", "Wildfire or earthquake insurance availability at this parcel", "", "Policy not reviewed", "Subject property", "unverified", "LACO-ASSESSOR-HOME")
add("CAT-18", "Business-interruption cover and lease allocation", "", "Lease and policy not reviewed", "Subject property", "unverified", "LACO-ASSESSOR-HOME")

# --- Regional outlook -----------------------------------------------------
add("POP-01", "Official county population projection to 2030", "", "Baseline 2024 series", "Los Angeles County", "unverified", "DOF-PROJ",
    "The Department of Finance publishes P-2 projections as an Excel workbook that could not be read in this environment. Values are withheld rather than copied from secondary sources.")
add("POP-02", "Official county population projection to 2035", "", "Baseline 2024 series", "Los Angeles County", "unverified", "DOF-PROJ",
    "Same limitation as POP-01.")
add("POP-03", "Mechanical trend projection of county population, 2035", "9,112,568 (about)", "2025 to 2035, mechanical", "Los Angeles County", "derived", "CEN-COUNTY",
    "Formula: 9,694,934 x (1 - 0.00618)^10, continuing the annualised 2020-2025 change in DEM-06. A mechanical continuation, not an official forecast and not a site forecast.")
add("POP-04", "Mechanical trend projection of MSA nonfarm employment, 2035", "6,603,400 (about)", "2026 to 2035, mechanical", "Los Angeles-Long Beach-Santa Ana MSA", "derived", "BLS-EAG",
    "Formula: 6,282.1 thousand x (1 + 0.005)^10, extending the 12-month change in ECO-06. Mechanical continuation, not an official forecast.")

STATUS_LABEL = {
    "verified": "Verified",
    "derived": "Derived",
    "unverified": "Unverified",
    "withheld": "Withheld",
}


def rows_for(prefixes):
    return [r for r in ROWS if r["id"].split("-")[0] in prefixes]
