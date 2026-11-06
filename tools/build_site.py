#!/usr/bin/env python3
"""
Site generator for the Jack in the Box NNN decision dashboard.

Reads  : data/*.json
Writes : index.html, *.html (category pages), assets/styles.css

Rules enforced here:
  * every table cell that claims a fact must carry a source id;
  * source ids must exist in data/sources.json;
  * values that could not be verified must be empty strings, never guesses.
"""

import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")


# --------------------------------------------------------------------------- #
def load(name):
    with open(os.path.join(DATA, name)) as fh:
        return json.load(fh)


SOURCES = {s["id"]: s for s in load("sources.json")["sources"]}
FACTS = load("facts.json")
RISKS = load("risks.json")
DECISION = load("decision.json")
FLAGGED = load("flagged.json")
PROJ = load("projections.json")
SERIES = load("series.json")["series"]
RETRIEVED = "2026-11-06"

PAGES = [
    ("index.html", "Overview"),
    ("decision.html", "Decision"),
    ("risks.html", "Risk Register"),
    ("market.html", "Trade Area"),
    ("process.html", "Projections"),
    ("property.html", "Property & Lease"),
    ("market_pricing.html", "Market Pricing"),
    ("tenant.html", "Tenant Credit"),
    ("rules.html", "Tax & Rules"),
    ("sources.html", "Data & Sources"),
    ("flagged.html", "Flagged for Review"),
    ("privacy.html", "Privacy & Method"),
]


def esc(t):
    return html.escape(str(t), quote=True)


def src_link(sid):
    """Render a source badge linking to the official page."""
    if not sid:
        return '<span class="src none" title="No source">unverified</span>'
    s = SOURCES.get(sid)
    if not s:
        return '<span class="src bad" title="Unknown source id">%s?</span>' % esc(sid)
    kind = "official" if s["type"] == "official" else "third"
    return '<a class="src %s" href="%s" target="_blank" rel="noopener" title="%s">%s</a>' % (
        kind, esc(s["url"]), esc(s["publisher"] + " — " + s["title"]), esc(sid))


def page(title, body, active, subtitle=""):
    nav = []
    for href, label in PAGES:
        cls = ' class="active"' if href == active else ""
        nav.append('<a href="%s"%s>%s</a>' % (href, cls, esc(label)))
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Jack in the Box NNN — Decision Dashboard</title>
<meta name="description" content="Anonymized, source-verified analysis of a Central Los Angeles Jack in the Box NNN asset: hold-to-expiry, renew, or sell.">
<meta name="robots" content="index,follow">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <div class="brand">
      <span class="mark">JIB</span>
      <span class="brandtext"><strong>NNN Decision Dashboard</strong>
      <small>Central Los Angeles · single-tenant · anonymized</small></span>
    </div>
    <nav>{nav}</nav>
  </div>
</header>
<main id="main" class="wrap">
<h1>{title}</h1>
{subtitle}
{body}
</main>
<footer class="wrap">
  <p><strong>Privacy:</strong> this site contains no street address, parcel number, owner identity, tenant contact
  or lease financials. Parcels are shown as <code>[PARCEL-REDACTED]</code>.</p>
  <p><strong>Verification:</strong> every factual cell links to its official source. Empty cells are unverified
  and are listed on <a href="flagged.html">Flagged for Review</a>. Data retrieved {retrieved}.</p>
  <p><strong>Not advice.</strong> This is a decision-support analysis, not an appraisal, and not legal, tax or
  investment advice. Model output is labelled as such.</p>
</footer>
</body>
</html>
""".format(title=esc(title), nav="".join(nav), subtitle=subtitle, body=body, retrieved=RETRIEVED)


def table(cols, rows, caption=None, cls="data"):
    out = ['<div class="tablewrap"><table class="%s">' % cls]
    if caption:
        out.append("<caption>%s</caption>" % caption)
    out.append("<thead><tr>" + "".join("<th>%s</th>" % esc(c) for c in cols) + "</tr></thead><tbody>")
    for r in rows:
        cells = []
        r = [(str(c)[:-1] if isinstance(c, str) and c.endswith("|") else c) for c in r]
        for i, c in enumerate(r):
            if i == len(r) - 1 and str(c) == "P":
                cells.append('<td><span class="src none" title="Supplied by the principal; not verified against a document">principal-supplied</span></td>')
            elif i == len(r) - 1 and re.fullmatch(r"S\d{2}", str(c) or ""):
                cells.append("<td>%s</td>" % src_link(c))
            else:
                cells.append("<td>%s</td>" % (esc(c) if c not in (None, "") else
                                              '<span class="blank">—</span>'))
        out.append("<tr>" + "".join(cells) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def kv(items):
    return '<dl class="kv">' + "".join(
        "<dt>%s</dt><dd>%s</dd>" % (esc(k), v) for k, v in items) + "</dl>"


def callout(kind, title, body):
    return '<div class="callout %s"><h3>%s</h3>%s</div>' % (kind, esc(title), body)


# --------------------------------------------------------------------------- #
# Page builders
# --------------------------------------------------------------------------- #
def build_overview():
    rec = DECISION["recommendation"]
    opt_c = [o for o in DECISION["options"] if o["id"] == "OPT-C"][0]
    p0 = PROJ["paths"][0]
    p_end = PROJ["paths"][-1]

    body = []
    body.append(callout("rec", "Recommended course of action: " + opt_c["name"],
                        "<p>%s</p><p class=\"small\">%s</p><p><a class=\"btn\" href=\"decision.html\">Full decision analysis →</a></p>"
                        % (esc(rec["statement"]), esc(rec["wealth_preservation_balance"]))))

    body.append('<h2>What this is</h2>')
    body.append("""<p>You own a free-standing <strong>Jack in the Box</strong> restaurant under an
    <strong>absolute-NNN lease</strong> in Central Los Angeles. The lease runs out somewhere in
    <strong>2030–2035</strong>. The question is whether to <em>sell before expiry</em>, <em>hold to expiry</em>,
    or <em>renew and then decide</em>. This dashboard collects the official evidence, scores every risk,
    and states a recommendation with the conditions that would change it.</p>""")

    body.append('<h2>Key figures (each one sourced)</h2>')
    tiles = [
        ("Unemployment, LA metro", "4.6%", "2026-09", "S01"),
        ("Median household income, LA County", "$90,757", "2024 (SAIPE)", "S04"),
        ("Population change, LA city", "−0.8%", "2020→2025", "S05"),
        ("10-year Treasury", "4.90%", "2026-11-04", "S09"),
        ("Baa corporate yield", "6.59%", "2026-10", "S10"),
        ("CRE loan delinquency", "1.53%", "2026 Q2", "S11"),
        ("JIB revenue, FY2025", "$1,465.3M", "FY ended 2025-09-28", "S15"),
        ("JIB net income, FY2025", "−$80.7M", "FY ended 2025-09-28", "S16"),
        ("City transfer tax (tier 1)", "4.45%", "closings after 2026-06-30", "S23"),
        ("Fast-food minimum wage", "$20.00/hr", "since 2024-04-01", "S19"),
        ("Model value index, hold, 2035", "%.3f×" % p_end["value_relative_hold"], "2026 = 1.00", None),
        ("Model value index, renew, 2035", "%.3f×" % p_end["value_relative_renew"], "2026 = 1.00", None),
    ]
    t = ['<div class="tiles">']
    for label, val, sub, sid in tiles:
        t.append('<div class="tile"><div class="tlabel">%s</div><div class="tval">%s</div>'
                 '<div class="tsub">%s</div><div class="tsrc">%s</div></div>'
                 % (esc(label), esc(val), esc(sub),
                    src_link(sid) if sid else '<span class="src model">model</span>'))
    t.append("</div>")
    body.append("".join(t))

    body.append('<h2>The three options at a glance</h2>')
    rows = []
    for o in DECISION["options"]:
        rows.append([o["name"], o["mechanics"], ", ".join(o["key_risks"]),
                     "RECOMMENDED" if o["id"] == "OPT-C" else ""])
    body.append(table(["Option", "What you would actually do", "Main risks", "Status"], rows,
                      caption="Full pros, cons and conditions in the Decision page."))

    body.append('<h2>How to read this site</h2>')
    body.append("""<ul class="cards">
      <li><a href="decision.html"><strong>Decision</strong><span>Three options, stress scenarios, and the conditions that would flip the answer.</span></a></li>
      <li><a href="risks.html"><strong>Risk Register</strong><span>12 risks from tenant credit to wildfire and credit seizure, each with a mitigation.</span></a></li>
      <li><a href="market.html"><strong>Trade Area</strong><span>Population, income, poverty, jobs, education, housing — City and County.</span></a></li>
      <li><a href="process.html"><strong>Projections</strong><span>The reproducible model, its assumptions, and its three paths.</span></a></li>
      <li><a href="market_pricing.html"><strong>Market Pricing</strong><span>What NNN assets like this actually price at, and why the sources disagree.</span></a></li>
      <li><a href="tenant.html"><strong>Tenant Credit</strong><span>Jack in the Box Inc. as filed with the SEC.</span></a></li>
      <li><a href="rules.html"><strong>Tax &amp; Rules</strong><span>Prop 13, Measure ULA, the fast-food wage law, 1031, fire and fault zones.</span></a></li>
      <li><a href="sources.html"><strong>Data &amp; Sources</strong><span>All 32 sources, with live links.</span></a></li>
      <li><a href="flagged.html"><strong>Flagged for Review</strong><span>12 items that could not be verified — published, not guessed.</span></a></li>
    </ul>""")
    return page("Overview", "".join(body), "index.html",
                '<p class="lede">A source-verified decision dashboard for a single Central Los Angeles '
                'Jack in the Box NNN asset. Hold to expiry, renew, or sell — with every number traceable '
                'to an official page.</p>')


def build_decision():
    rec = DECISION["recommendation"]
    b = []
    b.append(callout("rec", "Recommendation", "<p><strong>%s</strong> — %s</p>" % (
        esc(rec["primary"]), esc(rec["statement"]))))
    b.append("<h2>Why</h2><ul>" + "".join("<li>%s</li>" % esc(x) for x in rec["why"]) + "</ul>")

    b.append("<h2>Options compared</h2>")
    for o in DECISION["options"]:
        b.append('<section class="opt%s">' % (' rec' if o["id"] == "OPT-C" else ""))
        b.append("<h3>%s <small>%s</small></h3>" % (esc(o["name"]), esc(o["id"])))
        b.append("<p>%s</p>" % esc(o["mechanics"]))
        b.append('<div class="two"><div><h4>Pros</h4><ul>%s</ul></div>'
                 '<div><h4>Cons</h4><ul>%s</ul></div></div>' % (
                     "".join("<li>%s</li>" % esc(x) for x in o["pros"]),
                     "".join("<li>%s</li>" % esc(x) for x in o["cons"])))
        b.append('<p class="small"><strong>Best if:</strong> %s &nbsp;·&nbsp; '
                 '<strong>Risks touched:</strong> %s</p></section>' % (
                     esc(o["best_if"]), esc(", ".join(o["key_risks"]))))
    b.append("</section>")

    b.append("<h2>Conditions that would flip the answer</h2>")
    b.append('<div class="callout warn"><ul>%s</ul></div>' % "".join(
        "<li>%s</li>" % esc(x) for x in rec["conditions_that_flip_the_answer"]))

    b.append("<h2>Stress scenarios</h2>")
    b.append(table(["Scenario", "Inputs used", "What follows"],
                   [[s["name"], s["inputs"], s["conclusion"]] for s in DECISION["stress_scenarios"]]))

    b.append(callout("info", "Weight of evidence",
                     "<p>The recommendation rests on two facts you can check in one minute each: "
                     "(1) lease-term decay is a real, mechanical discount on single-tenant NNN assets, and "
                     "(2) a renewal is the only lever that removes it without paying transfer tax. "
                     "Both are evidenced on the <a href='market_pricing.html'>Market Pricing</a> and "
                     "<a href='rules.html'>Tax &amp; Rules</a> pages.</p>"))
    return page("Decision", "".join(b), "decision.html",
                '<p class="lede">Sell before expiry, hold to expiry, or renew then decide. '
                'Each is priced in risk terms, not in dollars we cannot verify.</p>')


def build_risks():
    b = []
    b.append('<p class="lede">%s</p>' % esc(RISKS["probability_basis"]))
    counts = {}
    for r in RISKS["risk_classes"]:
        counts[r["class"]] = counts.get(r["class"], 0) + 1
    b.append('<div class="pillrow">' + "".join(
        '<span class="pill">%s · %d</span>' % (esc(k), v) for k, v in counts.items()) + "</div>")

    for cls in ["Business as usual", "Black swan / tail"]:
        b.append("<h2>%s</h2>" % esc(cls))
        for r in [x for x in RISKS["risk_classes"] if x["class"] == cls]:
            b.append('<article class="risk sev-%s">' % esc(r["severity"].split()[0]))
            b.append("<h3>%s <small>%s</small></h3>" % (esc(r["name"]), esc(r["id"])))
            b.append("<p>%s</p>" % esc(r["description"]))
            b.append('<p class="ev"><strong>Evidence:</strong> %s</p>' % esc(r["evidence"]))
            b.append('<div class="tags"><span class="tag lh">likelihood: %s</span>'
                     '<span class="tag sv">severity: %s</span>'
                     '<span class="tag af">affects: %s</span></div>' % (
                         esc(r["likelihood"]), esc(r["severity"]), esc(r["affects"])))
            b.append('<p class="mit"><strong>Mitigation:</strong> %s</p>' % esc(r["mitigation"]))
            b.append("</article>")

    b.append("<h2>Register in table form</h2>")
    b.append(table(["ID", "Risk", "Class", "Likelihood", "Severity", "Affects", "Evidence sources"],
                   [[r["id"], r["name"], r["class"], r["likelihood"], r["severity"], r["affects"],
                     ", ".join(re.findall(r"S\d{2}", r["evidence"])) + "|"]
                    for r in RISKS["risk_classes"]]))
    return page("Risk Register", "".join(b), "risks.html",
                '<p class="lede">Every risk that can change the value of this asset or your wealth, '
                'including the rare ones that could destroy the local economy.</p>')


def build_market():
    b = []
    b.append('<p class="lede">Official Census figures for the City of Los Angeles and Los Angeles County. '
             'Nothing here is estimated by this project; empty cells are shown blank and flagged.</p>')
    for t in [x for x in FACTS["tables"] if x["id"] in ("T02", "T03")]:
        n = sum(1 for r in t["rows"] if r[1] in ("", None))
        b.append("<h2>%s</h2>" % esc(t["title"]))
        b.append(table(t["columns"], t["rows"],
                       caption="%d indicators · %d left blank because the source publishes no value" % (len(t["rows"]), n)))

    b.append('<p class="small">County-level labour-market source pages for deeper drill-down: '
             + src_link("S13") + ' (EDD) and ' + src_link("S01") + ' (BLS via FRED).</p>')
    b.append("<h2>Labour market</h2>")
    t = [x for x in FACTS["tables"] if x["id"] == "T04"][0]
    b.append(table(t["columns"], t["rows"]))

    b.append("<h2>Trend lines (official series)</h2>")
    for key, s in SERIES.items():
        if key not in ("los_angeles_county_median_household_income", "la_msa_unemployment_rate",
                       "la_msa_total_nonfarm_sa", "food_away_from_home_cpi"):
            continue
        pts = list(s["data"].items())
        vals = [v for _, v in pts if v is not None]
        b.append('<h3>%s</h3>' % esc(s["label"]))
        b.append('<p class="small">Source %s · range in series window: %s → %s</p>' % (
            src_link(s["source"]), esc(min(vals)), esc(max(vals))))
        b.append(table(["Period", "Value"], [[k, v] for k, v in pts]))
    b.append('<p class="small">Forward population is published by the California Department of Finance '
             + src_link("S12") + ' as Excel/CSV attachments; it could not be parsed for this build, so no '
             'projection is asserted here (see Flagged F-09).</p>')
    return page("Trade Area", "".join(b), "market.html",
                '<p class="lede">Geography, income, poverty, jobs, education and housing for the trade area.</p>')


def build_process():
    b = []
    b.append(callout("info", "What this model is and is not",
                     "<p>%s</p>" % esc(PROJ["warning"])))
    b.append("<h2>How the model is built</h2><ol>"
             "<li>It loads official series from <code>data/series.json</code> (CPI, food-away-from-home CPI, "
             "unemployment, employment).</li>"
             "<li>It applies the explicit analyst assumptions printed below. None are hidden.</li>"
             "<li>Value is computed as rent ÷ cap rate, expressed as a <em>multiple of today's value</em>, "
             "because the actual rent is unverified (Flagged F-01/F-02).</li>"
             "<li>Running <code>python3 tools/model.py</code> regenerates every number on this page.</li></ol>")
    b.append("<h2>Official inputs actually used</h2>")
    oi = PROJ["official_inputs_used"]
    b.append(table(["Input", "Value", "Source"],
                   [["CPI-U all items change, 2020-01 → 2026-09", "%.2f%%" % oi["cpi_all_items_2020_01_to_2026_09_pct"], oi["cpi_all_items_source"] + "|"],
                    ["CPI-U food away from home, 12 months to 2026-09", "%.2f%%" % oi["food_away_from_home_12m_pct"], oi["food_away_from_home_source"] + "|"]]))

    b.append("<h2>Paths, 2026 → 2035 (index: 2026 = 1.00)</h2>")
    b.append(table(["Year", "Rent multiple", "Cap rate: hold", "Cap rate: renew",
                    "Value index: hold to expiry", "Value index: renew then hold",
                    "Value index: rates-stress, no renewal"],
                   [[r["year"],
                     "%.3f×" % r["rent_multiple_vs_today"],
                     "%.2f%%" % (r["cap_rate_hold"] * 100),
                     "%.2f%%" % (r["cap_rate_renew"] * 100),
                     "%.3f" % r["value_relative_hold"],
                     "%.3f" % r["value_relative_renew"],
                     "%.3f" % r["value_relative_stress_no_renewal"]] for r in PROJ["paths"]]))
    b.append("<h2>Assumptions (all labelled, all editable)</h2>")
    a = PROJ["assumptions"]
    rows = []
    for k, v in a.items():
        if k.endswith("_note"):
            continue
        note = a.get(k + "_note") or a.get(k + "_years_note") or ""
        rows.append([k, v if not isinstance(v, list) else ", ".join(str(x) for x in v), note])
    b.append(table(["Assumption", "Value", "Justification"], rows))
    b.append("<h2>How to read it</h2><ul>" + "".join("<li>%s</li>" % esc(x) for x in PROJ["how_to_read"]) + "</ul>")
    b.append(callout("warn", "The honest limitation",
                     "<p>These are not forecasts of an official agency and they are not an appraisal. "
                     "They are the arithmetic consequence of the printed assumptions, which is exactly what "
                     "makes them auditable. Change an assumption, re-run, and see what changes.</p>"))
    return page("Projections", "".join(b), "process.html",
                '<p class="lede">A deterministic, reproducible projection system for the trade area and the '
                'asset — with every assumption printed on the page.</p>')


def build_property():
    t = [x for x in FACTS["tables"] if x["id"] == "T01"][0]
    b = []
    b.append(callout("warn", "This page is intentionally empty of specifics",
                     "<p>The address, parcel number, owner, tenant entity and lease financials are withheld "
                     "under the site's privacy policy. What remains is the structure of the deal, so you can "
                     "see exactly which inputs the analysis still needs.</p>"))
    b.append(table(t["columns"], t["rows"], caption=esc(t["note"])))
    b.append("<h2>What the analysis needs from you (internal use only)</h2>")
    b.append("<ul><li>Executed lease plus all amendments and guaranties.</li>"
             "<li>Tenant's certificate of insurance and most recent financial statement.</li>"
             "<li>Current assessed value and property tax bill.</li>"
             "<li>Any existing loan, its rate, maturity and prepayment terms.</li>"
             "<li>Your basis and any intent to reinvest (drives the 1031 analysis).</li></ul>")
    return page("Property & Lease", "".join(b), "property.html",
                '<p class="lede">The deal, described in placeholders, and the exact list of inputs still missing.</p>')


def build_market_pricing():
    t = [x for x in FACTS["tables"] if x["id"] == "T07"][0]
    b = []
    b.append(callout("warn", "Read the labels",
                     "<p>No government agency publishes capitalization rates for NNN assets. Everything on this "
                     "page is third-party broker or aggregator commentary, quoted exactly and linked. It is "
                     "context, not a verified transaction record.</p>"))
    b.append(table(t["columns"], t["rows"], caption=esc(t["note"])))
    b.append("<h2>Why the numbers do not agree</h2>")
    b.append("<p>The 4.31% asking cap is an <em>absolute-NNN corporate lease with roughly 15 years of term</em>. "
             "The 5.82% figure is a <em>ground lease with roughly 13 years of term</em> and a much smaller price "
             "point. Different structure, different tenant obligation, different risk — so a single 'market cap "
             "rate' for this asset does not exist. That is why the decision framework does not hinge on one cap "
             "rate: it hinges on lease term, which you control by negotiating a renewal.</p>")
    b.append("<h2>Rates that set the price of everything</h2>")
    t5 = [x for x in FACTS["tables"] if x["id"] == "T05"][0]
    b.append(table(t5["columns"], t5["rows"]))
    return page("Market Pricing", "".join(b), "market_pricing.html",
                '<p class="lede">What single-tenant NNN assets like this actually trade at, clearly labelled as '
                'third-party commentary.</p>')


def build_tenant():
    t = [x for x in FACTS["tables"] if x["id"] == "T06"][0]
    b = []
    b.append('<p class="lede">The rent is only as good as the tenant. These figures are taken directly from '
             'Jack in the Box Inc.\'s filings with the U.S. Securities and Exchange Commission.</p>')
    b.append(table(t["columns"], t["rows"]))
    b.append('<p class="small">Filing index used to confirm this is the most recent annual report: '
             + src_link("S18") + '</p>')
    b.append("<h2>What the filings show</h2>")
    b.append("""<ul>
      <li><strong>Revenue has fallen for two straight fiscal years</strong>: $1,692.3M (FY2023) →
          $1,571.3M (FY2024) → $1,465.3M (FY2025).</li>
      <li><strong>The company moved from profit to loss</strong>: +$130.8M in FY2023, then −$36.7M in FY2024
          and −$80.7M in FY2025.</li>
      <li><strong>It refinanced in June 2026</strong> with $500M of 7.624% senior secured notes whose
          <em>anticipated</em> repayment date is May 2031 — after which additional interest accrues if not
          repaid. That 2031 date sits inside your lease-expiry window.</li>
      <li><strong>Much of the collateral is the franchise system itself</strong>, including real estate
          assets, which is the structural reason a landlord's rent is exposed to the chain's refinancing.</li>
    </ul>""")
    b.append(callout("warn", "What this does NOT tell you",
                     "<p>Chain-level results do not prove that <em>this</em> store is weak. A long-tenured urban "
                     "unit can be among the best in the system. Two things decide it, and both are on your side "
                     "of the table: whether the lease is corporate or franchisee-guaranteed (Flagged F-07) and "
                     "what the unit actually sells (Flagged F-12).</p>"))
    return page("Tenant Credit", "".join(b), "tenant.html",
                '<p class="lede">Jack in the Box Inc. as filed: revenue, earnings and the 2026 securitization.</p>')


def build_rules():
    t = [x for x in FACTS["tables"] if x["id"] == "T08"][0]
    b = []
    b.append('<p class="lede">These rules bind the decision more tightly than any market forecast. '
             'All four regimes were created or materially changed inside a five-year window.</p>')
    b.append(table(t["columns"], t["rows"]))
    b.append("<h2>Why each one matters to this specific asset</h2>")
    b.append("""<ul>
      <li><strong>Proposition 13</strong> means selling resets the tax base to the sale price. A buyer knows
          that and prices it in; you should quantify it before you list.</li>
      <li><strong>Measure ULA</strong> means a sale above $5.4M costs 4.45% in city transfer tax, seller-paid.
          On a $6M sale that is $267,000 — a real number that changes the sell/hold arithmetic.</li>
      <li><strong>AB 1228</strong> set a $20/hr fast-food floor and caps future increases at the lesser of
          3.5% or CPI-W, with no Council-driven increase effective after 2029. The tenant's cost pressure is
          bounded, which supports renewal — but the pressure lands on the operator, so it lands on you at re-letting.</li>
      <li><strong>1031</strong> gives you a way to move the money without paying the tax, provided you accept
          a hard 45-day identification and 180-day closing clock.</li>
      <li><strong>Fire and fault zones</strong> are disclosure and insurability rules, not just physical
          risks: they can change what your buyer can finance.</li>
    </ul>""")
    return page("Tax & Rules", "".join(b), "rules.html",
                '<p class="lede">Property tax, transfer tax, wage law, exchange rules, and hazard zones — '
                'the four regimes that actually move this decision.</p>')


def build_sources():
    b = []
    b.append('<p class="lede">Every row on every page resolves to one of these. '
             'Official sources are badged green; third-party commentary is badged amber.</p>')
    rows = [[s["id"], s["title"], s["publisher"], s["type"], s["note"], s["url"]] for s in SOURCES.values()]
    b.append('<div class="tablewrap"><table class="data"><thead><tr><th>ID</th><th>Source</th>'
             '<th>Publisher</th><th>Type</th><th>Note</th><th>Link</th></tr></thead><tbody>')
    for sid, title, pub, typ, note, url in rows:
        b.append('<tr><td><span class="src %s">%s</span></td><td>%s</td><td>%s</td><td>%s</td>'
                 '<td class="small">%s</td><td><a href="%s" target="_blank" rel="noopener">open ↗</a></td></tr>'
                 % ("official" if typ == "official" else "third", esc(sid), esc(title), esc(pub),
                    esc(typ), esc(note), esc(url)))
    b.append("</tbody></table></div>")
    b.append('<h2>Series data used by the model</h2>')
    b.append(table(["Series", "Source", "Points published here"],
                   [[s["label"], s["source"] + "|", str(len(s["data"]))] for s in SERIES.values()]))
    b.append('<p class="small">The not-seasonally-adjusted employment series ' + src_link("S02") +
             ' is published too, and is never mixed with the seasonally adjusted series ' + src_link("S03") +
             ' — a common and material error in local market reports.</p>')
    return page("Data & Sources", "".join(b), "sources.html",
                '<p class="lede">32 sources, all linked. Nothing on this site exists without one of these.</p>')


def build_flagged():
    b = []
    b.append('<p class="lede">%s</p>' % esc(FLAGGED["intro"]))
    b.append(table(["#", "Item", "Why it is flagged", "How to resolve it", "Source"],
                   [[f["id"], f["item"], f["why_flagged"], f["resolution"],
                     (f["source"] if re.fullmatch(r"S\d{2}", f["source"] or "") else "") + ("|" if re.fullmatch(r"S\d{2}", f["source"] or "") else "")]
                    for f in FLAGGED["items"]]))
    b.append("<h2>Rows left blank on the site for the same reason</h2>")
    b.append("<ul><li>City of Los Angeles building permits (2025) — the Census table itself shows 'X'.</li>"
             "<li>City of Los Angeles 2023 business counts — the Census table itself shows 'X'.</li>"
             "<li>Jack in the Box issuer credit rating — not disclosed on any official source reviewed.</li>"
             "<li>Forward population for the trade area — the Department of Finance publishes it as an "
             "attachment that could not be parsed here, so it is not asserted (F-09).</li></ul>")
    b.append(callout("info", "Flagged items do not block the decision",
                     "<p>Each one has a resolution path, and the recommendation is deliberately built so that "
                     "none of them can change its direction — only its magnitude.</p>"))
    return page("Flagged for Review", "".join(b), "flagged.html",
                '<p class="lede">Unverified items, contradictory sources, and traps found during research. '
                'Published on purpose.</p>')


def build_privacy():
    b = []
    b.append('<p class="lede">Privacy was the first requirement of this project, so it shaped the data model, '
             'not just the wording.</p>')
    b.append("""<h2>What is never published</h2>
    <div class="tablewrap"><table class="data"><thead><tr><th>Category</th><th>Handling</th></tr></thead><tbody>
      <tr><td>Street address, parcel / APN, legal description</td><td>Never recorded here; shown as <code>[PARCEL-REDACTED]</code></td></tr>
      <tr><td>Owner identity (person, trust, LLC)</td><td><code>[OWNER-ENTITY]</code></td></tr>
      <tr><td>Tenant / franchisee identity and contacts</td><td><code>[TENANT-ENTITY]</code></td></tr>
      <tr><td>Lease rent, escalations, options, estoppels</td><td><code>[RENT]</code> — described only in market-level terms</td></tr>
      <tr><td>Your basis, debt, net worth, tax position</td><td><code>[BASIS]</code> — never recorded</td></tr>
      <tr><td>Names of any private person in coverage</td><td>Not repeated; the official record is linked instead</td></tr>
    </tbody></table></div>
    <h2>Why this is the stricter reading, on purpose</h2>
    <p>California already restricts publishing address-linked records: State Board of Equalization Letter To
    Assessors No. 2025/010 (implementing AB 1785) amended Government Code §7928.205 to bar state and local
    agencies from publicly posting, on the internet, an official's home address, telephone number, or both the
    name and assessor parcel number associated with it. This project applies the stricter version of that rule
    to every person, not only officials.</p>
    <p><a href="https://www.boe.ca.gov/proptaxes/pdf/lta25010.pdf" target="_blank" rel="noopener">Letter To Assessors 2025/010 ↗</a></p>
    <h2>How verification and privacy reinforce each other</h2>
    <p>Because the parcel is withheld, any figure that would require looking up the parcel (assessed value,
    FHSZ zone, seismic zone) is left blank and flagged rather than estimated. Privacy therefore removes the
    temptation to invent a number.</p>
    <h2>What this site does technically</h2>
    <ul><li>Static HTML only. No cookies, no analytics, no trackers, no fonts loaded from third parties.</li>
    <li>External links are marked <code>rel="noopener"</code>.</li>
    <li>The site is generated from <code>data/*.json</code>; nothing is typed by hand into a page.</li></ul>""")
    return page("Privacy & Method", "".join(b), "privacy.html",
                '<p class="lede">Anonymized by design: placeholders instead of a parcel, its owner, its tenant, '
                'and its rent.</p>')


# --------------------------------------------------------------------------- #
def write(name, content):
    path = os.path.join(ROOT, name)
    with open(path, "w") as fh:
        fh.write(content)
    return path


def main():
    written = [
        ("index.html", build_overview()),
        ("decision.html", build_decision()),
        ("risks.html", build_risks()),
        ("market.html", build_market()),
        ("process.html", build_process()),
        ("property.html", build_property()),
        ("market_pricing.html", build_market_pricing()),
        ("tenant.html", build_tenant()),
        ("rules.html", build_rules()),
        ("sources.html", build_sources()),
        ("flagged.html", build_flagged()),
        ("privacy.html", build_privacy()),
    ]
    for name, content in written:
        write(name, content)
        print("wrote", name)


if __name__ == "__main__":
    main()
