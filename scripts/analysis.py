#!/usr/bin/env python3
"""Risk register, decision paths and the projection/scenario model.

Everything numeric here is either a referenced verified figure from dataset.py or an
explicit, stated assumption. Assumption-driven outputs are labelled "model" and are
never presented as observed data. The model's job is to show the *shape* of the
trade-off and which input would have to move to change the answer — not to price the asset.
"""

# --------------------------------------------------------------------------- risk register
# id, title, class, triggers, exposure mechanics, mitigants, so_what, residual
RISKS = [
    (
        "R-01", "Tenant walks at expiry instead of renewing", "Business as usual",
        "Guided 50-100 closures in FY2026 (T-11); FY2025 same-store sales -4.2% (T-06) and -7.4% in Q4 (T-07).",
        "A dark box on a drive-thru parcel reverts to landlord: property tax, insurance, security, and a re-letting "
        "period. The prototype is only 1,372 sq ft (T-20), so the building is not the value - the land and the "
        "conditional-use entitlement for a drive-thru are.",
        "Start renewal dialogue 24-30 months before expiry, not 6. Confirm in writing whether the tenant holds "
        "options (PR-10). Have a re-use plan for the parcel: another QSR, a conversion, or redevelopment.",
        "This is the highest-probability adverse outcome and the one the owner can actually influence. It is a "
        "negotiation and timing risk, not a market risk.",
        "Medium probability; high severity if no fallback use exists",
    ),
    (
        "R-02", "Renewal is agreed but at a lower rent than today", "Business as usual",
        "Brand-level sales decline (T-06, T-07); the tenant's stated plan includes selling real estate (T-25).",
        "The landlord keeps occupancy and loses income. In a flat-to-declining population county (J-05, J-06) the "
        "tenant has credible alternatives, so the negotiating asymmetry favours the tenant.",
        "Model a renewal at a 0 to -15% rent reset and check the after-tax hold value still beats the sale. "
        "Ask for term length and credit (guaranty) rather than headline rent.",
        "A renewal is not automatically a win. A long renewal at a weak rent with no guaranty may be worse than "
        "a sale to a 1031 buyer who values the remaining term.",
        "Medium probability; medium severity",
    ),
    (
        "R-03", "The counterparty is the franchisee, not the brand", "Business as usual",
        "The 10-K states the company leases or subleases to the franchisee for a majority of franchised sites (T-04).",
        "Landlord credit is the operator's balance sheet, not a national brand's. A single-unit or small multi-unit "
        "franchisee can fail while the brand is healthy, and the brand is not obliged to keep the site open.",
        "Read the actual lease and any guaranty before any decision (PR-03, T-27). If there is no brand guaranty, "
        "underwrite the operator as an independent small business.",
        "This single unknown changes the risk class of the whole asset, which is why it is flagged as F-11.",
        "Unknown probability - must be resolved first",
    ),
    (
        "R-04", "Sale proceeds are eroded by transfer tax and tax on gain", "Business as usual",
        "Measure ULA 4.0%/5.5% plus a 0.45% city base tax (X-01 to X-07); federal and state tax on gain depends on basis (PR-22, X-13).",
        "Net proceeds, not gross price, is what the owner can redeploy. On a $6.5m sale the city-level transfer tax "
        "alone is 4.45% - and the thresholds are CPI-indexed every year, so the arithmetic changes.",
        "Compute the after-tax, after-cost number before any letter of intent. If the intent is to stay invested in "
        "real estate, test a §1031 exchange; if not, the tax is simply a cost of exiting.",
        "An owner who compares a sale price to a hold value without deducting 4.45%-5.95% plus income tax will "
        "overstate the sell case by a wide margin.",
        "High probability of occurring if a sale happens; severity set by basis",
    ),
    (
        "R-05", "Insurance cost or availability deteriorates", "Business as usual",
        "The Department of Insurance describes insurers withdrawing from areas as FAIR Plan enrolment grows (Z-13).",
        "Under a true NNN lease the tenant pays premiums, so the landlord is insulated while the lease runs. After "
        "expiry the landlord carries it - and an uninsurable parcel is a hard stop for most buyers and lenders.",
        "Obtain a current quote now, before deciding. Ask the tenant for the existing policy declarations. Confirm "
        "whether the lease obliges the tenant to insure and what happens if it cannot.",
        "Insurance is the quietest way a central-LA commercial parcel loses value: not through damage, but through "
        "the loss of a market.",
        "Medium probability; high severity if the parcel is in a mapped hazard zone",
    ),
    (
        "R-06", "Interest rates stay high or rise, compressing the sale multiple", "Business as usual",
        "10-year Treasury at 4.84% (C-01), up from the 2020-2021 range; no official cap-rate series exists for this asset (C-03).",
        "A buyer's required return moves with the risk-free rate. Every 100 bp of cap-rate expansion on a fixed rent "
        "stream is roughly a 15-20% value change at typical net-lease spreads.",
        "Rate the decision on cash flow and optionality rather than on a hoped-for multiple. If a sale is the goal, "
        "do not wait for a rate environment that may not return.",
        "Higher-for-longer is the base case the official data supports. A hold decision should not depend on "
        "cap-rate compression.",
        "Medium probability; medium-to-high severity",
    ),
    (
        "R-07", "Population and household decline in the county", "Business as usual",
        "County population -3.2% since 2020 (D-04); DOF projects a further -1.47% to 2035 (J-06); the state grows +2.23% over the same period (J-09).",
        "Fewer residents is fewer transactions at the counter. Restaurants absorb this through price and hours "
        "before they close, so it reaches the landlord as weaker renewal terms rather than immediately as vacancy.",
        "Weight the decision toward the durability of the location and the parcel's alternative use rather than "
        "toward county population growth, which is negative on the official baseline.",
        "This is the clearest official signal in the dataset that the area is not a growth market for a "
        "volume-driven restaurant.",
        "High probability of continuation; medium severity",
    ),
    (
        "R-08", "Operating-cost regulation squeezes the operator's margin", "Business as usual",
        "California fast-food minimum wage $20.00/hour since April 2024 (X-11), with a statutory council able to raise it; local minimum wages on top.",
        "The operator's rent-paying capacity is a residual after labour. A wage floor that rises faster than menu "
        "prices (menu inflation 2.8%, P-04) compresses that residual.",
        "Underwrite rent-to-sales at the operator level, not the brand level. Check which city minimum wage applies (X-12, unverified).",
        "Regulation here is a slow, persistent margin tax on the tenant, and therefore on the rent the landlord can negotiate.",
        "Medium probability; medium severity",
    ),
    (
        "R-09", "Property tax step-up on sale", "Business as usual",
        "Proposition 13 caps assessment growth at 2%/year and resets at a change of ownership (X-09).",
        "A sale transfers the low Prop 13 basis to the buyer, who must re-underwrite a higher tax bill. That "
        "reduces what a buyer will pay. A hold keeps the low basis.",
        "Quantify the buyer's post-sale tax step-up in the sale case; quantify the landlord's protected basis in the "
        "hold case. Where the basis is very low, holding has a real, measurable advantage.",
        "Prop 13 is one of the few structural reasons a long hold can beat a sale regardless of price.",
        "Certain if a sale occurs; severity set by the gap between basis and market value",
    ),
    (
        "R-10", "Wildfire: a regional event repricing the insurance market", "Black swan",
        "The January 2025 Palisades Fire destroyed 6,845 structures, damaged 975 and killed 12 (Z-01 to Z-05).",
        "A central-LA drive-thru box is not in the wildland-urban interface, so direct destruction risk is low. The "
        "real channel is secondary: after a major fire, insurers reprice and withdraw across the whole region, and "
        "the FAIR Plan grows (Z-13). Reinsurance and construction costs rise region-wide.",
        "Separate the two questions: (a) will this parcel burn, (b) will this parcel stay insurable and financeable "
        "after the region burns. (b) is the material one and it is not parcel-specific.",
        "The correct framing is insurance-market contagion, not ember exposure. Do not assign a burn probability to "
        "the parcel; do stress the post-event cost of cover.",
        "Low probability of direct damage; medium probability of a regional repricing event within a 10-year hold",
    ),
    (
        "R-11", "Earthquake: shaking, liquefaction or fault rupture", "Black swan",
        "USGS/CGS ShakeOut scenario models 1,800 deaths and $191bn of economic loss for an Mw 7.8 San Andreas event (Z-09, Z-10).",
        "Central Los Angeles sits in a basin with strong shaking amplification. CGS maps liquefaction and landslide "
        "zones, and Alquist-Priolo fault zones impose a 50-foot setback (Z-08). A single-storey box is more "
        "resilient than mid-rise, but a closed store, a red-tagged parcel and a business-interruption gap still hit "
        "rent collection.",
        "Query the CGS EQ Zapp and the Alquist-Priolo maps for the parcel (Z-15, F-21). Confirm the lease allocates "
        "repair obligation and whether rent abates on damage. Consider earthquake cover and its deductible.",
        "A 1,372 sq ft single-storey building is the favourable end of the exposure. The lease's damage and "
        "abatement language matters more than the building's structural risk.",
        "Low annual probability; high severity when it happens",
    ),
    (
        "R-12", "Flood and extreme heat", "Black swan",
        "Los Angeles County heat and flood exposure is mapped by FEMA and the County; the parcel-level result is not verified here (Z-16).",
        "Flood damages the box and the parking field and interrupts trade. Heat raises refrigeration and HVAC cost "
        "and suppresses midday foot traffic - relevant because a drive-thru's peak is lunch.",
        "Check the FEMA flood map and the County flood control viewer for the parcel. Confirm tenant obligation for "
        "HVAC replacement.",
        "Heat is the under-modelled risk for a drive-thru: it attacks the lunch daypart and the equipment "
        "simultaneously.",
        "Medium probability of heat events; low-to-medium severity for a single-storey box",
    ),
    (
        "R-13", "Civil unrest, crime or a localised demand shock", "Black swan",
        "No official parcel-level crime or unrest series was verified for this site; the general Los Angeles context is cited on the market page.",
        "A single-event shock can close a store for weeks and accelerate a closure decision that was already "
        "pending. For a tenant already closing 50-100 units a year, a shock can be the trigger.",
        "Confirm the lease's rent-abatement and casualty provisions. Confirm business-interruption cover belongs to "
        "the tenant, as it normally does under NNN.",
        "For a tenant in contraction, the black swan does not need to be large - it only needs to coincide with a "
        "closure list.",
        "Low probability; medium severity",
    ),
    (
        "R-14", "Regional economic recession", "Black swan",
        "Restaurant demand is discretionary. The tenant's own 10-K names consumer confidence and food-away-from-home "
        "spending as drivers of its results (T-06, sec10K risk factors).",
        "A recession hits same-store sales, then franchisee profitability, then rent-paying capacity, then renewal "
        "terms. Under NNN the landlord's cash flow is contractual and therefore lags the shock by the lease term.",
        "The lease term is the hedge. This is precisely the argument for a renewal: contractual rent through a "
        "downturn is worth more than a mark-to-market sale at the bottom.",
        "A recession argues for term, not for selling into weakness.",
        "Medium probability within a 10-year horizon; medium severity while a lease is in place",
    ),
    (
        "R-15", "Policy shock: new rent, transfer or business taxes", "Black swan",
        "Measure ULA itself is the precedent: a city-level transfer tax introduced in 2023 and indexed since (X-01 to X-08).",
        "The measure that taxed this asset class once can be extended. A higher transfer tax directly reduces net "
        "sale proceeds; a new commercial rent tax would hit the income stream.",
        "Nothing mitigates a future tax except timing and structure. Note that a sale now is taxed under known "
        "rules; a sale in 2033 is taxed under unknown ones.",
        "Policy risk cuts both ways and is not a reason to delay by itself - but it does argue against an "
        "open-ended hold with no exit plan.",
        "Low-to-medium probability; medium severity",
    ),
    (
        "R-16", "The owner's own liquidity, estate or concentration need", "Personal",
        "Not observable and not requested. No personal financial information is collected or published.",
        "This is the factor that most often overrides a pure asset analysis: a need for cash, an estate event, a "
        "portfolio that is too concentrated in one tenant, or a desire to stop being a landlord.",
        "Decide this first, privately. If liquidity is needed inside 36 months, the sale case dominates regardless "
        "of the market view.",
        "The asset analysis can tell the owner which path is better for the asset. Only the owner can say which "
        "path is better for the owner.",
        "Owner-specific",
    ),
]

# --------------------------------------------------------------------------- decision paths
# Path metadata only. All numbers in the site come from the computed model below.
PATHS = [
    {
        "id": "sell-now",
        "name": "Sell now, with the lease in place",
        "summary": "Market the property today as a leased NNN asset with roughly 4 to 9 years of remaining term.",
        "keeps": "Liquidity and the ability to redeploy into a diversified or higher-yielding asset; removes "
                 "single-tenant and single-parcel concentration immediately.",
        "gives_up": "The remaining contractual rent, the low Proposition 13 basis, and any option value in a "
                    "renewal at better terms. Also crystallises the gain.",
        "costs": "City transfer tax of 4.45% or 5.95% of price depending on the band, plus brokerage, legal, "
                 "loan payoff and defeasance, plus federal and California income tax on the gain.",
        "best_if": "The owner needs liquidity or diversification; the basis is high; the remaining term is short "
                   "enough that buyers price it as a re-tenanting play; or the parcel's alternative use is more "
                   "valuable than its restaurant use.",
        "fails_if": "The sale is priced off a cap rate that assumes a long lease the asset does not have, or the "
                    "owner has not quantified the transfer tax and the gain.",
        "verify_first": ["PR-22", "PR-21", "PR-09", "PR-10", "C-04", "X-03"],
    },
    {
        "id": "renew-hold",
        "name": "Renew, then decide later",
        "summary": "Negotiate an extension now, at a known rent, with the option to sell the re-rated asset in a "
                   "later, calmer market.",
        "keeps": "The income stream, the Prop 13 basis, and the ability to sell a longer-lease asset later at a "
                 "tighter cap rate. Converts an expiring asset into a saleable one.",
        "gives_up": "Negotiating leverage at expiry, and some rent - a tenant extending early will want a "
                    "concession. Locks in a tenant whose brand is contracting.",
        "costs": "Leasing commissions and legal fees; possibly a rent reset; possibly landlord-funded capital "
                 "(roof, HVAC, drive-thru lane resurfacing) to get the extension signed.",
        "best_if": "The tenant will sign 10+ years with a creditworthy guaranty at a rent that still clears the "
                   "after-tax sale proceeds; the parcel's highest and best use is likely to be restaurant for "
                   "another decade; the owner does not need liquidity.",
        "fails_if": "The extension is signed at a weak rent with a franchisee-only guaranty, or the owner is "
                    "forced to sell the newly extended asset into the same weak market anyway.",
        "verify_first": ["T-27", "PR-10", "PR-09", "PR-08", "PR-15", "PR-19"],
    },
    {
        "id": "hold-expiry",
        "name": "Hold to expiry and re-tenant or redevelop",
        "summary": "Collect rent to expiry, then act on the parcel with no tenant constraint.",
        "keeps": "Maximum flexibility at the end and no negotiation with a contracting tenant. Preserves the option "
                 "to redevelop if the zoning supports it.",
        "gives_up": "Rent between expiry and re-letting. In a county losing population (J-06), the re-letting "
                    "period is the main risk, and drive-thru entitlements are the scarce asset, not the building.",
        "costs": "Carrying costs while dark (tax, insurance, security), tenant-improvement allowance for a new "
                 "operator, and possibly a new conditional-use permit or a change of use.",
        "best_if": "The parcel has a higher-value alternative use or the site is strong enough that multiple "
                   "operators would compete for it at expiry.",
        "fails_if": "The parcel is a marginal drive-thru box with no alternative use, and the market at expiry is "
                    "the same or worse.",
        "verify_first": ["PR-15", "PR-11", "PR-12", "PR-13", "PR-19"],
    },
    {
        "id": "exchange",
        "name": "Sell and exchange under IRC §1031",
        "summary": "Sell, and defer the federal gain by buying qualifying replacement real property.",
        "keeps": "Capital in real estate, with the gain deferred rather than taxed. Diversifies out of one tenant "
                 "and one parcel without a tax bill on exit.",
        "gives_up": "Control over timing and choice - the exchange requires identifying and closing on replacement "
                    "property inside statutory windows. California does not conform to all federal deferral "
                    "mechanics for state purposes in every case; that needs a tax adviser.",
        "costs": "Qualified intermediary fees, tighter deadlines, and the risk of overpaying for replacement "
                 "property under time pressure.",
        "best_if": "The basis is low, the owner wants to stay in real estate, and a suitable replacement can be "
                   "identified before the sale.",
        "fails_if": "The owner needs cash, or buys a worse asset under deadline pressure.",
        "verify_first": ["PR-22", "X-13", "X-15"],
    },
]

# --------------------------------------------------------------------------- assumptions
# Named, explicit, and each one is a lever the reader can see. None of these is a fact.
ASSUMPTIONS = [
    ("A-01", "Holding period used to compare hold versus sell", "9 years (to 2035, the outer end of the stated expiry window)",
     "Compares the two paths over the longest possible remaining term. A shorter term shortens the hold case's advantage."),
    ("A-02", "Rent growth at renewal", "0% to +10% in equal steps",
     "Fixed bumps are typical but the actual structure is unknown (PR-09). The range spans a flat renewal to a modest increase."),
    ("A-03", "Discount rate applied to the rent stream", "6%, 7%, 8%",
     "A sensitivity band around a risk-free rate of 4.84% (C-01) plus a net-lease risk premium. These are illustrative rates, not a market quote."),
    ("A-04", "Residual value at the end of the holding period", "15 times the then-current rent",
     "A 6.67% exit cap as a round proxy. This is the single most influential assumption in the model and it is an assumption, not a verified cap rate."),
    ("A-05", "Illustrative rent base", "100 units of index",
     "The model runs in index units, not dollars, because no rent was disclosed (PR-08). Every output is therefore a ratio, which is valid for comparing paths and invalid as a valuation."),
    ("A-06", "Transfer tax on sale", "4.45% of price (lower ULA band, X-06)",
     "Chosen because a central-LA drive-thru parcel most plausibly trades in the $5.4m-$10.9m band. If it trades below $5.4m the rate is 0.45%; if above $10.9m it is 5.95%."),
    ("A-08", "Selling commission", "4% of price",
     "An assumed transaction cost, not a market quote. It is added to the published transfer tax to reach net proceeds."),
    ("A-07", "Binary event probabilities", "Not assigned",
     "The brief deliberately assigns no probability to wildfire, earthquake, flood or recession for this parcel. Assigning one would require data that does not exist at parcel level, and any number would be fabricated."),
]

# --------------------------------------------------------------------------- model
def hold_value(rent_base, annual_growth, discount_rate, residual_multiple, years):
    """Present value of an indexed rent stream plus a residual multiple at exit.

    rent_base is in index units. Returns the present value in the same units.
    """
    pv = 0.0
    flow = rent_base
    for year in range(1, years + 1):
        flow = rent_base * ((1 + annual_growth) ** (year - 1))
        pv += flow / ((1 + discount_rate) ** year)
    residual = (rent_base * ((1 + annual_growth) ** (years - 1))) * residual_multiple
    pv += residual / ((1 + discount_rate) ** years)
    return pv


def build_model():
    years = 9
    growths = [0.0, 0.05, 0.10]
    rates = [0.06, 0.07, 0.08]
    residual = 15.0
    rent_base = 100.0

    grid = []
    for growth in growths:
        row = {"growth": growth, "values": {}}
        for rate in rates:
            row["values"][rate] = hold_value(rent_base, growth, rate, residual, years)
        grid.append(row)

    # One year of rent = 100 index units. A sale today is priced at gross_multiple years of
    # today's rent (a cap rate of 1/gross_multiple). Net proceeds deduct the city transfer
    # tax and an assumed selling commission.
    transfer_tax = 0.0445      # combined LA rate, lower ULA band (X-06)
    commission = 0.04          # assumed, stated in A-08
    gross_multiple = residual
    net_multiple = gross_multiple * (1 - transfer_tax - commission)

    base_rate = 0.07
    base_growth = 0.05
    pv_with_residual = hold_value(rent_base, base_growth, base_rate, residual, years)
    pv_no_residual = hold_value(rent_base, base_growth, base_rate, 0.0, years)
    residual_share = (pv_with_residual - pv_no_residual) / pv_with_residual

    # The hold case's present value expressed as a multiple of one year of rent.
    hold_multiple = pv_with_residual / rent_base

    # Break-even residual multiple: the exit multiple in 2035 at which the hold case's
    # present value equals the net proceeds of selling today. Solved by bisection so the
    # relationship is explicit rather than asserted.
    # Units: hold_value returns index units where one year of rent = rent_base (100).
    # Net proceeds must therefore be expressed in the same units before comparing.
    net_proceeds_units = net_multiple * rent_base

    def pv_at(mult):
        return hold_value(rent_base, base_growth, base_rate, mult, years)

    lo, hi = 0.0, 60.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if pv_at(mid) < net_proceeds_units:
            lo = mid
        else:
            hi = mid
    break_even_multiple = (lo + hi) / 2


    return {
        "years": years,
        "growths": growths,
        "rates": rates,
        "residual_multiple": residual,
        "rent_base": rent_base,
        "grid": grid,
        "base_rate": base_rate,
        "base_growth": base_growth,
        "pv_with_residual": pv_with_residual,
        "pv_no_residual": pv_no_residual,
        "residual_share": residual_share,
        "transfer_tax": transfer_tax,
        "commission": commission,
        "gross_multiple": gross_multiple,
        "net_multiple": net_multiple,
        "hold_multiple": hold_multiple,
        "break_even_multiple": break_even_multiple,
        "net_proceeds_units": net_proceeds_units,
        "hold_advantage": pv_with_residual / net_proceeds_units,
    }


# --------------------------------------------------------------------------- projection system
# How each category is projected, and with what confidence. No number is invented here.
PROJECTION_METHOD = [
    ("Population", "Official projection, used as published",
     "DOF P-2A Baseline 2024 / Vintage 2026 county series (J-01 to J-07).",
     "High for the county; none for the trade area. The county series is the state's own demographic baseline."),
    ("State context", "Official projection, used as published",
     "DOF P-2A California series (J-08, J-09).",
     "High. Establishes that the county is diverging from the state, not tracking it."),
    ("Employment", "Current level and 12-month momentum only; no projection",
     "BLS CES via Economy at a Glance (E-05 to E-16).",
     "Medium for the current reading (preliminary data), none for a forecast. No official MSA employment projection was located, so none is published."),
    ("Prices", "Current 12-month change only; no projection",
     "BLS CPI Los Angeles (P-01 to P-07).",
     "Medium. Area indexes are volatile and BLS says they do not measure price-level differences between cities."),
    ("Income", "Current level only; no projection",
     "Census ACS 5-year and SAIPE via FRED (I-01 to I-06).",
     "High for the published year; none for a forecast. No official household income projection exists at this geography."),
    ("Housing and construction", "Current level only",
     "Census QuickFacts and the State EDD profile (H-01 to H-11).",
     "Medium. Two official 2025 permit counts conflict (F-06), and both are shown."),
    ("Schools", "Current district metrics only",
     "NCES CCD (S-01 to S-09).",
     "High for district aggregates; none for the campus, which is not identified."),
    ("Tenant", "Reported results plus company guidance",
     "SEC 10-K and Q4 FY2025 release (T-01 to T-25).",
     "High for what was filed; guidance is management's own forward-looking statement, not a forecast this brief endorses."),
    ("Hazards", "Realised severity references and open parcel checks",
     "CAL FIRE, OSFM, CGS, USGS, CDI (Z-01 to Z-17).",
     "High for the published event and scenario figures; none for the parcel. No probability is assigned."),
    ("Capital markets", "Current risk-free rate only",
     "FRED DGS10 (C-01, C-02).",
     "High for the yield; none for a cap rate, which is not published officially at asset level."),
]
