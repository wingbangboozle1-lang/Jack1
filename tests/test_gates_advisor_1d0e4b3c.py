"""Decision-gate board and one-page advisor sheet (session arena/1d0e4b3c-jack1, tasks X1-3 and X1-4)."""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_public  # noqa: E402
import build_timeline  # noqa: E402
from projection_model import load_data  # noqa: E402


class GateBoardTests(unittest.TestCase):
    def setUp(self):
        self.data = build_timeline.merge_supplement(load_data())
        self.html = build_public.build_gates(self.data)

    def test_every_register_question_is_on_exactly_one_gate(self):
        assigned = [qid for _, _, ids in build_public.GATES for qid in ids]
        self.assertEqual(sorted(assigned), sorted(q["id"] for q in self.data["questions"]))
        self.assertEqual(len(assigned), len(set(assigned)))

    def test_board_rows_and_blank_closing_dates(self):
        rows = re.findall(r"<tr>.*?</tr>", self.html, flags=re.S)
        body_rows = [r for r in rows if "<td" in r]
        self.assertEqual(len(body_rows), len(self.data["questions"]))
        for row in body_rows:
            self.assertIn("blank-value", row, "closed-on cell must stay blank until a gate is closed")
            self.assertIn("source-link", row, "every board row needs an official source link")

    def test_progress_counts_add_up(self):
        summary, _, totals = build_public.gate_progress(self.data)
        self.assertEqual(sum(g["total"] for g in summary), len(self.data["questions"]))
        self.assertEqual(sum(totals.values()), len(self.data["questions"]))

    def test_no_personal_identifiers(self):
        self.assertNotIn("@", self.html)
        self.assertIsNone(re.search(r"\bAPN\s*\d", self.html))


class AdvisorSheetTests(unittest.TestCase):
    def setUp(self):
        self.data = build_timeline.merge_supplement(load_data())
        self.html = build_public.build_advisor(self.data)

    def test_one_page_print_rules_present(self):
        css = (ROOT / "assets" / "styles.css").read_text(encoding="utf-8")
        self.assertIn("@page { size: letter;", css)
        self.assertIn('class="advisor-sheet"', self.html)

    def test_blank_property_fields_are_listed_by_name_only(self):
        for field in self.data["property_fields"]:
            if field["value"] is None:
                self.assertIn(field["field"], self.html)
        for field in self.data["property_fields"]:
            self.assertIsNone(field["value"], "property fields must remain blank in the dataset")

    def test_no_personal_identifiers_or_owner_names(self):
        self.assertNotIn("@", self.html)
        self.assertIsNone(re.search(r"\bAPN\s*\d", self.html))
        self.assertIsNone(re.search(r"\b\d{1,6}\s+[A-Z][a-z]+\s+(St|Ave|Blvd|Rd|Dr)\b", self.html))

    def test_figure_rows_link_official_sources(self):
        rows = re.findall(r"<tr>.*?</tr>", self.html, flags=re.S)
        for row in rows:
            if "<td" in row:
                self.assertIn("source-link", row)


if __name__ == "__main__":
    unittest.main()
