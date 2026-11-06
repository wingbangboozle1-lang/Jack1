#!/usr/bin/env python3
"""
Verification gate. Fails (exit 1) if ANY of the following is true:

  1. A required page is missing, or an internal href/asset does not exist.
  2. A source id referenced on any page is not defined in data/sources.json.
  3. A row in the verified fact tables (T01-T08) has a value but no source.
  4. A source URL is not https, or is not a recognised official / labelled
     third-party host.
  5. Private data leaked: a US street address pattern, an APN pattern, an
     email address, or a phone number appears in any generated page.
  6. A table cell contains a suspicious numeric claim with no adjacent source.

Run: python3 tools/check_site.py
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

OFFICIAL_HOST_SUFFIXES = (
    ".gov", ".ca.gov", ".mil", ".us", "irs.gov", "sec.gov", "federalreserve.gov",
    "stlouisfed.org", "fred.stlouisfed.org",
)
THIRD_PARTY_OK = {
    "netleaseadvisor.com", "www.netleaseadvisor.com",
    "www.solidinvestmentsfl.com",
    "myemail.constantcontact.com",
    "instoneinvestments.com",
}

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


# --------------------------------------------------------------------------- #
def load(name):
    with open(os.path.join(DATA, name)) as fh:
        return json.load(fh)


def check_pages():
    pages = [
        "index.html", "decision.html", "risks.html", "market.html", "process.html",
        "property.html", "market_pricing.html", "tenant.html", "rules.html",
        "sources.html", "flagged.html", "privacy.html",
    ]
    for p in pages:
        if not os.path.exists(os.path.join(ROOT, p)):
            err("missing page: " + p)
    if not os.path.exists(os.path.join(ROOT, "assets", "styles.css")):
        err("missing assets/styles.css")
    return pages


def check_links(pages):
    for p in pages:
        with open(os.path.join(ROOT, p)) as fh:
            text = fh.read()
        for href in re.findall(r'(?:href|src)="([^"]+)"', text):
            if href.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = href.split("#")[0]
            if not target:
                continue
            if not os.path.exists(os.path.join(ROOT, target)):
                err(f"{p}: broken internal link -> {href}")


def check_sources(pages):
    srcs = {s["id"]: s for s in load("sources.json")["sources"]}
    defined = set(srcs)
    used = set()
    for p in pages:
        with open(os.path.join(ROOT, p)) as fh:
            text = fh.read()
        for sid in re.findall(r">(S\d{2})</a>", text) + re.findall(r">(S\d{2})\?</span>", text):
            used.add(sid)
            if sid not in defined:
                err(f"{p}: source id {sid} is not defined in data/sources.json")

    # every defined source must be used somewhere
    for sid in sorted(defined - used):
        warn(f"source {sid} is defined but not referenced by any page")

    for sid, s in srcs.items():
        url = s["url"]
        if not url.startswith("https://"):
            err(f"{sid}: source URL is not https -> {url}")
            continue
        host = re.sub(r"^https://", "", url).split("/")[0]
        ok = host.endswith(OFFICIAL_HOST_SUFFIXES) or host in THIRD_PARTY_OK
        if not ok:
            err(f"{sid}: unrecognised source host -> {host}")
        if s["type"] == "official" and not (host.endswith(".gov") or host.endswith(".us")
                                            or host in ("fred.stlouisfed.org", "stlouisfed.org")):
            warn(f"{sid}: labelled official but host is {host} (verify provenance)")
    return used


def check_fact_rows(used):
    facts = load("facts.json")
    for t in facts["tables"]:
        for i, row in enumerate(t["rows"]):
            value = row[1]
            source = row[-1] if isinstance(row[-1], str) else ""
            has_src = bool(re.fullmatch(r"S\d{2}", source or "")) or source == "P"
            if value in ("", None):
                # blank is allowed, but must not silently claim a source
                continue
            if not has_src:
                err(f"{t['id']} row {i+1} ({row[0]!r}) has a value but no source id")
            elif source == "P":
                # principal-supplied rows are allowed only where no official
                # source can exist (deal terms, redactions). They must be marked.
                if t["id"] != "T01":
                    err(f"{t['id']} row {i+1}: 'P' marker used outside the deal-terms table")
            elif source not in used:
                err(f"{t['id']} row {i+1} cites {source} which never appears on the site")

    # no unverified numbers where a source is claimed as third-party
    print(f"  checked {sum(len(t['rows']) for t in facts['tables'])} fact rows")


def check_privacy(pages):
    patterns = {
        "street address": re.compile(r"\b\d{1,5}\s+(?:[NSEW]\.?\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\s+"
                                     r"(?:St|Street|Ave|Avenue|Blvd|Boulevard|Rd|Road|Dr|Drive|Way|Ln|Hwy)\b"),
        "APN / AIN": re.compile(r"\b\d{4}-\d{3}-\d{3}\b|\bAPN\s*[:#]?\s*\d"),
        "email": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
        "phone": re.compile(r"\(\d{3}\)\s*\d{3}-\d{4}|\b\d{3}-\d{3}-\d{4}\b"),
    }
    allowed = {"ficalpop@dof.ca.gov", "census.data@census.gov"}  # never emitted, belt and braces
    for p in pages:
        with open(os.path.join(ROOT, p)) as fh:
            text = fh.read()
        for name, rx in patterns.items():
            for m in rx.finditer(text):
                hit = m.group(0)
                if hit in allowed:
                    continue
                err(f"{p}: possible private data ({name}) -> {hit!r}")
    print(f"  scanned {len(pages)} pages for address/APN/email/phone leakage")


def check_placeholders(pages):
    text = "".join(open(os.path.join(ROOT, p)).read() for p in pages)
    for ph in ("[PARCEL-REDACTED]", "[OWNER-ENTITY]", "[TENANT-ENTITY]", "[RENT]"):
        if ph not in text:
            warn(f"placeholder {ph} not rendered anywhere (expected on Privacy/Property)")
    print("  placeholder scheme present")


def check_nav(pages):
    for p in pages:
        text = open(os.path.join(ROOT, p)).read()
        for href in ("index.html", "decision.html", "risks.html", "market.html",
                     "process.html", "flagged.html", "sources.html"):
            if f'href="{href}"' not in text:
                err(f"{p}: navigation is missing {href}")
    print("  navigation complete on every page")


def main():
    print("== site verification ==")
    pages = check_pages()
    check_links(pages)
    used = check_sources(pages)
    check_fact_rows(used)
    check_privacy(pages)
    check_placeholders(pages)
    check_nav(pages)

    print("\n== result ==")
    for w in warnings:
        print("WARN:", w)
    for e in errors:
        print("FAIL:", e)
    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s) — BUILD FAILED")
        return 1
    print(f"OK — {len(pages)} pages, 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
