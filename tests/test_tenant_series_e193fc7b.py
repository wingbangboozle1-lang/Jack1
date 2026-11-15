"""Tenant trend series (session e193fc7b, E-5): arithmetic, rendering, and source links.

Kept in its own file so it does not touch the worksheet, gate board, or advisor tests
added by session 1d0e4b3c.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_public  # noqa: E402
import projection_model as pm  # noqa: E402
import validate_site  # noqa: E402


class TenantSeriesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = pm.load_data()
        self.series = {s["id"]: s for s in self.data["tenant_series"]}

    def test_seven_quarters_in_order(self) -> None:
        ids = [s["id"] for s in self.data["tenant_series"]]
        self.assertEqual(ids, ["ts_q1_fy25", "ts_q2_fy25", "ts_q3_fy25", "ts_q4_fy25",
                               "ts_q1_fy26", "ts_q2_fy26", "ts_q3_fy26"])

    def test_franchise_rent_reconciles_to_filings(self) -> None:
        fy25 = sum(self.series[k]["franchise_rent_k"] for k in
                   ("ts_q1_fy25", "ts_q2_fy25", "ts_q3_fy25", "ts_q4_fy25"))
        self.assertEqual(fy25, 332735)  # FY2025 10-K row
        ytd26 = sum(self.series[k]["franchise_rent_k"] for k in ("ts_q1_fy26", "ts_q2_fy26", "ts_q3_fy26"))
        self.assertEqual(ytd26, 242526)  # 40-week 10-Q row

    def test_unit_counts_split_and_sum(self) -> None:
        for row in self.data["tenant_series"]:
            rc = row["restaurants_end"]
            self.assertEqual(rc["company"] + rc["franchise"], rc["total"], row["id"])
        self.assertEqual(self.series["ts_q3_fy25"]["restaurants_end"], {"total": 2168, "company": 142, "franchise": 2026})
        self.assertEqual(self.series["ts_q4_fy25"]["restaurants_end"], {"total": 2136, "company": 150, "franchise": 1986})

    def test_roll_forward_where_movements_are_read(self) -> None:
        def total(k: str) -> int:
            return self.series[k]["restaurants_end"]["total"]

        def move(k: str) -> int:
            return self.series[k]["opened"] - self.series[k]["closed"]

        # Q1 FY25 start is the prior-year "at Q4" row of the Q1 FY26 release (2,191).
        self.assertEqual(2191 + move("ts_q1_fy25"), total("ts_q1_fy25"))
        self.assertEqual(total("ts_q1_fy25") + move("ts_q2_fy25"), total("ts_q2_fy25"))
        self.assertEqual(total("ts_q2_fy25") + move("ts_q3_fy25"), total("ts_q3_fy25"))
        self.assertEqual(total("ts_q1_fy26") + move("ts_q2_fy26"), total("ts_q2_fy26"))
        self.assertEqual(total("ts_q2_fy26") + move("ts_q3_fy26"), total("ts_q3_fy26"))
        self.assertEqual(total("ts_q4_fy25") + move("ts_q1_fy26"), total("ts_q1_fy26"))

    def test_unread_cells_stay_blank(self) -> None:
        q4 = self.series["ts_q4_fy25"]
        self.assertIsNone(q4["sss_system"])
        self.assertIsNone(q4["opened"])
        self.assertIsNone(q4["closed"])

    def test_every_row_has_registered_sources(self) -> None:
        for row in self.data["tenant_series"]:
            self.assertTrue(row["sources"], row["id"])
            for sid in row["sources"]:
                self.assertIn(sid, self.data["sources"], row["id"])
                self.assertTrue(self.data["sources"][sid]["url"].startswith("https://"), sid)

    def test_no_transcript_citations(self) -> None:
        for row in self.data["tenant_series"]:
            self.assertNotIn("transcript", (row.get("note") or "").lower(), row["id"])

    def test_property_page_renders_series_with_derived_labels(self) -> None:
        page = build_public.render_all()["property.html"]
        self.assertIn('id="tenant-series"', page)
        self.assertIn("Direction, not one quarter", page)
        self.assertIn("-4.6%", page)  # Q3 FY26 vs Q3 FY25: 73,017 / 76,538 - 1
        self.assertIn("-7.9%", page)  # Q1 FY26 vs Q1 FY25: 97,387 / 105,781 - 1
        self.assertIn("Q4 FY2025 not read", page)
        self.assertIn("Derived: rent ÷ weeks", page)

    def test_series_rows_pass_the_page_validator(self) -> None:
        page = build_public.render_all()["property.html"]
        parser = validate_site.PageParser()
        parser.feed(page)
        series_rows = [r for r in parser.rows if r.get("table") == "tenant-series"] if parser.rows and "table" in parser.rows[0] else parser.rows
        self.assertTrue(series_rows)
        for row in series_rows:
            self.assertTrue(row["source_links"])

    def test_flags_and_audit_for_this_session(self) -> None:
        ids = {f["id"] for f in self.data["flags"]}
        for fid in ("flag_e193_q4fy25_gap", "flag_e193_q1_sixteen_week", "flag_e193_irs_threshold_year",
                    "flag_e193_ca_surcharge", "flag_e193_ula_base_vs_gross"):
            self.assertIn(fid, ids)
        self.assertIn("audit_e193fc7b_20261115", {a["id"] for a in self.data["audit"]})

    def test_ca_surcharge_flag_is_resolved_on_official_source(self) -> None:
        flag = next(f for f in self.data["flags"] if f["id"] == "flag_e193_ca_surcharge")
        self.assertIn("ftb_540_booklet_2025", flag["sources"])
        self.assertIn("line 62", flag["reason"])
        self.assertIn("resolved", flag["item"])


if __name__ == "__main__":
    unittest.main()
