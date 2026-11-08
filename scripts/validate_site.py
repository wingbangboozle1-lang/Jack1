#!/usr/bin/env python3
"""Validate navigation, table citations, and privacy basics for the static site."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PAGES = {"index.html", "market.html", "property.html", "decision.html", "risks.html", "flagged.html", "sources.html", "audit.html"}
PUBLIC_FILES = REQUIRED_PAGES | {"assets/styles.css", "assets/site.js", "404.html"}
OFFICIAL_DOMAINS = (
    "census.gov", "bls.gov", "scag.ca.gov", "lacity.gov", "lacity.org",
    "zimas.lacity.org", "assessor.lacounty.gov", "lacounty.gov",
    "propertytax.lacounty.gov", "sec.gov", "fema.gov", "fire.ca.gov",
    "insurance.ca.gov", "metro.net", "lausd.org", "cde.ca.gov", "irs.gov",
    "usgs.gov", "conservation.ca.gov", "ladbs.org", "waterboards.ca.gov",
    "epa.gov", "lapdonline.org", "publichealth.lacounty.gov", "dpw.lacounty.gov",
    "ttc.lacounty.gov", "emergency.lacity.gov", "climate.gov", "edd.ca.gov",
    "ladwp.com", "ftb.ca.gov", "stlouisfed.org",
)

class PageAudit(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids: list[str] = []
        self.links: list[tuple[str, str, str]] = []
        self.errors: list[str] = []
        self._in_tbody = False
        self._row: dict[str, bool] | None = None
        self.text_parts: list[str] = []
        self.table_body_rows = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = dict(attrs)
        if attrs_map.get("id"):
            self.ids.append(attrs_map["id"] or "")
        if tag == "tbody":
            self._in_tbody = True
        if tag == "tr" and self._in_tbody:
            self._row = {"official_source": False}
            self.table_body_rows += 1
        if tag == "a" and attrs_map.get("href"):
            href = attrs_map["href"] or ""
            self.links.append((href, attrs_map.get("target") or "", attrs_map.get("rel") or ""))
            parsed = urlparse(href)
            if parsed.scheme in ("http", "https"):
                host = (parsed.hostname or "").lower()
                if not any(host == domain or host.endswith("." + domain) for domain in OFFICIAL_DOMAINS):
                    self.errors.append(f"External link is not on the official-source allowlist: {href}")
                if attrs_map.get("target") == "_blank" and not {"noopener", "noreferrer"}.issubset(set((attrs_map.get("rel") or "").split())):
                    self.errors.append(f"External new-tab link lacks noopener/noreferrer: {href}")
                if self._row is not None:
                    self._row["official_source"] = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "tr" and self._row is not None:
            if not self._row["official_source"]:
                self.errors.append("A data row in a table body has no official source link")
            self._row = None
        if tag == "tbody":
            self._in_tbody = False

    def handle_data(self, data: str) -> None:
        self.text_parts.append(data)


def main() -> int:
    available_pages = {path.name for path in ROOT.glob("*.html")}
    missing = REQUIRED_PAGES - available_pages
    html_files = [ROOT / name for name in sorted(REQUIRED_PAGES) if (ROOT / name).is_file()]
    errors: list[str] = []
    if missing:
        errors.append("Missing required pages: " + ", ".join(sorted(missing)))
    if not html_files:
        errors.append("No required top-level HTML pages found")
        for error in errors:
            print("ERROR:", error)
        return 1

    known_pages = REQUIRED_PAGES
    page_ids: dict[str, set[str]] = {}
    page_links: dict[str, list[tuple[str, str, str]]] = {}

    for path in html_files:
        parser = PageAudit(path)
        parser.feed(path.read_text(encoding="utf-8"))
        if len(parser.ids) != len(set(parser.ids)):
            parser.errors.append("Duplicate id attribute")
        page_ids[path.name] = set(parser.ids)
        page_links[path.name] = parser.links
        errors.extend(f"{path.name}: {message}" for message in parser.errors)
        visible_text = " ".join(parser.text_parts)
        if re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", visible_text):
            errors.append(f"{path.name}: email address appears in rendered page text")
        if re.search(r"\b(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b", visible_text):
            errors.append(f"{path.name}: phone number appears in rendered page text")

    for page, links in page_links.items():
        for href, _target, _rel in links:
            parsed = urlparse(href)
            if parsed.scheme or href.startswith("mailto:") or href.startswith("tel:"):
                continue
            if not parsed.path:
                if parsed.fragment and parsed.fragment not in page_ids.get(page, set()):
                    errors.append(f"{page}: missing same-page anchor target: {href}")
                continue
            target_name = parsed.path
            if target_name not in PUBLIC_FILES:
                errors.append(f"{page}: relative link is outside the published file set: {href}")
                continue
            target_path = ROOT / target_name
            if not target_path.exists():
                errors.append(f"{page}: broken relative link: {href}")
                continue
            if parsed.fragment and target_path.name in known_pages and parsed.fragment not in page_ids.get(target_path.name, set()):
                errors.append(f"{page}: missing anchor target: {href}")

    if errors:
        for error in errors:
            print("ERROR:", error)
        print(f"Validation failed: {len(errors)} issue(s)")
        return 1

    table_rows = 0
    for path in html_files:
        parser = PageAudit(path)
        parser.feed(path.read_text(encoding="utf-8"))
        table_rows += parser.table_body_rows
    print(f"Validated {len(html_files)} pages and {table_rows} table-body rows. Every row has an official-source link; external links pass the allowlist; local paths and fragments resolve; no visible email/phone patterns found.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
