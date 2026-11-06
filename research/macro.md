# Research log — macro & capital markets

All values below were fetched and read on **2026-11-06**. Every row records the exact
figure seen, the page it came from, and the as-of date printed on that page. Nothing in
this file is estimated.

## M1. Policy rate

| Field | Value | Source | As-of on source |
|---|---|---|---|
| FOMC target range for federal funds | **3.75%–4.00%** | https://www.federalreserve.gov/monetarypolicy/openmarket.htm | Table "2026": only entry is *September 17, Increase 25 bp, Level 3.75-4.00*. |
| Prior path 2025 | 3.50–3.75 (Dec 11), 3.75–4.00 (Oct 30), 4.00–4.25 (Sep 18) — all decreases of 25 bp | same page | — |

Verified: page read directly; the 2026 row is an *increase* of 25 bp to 3.75–4.00, i.e.
the Fed had eased 75 bp through 2025 and then tightened once in Sept 2026.

## M2. Long rate (the single most important input to a NNN valuation)

| Field | Value | Source | As-of |
|---|---|---|---|
| 10-year Treasury constant maturity | **4.90%** (2026-11-04); 4.95 (11-03); 4.91 (11-02); 4.94 (10-30); 4.98 (10-29) | https://fred.stlouisfed.org/series/DGS10 — series DGS10, source *Board of Governors of the Federal Reserve System*, release *H.15 Selected Interest Rates* | 2026-11-04, updated Nov 5 2026 |

Treasury's own daily par-yield table (https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026)
was also opened; it renders 25 rows per page, so the FRED mirror of the Fed's H.15
release was used to read the most recent print. The H.15 series *is* the official series;
FRED is the Federal Reserve Bank of St. Louis redistributing it.

Implied spread of the 10-year over the top of the funds range: 4.90 − 4.00 = **+90 bp**.
That is a steep, term-premium-heavy curve — hostile to long-duration, bond-proxy assets
like a net-leased QSR.

## M3. Inflation

| Field | Value | Source | As-of |
|---|---|---|---|
| CPI-U, US city average, 12-month change | **+3.7%** | https://www.bls.gov/news.release/cpi.nr0.htm (USDL-26-1574) | September 2026, released 2026-10-14 |
| CPI-U core (all items less food & energy), 12-month | +2.6% | same | September 2026 |
| Food away from home, 12-month | +3.5% | same | September 2026 |
| Limited-service meals, 12-month | **+3.2%** | same | September 2026 |
| Shelter, 12-month | +3.2% | same | September 2026 |

Why "limited-service meals" matters: it is the price index for the exact product the
tenant sells. If the tenant's selling prices are rising 3.2% while a fixed-rent NNN lease
escalates 0–2%, the tenant's rent-to-sales ratio *falls* → the lease is cheap to the
tenant → renewal is more likely. This is a real, quantified argument in the memo.

## M4. Los Angeles metro inflation (BLS, same EAG page as labour data)

| Field | Value | Source | As-of |
|---|---|---|---|
| CPI-U Los Angeles-Long Beach-Anaheim, 12-month % change | **+3.7%** (Sept 2026); 3.6 (Aug), 3.4 (Jul), 3.3 (Jun), 3.6 (May), 3.7 (Apr) | https://www.bls.gov/eag/eag.ca_losangeles_msa.htm | data extracted 2026-11-05 |
| CPI-U index level | 358.725 (Sept 2026), 1982-84=100 | same | — |
| CPI-W LA, 12-month % change | +4.1% (Sept 2026) | same | — |

Local inflation running at the national rate. Note CPI-W at 4.1% — if the lease's
escalator is CPI-linked, that is the index that usually governs commercial leases, and
it is *higher* than CPI-U. Favourable to the landlord on renewal.

## M5. Rate environment summary used by the model

| Input | Value | Source |
|---|---|---|
| Risk-free 10-yr | 4.90% | M2 |
| Policy rate top | 4.00% | M1 |
| National CPI | 3.7% | M3 |
| LA CPI (CPI-W) | 4.1% | M4 |

Flagged: the 10-year at 4.90% with the funds rate at 3.75–4.00% implies mortgage/CMBS
spreads for single-tenant QSR paper in the 6.5–8.0% range. No official series publishes
commercial mortgage rates for this asset class, so **this spread is a stated assumption,
not a verified fact** — it is labelled as such everywhere it appears.
