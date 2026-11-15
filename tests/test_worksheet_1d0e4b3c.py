"""Browser worksheet arithmetic (session arena/1d0e4b3c-jack1, task X1-2).

The owner worksheet in assets/site.js is executed under Node with a minimal DOM stub, so the
real browser code is tested, not a copy. Expected values come from independent Python
arithmetic on a worked example with test-only inputs (not real property figures).
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_public  # noqa: E402

SITE_JS = ROOT / "assets" / "site.js"

NODE_HARNESS = r"""
const fs = require('fs');
const src = fs.readFileSync(process.argv[1], 'utf8');
const inputs = JSON.parse(process.argv[2]);
const fieldIds = ['ws-jurisdiction','ws-exchange','ws-sale-price','ws-debt','ws-debt-exit','ws-broker-pct',
  'ws-tax-basis','ws-tax-rate','ws-rent','ws-rent-tax','ws-interest','ws-years','ws-esc','ws-discount',
  'ws-exit-val','ws-downtime','ws-carry'];
const outIds = ['ws-out-dtt','ws-out-sale','ws-out-hold','ws-out-spread'];
const els = {};
function mk(id, value) {
  const el = { id: id, value: value === undefined ? '' : String(value), textContent: '', listeners: {},
    addEventListener(t, f) { (this.listeners[t] = this.listeners[t] || []).push(f); } };
  els[id] = el; return el;
}
fieldIds.forEach(function (id) { mk(id, id === 'ws-jurisdiction' ? 'la_city' : (id === 'ws-exchange' ? 'taxable' : '')); });
outIds.forEach(function (id) { mk(id, ''); mk(id + '-note', ''); });
const ws = mk('owner-worksheet', '');
ws.querySelectorAll = function () { return fieldIds.map(function (id) { return els[id]; }); };
ws.querySelector = function () { return null; };
const document = {
  getElementById: function (id) { return els[id] || null; },
  querySelector: function () { return null; },
  querySelectorAll: function () { return []; },
  addEventListener: function () {}
};
const window = { innerWidth: 1200 };
new Function('document', 'window', src)(document, window);
Object.keys(inputs).forEach(function (id) { els[id].value = inputs[id]; });
const f = els['ws-sale-price'].listeners['input'][0];
f();
const out = {};
outIds.forEach(function (id) { out[id] = els[id].textContent; });
process.stdout.write(JSON.stringify(out));
"""

WORKED = {
    "ws-sale-price": "5000000", "ws-debt": "1000000", "ws-broker-pct": "3", "ws-tax-basis": "2000000",
    "ws-tax-rate": "30", "ws-rent": "300000", "ws-rent-tax": "25", "ws-interest": "40000",
    "ws-years": "5", "ws-esc": "2", "ws-discount": "6", "ws-exit-val": "4000000",
    "ws-debt-exit": "800000", "ws-downtime": "6", "ws-carry": "20000",
}


def run_worksheet(inputs: dict) -> dict:
    proc = subprocess.run(
        ["node", "-e", NODE_HARNESS, str(SITE_JS), json.dumps(inputs)],
        capture_output=True, text=True, check=True, timeout=60,
    )
    return json.loads(proc.stdout)


def expected_worked_example() -> dict:
    """Independent arithmetic, stated in the same order as the worksheet's documented formulas."""
    def la_rate(p: float) -> float:
        if p >= 10_900_000:
            return 0.0606
        if p > 5_400_000:
            return 0.0456
        return 0.0056

    price, debt, broker, basis, tg = 5_000_000, 1_000_000, 0.03, 2_000_000, 0.30
    dtt = price * la_rate(price)
    closing = dtt + price * broker
    tax = max(0.0, (price - closing) - basis) * tg
    net_sale = price - debt - closing - tax

    rent, tr, interest, years, g, r = 300_000, 0.25, 40_000, 5, 0.02, 0.06
    debt_exit, exit_v, down_m, carry = 800_000, 4_000_000, 6, 20_000
    pv_ops = sum((rent * (1 + g) ** (t - 1) - interest) * (1 - tr) / (1 + r) ** t for t in range(1, years + 1))
    exit_cost = exit_v * (la_rate(exit_v) + broker)
    exit_tax = max(0.0, exit_v - exit_cost - basis) * tg
    pv_exit = (exit_v - exit_cost - debt_exit - exit_tax) / (1 + r) ** years
    pv_down = (rent * (1 + g) ** years * down_m / 12 + carry * down_m / 12) * (1 - tr) / (1 + r) ** years
    hold = pv_ops + pv_exit - pv_down
    return {"net_sale": net_sale, "hold": hold, "spread": hold - net_sale}


def usd(v: float) -> str:
    return ("-$" if v < 0 else "$") + f"{round(abs(v)):,}"


@unittest.skipUnless(shutil.which("node"), "node is required to execute the browser worksheet")
class WorksheetArithmeticTests(unittest.TestCase):
    def test_worked_example_matches_independent_arithmetic(self):
        exp = expected_worked_example()
        out = run_worksheet(WORKED)
        self.assertEqual(out["ws-out-dtt"], "$28,000")
        self.assertEqual(out["ws-out-sale"], usd(exp["net_sale"]))
        self.assertEqual(out["ws-out-hold"], usd(exp["hold"]))
        self.assertEqual(out["ws-out-spread"], "After-tax Sale ahead by " + usd(-exp["spread"]))

    def test_hold_is_after_tax_not_gross(self):
        # Setting the rent tax to zero must raise the hold value; the old pre-tax hold did not depend on it.
        taxed = run_worksheet(WORKED)
        untaxed = run_worksheet({**WORKED, "ws-rent-tax": "0"})
        self.assertNotEqual(taxed["ws-out-hold"], untaxed["ws-out-hold"])

    def test_every_hold_input_is_required(self):
        for field in ["ws-rent", "ws-rent-tax", "ws-interest", "ws-years", "ws-esc", "ws-discount",
                      "ws-exit-val", "ws-debt-exit", "ws-downtime", "ws-carry", "ws-tax-basis", "ws-tax-rate", "ws-broker-pct"]:
            with self.subTest(missing=field):
                inputs = {k: v for k, v in WORKED.items() if k != field}
                out = run_worksheet(inputs)
                self.assertEqual(out["ws-out-hold"], "—", f"hold output must stay blank without {field}")
                self.assertEqual(out["ws-out-spread"], "—")

    def test_blank_worksheet_shows_no_figures(self):
        out = run_worksheet({})
        for key in ["ws-out-dtt", "ws-out-sale", "ws-out-hold", "ws-out-spread"]:
            self.assertEqual(out[key], "—", key)

    def test_out_of_range_tax_rate_blanks_the_hold_case(self):
        out = run_worksheet({**WORKED, "ws-rent-tax": "150"})
        self.assertEqual(out["ws-out-hold"], "—")


class WorksheetMarkupTests(unittest.TestCase):
    def setUp(self):
        from projection_model import load_data
        import build_timeline
        self.html = build_public.build_decision(build_timeline.merge_supplement(load_data()))

    def test_new_inputs_present_and_blank(self):
        for field in ["ws-debt-exit", "ws-rent-tax", "ws-interest", "ws-downtime", "ws-carry"]:
            self.assertIn(f'id="{field}"', self.html)
        inputs = re.findall(r"<input [^>]*>", self.html)
        self.assertTrue(inputs)
        for tag in inputs:
            self.assertNotIn("value=", tag, f"worksheet input must not carry a default: {tag}")

    def test_worksheet_states_no_storage_or_network(self):
        self.assertIn("without cookies, storage, or network requests", self.html)
        js = SITE_JS.read_text(encoding="utf-8")
        for banned in ["localStorage", "sessionStorage", "document.cookie", "fetch(", "XMLHttpRequest", "sendBeacon"]:
            self.assertNotIn(banned, js)


if __name__ == "__main__":
    unittest.main()
