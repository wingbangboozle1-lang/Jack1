#!/usr/bin/env python3
"""Structural gate for the published dashboard.

This is a *consistency* gate, not a truth gate. It proves that the published pages are
internally coherent and that every table row carries a link to an official domain. It
cannot prove that a figure matches its source -- that is what VERIFICATION.md and
verification.html are for, and both are generated from a hand-checked register.

Checks performed:
  1. every required page exists and is non-trivial
  2. no git conflict marker survives in any published file
  3. every table-body row links to an allowlisted official domain
  4. every intentionally blank cell is adjacent to a review badge (no silent blanks)
  5. every relative link and #fragment resolves inside the published file set
  6. navigation is identical on every page and covers every published page
  7. no visible email address or phone number in rendered text
  8. every page has a title, a description and a single <h1>
  9. new-tab links carry rel="noopener noreferrer"

Exit code 1 on any violation, so the Pages workflow fails instead of publishing.
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PAGES = {
    "index.html", "market.html", "property.html", "decision.html", "projection.html",
    "risks.html", "flagged.html", "verification.html", "sources.html",
}
PUBLIC_FILES = REQUIRED_PAGES | {"assets/styles.css", "assets/site.js", ".nojekyll"}

OFFICIAL_DOMAINS = (
    "census.gov", "bls.gov", "scag.ca.gov", "lacity.gov", "lacity.org",
    "zimas.lacity.org", "assessor.lacounty.gov", "lacounty.gov",
    "propertytax.lacounty.gov", "sec.gov", "fema.gov", "fire.ca.gov",
    "insurance.ca.gov", "metro.net", "lausd.org", "cde.ca.gov", "irs.gov",
    "usgs.gov", "conservation.ca.gov", "ladbs.org", "waterboards.ca.gov",
    "epa.gov", "lapdonline.org", "publichealth.lacounty.gov", "dpw.lacounty.gov",
    "ttc.lacounty.gov", "emergency.lacity.gov", "climate.gov", "edd.ca.gov",
    "ladwp.com", "ftb.ca.gov", "noaa.gov", "stlouisfed.org", "bea.gov",
)
# Repository artefacts (a file or commit in this repo) may be cited as evidence for an audit
# row on the verification page only. They are never accepted as a data source anywhere else.
REPO_ARTIFACT_DOMAINS = ("github.com",)
CONFLICT_MARKERS = ("<<<<<<<", ">>>>>>>", "\n=======\n")


class PageAudit(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids: list[str] = []
        self.links: list[tuple[str, str, str]] = []
        self.errors: list[str] = []
        self._in_tbody = False
        self._row: dict[str, object] | None = None
        self.text_parts: list[str] = []
        self.table_body_rows = 0
        self.nav_hrefs: list[str] = []
        self._in_nav = False
        self.h1_count = 0
        self.has_description = False
        self._in_title = False
        self.title = ""

    # -- helpers ---------------------------------------------------------
    def _close_row(self) -> None:
        if self._row is None:
            return
        if not self._row.get("official_source"):
            self.errors.append(
                f"table-body row without an official-source link (row {self.table_body_rows})"
            )
        if self._row.get("has_blank") and not self._row.get("has_badge"):
            self.errors.append(
                f"intentionally blank cell without a status badge "
                f"(row {self.table_body_rows}) — blanks must be explained, never silent"
            )
        self._row = None

    # -- parser hooks ----------------------------------------------------
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"] or "")
        if tag == "meta" and (a.get("name") or "").lower() == "description" and a.get("content"):
            self.has_description = True
        if tag == "title":
            self._in_title = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "nav" and (a.get("class") or "") == "site-nav":
            self._in_nav = True
        if tag == "tbody":
            self._in_tbody = True
        if tag == "tr" and self._in_tbody:
            self._row = {"official_source": False, "has_blank": False, "has_badge": False}
            self.table_body_rows += 1
        if self._row is not None:
            cls = (a.get("class") or "")
            if "blank-value" in cls:
                self._row["has_blank"] = True
            if "badge" in cls:
                self._row["has_badge"] = True
        if tag == "a" and a.get("href"):
            href = a["href"] or ""
            rel = a.get("rel") or ""
            self.links.append((href, a.get("target") or "", rel))
            if self._in_nav:
                self.nav_hrefs.append(href)
            parsed = urlparse(href)
            if parsed.scheme in ("http", "https"):
                host = (parsed.hostname or "").lower()
                ok = any(host == d or host.endswith("." + d) for d in OFFICIAL_DOMAINS)
                if not ok and self.path.name == "verification.html":
                    ok = any(host == d or host.endswith("." + d) for d in REPO_ARTIFACT_DOMAINS)
                if not ok:
                    self.errors.append(f"external link is not on the official-source allowlist: {href}")
                if a.get("target") == "_blank" and not {"noopener", "noreferrer"}.issubset(set(rel.split())):
                    self.errors.append(f"new-tab link lacks noopener/noreferrer: {href}")
                if self._row is not None:
                    self._row["official_source"] = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "tr":
            self._close_row()
        if tag == "tbody":
            self._in_tbody = False
        if tag == "nav":
            self._in_nav = False
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        self.text_parts.append(data)
        if self._in_title:
            self.title += data


def main() -> int:
    errors: list[str] = []
    present = {p.name for p in ROOT.glob("*.html")}
    missing = REQUIRED_PAGES - present
    if missing:
        errors.append("missing required pages: " + ", ".join(sorted(missing)))

    html_files = [ROOT / n for n in sorted(REQUIRED_PAGES) if (ROOT / n).is_file()]
    if not html_files:
        print("ERROR: no required pages found")
        return 1

    # 1 - conflict markers anywhere in the published file set
    for rel in sorted(PUBLIC_FILES):
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"published file listed but absent: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in CONFLICT_MARKERS:
            if marker in text:
                errors.append(f"{rel}: git conflict marker present ({marker.strip()!r})")
        if rel != ".nojekyll" and len(text.strip()) < 200:
            errors.append(f"{rel}: published file is effectively empty")

    page_ids: dict[str, set[str]] = {}
    page_links: dict[str, list[tuple[str, str, str]]] = {}
    navs: dict[str, list[str]] = {}
    total_rows = 0
    total_blank = 0

    for path in html_files:
        parser = PageAudit(path)
        parser.feed(path.read_text(encoding="utf-8"))
        page_ids[path.name] = set(parser.ids)
        page_links[path.name] = parser.links
        navs[path.name] = parser.nav_hrefs
        total_rows += parser.table_body_rows
        total_blank += sum(1 for _ in parser.errors if "without a status badge" in _)
        errors.extend(f"{path.name}: {m}" for m in parser.errors)

        if len(parser.ids) != len(set(parser.ids)):
            errors.append(f"{path.name}: duplicate id attribute")
        if not parser.title.strip():
            errors.append(f"{path.name}: missing <title>")
        if not parser.has_description:
            errors.append(f"{path.name}: missing meta description")
        if parser.h1_count != 1:
            errors.append(f"{path.name}: expected exactly one <h1>, found {parser.h1_count}")

        visible = " ".join(parser.text_parts)
        if re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", visible):
            errors.append(f"{path.name}: email address appears in rendered text")
        if re.search(r"\b(?:\\+?1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b", visible):
            errors.append(f"{path.name}: phone number appears in rendered text")

    # 6 - navigation must be identical everywhere and cover every page
    reference_nav = navs.get("index.html", [])
    for name, nav in navs.items():
        if nav != reference_nav:
            errors.append(f"{name}: navigation differs from index.html")
    if sorted(set(reference_nav)) != sorted(REQUIRED_PAGES):
        errors.append(
            "navigation does not cover exactly the published pages: "
            f"{sorted(set(reference_nav))} vs {sorted(REQUIRED_PAGES)}"
        )

    # 5 - local links and fragments
    for page, links in page_links.items():
        for href, _target, _rel in links:
            if href.startswith(("mailto:", "tel:")):
                errors.append(f"{page}: contact link published ({href})")
                continue
            parsed = urlparse(href)
            if parsed.scheme:
                continue
            if not parsed.path:
                if parsed.fragment and parsed.fragment not in page_ids.get(page, set()):
                    errors.append(f"{page}: missing same-page anchor: {href}")
                continue
            if parsed.path not in PUBLIC_FILES:
                errors.append(f"{page}: relative link outside the published set: {href}")
                continue
            target = ROOT / parsed.path
            if not target.is_file():
                errors.append(f"{page}: broken relative link: {href}")
                continue
            if parsed.fragment and parsed.path in REQUIRED_PAGES:
                if parsed.fragment not in page_ids.get(parsed.path, set()):
                    errors.append(f"{page}: missing anchor target: {href}")

    if errors:
        for e in errors:
            print("ERROR:", e)
        print(f"Validation failed: {len(errors)} issue(s)")
        return 1

    print(
        f"Validated {len(html_files)} published pages and {total_rows} table-body rows:\n"
        f"  - every row links to an allowlisted official domain\n"
        f"  - every intentionally blank cell carries a status badge\n"
        f"  - no conflict markers, no emails, no phone numbers in published files\n"
        f"  - navigation identical across all {len(html_files)} pages and covers each one\n"
        f"  - all relative links and fragments resolve; new-tab links are safely rel'd"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
