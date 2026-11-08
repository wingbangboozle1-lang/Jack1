"""Reproducible, evidence-gated projection helpers.

Only transparent arithmetic is performed here. Official inputs are read from
`data/verified-2026-11-08.json`; missing property inputs produce None, never zero.
No cap rates, rent growth, probabilities, or parcel values are invented.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "verified-2026-11-08.json"


def load_data(path: Path | str = DATA_PATH) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def pct_change(start: float | None, end: float | None) -> float | None:
    if start is None or end is None or start == 0:
        return None
    return (end - start) / start * 100.0


def cagr(start: float | None, end: float | None, years: float | None) -> float | None:
    if start is None or end is None or years is None or years <= 0 or start <= 0 or end < 0:
        return None
    return ((end / start) ** (1.0 / years) - 1.0) * 100.0


def index_value(value: float | None, base: float | None) -> float | None:
    if value is None or base is None or base == 0:
        return None
    return value / base * 100.0


def _fmt_pct(value: float | None, digits: int = 2) -> str:
    return "—" if value is None else f"{value:+.{digits}f}%"


def _fmt_num(value: float | None, digits: int = 0) -> str:
    if value is None:
        return "—"
    if digits == 0:
        return f"{value:,.0f}"
    return f"{value:,.{digits}f}"


def dof_projection(data: dict[str, Any]) -> dict[str, Any]:
    p = data["projections"]["dof"]
    annual = {int(k): int(v) for k, v in p["annual"].items()}
    years = sorted(annual)
    base = annual[years[0]]
    rows = []
    prev = None
    for year in years:
        value = annual[year]
        rows.append({
            "year": year,
            "population": value,
            "yoy_pct": pct_change(prev, value),
            "change_from_base_pct": pct_change(base, value),
            "index_base_100": index_value(value, base),
            "display": {
                "population": _fmt_num(value),
                "yoy": _fmt_pct(pct_change(prev, value)),
                "change": _fmt_pct(pct_change(base, value)),
                "index": _fmt_num(index_value(value, base), 1),
            },
        })
        prev = value
    milestones = []
    for year_s, value in sorted(p["milestones"].items(), key=lambda kv: int(kv[0])):
        year = int(year_s)
        value = int(value)
        milestones.append({
            "year": year,
            "population": value,
            "change_from_2026_pct": pct_change(base, value),
            "cagr_from_2026_pct": cagr(base, value, year - years[0]),
            "display": {
                "population": _fmt_num(value),
                "change": _fmt_pct(pct_change(base, value)),
                "cagr": _fmt_pct(cagr(base, value, year - years[0])),
            },
        })
    return {"source": p["source"], "geography": p["geography"], "vintage": p["vintage"], "rows": rows, "milestones": milestones}


def scag_projection(data: dict[str, Any]) -> dict[str, Any]:
    p = data["projections"]["scag"]
    series = {}
    for name in ("population", "households", "employment"):
        vals = {int(k): int(v) for k, v in p[name].items()}
        years = sorted(vals)
        base_year = years[0]
        base = vals[base_year]
        rows = []
        for year in years:
            value = vals[year]
            rows.append({
                "year": year,
                "value": value,
                "change_from_base_pct": pct_change(base, value),
                "cagr_from_base_pct": cagr(base, value, year - base_year),
                "display": {
                    "value": _fmt_num(value),
                    "change": _fmt_pct(pct_change(base, value)),
                    "cagr": _fmt_num(cagr(base, value, year - base_year), 2) + "%" if cagr(base, value, year - base_year) is not None else "—",
                },
            })
        series[name] = {"base_year": base_year, "rows": rows}
    return {"source": p["source"], "geography": p["geography"], "vintage": p["vintage"], "series": series}


def agency_comparison(data: dict[str, Any]) -> list[dict[str, Any]]:
    dof = {int(k): int(v) for k, v in data["projections"]["dof"]["milestones"].items()}
    scag = {int(k): int(v) for k, v in data["projections"]["scag"]["population"].items()}
    rows = []
    for year in sorted(set(dof) & set(scag)):
        d, s = dof[year], scag[year]
        rows.append({
            "year": year,
            "dof": d,
            "scag": s,
            "difference": s - d,
            "difference_pct": pct_change(d, s),
            "display": {"dof": _fmt_num(d), "scag": _fmt_num(s), "difference": _fmt_num(s - d), "difference_pct": _fmt_pct(pct_change(d, s))},
        })
    return rows


def sector_projection(data: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for item in data["projections"]["sectors"]:
        years = item["end_year"] - item["start_year"]
        change = pct_change(item["start"], item["end"])
        growth = cagr(item["start"], item["end"], years)
        rows.append({
            **item,
            "derived_change_pct": change,
            "derived_cagr_pct": growth,
            "display": {
                "start": _fmt_num(item["start"]),
                "end": _fmt_num(item["end"]),
                "change": _fmt_pct(change, 1),
                "cagr": _fmt_pct(growth, 2),
                "published": item.get("published_change") or "Withheld — see flag",
            },
        })
    return rows


REQUIRED_PROPERTY_INPUTS = (
    "rent_schedule", "owner_costs", "capex_plan", "exit_value", "discount_rate",
    "tax_basis", "debt_payoff", "transaction_costs", "sale_price", "scenario_probabilities",
)


def net_sale_proceeds(sale_price: float | None, debt_payoff: float | None, transaction_costs: float | None, taxes: float | None) -> float | None:
    values = (sale_price, debt_payoff, transaction_costs, taxes)
    if any(v is None for v in values):
        return None
    return sale_price - debt_payoff - transaction_costs - taxes


def npv(cashflows: Iterable[float | None] | None, discount_rate: float | None) -> float | None:
    if cashflows is None or discount_rate is None or discount_rate <= -1:
        return None
    flows = list(cashflows)
    if not flows or any(v is None for v in flows):
        return None
    return sum(float(v) / ((1.0 + discount_rate) ** t) for t, v in enumerate(flows))


def property_decision_model(inputs: dict[str, Any] | None) -> dict[str, Any]:
    inputs = inputs or {}
    missing = [key for key in REQUIRED_PROPERTY_INPUTS if inputs.get(key) is None]
    outputs = {
        "net_sale_proceeds": None,
        "hold_npv": None,
        "renew_npv": None,
        "retenant_npv": None,
        "recommended_path": None,
    }
    if missing:
        return {"status": "blocked", "missing": missing, "outputs": outputs}
    # Even with all inputs present, this scaffold refuses to rank paths without
    # explicit verified cash-flow schedules. The public dataset intentionally
    # keeps every input null; no manual or inferred values are accepted here.
    return {"status": "requires_verified_cashflow_schedules", "missing": [], "outputs": outputs}


def build_projection_payload(data: dict[str, Any] | None = None) -> dict[str, Any]:
    data = data or load_data()
    return {
        "meta": {"date": data["meta"]["date"], "session": data["meta"]["session"], "method": "official inputs + transparent arithmetic; no interpolation or parcel extrapolation"},
        "dof": dof_projection(data),
        "scag": scag_projection(data),
        "agency_comparison": agency_comparison(data),
        "sectors": sector_projection(data),
        "stress": data["projections"]["stress"],
        "property_model": property_decision_model(data["projections"]["property_inputs"]),
    }


if __name__ == "__main__":
    print(json.dumps(build_projection_payload(), indent=2))
