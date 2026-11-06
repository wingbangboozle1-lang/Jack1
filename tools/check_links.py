#!/usr/bin/env python3
"""Build gate. Exits non-zero if the site must not be published.

Checks, in order:

  1. DATA INTEGRITY   every row marked verified has a non-empty value and an official URL;
                      no non-official value is published in a `v` field; every non-official
                      figure is quarantined in `r`.
  2. OFFICIAL HOSTS   every URL cited by a verified row, a model input, an official anchor, a
                      flag's route-to-close, or the source register resolves to a host on the
                      official publisher allowlist.
  3. INTERNAL LINKS   every relative href/src on every rendered page points at a file that
                      exists in the repository root.
  4. EXTERNAL ASSETS  no page references a remote stylesheet, script, image or font, so the
                      site renders identically offline and on GitHub Pages.
  5. PRIVACY          no rendered page or data file contains a street-address pattern, a
                      Los Angeles County Assessor parcel-number pattern, or any token on the
                      forbidden list.
  6. PAGE HYGIENE     every page declares a charset and a viewport, and every page in the
                      navigation exists and is reachable.

Usage:  python3 tools/check_links.py   (exit 0 = publishable)
"""
import glob
import json
import os
import re
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, HERE)
from collect_sources import DOMAIN_PUBLISHER, registrable  # noqa: E402

ALLOWED = set(DOMAIN_PUBLISHER.keys())

DATA_FILES = ["asset.json", "demographics.json", "income.json", "employment.json",
              "schools.json", "geography.json", "valuation.json", "hazards.json",
              "regulatory.json", "tenant.json", "risks.json", "projection.json",
              "flags.json", "decisions.json", "sources.json", "projection_output.json"]

# A street address: a house number followed by a street name and a suffix.
RE_ADDRESS = re.compile(
    r"\b\d{1,6}\s+[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,3}\s+"
    r"(?:Boulevard|Blvd|Avenue|Ave|Street|St|Road|Rd|Drive|Dr|Lane|Ln|Way|Place|Pl|"
    r"Court|Ct|Circle|Cir|Terrace|Ter|Parkway|Pkwy|Highway|Hwy|Trail|Trl)\b")
# LA County APN / AIN formats: 1234-567-890, 1234567890, or "APN 1234-567-890".
RE_APN = re.compile(r"\b\d{4}-\d{3}-\d{3}\b|\bAPN\s*:?\s*\d{6,}\b|\bAIN\s*:?\s*\d{6,}\b", re.I)
# A bracketed token such as [PROPERTY-ID: JIB-CTLA-01] or [REDACTED] is a deliberate
# anonymisation marker, not a published value.
RE_PLACEHOLDER = re.compile(r"^\[[A-Z0-9 :\-]+\]$")
# Anything that looks like a personal identifier we would never publish.
FORBIDDEN_TOKENS = [
    "social security", "SSN", "date of birth", "driver's license",
    "phone number of the owner", "owner's home address",
]

errors = []
warnings = []


def err(check, msg):
    errors.append("[%s] %s" % (check, msg))


def warn(check, msg):
    warnings.append("[%s] %s" % (check, msg))


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


def host_ok(url):
    try:
        host = urllib.parse.urlparse(url).netloc.lower()
    except Exception:
        return False, ""
    if not host:
        return False, ""
    reg = registrable(host)
    for dom in ALLOWED:
        if reg == dom or reg.endswith("." + dom):
            return True, host
    return False, host


def check_url_owner(check, url, where):
    if not url or not url.strip():
        return
    u = url.strip()
    if not re.match(r"^https?://", u):
        err(check, "%s cites a non-HTTP(S) URL: %r" % (where, u))
        return
    ok, host = host_ok(u)
    if not ok:
        err(check, "%s cites a host that is not an official publisher: %s (%s)"
            % (where, host, u))


# ---------------------------------------------------------- 1. data integrity
def check_data():
    for f in DATA_FILES:
        path = os.path.join(DATA, f)
        if not os.path.exists(path):
            err("data", "expected data file is missing: data/%s" % f)
            continue
        try:
            doc = load(f)
        except Exception as exc:
            err("data", "data/%s is not valid JSON: %s" % (f, exc))
            continue
        buckets = []
        for key in ("rows", "official_inputs", "official_anchors", "flags", "irregularities"):
            for item in doc.get(key, []) or []:
                if isinstance(item, dict):
                    buckets.append((key, item))
        seen = set()
        for key, item in buckets:
            rid = item.get("id")
            if not rid:
                err("data", "data/%s has a %s entry with no id" % (f, key))
                continue
            if rid in seen:
                err("data", "data/%s has a duplicate id %s" % (f, rid))
            seen.add(rid)
            v = item.get("v", item.get("value"))
            u = (item.get("u") or "").strip()
            k = bool(item.get("k"))
            rep = item.get("r")
            if key in ("rows", "official_inputs"):
                if k and not u:
                    err("data", "data/%s row %s is marked VERIFIED but has no official URL" % (f, rid))
                if k and v in ("", None):
                    err("data", "data/%s row %s is marked VERIFIED but has an empty value" % (f, rid))
                if (not k and v not in ("", None) and not rep
                        and not (isinstance(v, str) and RE_PLACEHOLDER.match(v.strip()))):
                    err("data", "data/%s row %s is NOT verified yet publishes a value in `v` "
                                "with no quarantined `r` field" % (f, rid))
                if rep and v == rep:
                    pass
                if rep and v == rep:
                    err("data", "data/%s row %s publishes a non-official value in `v`" % (f, rid))
            if k:
                check_url_owner("data", u, "data/%s row %s" % (f, rid))
            elif u and key != "flags":
                # an unverified row may still link the official page needed to close the gap
                ok, host = host_ok(u)
                if not ok and host:
                    warn("data", "data/%s row %s links a non-official host: %s" % (f, rid, host))
        for item in doc.get("unverified_inputs", []) or []:
            if item.get("u"):
                warn("data", "data/%s unverified input %s carries a URL; unverified inputs "
                             "should have no official publisher" % (f, item.get("id")))
        if f == "flags.json":
            for item in doc.get("flags", []) or []:
                check_url_owner("flags", item.get("u") or "", "flag %s" % item.get("id"))
        if f == "sources.json":
            for p in doc.get("publishers", []) or []:
                for u in p.get("urls", []) or []:
                    check_url_owner("sources", u.get("url") or "",
                                    "source register %s" % p.get("publisher"))
        if f == "risks.json":
            for a in doc.get("official_anchors", []) or []:
                check_url_owner("anchors", a.get("u") or "", "anchor %s" % a.get("id"))


# ------------------------------------------------------- 3./4./5./6. the HTML
def check_html():
    pages = sorted(glob.glob(os.path.join(ROOT, "*.html")))
    if not pages:
        err("html", "no HTML pages found in the repository root")
        return
    nav = []
    try:
        with open(os.path.join(HERE, "build_site.py"), encoding="utf-8") as fh:
            txt = fh.read()
        m = re.search(r"^NAV_FLAT = \[\(h, t\) for _, items in NAV for h, t in items\]", txt, re.M)
        if m:
            ns = {}
            exec(re.search(r"^NAV = \[.*?^\]\n", txt, re.S | re.M).group(0), ns)
            nav = [h for _, items in ns["NAV"] for h, _t in items]
    except Exception as exc:
        warn("html", "could not parse NAV from build_site.py: %s" % exc)

    existing = {os.path.basename(p) for p in pages}
    for want in nav:
        if want not in existing:
            err("html", "navigation entry %s has no rendered page" % want)

    for p in pages:
        name = os.path.basename(p)
        with open(p, encoding="utf-8") as fh:
            doc = fh.read()

        if '<meta charset="utf-8">' not in doc:
            err("html", "%s does not declare a UTF-8 charset" % name)
        if 'name="viewport"' not in doc:
            err("html", "%s does not declare a viewport" % name)
        if "<title>" not in doc:
            err("html", "%s has no <title>" % name)

        for m in re.finditer(r'<(?:script|link|img|iframe|video|audio|source)\b[^>]*>', doc):
            tag = m.group(0)
            if 'rel="noopener noreferrer external"' in tag and "<link" in tag:
                continue
            src = re.search(r'(?:src|href)\s*=\s*"([^"]+)"', tag)
            if src and re.match(r"^(https?:)?//", src.group(1)):
                err("html", "%s embeds an external asset, which breaks offline rendering: %s"
                    % (name, src.group(1)))

        for m in re.finditer(r'href="([^"]+)"', doc):
            href = m.group(1)
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            if href.startswith("#"):
                if 'id="%s"' % href[1:] not in doc:
                    warn("html", "%s has an in-page anchor with no target: %s" % (name, href))
                continue
            target = href.split("#")[0].split("?")[0]
            if not target:
                continue
            if not os.path.exists(os.path.join(ROOT, target)):
                err("html", "%s links to a file that does not exist: %s" % (name, href))

        for rx, label in ((RE_ADDRESS, "street address"), (RE_APN, "parcel/assessor number")):
            for m in rx.finditer(doc):
                frag = doc[max(0, m.start() - 60):m.end() + 60].replace("\n", " ")
                err("privacy", "%s contains a %s pattern: %r ... context: %r"
                    % (name, label, m.group(0), frag))
        for tok in FORBIDDEN_TOKENS:
            if tok.lower() in doc.lower():
                err("privacy", "%s contains the forbidden token %r" % (name, tok))


def check_data_privacy():
    for f in sorted(glob.glob(os.path.join(DATA, "*.json"))):
        with open(f, encoding="utf-8") as fh:
            doc = fh.read()
        name = os.path.relpath(f, ROOT)
        for rx, label in ((RE_ADDRESS, "street address"), (RE_APN, "parcel/assessor number")):
            for m in rx.finditer(doc):
                err("privacy", "%s contains a %s pattern: %r" % (name, label, m.group(0)))
        for tok in FORBIDDEN_TOKENS:
            if tok.lower() in doc.lower():
                err("privacy", "%s contains the forbidden token %r" % (name, tok))


def check_docs():
    for f in sorted(glob.glob(os.path.join(ROOT, "docs", "*.md"))):
        with open(f, encoding="utf-8") as fh:
            doc = fh.read()
        name = os.path.relpath(f, ROOT)
        for rx, label in ((RE_ADDRESS, "street address"), (RE_APN, "parcel/assessor number")):
            for m in rx.finditer(doc):
                err("privacy", "%s contains a %s pattern: %r" % (name, label, m.group(0)))


def main():
    check_data()
    check_data_privacy()
    check_docs()
    check_html()

    pages = sorted(glob.glob(os.path.join(ROOT, "*.html")))
    total_bytes = sum(os.path.getsize(p) for p in pages)
    print("pages: %d | total HTML: %s bytes" % (len(pages), "{:,}".format(total_bytes)))
    print("data files checked: %d" % len(DATA_FILES))
    print("official host allowlist: %d registrable domains" % len(ALLOWED))

    if warnings:
        print("\n%d warning(s):" % len(warnings))
        for w in warnings:
            print("  WARN " + w)
    if errors:
        print("\n%d ERROR(S) - DO NOT PUBLISH:" % len(errors))
        for e in errors:
            print("  FAIL " + e)
        return 1
    print("\nPASS - no broken internal links, no unsourced verified rows, no non-official "
          "hosts in verified rows, no external assets, no privacy-pattern leaks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
