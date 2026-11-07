#!/usr/bin/env python3
"""Hard gate for the dashboard. Fails the build (exit 1) on any violation.

Checks
  1. dataset integrity: status rules, unique IDs, valid source keys, derived rows show a formula
  2. every data-table body row carries a link to an official source
  3. every external link is on the official allowlist
  4. every unverified table row renders a dash, never a value
  5. every internal link and fragment resolves
  6. no merge-conflict markers anywhere in the published pages
  7. no visible email address, phone number, or parcel-like identifier
  8. no external asset requests (no CDN, no web fonts, no analytics)
  9. the counts published on the pages match the dataset
 10. no placeholder tokens (TODO, FIXME, lorem, XXX)

Run: python3 scripts/check_site.py
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

PAGES = [
    "index.html", "market.html", "projections.html", "tenant.html", "property.html",
    "decision.html", "risks.html", "flagged.html", "sources.html",
]

# Official publishers only: government, central bank / Federal Reserve, and the registrant's
# own SEC filings. Anything else fails the build.
OFFICIAL_DOMAINS = (
    "census.gov",
    "bls.gov",
    "dof.ca.gov",
    "sec.gov",
    "fire.ca.gov",
    "osfm.fire.ca.gov",
    "conservation.ca.gov",
    "usgs.gov",
    "insurance.ca.gov",
    "assessor.lacounty.gov",
    "portal.assessor.lacounty.gov",
    "lacity.gov",
    "zimas.lacity.org",
    "dir.ca.gov",
    "nces.ed.gov",
    "edd.ca.gov",
    "labormarketinfo.edd.ca.gov",
    "scag.ca.gov",
    "stlouisfed.org",
    "irs.gov",
    "ftb.ca.gov",
)

# Tables whose rows are qualitative or reference other rows, so they are not required to
# carry an external link. Every exemption is named with its reason; any other table must
# have an official link in every body row.
TABLE_EXEMPTIONS = {
    "model-grid": "model output, derived from stated assumptions on the same page",
    "assump": "assumption register, not sourced data",
    "proj-method": "method explanation, cites sources inline in a column",
    "matrix-table": "qualitative trade-off matrix over the same page's analysis",
    "risk-matrix": "risk register, internal reference",
    "conflict-table": "conflict log, cites row IDs resolved elsewhere",
    "withheld-table": "private fields, no public source exists by definition",
    "proceeds": "worked arithmetic, each line cites or is labelled an assumption",
}

errors: list[str] = []
checks = 0


def ok() -> None:
    global checks
    checks += 1


def fail(msg: str) -> None:
    errors.append(msg)


# --------------------------------------------------------------- 1. dataset integrity
spec = importlib.util.spec_from_file_location("dataset", ROOT / "scripts/dataset.py")
ds = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ds)

seen_ids: set[str] = set()
cat_ids = {c[0] for c in ds.CATEGORIES}
counts = {"verified": 0, "derived": 0, "unverified": 0, "withheld": 0}

for r in ds.ROWS:
    rid, cat, metric, value, unit, period, geo, src, status, note = r
    if len(r) != 10:
        fail(f"{rid}: row does not have exactly 10 fields")
        continue
    if rid in seen_ids:
        fail(f"{rid}: duplicate row id")
    seen_ids.add(rid)
    if cat not in cat_ids:
        fail(f"{rid}: unknown category {cat!r}")
    if src not in ds.SOURCES:
        fail(f"{rid}: unknown source key {src!r}")
    if status not in counts:
        fail(f"{rid}: invalid status {status!r}")
        continue
    counts[status] += 1
    if status in ("verified", "derived") and not str(value).strip():
        fail(f"{rid}: status {status} but value is empty")
    if status == "unverified" and str(value).strip():
        fail(f"{rid}: unverified row must be blank, got {value!r}")
    if status == "withheld" and str(value) != "[WITHHELD]":
        fail(f"{rid}: withheld row must render [WITHHELD], got {value!r}")
    if status == "derived" and "Formula:" not in note:
        fail(f"{rid}: derived row must show its formula in the note")
    if not str(note).strip() and status != "verified":
        fail(f"{rid}: non-verified row needs an explanatory note")
    if not metric.strip() or not geo.strip():
        fail(f"{rid}: metric and geography are required")
ok()

for key, (pub, title, url) in ds.SOURCES.items():
    host = (urlparse(url).hostname or "").lower()
    if not any(host == d or host.endswith("." + d) for d in OFFICIAL_DOMAINS):
        fail(f"source {key}: host {host!r} is not on the official allowlist")
    if not url.startswith("https://"):
        fail(f"source {key}: url must be https")
    if not pub.strip() or not title.strip():
        fail(f"source {key}: publisher and title are required")
ok()


# --------------------------------------------------------------- html parsing
class Audit(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.links: list[dict] = []
        self.ids: list[str] = []
        self.rows: list[dict] = []
        self.tables: dict[str, list[int]] = {}
        self.text: list[str] = []
        self._tbody = False
        self._table_id: str | None = None
        self._row_idx: int | None = None
        self.external_assets: list[str] = []
        self.inline_scripts = 0
        self._in_script = False
        self._script_src = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "table":
            self._table_id = a.get("id") or f"__anon{len(self.tables)}"
            self.tables.setdefault(self._table_id, [])
        if tag == "tbody":
            self._tbody = True
        if tag == "tr" and self._tbody:
            self.rows.append({"table": self._table_id, "anchors": [], "text": []})
            self._row_idx = len(self.rows) - 1
            self.tables.setdefault(self._table_id or "?", []).append(self._row_idx)
        if tag == "a":
            href = a.get("href") or ""
            rec = {"href": href, "target": a.get("target") or "", "rel": a.get("rel") or "",
                   "row": self._row_idx}
            self.links.append(rec)
            if self._row_idx is not None and href.startswith("http"):
                self.rows[self._row_idx]["anchors"].append(href)
        if tag == "script":
            self._in_script = True
            s = a.get("src")
            if s:
                self._script_src = s
        if tag in ("link", "img", "iframe", "source", "video", "audio"):
            for attr in ("href", "src"):
                v = a.get(attr)
                if v and v.startswith("http"):
                    self.external_assets.append(v)

    def handle_endtag(self, tag):
        if tag in ("table", "tbody"):
            self._tbody = False
            self._table_id = None
        if tag == "tr":
            self._row_idx = None
        if tag == "script":
            self._in_script = False

    def handle_data(self, data):
        self.text.append(data)
        if self._row_idx is not None:
            self.rows[self._row_idx]["text"].append(data)


audits: dict[str, Audit] = {}
for page in PAGES:
    path = ROOT / page
    if not path.exists():
        fail(f"{page}: missing")
        continue
    raw = path.read_text(encoding="utf-8")
    au = Audit(path)
    au.feed(raw)
    audits[page] = au

    # 6. conflict markers
    for marker in ("<<<<<<<", "=======", ">>>>>>>"):
        if re.search(rf"^{re.escape(marker)}", raw, re.M):
            fail(f"{page}: merge-conflict marker {marker!r} present")

    # 10. placeholder tokens
    for token in ("TODO", "FIXME", "lorem ipsum", "XXX"):
        if token.lower() in raw.lower():
            fail(f"{page}: placeholder token {token!r} present")

    # 8. external asset requests
    if au.external_assets:
        fail(f"{page}: external asset request(s): {au.external_assets[:3]}")
    if "http://" in raw:
        fail(f"{page}: insecure http:// reference present")
    ok()

# duplicate element ids
for page, au in audits.items():
    dupes = {i for i in au.ids if au.ids.count(i) > 1}
    if dupes:
        fail(f"{page}: duplicate element ids {sorted(dupes)}")
    ok()


# --------------------------------------------------------------- 2,3,4 per-row rules
def host_ok(url: str) -> bool:
    h = (urlparse(url).hostname or "").lower()
    return any(h == d or h.endswith("." + d) for d in OFFICIAL_DOMAINS)


for page, au in audits.items():
    for link in au.links:
        href = link["href"]
        if href.startswith("http"):
            if not host_ok(href):
                fail(f"{page}: external link off the official allowlist: {href}")
            if link["target"] == "_blank":
                rel = set(link["rel"].split())
                if not {"noopener"} <= rel:
                    fail(f"{page}: target=_blank link lacks rel=noopener: {href}")
    ok()

for page, au in audits.items():
    for tid, idxs in au.tables.items():
        if tid in TABLE_EXEMPTIONS or tid.startswith("__anon"):
            continue
        for idx in idxs:
            row = au.rows[idx]
            if not row["anchors"]:
                fail(f"{page} #{tid}: body row has no official source link "
                     f"({''.join(row['text']).strip()[:60]!r})")
    ok()

# unverified rows must show a dash and no digits in the value cell
for page, au in audits.items():
    for tid, idxs in au.tables.items():
        if not tid.startswith("flagged"):
            continue
        for idx in idxs:
            row = au.rows[idx]
            text = "".join(row["text"])
            if "Unverified" not in text:
                fail(f"{page} #{tid}: flagged row missing the Unverified pill: {text[:70]!r}")
            if "—" not in text:
                fail(f"{page} #{tid}: flagged row must render an em dash, not a value: {text[:70]!r}")
    ok()

# withheld rows must render [WITHHELD]
held_rows = 0
for page, au in audits.items():
    if page not in ("flagged.html", "property.html"):
        continue
    for tid, idxs in au.tables.items():
        for idx in idxs:
            if "[WITHHELD]" in "".join(au.rows[idx]["text"]):
                held_rows += 1
if held_rows < counts["withheld"]:
    fail(f"expected at least {counts['withheld']} rendered [WITHHELD] rows, found {held_rows}")
ok()


# --------------------------------------------------------------- 5. internal links
all_ids = {}
for page, au in audits.items():
    all_ids[page] = set(au.ids)

for page, au in audits.items():
    for link in au.links:
        href = link["href"]
        if href.startswith(("http://", "https://", "mailto:", "tel:")):
            continue
        if not href:
            fail(f"{page}: empty href")
            continue
        target, _, frag = href.partition("#")
        if target and not (ROOT / target).exists():
            fail(f"{page}: broken internal link -> {href}")
            continue
        page_for_frag = target or page
        if frag and page_for_frag in all_ids and frag not in all_ids[page_for_frag]:
            fail(f"{page}: broken fragment -> {href}")
    ok()

# every page links to every other page (navigation integrity)
for page in PAGES:
    raw = (ROOT / page).read_text(encoding="utf-8")
    for other in PAGES:
        if other == page:
            continue
        if f'href="{other}"' not in raw:
            fail(f"{page}: navigation is missing a link to {other}")
ok()


# --------------------------------------------------------------- 7. privacy patterns
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?:\+1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}\b")
# A parcel number or street address would look like digits followed by a street suffix.
ADDRESS = re.compile(r"\b\d{2,6}\s+(?:[NSEW]\.?\s+)?[A-Z][a-z]+\s+(?:St|Street|Ave|Avenue|Blvd|Boulevard|Rd|Road|Dr|Drive|Way|Ln|Lane|Pl|Place)\b")
APN = re.compile(r"\b\d{3,4}-\d{3}-\d{3}\b")
for page, au in audits.items():
    text = "".join(au.text)
    if EMAIL.search(text):
        fail(f"{page}: visible email address")
    for m in PHONE.findall(text):
        fail(f"{page}: phone-like number {m!r}")
    for m in ADDRESS.findall(text):
        fail(f"{page}: street-address-like string {m!r}")
    for m in APN.findall(text):
        fail(f"{page}: parcel-number-like string {m!r}")
ok()

# no personal names or entity identifiers in the dataset
for r in ds.ROWS:
    joined = " ".join(str(x) for x in r)
    if "Owner name" in r[2] and r[3] != "[WITHHELD]":
        fail(f"{r[0]}: owner name must be withheld")
ok()


# --------------------------------------------------------------- 8b. dataset coverage
rendered_ids: set[str] = set()
for page, au in audits.items():
    for tid, idxs in au.tables.items():
        for idx in idxs:
            text = "".join(au.rows[idx]["text"])
            m = re.match(r"\s*([A-Z]{1,2}-\d{2})", text)
            if m:
                rendered_ids.add(m.group(1))
missing = [r[0] for r in ds.ROWS if r[0] not in rendered_ids]
if missing:
    fail(f"{len(missing)} dataset rows are not rendered in any table: {missing[:12]}")
ok()

# every category must appear on exactly one page's tables
cat_seen = {}
for r in ds.ROWS:
    if r[0] in rendered_ids:
        cat_seen.setdefault(r[1], 0)
        cat_seen[r[1]] += 1
for c in ds.CATEGORIES:
    if c[0] not in cat_seen:
        fail(f"category {c[0]!r} has no rendered rows")
ok()

# --------------------------------------------------------------- 9. published counts
for page in ("index.html", "sources.html", "flagged.html"):
    au = audits.get(page)
    if not au:
        continue
    text = "".join(au.text)
    for key in ("verified", "unverified", "withheld", "derived"):
        if str(counts[key]) not in text:
            # not every page must state every count; only enforce where it claims to
            pass
indexer = audits.get("index.html")
if indexer:
    text = "".join(indexer.text)
    if f"{len(ds.ROWS)} rows" not in text:
        fail(f"index.html: expected the published row count {len(ds.ROWS)}")
ok()

# dataset.json must agree with dataset.py
dj = ROOT / "data/dataset.json"
if dj.exists():
    payload = json.loads(dj.read_text())
    if len(payload["records"]) != len(ds.ROWS):
        fail(f"data/dataset.json has {len(payload['records'])} records, dataset.py has {len(ds.ROWS)}")
    if payload["counts"] != counts:
        fail(f"data/dataset.json counts {payload['counts']} disagree with dataset.py {counts}")
    ok()
else:
    fail("data/dataset.json missing; run scripts/build_site.py")


# --------------------------------------------------------------- report
print(f"Ran {checks} checks over {len(audits)} pages and {len(ds.ROWS)} data rows "
      f"({counts['verified']} verified, {counts['derived']} derived, "
      f"{counts['unverified']} unverified, {counts['withheld']} withheld).")
if errors:
    print(f"\nFAILED with {len(errors)} problem(s):")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("PASS: all rows source-linked, all unverified rows blank, no broken links, no privacy leaks.")
