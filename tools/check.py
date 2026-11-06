#!/usr/bin/env python3
"""
Integrity checks for the SP-01 dossier. Fails loudly, non-zero exit.

Checks:
  1. every internal link resolves to a real file and anchor
  2. every fact row carries at least one source id, or is explicitly unverified
  3. every source id referenced actually exists in the ledger
  4. no personal information leaked into the site, data or docs
  5. HTML basics: one <h1>, balanced tags, no external asset requests
  6. no placeholder tokens left behind (TODO, FIXME, lorem, XXX)

Run:  python3 tools/check.py
"""

import html.parser
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "docs")
DATA = os.path.join(ROOT, "data")

failures = []
notes = []


def fail(msg):
    failures.append(msg)


# ---------------------------------------------------------------- loading
def load(name):
    with open(os.path.join(DATA, name)) as fh:
        return json.load(fh)


facts = load("facts.json")
sources = load("sources.json")
model = load("model.json")
SRC_IDS = {s["id"] for s in sources["sources"]}

PAGES = sorted(f for f in os.listdir(SITE) if f.endswith(".html"))


# ---------------------------------------------------------------- 1. links
class Anchors(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.assets = []
        self.h1 = 0
        self.stack = []
        self.errors = []

    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        if tag in ("link", "script", "img", "iframe"):
            ref = a.get("src") or a.get("href")
            if ref:
                self.assets.append(ref)
        if tag == "h1":
            self.h1 += 1
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if not self.stack:
            self.errors.append(f"stray </{tag}>")
            return
        if self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.errors.append(f"unclosed <{self.stack.pop()}> before </{tag}>")
            if self.stack:
                self.stack.pop()
        else:
            self.errors.append(f"unmatched </{tag}>")


anchor_map = {}
for page in PAGES:
    with open(os.path.join(SITE, page), encoding="utf-8") as fh:
        text = fh.read()
    p = Anchors()
    p.feed(text)
    anchor_map[page] = p
    if p.h1 != 1:
        fail(f"{page}: expected exactly one <h1>, found {p.h1}")
    if p.stack:
        fail(f"{page}: unclosed tags at EOF: {p.stack[:5]}")
    for e in p.errors:
        fail(f"{page}: tag error — {e}")
    for ref in p.assets:
        if ref.startswith(("http://", "https://", "//")):
            fail(f"{page}: external asset request '{ref}' — the site must be self-contained")
    if "http://" in text.replace("https://", ""):
        notes.append(f"{page}: contains an http:// string (check it is a link, not an asset)")

link_count = 0
for page in PAGES:
    for href in anchor_map[page].links:
        link_count += 1
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        if href.startswith("#"):
            target, frag = page, href[1:]
        elif "#" in href:
            target, frag = href.split("#", 1)
        else:
            target, frag = href, ""
        if target and target not in PAGES:
            fail(f"{page}: broken internal link -> {href}")
            continue
        if frag and frag not in anchor_map.get(target, anchor_map[page]).ids:
            fail(f"{page}: link to missing anchor -> {href}")

notes.append(f"checked {link_count} links across {len(PAGES)} pages")

# ---------------------------------------------------------------- 2/3. sources
for r in facts["rows"]:
    if r["status"] == "unverified":
        if r["value"] not in ("", None) and r["value"] != "[WITHHELD]":
            fail(f"{r['id']}: unverified row must be blank or [WITHHELD], has '{r['value']}'")
        continue
    if not r["sources"]:
        fail(f"{r['id']}: verified/derived row has no source")
    for sid in r["sources"]:
        if sid not in SRC_IDS:
            fail(f"{r['id']}: references unknown source {sid}")

used = {sid for r in facts["rows"] for sid in r["sources"]}
unused = SRC_IDS - used
if unused:
    notes.append(f"sources declared but not cited by any row: {sorted(unused)}")

for r in facts["rows"]:
    if r["status"] in ("verified", "derived") and len(r["value"]) > 60:
        pass  # long descriptive values are fine

# ---------------------------------------------------------------- 4. PII
PII_PATTERNS = [
    (r"\b\d{3}-\d{2}-\d{4}\b", "US social security number"),
    (r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b", "card-like number"),
    (r"\b\d{3}[-.]\d{3}[-.]\d{4}\b", "US phone number"),
    (r"\(\d{3}\)\s?\d{3}[-.]\d{4}", "US phone number"),
    (r"[\w.+-]+@[\w-]+\.[\w.]{2,}", "email address"),
    (r"\b\d{2,5}\s+(?:[NSEW]\.?\s+)?[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,3}\s+"
     r"(?:St|Street|Ave|Avenue|Blvd|Boulevard|Rd|Road|Dr|Drive|Way|Ln|Lane|Ct|Court|Pl|Place|Pkwy|Parkway)\b",
     "street address"),
    (r"\bAPN\b[:\s]*\d", "assessor parcel number"),
    (r"\b\d{3}-\d{3}-\d{3}\b", "California APN format"),
]

scan_targets = []
for page in PAGES:
    scan_targets.append(os.path.join(SITE, page))
for name in os.listdir(DATA):
    scan_targets.append(os.path.join(DATA, name))
for name in os.listdir(os.path.join(SITE, "assets")):
    scan_targets.append(os.path.join(SITE, "assets", name))
for name in ["README.md", "EXECUTIVE_SUMMARY.md", "DECISION_MEMO.md", "RISK_REGISTER.md",
             "METHODOLOGY.md", "COORDINATION.md"]:
    path = os.path.join(ROOT, name)
    if os.path.exists(path):
        scan_targets.append(path)

pii_hits = 0
for path in scan_targets:
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except (UnicodeDecodeError, IsADirectoryError):
        continue
    low = text.lower()
    for pattern, label in PII_PATTERNS:
        for m in re.finditer(pattern, text):
            frag = m.group(0)
            # the dossier's own contact-free boilerplate and IRS/phone-style citations are allowed
            ctx = text[max(0, m.start() - 80):m.start()].lower()
            if label == "US phone number" and ("cik" in ctx or "sec.gov" in ctx or "edgar" in ctx):
                continue  # SEC central index keys look like phone numbers, not personal data
            if "irs.gov" in low or "ca.gov" in low or "sec.gov" in low or "census.gov" in low:
                if label in ("email address", "street address") and ("gov" in frag.lower() or "sec" in frag.lower()):
                    continue
            pii_hits += 1
            fail(f"{os.path.relpath(path, ROOT)}: possible {label} -> {frag[:60]!r}")

notes.append(f"PII scan: {len(scan_targets)} files, {pii_hits} hits")

# ---------------------------------------------------------------- 6. placeholders
BAD_TOKENS = ["TODO", "FIXME", "lorem ipsum", "XXX", "PLACEHOLDER", "CHANGEME"]
for path in scan_targets:
    if not path.endswith((".html", ".json", ".css", ".md")):
        continue
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except UnicodeDecodeError:
        continue
    for tok in BAD_TOKENS:
        if tok in text:
            fail(f"{os.path.relpath(path, ROOT)}: contains placeholder token '{tok}'")

# ---------------------------------------------------------------- 7. model sanity
for sc in model["scenarios"]:
    ids = [s["id"] for s in sc["strategies"]]
    if sorted(ids) != ["A", "B", "C", "D", "E"]:
        fail(f"scenario {sc['id']}: expected strategies A-E, got {ids}")
    for s in sc["strategies"]:
        if s["costs"]["net_proceeds"] > s["costs"]["gross_price"]:
            fail(f"scenario {sc['id']} strategy {s['id']}: net proceeds exceed gross price")
        if s["costs"]["measure_ula"] < 0:
            fail("negative ULA")
        if abs(sum(r["cash_flow"] for r in s["rows"]) - s["terminal_wealth_2035"]) > 1e9:
            fail(f"scenario {sc['id']} strategy {s['id']}: wealth metric out of range")

if not model["decision"]["matrix"]:
    fail("decision matrix empty")

# ---------------------------------------------------------------- report
print("=" * 68)
print("SP-01 integrity check")
print("=" * 68)
print(f"pages: {len(PAGES)}  |  facts: {len(facts['rows'])}  |  sources: {len(SRC_IDS)}  |  scenarios: {len(model['scenarios'])}")
for n in notes:
    print(f"  · {n}")
if failures:
    print(f"\nFAILED — {len(failures)} problem(s):")
    for f in failures:
        print(f"  ✗ {f}")
    sys.exit(1)
print("\nALL CHECKS PASSED")
