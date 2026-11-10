#!/usr/bin/env python3
"""Validate the curated dashboard: structure, row sources, allowlist, links, blanks, privacy.

Usage:
  python3 scripts/validate_site.py            # validate canonical root pages
  python3 scripts/validate_site.py --site _site  # validate a deployable artifact boundary
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from projection_model import build_projection_payload, load_data  # noqa: E402

PAGES = ["index.html", "market.html", "property.html", "projections.html", "decision.html", "risks.html", "requirements.html", "flagged.html", "sources.html", "audit.html"]
PUBLIC_FILES = set(PAGES) | {"404.html", "assets/styles.css", "assets/site.js", "assets/projections.json", ".nojekyll"}

ALLOWED_HOSTS = {
    "www.census.gov", "census.gov",
    "www.bls.gov", "bls.gov", "data.bls.gov",
    "labormarketinfo.edd.ca.gov",
    "fred.stlouisfed.org",
    "home.treasury.gov",
    "dof.ca.gov",
    "scag.ca.gov", "www.scag.ca.gov",
    "planning.lacity.gov", "finance.lacity.gov", "wagesla.lacity.gov",
    "portal.assessor.lacounty.gov", "assessor.lacounty.gov",
    "www.boe.ca.gov", "boe.ca.gov",
    "www.ftb.ca.gov", "ftb.ca.gov",
    "www.irs.gov", "irs.gov",
    "www.dir.ca.gov", "dir.ca.gov",
    "www.caschooldashboard.org", "caschooldashboard.org",
    "www.cde.ca.gov", "cde.ca.gov", "sd.cde.ca.gov",
    "www.sec.gov", "sec.gov",
    "www.fema.gov", "fema.gov", "hazards.fema.gov",
    "fema.maps.arcgis.com",
    "www.usgs.gov", "usgs.gov", "pubs.usgs.gov", "earthquake.usgs.gov",
    "osfm.fire.ca.gov", "www.fire.ca.gov", "fire.ca.gov",
    "www.insurance.ca.gov", "insurance.ca.gov",
    "www.lapdonline.org", "lapdonline.org",
    "www.epa.gov", "epa.gov",
    "www.portoflosangeles.org", "portoflosangeles.org",
    "github.com", "wingbangboozle1-lang.github.io",
}
# Official hosted services are allowed only for the specific FEMA/CAL FIRE resources used.
ALLOWED_HOST_PATH_PREFIXES = {
    "services.arcgis.com": ["/XG15cJAlne2vxtgt/"],
    "34c031f8-c9fd-4018-8c5a-4159cdff6b0d-cdn-endpoint.azureedge.net": ["/-/media/osfm-website/"],
    "github.com": ["/wingbangboozle1-lang/Jack1"],
    "wingbangboozle1-lang.github.io": ["/Jack1/"],
}

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}(?!\d)")
APN_RE = re.compile(r"\b\d{4}-\d{3}-\d{3}\b")
SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
CONFLICT_RE = re.compile(r"^(<{7}|>{7})(?:\s|$)", re.M)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.rows: list[dict] = []
        self._row: dict | None = None
        self._in_tbody = False
        self._in_row = False
        self._cell_text: list[str] = []
        self._in_cell = False
        self._cell_blank = False
        self._cell_has_text = False
        self.blank_cells: list[bool] = []
        self.title = ""
        self._in_title = False
        self.nav_links: list[str] = []
        self._in_nav = False
        self.tables = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
            if self._in_nav:
                self.nav_links.append(a["href"])
            if self._in_row and "source-link" in a.get("class", ""):
                self._row["source_links"].append(a["href"])
        if tag == "nav":
            self._in_nav = True
        if tag == "title":
            self._in_title = True
        if tag == "table":
            self.tables += 1
        if tag == "tbody":
            self._in_tbody = True
        if tag == "tr" and self._in_tbody:
            self._in_row = True
            self._row = {"source_links": [], "cells": 0, "blank_ok": True}
        if tag in ("td", "th") and self._in_row:
            self._in_cell = True
            self._cell_text = []
            self._cell_has_text = False
            self._cell_blank = "blank-value" in a.get("class", "")
            if tag == "td":
                self._row["cells"] += 1

    def handle_endtag(self, tag):
        if tag == "nav":
            self._in_nav = False
        if tag == "title":
            self._in_title = False
        if tag in ("td", "th") and self._in_cell:
            if self._cell_blank:
                ok = not self._cell_has_text
                self.blank_cells.append(ok)
                if not ok:
                    self._row["blank_ok"] = False
            self._in_cell = False
        if tag == "tr" and self._in_row:
            self.rows.append(self._row)
            self._in_row = False
            self._row = None
        if tag == "tbody":
            self._in_tbody = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_cell and data.strip():
            self._cell_has_text = True


def allowed_external(url: str) -> bool:
    p = urlparse(url)
    if p.scheme not in ("http", "https"):
        return False
    host = p.netloc.lower()
    if host in ALLOWED_HOST_PATH_PREFIXES:
        return any(unquote(p.path).startswith(prefix) for prefix in ALLOWED_HOST_PATH_PREFIXES[host])
    return host in ALLOWED_HOSTS


def privacy_hits(text: str) -> list[str]:
    hits = []
    for name, rx in (("email", EMAIL_RE), ("phone", PHONE_RE), ("apn", APN_RE), ("ssn", SSN_RE)):
        for m in rx.finditer(text):
            hits.append(f"{name}:{m.group(0)[:3]}…")
    if CONFLICT_RE.search(text):
        hits.append("conflict-marker")
    return hits


def validate(site: Path, artifact: bool = False) -> list[str]:
    errors: list[str] = []
    data = load_data()
    if artifact:
        actual = {str(p.relative_to(site)) for p in site.rglob("*") if p.is_file()}
        extra = actual - PUBLIC_FILES
        missing = PUBLIC_FILES - actual
        if extra:
            errors.append(f"artifact contains non-public files: {sorted(extra)}")
        if missing:
            errors.append(f"artifact missing public files: {sorted(missing)}")
    parsers: dict[str, PageParser] = {}
    for page in PAGES:
        path = site / page
        if not path.exists():
            errors.append(f"missing page: {page}")
            continue
        text = path.read_text(encoding="utf-8")
        hits = privacy_hits(text)
        if hits:
            errors.append(f"{page}: privacy/conflict hits {hits}")
        parser = PageParser()
        parser.feed(text)
        parsers[page] = parser
        if not parser.title.strip():
            errors.append(f"{page}: missing title")
        if not parser.rows:
            errors.append(f"{page}: no table rows")
        for i, row in enumerate(parser.rows, 1):
            if not row["source_links"]:
                errors.append(f"{page}: row {i} has no official source link")
            for link in row["source_links"]:
                if not allowed_external(link):
                    errors.append(f"{page}: row {i} source not allowlisted: {link}")
            if row["cells"] < 3:
                errors.append(f"{page}: row {i} has too few cells")
        if not all(parser.blank_cells):
            errors.append(f"{page}: blank-value cell contains text")
        for href in parser.links:
            if href.startswith(("http://", "https://", "mailto:", "tel:")):
                if href.startswith(("http://", "https://")) and not allowed_external(href):
                    errors.append(f"{page}: external link not allowlisted: {href}")
                continue
            if href.startswith("#"):
                frag = href[1:]
                if frag and frag not in parser.ids:
                    errors.append(f"{page}: missing fragment #{frag}")
                continue
            target = (path.parent / unquote(href.split("#")[0])).resolve()
            if not target.exists():
                errors.append(f"{page}: broken local link {href}")
            elif href.split("#")[0].endswith(".html") and "#" in href:
                frag = href.split("#", 1)[1]
                tp = PageParser()
                tp.feed(target.read_text(encoding="utf-8"))
                if frag not in tp.ids:
                    errors.append(f"{page}: missing fragment {href}")
        for nav in PAGES:
            if nav not in parser.nav_links:
                errors.append(f"{page}: nav missing {nav}")
    # Dataset integrity
    source_ids = set(data["sources"])
    for collection in ("observations", "property_fields", "decisions", "risks", "requirements", "flags", "audit"):
        for item in data[collection]:
            if not item.get("sources"):
                errors.append(f"dataset {collection} {item.get('id')}: no sources")
            for sid in item.get("sources", []):
                if sid not in source_ids:
                    errors.append(f"dataset {collection} {item.get('id')}: unknown source {sid}")
    for obs in data["observations"]:
        if obs["status"] == "unverified" and obs["value"] is not None:
            errors.append(f"dataset observation {obs['id']}: unverified value must be null")
    for field in data["property_fields"]:
        if field["value"] is not None:
            errors.append(f"dataset property field {field['id']}: must remain null")
    for sid, src in data["sources"].items():
        if not allowed_external(src["url"]):
            errors.append(f"dataset source {sid}: URL not allowlisted")
    # Generated projection data must match model
    proj_path = site / "assets" / "projections.json"
    if proj_path.exists():
        try:
            actual_payload = json.loads(proj_path.read_text(encoding="utf-8"))
            expected_payload = build_projection_payload(data)
            if actual_payload != expected_payload:
                errors.append("assets/projections.json does not match projection model")
        except json.JSONDecodeError as exc:
            errors.append(f"assets/projections.json invalid: {exc}")
    else:
        errors.append("missing assets/projections.json")
    # Flagged page must mention every flag item
    flagged_text = (site / "flagged.html").read_text(encoding="utf-8") if (site / "flagged.html").exists() else ""
    for flag in data["flags"]:
        if flag["item"] not in flagged_text:
            errors.append(f"flagged.html missing flag item: {flag['item']}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=ROOT, help="Site root to validate (default: repository root).")
    parser.add_argument("--artifact", action="store_true", help="Enforce curated artifact file boundary.")
    args = parser.parse_args()
    errors = validate(args.site, args.artifact)
    if errors:
        print("VALIDATION FAILED", file=sys.stderr)
        for err in errors:
            print(f" - {err}", file=sys.stderr)
        return 1
    rows = 0
    for page in PAGES:
        p = PageParser()
        p.feed((args.site / page).read_text(encoding="utf-8"))
        rows += len(p.rows)
    print(f"VALIDATION PASS: {len(PAGES)} pages, {rows} sourced table rows, allowlist/local links/privacy/blanks OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
