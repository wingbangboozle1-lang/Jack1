"""Tests for the decision timeline supplement (session dcb5495c, 2026-11-12)."""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_public  # noqa: E402
import build_timeline  # noqa: E402
import projection_model as pm  # noqa: E402
import validate_site  # noqa: E402

ROW_COLLECTIONS = ("milestones", "clocks", "lease_facts", "monitors", "windows", "flags", "audit")
STATUSES = {"verified", "derived", "unverified"}


class TimelineDataTests(unittest.TestCase):
    def setUp(self):
        self.t = build_timeline.load_timeline()
        self.base = pm.load_data()

    def test_every_row_cites_a_known_allowlisted_source(self):
        sources = self.t["sources"]
        for sid, src in sources.items():
            self.assertTrue(sid.startswith("tl_"), sid)
            self.assertTrue(validate_site.allowed_external(src["url"]), sid)
            self.assertEqual(src["accessed"], self.t["meta"]["date"], sid)
            for key in ("title", "publisher", "kind"):
                self.assertTrue(src[key], (sid, key))
        for coll in ROW_COLLECTIONS:
            for row in self.t[coll]:
                self.assertTrue(row["sources"], (coll, row["id"]))
                for sid in row["sources"]:
                    self.assertIn(sid, sources, (coll, row["id"]))
        for sid in self.t["principal_schedule"]["sources"]:
            self.assertIn(sid, sources)

    def test_ids_do_not_collide_with_shared_dataset(self):
        self.assertFalse(set(self.t["sources"]) & set(self.base["sources"]))
        self.assertFalse({f["id"] for f in self.t["flags"]} & {f["id"] for f in self.base["flags"]})
        self.assertFalse({a["id"] for a in self.t["audit"]} & {a["id"] for a in self.base["audit"]})
        ids = [row["id"] for coll in ROW_COLLECTIONS for row in self.t[coll]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_unverified_rows_are_blank_and_flagged(self):
        flagged_text = " ".join(f["item"] + " " + f["reason"] for f in self.t["flags"])
        for m in self.t["milestones"]:
            self.assertIn(m["status"], STATUSES, m["id"])
            self.assertRegex(m["sort"], r"^\d{4}-\d{2}-\d{2}$", m["id"])
            if m["status"] == "unverified":
                self.assertIsNone(m["value"], m["id"])
            else:
                self.assertIsNotNone(m["when"], m["id"])
                self.assertIsNotNone(m["value"], m["id"])
        # The lease window dates must stay blank until the executed lease is read.
        for mid in ("tl_window_open", "tl_window_close"):
            m = next(x for x in self.t["milestones"] if x["id"] == mid)
            self.assertIsNone(m["when"])
            self.assertIsNone(m["value"])
        self.assertIn("lease expiry", flagged_text)
        self.assertIn("10-K not yet on EDGAR", flagged_text)

    def test_derived_arithmetic_reproduces(self):
        rows = build_timeline.schedule_rows(self.t)
        self.assertEqual(sum(r["thousands"] for r in rows), 1491984)
        self.assertAlmostEqual(rows[-1]["cumulative"], 100.0)
        self.assertAlmostEqual(rows[3]["share"], 432250 / 1491984 * 100)
        text = {m["id"]: m for m in self.t["milestones"]}
        self.assertEqual(round((426375 + 500000 + 503250) / 1491984 * 100, 1), 95.8)
        self.assertIn("95.8%", text["tl_ard_2032"]["note"])
        self.assertIn("$1,429.625 million", text["tl_ard_2032"]["note"])
        self.assertEqual(round(23356 / 1491984 * 100, 1), 1.6)
        self.assertIn("1.6%", text["tl_ard_2027"]["note"])
        dof = self.base["projections"]["dof"]["annual"]
        self.assertEqual(f'{dof["2030"]:,}', text["tl_dof_2030"]["value"])
        self.assertEqual(f'{dof["2035"]:,}', text["tl_dof_2035"]["value"])
        self.assertIn(f'{(dof["2030"] - dof["2026"]) / dof["2026"] * 100:.2f}%'.replace("-", "−"), text["tl_dof_2030"]["note"])
        self.assertIn(f'{(dof["2035"] - dof["2026"]) / dof["2026"] * 100:.2f}%'.replace("-", "−"), text["tl_dof_2035"]["note"])
        lease = {f["id"]: f for f in self.t["lease_facts"]}
        self.assertEqual(164 + 565 + 1020 + 387, 2136)
        self.assertIn(f"{565 / 2136 * 100:.1f}%", lease["tl_lease_ground"]["value"])
        self.assertIn(f"{387 / 2136 * 100:.1f}%", lease["tl_lease_franchise_direct"]["value"])

    def test_consistent_with_shared_dataset(self):
        """Values that also appear in the shared dataset must agree with it."""
        obs = {o["id"]: o for o in self.base["observations"]}
        text = {m["id"]: m for m in self.t["milestones"]}
        ten_year = re.search(r"10Y (\d\.\d\d%)", text["tl_now_treasury"]["value"]).group(1)
        self.assertIn(ten_year, obs["treasury_yields"]["value"])
        self.assertIn("$1,429.625M of $1,491.984M", obs["tenant_ard_wall"]["value"])
        self.assertIn("45 days", obs["irs_1031_timing"]["value"])
        self.assertIn("180 days", obs["irs_1031_timing"]["value"])
        # Session 1e8970d6 publishes the same schedule on the Property page; the two must agree.
        if "tenant_debt_maturities" in obs:
            for row in self.t["principal_schedule"]["rows"]:
                self.assertIn(f'${row["thousands"] / 1000:.3f}M', obs["tenant_debt_maturities"]["value"], row["period"])
            self.assertIn("$1,491.984M", obs["tenant_debt_maturities"]["value"])

    def test_merge_is_additive_and_idempotent(self):
        merged = build_timeline.merge_supplement(self.base)
        self.assertNotIn("timeline", self.base)
        self.assertEqual(len(merged["sources"]), len(self.base["sources"]) + len(self.t["sources"]))
        self.assertEqual(len(merged["flags"]), len(self.base["flags"]) + len(self.t["flags"]))
        self.assertEqual(len(merged["audit"]), len(self.base["audit"]) + len(self.t["audit"]))
        for key in ("observations", "property_fields", "projections", "decisions", "risks", "requirements", "questions"):
            self.assertEqual(merged[key], self.base[key], key)
        self.assertIs(build_timeline.merge_supplement(merged), merged)


class TimelinePageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs = build_public.render_all()
        cls.t = build_timeline.load_timeline()
        cls.page = cls.outputs[build_timeline.PAGE]
        cls.parser = validate_site.PageParser()
        cls.parser.feed(cls.page)

    def test_page_is_wired_into_site(self):
        self.assertIn(build_timeline.PAGE, build_public.PAGES)
        self.assertIn(build_timeline.PAGE, validate_site.PAGES)
        self.assertIn(build_timeline.PAGE, validate_site.PUBLIC_FILES)
        for name in validate_site.PAGES:
            self.assertIn(f'href="{build_timeline.PAGE}"', self.outputs[name], name)
        self.assertIn(f'href="{build_timeline.PAGE}"', self.outputs["404.html"])
        self.assertEqual((ROOT / build_timeline.PAGE).read_text(encoding="utf-8"), self.page)

    def test_rows_sourced_and_counted(self):
        expected = sum(len(self.t[c]) for c in ("milestones", "clocks", "lease_facts", "monitors", "windows")) + len(self.t["principal_schedule"]["rows"])
        self.assertEqual(len(self.parser.rows), expected)
        for row in self.parser.rows:
            self.assertTrue(row["source_links"])
            for link in row["source_links"]:
                self.assertTrue(validate_site.allowed_external(link), link)

    def test_blank_cells_match_null_values(self):
        nulls = sum((m["when"] is None) + (m["value"] is None) for m in self.t["milestones"])
        self.assertGreater(nulls, 0)
        self.assertEqual(self.page.count('<td class="blank-value"'), nulls)
        self.assertNotIn(">None<", self.page)
        self.assertNotIn("TBD", self.page)

    def test_flags_audit_and_sources_reach_registry_pages(self):
        for flag in self.t["flags"]:
            self.assertIn(build_public.e(flag["item"]), self.outputs["flagged.html"], flag["id"])
        for entry in self.t["audit"]:
            self.assertIn(build_public.e(entry["check"]), self.outputs["audit.html"], entry["id"])
        for sid, src in self.t["sources"].items():
            self.assertIn(build_public.e(src["url"]), self.outputs["sources.html"], sid)

    def test_privacy_and_no_personal_names(self):
        self.assertEqual(validate_site.privacy_hits(self.page), [])
        raw = (ROOT / "data" / "timeline-2026-11-12-dcb5495c.json").read_text(encoding="utf-8")
        self.assertEqual(validate_site.privacy_hits(raw), [])
        for word in ("Chief Executive", "President", "Mr.", "Ms.", "owner's name"):
            self.assertNotIn(word, self.page)

    def test_milestones_in_date_order(self):
        order = [m["sort"] for m in sorted(self.t["milestones"], key=lambda r: r["sort"])]
        positions = [self.page.index(build_public.e(m["milestone"])) for m in sorted(self.t["milestones"], key=lambda r: r["sort"])]
        self.assertEqual(order, sorted(order))
        self.assertEqual(positions, sorted(positions))


if __name__ == "__main__":
    unittest.main()
