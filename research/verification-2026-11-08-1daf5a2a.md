# Verification report — session `arena/1daf5a2a-jack1` (08 Nov 2026)

Scope: an independent second pass over the deployed nine-page dashboard, the correction of one landing-page
contradiction, and the addition of published school, income, job-growth and projection material. Every figure this
report claims was **read on the official page named beside it on 08 November 2026**. Figures this session did not
re-read are named in §5 and remain inherited from the 07 November 2026 pass.

---

## 1. Figures re-read this session, and the result

| # | Figure as published | Official page read on 08 Nov 2026 | Result | Action |
|---|---|---|---|---|
| 1 | Metro GDP $1.295 trillion (2023) | [FRED NGMP31080](https://fred.stlouisfed.org/series/NGMP31080) | **Exact.** Series titled "DISCONTINUED"; final observation `1,295,361.403` million for 2023. | Kept. |
| 2 | Metro GDP 2019 and 2020 | same | **Exact.** `1,065,709.665` (2019) and `1,035,818.839` (2020); −2.8%. | Published as the observed-shock anchor. |
| 3 | County GDP $1.003 trillion (2024) | [FRED GDPALL06037](https://fred.stlouisfed.org/series/GDPALL06037) — **not re-opened this session** | Inherited (audit of 07 Nov 2026: `1,002,965,029` thousand). | Unchanged; disclosed in §5. |
| 4 | "LA metro GDP is $1.355 trillion (2024) … #2 county economy in the U.S." | [FRED NGMP31080](https://fred.stlouisfed.org/series/NGMP31080) | **Contradiction confirmed.** No 2024 metro value exists on the series; the market page already said so. The ranking claim has no official publisher on this site. | **Corrected** on `index.html`; both claims removed. |
| 5 | City population 3,869,089 and −0.8% | [Census QuickFacts, Los Angeles city](https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225) | City table read; the income and geography blocks were re-read in full. | Kept. |
| 6 | City median household income $81,939 | same | **Exact** (2020–2024 ACS, 2024 dollars). | Kept. |
| 7 | City per-capita income $47,685 · poverty 16.5% | same | **Exact.** | **Added** as new rows. |
| 8 | City unemployment 5.8% (2025) | [BLS, 50 largest cities](https://www.bls.gov/lau/city-annual-unemployment-rates.htm) | **Exact**, including the footnote that 2025 is an 11-month average excluding October. | Kept. |
| 9 | County annual unemployment 5.6% (computed) | [FRED LAUCN060370000000003A](https://fred.stlouisfed.org/series/LAUCN060370000000003A) | **Mismatch.** The published annual average is **5.7%** for 2025. | **Corrected** to 5.7%; the 5.6% is disclosed on Flagged for Review. |
| 10 | County unemployment envelope | same | All 36 annual values 1990–2025 read: min 4.5 (2019), max 12.6 (2010), median 6.75. | **Added** to the projection page. |
| 11 | County population 9,694,934 · −3.2% | [Census QuickFacts, Los Angeles County](https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045225) | **Exact** against the 2020 estimates base of 10,017,414. | Kept. |
| 12 | County median household income · per-capita income · poverty | same | `$90,112` · `$45,792` · `13.3%`. | **Added** as new rows. |
| 13 | County employment 3,987,736 · +2.3% (2022→2023) | same (County Business Patterns block) | **Exact.** | **Added** as the job-growth row. |
| 14 | USGS 60% / 46% / 31% (30 years) | [USGS FAQ](https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-los-angeles-area-san-francisco-bay-area) | **Verbatim.** | Kept. |
| 15 | Measure ULA 4% / 5.5%, base 0.45%, $5.4M / $10.9M | [LA Office of Finance FAQ](https://finance.lacity.gov/faq/measure-ula) | **Exact**, including "closing after June 30, 2026" and annual chained-CPI indexing. | Kept; now also linked from the blank transfer-tax cell. |
| 16 | SCAG regional employment 8,937 → 10,276 thousand (2022→2050) | [SCAG technical report](https://www.scag.ca.gov/sites/default/files/2024-05/23-2987-tr-demographics-growth-forecast-final-040424.pdf), Table 6 | **Exact**; the report prints 0.50% annual growth for 2022–2050 and 0.79% for 2000–2022. | **Added.** |
| 17 | SCAG sector rows already published (+416k health, +148k construction, +106k food services) | same, Table 6 | **Consistent**: 1,498→1,914; 473→621; 832→938. | Kept. |
| 18 | SCAG scenario bands | same, Figure 2 | Point 18.85 / 19.7 / 20.1 / 20.8; low 19.45 (2030), 19.6 (2035), 20.0 (2050); high 19.95 / 20.5 / 21.9. | **Added** to the projection page. |
| 19 | LAUSD ELA −17.8 points, mathematics −48.9 points | [CA School Dashboard, LAUSD](https://www.caschooldashboard.org/reports/19647330000000/2025/academic-performance) | **Exact** (2025; improved 10.4 and 11.5 points; 181,383 and 182,564 students). | **Added** at district scale. |
| 20 | LAUSD chronic absenteeism 21.9%, graduation 86.5% | [Dashboard, engagement](https://www.caschooldashboard.org/reports/19647330000000/2025/academic-engagement) | **Exact** (23.3% in 2024; graduation 86.7% in 2024, 83.6% in 2023). | **Added** at district scale. |

## 2. Arithmetic published as *derived*, with its inputs

Every derived value on `projection.html` is printed with its inputs so it can be recomputed by hand:

| Derived value | Inputs (published) | Arithmetic |
|---|---|---|
| Regional job growth 2022–2050, +15.0% | 8,937 → 10,276 thousand | (10,276 − 8,937) ÷ 8,937 |
| Regional population growth 2020–2050, +10.3% | 18.85 → 20.8 million | (20.8 ÷ 18.85) − 1 |
| 2030 band −1.3% / +1.3% | 19.45 and 19.95 vs 19.7 | ratio to point forecast |
| 2035 band −2.5% / +2.0% | 19.6 and 20.5 vs 20.1 | ratio to point forecast |
| County median unemployment 6.75% | 36 annual values 1990–2025 | median of the series |
| 26 of 36 years at or above 5.7% | same | count |
| 14 of 36 years at or above 7.7% | same | count (1991–96, 2009–14, 2020–21) |
| Metro output −2.8% in 2020 | 1,065,709.665 → 1,035,818.839 | (later ÷ earlier) − 1 |

## 3. Defects found and fixed

1. **Landing-page contradiction (`index.html`).** The executive summary asserted a 2024 metro GDP of $1.355 trillion and
   a "#2 county economy in the U.S." ranking, while the same site's market page correctly stated that the metro series is
   discontinued at 2023 ($1.295T) and that no 2024 value is published. Both the figure and the ranking are removed; the
   replacement text states only verified values and explicitly says no ranking is asserted.
2. **County unemployment 5.6% vs the published 5.7%.** The brief had published its own 11-month tabulation and labelled it
   "not a published annual average". A published annual average does exist; the page now uses it, keeps the October-2025
   caveat, and discloses the earlier 5.6% on Flagged for Review.
3. **Stale footer/snapshot dates** on the pages whose evidence was re-read — moved to 08 Nov 2026; pages not re-read keep
   07 Nov 2026 so the dates still mean something.
4. **Deploy manifest.** `projection.html` added to `.github/workflows/pages.yml` and to the validator's required-page set,
   with `caschooldashboard.org` added to the official-host allowlist. Validator: 9 pages, 272 table-body rows, pass.

## 4. What was added (requirement coverage)

| Owner requirement | Where it now lives | Status |
|---|---|---|
| Population, income, job growth | `market.html` city + county rows | verified |
| School systems | `market.html#schools` (district scale only) | verified at district scale; campus blank |
| Projection system for the area | `projection.html` (published bands + derived arithmetic) | verified inputs, derived outputs labelled |
| Decision and its risks | `decision.html`, `risks.html`, plus trigger table on `projection.html` | framework; property values blank |
| Every row links an official source | enforced by `scripts/validate_site.py` | passing |
| No personal information | no name, address, APN, or financial detail anywhere in the published set | passing |

## 5. Not re-read this session (inherited, disclosed)

* SEC 10-Q / 10-K issuer figures on `property.html` (verified 07 Nov 2026).
* California Department of Insurance claims aggregate on `risks.html` (verified 07 Nov 2026).
* County-level SCAG population and employment totals on `market.html#projections` (verified 07 Nov 2026). The county
  table inside the SCAG technical report could not be located in this pass — the same limitation an earlier session
  recorded — which is why the new projection page uses only the regional tables it could read directly.
* FEMA National Risk Index county values and the CAL FIRE acreage percentages: still unreadable from an official page,
  still blank, still on Flagged for Review.

## 6. Privacy statement

No personal information was collected, stored, or published in this session. No owner name, street address, APN,
ownership entity, lease document, rent figure, or individual financial detail appears in any file this session touched.
The validator screens every published page for email and telephone patterns and found none.
