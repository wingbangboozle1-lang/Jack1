# Research log — site, area, demographics, schools

Fetched and read 2026-11-06. Property is anonymized as **SP-01**; no address is used or
stored anywhere, so no parcel-level lookup (FHSZ zone, flood zone, seismic site class,
zoning) could be performed. Those rows are published as **blank + flagged**, per the
verification rule.

## A1. City of Los Angeles — Census QuickFacts
Source: https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045224

| Metric | Value | Vintage (as printed) |
|---|---|---|
| Population estimate | 3,869,089 | July 1, 2025 (V2025) |
| Population, 2020 Census | 3,898,747 | Apr 1, 2020 |
| Change, 2020 base → 2025 | **−0.8%** | V2025 |
| Persons under 18 | 19.2% | V2025 |
| Persons 65+ | 14.2% | V2025 |
| Foreign-born | 35.7% | 2020–2024 ACS |
| Households | 1,439,097 | 2020–2024 |
| Persons per household | 2.61 | 2020–2024 |
| Owner-occupied housing unit rate | 36.0% | 2020–2024 |
| Median value, owner-occupied units | $921,200 | 2020–2024 |
| Median gross rent | $1,933 | 2020–2024 |
| Median household income (2024$) | **$81,939** | 2020–2024 |
| Per capita income (2024$) | $47,685 | 2020–2024 |
| Persons in poverty | **16.5%** | 2020–2024 |
| High school graduate or higher (25+) | 79.6% | 2020–2024 |
| Bachelor's degree or higher (25+) | 38.5% | 2020–2024 |
| In civilian labour force (16+) | 66.4% | 2020–2024 |
| Living in same house 1 yr ago | 89.3% | 2020–2024 |
| Language other than English at home | 56.4% | 2020–2024 |
| Mean travel time to work | 30.7 min | 2020–2024 |
| Population per square mile | 8,304.2 | 2020 |
| Land area | 469.49 sq mi | 2020 |
| Total retail sales | $81,351,523,000 | 2022 Economic Census |
| Retail sales per capita | $21,281 | 2022 |
| Accommodation & food services sales | $17,366,966,000 | 2022 |

## A2. Los Angeles County — Census QuickFacts
Source: https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045224

| Metric | Value | Vintage |
|---|---|---|
| Population estimate | 9,694,934 | July 1, 2025 |
| Change, 2020 base → 2025 | **−3.2%** | V2025 |
| Population, 2020 Census | 10,014,009 | 2020 |
| Persons 65+ | 17.1% | V2025 |
| Foreign-born | 33.4% | 2020–2024 |
| Hispanic or Latino | 49.3% | V2025 |

## A3. Schools — NCES Common Core of Data (federal, official)
Source: https://nces.ed.gov/ccd/districtsearch/district_detail.asp?ID2=0622710
Los Angeles Unified, NCES District ID 0622710, State ID CA-1964733.

| Metric | Value | School year |
|---|---|---|
| Total schools | 784 | 2025–26 directory |
| Total students | 408,026 | 2024–25 |
| Classroom teachers (FTE) | 21,246.18 | 2024–25 |
| Student/teacher ratio | 19.20 | 2024–25 |
| Total revenue | $14,773,154,000 | fiscal 2022–23 |
| Revenue per student | $34,533 | fiscal 2022–23 |
| Total expenditures | $11,493,204,000 ($26,866/student) | fiscal 2022–23 |
| Instructional expenditure share | 55% | fiscal 2022–23 |

**Irregularity flagged:** the California Department of Education's DataQuest district
enrollment page returned a generic error page on every attempt
(`dq.cde.ca.gov/dataquest/dqcensus/EnrDistLevels.aspx?...`), so no CDE enrollment figure
is published. Third-party aggregators disagreed with each other by more than 20%
(≈497,000 vs ≈392,000 for the same year, different definitions), which is exactly the
kind of value that must not be guessed at. NCES (official, federal) is used instead and
the CDE figure is left blank and flagged.

**What the school data does and does not tell you about SP-01:** a QSR's trade area is
roughly 1–3 miles. District-wide LAUSD averages say nothing about the specific campus
that serves the site. No school-quality metric is therefore used as a valuation input;
it is reported for completeness, and the site is explicit that a parcel-level school
assignment cannot be verified without the address.

## A4. What is missing at this level of aggregation, and why that matters

Census/NCES data is at city or district level. "Central Los Angeles" spans several
distinct sub-markets with very different income, density and traffic profiles
(e.g. Koreatown/Wilshire Center, Westlake, Downtown, Pico-Union, South LA, Hollywood).
Without an address, the honest answer is a **scenario band**, not a point estimate.
The site presents the sub-market comparison as *labelled scenario bands* and flags that
parcel-level verification is required before any transaction decision.
