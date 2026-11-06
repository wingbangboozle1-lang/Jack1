# FRED / BLS / Census raw extracts
All values below were retrieved 2026-11-06 via the public FRED CSV endpoint
(`https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIES>&cosd=<start>`).
Series metadata (title/source/units/coverage/last-updated) was read from `https://fred.stlouisfed.org/data/<SERIES>`.

---

## LAUR / unemployment — Los Angeles-Long Beach-Anaheim MSA (LOSA106UR)
Metadata: "Unemployment Rate in Los Angeles-Long Beach-Anaheim, CA (MSA)", Source U.S. Bureau of Labor Statistics,
Release "Metropolitan Area Employment and Unemployment", Smoothed Seasonally Adjusted, Monthly, Percent,
range 1990-01-01 to 2026-09-01, last updated 2026-10-28.
URL: https://fred.stlouisfed.org/series/LOSA106UR

Selected values (verbatim from CSV):
| date | value |
|---|---|
| 2019-12 | 4.2 |
| 2020-04 | 16.5 |
| 2020-05 | 18.2 |
| 2021-12 | 5.9 |
| 2022-12 | 4.4 |
| 2023-12 | 5.0 |
| 2024-07 | 5.5 |
| 2024-09 | 5.6 |
| 2024-12 | 5.4 |
| 2025-06 | 5.3 |
| 2025-09 | 5.4 |
| 2025-12 | 5.3 |
| 2026-03 | 5.1 |
| 2026-06 | 5.0 |
| 2026-08 | 4.7 |
| 2026-09 | 4.6 |
(minimum in series 1990→2026: 4.0 in 2000-09/10; maximum: 18.2 in 2020-05)

## CAUR — California unemployment rate
Metadata: Source U.S. Bureau of Labor Statistics; Monthly; Percent; seasonally adjusted; retrieved same day.
Selected: 2019-12 = 4.1; 2020-04 = 16.1; 2022-12 = 4.4; 2024-12 = 5.4; 2025-12 = 5.5; 2026-06 = 5.2; 2026-09 = 5.1.
URL: https://fred.stlouisfed.org/series/CAUR

## SMU06310800000000001 — Total nonfarm employment, Los Angeles-Long Beach-Anaheim MSA
Metadata: "All Employees: Total Nonfarm in Los Angeles-Long Beach-Anaheim, CA (MSA)",
Source BLS + FRED, NOT seasonally adjusted, Monthly, Thousands of Persons, 1990-01-01 → 2026-09-01.
URL: https://fred.stlouisfed.org/series/SMU06310800000000001
Selected (NSA, thousands):
| period | value |
|---|---|
| 2019-12 | 6347.6 |
| 2020-04 | 5252.9 |
| 2022-12 | 6234.8 |
| 2023-12 | 6258.3 |
| 2024-12 | 6283.7 |
| 2025-12 | 6282.4 |
| 2026-06 | 6311.1 |
| 2026-09 | 6299.9 |

## SMS06310800000000001 — same measure, SEASONALLY ADJUSTED
URL: https://fred.stlouisfed.org/series/SMS06310800000000001
Selected: 2019-12 n/a in excerpt; 2020-04 = 5257.8; 2022-12 = 6234.8; 2024-12 = 6283.7;
2025-12 = 6282.4; 2026-06 = 6311.1; 2026-09 = 6299.9.
**Verification note:** the two series (NSA vs SA) differ month-to-month; both are quoted with the correct label
because the series IDs differ only by `M`/`S` and are easy to confuse. Peak-of-record for the SA series in
the fetched window is 2026-06 = 6311.1; the series was 6310.2 in 2020-01.

## MHICA06037A052NCEN — Median household income, Los Angeles County
Metadata: Source U.S. Census Bureau, SAIPE, Annual, Dollars, 1989→2024, last updated 2026-02-09.
URL: https://fred.stlouisfed.org/series/MHICA06037A052NCEN
| year | value |
|---|---|
| 2010 | 52,595 |
| 2015 | 59,045 |
| 2019 | 72,721 |
| 2020 | 75,624 |
| 2021 | 77,356 |
| 2022 | 82,455 |
| 2023 | 86,499 |
| 2024 | 90,757 |

## CPIAUCSL — CPI-U, U.S. city average, all items, SA
URL: https://fred.stlouisfed.org/series/CPIAUCSL
Selected: 2020-01 = 259.127; 2024-12 = 317.604; 2026-09 = 336.298.
Derived (not a source value): 2020-01→2026-09 = +29.8% (336.298/259.127 − 1).

## CUSR0000SEFV — CPI-U, Food away from home, U.S. city average, SA
Metadata: Source BLS, "Consumer Price Index", Monthly, Index 1982-84=100, 1953→2026-09, updated 2026-10-14.
URL: https://fred.stlouisfed.org/series/CUSR0000SEFV
Selected: 2019-12 = 298.253; 2022-12 = 343.559; 2024-12 = 374.644; 2025-12 = 389.889; 2026-09 = 398.783.
Derived: 2020-01→2026-09 = +37.9%; 2025-09→2026-09 = +3.5%.

## DGS10 — 10-Year Treasury constant maturity
Metadata: Board of Governors of the Federal Reserve System (H.15), Daily, Percent.
URL: https://fred.stlouisfed.org/series/DGS10
Selected: 2020-01-02 = 1.88; 2021-12-31 = 1.51; 2024-12-31 = 4.57 (approx window); 2026-01-02 = 4.19;
2026-09-30 = 5.29; 2026-11-04 = 4.90.
Derived: 2026 low 3.97 (2026-02-27) → 2026 high 5.31 (2026-10-05) within the fetched window.

## BAA — Moody's Seasoned Baa corporate bond yield
URL: https://fred.stlouisfed.org/series/BAA
Selected: 2026-01 = 5.88; 2026-06 = 6.00; 2026-10 = 6.59.

## DRCRELEXFACBS — CRE loan delinquency rate, all commercial banks
Metadata: Board of Governors of the Federal Reserve System, "Charge-Off and Delinquency Rates on Loans and
Leases at Commercial Banks", Quarterly (end of period), Percent, 1991Q1 → 2026Q2, last updated 2026-08-25.
URL: https://fred.stlouisfed.org/series/DRCRELEXFACBS
Selected: 2019Q4 = 0.67; 2020Q4 = 1.15; 2024Q4 = 1.56; 2025Q4 = 1.58; 2026Q2 = 1.53.
Derived: today's delinquency (1.53%) is roughly 1/5 of the 2010 peak (8.75%) — relevant to the "credit-crunch
blocks my exit" scenario.

---

# CENSUS QUICKFACTS (retrieved 2026-11-06)
URL base: `https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045224` and
`.../losangelescountycalifornia/PST045224`

City of Los Angeles | Los Angeles County
| Indicator (vintage) | City | County |
|---|---|---|
| Population, 2025 est. (V2025) | 3,869,089 | 9,694,934 |
| Population, 2020 Census | 3,898,747 | 10,014,009 |
| % change 2020→2025 | −0.8% | −3.2% |
| Median household income (2020-24, 2024 $) | $81,939 | $90,112 |
| Per capita income (2020-24, 2024 $) | $47,685 | $45,792 |
| Persons in poverty | 16.5% | 13.3% |
| Bachelor's degree+ (2020-24) | 38.5% | 36.0% |
| HS graduate+ (2020-24) | 79.6% | 80.9% |
| Median gross rent (2020-24) | $1,933 | $1,954 |
| Median home value (2020-24) | $921,200 | $834,200 |
| Owner-occupied rate (2020-24) | 36.0% | 45.9% |
| Persons per household | 2.61 | 2.81 |
| Labor force participation (2020-24) | 66.4% | 64.7% |
| Language other than English at home | 56.4% | 55.1% |
| Building permits, 2025 | X (not available) | 22,250 |
| Total retail sales 2022 ($1,000) | 81,351,523 | 213,932,785 |
| Retail sales per capita 2022 | $21,281 | $22,010 |
| Accommodation & food services sales 2022 ($1,000) | 17,366,966 | 44,000,801 |
| Employer establishments 2023 | X | 304,988 |
| Total employment 2023 | X | 3,987,736 |
| Employment change 2022-23 | X | +2.3% |
| Population per sq mi (2020) | 8,304.2 | 2,466.9 |
| Land area sq mi (2020) | 469.49 | 4,059.28 |
| Mean travel time to work (min) | 30.7 | 30.4 |

Note "X" = the Census table itself shows "not applicable/not available" — these cells are left blank on the site.
