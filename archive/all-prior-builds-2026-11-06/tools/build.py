#!/usr/bin/env python3
"""
Static site generator for the SP-01 dossier.

Reads data/*.json and writes plain HTML into archive/arena-972c721e/. No framework, no external
CSS/JS, no analytics, no fonts fetched from anywhere: the published site makes
zero third-party requests, which is also the point for privacy.

Run:  python3 tools/build.py
"""

import json
import os
import shutil
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "archive", "arena-972c721e")
DATA = os.path.join(ROOT, "data")


def load(name):
    with open(os.path.join(DATA, name)) as fh:
        return json.load(fh)


SOURCES = load("sources.json")
FACTS = load("facts.json")
MODEL = load("model.json")

SRC_BY_ID = {s["id"]: s for s in SOURCES["sources"]}
ACCESSED = SOURCES["meta"]["accessed"]

NAV = [
    ("index.html", "Dashboard"),
    ("property.html", "Property"),
    ("market.html", "Market"),
    ("tenant.html", "Tenant"),
    ("valuation.html", "Valuation"),
    ("decision.html", "Decision"),
    ("risks.html", "Risks"),
    ("sources.html", "Sources"),
    ("flagged.html", "Flagged"),
]

VERIFIED = [r for r in FACTS["rows"] if r["status"] == "verified"]
DERIVED = [r for r in FACTS["rows"] if r["status"] == "derived"]
FLAGGED = [r for r in FACTS["rows"] if r["status"] == "unverified"]


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def money(x):
    if x is None:
        return "—"
    neg = x < 0
    s = f"${abs(int(round(x))):,}"
    return f"({s})" if neg else s


def pct(x, dp=1):
    return "—" if x is None else f"{x:.{dp}f}%"


def src_chips(ids):
    if not ids:
        return '<span class="src none" title="No official source available">none</span>'
    out = []
    for i in ids:
        s = SRC_BY_ID.get(i)
        t = esc(s["title"] + " — " + s["publisher"]) if s else ""
        out.append(f'<a class="src" href="sources.html#{i}" title="{t}">{i}</a>')
    return " ".join(out)


def chips_for_facts(fact_ids):
    """Resolve a list of fact IDs to the deduplicated source chips behind them."""
    ids = []
    for f in FACTS["rows"]:
        if f["id"] in fact_ids:
            for sid in f["sources"]:
                if sid not in ids:
                    ids.append(sid)
    return src_chips(ids)


def badge(status):
    labels = {
        "verified": ("verified", "Confirmed on an official source"),
        "derived": ("derived", "Arithmetic on verified figures — see note"),
        "unverified": ("flagged", "Could not be confirmed from an official source"),
        "industry": ("industry", "Non-government source — never mixed with verified data"),
    }
    cls, tip = labels.get(status, ("flagged", ""))
    return f'<span class="badge {cls}" title="{esc(tip)}">{cls}</span>'


def fact_table(rows, show_cat=False):
    head = ["ID", "Metric", "Value", "Unit", "Period", "Sources", "Status"]
    if show_cat:
        head.insert(1, "Category")
    h = "".join(f"<th>{x}</th>" for x in head)
    body = []
    for r in rows:
        val = esc(r["value"]) if r["value"] not in ("", None) else '<span class="blank">— blank —</span>'
        cells = [f'<td class="mono">{r["id"]}</td>', f"<td>{esc(r['metric'])}</td>",
                 f'<td class="val">{val}</td>', f"<td>{esc(r['unit'])}</td>",
                 f"<td class='nowrap'>{esc(r['period'])}</td>", f"<td>{src_chips(r['sources'])}</td>",
                 f"<td>{badge(r['status'])}</td>"]
        if show_cat:
            cells.insert(1, f"<td>{esc(r['cat'])}</td>")
        note = f'<div class="note">{esc(r["note"])}</div>' if r.get("note") else ""
        body.append("<tr>" + "".join(cells) + "</tr>")
        if note:
            body.append(f'<tr class="note-row"><td></td><td colspan="{len(head)-1}">{note}</td></tr>')
    return f'<div class="table-wrap"><table><thead><tr>{h}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def page(filename, title, subtitle, body, active=None):
    current = active or filename
    parts = []
    for href, label in NAV:
        cls = " class=\"active\"" if href == current else ""
        parts.append('<a href="%s"%s>%s</a>' % (href, cls, label))
    links = "".join(parts)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="index,follow">
<meta name="description" content="Anonymised, source-verified analysis of a single-tenant net-lease property in Central Los Angeles. No personal information is published.">
<title>{esc(title)} · SP-01 Dossier</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site">
  <div class="wrap">
    <div class="brand">
      <span class="mark">SP-01</span>
      <span class="brand-text"><strong>Net-lease decision dossier</strong>
      <small>Central Los Angeles · Jack in the Box · NNN · expiry 2030&ndash;2035</small></span>
    </div>
    <nav>{links}</nav>
  </div>
</header>
<main id="main" class="wrap">
<h1>{esc(title)}</h1>
<p class="lede">{subtitle}</p>
{body}
</main>
<footer class="site">
  <div class="wrap">
    <p><strong>Privacy:</strong> this site contains no address, parcel number, owner name, rent, or NOI. The subject property is referred to only as SP-01. Anything knowable only from private documents is shown as <code>[WITHHELD]</code> or as a labelled assumption.</p>
    <p><strong>Verification:</strong> {len(VERIFIED)} facts confirmed against official sources, {len(DERIVED)} derived by arithmetic on those facts, {len(FLAGGED)} published as blank and flagged. Every row links to the source that was actually opened. Data accessed {ACCESSED}.</p>
    <p>This is analysis, not legal, tax or investment advice. Verify the lease, the parcel and the tenant before acting.</p>
  </div>
</footer>
</body>
</html>
"""
    with open(os.path.join(SITE, filename), "w") as fh:
        fh.write(html)


def cat_rows(key):
    return [r for r in FACTS["rows"] if r["cat"] == key]


# --------------------------------------------------------------------------
# pages
# --------------------------------------------------------------------------
def build_index():
    best = MODEL["decision"]["matrix"][0]
    strat = {s["id"]: s for s in MODEL["scenarios"][0]["strategies"]}
    der = MODEL["derived"]
    central = [s for s in MODEL["scenarios"] if s["noi"] == 180000]

    kpis = [
        ("Recommendation", "Extend now · hold ~5 yrs · sell with term", "Strategy E — highest risk-adjusted score (4.20 / 5)", ""),
        ("What the term is worth", f"+{der['term_premium_3_to_9_pct']}%",
         "Same NOI at 9 years of term instead of 3. Term, not rent, is the biggest lever in the file.", ""),
        ("Sell-today friction", pct(der["sell_cost_pct_pre_ula"], 2),
         "Brokerage, closing, city and county transfer tax — before any Measure ULA.", ""),
        ("Measure ULA cliff", money(der["ula_at_threshold"]),
         f"Tax triggered the moment a sale price crosses ${der['ula_threshold']:,}.", ""),
        ("Tenant trajectory", "−1.1%", "JACK system same-store sales, Q3 FY2026. 50–60 closures guided for FY2026.", ""),
        ("Metro labour market", "4.4%", "LA unemployment, Sep 2026 — tight labour, but total jobs only +0.5% year over year.", ""),
        ("10-year Treasury", "4.90%", "The discount rate that sets every cap rate in this file. Verified 2026-11-04.", ""),
        ("Verified vs flagged", f"{len(VERIFIED)} / {len(FLAGGED)}",
         "Facts confirmed on official sources versus rows deliberately left blank and flagged.", ""),
    ]
    kpi_html = "".join(
        f'<div class="kpi"><div class="kpi-label">{esc(k)}</div>'
        f'<div class="kpi-value">{esc(v)}</div><div class="kpi-note">{esc(n)}</div></div>'
        for k, v, n, _ in kpis
    )

    rank_rows = []
    names = {s["id"]: s["name"] for s in MODEL["scenarios"][0]["strategies"]}
    for item in MODEL["decision"]["matrix"]:
        sid = item["id"]
        npvs = [st["npv"] for sc in central for st in sc["strategies"] if st["id"] == sid]
        rank_rows.append(
            f'<tr><td class="rank">{MODEL["decision"]["ranking"].index(sid)+1}</td>'
            f'<td class="mono">{sid}</td><td>{esc(names[sid])}</td>'
            f'<td class="num">{item["weighted_score"]:.2f}</td>'
            f'<td class="num">{money(min(npvs))} – {money(max(npvs))}</td></tr>'
        )

    body = f"""
<section class="hero">
  <p class="tag">Decision brief · built {ACCESSED}</p>
  <h2 class="hero-q">Sell the Jack in the Box before the lease expires, or renew and hold?</h2>
  <p class="hero-a"><strong>Renew — but renew now, and do not sell into the expiry.</strong>
  The single most valuable thing in this file is <em>time</em>: a buyer pays roughly
  <strong>{der['term_premium_3_to_9_pct']}% more</strong> for the same net operating income when nine years of lease term remain instead of three.
  Waiting until the lease is nearly over is the one path the model shows destroying value in
  every expiry case, and it is also the path that requires no decision at all.</p>
  <p class="hero-a">The recommended sequence is: <strong>negotiate a long extension now</strong> (while the tenant still
  wants the site), <strong>hold about five years</strong> to keep the rent and the Proposition 13 tax wedge,
  then <strong>sell with five years of firm term</strong> into the deepest buyer pool. If the tenant refuses
  to extend, the answer flips: sell within twelve months rather than ride the lease to expiry.</p>
</section>

<div class="kpis">{kpi_html}</div>

<h2>Decision at a glance</h2>
<p>Five strategies, each run against the owner's whole stated expiry window (2030, 2032 and 2035)
and three illustrative NOI cases. Scores are judgement against the verified evidence; the
weights and every cell are published on the <a href="decision.html">Decision</a> page so you can
disagree with a specific cell rather than the whole conclusion.</p>
<div class="table-wrap"><table>
<thead><tr><th>#</th><th>ID</th><th>Strategy</th><th class="num">Score / 5</th><th class="num">NPV vs selling today (central NOI)</th></tr></thead>
<tbody>{''.join(rank_rows)}</tbody></table></div>
<p class="small">NPV is measured at a 7.40% required return against a sell-today baseline, so 0 means
"no better or worse than selling now". Negative means "you would be paying to wait".</p>

<h2>The three findings that drive the answer</h2>
<div class="cards">
  <article class="card"><h3>1 · Term is the price</h3>
  <p>Cap rates are a function of how long the buyer can count on the rent. In this model
  3 years of term prices at {MODEL['term_value'][2]['cap_pct']}%, five years at {MODEL['term_value'][4]['cap_pct']}%,
  nine years at {MODEL['term_value'][8]['cap_pct']}%. On unchanged income that is a
  <strong>{der['term_premium_3_to_5_pct']}% step</strong> from three to five years and
  <strong>{der['term_premium_3_to_9_pct']}%</strong> from three to nine.</p>
  <p><a href="valuation.html">See the term curve →</a></p></article>

  <article class="card"><h3>2 · The tenant is contracting</h3>
  <p>Jack in the Box Inc. reported system same-store sales of <strong>−1.1%</strong>, guided to
  <strong>50–60 closures</strong> in fiscal 2026 — "most of which will be franchise restaurants" — and
  folds "block closure" and "selling real estate" into its own turnaround plan. A renewal is not
  something to assume; it is something to negotiate while you still have something to trade.</p>
  <p><a href="tenant.html">Read the SEC record →</a></p></article>

  <article class="card"><h3>3 · The area is full, but not growing</h3>
  <p>Los Angeles unemployment is <strong>4.4%</strong> — effectively full employment — while total
  nonfarm jobs grew <strong>0.5%</strong> year over year and the city's population is down
  <strong>0.8%</strong> since 2020 (the county, −3.2%). Demand is deep but static, and the local
  wage floor is the highest in the country for this format.</p>
  <p><a href="market.html">Interrogate the market data →</a></p></article>
</div>

<h2>Where the risk sits</h2>
<div class="cards">
  <article class="card warn"><h3>Black-swan surface</h3>
  <p>Wildfire, earthquake, and the insurance channel that links them. California's FAIR Plan now
  carries <strong>21,717 commercial policies</strong> (from 7,315 in 2022) and <strong>$724 billion</strong>
  of exposure. A net lease passes insurance cost to the tenant — which protects the owner's income
  but raises the tenant's occupancy cost, and therefore the odds it walks.</p>
  <p><a href="risks.html">The full risk register →</a></p></article>

  <article class="card warn"><h3>What is missing</h3>
  <p>No address, no rent, no NOI, no lease document, no parcel number. Those are withheld on purpose
  and every property-specific number on this site is a labelled assumption band. The framework is
  sound; the final arithmetic is not, until the documents are read.</p>
  <p><a href="flagged.html">{len(FLAGGED)} flagged items →</a></p></article>

  <article class="card"><h3>How to read this site</h3>
  <p>Everything either says <span class="badge verified">verified</span> with a link to the official
  page that was actually opened, <span class="badge derived">derived</span> where it is arithmetic on
  those figures, or <span class="badge flagged">flagged</span> where it could not be confirmed and was
  left blank instead of guessed.</p>
  <p><a href="sources.html">The source ledger →</a></p></article>
</div>
"""
    page("index.html", "Dashboard", "One property, one question, one answer — with the working shown.", body)


def build_property():
    timeline = [
        ("Today", "Lease in force. Remaining term is somewhere between 4 and 9 years, because the expiry sits somewhere in a five-year window. The owner has not supplied the exact date."),
        ("Notice window", "Typically 6–12 months before expiry in a net lease. This, not the expiry date, is the real decision deadline — miss it and the tenant's option lapses and the asset is priced as a vacancy risk."),
        ("2030–2035", "Lease expiry, per the owner's own description. At expiry the tenant either renews, renegotiates, or leaves."),
        ("Today to 2035", "The investment horizon used throughout the model."),
    ]
    tl = "".join(f'<li><strong>{esc(a)}</strong><span>{esc(b)}</span></li>' for a, b in timeline)

    known = [r for r in FACTS["rows"] if r["cat"] == "open"][:9]
    body = f"""
<section class="panel">
<h2>What is actually known</h2>
<ul class="tight">
  <li><strong>Asset type:</strong> single-tenant quick-service restaurant building on a net (NNN) lease.</li>
  <li><strong>Tenant brand:</strong> Jack in the Box (NASDAQ: JACK — verified via SEC filings).</li>
  <li><strong>Location granularity:</strong> "around Central Los Angeles" — the owner's own wording. Not narrowed further, by design.</li>
  <li><strong>Lease expiry:</strong> somewhere in 2030–2035 — the owner's own wording. Presented as three cases, not one number.</li>
  <li><strong>Decision to be made:</strong> sell before expiry, or renew and hold.</li>
</ul>
</section>

<section class="panel">
<h2>The lease clock</h2>
<p class="lede">A net lease does not end on the expiry date. It ends when the renewal option lapses, which is why the
notice window — not the expiry date — is the decision deadline.</p>
<ol class="timeline">{tl}</ol>
</section>

<h2>What is withheld, and why</h2>
<p>The brief requires that no personal information appears in the product. A property address is personal
information: it identifies the owner. So the address, parcel number, rent, NOI, tenant of record and lease
document are all withheld, and every analysis below is either area-level (public data) or explicitly
labelled as an assumption band.</p>
<div class="callout">
<strong>The consequence you should weigh:</strong> the decision framework is complete, but the final numbers are not.
The model runs on three illustrative NOI cases. Replace them with your actual NOI and the same engine
gives you your actual answer — that is what the <a href="valuation.html">Valuation page</a> and its
calculator are for.
</div>

<h2>Property-specific inputs</h2>
<p>Each row below is blank on purpose. "Unverified" here is not a data failure; it is a decision to publish a
gap rather than invent a number.</p>
{fact_table(known)}

<h2>Privacy statement</h2>
<div class="panel">
<p>This project processes no personal information. Specifically:</p>
<ul class="tight">
  <li>No name, address, parcel number, phone, email or account identifier is stored in this repository or published on this site.</li>
  <li>The subject property is labelled <code>SP-01</code> throughout, including in the source code, the data files and the model.</li>
  <li>The site makes zero third-party requests: no fonts, no analytics, no trackers, no CDN. The pages are plain HTML and one local stylesheet.</li>
  <li>The valuation calculator runs entirely in your browser. Nothing typed into it is transmitted, stored, logged or committed.</li>
  <li>Any figure that could only be known from private documents is rendered as <code>[WITHHELD]</code> rather than approximated.</li>
</ul>
</div>
"""
    page("property.html", "The property", "An anonymised dossier: what is known, what is withheld, and the lease clock that actually forces the decision.", body)


def build_market():
    def section(key, blurb=None):
        rows = cat_rows(key)
        if not rows:
            return ""
        title = next(c["title"] for c in FACTS["categories"] if c["key"] == key)
        blurb = blurb or next(c["blurb"] for c in FACTS["categories"] if c["key"] == key)
        return f"<h2>{esc(title)}</h2><p class='lede'>{esc(blurb)}</p>{fact_table(rows)}"

    body = f"""
<div class="callout">
<strong>Granularity warning.</strong> "Central Los Angeles" spans sub-markets with materially different income,
density and traffic profiles. Everything below is city-, county- or metro-level official data because a
trade-area analysis needs the address, which is withheld. Treat these as the economic weather, not as a
site appraisal.
</div>

{section("macro")}
{section("labor")}
{section("demo")}
{section("schools")}

<h2>What the numbers say together</h2>
<div class="cards">
  <article class="card"><h3>Tight, not growing</h3>
  <p>4.4% unemployment is full employment. But total nonfarm employment is up 0.5% year over year, and the
  city has lost 0.8% of its population since 2020 while the county lost 3.2%. A quick-service restaurant
  here competes for share in a market that is not expanding — which is exactly why the tenant's own
  same-store sales are negative.</p></article>

  <article class="card"><h3>The wage floor is the constraint</h3>
  <p>California's fast-food minimum wage is $20.00/hr, statutorily above the $16.90 state rate, and the
  Fast Food Council can raise it again. The state rate itself escalates with CPI-W, capped at 3.5% a year,
  and cannot be cut. The tenant's largest controllable cost has an upward ratchet written into law.</p></article>

  <article class="card"><h3>Deep demand, thin growth</h3>
  <p>$81.35 billion of retail sales and $17.37 billion of food-service sales is a very large pool. Household
  income of $81,939 against 16.5% poverty describes a market that is polarised — consistent with a
  value-oriented QSR, which is the brand's positioning.</p></article>
</div>

<h2>What is missing at this granularity</h2>
<p>Retail asking rents, sub-market vacancy, trade-area traffic counts and the parcel's own zoning cannot be
sourced from an official statistical series. No broker report is substituted for them. They are published
as blank and flagged on the <a href="flagged.html">Flagged for Review</a> page.</p>
"""
    page("market.html", "Market & area economics", "Official data on the economy the restaurant trades in — and a blunt note on what city-level averages can and cannot tell you.", body)


def build_tenant():
    rows = cat_rows("tenant")
    body = f"""
<section class="hero compact">
  <p class="tag">Tenant credit</p>
  <h2 class="hero-q">The lease is only as good as the operator behind it.</h2>
  <p class="hero-a">Jack in the Box Inc. is a public company, so its direction of travel is not a matter of
  opinion — it is in the filings. In the most recent quarter the system's same-store sales were
  <strong>−1.1%</strong>, the company guided to <strong>50–60 closures</strong> for the fiscal year (mostly
  franchised units), its franchise-level margin fell, bad debt rose, and its turnaround plan explicitly
  includes "block closure" and "selling real estate".</p>
  <p class="hero-a"><strong>For a landlord, that reads as: do not assume renewal.</strong> A lease expiring in
  2030–2035 is a negotiation to be started while the site still has strategic value to the operator, not a
  renewal to be collected at the end.</p>
</section>

<h2>The SEC record</h2>
<p>Every figure below is from the company's own Form 8-K earnings release for the quarter ended 5 July 2026,
filed 12 August 2026, plus the filing index. Each row links to the filing.</p>
{fact_table(rows)}

<h2>Why a landlord should read this differently than an investor</h2>
<div class="cards">
  <article class="card"><h3>Closures are mostly franchised</h3>
  <p>The guidance language matters: "approximately 50 to 60 closures, most of which will be franchise
  restaurants". If SP-01's tenant of record is a franchisee, the unit sits inside the segment being pruned.
  Which it is, is withheld — see the <a href="flagged.html">flagged list</a>.</p></article>

  <article class="card"><h3>Bad debt is rising</h3>
  <p>The company attributes part of the franchise-margin decline to higher bad debt. In a franchise system
  that usually means franchisees are not paying what they owe. A landlord's rent is in that same queue.</p></article>

  <article class="card"><h3>Real estate is a funding source</h3>
  <p>"Selling real estate" is named as a lever in the turnaround. That cuts both ways: it can mean the brand
  wants to monetise good sites (a sale-leaseback is a potential exit to the owner), or that it wants to
  shed sites it no longer wants.</p></article>

  <article class="card"><h3>Rent-to-sales is probably falling</h3>
  <p>Menu-price inflation for limited-service meals is +3.2% year over year. If the lease escalates at 2%,
  the rent-to-sales ratio falls, which makes the unit cheaper to keep. That is the single strongest argument
  for renewal — and the reason a renewal request is likely to be received seriously.</p></article>
</div>
"""
    page("tenant.html", "Tenant & brand credit", "What Jack in the Box Inc. has told the SEC, and what it means for a lease that expires between 2030 and 2035.", body)


def build_valuation():
    defs = MODEL["derived"]
    tv = MODEL["term_value"]

    term_rows = "".join(
        f'<tr><td class="num">{t["term_years"]}</td><td class="num">{t["cap_pct"]:.2f}%</td>'
        f'<td class="num">{money(t["value_per_100k_noi"])}</td>'
        f'<td class="num">{("+" if t["pct_vs_3yr"] > 0 else "")}{t["pct_vs_3yr"]:.1f}%</td></tr>'
        for t in tv
    )

    cap_rows = "".join(
        f'<tr><td>{esc(c["label"])}</td><td class="num">{c["cap_pct"]:.2f}%</td>'
        f'<td class="num">+{c["spread_bp"]} bp</td></tr>' for c in MODEL["cap_curve"]
    ) if "label" in MODEL["cap_curve"][0] else "".join(
        f'<tr><td class="num">{c["term_years"]:.0f} years</td><td class="num">{c["cap_pct"]:.2f}%</td>'
        f'<td class="num">+{round((c["cap_pct"]/100 - MODEL["verified_inputs"]["risk_free_10y_pct"]/100)*10000)} bp</td></tr>'
        for c in MODEL["cap_curve"]
    )

    # per-expiry strategy tables at the central NOI
    strat_tables = ""
    names = {s["id"]: s["name"] for s in MODEL["scenarios"][0]["strategies"]}
    for sc in [x for x in MODEL["scenarios"] if x["noi"] == 180000]:
        rows = []
        for st in sc["strategies"]:
            rows.append(
                f'<tr><td class="mono">{st["id"]}</td><td>{esc(st["name"])}</td>'
                f'<td class="num">{money(st["gross_price"])}</td>'
                f'<td class="num">{money(st["costs"]["net_proceeds"])}</td>'
                f'<td class="num">{money(st["npv"])}</td>'
                f'<td class="num">{pct(st["irr_pct"]) if st["irr_pct"] is not None else "n/a"}</td>'
                f'<td class="num">{money(st["terminal_wealth_2035"])}</td></tr>')
        strat_tables += f"""
<h3>If the lease expires in {sc['expiry']} ({sc['years_left']} years remaining)</h3>
<p class="small">Cap rate today on that remaining term: <strong>{sc['cap_today_pct']}%</strong>.
Selling today would net <strong>{money(sc['sell_today_net'])}</strong> after costs.</p>
<div class="table-wrap"><table>
<thead><tr><th>ID</th><th>Strategy</th><th class="num">Gross price</th><th class="num">Net proceeds</th>
<th class="num">NPV vs selling today</th><th class="num">IRR</th><th class="num">Wealth 2035</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>"""

    # NPV matrix across NOI x expiry
    npv_rows = ""
    for sc in MODEL["scenarios"]:
        by = {s["id"]: s["npv"] for s in sc["strategies"]}
        npv_rows += (f'<tr><td class="num">{money(sc["noi"])}</td><td class="num">{sc["expiry"]}</td>'
                     + "".join(f'<td class="num {"pos" if by[i] > 0 else ("neg" if by[i] < 0 else "")}">{money(by[i])}</td>'
                               for i in ["A", "B", "C", "D", "E"]) + "</tr>")

    # rate sensitivity at 180k / 2032
    sens = [sc for sc in MODEL["scenarios"] if sc["noi"] == 180000 and sc["expiry"] == 2032][0]["rate_sensitivity"]
    sens_rows = "".join(
        f'<tr><td class="num">{s["shift_bp"]:+d} bp</td><td class="num">{s["cap_pct"]:.2f}%</td>'
        f'<td class="num">{money(s["gross_value"])}</td><td class="num">{money(s["net_proceeds"])}</td>'
        f'<td>{"yes" if s["ula_applies"] else "no"}</td></tr>' for s in sens)

    assumptions_rows = "".join(
        f'<tr><td class="mono">{a["key"]}</td><td>{esc(a["name"])}</td>'
        f'<td class="val">{esc(a["value"])}</td><td>{esc(a["basis"])}</td></tr>'
        for a in MODEL["assumptions"])

    body = f"""
<section class="hero compact">
  <p class="tag">Valuation engine</p>
  <h2 class="hero-q">Value is income divided by a cap rate. Everything else is an argument about the cap rate.</h2>
  <p class="hero-a">The cap rate is not a constant. It is a function of how many years of rent the buyer can
  count on, and of what the risk-free rate is that day. So the engine models two things explicitly: a
  <strong>term structure</strong> (shorter lease, higher cap) and a <strong>rate sensitivity</strong>
  (verified 10-year Treasury of 4.90% as the anchor, with a ±75bp band).</p>
</section>

<div class="kpis">
  <div class="kpi"><div class="kpi-label">Term premium, 3 → 9 years</div><div class="kpi-value">+{defs['term_premium_3_to_9_pct']}%</div><div class="kpi-note">Same NOI. The entire difference is remaining lease term.</div></div>
  <div class="kpi"><div class="kpi-label">Term premium, 3 → 5 years</div><div class="kpi-value">+{defs['term_premium_3_to_5_pct']}%</div><div class="kpi-note">Why even a five-year extension is worth negotiating hard for.</div></div>
  <div class="kpi"><div class="kpi-label">Round-trip sale friction</div><div class="kpi-value">{defs['sell_cost_pct_pre_ula']:.2f}%</div><div class="kpi-note">Brokerage and closing plus city/county transfer tax, before ULA.</div></div>
  <div class="kpi"><div class="kpi-label">Proposition 13 wedge over 9 years</div><div class="kpi-value">{defs['prop13_wedge_pct']}%</div><div class="kpi-note">Assessed value is capped at +2%/yr while the model assumes +3% market growth.</div></div>
</div>

<h2>The cap-rate term structure (assumption, stated as such)</h2>
<p>No government series publishes net-lease cap rates. Rather than assert a market cap rate, the engine builds
one from the verified 10-year Treasury plus a stated spread, and applies it by remaining term.</p>
<div class="table-wrap"><table>
<thead><tr><th>Remaining lease term</th><th class="num">Cap rate</th><th class="num">Spread over the 4.90% 10-year</th></tr></thead>
<tbody>{cap_rows}</tbody></table></div>

<h2>What one extra year of term is worth</h2>
<p>Per $100,000 of net operating income, at the interpolated cap rate:</p>
<div class="table-wrap"><table>
<thead><tr><th class="num">Years of term</th><th class="num">Cap rate</th><th class="num">Value per $100k NOI</th><th class="num">vs. 3-year term</th></tr></thead>
<tbody>{term_rows}</tbody></table></div>

<h2>Strategy comparison</h2>
<p>Illustrative NOI case of <strong>$180,000</strong> — the middle of the three cases. <em>These are model
outputs on assumed inputs, not market facts.</em> The NPV column measures each strategy against selling today
at a 7.40% required return; the wealth column reinvests every dollar received at the verified 4.90% Treasury
yield until 2035.</p>
{strat_tables}

<h2>NPV across every NOI and expiry case</h2>
<div class="table-wrap"><table>
<thead><tr><th class="num">NOI</th><th class="num">Expiry</th><th class="num">A sell now</th><th class="num">B hold, tenant leaves</th>
<th class="num">C wait and renew</th><th class="num">D extend, sell 2028</th><th class="num">E extend, sell 2031</th></tr></thead>
<tbody>{npv_rows}</tbody></table></div>
<p class="small">Positive = better than selling today. Note that C is the highest or near-highest in every
case and E is the only strategy that is positive in <em>all</em> of them — which is precisely why the
recommendation is E rather than C: C's number assumes the renewal happens.</p>

<h2>How much of this answer is just a rates call?</h2>
<p>Selling today, at the $180,000 NOI and a 2032 expiry, against a shift in the cap rate:</p>
<div class="table-wrap"><table>
<thead><tr><th class="num">Cap shift</th><th class="num">Cap rate</th><th class="num">Gross value</th><th class="num">Net proceeds</th><th>Measure ULA applies?</th></tr></thead>
<tbody>{sens_rows}</tbody></table></div>
<p class="small">A 75bp move at this size is worth roughly a year and a half of rent. That is why the
recommendation separates the <em>lease</em> decision (in your control) from the <em>rate</em> decision
(not in your control).</p>

<h2>Every assumption in the engine</h2>
<p>If you disagree with the model, this is where to find it. Property-specific inputs were not supplied,
so they are assumptions with a stated basis, not data.</p>
<div class="table-wrap"><table>
<thead><tr><th>Key</th><th>Assumption</th><th>Value</th><th>Basis</th></tr></thead>
<tbody>{assumptions_rows}</tbody></table></div>

<h2>Run it yourself</h2>
<p>Enter your own NOI, cap rate and remaining term. Nothing leaves your browser — the calculation is
JavaScript in this page, and the page makes no network requests at all.</p>
<div class="panel calc">
  <label>Net operating income ($) <input id="c-noi" type="number" value="180000" step="5000"></label>
  <label>Cap rate (%) <input id="c-cap" type="number" value="6.875" step="0.125"></label>
  <label>Years of lease term remaining <input id="c-term" type="number" value="4" step="1" min="0" max="20"></label>
  <label>Sale price ($, optional — for the ULA check) <input id="c-price" type="number" value="" placeholder="auto"></label>
  <div class="calc-out" id="c-out">—</div>
</div>
<script>
(function() {{
  var ULA_LOW = {defs['ula_threshold']}, ULA_HIGH = 10900000;
  function money(n) {{ return (n < 0 ? "($" : "$") + Math.abs(Math.round(n)).toLocaleString() + (n < 0 ? ")" : ""); }}
  function capForTerm(t) {{
    var k = [[0,0.0725],[3,0.0725],[5,0.0650],[9,0.0600],[15,0.0590]];
    if (t <= 0) return k[0][1];
    for (var i = 0; i < k.length - 1; i++) {{
      if (t >= k[i][0] && t <= k[i+1][0]) {{
        var f = (t - k[i][0]) / (k[i+1][0] - k[i][0]);
        return k[i][1] + (k[i+1][1] - k[i][1]) * f;
      }}
    }}
    return k[k.length-1][1];
  }}
  var noi = document.getElementById("c-noi"),
      cap = document.getElementById("c-cap"),
      term = document.getElementById("c-term"),
      price = document.getElementById("c-price"),
      out = document.getElementById("c-out");
  function calc() {{
    var n = parseFloat(noi.value) || 0,
        c = (parseFloat(cap.value) || 0) / 100,
        t = parseFloat(term.value) || 1,
        mid = capForTerm(t);
    var v = c > 0 ? n / c : 0;
    var sugg = n / mid;
    var p = parseFloat(price.value) || v;
    var ula = p >= ULA_HIGH ? p * 0.055 : (p > ULA_LOW ? p * 0.04 : 0);
    var costs = p * 0.05 + p * 0.0056 + ula;
    out.innerHTML =
      "<div><span>Implied value at your cap rate</span><strong>" + money(v) + "</strong></div>" +
      "<div><span>Model cap rate for " + t + " years of term</span><strong>" + (mid*100).toFixed(2) + "%</strong></div>" +
      "<div><span>Implied value at the model's cap for that term</span><strong>" + money(sugg) + "</strong></div>" +
      "<div><span>Measure ULA on " + money(p) + "</span><strong>" + (ula ? money(ula) : "none") + "</strong></div>" +
      "<div><span>Total cost of sale (5% + 0.56% + ULA)</span><strong>" + money(costs) + "</strong></div>" +
      "<div><span>Net proceeds</span><strong>" + money(p - costs) + "</strong></div>";
  }}
  [noi, cap, term, price].forEach(function(el) {{ el.addEventListener("input", calc); }});
  calc();
}})();
</script>
"""
    page("valuation.html", "Valuation & projection", "A deterministic engine: cap rates as a function of lease term, anchored to a verified risk-free rate, with every assumption published.", body)


def build_decision():
    d = MODEL["decision"]
    names = {s["id"]: s["name"] for s in MODEL["scenarios"][0]["strategies"]}
    names["C"] = "Hold to expiry and renew then — probability-weighted"
    names["E"] = "Extend now on a long term, hold five years, sell with term intact"

    crit_head = "".join(f'<th class="num">{esc(c["name"])}<br><small>{int(c["weight"]*100)}%</small></th>' for c in d["criteria"])
    rows = ""
    for item in d["matrix"]:
        cells = "".join(f'<td class="num score s{item["scores"][c["key"]]}">{item["scores"][c["key"]]}</td>' for c in d["criteria"])
        rows += (f'<tr><td class="rank">{d["ranking"].index(item["id"])+1}</td>'
                 f'<td class="mono">{item["id"]}</td><td>{esc(names[item["id"]])}</td>{cells}'
                 f'<td class="num"><strong>{item["weighted_score"]:.2f}</strong></td></tr>')
    why = "".join(f'<div class="panel"><h3>{item["id"]} · {esc(names[item["id"]])}</h3><p>{esc(item["why"])}</p></div>' for item in d["matrix"])

    central = [sc for sc in MODEL["scenarios"] if sc["noi"] == 180000]
    e_npv = [st["npv"] for sc in central for st in sc["strategies"] if st["id"] == "E"]
    best = d["matrix"][0]

    body = f"""
<section class="hero">
  <p class="tag">Recommendation</p>
  <h2 class="hero-q">Extend now. Hold five years. Sell with term intact.</h2>
  <p class="hero-a">Strategy <strong>E</strong> wins the risk-weighted comparison
  ({best['weighted_score']:.2f} out of 5) and is the only strategy in the model with a
  <strong>positive NPV in every expiry case</strong> — {money(min(e_npv))} to {money(max(e_npv))} on the
  central NOI case. It resolves the tenant tail while you still have leverage, keeps the rent and the
  Proposition 13 wedge for five more years, and sells at the point where a buyer can underwrite five years
  of firm term instead of a hope.</p>
</section>

<h2>The decision, in four moves</h2>
<ol class="steps">
  <li><strong>Find the notice date before anything else.</strong> The owner has described a five-year expiry
  window. The lease has one date. Until that date — and the notice window that precedes it, typically 6 to 12
  months — is known, every other decision is provisional. This is the first action and it costs nothing.</li>
  <li><strong>Open the extension conversation now, not in 2030.</strong> The tenant's own filings show a
  system closing 50–60 units a year with "block closure" as policy. Your leverage peaks while the site is
  still one the operator wants. Target a long firm term (5 years minimum, 10 preferred) with CPI or 2%+
  escalators, and budget a concession — the model charges $150,000 for it.</li>
  <li><strong>If the extension is signed, hold about five years.</strong> Collect the rent, keep the Prop 13
  wedge (assessed value capped at +2% a year against ~3% assumed market growth, worth about
  {MODEL['derived']['prop13_wedge_pct']}% of the tax base over the period), and let the market reprice the asset.</li>
  <li><strong>Sell with about five years of firm term remaining.</strong> That is the deepest buyer pool: long
  enough to be underwritten as a net lease, short enough that the buyer is not paying for 2035 risk. Then
  decide whether to 1031, which must be arranged <em>before</em> closing.</li>
</ol>

<div class="callout danger">
<strong>The branch that matters.</strong> If the tenant will not extend, the answer changes completely:
<strong>sell within twelve months</strong>, while the lease still has years on it. Strategy B — do nothing and
let the lease run out — is the worst risk-adjusted outcome in the model and destroys value outright in two of
the three expiry cases. "No decision" is a decision here, and it is the expensive one.
</div>

<h2>Why not simply sell now?</h2>
<p>Selling now (strategy A) is not a bad outcome — it is the second-lowest-risk option and it deletes the
concentration problem in one transaction. It loses on two counts:</p>
<ul class="tight">
  <li><strong>It sells at the short-term cap.</strong> With nine years of term, the same NOI supports a
  materially higher price than with three. Selling now locks in whatever term the market can see today.</li>
  <li><strong>It triggers a one-way tax event.</strong> California's transfer taxes and federal capital-gains
  tax are payable, and the Proposition 13 base is destroyed — the assessed-value cap is a benefit that only
  exists while you hold. A 1031 exchange can defer the federal gain, but it must be set up before closing and
  completed inside the IRS's 45/180-day windows.</li>
</ul>
<p>Selling now <em>is</em> the right answer if you need liquidity, if you want out of a single-tenant risk
entirely, or if the tenant refuses to extend. It is the wrong answer if the only reason is that the lease
expiry is approaching.</p>

<h2>The scoring</h2>
<div class="table-wrap"><table class="matrix">
<thead><tr><th>#</th><th>ID</th><th>Strategy</th>{crit_head}<th class="num">Weighted</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="small">{esc(d['note'])}</p>

<h2>The reasoning behind each score</h2>
{why}

<h2>Risks that would change the recommendation</h2>
<ul class="tight">
  <li><strong>The tenant refuses to extend</strong> → switch to A (sell within twelve months). Do not drift into B.</li>
  <li><strong>The 10-year Treasury falls materially</strong> → cap rates compress, the asset re-rates upward, and holding becomes more attractive (C becomes dominant). The reverse is also true: a 75bp rise costs roughly a year and a half of rent.</li>
  <li><strong>A catastrophe event</strong> → see <a href="risks.html">Risks</a>. Wildfire does not have to reach the parcel to reprice the insurance and the buyer pool across the whole metro.</li>
  <li><strong>A better use for the capital</strong> → a 1031 into diversified net-lease assets converts one tenant's credit into many, which is the cheapest reduction in concentration risk available to you.</li>
  <li><strong>The expiry turns out to be 2035</strong> → the urgency falls but the reasoning does not: you still want the extension signed while you have leverage, and E is still positive in that case ({money([st['npv'] for sc in central if sc['expiry']==2035 for st in sc['strategies'] if st['id']=='E'][0])}).</li>
</ul>
"""
    page("decision.html", "Decision", "The recommendation, the four moves that implement it, the branch where it flips, and the reasoning behind every score.", body)


def build_risks():
    cat_facts = cat_rows("cat")
    industry = [r for r in FACTS["rows"] if r["status"] == "industry"]

    register = [
        ("Tenant non-renewal", "High", "High",
         "The franchisor is closing 50–60 units a year, mostly franchisee units, and names block closure and real-estate sales in its turnaround.",
         "Negotiate the extension now; if refused, sell inside twelve months.",
         "F071, F078, F063"),
        ("Lease tail / pricing cliff", "High", "High",
         "A buyer prices remaining term. The same NOI is worth roughly a fifth less with three years left than with nine.",
         "Never market the asset with a short tail. Extend first.",
         "F001"),
        ("Interest-rate shock", "Medium", "High",
         "The verified 10-year sits at 4.90% against a 3.75–4.00% funds rate — a steep curve. Cap rates set value, and a 75bp move is worth about 18 months of rent at this size.",
         "Model a ±75bp band before transacting; prefer a sale window you choose over one forced by expiry.",
         "F001, F002, F003"),
        ("Insurance repricing", "High", "Medium",
         "The FAIR Plan's commercial book grew from 7,315 to 21,717 policies since 2022, with $724B of total exposure. In a true NNN the tenant absorbs the premium — which protects income but raises the tenant's occupancy cost and its incentive to leave.",
         "Confirm who insures and who pays. If the owner pays, this is a direct NOI risk.",
         "F096, F098, F100"),
        ("Wildfire (indirect)", "Medium", "High",
         "Central Los Angeles is not wildland-urban interface, but the January 2025 fires repriced insurance and buyer sentiment across the whole metro. The FAIR Plan paid about $3.5B on roughly 5,400 claims.",
         "Parcel-level FHSZ cannot be determined without the address — flagged, not assumed. Treat metro-wide repricing as the live exposure.",
         "F094, F100, F093"),
        ("Earthquake", "Low", "Very high",
         "The Los Angeles basin is seismically active. USGS maintains the 2023 National Seismic Hazard Model; site class and liquefaction cannot be determined without the parcel.",
         "Get a seismic and insurance review before transacting; a single-storey drive-thru box is a favourable structure but not a favourable location.",
         "F101, F112"),
        ("Measure ULA at the threshold", "Low", "Medium",
         "A sale at $5,399,000 pays nothing; $5,400,001 pays about $216,000, because the rate applies to the whole price. Only bites if the asset is worth more than $5.4M.",
         "If the value is near the line, price the transaction with the cliff in view — but never structure falsely around it.",
         "F081, F083"),
        ("Tax on exit", "Certain", "Medium",
         "Transfer taxes of about 0.56% plus brokerage and closing of about 5.0% are unavoidable. Capital-gains tax depends on a basis that is private; a 1031 defers but does not eliminate it.",
         "Plan the 1031 before closing: 45 days to identify, 180 to complete, and the proceeds cannot touch your hands.",
         "F084, F085, F088"),
        ("Concentration", "High", "High",
         "One parcel, one tenant, one sub-market, one metro. For an individual preserving wealth, this is usually the largest unmanaged risk in the file — larger than any single market variable.",
         "The cheapest fix is a 1031 into diversified net-lease assets at exit.",
         "F105, F107"),
        ("Policy / regulatory", "Medium", "Medium",
         "The fast-food wage floor is statutorily ratcheted (currently $20.00/hr, above the $16.90 state rate) and the council can raise it again. Local transfer taxes are indexed upward annually.",
         "Model the wage floor into renewal rent expectations rather than resisting it.",
         "F026, F027, F028"),
    ]
    reg_rows = ""
    for name, lik, sev, what, act, refs in register:
        chips = chips_for_facts(refs.split(", "))
        reg_rows += (f'<tr><td><strong>{esc(name)}</strong></td><td><span class="pill l-{lik.lower().replace(" ","")}">{esc(lik)}</span></td>'
                     f'<td><span class="pill s-{sev.lower().replace(" ","")}">{esc(sev)}</span></td>'
                     f'<td>{esc(what)}</td><td>{esc(act)}</td><td>{chips}</td></tr>')

    body = f"""
<section class="hero compact">
  <p class="tag">Risk register</p>
  <h2 class="hero-q">What can go wrong, how bad it is, and what to do about it.</h2>
  <p class="hero-a">Likelihood and severity are analyst judgements, stated openly — official statistics do not
  publish the probability that a specific franchisee walks away from a specific lease. What <em>is</em>
  verifiable, and is therefore cited, is the evidence underneath each judgement.</p>
</section>

<h2>Business-as-usual risks</h2>
<div class="table-wrap"><table>
<thead><tr><th>Risk</th><th>Likelihood</th><th>Severity</th><th>Why it is on the list</th><th>Management</th><th>Sources</th></tr></thead>
<tbody>{reg_rows}</tbody></table></div>

<h2>Black-swan events</h2>
<p>The brief asks specifically about events that could destroy the local economy. The honest treatment is to
separate <em>severity</em>, which can be reasoned about, from <em>probability</em>, which official data does not
support at parcel level. Nothing below assigns a fabricated probability.</p>

<div class="cards">
  <article class="card warn"><h3>Wildfire</h3>
  <p>Structure: a single-storey drive-thru box, low fuel load, urban block — materially lower direct fire risk
  than a hillside asset. The real exposure is <em>indirect</em>: insurance repricing, buyer sentiment, and
  evacuation-level disruption to a trade area. The January 2025 fires cost the FAIR Plan alone about
  $3.5 billion across roughly 5,400 claims.</p>
  <p><strong>Severity:</strong> high, metro-wide. <strong>Parcel-level hazard:</strong> cannot be determined
  without the address — flagged, not assumed.</p></article>

  <article class="card warn"><h3>Earthquake</h3>
  <p>The LA basin sits over blind-thrust faults. A single-storey wood-and-steel box is one of the more
  survivable structures, but business interruption is not: an unsafe-to-occupy placard can stop the restaurant
  for months regardless of physical damage.</p>
  <p><strong>Severity:</strong> very high. <strong>Mitigation:</strong> confirm the lease allocates seismic
  risk, and confirm insurance actually covers business interruption for the tenant.</p></article>

  <article class="card warn"><h3>Insurance-market failure</h3>
  <p>The FAIR Plan now carries $724 billion of exposure and 21,717 commercial policies, with statutory rights
  to assess admitted insurers when claims outrun its capacity. If the residual market is the only market, the
  cost of cover becomes a tax on occupancy — and a tenant facing that tax is a tenant that recalculates rent.</p>
  <p><strong>Severity:</strong> high. <strong>Signal to watch:</strong> who carries the policy at renewal, and
  whether the premium is inside the tenant's controllable-cost cap.</p></article>

  <article class="card warn"><h3>Tenant insolvency</h3>
  <p>A franchisee bankruptcy can reject a lease in a way a corporate tenant's would not, and the brand's own
  disclosure names rising bad debt. In that scenario the landlord becomes an unsecured creditor for
  pre-petition rent.</p>
  <p><strong>Severity:</strong> high. <strong>Mitigation:</strong> know who the tenant of record is, and
  whether there is a guaranty. Both are withheld in this file — see flagged items.</p></article>

  <article class="card warn"><h3>Rate shock</h3>
  <p>Not rare, just slow. The verified 10-year at 4.90% against a 3.75–4.00% policy rate is already the
  post-2022 regime. A further 100bp would take the short-term cap materially above 8%, which is a
  double-digit percentage hit to value.</p>
  <p><strong>Severity:</strong> high. <strong>Mitigation:</strong> sell into a market you chose, on a
  timetable you set — not at a forced expiry.</p></article>

  <article class="card warn"><h3>Regulatory shock</h3>
  <p>Local transfer taxes are indexed upward annually by statute, and the state wage floor ratchets with
  CPI-W. A future expansion of Measure ULA, or commercial rent regulation, would reprice exit economics
  overnight.</p>
  <p><strong>Severity:</strong> medium. <strong>Note:</strong> the ULA threshold is now $5.4M and rises with
  the Chained CPI — a sale above it pays 4% of the <em>whole</em> price.</p></article>
</div>

<h2>The catastrophe and insurance data behind this page</h2>
{fact_table(cat_facts)}

<h2>Industry data — clearly separated</h2>
<p>Nothing in this table is government data, so it is kept apart from the verified tables rather than mixed
in. Currently nothing has been admitted here: cap-rate comparables and retail rent surveys were considered
and rejected as unverifiable at parcel level, so the model uses stated spread assumptions instead.</p>
{"<p class='small'>No industry rows are published.</p>" if not industry else fact_table(industry)}
"""
    page("risks.html", "Risks", "A register of the ordinary risks and the tail risks, with the evidence under each one — and no invented probabilities.", body)


def build_sources():
    rows = ""
    for s in SOURCES["sources"]:
        rows += (f'<tr id="{s["id"]}"><td class="mono">{s["id"]}</td>'
                 f'<td><a href="{esc(s["url"])}" rel="noopener noreferrer nofollow" target="_blank">{esc(s["title"])}</a>'
                 f'<div class="note">{esc(s["note"])}</div></td>'
                 f'<td>{esc(s["publisher"])}</td><td><span class="badge {"verified" if s["type"] in ("gov","sec") else "industry"}">{esc(s["type"])}</span></td>'
                 f'<td class="nowrap">{esc(s["as_of"])}</td>'
                 f'<td class="nowrap">{esc(ACCESSED)}</td></tr>')

    counts = {}
    for r in FACTS["rows"]:
        counts[r["cat"]] = counts.get(r["cat"], 0) + 1

    body = f"""
<section class="hero compact">
  <p class="tag">Source ledger</p>
  <h2 class="hero-q">Every source in this file, and the date it was read.</h2>
  <p class="hero-a">Each of these pages was opened and read on <strong>{ACCESSED}</strong>. Where a page's own
  data carried a different as-of date, that date is shown separately. Nothing is cited from memory and nothing
  is cited from a summary of a summary.</p>
</section>

<div class="table-wrap"><table>
<thead><tr><th>ID</th><th>Source</th><th>Publisher</th><th>Type</th><th>Data as of</th><th>Accessed</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<h2>How to check any number on this site</h2>
<ol class="steps">
  <li>Find the fact ID on any table — for example <span class="mono">F001</span>.</li>
  <li>Follow the source chip next to it (for example <a class="src" href="sources.html#S02">S02</a>).</li>
  <li>Open the publisher's page and compare the figures. The note under each source records exactly what was seen, including any qualifying language on the page.</li>
  <li>If a number cannot be reproduced from that page, treat it as an error in this file and flag it.</li>
</ol>

<h2>Deliberate exclusions</h2>
<ul class="tight">
  <li><strong>No broker listings or market reports</strong> are used as evidence. A listing is an asking price by an interested party, not a verified transaction, and no official series publishes net-lease cap rates or sub-market retail rents.</li>
  <li><strong>No data aggregators</strong> are cited for anything a primary source covers. Where aggregators disagreed with each other by more than 20% (school enrolment), the primary federal source was used instead.</li>
  <li><strong>No projections from private forecasters</strong> are presented as data. The projection on this site is a transparent deterministic model, not a purchased forecast.</li>
</ul>
"""
    page("sources.html", "Sources", "The full ledger of 22 sources, what each one was used for, and how to reproduce every figure.", body)


def build_flagged():
    rows = [r for r in FACTS["rows"] if r["status"] == "unverified"]
    irregularities = [
        ("The exact lease expiry date was not supplied",
         "The owner described the expiry as falling somewhere in 2030–2035. That is a five-year window, and a lease has one date. Because the remaining term drives the cap rate — and therefore the value — the model runs all three cases rather than picking one.",
         "Lease document. Nothing else resolves this."),
        ("Rent, NOI, and the escalation clause were not supplied",
         "Every dollar figure in the model is therefore an illustrative band, not the property's numbers. The engine is correct; the inputs are placeholders.",
         "The lease and the last three years of operating statements."),
        ("The tenant of record is unknown",
         "Corporate-operated unit and franchisee unit are different credits and different risks — the franchisor's own disclosure says most planned closures will be franchise units. The analysis flags this rather than assuming.",
         "The lease, or a call to the franchisor's real-estate group."),
        ("Whether the lease is truly triple-net was not supplied",
         "It determines whether insurance premium inflation and capital items hit the owner's income or the tenant's occupancy cost. The treatment of insurance is the difference between being hedged against the state's insurance crisis and being exposed to it.",
         "The lease, specifically the insurance, repairs and capital-replacement clauses."),
        ("Parcel-level hazard data could not be retrieved",
         "Fire Hazard Severity Zone, FEMA flood zone, seismic site class and Alquist-Priolo status all require the address. CAL FIRE's own page states that Local Responsibility Area determinations come from the local jurisdiction. The California Geological Survey Alquist-Priolo page returned a 404 on the access date.",
         "The address, then an FHSZ lookup with the City of Los Angeles plus a parcel hazard report."),
        ("The California Department of Education enrolment endpoint returned an error",
         "DataQuest's district enrolment page returned a generic error on every attempt. Federal NCES figures are used instead. Third-party aggregators disagreed by more than 20% for the same year, so none of them was used.",
         "Re-run the DataQuest query, or use the CDE downloadable data files."),
        ("The IRS Section 1031 source is an archival page",
         "The IRS marks FS-2008-18 as archival and points to a newer 'Real Estate Tax Tips' page. The 45-day and 180-day mechanics quoted here are from the archival sheet. They are long-standing law, but this is flagged rather than asserted as current.",
         "The owner's CPA, and the IRS's current page, before any exchange is executed."),
        ("Whether the $20.00 fast-food minimum wage changed during 2026 is unconfirmed",
         "The DIR FAQ still states $20.00 on the access date and no Fast Food Council determination raising it was found on a DIR page. Several non-official sites say there was no change in 2026 — that is not an official confirmation, so it is published as unverified rather than asserted.",
         "The DIR Fast Food Council page or a DIR news release."),
        ("Cap rates and retail rents have no official source",
         "No government series publishes net-lease cap rates or sub-market retail asking rents. Rather than launder a broker estimate into the analysis, the model builds its cap rates from the verified risk-free rate plus a stated spread, and shows a sensitivity band.",
         "Comparable transaction evidence, ideally from an appraiser with access to recorded sales."),
        ("Two LA County Assessor pages redirected to the homepage",
         "The Assessor's Proposition 13 and Proposition 19 URLs both served the homepage rather than the requested page, so no assessor statement is cited. Proposition 13's 2% cap is instead verified against the California Constitution itself.",
         "Direct navigation on assessor.lacounty.gov at the time of the transaction."),
        ("Share of JACK restaurants in California was not extracted",
         "Item 1 of the FY2025 Form 10-K would contain it. The 10-K is a 53-chunk document and the specific passage was not reached in this pass, so the figure is left blank rather than inferred.",
         "Item 1 of the FY2025 Form 10-K, or the franchise disclosure document."),
    ]
    irr_html = "".join(
        f'<div class="panel"><h3>{esc(t)}</h3><p>{esc(b)}</p><p class="small"><strong>To resolve:</strong> {esc(c)}</p></div>'
        for t, b, c in irregularities)

    body = f"""
<section class="hero compact warn">
  <p class="tag">Flagged for review</p>
  <h2 class="hero-q">Everything that could not be verified, published instead of guessed.</h2>
  <p class="hero-a">This page exists because the alternative — quietly filling gaps with plausible numbers — is
  how bad decisions get made. {len(rows)} data rows are blank and flagged, and {len(irregularities)} further
  irregularities are documented below. None of them blocks the analysis; all of them bound it.</p>
</section>

<h2>Blank rows</h2>
<p>Each value was left empty rather than estimated. The note states what would be needed to fill it.</p>
{fact_table(rows)}

<h2>Irregularities found during the work</h2>
{irr_html}

<h2>What this means for the recommendation</h2>
<div class="callout">
<p>The <em>structure</em> of the answer does not depend on any of the missing items: term drives price, the
tenant is contracting, and holding passively into an expiry is the worst risk-adjusted path. Those conclusions
follow from official data that is verified and linked.</p>
<p>The <em>arithmetic</em> does depend on them. The dollar figures on this site are model output on assumed
inputs. Substitute your actual NOI, cap rate and remaining term into the calculator on the
<a href="valuation.html">Valuation</a> page and the same engine produces your numbers — but treat the
~$0.5M-scale NPV gaps between strategies as illustrative until the lease has been read.</p>
</div>
"""
    page("flagged.html", "Flagged for review", "The gaps, the errors encountered, and the judgement calls — documented so they can be challenged.", body)


def main():
    os.makedirs(os.path.join(SITE, "data"), exist_ok=True)
    build_index()
    build_property()
    build_market()
    build_tenant()
    build_valuation()
    build_decision()
    build_risks()
    build_sources()
    build_flagged()
    # ship a machine-readable copy so anyone can re-run the analysis
    for name in ("facts.json", "sources.json", "assumptions.json", "model.json"):
        shutil.copy(os.path.join(DATA, name), os.path.join(SITE, "data", name))
    print(f"built {len(NAV)} pages at {SITE}")


if __name__ == "__main__":
    main()
