#!/usr/bin/env python3
"""Deterministic, privacy-preserving projection engine for the anonymized NNN decision.

WHAT THIS IS
  A reproducible net-present-value / break-even calculator. It combines
  (a) official macro anchors read from data/brief_scenarios.json, each of which is
      copied from a verified row in data/brief_rows.json and linked to an official
      publisher, with
  (b) private, owner-supplied parameters supplied on the command line.

WHAT THIS IS NOT
  It is not an appraisal, a forecast, a cap-rate source, or a recommendation. It never
  fetches data, never contains owner/tenant/address/APN/rent/valuation information, never
  infers a missing value, and never writes a result into the published website. Every
  number it prints is labelled OFFICIAL ANCHOR, OWNER-SUPPLIED, or MODEL OUTPUT.
  Model outputs are computations, NOT official statistics, and are deliberately not
  published on the site (see projection.html and flagged.html).

USAGE
  python3 tools/projection.py --self-test
  python3 tools/projection.py --annual-rent 240000 --remaining-years 6 \
      --renewal-years 10 --gross-sale-price 6200000 --residual-value 5200000 \
      --rent-escalation 0.02 --risk-premium 0.02 --professional-cost-rate 0.015 \
      --stress-loss-rate 0.15 [--output /tmp/my-private-result.json]

No manual input is required from any reader of the website; this tool exists only so the
owner can reproduce the arithmetic locally with their own private numbers.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANCHOR_FILE = ROOT / "data/brief_scenarios.json"
ROW_FILE = ROOT / "data/brief_rows.json"
SOURCE_FILE = ROOT / "data/brief_sources.json"


def load_inputs():
    scen = json.loads(ANCHOR_FILE.read_text(encoding="utf-8"))
    rows = json.loads(ROW_FILE.read_text(encoding="utf-8"))["rows"]
    sources = json.loads(SOURCE_FILE.read_text(encoding="utf-8"))["sources"]
    row_by_id = {r["id"]: r for r in rows}
    anchors = {}
    provenance = []
    for a in scen["anchors"]:
        rid = a["row"]
        if rid not in row_by_id:
            raise SystemExit(f"anchor {a['key']} references missing row {rid}")
        row = row_by_id[rid]
        if row["status"] != "verified" or a["source"] not in row["sources"]:
            raise SystemExit(f"anchor {a['key']} is not backed by a verified official row")
        src = sources[a["source"]]
        anchors[a["key"]] = a["value"]
        provenance.append({
            "key": a["key"], "value": a["value"], "unit": a["unit"],
            "label": a["label"], "row": rid,
            "official_publisher": src["publisher"], "official_url": src["url"],
        })
    return scen, anchors, provenance


def pv_annuity(annual_rent: float, years: int, rate: float, escalation: float) -> float:
    """PV of rent received at each year end, growing at `escalation`, discounted at `rate`."""
    if years <= 0:
        return 0.0
    total = 0.0
    for t in range(1, years + 1):
        total += annual_rent * ((1.0 + escalation) ** (t - 1)) / ((1.0 + rate) ** t)
    return total


def ula_rate(price: float, a: dict, exempt: bool) -> float:
    """Official City of LA transfer tax: base 0.45% + ULA tier on the whole consideration.

    Thresholds ($5.4M / $10.9M) apply to conveyances after June 30, 2026 and are indexed
    annually; the owner must re-check the figures in force at closing (see ULA_FAQ).
    """
    base = a["ula_base_rate"]
    if exempt or price <= a["ula_lower_threshold_usd"]:
        return base
    if price < a["ula_upper_threshold_usd"]:
        return base + a["ula_lower_rate"]
    return base + a["ula_upper_rate"]


def compute(args, scen, anchors, provenance):
    a = anchors
    private = {
        "annual_rent_usd": args.annual_rent,
        "remaining_term_years": args.remaining_years,
        "renewal_term_years": args.renewal_years,
        "gross_sale_price_usd": args.gross_sale_price,
        "residual_value_usd": args.residual_value,
        "rent_escalation_rate": args.rent_escalation,
        "equity_illiquidity_premium": args.risk_premium,
        "professional_cost_rate": args.professional_cost_rate,
        "loan_payoff_usd": args.loan_payoff,
        "owner_tax_usd": args.owner_tax,
        "stress_loss_rate": args.stress_loss_rate,
        "ula_exempt": args.ula_exempt,
        "renewal_probability": args.renewal_probability,
    }
    for key, value in private.items():
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            raise SystemExit(f"invalid owner-supplied value for {key}")

    discount_rate = a["risk_free_10y"] + args.risk_premium
    if discount_rate <= -1.0:
        raise SystemExit("discount rate must be greater than -100%")

    n = int(args.remaining_years)
    m = int(args.renewal_years)

    pv_rent_remaining = pv_annuity(args.annual_rent, n, discount_rate, args.rent_escalation)
    pv_rent_extended = pv_annuity(args.annual_rent, n + m, discount_rate, args.rent_escalation)
    pv_residual_no_renew = args.residual_value / ((1.0 + discount_rate) ** n)
    pv_residual_renew = args.residual_value / ((1.0 + discount_rate) ** (n + m))

    hold_no_renew = pv_rent_remaining + pv_residual_no_renew
    hold_renew = pv_rent_extended + pv_residual_renew
    stressed_hold = hold_no_renew * (1.0 - args.stress_loss_rate)

    transfer_rate = ula_rate(args.gross_sale_price, a, args.ula_exempt)
    transfer_tax = args.gross_sale_price * transfer_rate
    professional_costs = args.gross_sale_price * args.professional_cost_rate
    net_sale = args.gross_sale_price - transfer_tax - professional_costs - args.loan_payoff - args.owner_tax

    denom = hold_renew - stressed_hold
    if abs(denom) < 1e-9:
        break_even_p = None
        break_even_note = "No renewal probability changes the ranking under these inputs (denominator ~ 0)."
    else:
        raw = (net_sale - stressed_hold) / denom
        break_even_p = max(0.0, min(1.0, raw))
        break_even_note = (
            "Renew-and-hold is preferred when the owner's renewal probability exceeds this value; "
            "selling is preferred below it. Raw value clipped to [0, 1]."
            if 0.0 <= raw <= 1.0 else
            "Raw break-even probability fell outside [0, 1]; one path dominates for all probabilities."
        )

    expected_hold = None
    if args.renewal_probability is not None:
        p = args.renewal_probability
        expected_hold = p * hold_renew + (1.0 - p) * stressed_hold

    warnings = []
    if args.gross_sale_price > a["ula_lower_threshold_usd"] and not args.ula_exempt:
        at_threshold = a["ula_lower_threshold_usd"] * (1.0 - a["ula_base_rate"] - args.professional_cost_rate)
        above = args.gross_sale_price * (1.0 - transfer_rate - args.professional_cost_rate)
        if above < at_threshold:
            warnings.append(
                "ULA cliff: a price just above the official threshold can net less than a price at "
                "the threshold because the ULA tier applies to the whole consideration."
            )
    if n + m > a["edd_horizon_year"] - 2026:
        warnings.append(
            "The modeled hold extends beyond 2033, the last year of the official EDD occupational "
            "projections. No employment or income series is extrapolated; treat the tail as scenario only."
        )
    if args.risk_premium == 0.0:
        warnings.append(
            "No owner-supplied equity/illiquidity premium was provided, so the discount rate equals "
            "the official 10-year Treasury anchor. This is a lower bound, not a market cap rate."
        )
    warnings.append(
        "All owner-supplied numbers and every MODEL OUTPUT below are private computations. "
        "They are not official statistics and must not be published on the website."
    )

    return {
        "engine": "tools/projection.py",
        "classification": "PRIVATE / OWNER-RUN — NOT PUBLISHED",
        "official_anchors": provenance,
        "owner_supplied_inputs": {k: v for k, v in private.items() if v is not None},
        "model_parameters": {
            "discount_rate": discount_rate,
            "discount_rate_basis": "OFFICIAL ANCHOR risk_free_10y + OWNER-SUPPLIED equity_illiquidity_premium",
            "transfer_tax_rate_applied": transfer_rate,
            "transfer_tax_rate_basis": "OFFICIAL ANCHOR (0.45% base + ULA tier)",
        },
        "model_outputs_not_official_statistics": {
            "pv_contractual_rent_remaining_term": pv_rent_remaining,
            "pv_residual_no_renew": pv_residual_no_renew,
            "hold_value_no_renew": hold_no_renew,
            "pv_contractual_rent_with_renewal": pv_rent_extended,
            "pv_residual_with_renewal": pv_residual_renew,
            "hold_value_with_renewal": hold_renew,
            "stressed_hold_value": stressed_hold,
            "transfer_tax_usd": transfer_tax,
            "professional_costs_usd": professional_costs,
            "net_sale_proceeds": net_sale,
            "sell_minus_no_renew_hold": net_sale - hold_no_renew,
            "break_even_renewal_probability": break_even_p,
            "break_even_renewal_probability_note": break_even_note,
            "expected_hold_value_at_owner_probability": expected_hold,
        },
        "warnings": warnings,
        "scenarios_considered": [{"id": s["id"], "name": s["name"], "decision_row": s["decision_row"]} for s in scen["scenarios"]],
        "rule": "If a value is not published by an official source, it is blank in the dataset and flagged on flagged.html. Nothing is inferred here.",
    }


def fmt(v):
    if v is None:
        return "n/a"
    if isinstance(v, float) and abs(v) < 1:
        return f"{v:.4f}"
    if isinstance(v, float):
        return f"{v:,.2f}"
    return str(v)


def self_test():
    scen, anchors, _ = load_inputs()
    base = argparse.Namespace(
        annual_rent=240000.0, remaining_years=6, renewal_years=10,
        gross_sale_price=6200000.0, residual_value=5200000.0,
        rent_escalation=0.02, risk_premium=0.02, professional_cost_rate=0.015,
        loan_payoff=0.0, owner_tax=0.0, stress_loss_rate=0.15,
        ula_exempt=False, renewal_probability=None,
    )
    r1 = compute(base, scen, anchors, [])
    r2 = compute(base, scen, anchors, [])
    assert json.dumps(r1["model_outputs_not_official_statistics"], sort_keys=True) == json.dumps(
        r2["model_outputs_not_official_statistics"], sort_keys=True), "non-deterministic output"
    o = r1["model_outputs_not_official_statistics"]
    for k, v in o.items():
        if isinstance(v, float):
            assert math.isfinite(v), f"non-finite model output: {k}"
    assert o["hold_value_with_renewal"] > 0, "hold PV must be positive"
    assert o["net_sale_proceeds"] < base.gross_sale_price, "costs must reduce proceeds"
    # Official ULA cliff behaviour: a price just above the threshold nets less than the threshold.
    just_below = ula_rate(anchors["ula_lower_threshold_usd"], anchors, False)
    just_above = ula_rate(anchors["ula_lower_threshold_usd"] + 1, anchors, False)
    assert just_above > just_below, "ULA tier must apply above the official threshold"
    print("SELF-TEST OK (synthetic private inputs, not a projection, not published)")
    print("  official anchors loaded:", len(anchors))
    print("  ULA rate at threshold:", fmt(just_below), "/ just above:", fmt(just_above))
    print("  sample MODEL OUTPUT hold-with-renewal:", fmt(o["hold_value_with_renewal"]))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-test", action="store_true", help="Run deterministic checks with clearly labelled synthetic inputs.")
    ap.add_argument("--annual-rent", type=float, default=0.0, help="OWNER-SUPPLIED annual base rent (USD).")
    ap.add_argument("--remaining-years", type=int, default=0, help="OWNER-SUPPLIED years to the exact lease expiry.")
    ap.add_argument("--renewal-years", type=int, default=0, help="OWNER-SUPPLIED additional years if renewed.")
    ap.add_argument("--gross-sale-price", type=float, default=0.0, help="OWNER-SUPPLIED gross sale price (USD).")
    ap.add_argument("--residual-value", type=float, default=0.0, help="OWNER-SUPPLIED residual value at expiry (USD).")
    ap.add_argument("--rent-escalation", type=float, default=0.0, help="OWNER-SUPPLIED annual rent escalation rate.")
    ap.add_argument("--risk-premium", type=float, default=0.0, help="OWNER-SUPPLIED equity/illiquidity premium over the official Treasury anchor.")
    ap.add_argument("--professional-cost-rate", type=float, default=0.0, help="OWNER-SUPPLIED professional/closing cost rate.")
    ap.add_argument("--loan-payoff", type=float, default=0.0, help="OWNER-SUPPLIED loan payoff (USD).")
    ap.add_argument("--owner-tax", type=float, default=0.0, help="OWNER-SUPPLIED tax on sale (USD).")
    ap.add_argument("--stress-loss-rate", type=float, default=0.0, help="OWNER-SUPPLIED tail-event value haircut.")
    ap.add_argument("--renewal-probability", type=float, default=None, help="OWNER-SUPPLIED scenario probability (not an estimate).")
    ap.add_argument("--ula-exempt", action="store_true", help="OWNER-SUPPLIED claim that an official ULA exemption applies.")
    ap.add_argument("--output", type=str, default=None, help="Optional PRIVATE output path for the JSON (never an .html file).")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()
    if args.output and Path(args.output).suffix.lower() in {".html", ".htm"}:
        raise SystemExit("Refusing to write a model result into an HTML page. Use a private JSON path.")
    if args.annual_rent <= 0 or args.remaining_years <= 0 or args.gross_sale_price <= 0:
        ap.error("provide positive --annual-rent, --remaining-years and --gross-sale-price (or use --self-test)")

    scen, anchors, provenance = load_inputs()
    result = compute(args, scen, anchors, provenance)
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"Private model result written to {args.output} — do not publish it.")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
