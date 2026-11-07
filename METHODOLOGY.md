# Methodology

## 1. Principle

Publish what an official page says, with the link; leave blank what no official page says; state the arithmetic when a
number is computed. No value is inferred, interpolated, blended across geographies, or carried over from a prior build
without being re-read.

## 2. Status vocabulary

| Status | Meaning | Rendered as |
|---|---|---|
| `verified` | Read directly from the linked official page on 2026-11-07 | Value + green badge |
| `derived` | Arithmetic on verified values; formula stated in the row note | Value + blue badge |
| `unverified` | No official source could confirm it in this session | Blank + amber badge |
| `withheld` | Exists in the owner's file; excluded by the privacy policy | Blank + grey badge |

A blank is never zero and never an estimate.

## 3. Sources and what each was used for

| Source | Used for |
|---|---|
| Census QuickFacts, Los Angeles city and county (V2025 / ACS 2020-2024) | Population, households, income, poverty, housing, density, education, travel time |
| BLS Economy at a Glance, Los Angeles-Long Beach-Santa Ana MSA | Labour force, employment, unemployment rate, nonfarm and sector change |
| BLS CPI, Los Angeles area, September 2026 | Headline, core, food, food away from home, shelter, energy, gasoline |
| Federal Reserve H.15 via FRED, series DGS10 | 10-year Treasury yield (2026-11-05: 4.84%) |
| SEC EDGAR, 8-K Ex-99.1, Q4/FY2025 earnings release | Tenant restaurant counts, same-store sales, closures, revenue, EBITDA, guidance, dividend |
| City of Los Angeles Office of Finance, transfer tax and Measure ULA FAQ | 0.45% base tax; 4.0% above $5.4m; 5.5% at $10.9m; chained-CPI indexation |
| LA County Assessor, decline-in-value | Proposition 13 2% cap; Proposition 8 relief; RP-87 filing window |
| California DIR, Fast Food Council | $20.00/hour fast-food minimum wage from 2024-04-01 |
| CAL FIRE, Palisades Fire | Acres, structures destroyed and damaged, fatalities, containment, cause |
| CAL FIRE OSFM, Fire Hazard Severity Zones | Three hazard classes; SRA effective date; 2025 LRA rollout |
| California Geological Survey, Alquist-Priolo | 50 ft setback rule; definition of an active fault; disclosure duties |
| USGS, ShakeOut scenario | 1,800 deaths, 53,000 injuries, $191bn loss, ~1,600 fires |
| NCES Common Core of Data, Los Angeles Unified | Schools, enrolment, teachers, ratio, revenue and spending per student |
| California School Dashboard (CDE) | Official lookup for district performance (not opened; item left blank) |
| California Department of Finance, population projections | Official county projections (workbook unreadable; items left blank) |
| BEA GDP by metro area and by county (via FRED) | Metropolitan and county output |
| USGS UCERF3 FAQ | 30-year regional earthquake probability |
| IRS, Section 1031 fact sheet | 45-day identification, 180-day completion, real-property scope |
| LA City Planning (ZIMAS), LA County Assessor lookup | Official parcel lookups (no query run without the address) |

## 4. Model

The projection model is arithmetic, not forecasting.

- Value: `V = NOI / c`
- Net proceeds: `P - (0.0045 + u(P))·P - 0.02·P`, with `u(P) = 0` up to $5.4m, `0.04` above $5.4m, `0.055` at $10.9m+
- Hold NPV: `Σ_{t=1..5} NOI·(1+g)^t/(1+d)^t + net proceeds(NOI·(1+g)^5 / c5)/(1+d)^5`
- Break-even exit rate: bisection on the hold NPV

Assumptions are labelled as assumptions on the model page: NOI scenarios of $150k-$300k, cap rates 5.25%-7.25%, rent
growth 2.5%, discount rate 7.5%, sale costs 2.0%. They are inputs chosen to show sensitivity, not observations.

## 5. Validation gate

`python3 scripts/validate_site.py` performs 3,018 assertions and fails the build on:

1. a missing page, asset or dataset;
2. a page missing its doctype, language, title, single `h1`, main landmark or navigation, or a navigation that does not
   list all eleven pages;
3. a broken internal link or an unresolved in-page anchor;
4. a data-table row with no official source link (computed tables must instead carry an official basis in a footer row);
5. an external link outside the official-domain allowlist (census.gov, bls.gov, fred.stlouisfed.org, sec.gov,
   lacity.gov, lacounty.gov, ca.gov, usgs.gov, irs.gov, nces.ed.gov, caschooldashboard.org);
6. an external link without `target="_blank"` and `rel="noopener"`;
7. a value published on an `unverified` or `withheld` row, or a blank on a `verified` or `derived` row;
8. a source URL that is not https or not allowlisted;
9. an email-address or telephone-number pattern on any page.

## 6. Reproduction

```
python3 scripts/build_site.py     # regenerate all pages, CSS, JS, data/published-records.json
python3 scripts/validate_site.py  # run the gate
python3 -m http.server 4173 --bind 0.0.0.0   # preview
```

## 7. Limits

Point-in-time (2026-11-07). Labour and price series are revised. The tenant's audited statements, credit rating,
location-level performance and the executed lease were not reviewed. No parcel is identified. Official county population
projections could not be read in this environment and are withheld rather than approximated. No probability is assigned to
any hazard or black-swan event.
