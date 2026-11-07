#!/usr/bin/env python3
"""Authoritative gate for the decision brief: dataset, HTML, links, PII, deploy artifact.

Run by CI before deploy. Fails closed on any of these:

  * a dataset row with no official source, a blank verified value, a filled unverified value,
    a missing flag, a duplicate id, an unknown source or an unapproved domain;
  * a scenario anchor not traceable to a verified row and its official publisher;
  * a generated page with a duplicate id, a broken relative link, a missing fragment,
    an unapproved external link, a new-tab link without noopener/noreferrer, or a table row
    with no official source link;
  * personal information in any published page or dataset (email, phone, SSN, APN, street
    address, person-name labels);
  * a flagged row or irregularity missing from flagged.html, a source missing from
    sources.html, or a dataset row missing from its own category page;
  * a canonical page missing from the GitHub Pages deployment artifact;
  * an archived prior-session HTML page without a superseded/noindex banner;
  * a failing projection engine self-test.
"""
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

# Suffixes of official publisher hosts. github.com is included only for repository-state
# evidence (conflict repair, workflow, PRs) on the Flagged for Review page.
OFFICIAL_DOMAINS = {
    "census.gov", "bls.gov", "bea.gov", "dof.ca.gov", "edd.ca.gov", "dir.ca.gov",
    "cde.ca.gov", "caschooldashboard.org", "scag.ca.gov", "lacity.gov", "lacity.org",
    "lacounty.gov", "assessor.lacounty.gov", "metro.net", "fire.ca.gov",
    "insurance.ca.gov", "usgs.gov", "conservation.ca.gov", "waterboards.ca.gov",
    "epa.gov", "fema.gov", "irs.gov", "ftb.ca.gov", "treasury.gov", "stlouisfed.org",
    "sec.gov", "climate.gov", "noaa.gov", "lapdonline.org", "publichealth.lacounty.gov",
    "ladwp.com", "lausd.org", "github.com",
}

CANONICAL_PAGES = [
    "index.html", "decision.html", "projection.html", "property.html", "tenant.html",
    "market.html", "geography.html", "demographics.html", "income.html", "employment.html",
    "schools.html", "economy.html", "hazards.html", "regulatory.html", "risks.html",
    "sources.html", "flagged.html", "privacy.html", "scope.html",
]
ALIAS_PAGES = ["model.html", "risk.html"]
ALL_ROOT_PAGES = CANONICAL_PAGES + ALIAS_PAGES + ["404.html"]
PUBLIC_FILES = set(ALL_ROOT_PAGES) | {
    "assets/brief.css", "assets/brief.js", "assets/styles.css", "assets/site.js",
    "assets/style.css", "assets/site.js", ".nojekyll", "robots.txt", "sitemap.xml",
}

PII_PATTERNS = {
    "email": re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
    "phone": re.compile(r"\b(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "apn": re.compile(r"\b\d{4}[- ]\d{3}[- ]\d{3}\b"),
    "street address": re.compile(
        r"\b\d{1,6}\s+(?:N|S|E|W|North|South|East|West)?\.?\s+[A-Z][a-zA-Z]+\s+"
        r"(?:St|Street|Ave|Avenue|Blvd|Boulevard|Rd|Road|Dr|Drive|Pl|Place|Way|Ln|Lane|Ct|Court)\b"
    ),
    "person-name label": re.compile(
        r"(?:Owner|Landlord|Tenant|Guarantor|Borrower|Buyer|Seller|APN|Assessor Parcel Number)\s*[:=]\s*"
        r"[A-Z][a-z]+\s+[A-Z][a-z]+"
    ),
}

REQUIRED_PRIVACY_TERMS = ("no personal information", "anonymized", "flagged")


def allowed(host: str) -> bool:
    host = (host or "").lower()
    return any(host == d or host.endswith("." + d) for d in OFFICIAL_DOMAINS)


class PageAudit(HTMLParser):
    def __init__(self, name: str):
        super().__init__(convert_charrefs=True)
        self.name = name
        self.ids: list[str] = []
        self.links: list[str] = []
        self.external: list[str] = []
        self.errors: list[str] = []
        self.text: list[str] = []
        self.rows = 0
        self.rows_without_link = 0
        self._in_tbody = False
        self._row_has_official = False
        self._in_row = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "tbody":
            self._in_tbody = True
        if tag == "tr" and self._in_tbody:
            self._in_row = True
            self._row_has_official = False
            self.rows += 1
        if tag == "a" and a.get("href"):
            href = a["href"] or ""
            self.links.append(href)
            p = urlparse(href)
            if p.scheme in ("http", "https"):
                self.external.append(href)
                if not allowed(p.hostname):
                    self.errors.append(f"External link not on official allowlist: {href}")
                if a.get("target") == "_blank":
                    rel = set((a.get("rel") or "").split())
                    if not {"noopener", "noreferrer"}.issubset(rel):
                        self.errors.append(f"New-tab link lacks noopener/noreferrer: {href}")
                if not p.scheme == "https":
                    self.errors.append(f"External link is not HTTPS: {href}")
                if self._in_row and allowed(p.hostname):
                    self._row_has_official = True
            elif p.scheme:
                self.errors.append(f"Non-web external link: {href}")

    def handle_endtag(self, tag):
        if tag == "tr" and self._in_row:
            if not self._row_has_official:
                self.rows_without_link += 1
                self.errors.append("A table-body row has no official source link")
            self._in_row = False
        if tag == "tbody":
            self._in_tbody = False

    def handle_data(self, data):
        self.text.append(data)


def error_log(errors: list[str]) -> None:
    for e in errors:
        print("ERROR:", e)


def pii_scan(name: str, text: str, errors: list[str]) -> None:
    for label, pat in PII_PATTERNS.items():
        m = pat.search(text)
        if m:
            errors.append(f"{name}: possible {label} in published text: {m.group(0)!r}")


def check_dataset(errors: list[str]):
    rows = json.loads((ROOT / "data/brief_rows.json").read_text(encoding="utf-8"))["rows"]
    srcs = json.loads((ROOT / "data/brief_sources.json").read_text(encoding="utf-8"))["sources"]
    fl = json.loads((ROOT / "data/brief_flags.json").read_text(encoding="utf-8"))["irregularities"]
    sc = json.loads((ROOT / "data/brief_scenarios.json").read_text(encoding="utf-8"))

    for fname in ("data/brief_rows.json", "data/brief_sources.json", "data/brief_flags.json", "data/brief_scenarios.json"):
        pii_scan(fname, (ROOT / fname).read_text(encoding="utf-8"), errors)

    ids = [r["id"] for r in rows]
    for rid in sorted({i for i in ids if ids.count(i) > 1}):
        errors.append(f"Duplicate row id: {rid}")
    by_id = {r["id"]: r for r in rows}

    valid_pages = {Path(p).stem for p in CANONICAL_PAGES}
    flag_ids = set()
    for r in rows:
        rid = r["id"]
        if r["page"] not in valid_pages:
            errors.append(f"{rid}: unknown page {r['page']}")
        if not r["group"] or not r["metric"] or not r["finding"]:
            errors.append(f"{rid}: empty group, metric or finding")
        if not r["sources"]:
            errors.append(f"{rid}: no official source")
        for sid in r["sources"]:
            if sid not in srcs:
                errors.append(f"{rid}: unknown source id {sid}")
        if r["status"] == "verified":
            if not r["value"].strip():
                errors.append(f"{rid}: verified row has a blank value")
            if r["flag"]:
                errors.append(f"{rid}: verified row carries a flag")
        elif r["status"] == "unverified":
            if r["value"].strip():
                errors.append(f"{rid}: unverified row has a filled value (never infer)")
            if not r["flag"].startswith("U-"):
                errors.append(f"{rid}: unverified row lacks a U- flag")
            if r["flag"] in flag_ids:
                errors.append(f"{rid}: duplicate flag {r['flag']}")
            flag_ids.add(r["flag"])
        else:
            errors.append(f"{rid}: invalid status {r['status']}")

    for sid, s in srcs.items():
        p = urlparse(s["url"])
        if p.scheme != "https" or not allowed(p.hostname):
            errors.append(f"source {sid}: URL not an official HTTPS host: {s['url']}")
        if not s.get("publisher") or not s.get("title"):
            errors.append(f"source {sid}: missing publisher or title")

    irr_ids = set()
    for f in fl:
        if f["id"] in irr_ids:
            errors.append(f"duplicate irregularity id {f['id']}")
        irr_ids.add(f["id"])
        if not f["links"]:
            errors.append(f"{f['id']}: no official link")
        for u in f["links"]:
            p = urlparse(u)
            if p.scheme != "https" or not allowed(p.hostname):
                errors.append(f"{f['id']}: link not an official HTTPS host: {u}")

    for a in sc["anchors"]:
        r = by_id.get(a["row"])
        if r is None:
            errors.append(f"scenario anchor {a['key']}: missing row {a['row']}")
        elif r["status"] != "verified" or a["source"] not in r["sources"]:
            errors.append(f"scenario anchor {a['key']}: not backed by its verified official row")
        if not isinstance(a["value"], (int, float)):
            errors.append(f"scenario anchor {a['key']}: non-numeric value")
    scen_ids = [s["id"] for s in sc["scenarios"]]
    if len(scen_ids) != len(set(scen_ids)):
        errors.append("duplicate scenario id")
    for s in sc["scenarios"]:
        if s["decision_row"] not in by_id:
            errors.append(f"scenario {s['id']}: missing decision row {s['decision_row']}")
    return rows, srcs, fl, sc


def check_pages(rows, srcs, fl, errors: list[str]):
    page_ids: dict[str, set[str]] = {}
    all_parsed: dict[str, PageAudit] = {}
    for name in ALL_ROOT_PAGES:
        path = ROOT / name
        if not path.is_file():
            errors.append(f"Missing canonical page: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"^(<<<<<<<|=======|>>>>>>>)", text, re.M):
            errors.append(f"{name}: unresolved conflict marker")
        if "<<<<<<<" in text or ">>>>>>>" in text:
            errors.append(f"{name}: conflict-marker text present")
        p = PageAudit(name)
        p.feed(text)
        all_parsed[name] = p
        page_ids[name] = set(p.ids)
        if len(p.ids) != len(set(p.ids)):
            errors.append(f"{name}: duplicate id attribute")
        errors.extend(f"{name}: {e}" for e in p.errors)
        pii_scan(name, " ".join(p.text), errors)

    # relative links and fragments, across canonical root pages
    for name, p in all_parsed.items():
        for href in p.links:
            u = urlparse(href)
            if u.scheme or href.startswith(("mailto:", "tel:")):
                continue
            if not u.path:
                if u.fragment and u.fragment not in page_ids.get(name, set()):
                    errors.append(f"{name}: missing same-page fragment #{u.fragment}")
                continue
            target = u.path.lstrip("/")
            if target not in PUBLIC_FILES:
                errors.append(f"{name}: link outside published file set: {href}")
                continue
            target_path = ROOT / target
            if not target_path.is_file():
                errors.append(f"{name}: broken relative link: {href}")
                continue
            if u.fragment and target.endswith(".html"):
                if u.fragment not in page_ids.get(target_path.name, set()):
                    errors.append(f"{name}: missing fragment in {target}: {href}")

    # every dataset row must appear on its category page, with its id
    for r in rows:
        target = r["page"] + ".html"
        if target not in all_parsed:
            continue
        if f'>{r["id"]}<' not in (ROOT / target).read_text(encoding="utf-8"):
            errors.append(f"{r['id']}: row missing from {target}")
        if r["status"] == "unverified":
            txt = (ROOT / target).read_text(encoding="utf-8")
            if 'col-value--blank' not in txt:
                errors.append(f"{target}: no blank value cells rendered")
            if r["flag"] not in txt:
                errors.append(f"{r['id']}: flag {r['flag']} missing from {target}")

    # flagged page completeness
    flagged_text = (ROOT / "flagged.html").read_text(encoding="utf-8")
    for r in rows:
        if r["status"] == "unverified" and r["flag"] not in flagged_text:
            errors.append(f"{r['flag']}: missing from flagged.html")
    for f in fl:
        if f["id"] not in flagged_text:
            errors.append(f"{f['id']}: missing from flagged.html")
    if "Flagged for Review" not in flagged_text:
        errors.append("flagged.html: missing 'Flagged for Review' heading")

    # sources page completeness
    sources_text = (ROOT / "sources.html").read_text(encoding="utf-8")
    for sid, s in srcs.items():
        if f">{sid}<" not in sources_text:
            errors.append(f"{sid}: missing from sources.html")
        if html.escape(s["url"], quote=True) not in sources_text:
            errors.append(f"{sid}: official URL missing from sources.html")

    # privacy page must state the posture
    privacy_text = (ROOT / "privacy.html").read_text(encoding="utf-8").lower()
    for term in REQUIRED_PRIVACY_TERMS:
        if term not in privacy_text:
            errors.append(f"privacy.html: missing privacy term {term!r}")
    return all_parsed


def check_archives(errors: list[str]) -> int:
    count = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if ".git" in path.parts or (len(rel.parts) == 1 and path.name in ALL_ROOT_PAGES):
            continue
        count += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        if "data-legacy-superseded" not in text:
            errors.append(f"{rel}: archived prior-session page lacks a superseded banner")
        if "noindex" not in text:
            errors.append(f"{rel}: archived prior-session page lacks a noindex directive")
        pii_scan(str(rel), re.sub(r"<[^>]+>", " ", text), errors)
        if re.search(r"^(<<<<<<<|=======|>>>>>>>)", text, re.M):
            errors.append(f"{rel}: unresolved conflict marker")
    return count


def check_deploy(errors: list[str]) -> None:
    wf = ROOT / ".github/workflows/pages.yml"
    if not wf.is_file():
        errors.append("Missing .github/workflows/pages.yml")
        return
    text = wf.read_text(encoding="utf-8")
    for name in ALL_ROOT_PAGES:
        if name not in text:
            errors.append(f"deploy artifact missing canonical page: {name}")
    for asset in ("assets/brief.css", "assets/brief.js", ".nojekyll", "robots.txt", "sitemap.xml"):
        if asset not in text:
            errors.append(f"deploy artifact missing: {asset}")
    if not (ROOT / ".nojekyll").is_file():
        errors.append("Missing .nojekyll")
    if "python tools/verify_brief.py" not in text and "python scripts/validate_site.py" not in text:
        errors.append("Pages workflow does not run the verification gate")
    if "cp " not in text:
        errors.append("Pages workflow has no artifact assembly step")


def check_coordination(errors: list[str]) -> None:
    p = ROOT / "COORDINATION.md"
    if not p.is_file():
        errors.append("Missing COORDINATION.md")
        return
    text = p.read_text(encoding="utf-8")
    if re.search(r"^(<<<<<<<|=======|>>>>>>>)", text, re.M):
        errors.append("COORDINATION.md: unresolved conflict markers")
    if "arena/dac604b9-jack1" not in text:
        errors.append("COORDINATION.md: current session board missing")


def main() -> int:
    errors: list[str] = []
    rows, srcs, fl, sc = check_dataset(errors)
    parsed = check_pages(rows, srcs, fl, errors)
    archived = check_archives(errors)
    check_deploy(errors)
    check_coordination(errors)

    test = subprocess.run(
        [sys.executable, str(ROOT / "tools/projection.py"), "--self-test"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    if test.returncode != 0:
        errors.append("projection engine self-test failed: " + (test.stderr or test.stdout).strip()[:400])

    if errors:
        error_log(errors)
        print(f"Verification FAILED: {len(errors)} issue(s)")
        return 1

    table_rows = sum(p.rows for p in parsed.values())
    external = sum(len(p.external) for p in parsed.values())
    print(
        f"Verification OK: {len(parsed)} canonical pages, {len(rows)} dataset rows "
        f"({sum(1 for r in rows if r['status'] == 'verified')} verified / "
        f"{sum(1 for r in rows if r['status'] == 'unverified')} blank+flagged), "
        f"{len(srcs)} official sources, {len(fl)} irregularities, "
        f"{table_rows} published table rows, {external} official links, "
        f"{archived} archived pages labelled superseded. "
        "Every table row has an official source link; no broken links; no PII; "
        "no unverified value was filled."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
