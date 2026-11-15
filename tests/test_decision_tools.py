"""Tests for the decision tools supplement (session 4c386ad4, 2026-11-15).

Covers: supplement sources and rule tables, the after-tax page (wiring, row sources, blanks,
privacy), the calculator's no-network / no-storage rule, and the after-tax arithmetic against
hand-worked cases and an independent Python implementation (run through Node when available).
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_decision_tools as bdt  # noqa: E402
import build_public  # noqa: E402
import validate_site  # noqa: E402

DATA = ROOT / "data" / "verified-2026-11-10.json"
JS = ROOT / "assets" / "aftertax.js"


def load_merged():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    import build_timeline  # noqa: E402

    data = build_timeline.merge_supplement(data)
    return bdt.merge_supplement(data)


class SupplementRulesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sup = bdt.load_supplement()
        cls.data = load_merged()

    def test_federal_2026_thresholds_match_rev_proc_2025_32(self):
        fed = self.sup["rules"]["federal_ltcg_2026"]
        self.assertEqual(fed["zero_rate_max"], {"single": 49450, "mfj": 98900, "hoh": 66200, "mfs": 49450})
        self.assertEqual(fed["fifteen_rate_max"], {"single": 545500, "mfj": 613700, "hoh": 579600, "mfs": 306850})
        self.assertEqual(fed["unrecaptured_1250_max_rate"], 0.25)
        self.assertEqual(fed["top_ltcg_rate"], 0.20)
        self.assertEqual(self.sup["rules"]["niit"]["threshold"], {"single": 200000, "hoh": 200000, "mfj": 250000, "mfs": 125000})

    def test_ca_schedules_are_continuous_and_match_printed_base_tax(self):
        cs = self.sup["rules"]["ca_schedules_2025"]
        for name in ("X", "Y", "Z"):
            rows = cs[name]
            self.assertEqual(rows[0][0], 0)
            self.assertIsNone(rows[-1][1])
            for i in range(len(rows) - 1):
                lower, upper, base, rate = rows[i]
                nlower, _, nbase, _ = rows[i + 1]
                self.assertEqual(upper, nlower, f"{name} band {i + 1} is not contiguous")
                expected = round(base + rate * (upper - lower), 2)
                self.assertAlmostEqual(nbase, expected, delta=0.01, msg=f"{name} base tax mismatch at band {i + 2}")
            rates = [r[3] for r in rows]
            self.assertEqual(rates, sorted(rates))
            self.assertEqual(rates[-1], 0.123)

    def test_schedule_mapping_by_filing_status(self):
        m = self.sup["rules"]["ca_schedules_2025"]["schedule_for_status"]
        self.assertEqual(m, {"single": "X", "mfs": "X", "mfj": "Y", "hoh": "Z"})

    def test_every_rule_source_exists_and_is_allowlisted(self):
        for sid, src in self.sup["sources"].items():
            self.assertIn(sid, self.data["sources"])
            self.assertTrue(validate_site.allowed_external(src["url"]), src["url"])
        for key, rule in self.sup["rules"].items():
            for sid in rule.get("source_ids", []):
                self.assertIn(sid, self.data["sources"], f"{key} cites unknown source {sid}")

    def test_supplement_ids_do_not_collide_and_flags_cite_sources(self):
        ids = [f["id"] for f in self.data["flags"]]
        self.assertEqual(len(ids), len(set(ids)))
        for flag in self.sup["flags"]:
            self.assertTrue(flag["sources"], flag["id"])
            for sid in flag["sources"]:
                self.assertIn(sid, self.data["sources"], flag["id"])

    def test_rules_block_matches_supplement_and_is_safe_in_html(self):
        text = bdt.aftertax_rules_json(self.sup)
        self.assertNotIn("</", text)
        parsed = json.loads(text.replace("<\\/", "</"))
        self.assertEqual(parsed["federal_ltcg_2026"]["zero_rate_max"]["mfj"], 98900)
        self.assertEqual(parsed["dtt"]["ula_upper_threshold"], 10900000)


class PagesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_merged()
        cls.outputs = build_public.render_all()

    def test_pages_are_wired_into_site(self):
        for page in bdt.PAGES:
            self.assertIn(page, build_public.PAGES)
            self.assertIn(page, validate_site.PAGES)
            self.assertIn(page, validate_site.PUBLIC_FILES)
            self.assertIn(f'href="{page}"', self.outputs["404.html"], page)
        for name in validate_site.PAGES:
            for page in bdt.PAGES:
                self.assertIn(f'href="{page}"', self.outputs[name], f"{name} lacks nav link to {page}")
        self.assertIn("assets/aftertax.js", validate_site.PUBLIC_FILES)

    def test_every_table_row_has_allowlisted_official_source(self):
        for page in bdt.PAGES:
            parser = validate_site.PageParser()
            parser.feed(self.outputs[page])
            self.assertTrue(parser.rows, page)
            for i, row in enumerate(parser.rows, 1):
                self.assertTrue(row["source_links"], f"{page} row {i}")
                for link in row["source_links"]:
                    self.assertTrue(validate_site.allowed_external(link), f"{page} row {i}: {link}")

    def test_no_privacy_hits_on_new_pages(self):
        for page in bdt.PAGES:
            self.assertEqual(validate_site.privacy_hits(self.outputs[page]), [], page)

    def test_calculator_page_has_no_network_or_storage_and_blank_inputs(self):
        html = self.outputs[bdt.AFTERTAX_PAGE]
        js = JS.read_text(encoding="utf-8")
        forbidden = ["fetch(", "XMLHttpRequest", "localStorage", "sessionStorage", "document.cookie",
                     "sendBeacon", "WebSocket", "import(", "indexedDB", "navigator.serviceWorker"]
        for token in forbidden:
            self.assertNotIn(token, js, token)
            self.assertNotIn(token, html, token)
        parser = validate_site.PageParser()
        parser.feed(html)
        self.assertEqual(parser.nonempty_input_values, [])
        self.assertNotIn("<form", html)
        self.assertIn('src="assets/aftertax.js"', html)
        self.assertIn('id="aftertax-rules"', html)


# ----------------------------------------------------------------- arithmetic
CASES = {
    # A: LA City, MFJ, seller pays; price above $5.4M, ULA 4% band; CA top band with BHST.
    "A_la_city_mfj_ula": {
        "inp": {
            "status": "mfj", "jurisdiction": "la_city", "sellerPaysTransfer": "yes", "heldMoreThanOneYear": "yes",
            "price": 6000000, "sellingCosts": 150000, "debt": 2000000, "adjustedBasis": 1500000,
            "unrecapturedGain": 400000, "fedTaxableIncomeBefore": 300000, "magiBefore": 320000,
            "otherNii": 20000, "caTaxableIncomeBefore": 250000, "caGain": None, "holdValue": None,
        },
        "expect": {"transferTax": 273600.00, "gain": 4076400.00, "fedTax": 835280.00,
                   "niit": 154903.20, "caGainTax": 510957.14, "afterTaxNetProceeds": 2075259.66},
    },
    # B: County only, single, buyer pays the transfer tax; 25% unrecaptured + 15%/20% stack; NIIT over threshold.
    "B_county_single_buyer_pays": {
        "inp": {
            "status": "single", "jurisdiction": "county_only", "sellerPaysTransfer": "no", "heldMoreThanOneYear": "yes",
            "price": 2000000, "sellingCosts": 60000, "debt": 0, "adjustedBasis": 500000,
            "unrecapturedGain": 100000, "fedTaxableIncomeBefore": 80000, "magiBefore": 90000,
            "otherNii": 0, "caTaxableIncomeBefore": 70000, "caGain": None, "holdValue": None,
        },
        "expect": {"transferTax": 0.0, "gain": 1440000.00, "fedTax": 274725.00,
                   "niit": 50540.00, "caGainTax": 168682.57, "afterTaxNetProceeds": 1446052.43},
    },
    # C: Low income; the gain fills the 0% band first and the rest sits at 15%; county-only transfer tax.
    "C_low_income_zero_band": {
        "inp": {
            "status": "single", "jurisdiction": "county_only", "sellerPaysTransfer": "yes", "heldMoreThanOneYear": "yes",
            "price": 300000, "sellingCosts": 15000, "debt": 0, "adjustedBasis": 200000,
            "unrecapturedGain": 0, "fedTaxableIncomeBefore": 20000, "magiBefore": 20000,
            "otherNii": 0, "caTaxableIncomeBefore": 20000, "caGain": None, "holdValue": None,
        },
        "expect": {"transferTax": 330.00, "gain": 84670.00, "fedTax": 8283.00,
                   "niit": 0.0, "caGainTax": 5883.74, "afterTaxNetProceeds": 270503.26},
    },
}


def python_reference(inp: dict, rules: dict) -> dict:
    """Independent implementation of the same rules, written separately from assets/aftertax.js."""
    s = inp["status"]
    price = inp["price"]
    # Transfer tax
    if inp["sellerPaysTransfer"] == "yes" and price > 100:
        if inp["jurisdiction"] == "la_city":
            county = price * 0.0011
            city = -(-price // 500) * 2.25
            ula = 0.0
            if price >= 10900000:
                ula = price * 0.055
            elif price > 5400000:
                ula = price * 0.04
        else:
            county = -(-price // 500) * 0.55
            city = 0.0
            ula = 0.0
        tt = round(county + city + ula, 2)
    else:
        tt = 0.0
    realized = price - inp["sellingCosts"] - tt
    gain = max(0.0, realized - inp["adjustedBasis"])
    unrec = min(inp["unrecapturedGain"], gain)
    ltcg = gain - unrec
    zmax = rules["federal_ltcg_2026"]["zero_rate_max"][s]
    fmax = rules["federal_ltcg_2026"]["fifteen_rate_max"][s]
    b0 = inp["fedTaxableIncomeBefore"] + unrec
    z = min(ltcg, max(0.0, zmax - b0))
    m = min(ltcg - z, max(0.0, fmax - max(b0, zmax)))
    t = ltcg - z - m
    fed = round(0.25 * unrec + 0.15 * m + 0.20 * t, 2)
    thr = rules["niit"]["threshold"][s]
    with_ = min(inp["otherNii"] + gain, max(0.0, inp["magiBefore"] + gain - thr))
    without = min(inp["otherNii"], max(0.0, inp["magiBefore"] - thr))
    niit = round(0.038 * (with_ - without), 2)
    sched = rules["ca_schedules_2025"][rules["ca_schedules_2025"]["schedule_for_status"][s]]

    def ca(ti: float) -> float:
        if ti <= 0:
            return 0.0
        for lo, hi, base, rate in sched:
            if ti > lo and (hi is None or ti <= hi):
                return base + rate * (ti - lo)
        return 0.0

    def bh(ti: float) -> float:
        return 0.01 * max(0.0, ti - 1000000)

    c0 = inp["caTaxableIncomeBefore"]
    ca_gain = inp["caGain"] if inp.get("caGain") is not None else gain
    ca_tax = round(ca(c0 + ca_gain) - ca(c0) + bh(c0 + ca_gain) - bh(c0), 2)
    pre = price - inp["sellingCosts"] - tt - inp["debt"]
    return {"transferTax": tt, "gain": round(gain, 2), "fedTax": fed, "niit": niit,
            "caGainTax": ca_tax, "afterTaxNetProceeds": round(pre - fed - niit - ca_tax, 2)}


def run_js(cases: dict, rules: dict) -> dict:
    node = shutil.which("node")
    if not node:
        raise unittest.SkipTest("node not available")
    script = ("const A=require(process.argv[1]);let s='';process.stdin.on('data',d=>s+=d)"
              ".on('end',()=>{const x=JSON.parse(s);const out={};for(const k of Object.keys(x.cases)){"
              "out[k]=A.compute(x.cases[k],x.rules).result;}process.stdout.write(JSON.stringify(out));});")
    payload = json.dumps({"cases": cases, "rules": rules})
    proc = subprocess.run([node, "-e", script, str(JS)], input=payload, capture_output=True, text=True, timeout=60)
    if proc.returncode != 0:
        raise AssertionError(proc.stderr)
    return json.loads(proc.stdout)


class AfterTaxArithmeticTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sup = bdt.load_supplement()
        cls.rules = json.loads(bdt.aftertax_rules_json(sup).replace("<\\/", "</"))

    def test_python_reference_matches_hand_worked_cases(self):
        for name, case in CASES.items():
            got = python_reference(case["inp"], self.rules)
            for key, want in case["expect"].items():
                self.assertAlmostEqual(got[key], want, delta=0.01, msg=f"{name}.{key}")

    def test_javascript_matches_hand_worked_cases(self):
        out = run_js({k: v["inp"] for k, v in CASES.items()}, self.rules)
        for name, case in CASES.items():
            res = out[name]
            self.assertIsNotNone(res, name)
            self.assertAlmostEqual(res["transferTax"]["total"], case["expect"]["transferTax"], delta=0.01, msg=name)
            self.assertAlmostEqual(res["gain"], case["expect"]["gain"], delta=0.01, msg=name)
            self.assertAlmostEqual(res["fedTax"], case["expect"]["fedTax"], delta=0.01, msg=name)
            self.assertAlmostEqual(res["niit"], case["expect"]["niit"], delta=0.01, msg=name)
            self.assertAlmostEqual(res["caGainTax"], case["expect"]["caGainTax"], delta=0.01, msg=name)
            self.assertAlmostEqual(res["afterTaxNetProceeds"], case["expect"]["afterTaxNetProceeds"], delta=0.01, msg=name)

    def test_javascript_agrees_with_python_reference_on_edge_cases(self):
        edge = {
            "ula_lower_boundary_no_ula": dict(CASES["A_la_city_mfj_ula"]["inp"], price=5400000),
            "ula_top_band": dict(CASES["A_la_city_mfj_ula"]["inp"], price=10900000),
            "loss_gives_no_gain_tax": dict(CASES["B_county_single_buyer_pays"]["inp"], adjustedBasis=5000000),
            "debt_exceeds_net": dict(CASES["B_county_single_buyer_pays"]["inp"], debt=3000000),
            "ca_gain_override": dict(CASES["C_low_income_zero_band"]["inp"], caGain=10000),
        }
        out = run_js(edge, self.rules)
        for name, inp in edge.items():
            ref = python_reference(inp, self.rules)
            res = out[name]
            self.assertAlmostEqual(res["transferTax"]["total"], ref["transferTax"], delta=0.01, msg=name)
            self.assertAlmostEqual(res["fedTax"], ref["fedTax"], delta=0.01, msg=name)
            self.assertAlmostEqual(res["niit"], ref["niit"], delta=0.01, msg=name)
            self.assertAlmostEqual(res["caGainTax"], ref["caGainTax"], delta=0.01, msg=name)
            self.assertAlmostEqual(res["afterTaxNetProceeds"], ref["afterTaxNetProceeds"], delta=0.01, msg=name)
        self.assertTrue(out["debt_exceeds_net"]["negativeNet"])
        self.assertEqual(out["loss_gives_no_gain_tax"]["gain"], 0)
        self.assertEqual(out["loss_gives_no_gain_tax"]["fedTax"], 0)

    def test_blank_inputs_report_missing_fields_not_zero(self):
        empty = {k: None for k in CASES["A_la_city_mfj_ula"]["inp"]}
        empty.update({"status": "", "jurisdiction": "", "sellerPaysTransfer": "", "heldMoreThanOneYear": ""})
        out = run_js({"empty": empty}, self.rules)["empty"]
        self.assertIsNone(out)  # run_js returns result only; a None result means it reported missing fields
        js_text = JS.read_text(encoding="utf-8")
        self.assertIn("missing.push", js_text)


if __name__ == "__main__":
    unittest.main()
