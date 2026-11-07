# Executive summary

**Subject:** Jack in the Box quick-service restaurant on a reported triple-net (NNN) lease, described as near
central Los Angeles, with an expiry window the owner puts at 2030-2035.
**Question:** sell before expiry, or renew?
**Answer:** **renew on market terms, hold, and sell only into a priced bid or on a stated trigger.**
**Evidence date:** 2026-11-07. **Published rows:** 154 (109 verified, 4 derived, 33 unverified/blank, 8 withheld/blank).

## 1. The recommendation in one paragraph

Secure a five-year extension or a new term now, at rent supported by independent comparables, with documented
escalations, tenant-funded roof and structure, and a guaranty. Hold the asset. Refuse to sell until a bid implies a
capitalisation rate inside the break-even band shown on the model page, or until one of the named triggers fires
(two more quarters of same-store sales below -5%, a guidance cut, a unit-count guide below 2,050, or a coverage
exclusion at insurance renewal). The failure mode to avoid is not selling too late or too early - it is arriving at
2030 with two years of term, a vacant building and no comparable sale.

## 2. Why - the five verified facts that decide it

| # | Fact | Value | Source |
|---|---|---|---|
| 1 | Remaining term is the asset's value driver; a signed extension raises both rent coverage and sale price | 5-9 years (owner-stated window, not contract-verified) | Owner statement; see `property.html` |
| 2 | The tenant's credit is weakening but intact | Systemwide same-store sales -7.4% Q4 FY2025 and -4.2% FY2025; 86 closures vs 31 openings; dividend discontinued; FY2026 guidance 2,050-2,100 restaurants, franchise-level margin $275-290m, Adjusted EBITDA $225-240m | SEC 8-K Ex-99.1 (Q4 FY2025) |
| 3 | The area economy is mild, not collapsing | MSA unemployment 4.4% (Sep 2026, preliminary); nonfarm +0.5% y/y; county population -3.2% since 2020; city -0.8% | BLS Economy at a Glance; Census QuickFacts |
| 4 | Exit friction is high and has a cliff | City base transfer tax 0.45%; Measure ULA 4.0% above $5,400,000 and 5.5% at $10,900,000, on the whole price; one dollar over the line costs about $216,000 | LA Office of Finance |
| 5 | Money is not cheap, and value is rate-sensitive | 10-year Treasury 4.84% (2026-11-05); the same income stream is worth 38% more at a 5.25% rate than at 7.25% | Federal Reserve H.15 via FRED; model page |

## 3. The decision rule (from the model)

- At a 6.25% entry capitalisation rate with $200,000 of annual NOI, the asset is worth $3.20m. Net proceeds today
  would be about $3.12m after transfer tax and assumed 2.0% costs.
- Holding five years, with 2.5% annual rent growth and a 7.5% discount rate, beats selling today unless the exit
  capitalisation rate is wider than **6.83%**.
- Read the other way: selling now is a bet that cap rates widen more than about 58 basis points, or a decision that
  liquidity is worth more than the arithmetic.
- A bid that implies 6.25% or tighter should be taken seriously; that is the "sell into strength" condition.

## 4. What is risk, and how it is bounded

| Risk | Verified evidence | Bound |
|---|---|---|
| Tenant credit | Same-store sales -7.4% Q4, 86 closures, no dividend | Quarterly watch; guaranty and covenants at renewal; sell trigger at two more quarters below -5% |
| Rate / cap-rate expansion | 10-year Treasury 4.84% | Fixed-rate debt if any; sell on a bid, never on a forecast |
| Transfer tax | 0.45% base + 0.0/4.0/5.5% ULA | Price the tier before listing; written opinion on the transaction |
| Operating-cost shock | California fast-food minimum wage $20.00/hour | Rent coverage tested against flat unit sales, not rising ones |
| Hazard | Palisades Fire 2025: 6,845 structures destroyed; ShakeOut Mw 7.8 scenario: $191bn regional loss | Parcel not mapped; confirm FHSZ, fault zone, insurance and lease restoration |
| Vacancy / re-tenanting | No verified market rent for the parcel | Reserve sized to a realistic downtime; renew rather than ride to expiry |

Black-swan events are named, sourced and left unquantified. No probability is invented for this parcel.

## 5. What the owner must supply (all flagged on the site)

Executed lease and amendments; rent ledger and NNN reconciliations; title, survey and parcel record; insurance
policy and quotes; three closed net-lease comparables and two rent comparables; the tenant's or franchisee's
financials; the owner's tax basis and liquidity needs. Until those arrive, every property-specific conclusion is
conditional - which is why the brief publishes ranges and rules instead of a valuation.

## 6. Deliverables

Live dashboard with eleven pages (`index.html`, `demographics.html`, `economy.html`, `schools.html`,
`property.html`, `tenant.html`, `model.html`, `decision.html`, `risks.html`, `flagged.html`, `sources.html`),
a machine-readable dataset (`data/published-records.json`), a deterministic generator (`scripts/build_site.py`),
a 2,952-assertion validation gate (`scripts/validate_site.py`), this summary, `DECISION_MEMO.md`,
`RISK_REGISTER.md`, `METHODOLOGY.md`, and the shared task board (`COORDINATION.md`).

*Analysis for the owner. Not appraisal, legal, tax or investment advice.*
