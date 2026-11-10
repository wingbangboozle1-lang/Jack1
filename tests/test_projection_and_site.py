from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_public  # noqa: E402
import projection_model as pm  # noqa: E402
import validate_site  # noqa: E402


class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.data = pm.load_data()

    def test_pct_and_cagr(self):
        self.assertAlmostEqual(pm.pct_change(100, 110), 10.0)
        self.assertIsNone(pm.pct_change(0, 10))
        self.assertIsNone(pm.pct_change(None, 10))
        self.assertAlmostEqual(pm.cagr(100, 121, 2), 10.0)
        self.assertIsNone(pm.cagr(100, 121, 0))

    def test_dof_official_inputs_and_derived_only(self):
        dof = pm.dof_projection(self.data)
        self.assertEqual(dof["rows"][0]["year"], 2026)
        self.assertEqual(dof["rows"][0]["population"], 9811358)
        self.assertEqual(dof["rows"][-1]["year"], 2035)
        self.assertEqual(dof["rows"][-1]["population"], 9708647)
        self.assertIsNone(dof["rows"][0]["yoy_pct"])
        self.assertAlmostEqual(dof["rows"][0]["index_base_100"], 100.0)
        self.assertLess(dof["milestones"][-1]["change_from_2026_pct"], 0)

    def test_scag_no_interpolation(self):
        scag = pm.scag_projection(self.data)
        years = [r["year"] for r in scag["series"]["population"]["rows"]]
        self.assertEqual(years, [2019, 2030, 2045, 2050])
        self.assertNotIn(2035, years)

    def test_property_model_gated(self):
        result = pm.property_decision_model(self.data["projections"]["property_inputs"])
        self.assertEqual(result["status"], "blocked")
        self.assertTrue(all(v is None for v in result["outputs"].values()))
        self.assertEqual(set(result["missing"]), set(pm.REQUIRED_PROPERTY_INPUTS))
        self.assertIsNone(pm.net_sale_proceeds(None, 0, 0, 0))
        self.assertIsNone(pm.npv([100, None], 0.05))
        self.assertAlmostEqual(pm.net_sale_proceeds(1000, 200, 50, 100), 650)
        self.assertAlmostEqual(pm.npv([100, 100], 0.0), 200.0)

    def test_manufacturing_flag_withheld(self):
        sectors = pm.sector_projection(self.data)
        manufacturing = next(s for s in sectors if s["name"] == "Manufacturing")
        self.assertIsNone(manufacturing["published_change"])
        self.assertIn("153%", manufacturing["flag"])
        self.assertAlmostEqual(manufacturing["derived_change_pct"], (706000 - 612000) / 612000 * 100)


class SessionCd460c3bTests(unittest.TestCase):
    """Regression guards for the 2026-11-10 re-verification pass.

    The 2026-11-08 build published the Del Taco California row (351 / 94 / 257) as the
    Jack in the Box California count. These tests pin the corrected figures so the error
    cannot silently return.
    """

    def setUp(self):
        self.data = pm.load_data()
        self.obs = {o["id"]: o for o in self.data["observations"]}

    def test_dataset_is_the_2026_11_10_build(self):
        self.assertTrue(str(pm.DATA_PATH).endswith("data/verified-2026-11-10.json"))
        self.assertEqual(self.data["meta"]["date"], "2026-11-10")
        self.assertEqual(self.data["meta"]["session"], "cd460c3b")

    def test_california_tenant_count_is_jack_not_del_taco(self):
        ca = self.obs["tenant_ca_2025"]["value"]
        self.assertIn("941 total", ca)
        self.assertIn("96 company-operated", ca)
        self.assertIn("845 franchise", ca)
        self.assertNotIn("351", ca)
        self.assertNotIn("257", ca)
        for obs in self.data["observations"]:
            self.assertNotEqual(obs["value"], "351 total; 94 company; 257 franchise")

    def test_california_share_matches_the_corrected_count(self):
        share = self.obs["tenant_ca_share"]
        self.assertEqual(share["status"], "derived")
        self.assertEqual(share["value"], "44.1%")
        self.assertAlmostEqual(round(941 / 2136 * 100, 1), 44.1, places=1)
        check = next(c for c in self.data["derived_checks"] if c["id"] == "tenant_ca_share")
        self.assertEqual(check["inputs"]["numerator"], 941)
        self.assertEqual(check["inputs"]["denominator"], 2136)
        self.assertAlmostEqual(check["expected_value"], 44.1, places=1)

    def test_correction_is_disclosed_on_the_flagged_page(self):
        flag = next(f for f in self.data["flags"] if f["id"] == "flag_tenant_ca_correction")
        self.assertIn("Del Taco", flag["reason"])
        self.assertIn("16.4%", flag["action"])
        self.assertIn("44.1%", flag["action"])
        self.assertIn("sec_10k", flag["sources"])
        outputs = build_public.render_all()
        self.assertIn(flag["item"], outputs["flagged.html"])

    def test_treasury_refreshed_to_latest_business_day(self):
        treasury = self.obs["treasury_yields"]
        self.assertIn("10Y 4.88%", treasury["value"])
        self.assertIn("November 9, 2026", treasury["period"])
        risk = next(r for r in self.data["risks"] if r["id"] == "risk_rates")
        self.assertIn("4.88%", risk["context"])
        self.assertNotIn("4.86%", risk["context"])

    def test_new_rows_carry_official_sources(self):
        for obs_id in (
            "geo_county_density", "geo_commute_city", "households_city", "health_insurance_city",
            "education_city", "housing_cost_city", "retail_county", "business_county",
            "tenant_lease_structure", "tenant_property_mix", "tenant_prototype_size",
            "tenant_franchise_terms", "tenant_portfolio", "tenant_discontinued_ops",
            "tenant_franchising_mix",
        ):
            obs = self.obs[obs_id]
            self.assertTrue(obs["sources"], obs_id)
            self.assertTrue(obs["value"], obs_id)
            for sid in obs["sources"]:
                self.assertIn(sid, self.data["sources"])

    def test_no_personal_names_published(self):
        outputs = build_public.render_all()
        for name in ("Anil", "Yadav", "Ruggeri", "Montgomery", "Tucker", "Hooper"):
            for page, text in outputs.items():
                self.assertNotIn(name, text, f"{name} must not appear in {page}")

    def test_validator_flags_broken_derived_share(self):
        broken = json.loads(json.dumps(self.data))
        for obs in broken["observations"]:
            if obs["id"] == "tenant_ca_share":
                obs["value"] = "16.4%"
        errors = validate_site.check_derived_consistency(broken)
        self.assertTrue(errors)
        self.assertTrue(any("tenant_ca_share" in e for e in errors))


class BuildAndValidationTests(unittest.TestCase):
    def test_build_deterministic_and_check(self):
        first = build_public.render_all()
        second = build_public.render_all()
        self.assertEqual(first, second)
        proc = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_public.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)

    def test_validator_root(self):
        errors = validate_site.validate(ROOT, artifact=False)
        self.assertEqual(errors, [])

    def test_artifact_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "_site"
            proc = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_public.py"), "--out", str(out)], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            errors = validate_site.validate(out, artifact=True)
            self.assertEqual(errors, [])
            files = {str(p.relative_to(out)) for p in out.rglob("*") if p.is_file()}
            self.assertEqual(files, validate_site.PUBLIC_FILES)
            self.assertNotIn("COORDINATION.md", files)
            self.assertFalse(any(f.startswith(("archive/", "research/", "verification/", "pages/", "site/")) for f in files))

    def test_every_row_has_official_source(self):
        outputs = build_public.render_all()
        for page in validate_site.PAGES:
            parser = validate_site.PageParser()
            parser.feed(outputs[page])
            self.assertTrue(parser.rows, page)
            for row in parser.rows:
                self.assertTrue(row["source_links"], page)
                for link in row["source_links"]:
                    self.assertTrue(validate_site.allowed_external(link), (page, link))

    def test_privacy_patterns(self):
        outputs = build_public.render_all()
        for page, text in outputs.items():
            self.assertEqual(validate_site.privacy_hits(text), [], page)
        self.assertEqual(validate_site.privacy_hits("contact@example.com"), ["email:con…"])
        self.assertEqual(validate_site.privacy_hits("213-555-1234"), ["phone:213…"])
        self.assertEqual(validate_site.privacy_hits("1234-567-890"), ["apn:123…"])
        self.assertEqual(validate_site.privacy_hits("<<<<<<< HEAD"), ["conflict-marker"])

    def test_projection_json_matches_model(self):
        outputs = build_public.render_all()
        payload = json.loads(outputs["assets/projections.json"])
        self.assertEqual(payload, pm.build_projection_payload())


if __name__ == "__main__":
    unittest.main()
