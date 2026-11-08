# Verification log — 08 November 2026 pass

Session: `arena-9707cb4b` · branch `arena/9707cb4b-jack1`
Scope: every headline figure on the published dashboard, re-read from the official page. No value was
inherited from a prior session without being re-opened; anything not re-opened is listed in §4.

Method: each official page was fetched directly and read in full text (Census QuickFacts tables, BLS
series data, FRED series pages, SEC/N/A pages, CAL FIRE incident pages, City of LA FAQ/wage pages).
Where a figure is arithmetic on a published figure, the formula and both inputs are recorded here and
the site labels the output `derived`.

---

## 1. Checks performed — matched

| # | Figure on site | Official page read | Value found | Result |
|---|---|---|---|---|
| V-01 | LA city population 3,869,089 | https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225 | 3,869,089 (July 1, 2025, V2025) | match |
| V-02 | City population change −0.8% | same | −0.8% (2020 estimates base → 2025) | match |
| V-03 | City median household income $81,939 | same | $81,939 (2020–2024, 2024 dollars) | match |
| V-04 | City median gross rent $1,933 | same | $1,933 | match |
| V-05 | Owner-occupied rate 36.0% | same | 36.0% | match |
| V-06 | Population density 8,304.2/sq mi | same | 8,304.2 (2020 Census) | match |
| V-07 | Retail sales $81.35B (2022) | same | $81,351,523 thousand | match |
| V-08 | Accommodation & food services $17.37B (2022) | same | $17,366,966 thousand | match |
| V-09 | County population 9,694,934; −3.2% | https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045225 | 9,694,934; −3.2% (base 10,017,414) | match |
| V-10 | City annual unemployment 5.8% (2025) | https://www.bls.gov/lau/city-annual-unemployment-rates.htm | 5.8; footnote: 2025 = 11-month average excluding October | match, caveat confirmed |
| V-11 | County GDP $1.003T (2024) | https://fred.stlouisfed.org/series/GDPALL06037 | 1,002,965,029 thousand (2024) | match |
| V-12 | Metro GDP $1.295T (2023) | https://fred.stlouisfed.org/series/NGMP31080 | 1,295,361.403 million (2023), series title includes (DISCONTINUED) | match |
| V-13 | USGS 60% / 46% / 31% in 30 years | https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-los-angeles-area-san-francisco-bay-area | 60% M6.7, 46% M7.0, 31% M7.5 | match |

## 2. Checks that produced a change

| # | Issue | Evidence | Action |
|---|---|---|---|
| V-14 | Executive summary asserted metro GDP "$1.355 trillion (2024, BEA)" | NGMP31080 has no 2024 observation and is marked DISCONTINUED; latest is 2023 = $1.295T | text replaced with the 2023 value and discontinued status |
| V-15 | Same paragraph asserted LA County was the "#2 county economy in the U.S." | No official BEA/Census page located stating the ranking | claim removed; the verified level retained |
| V-16 | County labour rows were the December 2025 vintage | BLS LAUS series now publishes through September 2026: 4.5% preliminary; LF 5,031,013; employed 4,806,494; unemployed 224,519 | latest vintage added; both vintages shown |
| V-17 | CAL FIRE KPI card was "Flagged" with a withheld 26% claim | CAL FIRE incident pages publish realised damage: Palisades 23,448 ac / 6,845 destroyed / 975 damaged / 12 fatalities; Eaton 14,021 ac / 9,419 destroyed / 1,076 damaged / 19 fatalities | card replaced with verified realised impact; damage counts used, percentage-expansion claims still withheld |
| V-18 | Measure ULA thresholds previously treated as unconfirmable | https://finance.lacity.gov/faq/measure-ula states $5,400,000 / $10,900,000 for closings after June 30, 2026, ULA 4%/5.5%, base 0.45% | published; flagged item closed |

## 3. New figures added in this pass (verified same day)

| # | Figure | Official page | Value |
|---|---|---|---|
| V-19 | CPI-U | https://fred.stlouisfed.org/series/CPIAUCSL | Sep 2026 336.298; Sep 2025 324.245 |
| V-20 | 10-year Treasury | https://fred.stlouisfed.org/series/DGS10 | 4.84% (2026-11-05) |
| V-21 | LA City minimum wage | https://wagesla.lacity.gov/ | $18.42/hour effective July 1, 2026 |
| V-22 | California fast-food wage (AB 1228) | https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm | $20.00/hour from April 1, 2024; covers franchisee employers |

## 4. Carried forward — NOT re-read in this pass

These remain on the site with the date they were last read (07 Nov 2026). They are not upgraded here.

- SCAG Connect SoCal 2024 forecast tables (county population 10.046M→10.793M; employment 5.031M→5.461M; sector additions).
- LA City Planning DTLA 2040 quantities (100,000 homes; 175,000 residents; 100,000 work opportunities).
- SEC Form 10-Q (period ended 05 Jul 2026) line items: revenue, continuing-operations earnings, debt, restaurant counts; Form 10-K lease disclosures.
- FEMA National Risk Index county scores, expected annual loss, and declaration counts — not readable from an official page in the 07 Nov pass; still blank.
- California Department of Insurance wildfire claims tracker aggregates.
- IRS Publication 544 and California FTB capital-gain pages (tax framework only).
- LA County Assessor portal, ZIMAS, LA City Planning zoning search, CGS EQ Zapp, FEMA flood tools, Census/LAUSD/CDE school lookups — linked as lookup tools, no value published.
- CAL FIRE FHSZ 2025 mapping percentages (26% very-high expansion; 35% statewide) — still withheld; no official page carrying the percentages was located.

## 5. Derived arithmetic performed (all site outputs labelled `derived`)

| # | Output | Inputs | Formula | Result |
|---|---|---|---|---|
| D-01 | SCAG county population CAGR | 10.046M (2019) → 10.793M (2050) | (end/start)^(1/31)−1 | +0.232%/yr |
| D-02 | SCAG county employment CAGR | 5.031M → 5.461M | (end/start)^(1/31)−1 | +0.265%/yr |
| D-03 | CPI year-over-year | 336.298 / 324.245 | ratio−1 | +3.72% |
| D-04 | CPI five-year CAGR | 273.910 (Sep 2021) → 336.298 (Sep 2026) | ^(1/5)−1 | +4.19%/yr |
| D-05 | County 2025 average unemployment | eleven published months, sum 62.1 | ÷11 | 5.645% → shown as 5.6% |
| D-06 | Annualised earthquake probability | 30-year p = 0.60 / 0.46 / 0.31 | 1−(1−p)^(1/30) | 3.0% / 2.0% / 1.2% per year |
| D-07 | Break-even NOI growth vs cap change | entry 6.00% (illustrative), exit 6.50/7.00/7.50, n = 4/6/9 | (c1/c0)^(1/n)−1 | 0.90%–5.73% |
| D-08 | Value-ratio sensitivity | g = 2/3/4%, n = 6, exit 6.00–7.50% | (1+g)^n × (c0/c1) | 0.901–1.265 |
| D-09 | ULA arithmetic | 0.45% base, 4.0%/5.5% ULA, thresholds $5.4M/$10.9M | rate × consideration | 22,500 / 356,000 / 714,000 on illustrative $5M / $8M / $12M |

## 6. Source-integrity observations from this pass

1. **FRED NGMP31080** carries "(DISCONTINUED)" in its own title and no 2024 value. Any brief quoting a
   2024 metro GDP for this MSA must show a different, named series or it is unsupported.
2. **BLS LAUS** October 2025 rows read `-(X)` with the note "Data unavailable due to the 2025 lapse in
   appropriations", confirming the 11-month city average and forcing the county 2025 average to be
   labelled derived rather than published.
3. **CAL FIRE Eaton page** states in one paragraph that inspection teams "have completed inspections for
   100% of all structures" and in the next that "damage inspections are ongoing". Counts are used, the
   inconsistency is published on Flagged for Review, and the figures are flagged as revisable.
4. **LA Office of Finance ULA FAQ** sets thresholds by closing date, not by publication date; a future
   sale must re-read the page because the thresholds are indexed annually to chained CPI.
5. **Census vs SCAG direction conflict**: the Census Vintage-2025 estimate puts the county 3.2% below its
   2020 base while SCAG's adopted forecast shows growth to 2050. Both are official; neither is averaged
   into the other on this site.

## 7. What this pass did not do

- It did not appraise the property, and it publishes no capitalisation rate, rent, or value for it.
- It did not query any parcel or address lookup tool; every such tool is linked as a starting point only.
- It did not re-verify the SEC, SCAG, FEMA, CDI, IRS, FTB, Assessor, ZIMAS, CGS or school sources
  listed in §4; those keep their 07 Nov 2026 read date.
