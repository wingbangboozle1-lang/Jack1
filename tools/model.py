#!/usr/bin/env python3
"""
Deterministic projection model for the Jack in the Box NNN hold-vs-sell decision.

Design rules
------------
1. NO hidden inputs. Every number is either (a) an official statistic loaded from
   data/series.json, (b) an explicit, labelled analyst assumption defined in
   ASSUMPTIONS below, or (c) arithmetic on (a) and (b).
2. NO deal-specific rent. The actual rent is unknown (Flagged item F-01), so the
   model works in INDEX form: it reports value *relatives* against the current
   observed market cap rate, plus a clearly-labelled illustrative $1 of rent.
3. Reproducible: `python3 tools/model.py` rewrites data/projections.json.
4. Any output that depends on an unverified assumption is marked
   "basis": "model" so the site can label it as model output, not fact.
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------- #
# Analyst assumptions (labelled; not facts). Each is justified in the site.
# --------------------------------------------------------------------------- #
ASSUMPTIONS = {
    "hold_horizon_years": 9,
    "hold_horizon_note": "Lease expiry window 2030-2035 (principal-supplied); "
                         "9 years from 2026 approximates the midpoint.",
    "cap_rate_current": 0.0491,
    "cap_rate_current_note": "S28: Net Lease Advisor page-stated trailing 12-month "
                             "average cap rate for the Jack in the Box brand.",
    "cap_rate_band": [0.0431, 0.0582],
    "cap_rate_band_note": "F-05: the two Los Angeles data points in S30 and S31. "
                          "Deliberately NOT averaged (different structures).",
    "cap_rate_drift_base_bp_per_year": 5,
    "cap_rate_drift_base_note": "Assumption: 5 bp/yr of continued mild repricing, "
                                "consistent with the Baa yield moving 5.88%->6.59% "
                                "during 2026 (S10). Not an official forecast.",
    "cap_rate_drift_stress_bp_per_year": 20,
    "rent_growth_base": 0.030,
    "rent_growth_base_note": "Assumption anchored to CPI-U food away from home "
                             "(S08: +3.5% over the 12 months to 2026-09) rounded down.",
    "lease_term_decay_discount_per_year": 0.0125,
    "lease_term_decay_note": "Assumption: each year of lost WALT costs ~1.25% of "
                             "value while the lease has fewer than 10 years left. "
                             "A convention, not a measured constant.",
    "renewal_cap_rate_benefit_bp": 75,
    "renewal_cap_rate_benefit_note": "Assumption: a 10-year extension re-rates the "
                                     "asset by ~75 bp versus a sub-5-year term.",
    "transfer_tax_tier1": 0.0445,
    "transfer_tax_tier1_note": "S23: 4.45% combined city base + Measure ULA, tier 1.",
    "transfer_tax_threshold": 5400000,
    "transfer_tax_threshold_note": "S23: $5,400,000 (closings after 2026-06-30).",
    "prop13_rate": 0.01,
    "prop13_rate_note": "S20: 1% of base-year value.",
    "prop13_cap": 0.02,
    "prop13_cap_note": "S20: annual increase limited to 2%.",
}


def load_series():
    with open(os.path.join(ROOT, "data", "series.json")) as fh:
        return json.load(fh)["series"]


def value_relative(cap_rate):
    """Value per $1 of current rent = (1/cap_rate) normalised so that the
    current observed cap rate == 1.0. Pure arithmetic."""
    base = ASSUMPTIONS["cap_rate_current"]
    return base / cap_rate


def project():
    s = load_series()
    cpi = s["cpi_all_items"]["data"]
    food = s["food_away_from_home_cpi"]["data"]
    a = ASSUMPTIONS

    cpi_growth = cpi["2026-09"] / cpi["2020-01"] - 1.0
    food_growth_12m = food["2026-09"] / food["2025-09"] - 1.0

    base = a["cap_rate_current"]
    rows = []
    # Two paths: sell-now (value realised at year 0) vs hold-and-renew.
    for year in range(0, a["hold_horizon_years"] + 1):
        drift = a["cap_rate_drift_base_bp_per_year"] / 10000.0 * year
        stress_drift = a["cap_rate_drift_stress_bp_per_year"] / 10000.0 * year

        rent_multiple = (1.0 + a["rent_growth_base"]) ** year
        decay = (1.0 - a["lease_term_decay_discount_per_year"]) ** year

        # Normalisation: value = rent / cap, and all paths are expressed as a
        # multiple of TODAY's value (base / cap_today == 1.0 at year 0).

        # Path H: hold to expiry without renewal -> rent grows, cap rate drifts,
        #         residual discount compounds as the term shortens.
        cap_hold = base + drift
        val_hold = base / cap_hold * rent_multiple * decay

        # Path R: a 10-year renewal is signed during year 1 (2027), so the cap-rate
        #         benefit starts then and residual decay never applies.
        benefit = a["renewal_cap_rate_benefit_bp"] / 10000.0 if year >= 1 else 0.0
        cap_renew = base + drift - benefit
        val_renew = base / cap_renew * rent_multiple

        # Path S: stress case on rates, same rent growth, no renewal.
        cap_stress = base + stress_drift
        val_stress = base / cap_stress * rent_multiple * decay

        rows.append({
            "year": 2026 + year,
            "rent_multiple_vs_today": round(rent_multiple, 4),
            "cap_rate_hold": round(cap_hold, 4),
            "cap_rate_renew": round(cap_renew, 4),
            "cap_rate_stress": round(cap_stress, 4),
            "value_relative_hold": round(val_hold, 4),
            "value_relative_renew": round(val_renew, 4),
            "value_relative_stress_no_renewal": round(val_stress, 4),
        })

    # Illustrative economics per $1 of current annual rent (the principal can
    # multiply by the true rent once F-01 is resolved).
    ill = {
        "unit": "$1.00 of current annual rent",
        "transfer_tax_pct_if_above_threshold": a["transfer_tax_tier1"],
        "transfer_tax_threshold_usd": a["transfer_tax_threshold"],
        "prop13_annual_rate": a["prop13_rate"],
        "prop13_cap": a["prop13_cap"],
        "note": "Actual dollars cannot be computed because the rent is unverified "
                "(Flagged F-01/F-02).",
    }

    return {
        "generated": "2026-11-06",
        "model_version": "1.0.0",
        "basis": "model",
        "warning": "Model output. Not an appraisal. Not a forecast of any official "
                   "agency. All inputs are either official statistics (cited) or "
                   "explicit analyst assumptions listed below.",
        "assumptions": ASSUMPTIONS,
        "official_inputs_used": {
            "cpi_all_items_2020_01_to_2026_09_pct": round(cpi_growth * 100, 2),
            "cpi_all_items_source": "S07",
            "food_away_from_home_12m_pct": round(food_growth_12m * 100, 2),
            "food_away_from_home_source": "S08",
        },
        "paths": rows,
        "illustrative": ill,
        "how_to_read": [
            "value_relative_* is a multiple of today's market value, not dollars.",
            "value_relative_renew > value_relative_hold at every year because the "
            "renewal both removes residual decay and re-rates the cap rate.",
            "value_relative_stress_no_renewal shows what the same asset is worth if "
            "rates drift 20 bp/yr instead of 5 bp/yr while you wait.",
            "None of these are guarantees; they are the arithmetic consequence of the "
            "assumptions printed above."
        ],
    }


def main():
    out = project()
    path = os.path.join(ROOT, "data", "projections.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")
    print(f"wrote {path}")
    for r in out["paths"]:
        print(r["year"], r["value_relative_hold"], r["value_relative_renew"],
              r["value_relative_stress_no_renewal"])


if __name__ == "__main__":
    main()
