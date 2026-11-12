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

    def test_suggestions_are_review_only_and_source_linked(self):
        outputs = build_public.render_all()
        page = outputs["suggestions.html"]
        parser = validate_site.PageParser()
        parser.feed(page)
        data = pm.load_data()
        # Six original proposals (session 87c0c876) plus dataset-driven site and discovery rows (session 1520648f).
        self.assertEqual(len(parser.rows), 6 + len(data["suggestions"]) + len(data["discovery"]))
        self.assertEqual(page.count("Proposed · not approved or implemented"), 6)
        self.assertIn("not verified property conclusions", page)
        self.assertNotIn("<form", page)
        for name in validate_site.PAGES:
            self.assertIn('href="suggestions.html"', outputs[name])
        self.assertIn('href="suggestions.html"', outputs["404.html"])
        for row in parser.rows:
            self.assertTrue(row["source_links"])

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

    def test_rolling_sources_and_treasury_card_not_stale(self):
        data = pm.load_data()
        obs = {o["id"]: o for o in data["observations"]}
        pages = build_public.render_all()
        self.assertIn("86,837", obs["crime_status"]["value"])
        self.assertIn("24,349", obs["crime_central_bureau"]["value"])
        self.assertIn("November 7, 2026", obs["crime_status"]["period"])
        self.assertIn("4.98%", obs["treasury_yields"]["value"])
        self.assertIn("4.98%", pages["index.html"])
        self.assertNotIn("Nov 9 10Y Treasury 4.88%", pages["index.html"])
        self.assertNotIn("4.88% 10Y Treasury", pages["decision.html"])
        self.assertNotIn("forecast 2027", obs["metro_transit_drivers"]["value"])
        self.assertIn("review completed", obs["cdi_fairplan_catmodel"]["value"])
        questions = {q["id"]: q for q in data["questions"]}
        self.assertIn(obs["treasury_yields"]["period"], questions["q_financing"]["answer"])
        self.assertIn("10Y 4.98%", questions["q_financing"]["answer"])
        self.assertIn("offenses", questions["q_safety"]["answer"])
        self.assertNotIn("incidents year to date", questions["q_safety"]["answer"])

    def test_projection_json_matches_model(self):
        outputs = build_public.render_all()
        payload = json.loads(outputs["assets/projections.json"])
        self.assertEqual(payload, pm.build_projection_payload())

    def test_404_aligned_and_worksheet_blank_defaults(self):
        outputs = build_public.render_all()
        self.assertIn("404.html", outputs)
        # Nested unknown paths must still resolve the dashboard links to the published root.
        self.assertIn('<base href="/Jack1/">', outputs["404.html"])
        err_html = outputs["404.html"]
        for page in validate_site.PAGES:
            self.assertIn(page, err_html)
        for legacy in validate_site.LEGACY_EXCLUDED_PAGES:
            self.assertNotIn(legacy, err_html)
        dp = validate_site.PageParser()
        dp.feed(outputs["decision.html"])
        self.assertEqual(dp.nonempty_input_values, [])

    def test_decision_question_register(self):
        data = pm.load_data()
        questions = data["questions"]
        self.assertGreaterEqual(len(questions), 20)
        valid = {"answered", "partial", "open", "blocked", "derived", "analysis"}
        for q in questions:
            for key in ("id", "question", "answer", "status", "obtain", "sources"):
                self.assertIn(key, q)
            self.assertIn(q["status"], valid, q["id"])
            self.assertTrue(q["sources"], q["id"])
            for sid in q["sources"]:
                self.assertIn(sid, data["sources"], (q["id"], sid))
            # An "open" gate is genuinely blank; a "blocked" gate may state the governing rule
            # while the property-specific amount stays unknown.
            if q["status"] == "open":
                self.assertIsNone(q["answer"], q["id"])
            else:
                self.assertTrue(q["answer"], q["id"])
            if q["status"] == "blocked":
                self.assertIn("blank", q["answer"].lower(), q["id"])
        outputs = build_public.render_all()
        self.assertIn("Questions that must be answered before a decision", outputs["requirements.html"])
        self.assertIn("decision-questions", outputs["requirements.html"])
        self.assertIn("How to close the blanks without guessing", outputs["requirements.html"])

    def test_suggestions_are_proposals_with_sources(self):
        data = pm.load_data()
        self.assertGreaterEqual(len(data["suggestions"]), 8)
        self.assertEqual(len(data["decision_risks"]), len(data["decisions"]))
        for coll in ("suggestions", "discovery", "decision_risks"):
            for item in data[coll]:
                self.assertTrue(item["sources"], item["id"])
                for sid in item["sources"]:
                    self.assertIn(sid, data["sources"], (item["id"], sid))
        for item in data["suggestions"]:
            self.assertIn("A.", item["options"], item["id"])
        outputs = build_public.render_all()
        page = outputs["suggestions.html"]
        self.assertIn("Only chosen items will be built", page)
        self.assertEqual(page.count("Proposed — not implemented"), len(data["suggestions"]) + len(data["discovery"]))
        self.assertIn("decision-risks", outputs["decision.html"])
        self.assertIn("suggestions.html", outputs["index.html"])
        self.assertIn("suggestions.html", outputs["404.html"])

    def test_public_safety_rows_share_one_vintage(self):
        data = pm.load_data()
        obs = {o["id"]: o for o in data["observations"]}
        city, bureau = obs["crime_status"], obs["crime_central_bureau"]
        self.assertIn("November 7, 2026", city["period"])
        self.assertIn("November 7, 2026", bureau["period"])
        self.assertIn("86,837", city["value"])
        self.assertIn("24,349", bureau["value"])
        # 24,349 / 86,837 = 28.0% at a single vintage; a cross-vintage share must not be published.
        self.assertAlmostEqual(24349 / 86837 * 100, 28.0, places=1)
        self.assertIn("28.0%", bureau["note"])
        flag_ids = {f["id"] for f in data["flags"]}
        self.assertIn("flag_lapd_rolling_vintage", flag_ids)
        # Source registry titles must describe the same cut the rows publish.
        self.assertIn("Nov 7, 2026", data["sources"]["lapd_city"]["title"])
        self.assertIn("Nov 7, 2026", data["sources"]["lapd_central"]["title"])
        # The superseded October 31 cut may survive only as documented history on the flagged page.
        outputs = build_public.render_all()
        for page in ("index.html", "market.html", "risks.html", "requirements.html", "decision.html", "sources.html"):
            self.assertNotIn("83,596", outputs[page], page)
        self.assertIn("83,596", outputs["flagged.html"])

    def test_2026_11_10_dataset_enrichment(self):
        data = pm.load_data()
        self.assertEqual(data["meta"]["date"], "2026-11-11")
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
            "verification/2026-11-10-a8681975.md",
            "verification/2026-11-10-c5e199ef.md",
            "verification/2026-11-08-0e369d53.md",
            "verification/2026-11-11-a6ebbd99.md",
            "verification/2026-11-11-2efe9aec.md",
        ):
            self.assertIn(log_name, outputs["audit.html"])


    def test_signal_scorecard_and_best_course(self):
        data = pm.load_data()
        score = pm.signal_scorecard(data)
        self.assertEqual(score["total"], len(data["signals"]))
        self.assertEqual(sum(score["overall"].values()), score["total"])
        self.assertEqual(set(score["overall"]), set(pm.SIGNAL_LEANS))
        for group, counts in score["by_group"].items():
            self.assertEqual(sum(counts.values()), sum(1 for s in data["signals"] if s["group"] == group))
        for coll in ("signals", "verdicts"):
            for item in data[coll]:
                self.assertTrue(item["sources"], item["id"])
                for sid in item["sources"]:
                    self.assertIn(sid, data["sources"], (item["id"], sid))
        for s in data["signals"]:
            self.assertIn(s["lean"], pm.SIGNAL_LEANS, s["id"])
            self.assertTrue(s["reading"] and s["why"], s["id"])
        with self.assertRaises(ValueError):
            pm.signal_scorecard({"signals": [{"id": "x", "group": "g", "signal": "s", "reading": "r", "lean": "buy", "sources": []}]})
        outputs = build_public.render_all()
        self.assertIn('id="signal-scorecard"', outputs["projections.html"])
        self.assertIn('id="best-course"', outputs["decision.html"])
        self.assertIn("projections.html#signal-scorecard", outputs["index.html"])
        # No weight, score, or probability may be attached to a signal.
        for s in data["signals"]:
            self.assertFalse({"weight", "score", "probability"} & set(s), s["id"])

    def test_2026_11_12_corrections_83da931a(self):
        data = pm.load_data()
        obs = {o["id"]: o for o in data["observations"]}
        wage = obs["wage_state_2027"]
        self.assertNotIn("2.97", wage["value"])
        self.assertIn("2.99%", wage["value"])
        self.assertAlmostEqual((17.40 / 16.90 - 1) * 100, 2.96, places=2)
        self.assertIn("dof_minwage_cert", wage["sources"])
        self.assertNotEqual(obs["housing_dof_net_2025"]["geography"], "Los Angeles County")
        self.assertNotIn("Q3 provision", obs["tenant_ar_allowance"]["note"])
        # Derived percentages must reproduce from the official dollar figures in the same row.
        self.assertAlmostEqual((242526 - 260254) / 260254 * 100, -6.8, places=1)
        self.assertAlmostEqual((73017 - 76538) / 76538 * 100, -4.6, places=1)
        self.assertAlmostEqual((66259 - 80793) / 80793 * 100, -18.0, places=1)
        self.assertIn("−6.8%", obs["tenant_rent_trend"]["value"])
        self.assertEqual(164 + 565 + 1020 + 387, 2136)
        self.assertIn("387", obs["tenant_site_control"]["value"])
        flag_ids = {f["id"] for f in data["flags"]}
        self.assertTrue({"flag_wage_pct_corrected", "flag_dof_housing_jurisdiction", "flag_ar_provision_label", "flag_scorecard_judgment", "flag_not_reread_20261112"}.issubset(flag_ids))
        self.assertIn("audit_83da931a_n2", {a["id"] for a in data["audit"]})


if __name__ == "__main__":
    unittest.main()
