#!/usr/bin/env python3
"""Scan every data/*.json row and build the canonical source register.

A row counts as a SOURCE only if it has a non-empty official URL. Rows with no
URL are structural gaps (no official publisher exists) and are handled by the
flag register instead. Nothing here is hand-maintained: the Sources page and
docs/SOURCES.md are both generated from this file, so they cannot drift.
"""
import json, os, sys, urllib.parse
from collections import OrderedDict

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

FILES = ["asset.json", "demographics.json", "income.json", "employment.json",
         "schools.json", "geography.json", "valuation.json", "hazards.json",
         "regulatory.json", "tenant.json", "risks.json", "projection.json",
         "flags.json", "decisions.json"]

DOMAIN_PUBLISHER = OrderedDict([
    ("sec.gov", "U.S. Securities and Exchange Commission (EDGAR)"),
    ("census.gov", "U.S. Census Bureau"),
    ("bls.gov", "U.S. Bureau of Labor Statistics"),
    ("bea.gov", "U.S. Bureau of Economic Analysis"),
    ("treasury.gov", "U.S. Department of the Treasury"),
    ("fhfa.gov", "U.S. Federal Housing Finance Agency"),
    ("fema.gov", "U.S. Federal Emergency Management Agency"),
    ("usgs.gov", "U.S. Geological Survey"),
    ("nces.ed.gov", "U.S. National Center for Education Statistics"),
    ("noaa.gov", "U.S. National Oceanic and Atmospheric Administration"),
    ("irs.gov", "U.S. Internal Revenue Service"),
    ("stlouisfed.org", "Federal Reserve Bank of St. Louis (FRED) - republishing official federal series"),
    ("ca.gov", "State of California"),
    ("lacounty.gov", "County of Los Angeles"),
    ("lacity.gov", "City of Los Angeles"),
    ("lacity.org", "City of Los Angeles"),
    ("ladbs.org", "City of Los Angeles Department of Building and Safety"),
    ("lafd.org", "Los Angeles Fire Department"),
    ("caschooldashboard.org", "California School Dashboard (California Department of Education)"),
    ("nces.ed.gov", "U.S. National Center for Education Statistics"),
    ("lausd.org", "Los Angeles Unified School District"),
    ("metro.net", "Los Angeles County Metropolitan Transportation Authority (Metro)"),
])


def registrable(host):
    host = host.lower().lstrip(".")
    parts = host.split(".")
    if len(parts) >= 3 and parts[-2] in ("co", "com", "org", "net", "ac", "gov", "edu", "ed", "k12"):
        return ".".join(parts[-3:])
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


def publisher_for(url):
    try:
        host = urllib.parse.urlparse(url).netloc
    except Exception:
        return "Unidentified publisher"
    reg = registrable(host)
    for dom, label in DOMAIN_PUBLISHER.items():
        if reg == dom or reg.endswith("." + dom):
            return label
    return host


def iter_rows(doc):
    for key in ("rows", "official_inputs", "unverified_inputs", "official_anchors",
                "flags", "irregularities"):
        for item in doc.get(key, []) or []:
            if isinstance(item, dict):
                yield key, item


def main():
    register = OrderedDict()
    per_file = OrderedDict()
    stats = {"rows_total": 0, "rows_verified": 0, "rows_unverified": 0,
             "rows_blank": 0, "rows_no_url": 0}

    for fname in FILES:
        path = os.path.join(DATA, fname)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
        counts = {"rows": 0, "verified": 0, "unverified": 0, "blank": 0, "no_url": 0}
        for bucket, item in iter_rows(doc):
            url = (item.get("u") or "").strip()
            verified = bool(item.get("k"))
            blank = item.get("v") in ("", None) and bucket in ("rows", "official_inputs")
            if bucket == "rows":
                counts["rows"] += 1
                stats["rows_total"] += 1
                if verified:
                    counts["verified"] += 1
                    stats["rows_verified"] += 1
                else:
                    counts["unverified"] += 1
                    stats["rows_unverified"] += 1
                if blank:
                    counts["blank"] += 1
                    stats["rows_blank"] += 1
                if not url:
                    counts["no_url"] += 1
                    stats["rows_no_url"] += 1
            if not url:
                continue
            pub = publisher_for(url)
            entry = register.setdefault(pub, {"publisher": pub, "urls": OrderedDict()})
            rec = entry["urls"].setdefault(url, {"url": url, "cited_by": [], "row_names": set()})
            rid = item.get("id")
            if rid:
                rec["cited_by"].append(rid)
                rec["row_names"].add(
                    (item.get("m") or item.get("name") or item.get("title") or "")[:90])
        per_file[fname] = counts

    out = {
        "meta": {
            "task": "T16",
            "title": "Sources & Verification Register",
            "generated_by": "tools/collect_sources.py",
            "retrieved": "2026-11-06",
            "policy": "Generated automatically from every row in data/*.json so the register cannot drift from the tables it documents. A URL appears here only if at least one row cites it. Every entry is an official government, regulator, central-bank, regional-agency or SEC-filing publisher.",
            "stats": stats,
            "per_file": per_file,
        },
        "publishers": [
            {"publisher": v["publisher"],
             "url_count": len(v["urls"]),
             "row_citations": sum(len(u["cited_by"]) for u in v["urls"].values()),
             "urls": [{"url": u["url"],
                       "cited_by": sorted(set(u["cited_by"]), key=lambda x: (x.split("-")[0], x)),
                       "topics": sorted(n for n in u["row_names"] if n)[:6]}
                      for u in v["urls"].values()]}
            for v in register.values()
        ],
    }
    # ---------------------------------------------------- docs/SOURCES.md
    md = ["# Sources & Verification Register", "",
          "Generated by `tools/collect_sources.py` from every row in `data/*.json`. It cannot "
          "drift from the tables it documents: a URL appears here only if at least one row "
          "cites it.", "",
          "Retrieved %s. Every publisher below is a government agency, a regulator, a central "
          "bank, a Federal Reserve Bank republishing a federal series, a federally designated "
          "regional planning agency, or the U.S. Securities and Exchange Commission."
          % "2026-11-06", "",
          "## Coverage", "",
          "| Measure | Count |", "| --- | --- |",
          "| Table rows published | %d |" % stats["rows_total"],
          "| Rows verified from an official source | %d (%.1f%%) |"
          % (stats["rows_verified"], stats["rows_verified"] * 100.0 / stats["rows_total"]),
          "| Rows unverified (value withheld) | %d |" % stats["rows_unverified"],
          "| Rows with a blank value cell | %d |" % stats["rows_blank"],
          "| Rows with no official publisher at all | %d |" % stats["rows_no_url"],
          "| Distinct official URLs | %d |" % sum(len(v["urls"]) for v in register.values()),
          "| Official publishers | %d |" % len(register), "",
          "## Per-file coverage", "",
          "| Data file | Rows | Verified | Unverified | Blank | No URL | Verified share |",
          "| --- | --- | --- | --- | --- | --- | --- |"]
    for f, c in per_file.items():
        if not c["rows"]:
            continue
        md.append("| `%s` | %d | %d | %d | %d | %d | %.0f%% |"
                  % (f, c["rows"], c["verified"], c["unverified"], c["blank"], c["no_url"],
                     c["verified"] * 100.0 / c["rows"]))
    md += ["", "## Every official publisher, URL and the rows that cite it", ""]
    for v in register.values():
        md.append("### %s" % v["publisher"])
        md.append("")
        for u in v["urls"].values():
            cited = sorted(set(u["cited_by"]))
            md.append("- <%s>" % u["url"])
            md.append("  - Cited by: %s" % ", ".join("`%s`" % c for c in cited))
            topics = sorted(n for n in u["row_names"] if n)[:4]
            if topics:
                md.append("  - Topics: %s" % "; ".join(topics))
        md.append("")
    md += ["## Source classes deliberately excluded", "",
           "Where a value from one of these appeared during research it is confined to the "
           "`reported` field of a row marked unverified, and is never used as a model input or "
           "as a basis for the recommendation.", ""]
    for c in ["Commercial hazard and risk aggregators that republish FEMA National Risk Index data",
              "Real-estate brokerages, investment platforms and capitalisation-rate research providers",
              "Credit-rating agencies",
              "Local and national news outlets, including television stations and newspapers",
              "Encyclopedias and wikis",
              "Earnings calendars, stock-screeners and financial data aggregators",
              "Legal-information and tax-calculator websites",
              "Insurance comparison and lead-generation websites",
              "Real-estate listing portals and neighbourhood-score providers"]:
        md.append("- %s" % c)
    md.append("")
    docs_dir = os.path.join(os.path.dirname(DATA), "docs")
    os.makedirs(docs_dir, exist_ok=True)
    with open(os.path.join(docs_dir, "SOURCES.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")

    dest = os.path.join(DATA, "sources.json")
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print("wrote", dest)
    print("publishers:", len(out["publishers"]),
          "| distinct URLs:", sum(p["url_count"] for p in out["publishers"]))
    print("stats:", json.dumps(stats))
    for f, c in per_file.items():
        print("  ", f, c)


if __name__ == "__main__":
    sys.exit(main())
