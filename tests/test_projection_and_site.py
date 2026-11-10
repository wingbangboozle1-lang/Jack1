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

    def test_404_aligned_and_worksheet_blank_defaults(self):
        outputs = build_public.render_all()
        self.assertIn("404.html", outputs)
        err_html = outputs["404.html"]
        for page in validate_site.PAGES:
            self.assertIn(page, err_html)
        for legacy in validate_site.LEGACY_EXCLUDED_PAGES:
            self.assertNotIn(legacy, err_html)
        dp = validate_site.PageParser()
        dp.feed(outputs["decision.html"])
        self.assertEqual(dp.nonempty_input_values, [])

    def test_2026_11_10_dataset_enrichment(self):
        data = pm.load_data()
        self.assertEqual(data["meta"]["date"], "2026-11-10")
        obs = {o["id"]: o for o in data["observations"]}
        for required in (
            "tenant_ard_wall",
            "tenant_ar_allowance",
            "dtt_combined_stack",
            "openfema_declarations_la",
            "pop_dof_city_2026",
            "wage_state_2027",
            "pop_dof_census_2025_gap",
        ):
            self.assertIn(required, obs)
        # Ensure FY2025 10-K Item 2 California unit count uses Jack in the Box (941 / 44.1%), not Del Taco (351).
        self.assertIn("941", obs["tenant_ca_2025"]["value"])
        self.assertNotIn("351", obs["tenant_ca_2025"]["value"])
        self.assertIn("44.1%", obs["tenant_ca_share"]["value"])
        # Ensure merged c5e199ef and af77a54e flags/audit entries and caution callout remain preserved.
        flag_ids = {f["id"] for f in data["flags"]}
        self.assertTrue({"flag_dof_census_base", "flag_git_metadata_privacy", "flag_root_briefs", "flag_ca_units_correction"}.issubset(flag_ids))
        audit_ids = {a["id"] for a in data["audit"]}
        self.assertTrue({"audit_c5e199ef_pass", "audit_recheck_2026_11_10", "audit_ac5b9087_pass"}.issubset(audit_ids))
        for sid, src in data["sources"].items():
            self.assertTrue(validate_site.allowed_external(src["url"]), (sid, src["url"]))

    def test_merged_callout_and_verification_logs_present(self):
        outputs = build_public.render_all()
        self.assertIn("Caution: DOF level vs Census estimate", outputs["projections.html"])
        for log_name in (
            "verification/2026-11-10-2eefc54d.md",
            "verification/2026-11-10-ac5b9087.md",
            "verification/2026-11-10-af77a54e.md",
            "verification/2026-11-10-c5e199ef.md",
            "verification/2026-11-08-0e369d53.md",
        ):
            self.assertIn(log_name, outputs["audit.html"])


if __name__ == "__main__":
    unittest.main()
