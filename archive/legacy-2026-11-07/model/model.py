#!/usr/bin/env python3
"""
SP-01 net-lease decision model.

Deterministic. No randomness, no Monte Carlo, no black box. Every number here
traces either to a verified fact in data/facts.json or to a labelled assumption
in data/assumptions.json.

Key structural idea: the owner's stated expiry window (2030-2035) is not one
asset — it is three. A lease with 4 years left and a lease with 9 years left
price differently today, and they resolve differently. The model therefore runs
each strategy against an early / central / late expiry case, and prices the cap
rate off the remaining term rather than assuming a single cap rate.

Run:  python3 model/model.py > data/model.json
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

with open(os.path.join(ROOT, "data", "assumptions.json")) as fh:
    A = json.load(fh)

V = A["verified_inputs"]
HORIZON = A["horizon_years"]      # 9 years: 2026 -> 2035
START = A["start_year"]

NOI_CASES = [140_000, 180_000, 240_000]          # A1
EXPIRY_CASES = [2030, 2032, 2035]                 # owner-stated window
CAP_BAND = 0.0075                                 # A5
ESC = 0.020                                       # A6
MKT_GROWTH = 0.030                                # A7
DISC = 0.0740                                     # A8
SELL_COST = 0.050                                 # A9
TRANSFER_TAX = (V["city_transfer_tax_pct"] + V["county_transfer_tax_pct"]) / 100.0
RETENANT_COST = 150_000                           # A11
FREE_RENT_MONTHS = 6                              # A11
RENEWAL_UPLIFT = 0.10                             # A12
RENEWAL_CONCESSION = 150_000                      # A15
P_RENEW_AT_EXPIRY = 0.60                          # A16
P_RENEW_AT_EXPIRY_BAND = (0.35, 0.75)             # A16 sensitivity band

RISK_FREE = V["risk_free_10y_pct"] / 100.0

# Cap-rate term structure (A2/A3/A4): knots on remaining term in years.
CAP_KNOTS = [(0.0, 0.0725), (3.0, 0.0725), (5.0, 0.0650), (9.0, 0.0600), (15.0, 0.0590)]


def cap_for_term(years):
    """Interpolate the cap rate from remaining lease term. Longer term, lower cap."""
    if years <= CAP_KNOTS[0][0]:
        return CAP_KNOTS[0][1]
    for (x0, y0), (x1, y1) in zip(CAP_KNOTS, CAP_KNOTS[1:]):
        if x0 <= years <= x1:
            return y0 + (y1 - y0) * (years - x0) / (x1 - x0)
    return CAP_KNOTS[-1][1]


def ula_tax(price):
    if price > V["ula_threshold_2026"] and price < V["ulas_upper_threshold"]:
        return price * V["ula_tier1_pct"] / 100.0
    if price >= V["ulas_upper_threshold"]:
        return price * V["ula_tier2_pct"] / 100.0
    return 0.0


def sale_costs(price):
    brokerage = price * SELL_COST
    transfer = price * TRANSFER_TAX
    ula = ula_tax(price)
    return {
        "gross_price": price,
        "brokerage_and_closing": brokerage,
        "transfer_taxes_city_county": transfer,
        "measure_ula": ula,
        "total_costs": brokerage + transfer + ula,
        "net_proceeds": price - brokerage - transfer - ula,
    }


def npv(flows, rate=DISC):
    return sum(amt / ((1 + rate) ** t) for t, amt in flows)


def irr(flows, lo=-0.90, hi=2.0):
    def f(r):
        return sum(amt / ((1 + r) ** t) for t, amt in flows)
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        fm = f(mid)
        if abs(fm) < 1e-7:
            return mid
        if fm * flo < 0:
            hi = mid
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2


def wealth_2035(rows):
    """Reinvest every dollar received at the verified 4.90% Treasury yield until 2035."""
    tot = 0.0
    for row in rows:
        t = row["year"] - START
        tot += row["cash_flow"] * ((1 + RISK_FREE) ** (HORIZON - t))
    return tot


def market_rent(noi0, t):
    return noi0 * ((1 + MKT_GROWTH) ** t)


def inplace_rent(noi0, t):
    return noi0 * ((1 + ESC) ** t)


# ---------------------------------------------------------------------------
# Strategies. Each takes the NOI case, the years remaining on the lease, and the
# net proceeds that selling today would produce (the opportunity cost).
# ---------------------------------------------------------------------------
def s_sell_now(noi0, years_left, v0):
    price = noi0 / cap_for_term(years_left)
    costs = sale_costs(price)
    rows = [{"year": START, "label": "Sale at today's term-appropriate cap", "cash_flow": costs["net_proceeds"]}]
    return {
        "id": "A",
        "name": "Sell now, at the cap the remaining term deserves",
        "rows": rows,
        "gross_price": price,
        "costs": costs,
        "terminal_wealth_2035": wealth_2035(rows),
        "npv": 0.0,
        "irr": RISK_FREE,
        "irr_pct": round(RISK_FREE * 100, 2),
        "is_baseline": True,
        "annual_note": "Baseline. Cash today, no tenant, no lease tail, no re-tenanting risk — but no Prop 13 wedge and no rent either.",
    }


def s_hold_vacate(noi0, years_left, v0):
    """Hold to expiry, tenant leaves, owner pays to refill the box, sell 2035."""
    rows, flows = [], []
    R = min(int(round(years_left)), HORIZON)
    for t in range(1, R + 1):
        cf = inplace_rent(noi0, t)
        rows.append({"year": START + t, "label": "In-place rent", "cash_flow": cf})
        flows.append((t, cf))

    if R < HORIZON:
        free_rent = market_rent(noi0, R + 1) * (FREE_RENT_MONTHS / 12.0)
        vacant_cf = -RETENANT_COST - free_rent
        rows.append({"year": START + R + 1, "label": "Vacant year: re-tenanting cost plus free rent", "cash_flow": vacant_cf})
        flows.append((R + 1, vacant_cf))
        for t in range(R + 2, HORIZON + 1):
            cf = market_rent(noi0, t) * ((1 + ESC) ** (t - R - 2))
            rows.append({"year": START + t, "label": "Re-leased at market rent", "cash_flow": cf})
            flows.append((t, cf))
        terminal_noi = market_rent(noi0, HORIZON) * ((1 + ESC) ** (HORIZON - R - 2))
        term_left = 3.0
    else:
        terminal_noi = inplace_rent(noi0, HORIZON)
        term_left = 0.5

    price = terminal_noi / cap_for_term(term_left)
    costs = sale_costs(price)
    rows.append({"year": START + HORIZON, "label": f"Sale with {term_left:.1f} years of term", "cash_flow": costs["net_proceeds"]})
    flows.append((HORIZON, costs["net_proceeds"]))
    return {
        "id": "B",
        "name": "Hold to expiry, tenant leaves, re-tenant and sell in 2035",
        "rows": rows,
        "gross_price": price,
        "costs": costs,
        "terminal_wealth_2035": wealth_2035(rows),
        "npv": npv([(0, -v0)] + flows),
        "irr": irr([(0, -v0)] + flows),
        "annual_note": "The do-nothing path. Rent stops when the lease stops, the owner pays to refill a drive-thru box in a metro that is losing population, and the asset is then sold with almost no term left.",
    }


def s_hold_renew(noi0, years_left, v0, deterministic=False):
    """Hold to expiry, tenant renews on a 5-year term, sell 2035."""
    rows, flows = [], []
    R = min(int(round(years_left)), HORIZON)
    for t in range(1, R + 1):
        cf = inplace_rent(noi0, t)
        rows.append({"year": START + t, "label": "In-place rent", "cash_flow": cf})
        flows.append((t, cf))

    renewed = market_rent(noi0, R) * (1 + RENEWAL_UPLIFT)
    for t in range(R + 1, HORIZON + 1):
        cf = renewed * ((1 + ESC) ** (t - R - 1))
        rows.append({"year": START + t, "label": "Renewed at market with reset", "cash_flow": cf})
        flows.append((t, cf))
    terminal_noi = renewed * ((1 + ESC) ** (HORIZON - R - 1)) if HORIZON > R else renewed
    price = terminal_noi / cap_for_term(5.0)
    costs = sale_costs(price)
    rows.append({"year": START + HORIZON, "label": "Sale with 5 years of renewed term", "cash_flow": costs["net_proceeds"]})
    flows.append((HORIZON, costs["net_proceeds"]))
    return {
        "id": "C",
        "name": "Hold, tenant renews at expiry, sell in 2035",
        "rows": rows,
        "gross_price": price,
        "costs": costs,
        "terminal_wealth_2035": wealth_2035(rows),
        "npv": npv([(0, -v0)] + flows),
        "irr": irr([(0, -v0)] + flows),
        "annual_note": "Keeps the Prop 13 wedge and defers capital-gains tax, and pays off if the tenant renews. The renewal is not negotiated in this option — it is hoped for, against a franchisor that is closing 50-60 units a year.",
    }


def s_hold_renew_expected(noi0, years_left, v0):
    """Hold to expiry. If the tenant renews (A16) take the C path, otherwise the B path.
    The published NPV is the probability-weighted expectation."""
    c = s_hold_renew(noi0, years_left, v0, deterministic=True)
    b = s_hold_vacate(noi0, years_left, v0)
    p = P_RENEW_AT_EXPIRY
    npv_exp = p * c["npv"] + (1 - p) * b["npv"]
    wealth_exp = p * c["terminal_wealth_2035"] + (1 - p) * b["terminal_wealth_2035"]
    out = dict(c)
    out.update({
        "id": "C",
        "name": "Hold to expiry and renew then — probability-weighted",
        "npv_if_renews": round(c["npv"]),
        "npv_if_leaves": round(b["npv"]),
        "npv": npv_exp,
        "terminal_wealth_2035": wealth_exp,
        "terminal_wealth_if_renews": round(c["terminal_wealth_2035"]),
        "terminal_wealth_if_leaves": round(b["terminal_wealth_2035"]),
        "p_renew": p,
        "p_renew_band": list(P_RENEW_AT_EXPIRY_BAND),
        "irr_pct": None,
        "annual_note": "The 'do nothing and hope' path, priced honestly: a 60% chance the tenant renews, a 40% chance the box goes dark for a year. Published NPV is the weighted average of those two worlds, not the good one.",
    })
    out.pop("irr", None)
    return out


def s_extend_sell_later(noi0, years_left, v0):
    """Negotiate a 10-year extension now, hold to 2031, sell with ~5 years left."""
    rows, flows = [], []
    renewed = noi0 * (1 + RENEWAL_UPLIFT)
    rows.append({"year": START, "label": "Renewal concession (TI / abatement)", "cash_flow": -RENEWAL_CONCESSION})
    flows.append((0, -RENEWAL_CONCESSION))
    sale_offset = 5
    for t in range(1, sale_offset + 1):
        cf = renewed * ((1 + ESC) ** t)
        rows.append({"year": START + t, "label": "Extended-term rent", "cash_flow": cf})
        flows.append((t, cf))
    terminal_noi = renewed * ((1 + ESC) ** (sale_offset + 1))
    price = terminal_noi / cap_for_term(5.0)
    costs = sale_costs(price)
    rows.append({"year": START + sale_offset, "label": "Sale with ~5 years of firm term", "cash_flow": costs["net_proceeds"]})
    flows.append((sale_offset, costs["net_proceeds"]))
    return {
        "id": "E",
        "name": "Extend now on a long term, hold five years, sell with term intact",
        "rows": rows,
        "gross_price": price,
        "costs": costs,
        "terminal_wealth_2035": wealth_2035(rows),
        "npv": npv([(0, -v0)] + flows),
        "irr": irr([(0, -v0)] + flows),
        "annual_note": "The compromise: the term premium is captured while you still own the asset, and the sale happens at the point where the buyer pool is deepest — five years of firm term plus options.",
    }


def s_renew_then_sell(noi0, years_left, v0):
    """Negotiate a 5-year extension now, pay a concession, sell in 2028."""
    rows, flows = [], []
    renewed = noi0 * (1 + RENEWAL_UPLIFT)
    rows.append({"year": START, "label": "Renewal concession (TI / abatement)", "cash_flow": -RENEWAL_CONCESSION})
    flows.append((0, -RENEWAL_CONCESSION))
    for t in range(1, 3):
        cf = renewed * ((1 + ESC) ** t)
        rows.append({"year": START + t, "label": "Extended-term rent", "cash_flow": cf})
        flows.append((t, cf))
    sale_offset = 2
    terminal_noi = renewed * ((1 + ESC) ** (sale_offset + 1))
    term_left_at_sale = 5.0 - sale_offset          # 3 years firm remaining in 2028
    price = terminal_noi / cap_for_term(term_left_at_sale)
    costs = sale_costs(price)
    rows.append({"year": START + sale_offset, "label": f"Sale with {term_left_at_sale:.0f} years firm plus options", "cash_flow": costs["net_proceeds"]})
    flows.append((sale_offset, costs["net_proceeds"]))
    return {
        "id": "D",
        "name": "Renew now, then sell in 2028 while the term is still long",
        "rows": rows,
        "gross_price": price,
        "costs": costs,
        "terminal_wealth_2035": wealth_2035(rows),
        "npv": npv([(0, -v0)] + flows),
        "irr": irr([(0, -v0)] + flows),
        "annual_note": "Same building, same corner, same tenant base. The only thing that changes is the number of years the buyer can count on — and a three-year tail is priced very differently from a four-to-nine-year one.",
    }


def s_renew_hold(noi0, years_left, v0):
    """Renew now for 5 years and hold, selling in 2035 with a short tail."""
    rows, flows = [], []
    renewed = noi0 * (1 + RENEWAL_UPLIFT)
    rows.append({"year": START, "label": "Renewal concession (TI / abatement)", "cash_flow": -RENEWAL_CONCESSION})
    flows.append((0, -RENEWAL_CONCESSION))
    for t in range(1, HORIZON + 1):
        cf = renewed * ((1 + ESC) ** t)
        rows.append({"year": START + t, "label": "Extended-term rent", "cash_flow": cf})
        flows.append((t, cf))
    terminal_noi = renewed * ((1 + ESC) ** HORIZON)
    term_left = 5.0 - HORIZON
    price = terminal_noi / cap_for_term(max(term_left, 0.5))
    costs = sale_costs(price)
    rows.append({"year": START + HORIZON, "label": "Sale with essentially no term left", "cash_flow": costs["net_proceeds"]})
    flows.append((HORIZON, costs["net_proceeds"]))
    return {
        "id": "E",
        "name": "Renew now and hold to 2035, selling into an expired tail",
        "rows": rows,
        "gross_price": price,
        "costs": costs,
        "terminal_wealth_2035": wealth_2035(rows),
        "npv": npv([(0, -v0)] + flows),
        "irr": irr([(0, -v0)] + flows),
        "annual_note": "Signs the renewal and then gives the term away by waiting until it has run out. Captures the tax wedge, hands back the pricing benefit the renewal created.",
    }


STRATS = [s_sell_now, s_hold_vacate, s_hold_renew_expected, s_renew_then_sell, s_extend_sell_later]


def run():
    out = {
        "meta": A["meta"],
        "framing": {
            "baseline": "Selling today at the cap rate the remaining lease term deserves, net of 5.0% cost of sale, 0.56% city+county transfer tax, and Measure ULA where it applies.",
            "npv_meaning": "NPV is measured against that sell-today baseline at a 7.40% required return. Positive means the strategy is worth more than selling now.",
            "wealth_meaning": "Wealth in 2035 reinvests every dollar received at the moment it is received at the verified 4.90% 10-year Treasury yield, so strategies with different cash-flow timing are compared like for like.",
            "term_structure": "Cap rate is a function of remaining lease term, not a single number: 7.25% at <=3 years, 6.50% at 5 years, 6.00% at 9+ years, linearly interpolated between.",
        },
        "verified_inputs": V,
        "assumptions": A["assumptions"],
        "horizon": {"start": START, "end": START + HORIZON, "years": HORIZON},
        "cap_curve": [{"term_years": y, "cap_pct": round(c * 100, 3)} for y, c in CAP_KNOTS],
        "scenarios": [],
    }

    for noi0 in NOI_CASES:
        for expiry in EXPIRY_CASES:
            years_left = expiry - START
            v0 = sale_costs(noi0 / cap_for_term(years_left))["net_proceeds"]
            results = []
            for fn in STRATS:
                r = fn(noi0, years_left, v0)
                r["npv"] = round(r["npv"])
                r["irr_pct"] = round(r["irr"] * 100, 2) if r.get("irr") is not None else None
                r.pop("irr", None)
                r["terminal_wealth_2035"] = round(r["terminal_wealth_2035"])
                r["gross_price"] = round(r["gross_price"])
                for k in ("gross_price", "brokerage_and_closing", "transfer_taxes_city_county",
                          "measure_ula", "total_costs", "net_proceeds"):
                    r["costs"][k] = round(r["costs"][k])
                for row in r["rows"]:
                    row["cash_flow"] = round(row["cash_flow"])
                results.append(r)

            # rate sensitivity on the sell-today leg only
            sens = []
            for shift_bp in (-75, -50, -25, 0, 25, 50, 75):
                cap = cap_for_term(years_left) + shift_bp / 10000.0
                price = noi0 / cap
                sens.append({
                    "shift_bp": shift_bp,
                    "cap_pct": round(cap * 100, 2),
                    "gross_value": round(price),
                    "net_proceeds": round(sale_costs(price)["net_proceeds"]),
                    "ula_applies": ula_tax(price) > 0,
                })

            out["scenarios"].append({
                "id": f"NOI{noi0 // 1000}k-EXP{expiry}",
                "noi": noi0,
                "expiry": expiry,
                "years_left": years_left,
                "cap_today_pct": round(cap_for_term(years_left) * 100, 3),
                "sell_today_net": round(v0),
                "strategies": results,
                "rate_sensitivity": sens,
            })

    # term value table, NOI-independent in percentage terms
    out["term_value"] = [{
        "term_years": y,
        "cap_pct": round(cap_for_term(y) * 100, 2),
        "value_per_100k_noi": round(100_000 / cap_for_term(y)),
        "pct_vs_3yr": round((cap_for_term(3.0) / cap_for_term(y) - 1) * 100, 1),
    } for y in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]

    wedge = ((1 + V["prop13_annual_cap_pct"] / 100) / (1 + MKT_GROWTH)) ** HORIZON
    out["derived"] = {
        "prop13_wedge_ratio": round(wedge, 4),
        "prop13_wedge_pct": round((1 - wedge) * 100, 2),
        "prop13_note": "Verified Proposition 13 caps annual assessed-value growth at 2% (F087) while the model assumes 3% market growth. After 9 years the taxable base sits about 8.4% below what a 3%-growth market implies. That wedge accrues only while the owner holds, and a sale destroys it.",
        "ula_threshold": V["ula_threshold_2026"],
        "ula_at_threshold": round(V["ula_threshold_2026"] * V["ula_tier1_pct"] / 100.0),
        "ula_note": "A sale at $5,399,000 pays no ULA. A sale at $5,400,001 pays about $216,000, because the rate applies to the whole price, not the excess.",
        "sell_cost_pct_pre_ula": round((SELL_COST + TRANSFER_TAX) * 100, 2),
        "term_premium_3_to_9_pct": round((cap_for_term(3.0) / cap_for_term(9.0) - 1) * 100, 1),
        "term_premium_3_to_5_pct": round((cap_for_term(3.0) / cap_for_term(5.0) - 1) * 100, 1),
    }

    # ---- decision matrix ---------------------------------------------------
    criteria = [
        {"key": "risk", "name": "Downside / risk control", "weight": 0.30},
        {"key": "value", "name": "Value and return", "weight": 0.25},
        {"key": "liquidity", "name": "Liquidity and optionality", "weight": 0.15},
        {"key": "tax", "name": "Tax efficiency", "weight": 0.15},
        {"key": "growth", "name": "Growth potential", "weight": 0.10},
        {"key": "simple", "name": "Execution burden (higher = simpler)", "weight": 0.05},
    ]
    scores = {
        "A": {"risk": 5, "value": 2, "liquidity": 5, "tax": 1, "growth": 1, "simple": 5,
              "why": "Deletes single-asset and single-tenant concentration in one transaction and prices in the short remaining term. But it sells the same NOI at the short-lease cap, crystallises capital-gains tax unless a 1031 is executed inside the IRS 45/180-day windows, and forfeits the Prop 13 wedge. Financially the weakest of the sensible options; operationally the cleanest."},
        "B": {"risk": 1, "value": 3, "liquidity": 2, "tax": 4, "growth": 2, "simple": 4,
              "why": "Combines the tenant's contraction risk with a 12-month vacancy and a re-tenanting bill, then sells the asset just after the market watched it go dark. In the 2032 and 2035 expiry cases this path destroys value even before risk is considered."},
        "C": {"risk": 2, "value": 5, "liquidity": 2, "tax": 5, "growth": 4, "simple": 5,
              "why": "Highest expected NPV in two of three expiry cases and keeps the Prop 13 wedge, but the owner spends four to nine more years exposed to a franchisor that is closing 50-60 units a year with no term secured. Roughly a 40% chance of absorbing a vacant year plus a re-tenanting bill. Requires no action, which is exactly the problem."},
        "D": {"risk": 3, "value": 2, "liquidity": 4, "tax": 3, "growth": 2, "simple": 3,
              "why": "Secures the term, then exits almost immediately and gives up the rent stream that the extension was supposed to protect. Only wins when the lease has a very short tail (the 2030 case); negative NPV in the 2032 and 2035 cases."},
        "E": {"risk": 4, "value": 5, "liquidity": 4, "tax": 4, "growth": 4, "simple": 3,
              "why": "Negotiates the extension now, so the tenant tail is resolved while the owner still has leverage; holds five more years to keep rent and the Prop 13 wedge; then sells with five years of firm term into the deepest part of the buyer pool. Positive NPV in all three expiry cases and the best risk-adjusted result."},
    }
    matrix = []
    for sid in ["A", "B", "C", "D", "E"]:
        weighted = sum(scores[sid][c["key"]] * c["weight"] for c in criteria)
        matrix.append({
            "id": sid,
            "scores": {c["key"]: scores[sid][c["key"]] for c in criteria},
            "weighted_score": round(weighted, 2),
            "why": scores[sid]["why"],
        })
    matrix.sort(key=lambda m: -m["weighted_score"])
    out["decision"] = {
        "criteria": criteria,
        "matrix": matrix,
        "ranking": [m["id"] for m in matrix],
        "note": "Scores are analyst judgement against the verified evidence, not a statistical estimate. Weights and every cell are published so a reader can reject a specific judgement rather than the whole conclusion.",
    }
    return out


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
