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


if __name__ == "__main__":
    unittest.main()


class VerificationInvariantTests(unittest.TestCase):
    """Guards for the 2026-11-10 pass: arithmetic restated on the page must stay true."""

    def setUp(self):
        self.data = pm.load_data()

    def test_rate_change_arithmetic(self):
        # 10-year Treasury, 2025-11-06 (4.11) to 2026-11-06 (4.86) = +75 bp.
        published = {o["id"]: o for o in self.data["observations"]}
        self.assertIn("+75 basis points", published["yield_10y_change"]["value"])
        self.assertAlmostEqual(round((4.86 - 4.11) * 100), 75)

    def test_six_month_yield_range(self):
        published = {o["id"]: o for o in self.data["observations"]}
        self.assertIn("93 bp", published["yield_10y_range"]["value"])
        self.assertAlmostEqual(round((5.31 - 4.38) * 100), 93)

    def test_us_cpi_yoy_uses_not_seasonally_adjusted_series(self):
        # A September-to-September comparison must use the NSA index (CPIAUCNS):
        # 336.940 (Sep 2026) / 324.800 (Sep 2025) - 1 = +3.74%.
        self.assertAlmostEqual(round((336.940 / 324.800 - 1) * 100, 2), 3.74)
        published = {o["id"]: o for o in self.data["observations"]}
        self.assertIn("+3.74%", published["cpi_yoy_us"]["value"])
        self.assertIn("CPIAUCNS", self.data["sources"]["fred_cpi"]["url"])

    def test_derived_share_rows_still_reproduce(self):
        published = {o["id"]: o for o in self.data["observations"]}
        self.assertEqual(published["tenant_ca_share"]["value"], "16.4%")
        self.assertAlmostEqual(round(351 / 2136 * 100, 1), 16.4)
        self.assertEqual(published["calfire_share"]["value"], "65.3%")
        self.assertAlmostEqual(round(769561 / 1177944 * 100, 1), 65.3)

    def test_new_rows_have_allowlisted_sources(self):
        for obs_id in ("yield_10y_change", "yield_10y_range", "cpi_yoy_us",
                       "tenant_lease_obligation", "tenant_hazard_geography"):
            obs = next(o for o in self.data["observations"] if o["id"] == obs_id)
            self.assertTrue(obs["sources"], obs_id)
            for sid in obs["sources"]:
                self.assertTrue(validate_site.allowed_external(self.data["sources"][sid]["url"]), sid)

    def test_derived_rows_are_labelled_derived(self):
        for obs_id in ("yield_10y_change", "yield_10y_range", "cpi_yoy_us"):
            obs = next(o for o in self.data["observations"] if o["id"] == obs_id)
            self.assertEqual(obs["status"], "derived", obs_id)
            self.assertIn("Calculation:", obs["note"], obs_id)


class SiteIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.data = pm.load_data()

    def test_404_is_generated_from_nav(self):
        """A retired URL must land on a page that lists the real published pages."""
        html = build_public.render_all(self.data)["404.html"]
        for href, _label in build_public.NAV:
            self.assertIn(f'href="{href}"', html)
        self.assertNotIn("seventeen pages", html)
        for retired in ("geography.html", "population.html", "income.html",
                        "schools.html", "economy.html", "jobs.html", "tenant.html",
                        "repo-review.html"):
            self.assertNotIn(f'href="{retired}"', html, retired)

    def test_404_is_published_and_not_excluded(self):
        self.assertIn("404.html", validate_site.PUBLIC_FILES)
        excluded = (ROOT / "_config.yml").read_text(encoding="utf-8")
        self.assertNotIn("  - 404.html", excluded)

    def test_every_published_page_reaches_404_by_nav(self):
        """The published set and the navigation list must not drift apart."""
        rendered = build_public.render_all(self.data)
        for page in validate_site.PAGES:
            self.assertIn(page, rendered)
        self.assertEqual(len(rendered), len(validate_site.PAGES) + 2)
