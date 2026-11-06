# Research log — tenant, tax/regulatory, catastrophe

Fetched and read 2026-11-06.

## T1. Tenant — Jack in the Box Inc. (NASDAQ: JACK), latest official results

Primary source: Form 8-K filed **2026-08-12**, Exhibit 99.1 earnings release for the
third quarter of fiscal 2026 ended **July 5, 2026**.
https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm

| Metric | Q3 FY2026 | Q3 FY2025 |
|---|---|---|
| System same-store sales | **−1.1%** | −7.1% |
| Franchise same-store sales | −1.2% | −7.2% |
| Company same-store sales | −0.9% | −6.4% |
| Systemwide sales change | −1.4% | — |
| Restaurant-level margin (company) | 17.6% | 17.9% |
| Franchise-level margin | $60.3M / 37.4% | $66.2M / 39.3% |
| Total revenues | $257.7M | $262.4M |
| Restaurant count, end of quarter | **2,115** (149 company + 1,966 franchise) | 2,168 |
| Openings / closures in quarter | 4 / **17** | 6 / 21 |
| Adjusted EBITDA | $61.2M | $57.1M |

Direct quotes that matter for a landlord:
* "The decrease [in franchise-level margin] was primarily due to lower sales driving lower
  rent and royalty revenue and a decrease in the number of restaurants as part of the
  **'JACK on Track' closure program**. **Bad debt expense was also higher** versus the
  prior year quarter."
* FY2026 guidance: restaurant count "approximately 2,100… approximately 25 new restaurant
  openings and approximately **50 to 60 closures, most of which will be franchise
  restaurants**."
* "'JACK on Track' plan, which includes a **block closure program and selling real
  estate**".
* The dividend and share repurchase programme have been discontinued.
* Del Taco was sold; the sale completed **2025-12-22** (discontinued operations).
* Refinancing completed in FY2026: $500M of 2026-1 Class A-2 Notes, anticipated repayment
  May 2031; 2019-1 Class A-2-II notes fully repaid.

**Interpretation (analysis, not fact):** the franchisor is shrinking its system, is
closing mostly franchisee units, and is explicitly harvesting real estate. A landlord
whose lease expires in 2030–2035 faces a tenant whose system is contracting, not
expanding. This is the single most important fact in the whole file: it argues *against*
assuming renewal happens automatically, and it argues *for* getting a renewal signed
before expiry, when the asset still has tenant demand.

**Not verified:** the share of JACK restaurants located in California, the specific
franchisee's financial condition, the franchisee's unit-level AUV, and the franchisee's
intent. All flagged.

## X1. Tax and transfer costs

### Measure ULA (City of Los Angeles) — official City page
https://finance.lacity.gov/faq/measure-ula (read 2026-11-06)

* City base real property transfer tax: **$2.25 per $500 = 0.45%**.
* ULA tax, effective for closings **after June 30, 2026**:
  * >$5,400,000 and <$10,900,000 → **4%** of the *whole* consideration (not marginal).
  * ≥$10,900,000 → **5.5%**.
* Thresholds are indexed annually to the BLS Chained CPI.
* ULA applies to **commercial** property as well as residential.
* Exemptions are limited to qualified affordable-housing transferees.

**Decision-relevant cliff:** a sale at $5,399,000 pays **$0** ULA; a sale at $5,400,001
pays **≈$216,000**. Nothing else in the file has that shape.

### County documentary transfer tax — official Recorder page
https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info

* County rate **$0.55 per $500 = 0.11%** of net value, rounded up to the next $500.
* For the five "special" cities (incl. City of Los Angeles) the county line is computed at
  the full **$1.10 per $1,000**; the City of LA adds **$2.25 per $500** plus the ULA tiers.
* County and city tax must be listed separately on the declaration.
* Combined City of LA + County documentary burden therefore ≈ **0.56%** before ULA.

### Proposition 13 (California Constitution, Article XIII A) — official statute text
https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=CONS&article=XIII%20A

Verified in the fetched text: the full cash value base "may reflect from year to year the
inflationary rate **not to exceed 2 percent** for any given year", and the base may be
reduced for "substantial damage, destruction, or other factors causing a decline in
value". Change of ownership triggers a new base year value (that is the mechanics of
Article XIII A §2), which is why a sale resets the buyer's assessment.

**Practical consequence:** a long hold compounds a tax wedge in the owner's favour —
assessed value can rise at most 2%/yr while market value is free to rise faster. That
wedge is destroyed the moment the property sells. This is a real, quantified component of
"preservation of wealth" and it is modelled.

### Section 1031 like-kind exchange — IRS fact sheet FS-2008-18
https://www.irs.gov/newsroom/like-kind-exchanges-under-irc-code-section-1031

* Gain is **deferred, not eliminated**.
* **45 days** to identify replacement property in writing; **180 days** (or the tax return
  due date, if earlier) to close.
* Cannot touch the proceeds — a qualified intermediary is required.
* **Flagged:** the IRS marks this page as archival/historical and points to
  "Like-Kind Exchanges – Real Estate Tax Tips". The 45/180-day mechanics quoted here are
  from the archival sheet; the owner's CPA must confirm current law before relying on it.

## C1. Catastrophe and insurance

### CAL FIRE Fire Hazard Severity Zones (official method + status)
https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones

* FHSZ classes: Moderate / High / Very High. Maps rank **hazard**, not risk.
* SRA maps effective **April 1, 2024**; LRA maps rolled out in four phases during 2025.
* For Local Responsibility Area (which is what the City of Los Angeles is), the page says
  to "contact your local jurisdiction for information on a specific area".
* **Therefore: SP-01's FHSZ class cannot be verified without the address. Left blank, flagged.**

### CAL FIRE 2026 year-to-date statewide activity (official dashboard)
https://www.fire.ca.gov/incidents — as displayed 2026-11-06:
6,389 wildfires · 339,481 acres burned · 3 fatalities · 177 structures destroyed ·
521,017 total emergency responses.
The same page's seasonal outlook (through February 2027) forecasts **below-normal**
significant fire potential for Southern California, with cooler/wetter conditions and a
possible strong El Niño.

### California FAIR Plan — official presentation to the Assembly Insurance Committee,
28 January 2026 (Legislative source)
https://ains.assembly.ca.gov/system/files/2026-01/fair-plan-oversight-hearing-powerpoint.pdf

| Metric | Value (as presented) |
|---|---|
| FAIR Plan total exposure | **$724 billion** (Dec 2025) |
| Policies in force | **668,609** (Dec 2025) |
| Commercial policies in force | **21,717** (Dec 2025) — vs 7,315 (Sep 2022) |
| Dwelling policies in force | 646,892 (Dec 2025) |
| Commercial Fire Policy limits | $100M per location (3-yr programme), $20M per building |
| Dwelling rate filing 9/2025 | 35.8% filed, **pending** at the time of the presentation |
| Eaton & Palisades fires, one year on | ~5,400 claims, ~$3.5B paid to date |

**Why this matters for a NNN landlord:** in a true NNN lease the tenant pays insurance, so
the landlord is *hedged* on premium inflation — but the tenant's occupancy cost rises, and
that is a renewal risk, not a landlord cost. Where the lease is not truly NNN (landlord
insures, or caps controllable costs), premium inflation is a direct NOI hit. Which of the
two applies to SP-01 is **unknown and flagged**.

### USGS Earthquake Hazards Program (official)
https://www.usgs.gov/programs/earthquake-hazards — verified live 2026-11-06 (2023 50-state
National Seismic Hazard Model is the current revision). Site-specific ground motion,
liquefaction and Alquist-Priolo fault-zone status for SP-01 **not verified** — the CGS
Alquist-Priolo page returned a 404 and a parcel-level query needs the address. Blank + flagged.
