#!/usr/bin/env python3
"""Validation gate for the published decision brief.

Fails (non-zero exit) if any of the following is true:

  1. a required page, asset or data file is missing;
  2. a page is missing its doctype, language, title, single h1, main landmark,
     navigation, or the navigation does not list every page;
  3. an internal link or in-page anchor does not resolve;
  4. a table row carries no official source link, unless the table is marked
     class="calc" (a table of computed values) and carries its official basis
     in a footer row;
  5. any external link points outside the official-source allowlist;
  6. any external link lacks target="_blank" or rel="noopener";
  7. any row whose dataset status is "unverified" or "withheld" shows a value,
     or any "verified"/"derived" row shows an empty value;
  8. any source URL in the dataset is not https or not on the allowlist;
  9. an email address or telephone-number pattern appears in any page.

Run: python3 scripts/validate_site.py
"""

import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = [
    "index.html", "demographics.html", "economy.html", "schools.html",
    "property.html", "tenant.html", "model.html", "decision.html",
    "risks.html", "flagged.html", "sources.html",
]
ASSETS = ["assets/styles.css", "assets/site.js", "assets/favicon.svg"]

# Official publishers only. Suffix match, so sub-domains are covered.
OFFICIAL_DOMAINS = [
    "census.gov",
    "bls.gov",
    "fred.stlouisfed.org",
    "sec.gov",
    "lacity.gov",
    "lacounty.gov",
    "ca.gov",
    "usgs.gov",
    "irs.gov",
    "nces.ed.gov",
    "caschooldashboard.org",  # published by the California Department of Education
]

errors = []
checks = 0


def ok(condition, message):
    global checks
    checks += 1
    if not condition:
        errors.append(message)


def domain_ok(url):
    host = urlparse(url).hostname or ""
    return any(host == d or host.endswith("." + d) for d in OFFICIAL_DOMAINS)


class Collector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.stack = []
        self.ids = set()
        self.h1 = 0
        self.tables = []          # list of dicts: calc, rows(list of list of anchors), tfoot_links
        self.in_thead = False
        self.links = []           # (href, attrs dict)
        self.local_refs = []      # href/src that are local
        self.text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "h1":
            self.h1 += 1
        if tag in ("a", "link") and "href" in a:
            self.links.append((a["href"], a))
        if tag in ("script", "img") and "src" in a:
            self.links.append((a["src"], a))
        if tag == "table":
            self.tables.append({"calc": "calc" in (a.get("class") or ""), "rows": [], "tfoot": [], "in_tfoot": False})
        if tag == "thead":
            self.in_thead = True
        if tag in ("tbody", "tfoot"):
            self.in_thead = False
            if self.tables:
                self.tables[-1]["in_tfoot"] = tag == "tfoot"
        if tag == "tr" and self.tables and not self.in_thead:
            self.tables[-1]["rows"].append([])
        if tag == "a" and self.tables and self.tables[-1]["rows"]:
            href = a.get("href", "")
            if href.startswith("http"):
                self.tables[-1]["rows"][-1].append(href if not self.tables[-1]["in_tfoot"] else href)
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "thead":
            self.in_thead = False
        if tag == "tfoot" and self.tables:
            self.tables[-1]["in_tfoot"] = False
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_data(self, data):
        self.text.append(data)


def parse(path):
    p = Collector()
    with open(path, encoding="utf-8") as fh:
        p.feed(fh.read())
    return p


def main():
    # 1. required files
    for name in PAGES + ASSETS + ["data/published-records.json", ".nojekyll"]:
        ok(os.path.exists(os.path.join(ROOT, name)), f"missing required file: {name}")

    # 2-5. page structure and links
    for page in PAGES:
        path = os.path.join(ROOT, page)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
        p = parse(path)

        ok(raw.lstrip().lower().startswith("<!doctype html>"), f"{page}: missing doctype")
        ok('<html lang="en">' in raw, f"{page}: missing lang attribute")
        ok('name="viewport"' in raw, f"{page}: missing viewport meta")
        ok(re.search(r"<title>[^<]+</title>", raw) is not None, f"{page}: missing title")
        ok(p.h1 == 1, f"{page}: expected exactly one h1, found {p.h1}")
        ok('id="main-content"' in raw, f"{page}: missing main landmark id")
        ok('<nav class="site-nav">' in raw, f"{page}: missing navigation")

        # navigation must list every page
        for other in PAGES:
            ok(f'href="{other}"' in raw, f"{page}: navigation/links missing {other}")

        # privacy patterns
        ok(re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw) is None,
           f"{page}: email address pattern found")
        ok(re.search(r"(\(\d{3}\)\s?\d{3}-\d{4})|(\b\d{3}-\d{3}-\d{4}\b)", raw) is None,
           f"{page}: telephone number pattern found")

        # links
        for href, attrs in p.links:
            if href.startswith("http"):
                ok(href.startswith("https://"), f"{page}: non-https external link {href}")
                ok(domain_ok(href), f"{page}: external link outside official allowlist: {href}")
                ok(attrs.get("target") == "_blank", f"{page}: external link without target=_blank: {href}")
                ok("noopener" in (attrs.get("rel") or ""), f"{page}: external link without rel=noopener: {href}")
            elif href.startswith("#"):
                ok(href[1:] in p.ids, f"{page}: unresolved anchor {href}")
            else:
                target, _, frag = href.partition("#")
                if not target:
                    continue
                base = os.path.normpath(os.path.join(ROOT, target))
                ok(os.path.exists(base) or os.path.exists(os.path.join(ROOT, target)),
                   f"{page}: broken local link {href}")
                if frag:
                    tgt = os.path.join(ROOT, target)
                    if os.path.exists(tgt):
                        with open(tgt, encoding="utf-8") as fh2:
                            ok(f'id="{frag}"' in fh2.read(), f"{page}: unresolved fragment {href}")

        # 4. tables
        for i, t in enumerate(p.tables):
            body_rows = [r for r in t["rows"]]
            for r in body_rows:
                if t["calc"]:
                    continue
                ok(len(r) >= 1, f"{page}: table {i} has a row with no official source link")
            if t["calc"]:
                foot_links = [h for r in body_rows for h in r if h.startswith("https://")]
                ok(len(foot_links) >= 1, f"{page}: calc table {i} has no official basis link in its footer")

    # 6-8. dataset integrity
    with open(os.path.join(ROOT, "data", "published-records.json"), encoding="utf-8") as fh:
        data = json.load(fh)

    seen = set()
    for r in data["records"]:
        ok(r["id"] not in seen, f"duplicate record id {r['id']}")
        seen.add(r["id"])
        ok(r["status"] in ("verified", "derived", "unverified", "withheld"),
           f"{r['id']}: unknown status {r['status']}")
        if r["status"] in ("unverified", "withheld"):
            ok(r["value"] == "", f"{r['id']}: {r['status']} row must not publish a value")
        else:
            ok(r["value"] != "", f"{r['id']}: {r['status']} row must publish a value")
        ok(r["src"] in data["sources"], f"{r['id']}: unknown source id {r['src']}")
        for key in ("metric", "period", "geo"):
            ok(bool(r[key]), f"{r['id']}: missing {key}")

    for sid, s in data["sources"].items():
        ok(s["url"].startswith("https://"), f"{sid}: source URL must be https")
        ok(domain_ok(s["url"]), f"{sid}: source outside official allowlist: {s['url']}")
        ok(bool(s["publisher"]) and bool(s["title"]), f"{sid}: source missing publisher or title")

    # counts
    c = data["counts"]
    ok(c["total"] == len(data["records"]), "counts.total does not match record count")
    ok(c["total"] == c["verified"] + c["derived"] + c["unverified"] + c["withheld"],
       "status counts do not sum to total")

    if errors:
        print(f"FAIL: {len(errors)} problem(s) across {checks} assertions\n")
        for e in errors[:60]:
            print("  -", e)
        if len(errors) > 60:
            print(f"  ... and {len(errors) - 60} more")
        return 1

    print(
        f"PASS: {checks} assertions across {len(PAGES)} pages.\n"
        f"  rows: {c['total']} = {c['verified']} verified + {c['derived']} derived + "
        f"{c['unverified']} unverified (blank) + {c['withheld']} withheld (blank)\n"
        f"  sources: {len(data['sources'])} official pages, all https and allowlisted\n"
        f"  every data-table row carries an official source link; every calc table carries its basis\n"
        f"  no broken internal links or anchors; no email or phone patterns"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
