"""Checks for the rows added by session 1e8970d6 on 2026-11-12 (macro outlook, stress history, Census detail)."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_public  # noqa: E402
import validate_site  # noqa: E402
from projection_model import build_projection_payload, load_data  # noqa: E402

STAGED = ROOT / "data" / "additions-2026-11-12-1e8970d6.json"


class AdditionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_data()
        cls.staged = json.loads(STAGED.read_text(encoding="utf-8"))
        cls.obs = {o["id"]: o for o in cls.data["observations"]}

    def test_every_staged_item_is_preserved_except_audited_citation_correction(self):
        for sid, src in self.staged["sources"].items():
            self.assertEqual(self.data["sources"][sid], src)
        for coll in ("observations", "flags", "audit"):
            have = {x["id"]: x for x in self.data[coll]}
            for item in self.staged[coll]:
                current = have[item["id"]]
                if coll == "observations" and item["id"] == "nri_additional_ratings":
                    # C-1 verified that the composite query omits these fields; preserve values,
                    # but point this row to the separate official 18-hazard-ratings query.
                    prior = {k: v for k, v in item.items() if k not in ("period", "sources")}
                    corrected = {k: v for k, v in current.items() if k not in ("period", "sources")}
                    self.assertEqual(corrected, prior)
                    self.assertEqual(current["period"], "NRI v1.20, December 2025")
                    self.assertEqual(current["sources"], ["fema_hazard_ratings"])
                else:
                    self.assertEqual(current, item)

    def test_staged_rows_have_allowlisted_official_sources(self):
        for item in self.staged["observations"] + self.staged["flags"]:
            self.assertTrue(item["sources"], item["id"])
            for sid in item["sources"]:
                self.assertIn(sid, self.data["sources"], item["id"])
                self.assertTrue(validate_site.allowed_external(self.data["sources"][sid]["url"]), sid)

    def test_no_staged_row_is_blank_or_touches_property_fields(self):
        for item in self.staged["observations"]:
            self.assertIn(item["status"], ("verified", "derived"))
            self.assertTrue(item["value"])
        for field in self.data["property_fields"]:
            self.assertIsNone(field["value"])

    def test_derived_arithmetic_reproduces(self):
        # Inputs are the published monthly values quoted in each row's value text.
        self.assertEqual(3_820_951 - 5_054_309, -1_233_358)
        self.assertEqual(round((3_820_951 - 5_054_309) / 5_054_309 * 100, 1), -24.4)
        self.assertEqual(4_893_555 - 5_054_309, -160_754)
        self.assertEqual(round((4_893_555 - 5_054_309) / 5_054_309 * 100, 1), -3.2)
        self.assertEqual(4_267_379 - 4_713_759, -446_380)
        self.assertEqual(round((4_267_379 - 4_713_759) / 4_713_759 * 100, 1), -9.5)
        self.assertEqual(round(215.7 - 397.9, 1), -182.2)
        self.assertEqual(round((215.7 - 397.9) / 397.9 * 100, 1), -45.8)
        self.assertEqual(round(392.4 - 385.2, 1), 7.2)
        self.assertEqual(round(392.4 - 400.6, 1), -8.2)
        self.assertEqual(12 * 4 + 2, 50)  # January 2009 through February 2013 inclusive
        self.assertEqual(6_030 + 73_728 + 35_500 + 432_250 + 16_000 + 928_476, 1_491_984)
        for rid, needles in {
            "laus_2020_shock_employment": ["5,054,309", "3,820,951", "−1,233,358", "−24.4%"],
            "laus_2020_recovery": ["4,893,555", "−160,754", "−3.2%"],
            "laus_gfc_duration": ["4,713,759", "4,267,379", "−446,380", "−9.5%", "50 consecutive months"],
            "ces_food_2020_shock": ["397.9", "215.7", "−182.2", "−45.8%"],
            "ces_food_current": ["392.4", "+7.2", "−8.2"],
            "tenant_debt_maturities": ["$6.030M", "$73.728M", "$35.500M", "$432.250M", "$16.000M", "$928.476M", "$1,491.984M"],
        }.items():
            for needle in needles:
                self.assertIn(needle, self.obs[rid]["value"], rid)
            if rid != "tenant_debt_maturities":
                self.assertEqual(self.obs[rid]["status"], "derived", rid)

    def test_conflicting_usgs_figures_are_both_published_and_flagged(self):
        value = self.obs["usgs_northridge_1994"]["value"]
        for needle in ("33 killed", "$40 billion", "57 died", "$20 billion"):
            self.assertIn(needle, value)
        self.assertIn("flag_usgs_northridge_conflict", {f["id"] for f in self.data["flags"]})

    def test_projection_page_shows_macro_and_stress_tables_with_caveats(self):
        outputs = build_public.render_all()
        page = outputs["projections.html"]
        for needle in ('id="macro-outlook"', 'id="stress-history"', "not Los Angeles, tenant or parcel forecasts", "not probabilities and not forecasts"):
            self.assertIn(needle, page)
        flagged = outputs["flagged.html"]
        for flag in self.staged["flags"]:
            self.assertIn(flag["item"], flagged)

    def test_macro_rows_do_not_feed_the_gated_property_model(self):
        payload = build_projection_payload(self.data)
        self.assertTrue(all(v is None for v in payload["property_model"]["outputs"].values()))


if __name__ == "__main__":
    unittest.main()
