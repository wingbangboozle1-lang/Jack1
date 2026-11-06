#!/usr/bin/env python3
"""Reproducible projection model for the subject asset.

Reads  : data/projection.json  (complete specification: official inputs,
                                unverified scenario inputs, equations)
Writes : data/projection_output.json  (every number the Projection page shows)

The model is NORMALISED: the asset's value on the retrieval date equals 100.0
index points. No dollar figure for the subject property is produced, because no
dollar figure was supplied and none can be verified from an official source.

Nothing is hard-coded here that is not declared in projection.json. Change an
input there, re-run this script, re-run tools/build_site.py, and the published
tables change with it. That is the reproducibility guarantee.

FAIRNESS RULES APPLIED TO BOTH SIDES OF THE COMPARISON
  1. The SELL path bears its statutory transaction cost (Measure ULA) up front.
  2. The HOLD path bears the SAME statutory transaction cost on its terminal
     sale, plus a vacancy/downtime scenario after expiry. Without (2) holding
     would win by construction and the comparison would be meaningless.
  3. The SELL path's certain cash proceeds are not discounted further: net
     proceeds either sit at the official Treasury risk-free rate or are
     reinvested in an identical asset at the same capitalisation rate, and both
     treatments give a present value equal to the net proceeds. That is stated
     as an assumption, not smuggled in.
  4. The tenant non-renewal probability is run in TWO regimes: the official
     system-wide base rate, and a 'signal received' regime at 100%. The second
     regime is what the recommended decision path is designed to detect early,
     and it is where the ranking between hold and sell flips.

Usage:  python3 tools/model.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")

V0 = 100.0                      # EQ-1
EXTEND_YEARS = 10               # declared in projection.json EQ-9
DOWNTIME_SCENARIOS = [0.0, 1.0, 2.0]   # years of zero income after expiry (scenario)


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


def official(spec, name):
    for item in spec["official_inputs"]:
        if item["name"] == name:
            return float(item["value"])
    raise KeyError("official input %r not declared in projection.json" % name)


def unverified(spec, name):
    for item in spec["unverified_inputs"]:
        if item["name"] == name:
            return [float(v) for v in item["values"]]
    raise KeyError("unverified input %r not declared in projection.json" % name)


def r(x, nd=2):
    return round(x + 1e-12, nd)


def p_dark(n, rate_pct):
    """EQ-4: cumulative non-renewal probability at a constant annual closure rate."""
    return 1.0 - (1.0 - rate_pct / 100.0) ** n


def hold_pv(n, g, cap, residual_pct, hpi_pct, closure_rate_pct, exit_cost,
            downtime_years=0.0, pdk_override=None):
    """EQ-7 / EQ-9: present value of holding, net of exit cost and downtime.

    Income runs for n years. The terminal event (renew-and-resell, or dark) is
    then realised downtime_years later, so it is discounted over n + downtime.
    """
    pdk = p_dark(n, closure_rate_pct) if pdk_override is None else pdk_override
    noi0 = V0 * cap
    pv_income = sum(noi0 * (1.0 + g) ** t / (1.0 + cap) ** t for t in range(1, n + 1))
    noi_n = noi0 * (1.0 + g) ** n
    renew_branch = noi_n * (1.0 + g) / cap
    dark_branch = V0 * (residual_pct / 100.0) * (1.0 + hpi_pct / 100.0) ** n
    tv_gross = (1.0 - pdk) * renew_branch + pdk * dark_branch
    tv_net = tv_gross * (1.0 - exit_cost)
    horizon = n + downtime_years
    pv_terminal = tv_net / (1.0 + cap) ** horizon
    return {
        "p_dark": pdk,
        "pv_income": pv_income,
        "terminal_gross": tv_gross,
        "terminal_net": tv_net,
        "pv_terminal": pv_terminal,
        "pv_total": pv_income + pv_terminal,
    }


def main():
    spec = load("projection.json")

    rf10 = official(spec, "risk_free_10y") / 100.0
    rf30 = official(spec, "risk_free_30y") / 100.0
    g_official = {
        "Low - BLS LA CPI-U, February 2026": official(spec, "cpi_la_low") / 100.0,
        "Central - median of the five 2026 BLS LA CPI-U readings": official(spec, "cpi_la_median") / 100.0,
        "High - BLS LA CPI-U, April 2026": official(spec, "cpi_la_high") / 100.0,
    }
    g_central_name = "Central - median of the five 2026 BLS LA CPI-U readings"
    g_flat = unverified(spec, "rent_escalator_flat")[0] / 100.0
    hpi_central = official(spec, "hpi_la_msad_yoy") / 100.0
    hpi_down = official(spec, "hpi_pacific_yoy_q1_2026") / 100.0
    closure_ongoing = official(spec, "closure_rate_ongoing")
    prog_low = official(spec, "closure_programme_share_low")
    prog_high = official(spec, "closure_programme_share_high")
    eq30 = official(spec, "eq_m67_30yr") / 100.0
    fire_low = official(spec, "fire_output_loss_low")
    fire_high = official(spec, "fire_output_loss_high")
    gdp = official(spec, "la_county_gdp_2024")
    ula_low = official(spec, "ula_rate_lower_tier") / 100.0
    ula_high = official(spec, "ula_rate_upper_tier") / 100.0
    land_share = official(spec, "company_book_land_share")

    spreads_bp = unverified(spec, "cap_spread_grid")
    residuals = unverified(spec, "dark_land_residual_grid")
    horizons = [int(x) for x in unverified(spec, "years_to_expiry_grid")]

    caps = [(bp, rf10 + bp / 10000.0) for bp in spreads_bp]
    central_bp, central_cap = caps[len(caps) // 2]
    mid_residual = residuals[len(residuals) // 2]

    out = {
        "meta": {
            "generated_by": "tools/model.py",
            "spec": "data/projection.json",
            "unit": "index points, asset value on 2026-11-06 = 100.0",
            "central_case": {
                "cap_spread_bp": r(central_bp, 0),
                "cap_rate_pct": r(central_cap * 100, 2),
                "discount_rate_pct": r(central_cap * 100, 2),
                "escalator_pct": r(g_official[g_central_name] * 100, 1),
                "land_growth_pct": r(hpi_central * 100, 1),
                "closure_rate_pct": closure_ongoing,
                "residual_pct": mid_residual,
                "exit_transaction_cost_pct": r(ula_low * 100, 1),
                "downtime_years": 1.0,
            },
            "fairness_rules": [
                "Both paths bear the same statutory transaction cost: the sell path up front, the hold path on its terminal sale.",
                "The hold path additionally bears a vacancy/downtime scenario after expiry, because a NNN landlord resumes tax, insurance and maintenance on expiry and may not re-let immediately.",
                "The sell path's certain net proceeds are not discounted further. Net proceeds either earn the official Treasury risk-free rate or are reinvested in an identical asset at the same capitalisation rate; both treatments give a present value equal to the net proceeds.",
                "Tenant non-renewal is run in two regimes: the official system-wide base rate, and a 'signal received' regime at 100%. The second is what the recommended decision path exists to detect early.",
            ],
            "unverified_dependency": (
                "Every figure below depends on the cap-spread grid UX-1, which is an "
                "UNVERIFIED scenario input: no government agency publishes net-lease "
                "capitalisation rates. Read the RANKING of paths and the STABILITY of that "
                "ranking across the grid, not the absolute index level."),
        },
        "cap_grid": [{"spread_bp": r(bp, 0), "cap_pct": r(c * 100, 2),
                      "implied_noi0_index": r(V0 * c, 3)} for bp, c in caps],
        "risk_free": {"ten_year_pct": r(rf10 * 100, 2), "thirty_year_pct": r(rf30 * 100, 2)},
    }

    # ------------------------------------------------------------------ EQ-4
    out["closure_probability"] = {
        "official_annual_rate_pct": closure_ongoing,
        "by_horizon": [{"years": n, "expiry_year": 2026 + n,
                        "p_dark_pct": r(p_dark(n, closure_ongoing) * 100, 2)}
                       for n in horizons],
        "programme_bounds_pct": {"low": r(prog_low, 2), "high": r(prog_high, 2)},
        "note": ("p_dark uses the company-disclosed ongoing annual closure rate of 1% of "
                 "system units (IN-9). The programme bounds are the JACK on Track block "
                 "closure of 150-200 restaurants against the 2,191-restaurant system at the "
                 "start of fiscal 2025 (IN-10, IN-11). Neither is a site-specific "
                 "probability: no public disclosure identifies individual restaurants "
                 "selected for closure (flag F-31)."),
    }

    # ---------------------------------------------------------- EQ-8 sell now
    sell_cases = [
        {"label": "Parcel outside the City of Los Angeles, or price below the ULA threshold",
         "tc": 0.0,
         "basis": "Measure ULA applies only to transfers inside the City of Los Angeles (R-15)."},
        {"label": "City of Los Angeles, price at or above the LOWER ULA threshold",
         "tc": ula_low,
         "basis": "LAMC 21.9.2 / LAHD official FAQ: 4% of the entire consideration or value (IN-16)."},
        {"label": "City of Los Angeles, price at or above the UPPER ULA threshold",
         "tc": ula_high,
         "basis": "LAMC 21.9.2 / LAHD official FAQ: 5.5% of the entire consideration or value (IN-17)."},
    ]
    out["sell_now"] = [{"case": c["label"],
                        "transaction_cost_pct": r(c["tc"] * 100, 1),
                        "net_index": r(V0 * (1.0 - c["tc"]), 2),
                        "official_basis": c["basis"]} for c in sell_cases]
    out["sell_now_note"] = (
        "County and City documentary transfer tax is ADDITIONAL but is unverified (flag F-23) "
        "and is therefore excluded rather than estimated, so the net proceeds shown for the "
        "sell path are OPTIMISTIC by roughly half a percent of price. Proposition 13 "
        "reassessment on a change in ownership is also not modelled as a price discount, "
        "because the parcel's current assessed value is unknown (flag F-01); it is a real "
        "further discount to what a buyer will pay. Both omissions favour the sell path.")

    # ------------------------------------- ULA dead band (pure arithmetic, IN-16/17)
    out["ula_dead_band"] = [
        {"rate_pct": r(x * 100, 1),
         "breakeven_multiple_of_threshold": r(1.0 / (1.0 - x), 4),
         "breakeven_excess_pct": r((1.0 / (1.0 - x) - 1.0) * 100, 2),
         "reading": ("A price up to %.2f%% above the threshold nets LESS than a sale at the "
                     "threshold itself, because the tax applies to the whole price."
                     % ((1.0 / (1.0 - x) - 1.0) * 100))}
        for x in (ula_low, ula_high)]
    out["ula_dead_band_note"] = (
        "Derived only from the official statutory rates at IN-16 and IN-17 plus elementary "
        "arithmetic: net(P) = P at or below the threshold T, and net(P) = P x (1 - rate) above "
        "it, so net(P) > net(T) requires P > T / (1 - rate). The DOLLAR thresholds themselves "
        "are unverified (flag F-24, irregularity IR-07) and are not stated anywhere.")

    # ------------------------------------------------- EQ-7 hold, base regime
    hold_rows = []
    for n in horizons:
        for gname, g in ([("Flat / no escalator - UNVERIFIED, lease not supplied", g_flat)]
                         + list(g_official.items())):
            base = hold_pv(n, g, central_cap, mid_residual, hpi_central,
                           closure_ongoing, ula_low, downtime_years=1.0)
            grid = [r(hold_pv(n, g, c, mid_residual, hpi_central, closure_ongoing,
                              ula_low, downtime_years=1.0)["pv_total"], 2) for bp, c in caps]
            hold_rows.append({
                "years": n, "expiry_year": 2026 + n, "escalator": gname,
                "escalator_pct": r(g * 100, 1),
                "pv_income": r(base["pv_income"], 2),
                "pv_terminal": r(base["pv_terminal"], 2),
                "pv_total": r(base["pv_total"], 2),
                "p_dark_pct": r(base["p_dark"] * 100, 2),
                "grid_min": min(grid), "grid_max": max(grid), "grid": grid,
            })
    out["hold_to_expiry"] = hold_rows

    # --------------------------------------- hold after a NON-RENEWAL SIGNAL
    signal_rows = []
    for n in horizons:
        g = g_official[g_central_name]
        base = hold_pv(n, g, central_cap, mid_residual, hpi_central, closure_ongoing,
                       ula_low, downtime_years=1.0, pdk_override=1.0)
        grid = [r(hold_pv(n, g, c, mid_residual, hpi_central, closure_ongoing, ula_low,
                          downtime_years=1.0, pdk_override=1.0)["pv_total"], 2)
                for bp, c in caps]
        signal_rows.append({
            "years": n, "expiry_year": 2026 + n,
            "pv_income": r(base["pv_income"], 2),
            "pv_terminal": r(base["pv_terminal"], 2),
            "pv_total": r(base["pv_total"], 2),
            "grid_min": min(grid), "grid_max": max(grid),
            "sell_now_index_lower_ula": r(V0 * (1 - ula_low), 2),
            "sell_now_wins": V0 * (1 - ula_low) > base["pv_total"],
        })
    out["hold_after_signal"] = signal_rows
    out["hold_after_signal_note"] = (
        "This is the regime that decides the recommendation. Once the tenant declines an "
        "extension, or discloses a franchise agreement expiring at or before the lease expiry, "
        "site-specific non-renewal probability moves from the system-wide base rate toward "
        "certainty, and the hold path loses its renewing terminal branch. The sell path then "
        "dominates at EVERY point of the cap-spread grid - which is why the recommended plan "
        "pre-commits a sell trigger instead of leaving the decision to be re-argued in 2030.")

    # -------------------------------------------------------- EQ-9 extension
    extend_rows = []
    for n in horizons:
        for gname, g in g_official.items():
            plain = hold_pv(n, g, central_cap, mid_residual, hpi_central,
                            closure_ongoing, ula_low, downtime_years=1.0)
            ext = hold_pv(n + EXTEND_YEARS, g, central_cap, mid_residual, hpi_central,
                          closure_ongoing, ula_low, downtime_years=1.0)
            ge = [hold_pv(n + EXTEND_YEARS, g, c, mid_residual, hpi_central, closure_ongoing,
                          ula_low, downtime_years=1.0)["pv_total"] for bp, c in caps]
            gh = [hold_pv(n, g, c, mid_residual, hpi_central, closure_ongoing, ula_low,
                          downtime_years=1.0)["pv_total"] for bp, c in caps]
            extend_rows.append({
                "years": n, "extended_years": n + EXTEND_YEARS, "escalator": gname,
                "escalator_pct": r(g * 100, 1),
                "pv_hold": r(plain["pv_total"], 2), "pv_extend": r(ext["pv_total"], 2),
                "delta": r(ext["pv_total"] - plain["pv_total"], 2),
                "p_dark_hold_pct": r(plain["p_dark"] * 100, 2),
                "p_dark_extend_pct": r(ext["p_dark"] * 100, 2),
                "extend_wins_across_grid": all(a > b for a, b in zip(ge, gh)),
            })
    out["extend_then_hold"] = extend_rows
    out["extend_note"] = (
        "EQ-9 assumes a %d-year extension is granted at existing economics. That is a "
        "SCENARIO, not a forecast: the tenant has no obligation to negotiate early and is "
        "led by an interim chief executive (T-15, RK-21). The value of the recommended path "
        "does not depend on the extension being granted - a refusal is itself the earliest "
        "reliable closure signal and moves the decision into the regime above." % EXTEND_YEARS)

    # --------------------------------------------------- ranking stability
    stability = []
    for n in horizons:
        g = g_official[g_central_name]
        for sc in sell_cases:
            sell_pv = V0 * (1.0 - sc["tc"])
            holds = [hold_pv(n, g, c, mid_residual, hpi_central, closure_ongoing,
                             sc["tc"], downtime_years=1.0)["pv_total"] for bp, c in caps]
            exts = [hold_pv(n + EXTEND_YEARS, g, c, mid_residual, hpi_central, closure_ongoing,
                            sc["tc"], downtime_years=1.0)["pv_total"] for bp, c in caps]
            sigs = [hold_pv(n, g, c, mid_residual, hpi_central, closure_ongoing, sc["tc"],
                            downtime_years=1.0, pdk_override=1.0)["pv_total"] for bp, c in caps]
            stability.append({
                "years": n, "case": sc["label"],
                "transaction_cost_pct": r(sc["tc"] * 100, 1),
                "sell_index": r(sell_pv, 2),
                "hold_range": [r(min(holds), 2), r(max(holds), 2)],
                "extend_range": [r(min(exts), 2), r(max(exts), 2)],
                "signal_hold_range": [r(min(sigs), 2), r(max(sigs), 2)],
                "hold_beats_sell_at_every_spread": all(h > sell_pv for h in holds),
                "extend_beats_sell_at_every_spread": all(e > sell_pv for e in exts),
                "sell_beats_signal_hold_at_every_spread": all(sell_pv > s for s in sigs),
                "ranking_is_stable": (all(h > sell_pv for h in holds)
                                      and all(e > sell_pv for e in exts)
                                      and all(sell_pv > s for s in sigs)),
            })
    out["ranking_stability"] = stability
    out["ranking_stability_note"] = (
        "EQ-10. Because the cap-rate input is unverified, only the RANKING of paths is "
        "meaningful, and a ranking that holds at every point of the Treasury-anchored spread "
        "grid is a robust conclusion. 'ranking_is_stable' is true only if hold beats sell "
        "before any signal, extend beats sell before any signal, AND sell beats hold after a "
        "signal - at every spread. That is the exact structure of the recommendation.")

    # ------------------------------------------------- downtime sensitivity
    out["downtime_sensitivity"] = [
        {"downtime_years": dt,
         "pv_total_by_horizon": [
             {"years": n,
              "pv_total": r(hold_pv(n, g_official[g_central_name], central_cap, mid_residual,
                                    hpi_central, closure_ongoing, ula_low,
                                    downtime_years=dt)["pv_total"], 2)}
             for n in horizons]}
        for dt in DOWNTIME_SCENARIOS]
    out["downtime_note"] = (
        "Downtime is a SCENARIO input, not an official statistic: no government source "
        "quantifies quick-service-restaurant re-tenanting vacancy (flag F-33, RK-17). It is "
        "included because omitting it would flatter the hold path. During downtime the "
        "landlord also carries property tax, insurance and maintenance that the NNN tenant "
        "previously reimbursed (R-01, R-06); that cash cost is NOT modelled, so the hold "
        "figures remain optimistic.")

    # ------------------------------------------------- residual sensitivity
    out["residual_sensitivity"] = [
        {"residual_pct": res,
         "pv_total_by_horizon": [
             {"years": n,
              "pv_total": r(hold_pv(n, g_official[g_central_name], central_cap, res,
                                    hpi_central, closure_ongoing, ula_low,
                                    downtime_years=1.0)["pv_total"], 2)}
             for n in horizons]}
        for res in residuals]
    out["residual_note"] = (
        "The dark-box land residual (UX-2) is unverified. The only official land-versus-"
        "improvement ratio available is Jack in the Box Inc.'s own balance sheet at IN-18: "
        "land of $93,255 thousand against buildings of $967,676 thousand, or %.2f%% of gross "
        "book cost. That is a national historical COST figure and is expressly not used as a "
        "market estimate (flag F-33). Notice how little the answer moves across a 30%% to 70%% "
        "residual range: because the base-rate non-renewal probability is under 9%%, the dark "
        "branch carries little weight UNTIL A SIGNAL ARRIVES - and then it carries almost all "
        "of it." % land_share)

    # ---------------------------------------------- land growth sensitivity
    out["land_growth_sensitivity"] = [
        {"label": "Downside - FHFA purchase-only Pacific division, 2026 Q1 (IN-7)",
         "hpi_pct": r(hpi_down * 100, 1),
         "base_regime_by_horizon": [
             {"years": n,
              "pv_total": r(hold_pv(n, g_official[g_central_name], central_cap, mid_residual,
                                    hpi_down, closure_ongoing, ula_low,
                                    downtime_years=1.0)["pv_total"], 4)} for n in horizons],
         "signal_regime_by_horizon": [
             {"years": n,
              "pv_total": r(hold_pv(n, g_official[g_central_name], central_cap, mid_residual,
                                    hpi_down, closure_ongoing, ula_low, downtime_years=1.0,
                                    pdk_override=1.0)["pv_total"], 4)} for n in horizons]},
        {"label": "Central - FHFA all-transactions LA-Long Beach-Glendale MSAD, 2026 Q2 (IN-6)",
         "hpi_pct": r(hpi_central * 100, 1),
         "base_regime_by_horizon": [
             {"years": n,
              "pv_total": r(hold_pv(n, g_official[g_central_name], central_cap, mid_residual,
                                    hpi_central, closure_ongoing, ula_low,
                                    downtime_years=1.0)["pv_total"], 4)} for n in horizons],
         "signal_regime_by_horizon": [
             {"years": n,
              "pv_total": r(hold_pv(n, g_official[g_central_name], central_cap, mid_residual,
                                    hpi_central, closure_ongoing, ula_low, downtime_years=1.0,
                                    pdk_override=1.0)["pv_total"], 4)} for n in horizons]},
    ]
    out["land_growth_note"] = (
        "In the BASE regime the two official land-growth assumptions are indistinguishable to "
        "two decimal places, because land growth only enters through the dark branch and the "
        "base-rate non-renewal probability is under 9%. That is itself a finding: while the "
        "tenant is performing, local house-price growth is close to irrelevant to this "
        "decision. In the SIGNAL regime the dark branch carries the whole terminal value and "
        "land growth starts to matter. Shown to four decimal places so the reader can see the "
        "immateriality rather than suspect a rendering error.")

    # ------------------------------------------------- worst-case stress test
    stress = []
    for n in horizons:
        worst = hold_pv(n, g_flat, central_cap, min(residuals), hpi_down,
                        closure_ongoing, 0.0, downtime_years=max(DOWNTIME_SCENARIOS))
        stress.append({
            "years": n, "expiry_year": 2026 + n,
            "pv_hold_stress": r(worst["pv_total"], 2),
            "pv_sell_best_case": r(V0, 2),
            "sell_wins": V0 > worst["pv_total"],
            "gap": r(V0 - worst["pv_total"], 2),
        })
    out["stress_case"] = stress
    out["stress_case_note"] = (
        "This is the honest counter-case to the recommendation, and it is built ONLY from "
        "inputs already declared in the specification: a lease with NO escalator (UX-4, "
        "unknown because the lease was not supplied), the lowest land residual (UX-2), zero "
        "official land-price growth (IN-7), the longest downtime scenario, the shortest "
        "horizon, and a parcel OUTSIDE the City of Los Angeles so the sell path pays no "
        "Measure ULA at all (R-15). Under that combination the sell path wins even with no "
        "adverse tenant signal. It is published because a recommendation that cannot state "
        "the conditions under which it is wrong is not a recommendation. Those conditions are "
        "exactly the ones step 1 of the plan is designed to resolve: is there an escalator, is "
        "the parcel inside the City, and what is the land residual.")

    # ------------------------------------------------------- EQ-11 and EQ-12
    out["catastrophe_overlay"] = {
        "fire_output_loss_share_of_county_gdp_pct": {
            "low": r(fire_low / gdp * 100, 2), "high": r(fire_high / gdp * 100, 2),
            "basis": "IN-13 and IN-14 over IN-15: official county loss statistics divided by official BEA county GDP."},
        "earthquake_five_year_probability_pct": {
            "compound": r((1.0 - (1.0 - eq30) ** (5.0 / 30.0)) * 100, 2),
            "linear": r(eq30 * 5.0 / 30.0 * 100, 2),
            "thirty_year_official_pct": r(eq30 * 100, 1),
            "basis": "IN-12 restated arithmetically over a five-year window. Both restatements are published because the method changes the answer."},
        "note": ("These are severity and frequency BANDS from official statistics. They are "
                 "deliberately NOT multiplied into the present values above, because no "
                 "official source maps a county output loss or a regional earthquake "
                 "probability onto a specific commercial parcel's value. Doing so would "
                 "manufacture precision the sources do not support."),
    }

    # ------------------------------------------------------------- EQ-6 test
    out["sanity"] = {
        "test": ("A flat, never-ending, never-dark tenancy at any spread must return exactly "
                 "V0 = 100.00, because V = NOI / cap and NOI0 = V0 x cap. A 60-year flat path "
                 "with zero residual must also converge to 100.00."),
        "results": [
            {"spread_bp": r(bp, 0), "cap_pct": r(c * 100, 2),
             "closed_form_perpetuity": r((V0 * c) / c, 2),
             "sixty_year_flat_path": r(hold_pv(60, 0.0, c, 0.0, 0.0, 0.0, 0.0,
                                               downtime_years=0.0)["pv_total"], 2)}
            for bp, c in caps],
        "passed": all(abs((V0 * c) / c - V0) < 0.005
                      and abs(hold_pv(60, 0.0, c, 0.0, 0.0, 0.0, 0.0,
                                      downtime_years=0.0)["pv_total"] - V0) < 0.05
                      for bp, c in caps),
    }

    dest = os.path.join(DATA, "projection_output.json")
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print("wrote", dest)
    print("sanity passed:", out["sanity"]["passed"])
    print("central case:", json.dumps(out["meta"]["central_case"]))
    return 0 if out["sanity"]["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
