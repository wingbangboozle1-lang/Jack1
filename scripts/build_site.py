#!/usr/bin/env python3
"""Build the static decision-brief site from scripts/site_data.py.

Deterministic: running this script rewrites every HTML page and the CSS
from the same verified dataset.  No runtime data fetching, no third-party
scripts, no analytics, no cookies.
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from site_data import ACCESSION_DATE, ROWS, SOURCES, STATUS_LABEL, rows_for  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SHORT = {
    "CEN-CITY": "Census Bureau",
    "CEN-COUNTY": "Census Bureau",
    "BLS-EAG": "BLS",
    "BLS-CPI": "BLS",
    "FRED-DGS10": "Federal Reserve / FRED",
    "FRED-GDP-METRO": "BEA via FRED",
    "FRED-GDP-COUNTY": "BEA via FRED",
    "USGS-UCERF3": "USGS",
    "SEC-Q4": "SEC EDGAR",
    "LA-ULA": "LA Office of Finance",
    "LACO-ASSESSOR": "LA County Assessor",
    "LACO-ASSESSOR-HOME": "LA County Assessor",
    "DIR-FF": "CA Dept. of Industrial Relations",
    "CALFIRE-PAL": "CAL FIRE",
    "OSFM-FHSZ": "CAL FIRE / State Fire Marshal",
    "CGS-AP": "CA Geological Survey",
    "USGS-SHAKEOUT": "USGS",
    "NCES-LAUSD": "NCES (U.S. Dept. of Education)",
    "IRS-1031": "IRS",
    "DOF-PROJ": "CA Dept. of Finance",
    "LA-ZIMAS": "LA City Planning (ZIMAS)",
    "CSC-DASH": "CA School Dashboard",
}

NAV = [
    ("Overview", [("index.html", "Executive summary")]),
    ("Area economy", [
        ("demographics.html", "Population &amp; income"),
        ("economy.html", "Jobs &amp; prices"),
        ("schools.html", "Schools"),
    ]),
    ("Asset &amp; tenant", [
        ("property.html", "Lease &amp; property"),
        ("tenant.html", "Tenant credit"),
    ]),
    ("Analysis", [
        ("model.html", "Projection model"),
        ("decision.html", "Sell vs renew"),
        ("risks.html", "Risk register"),
    ]),
    ("Verification", [
        ("flagged.html", "Flagged for review"),
        ("sources.html", "Sources &amp; method"),
    ]),
]

PAGE_ORDER = [slug for _, items in NAV for slug, _ in items]

# --------------------------------------------------------------------------
# Model (transparent arithmetic; assumptions are labelled as assumptions)
# --------------------------------------------------------------------------

NOI_SCENARIOS = [150_000, 200_000, 250_000, 300_000]
CAP_RATES = [0.0525, 0.0575, 0.0625, 0.0675, 0.0725]
RENT_GROWTH = 0.025          # assumption
DISCOUNT_RATE = 0.075        # assumption
SALE_OTHER_COSTS = 0.020     # assumption: brokerage, legal, escrow
HOLD_YEARS = 5

ULA_LOW = 5_400_000
ULA_HIGH = 10_900_000
BASE_TRANSFER = 0.0045


def ula_rate(price):
    if price >= ULA_HIGH:
        return 0.055
    if price > ULA_LOW:
        return 0.04
    return 0.0


def city_transfer_tax(price):
    return BASE_TRANSFER * price + ula_rate(price) * price


def sale_friction(price):
    """City transfer tax plus assumed brokerage / legal / escrow."""
    return city_transfer_tax(price) + SALE_OTHER_COSTS * price


def net_sale_proceeds(price):
    return price - sale_friction(price)


def direct_cap_value(noi, cap):
    return noi / cap


def npv_hold(noi, c0, c5, g=RENT_GROWTH, d=DISCOUNT_RATE, years=HOLD_YEARS):
    total = 0.0
    for t in range(1, years + 1):
        total += noi * (1 + g) ** t / (1 + d) ** t
    terminal = noi * (1 + g) ** years / c5
    total += net_sale_proceeds(terminal) / (1 + d) ** years
    return total


def breakeven_exit_cap(noi, c0, g=RENT_GROWTH, d=DISCOUNT_RATE, years=HOLD_YEARS):
    """Exit cap rate at which holding equals selling today (NPV basis)."""
    target = net_sale_proceeds(direct_cap_value(noi, c0))
    lo, hi = 0.03, 0.30
    for _ in range(200):
        mid = (lo + hi) / 2
        if npv_hold(noi, c0, mid, g, d, years) > target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def money(x):
    if x >= 1_000_000:
        return f"${x/1_000_000:,.2f}M"
    return f"${x:,.0f}"


def pct(x, places=2):
    return f"{x*100:.{places}f}%"


# population / employment trend continuation
COUNTY_POP_2025 = 9_694_934
COUNTY_POP_G = (1 - 0.032) ** (1 / 5.25) - 1
CITY_POP_2025 = 3_869_089
CITY_POP_G = (1 - 0.008) ** (1 / 5.25) - 1
MSA_EMP_2026 = 6_282.1  # thousands
MSA_EMP_G = 0.005


def trend_rows():
    out = []
    for year in (2026, 2030, 2035):
        pop = COUNTY_POP_2025 * (1 + COUNTY_POP_G) ** (year - 2025)
        emp = MSA_EMP_2026 * (1 + MSA_EMP_G) ** (year - 2026)
        out.append((str(year), f"{pop:,.0f}", f"{emp:,.1f} thousand"))
    return out


# --------------------------------------------------------------------------
# HTML helpers
# --------------------------------------------------------------------------

def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                if "&" not in text else text) if False else text


def badge(status):
    return f'<span class="badge badge-{status}">{STATUS_LABEL[status]}</span>'


def source_link(src_id):
    s = SOURCES[src_id]
    label = SHORT.get(src_id, s["publisher"])
    return (f'<a href="{s["url"]}" target="_blank" rel="noopener noreferrer" '
            f'title="{s["publisher"]} - {s["title"]}">{label}<span class="ext" aria-hidden="true">&#8599;</span></a>')


def table(rows, columns=("metric", "value", "period", "status", "source"), caption=""):
    head = {
        "metric": "Indicator",
        "value": "Value",
        "period": "Period / geography",
        "status": "Status",
        "source": "Official source",
        "note": "Verification note",
    }
    parts = ['<div class="table-wrap">', '<table class="data-table">']
    parts.append("<thead><tr>" + "".join(f'<th scope="col">{head[c]}</th>' for c in columns) + "</tr></thead><tbody>")
    for r in rows:
        cells = []
        for c in columns:
            if c == "metric":
                note = f'<span class="row-note">{r["note"]}</span>' if r["note"] else ""
                cells.append(f'<td class="cell-metric">{r["metric"]}{note}</td>')
            elif c == "value":
                if r["value"]:
                    cells.append(f'<td class="cell-value">{r["value"]}</td>')
                else:
                    flag = "Not published - withheld for privacy" if r["status"] == "withheld" else "Not published - unverified"
                    cells.append(f'<td class="cell-value cell-empty">{flag}</td>')
            elif c == "period":
                cells.append(f'<td>{r["period"]}<span class="row-note">{r["geo"]}</span></td>')
            elif c == "status":
                cells.append(f'<td>{badge(r["status"])}</td>')
            elif c == "source":
                cells.append(f'<td class="cell-source">{source_link(r["src"])}</td>')
            elif c == "note":
                cells.append(f'<td>{r["note"]}</td>')
        parts.append("<tr>" + "".join(cells) + "</tr>")
    parts.append("</tbody></table></div>")
    if caption:
        return caption + "".join(parts)
    return "".join(parts)


def simple_table(headers, rows, caption="", foot=None, cls=""):
    """Render a table.

    cls="calc" marks a table of computed or comparative values rather than
    sourced observations.  Such a table carries its official basis in a
    footer row of links; every other table must link a source in every row.
    """
    klass = "data-table calc" if cls == "calc" else "data-table"
    out = ['<div class="table-wrap">', f'<table class="{klass}">']
    out.append("<thead><tr>" + "".join(f'<th scope="col">{h}</th>' for h in headers) + "</tr></thead><tbody>")
    for row in rows:
        out.append("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>")
    out.append("</tbody>")
    if foot:
        out.append(f'<tfoot><tr><td colspan="{len(headers)}">{foot}</td></tr></tfoot>')
    out.append("</table></div>")
    return (caption or "") + "".join(out)


def nav_html(current):
    out = []
    n = 0
    for group, items in NAV:
        out.append(f'<p class="nav-label">{group}</p><nav class="site-nav">')
        for slug, label in items:
            n += 1
            cur = ' aria-current="page"' if slug == current else ""
            out.append(f'<a href="{slug}"{cur}><span class="nav-dot">{n:02d}</span>{label}</a>')
        out.append("</nav>")
    return "".join(out)


TITLES = {
    "index.html": ("Executive summary", "Decision support / Executive summary"),
    "demographics.html": ("Population &amp; income", "Area economy / Population &amp; income"),
    "economy.html": ("Jobs &amp; prices", "Area economy / Jobs &amp; prices"),
    "schools.html": ("Schools", "Area economy / Schools"),
    "property.html": ("Lease &amp; property", "Asset &amp; tenant / Lease &amp; property"),
    "tenant.html": ("Tenant credit", "Asset &amp; tenant / Tenant credit"),
    "model.html": ("Projection model", "Analysis / Projection model"),
    "decision.html": ("Sell vs renew", "Analysis / Sell vs renew"),
    "risks.html": ("Risk register", "Analysis / Risk register"),
    "flagged.html": ("Flagged for review", "Verification / Flagged for review"),
    "sources.html": ("Sources &amp; method", "Verification / Sources &amp; method"),
}


def shell(slug, page_title, body):
    doc_title, crumb = TITLES[slug]
    nav = nav_html(slug)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Source-linked decision brief for a Jack in the Box triple-net property described as being near central Los Angeles. No owner or property identifiers are published.">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="robots" content="index, follow">
<title>{doc_title} | Jack in the Box Property Brief</title>
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<a class="skip-link" href="#main-content">Skip to content</a>
<div class="app-shell">
  <aside class="sidebar" id="site-nav" aria-label="Main navigation">
    <a class="brand" href="index.html" aria-label="Decision brief home">
      <span class="brand-mark" aria-hidden="true">JB</span>
      <span class="brand-copy"><strong>Property decision brief</strong><span>Central Los Angeles &middot; public-data review</span></span>
    </a>
    <p class="nav-label">Research dashboard</p>
    {nav}
    <div class="sidebar-note"><strong>Privacy-first publication</strong>No owner name, street address, parcel number, lease document or personal financial detail is published or collected by this site.</div>
  </aside>
  <div class="main-column">
    <header class="topbar">
      <div class="topbar-left">
        <button class="nav-toggle" type="button" data-nav-toggle aria-controls="site-nav" aria-expanded="false">Menu</button>
        <span class="crumb">{crumb}</span>
      </div>
      <div class="snapshot">Evidence collected {ACCESSION_DATE}</div>
    </header>
    <main id="main-content" class="content">
{body}
    </main>
    <footer class="site-footer">
      <p><strong>Privacy:</strong> aggregated public statistics only. No personal identifiers are stored in this repository or served by this site.</p>
      <p>Every table value links to the official page it was read from on {ACCESSION_DATE}. Blank cells are unverified or withheld by policy &mdash; they are listed on <a href="flagged.html">Flagged for review</a>. This is analysis for the owner, not appraisal, legal, tax or investment advice.</p>
    </footer>
  </div>
</div>
<script src="assets/site.js" defer></script>
</body>
</html>
"""


def hero(eyebrow, pill, h1, lede, actions=""):
    return f"""<section class="hero">
  <p class="eyebrow">{eyebrow}</p>
  <span class="status-pill">{pill}</span>
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
  <div class="hero-actions">{actions}</div>
</section>"""


def section(eyebrow, h2, body, after="", anchor=""):
    ident = f' id="{anchor}"' if anchor else ""
    return f"""<section class="section"{ident}>
  <div class="section-heading"><div><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2></div>{after}</div>
  {body}
</section>"""


def card_grid(cards):
    out = ['<div class="card-grid">']
    for label, value, meta, link in cards:
        out.append(f'<article class="metric-card"><div class="metric-label">{label}</div>'
                   f'<div class="metric-value">{value}</div><div class="metric-meta">{meta}</div>'
                   f'{link}</article>')
    return "".join(out) + "</div>"


def src_href(src_id):
    s = SOURCES[src_id]
    label = SHORT.get(src_id, s["publisher"])
    return f'<a class="metric-source" href="{s["url"]}" target="_blank" rel="noopener noreferrer">{label} &#8599;</a>'


def counts():
    c = {"verified": 0, "derived": 0, "unverified": 0, "withheld": 0}
    for r in ROWS:
        c[r["status"]] += 1
    c["total"] = len(ROWS)
    return c


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------

def page_index():
    c = counts()
    cards = card_grid([
        ("Unemployment rate - LA MSA", "4.4%", "September 2026, preliminary. Metropolitan area, not the parcel catchment.", src_href("BLS-EAG")),
        ("Median household income - city", "$81,939", "2020-2024 ACS, 2024 dollars. Citywide median, not a trade-area median.", src_href("CEN-CITY")),
        ("CPI-U 12-month change - LA area", "3.7%", "September 2026. Food away from home +2.8% - the tenant's pricing environment.", src_href("BLS-CPI")),
        ("10-year Treasury yield", "4.84%", "2026-11-05. Cost-of-capital context only - not a capitalisation rate.", src_href("FRED-DGS10")),
        ("Jack in the Box same-store sales", "-7.4%", "Fourth quarter fiscal 2025, systemwide. The credit behind the rent.", src_href("SEC-Q4")),
        ("City transfer tax at the ULA line", "$240,300", "On a $5,400,001 sale - versus $24,300 at $5,400,000.", src_href("LA-ULA")),
    ])

    body = hero(
        "Jack in the Box &middot; reported NNN lease &middot; central Los Angeles (approximate location)",
        "Recommendation: renew on market terms, hold, and sell only into a supported number",
        "Keep the income and the optionality; do not ride to expiry, and do not sell blind.",
        "Public data can describe Los Angeles at city, county and metropolitan scale, and it can describe the tenant's "
        "credit trend from its own SEC filings. It cannot describe this parcel. The recommendation below is therefore "
        "built so that every input you must supply is named, and every number that would change the answer is testable.",
        '<a class="button" href="decision.html">Read the decision <span aria-hidden="true">&rarr;</span></a>'
        '<a class="button button-secondary" href="model.html">Open the projection model</a>',
    )

    body += section("At a glance", "Six verified numbers that frame the decision", cards)

    body += section("The decision", "What the evidence supports", """
<ol class="findings">
  <li><strong>Renew rather than sell, on the evidence available.</strong> A triple-net lease with five to nine years
  remaining is the most valuable thing you own here: it converts tenant credit into contractual rent while you keep
  title. Selling converts that into cash at a price that depends on a capitalisation rate nobody has quoted you yet.</li>
  <li><strong>The tenant is the credit, and the credit is weakening - but not broken.</strong> Systemwide same-store
  sales fell 7.4% in the fourth quarter and 4.2% for fiscal 2025, 86 restaurants were closed, and the dividend was
  discontinued. Against that, franchise-level margin is guided at $275-290 million for fiscal 2026 and restaurant count
  is guided to 2,050-2,100. This is a "negotiate now, monitor quarterly" credit, not a "sell in a panic" credit.</li>
  <li><strong>The area economy is mild, not collapsing.</strong> Metropolitan employment grew 0.5% year over year while
  population fell -0.8% in the city and -3.2% in the county since 2020. Education and health services (+3.8%) is
  carrying growth; information (-5.7%) and financial activities (-1.7%) are shrinking.</li>
  <li><strong>Transaction friction is unusually high in this jurisdiction, with a cliff.</strong> Los Angeles adds a 4.0%
  Measure ULA surcharge on a sale above $5,400,000 and 5.5% at $10,900,000 or more, on top of a 0.45% base tax. One
  dollar above the threshold costs about $216,000 more in tax. That is a reason to price a sale carefully and to
  negotiate the timing, not a reason to avoid selling forever.</li>
  <li><strong>The black-swan exposures are real but unquantified for this site.</strong> The January 2025 Palisades fire
  destroyed 6,845 structures in this county; a modelled Mw 7.8 San Andreas event carries 1,800 deaths and $191 billion
  of regional economic loss. Neither is a probability for this parcel. Both are reasons to confirm insurance, lease
  allocation and resilience before you commit capital.</li>
</ol>""")

    body += section("Path comparison", "Three paths, scored on the evidence", simple_table(
        ["Path", "What it protects", "What it costs", "What the evidence says", "Risk level", "Verdict"],
        [
            ["<strong>A. Renew / extend, then hold</strong>",
             "Contractual NNN income, title, optionality to sell later with a longer term in place.",
             "Renewal rent may reset below today's rent; capital stays concentrated in one asset.",
             "Tenant credit is weakening but franchise margin guidance is positive; area employment is flat-to-positive.",
             '<span class="badge badge-verified">Moderate</span>',
             "<strong>Recommended first step.</strong> Negotiate now; do not wait for the option window."],
            ["<strong>B. Sell with the lease in place</strong>",
             "Liquidity, diversification, removal of single-tenant and single-asset risk.",
             "0.45% base transfer tax, 0-5.5% ULA, brokerage and legal costs, and loss of future rent.",
             "No verified capitalisation rate or price exists for this parcel, so the sale cannot be underwritten here.",
             '<span class="badge badge-unverified">High while unpriced</span>',
             "Do it when a bid implies a cap rate at or inside the break-even in the model, or when a trigger fires."],
            ["<strong>C. Hold to expiry, then re-tenant</strong>",
             "Full control of the real estate at expiry; possible re-use upside.",
             "Vacancy, downtime, tenant improvements, and a shorter lease at sale.",
             "Downtime and re-leasing cost are unverified for this site; the model shows the income gap this creates.",
             '<span class="badge badge-withheld">Highest</span>',
             "Not recommended as a plan. It is the default outcome if the renewal is not signed."],
        ], cls="calc", foot="Basis: " + source_link("SEC-Q4") + " &middot; " + source_link("LA-ULA") + " &middot; " + source_link("BLS-EAG") + " &middot; " + source_link("FRED-DGS10") + ". Risk levels are the brief's assessment, not a published rating."))

    tiles = []
    for label, slug, prefixes, blurb in [
        ("Population &amp; income", "demographics.html", ["DEM", "INC", "HOU"],
         "Population, households, income, poverty and housing at city and county scale."),
        ("Jobs &amp; prices", "economy.html", ["ECO", "PRI", "CAP"],
         "Employment, sector change, consumer prices and the cost of capital."),
        ("Schools", "schools.html", ["SCH"], "District size, staffing and spending from federal data."),
        ("Lease &amp; property", "property.html", ["PRP", "REG"],
         "The blank fields, the official lookups that fill them, and the transfer-tax rules."),
        ("Tenant credit", "tenant.html", ["TEN"], "Jack in the Box results and guidance from its own filings."),
        ("Projection model", "model.html", ["POP"], "Value grid, sale friction, hold-versus-sell and trend continuation."),
        ("Risk register", "risks.html", ["CAT"], "Hazards, operations, regulation and black-swan scenarios."),
        ("Flagged for review", "flagged.html", [], "Everything not verified, and why it is not published."),
    ]:
        n = len([r for r in ROWS if r["id"].split("-")[0] in prefixes]) if prefixes else counts()["unverified"] + counts()["withheld"]
        count_text = f"{n} rows" if prefixes else f"{n} items"
        tiles.append(f'<a class="tile" href="{slug}"><span class="tile-title">{label}</span>'
                     f'<span class="tile-blurb">{blurb}</span><span class="tile-count">{count_text}</span></a>')

    body += section("Browse by category", "Every dataset in this brief",
                    '<div class="tiles">' + "".join(tiles) + "</div>")

    body += section("Evidence status", "What is verified, what is not", f"""
<p class="prose">{c['total']} published rows: <strong>{c['verified']} verified</strong> against an official page opened on
{ACCESSION_DATE}, <strong>{c['derived']} derived</strong> by stated arithmetic, <strong>{c['unverified']} left blank</strong>
because no official source could confirm them, and <strong>{c['withheld']} withheld</strong> by the privacy policy.
A blank is never zero and never an estimate. The build script fails if a number appears in an unverified row.</p>
{simple_table(["Status", "Rows", "What it means", "Where to check"],
 [["Verified", str(c['verified']), "Read directly from a government or SEC page linked in the row.", '<a href="sources.html">Sources &amp; method</a>'],
  ["Derived", str(c['derived']), "Arithmetic on verified values; the formula is in the row note.", '<a href="model.html">Projection model</a>'],
  ["Unverified", str(c['unverified']), "No official source could confirm it; value left blank.", '<a href="flagged.html">Flagged for review</a>'],
  ["Withheld", str(c['withheld']), "Known to the owner but excluded by the privacy policy.", '<a href="flagged.html">Flagged for review</a>']],
  cls="calc", foot="Basis: row-level sources are on each dataset page and in " + source_link("CEN-CITY") + " plus the register on <a href='sources.html'>Sources &amp; method</a>.")}
""")

    body += section("Scope and privacy", "Public evidence only", """
<p class="prose">This site publishes aggregated public statistics and the official page each one came from. It contains no
owner name, street address, parcel number, ownership entity, lease document, rent figure, debt balance or personal
financial detail, and it collects nothing from visitors: no cookies, no analytics, no third-party scripts, no forms.
Asset-specific fields that cannot be checked from public data are blank and listed on
<a href="flagged.html">Flagged for review</a>, together with the official lookup that would close each one.</p>""")

    return shell("index.html", "Executive summary", body)


def page_demographics():
    body = hero(
        "Area economy &middot; population, income and housing",
        "Geography: city and county - never the parcel",
        "A declining county population with rising incomes and very high housing costs.",
        "Los Angeles County lost 3.2% of its population between the 2020 estimate base and July 2025, and the city lost 0.8%. "
        "Incomes and housing costs still rose. Both facts matter for a restaurant site: they describe the customer base and "
        "the labour pool, and they conflict, so neither can be used alone.",
        '<a class="button" href="economy.html">Jobs &amp; prices <span aria-hidden="true">&rarr;</span></a>',
    )

    body += section("Population", "Population, households and density",
        table(rows_for(["DEM"])) +
        """<p class="prose"><strong>Reading:</strong> the city is 3,869,089 people as of 1 July 2025, down 0.8% from the 2020
estimate base; the county is 9,694,934, down 3.2%. Annualised, that is -0.15% and -0.62% a year (derived rows DEM-05 and
DEM-06 show the arithmetic). Density is 8,304 people per square mile in the city, so a "central Los Angeles" store is
inside a very large, very dense market even while the aggregate shrinks slightly.</p>""")

    body += section("Income", "Income, poverty and education", table(rows_for(["INC"])) +
        """<p class="prose"><strong>Reading:</strong> the city median household income is $81,939 and the county median is
$90,112 in 2024 dollars; 16.5% of city residents are below the poverty line. A quick-service restaurant sits between those
two facts - it depends on household cash flow, not on median income alone. No verified source describes the income of the
households inside this site's actual trade area (DEM-17), and none is inferred.</p>""")

    body += section("Housing", "Housing cost, tenure and construction", table(rows_for(["HOU"])) +
        """<p class="prose"><strong>Reading:</strong> median gross rent is $1,933 a month in the city and $1,954 in the county,
with a 36.0% owner-occupied rate in the city. High housing cost absorbs household budget before discretionary food spend,
which is one mechanism behind the tenant's negative same-store sales. It also constrains hiring: the California fast-food
minimum wage is $20.00 an hour (see <a href="property.html#regulation">regulation</a>). County building permits of 22,250 in
2025 show construction is active, which supports construction employment but also spreads demand across new locations.</p>""")

    return shell("demographics.html", "Population &amp; income", body)


def page_economy():
    body = hero(
        "Area economy &middot; jobs, prices and cost of capital",
        "Metropolitan area figures - not a trade area",
        "Employment is flat-to-growing, the consumer price index is not, and money is not cheap.",
        "Total nonfarm employment in the Los Angeles-Long Beach-Santa Ana metropolitan area grew 0.5% over the twelve months "
        "to September 2026, with unemployment at 4.4%. Los Angeles area consumer prices rose 3.7% over the year. The ten-year "
        "Treasury yields 4.84%. Each number pushes the sell-versus-renew answer in a different direction.",
        '<a class="button" href="model.html">See how these feed the model <span aria-hidden="true">&rarr;</span></a>',
    )

    body += section("Labour market", "Employment and sector change", table(rows_for(["ECO"])) +
        """<p class="prose"><strong>Reading:</strong> the metro added roughly 31,000 nonfarm jobs over the year (0.5% of 6.28
million). The mix matters more than the total: education and health services added 3.8%, while information shed 5.7% and
financial activities 1.7%. A central Los Angeles quick-service site draws on office, health, education and visitor traffic,
so a shrinking information sector is a headwind for weekday lunch and a growing health sector is a partial offset. The
county's own unemployment rate is not published here because the BLS page read covers the metropolitan area (ECO-22).</p>""")

    body += section("Prices", "Consumer prices, Los Angeles area", table(rows_for(["PRI"])) +
        """<p class="prose"><strong>Reading:</strong> food away from home rose 2.8% over the year while all items rose 3.7% and
energy rose 20.3%. Restaurant menu prices are therefore rising more slowly than the household's overall basket, which
squeezes real margins at the same time as California's $20.00 fast-food wage floor pushes costs up. For a landlord, this is
the mechanism that turns into rent-coverage pressure at renewal.</p>""")

    body += section("Cost of capital", "Interest rates and capitalisation", table(rows_for(["CAP"])) +
        f"""<p class="prose"><strong>Reading:</strong> the ten-year Treasury closed at 4.84% on 2026-11-05 (CAP-01). Long-term
rates at that level keep pressure on net-lease pricing, because a buyer financed at a positive spread needs a higher
capitalisation rate to clear their cost of funds. No official source publishes a capitalisation rate for this asset, so
CAP-02 is blank and the model instead shows value across a range of rates you can test yourself.</p>""")

    body += section("Regional outlook", "Projections - what is official and what is mechanical",
        table(rows_for(["POP"])) +
        f"""<p class="prose">The California Department of Finance publishes official county projections (Baseline 2024,
P-2 series). They ship as an Excel workbook that could not be read in this environment, so those official figures are
deliberately <em>not</em> published (POP-01, POP-02). The two derived rows are mechanical continuations of verified recent
change, shown for scale only: county population on the 2020-2025 trend reaches about 9.40 million by 2030 and 9.11 million
by 2035, while metropolitan employment on its current 0.5% trend reaches about 6.41 million and 6.57 million. Neither is a
forecast and neither applies to the site.</p>""")

    return shell("economy.html", "Jobs &amp; prices", body)


def page_schools():
    body = hero(
        "Area economy &middot; schools",
        "District-level data only",
        "The district is enormous and adequately documented; the assigned school is not.",
        "Central Los Angeles is served by Los Angeles Unified, with 784 schools and 408,026 students. Federal data describes its scale, staffing and spending. It says nothing about the "
        "school assigned to this parcel, because that depends on an address the brief does not publish.",
        '<a class="button" href="demographics.html">Population &amp; income <span aria-hidden="true">&rarr;</span></a>',
    )
    body += section("District", "Los Angeles Unified - verified federal figures", table(rows_for(["SCH"])) +
        """<p class="prose"><strong>Reading:</strong> 408,026 students across 784 schools with 21,246 classroom teachers
implies a 19.20 student-to-teacher ratio, and current expenditure of $22,606 per student. Those figures describe the
district, not a neighbourhood. For a restaurant site the school system matters in two concrete ways: it is a large
public-sector employer (education and health services is the metro's fastest-growing sector at +3.8%), and it is a source of
family household demand. Neither effect can be sized without the parcel.</p>
<p class="prose">Academic performance is <strong>not</strong> published here: the California School Dashboard district report
was not opened in this session, so SCH-10 is left blank and flagged rather than filled from a secondary summary. Assignment
boundaries are address-specific (SCH-09).</p>""")
    return shell("schools.html", "Schools", body)


def page_property():
    body = hero(
        "Asset &amp; tenant &middot; lease and property",
        "Sixteen fields are blank on purpose",
        "The lease, not the logo, determines what this asset is worth.",
        "A Jack in the Box sign and the words \u201ctriple net\u201d do not establish the legal tenant, the guarantor, the rent, the "
        "landlord's obligations or the sale value. Each field below names the official record that would close it. Until then "
        "every property-level conclusion in this brief is conditional.",
        '<a class="button" href="tenant.html">Tenant credit <span aria-hidden="true">&rarr;</span></a>',
    )
    body += section("Asset facts", "Property and lease fields", table(rows_for(["PRP"])) +
        """<p class="prose"><strong>Reading:</strong> what is verified is only what the owner described: a triple-net lease with
an expiry window of 2030-2035 (PRP-05, PRP-10). Everything else - address, parcel, rent, escalation, options, area, year
built, assessed value, debt, insurance and condition - is either withheld for privacy or genuinely unknown to this
analysis. <em>Withheld</em> means it exists and is excluded; <em>unverified</em> means no official source confirmed it. The
distinction matters at sale: a buyer will price the lease it reads, not the lease described in a marketing summary.</p>""")

    body += section("Regulation", "Transfer tax, assessment and wage rules", anchor="regulation", body=table(rows_for(["REG"])) +
        f"""<p class="prose"><strong>The ULA cliff.</strong> The City of Los Angeles charges a 0.45% base real property transfer
tax. Measure ULA adds 4.0% on consideration above ${ULA_LOW:,} and 5.5% at ${ULA_HIGH:,} or more, and the surcharge applies
to the whole price, not the excess. On a sale at exactly ${ULA_LOW:,} the city tax is {money(city_transfer_tax(ULA_LOW))};
one dollar higher it is {money(city_transfer_tax(ULA_LOW + 1))}. Working the other way, at a 6.25% capitalisation rate a
${ULA_LOW:,} price corresponds to {money(ULA_LOW * 0.0625)} of annual net operating income - so whether a sale crosses the
line is a question about rent, not about negotiation style.</p>
<p class="prose"><strong>Assessment and wages.</strong> Proposition 13 caps assessed-value growth at 2% a year, and Proposition 8
allows a temporary decline-in-value reduction filed between 2 July and 30 November (REG-06, REG-07). California's fast-food
minimum wage has been $20.00 an hour since 1 April 2024, which is a direct cost line for the tenant and therefore a rent-coverage
risk for the landlord (REG-08). Unverified regulatory items - the citywide minimum wage, county documentary transfer tax and the
parcel's own tax rate - are blank (REG-10 to REG-12).</p>""")

    body += section("Diligence", "The five documents that decide this question", """
<div class="callout"><p><strong>In priority order:</strong></p>
<ol class="findings">
<li><strong>The executed lease and every amendment.</strong> Firm term, expiry date, renewal options and notice windows, rent
schedule, percentage rent, NNN exclusions, roof and structure, assignment and change-of-control, guaranty and recourse.</li>
<li><strong>Two years of rent ledger and NNN reconciliations.</strong> What was actually billed and collected, and what the
tenant disputed.</li>
<li><strong>Current title, survey and the assessor's parcel record.</strong> Vesting, easements, liens, access and the
Prop 13 base year value.</li>
<li><strong>Insurance policy, loss runs and quotes.</strong> Coverage, deductibles, exclusions, business-interruption terms
and what the lease makes the tenant carry.</li>
<li><strong>A broker's opinion of value with three closed net-lease comparables</strong> inside central Los Angeles, plus the
tenant's most recent quarterly filing.</li>
</ol></div>""")
    return shell("property.html", "Lease &amp; property", body)


def page_tenant():
    body = hero(
        "Asset &amp; tenant &middot; credit",
        "Issuer-wide filings - the subject unit is not identified in them",
        "A franchisor with falling sales, closing stores and no dividend - and $275-290 million of guided franchise margin.",
        "The tenant of record may be Jack in the Box Inc. or a franchisee; the filings cannot tell you which, and no public "
        "record in this repository identifies the operator (TEN-18). What the filings can tell you is how the brand is "
        "trading, and that is the credit behind the rent.",
        '<a class="button" href="risks.html">Risk register <span aria-hidden="true">&rarr;</span></a>',
    )
    body += section("Results", "Fiscal 2025 results and fiscal 2026 guidance", table(rows_for(["TEN"])) +
        """<p class="prose"><strong>Reading:</strong> same-store sales fell 7.4% in the fourth quarter - worse in franchise
stores (-7.6%) than company stores (-5.3%) - and 4.2% for the year, with 86 closures against 31 openings. Adjusted EBITDA
of $45.6 million in the quarter was down from $65.5 million a year earlier, and the dividend was discontinued. Franchisees
carry the sales decline and the $20.00 California wage floor at the same time, which is the channel through which a
landlord's rent coverage weakens.</p>
<p class="prose">The offsetting facts are equally verified: fiscal 2026 guidance keeps the brand at 2,050-2,100 restaurants
with same-store sales of -1% to +1% and franchise-level margin of $275-290 million. A franchisor in that position is still
collecting royalties and still needs its better locations. That is the definition of a negotiable credit.</p>
<p class="prose"><strong>Not published:</strong> the operator of the subject unit, any guaranty, the issuer's credit rating and
any location-level sales (TEN-18 to TEN-20). No rating-agency page was opened for this brief, so no rating is stated.</p>""")
    return shell("tenant.html", "Tenant credit", body)


def page_model():
    grid_rows = []
    for noi in NOI_SCENARIOS:
        cells = [f"<strong>{money(noi)}</strong>"]
        for c in CAP_RATES:
            cells.append(f"{money(direct_cap_value(noi, c))}")
        grid_rows.append(cells)

    friction_rows = []
    for p in [4_500_000, 5_300_000, ULA_LOW, ULA_LOW + 1, 6_000_000, 10_800_000, ULA_HIGH, 11_000_000]:
        friction_rows.append([
            money(p),
            pct(ula_rate(p), 1),
            money(BASE_TRANSFER * p),
            money(ula_rate(p) * p),
            money(sale_friction(p)),
            money(net_sale_proceeds(p)),
        ])

    c0_ref = 0.0625
    noi_ref = 200_000
    hold_rows = []
    sell_now = net_sale_proceeds(direct_cap_value(noi_ref, c0_ref))
    for c5 in CAP_RATES:
        npv = npv_hold(noi_ref, c0_ref, c5)
        diff = npv - sell_now
        verdict = "Hold wins" if diff > 0 else "Sale wins"
        hold_rows.append([pct(c5), money(npv), money(sell_now), money(diff), f"{npv/sell_now:.3f}x", verdict])

    be_rows = []
    for c0 in CAP_RATES:
        be = breakeven_exit_cap(noi_ref, c0)
        be_rows.append([pct(c0), money(direct_cap_value(noi_ref, c0)),
                        money(net_sale_proceeds(direct_cap_value(noi_ref, c0))),
                        pct(be), f"{(be - c0)*10000:+.0f} bp"])

    trend = trend_rows()

    body = hero(
        "Analysis &middot; projection model",
        "Deterministic arithmetic - reproducible with python3 scripts/build_site.py",
        "A value range you can test, not a valuation you can trust.",
        "The appraised value, the rent and the capitalisation rate are not public. Rather than invent them, the model runs "
        "them as inputs and reports what the answer is for each combination, including the exact exit capitalisation rate at "
        "which holding stops beating selling.",
        '<a class="button" href="decision.html">Use the model in the decision <span aria-hidden="true">&rarr;</span></a>',
    )

    body += section("Assumptions", "What is an input, and what is verified", simple_table(
        ["Input", "Value used", "Status", "Basis"],
        [
            ["Annual net operating income (NNN rent)", "$150,000 / $200,000 / $250,000 / $300,000", '<span class="badge badge-unverified">Assumption</span>',
             "Scenarios, not observations. Your lease supplies the real number (PRP-07)."],
            ["Entry capitalisation rate (sale today)", "5.25% to 7.25% in 50 bp steps", '<span class="badge badge-unverified">Assumption</span>',
             "No official source publishes a cap rate for this asset (CAP-02)."],
            ["Exit capitalisation rate (sale in year 5)", "same range", '<span class="badge badge-unverified">Assumption</span>',
             "Tested explicitly rather than guessed."],
            ["Rent growth", "2.5% a year", '<span class="badge badge-unverified">Assumption</span>',
             "Between the verified 2.6% core CPI and 3.7% headline CPI for Los Angeles (PRI-01, PRI-02)."],
            ["Discount rate", "7.5%", '<span class="badge badge-unverified">Assumption</span>',
             "A required return for a single-tenant net-lease asset; not sourced."],
            ["Brokerage, legal and escrow on sale", "2.0% of price", '<span class="badge badge-unverified">Assumption</span>',
             "Typical range; obtain a quote."],
            ["City base transfer tax", "0.45% of price", '<span class="badge badge-verified">Verified</span>', "LA Office of Finance (REG-01)."],
            ["Measure ULA surcharge", "4.0% above $5.4m; 5.5% at $10.9m or more", '<span class="badge badge-verified">Verified</span>',
             "LA Office of Finance (REG-02 to REG-04)."],
            ["Cost-of-capital context", "10-year Treasury 4.84% (2026-11-05)", '<span class="badge badge-verified">Verified</span>',
             "Federal Reserve H.15 via FRED (CAP-01)."],
        ], cls="calc", foot="Source basis: " + source_link("LA-ULA") + " (transfer tax and ULA rates), " + source_link("FRED-DGS10") + " (10-year Treasury), " + source_link("BLS-CPI") + " (inflation context). Rows marked Assumption are the brief's inputs, not observations."))

    body += section("Valuation", "Direct capitalisation value grid",
        simple_table(["Annual NOI"] + [pct(c) for c in CAP_RATES], grid_rows,
                     '<p class="caption">Sale value = annual NOI / capitalisation rate. Read across a row: at $200,000 of NOI the asset is worth $2.76M at a 7.25% rate and $3.81M at a 5.25% rate - the same income stream is worth 38% more at 5.25% than at 7.25%, a spread produced by a 200 basis-point move alone.</p>', cls="calc", foot="Value = NOI / cap rate. Cap rates are the labelled assumptions above; no official cap rate exists for this asset (" + source_link("FRED-DGS10") + " supplies only the risk-free rate).") +
        """<p class="prose"><strong>What this means for the decision:</strong> the value question is not "what is it worth" but
"what rate would a buyer pay, and do I know something about the rent that a buyer would pay more for?" Renewing at market
rent with documented escalations is the only lever in your control that raises the numerator of that fraction.</p>""")

    body += section("Exit cost", "Transfer tax and the $5.4 million cliff",
        simple_table(["Sale price", "ULA rate", "Base tax (0.45%)", "ULA surcharge", "Total friction (+2% costs)", "Net proceeds"], friction_rows,
                     '<p class="caption">Friction = city base transfer tax + Measure ULA + assumed 2.0% brokerage/legal/escrow. '
                     'The surcharge applies to the whole consideration, which is why the jump from $5,400,000 to $5,400,001 costs about $216,000.</p>',
                     cls="calc", foot="Rates from " + source_link("LA-ULA") + " (0.45% base; 4.0% above $5,400,000; 5.5% at $10,900,000 or more, for closings after 30 June 2026). The 2.0% brokerage/legal/escrow line is an assumption.") +
        f"""<p class="prose"><strong>Implication:</strong> if a bid lands just above the threshold, the marginal cost of those
last dollars is enormous. Negotiating price, allocating fixtures or personal property, or timing a sale so that the price sits
below the line are legitimate levers - all of which require a professional opinion on how the City applies the tax to your
specific transaction. This brief does not give tax advice; it flags the cliff and its verified rate.</p>""")

    body += section("Hold versus sell", "Five-year hold against an immediate sale",
        f"""<p class="caption">Reference case: $200,000 of annual NOI, entry capitalisation rate 6.25% (a {money(direct_cap_value(noi_ref, c0_ref))} price),
rent growth 2.5%, discount rate 7.5%, five-year hold, exit at the capitalisation rate shown.</p>""" +
        simple_table(["Exit cap rate", "NPV of holding", "Net proceeds if sold today", "Difference", "Hold / sell ratio", "Result"], hold_rows,
                     cls="calc", foot="Arithmetic on the labelled assumptions; the ten-year Treasury (" + source_link("FRED-DGS10") + ") and the Los Angeles CPI (" + source_link("BLS-CPI") + ") are context for the discount and growth inputs, not values read into the model.") +
        """<p class="prose"><strong>Reading:</strong> holding wins unless the exit capitalisation rate is more than about 58 basis
points wider than today's. That is the single most important number in this brief: the case for selling is a bet that
cap rates will widen by more than that within five years, or a need for liquidity that outweighs the arithmetic. Note the
model is pre-tax and unlevered; after-tax results depend on your basis and cannot be computed without it (see
<a href="flagged.html">flagged items</a>).</p>""")

    body += section("Break-even", "The exit rate at which holding stops paying",
        simple_table(["Entry cap rate", "Price today", "Net proceeds today", "Break-even exit cap rate", "Cushion"], be_rows,
                     '<p class="caption">Break-even exit rate: the rate at which the discounted value of five years of rent plus a sale equals the net cash you would hold today. A wider cushion means holding is more robust to a repricing.</p>',
                     cls="calc", foot="Bisection solution of the hold NPV in the Method section. Transfer-tax rates from " + source_link("LA-ULA") + ".") +
        """<p class="prose"><strong>Reading:</strong> the cheaper the entry price (a higher entry cap rate), the more room
there is for rates to rise before selling would have been better. If a broker quotes you a 5.25% cap rate today, the
break-even exit rate is only about 5.40% - almost no cushion. If the market is really at 7.25%, the break-even exit is
8.44% - a comfortable margin. Ask for the cap-rate evidence before you accept either.</p>""")

    body += section("Area trend", "Mechanical continuation of verified change",
        simple_table(["Year", "Los Angeles County population (trend)", "MSA nonfarm employment (trend)"], trend,
                     '<p class="caption">Population: 9,694,934 (Census, 1 July 2025) extended at -0.618% a year, the annualised 2020-2025 county change. '
                     'Employment: 6,282.1 thousand (BLS, September 2026) extended at +0.5% a year, the verified 12-month change. Mechanical only.</p>',
                     cls="calc", foot="Population base " + source_link("CEN-COUNTY") + "; employment base " + source_link("BLS-EAG") + ". Growth rates are the verified 2020-2025 and 12-month changes, continued mechanically.") +
        """<p class="prose">These two lines point in opposite directions - a slowly shrinking county and a slowly growing job
base. For a restaurant site the job number matters more for lunch traffic and the population number more for residential
dinner traffic, which is exactly why no single area statistic can decide this asset. The official California Department of
Finance projection exists but could not be read in this build (POP-01); it is flagged rather than approximated.</p>""")

    body += section("Method", "Formulas, so the arithmetic can be checked", """
<div class="formula">
<p><strong>Value:</strong> V = NOI / c</p>
<p><strong>Net proceeds:</strong> P - (0.0045 + u(P)) x P - 0.02 x P, where u(P) = 0 above $5.4m, 0.04 above $5.4m, 0.055 at $10.9m or more</p>
<p><strong>Hold NPV:</strong> sum over t = 1..5 of NOI x (1+g)^t / (1+d)^t + net proceeds of a sale at NOI x (1+g)^5 / c5, discounted 5 years</p>
<p><strong>Break-even exit rate:</strong> solve for c5 where hold NPV equals net proceeds today (bisection, 200 iterations)</p>
</div>
<p class="prose"><strong>Limits.</strong> Pre-tax, unlevered, no capital expenditure, no vacancy, no lease-expiry event inside
the five years, no transaction-cost inflation and no probability weighting. It is a sensitivity tool: it tells you which
inputs matter and how much, not what will happen. A licensed appraiser, a tax adviser and a broker's opinion of value are
required before any transaction.</p>""")

    return shell("model.html", "Projection model", body)


def page_decision():
    rec_rows = [
        ["<strong>1. Secure the renewal before the option window closes.</strong>",
         "Ask the operator now - not at expiry - for a five-year extension or a new term with market rent, documented annual "
         "escalations, tenant-funded roof and structure, and a guaranty. A signed lease with eight or more years of term is "
         "worth more to a buyer than the same asset with two.",
         "Tenant credit still supports occupancy: 2,136 restaurants, franchise-level margin guided at $275-290 million, and a "
         "same-store sales guide of -1% to +1% for fiscal 2026. Waiting converts a negotiating position into a countdown.",
         "SEC filing (Q4 FY2025 release)", "SEC-Q4"],
        ["<strong>2. Price the alternative before you sign.</strong>",
         "Obtain a broker's opinion of value with closed net-lease comparables, and two rent comparables for the same trade area. "
         "Agree to renewal rent only against that evidence, never against the tenant's first offer.",
         "No verified capitalisation rate or market rent exists for this parcel, so any rent you accept without comps is arbitrary.",
         "Model: value grid and break-even", None],
        ["<strong>3. Do not sell while the price is ununderwritten.</strong>",
         "Selling without a bid is not a decision, it is a surrender of the option. Sell when a bid implies a capitalisation "
         "rate inside the break-even band - or when a trigger below fires.",
         "At a 6.25% entry rate the break-even exit rate is about 6.83%; a sale today only wins if you believe cap rates widen "
         "beyond that, or you need the liquidity.",
         "Model: hold versus sell", None],
        ["<strong>4. Treat the transfer-tax cliff as a design constraint.</strong>",
         "If a sale is likely, plan the process so that a marginal bid above $5,400,000 cannot cost you $216,000 in tax. Get a "
         "written opinion on how the City will apply the tax to your transaction.",
         "Measure ULA is 4.0% of the whole price above $5.4m and 5.5% at $10.9m; the base tax is 0.45%.",
         "LA Office of Finance", "LA-ULA"],
        ["<strong>5. Hold the asset only at a risk you can carry.</strong>",
         "Confirm insurance (including business interruption and what the lease makes the tenant carry), a reserve for roof and "
         "structure, and a written plan for the day the tenant vacates. If a single asset is most of your net worth, that is an "
         "argument for a partial exit, not for an unpriced one.",
         "Concentration, insurability and vacancy downtime are unverified for this parcel; the brief does not assume they are fine.",
         "Flagged for review", None],
    ]

    trigger_rows = [
        ["Tenant same-store sales", "Two more consecutive quarters below -5%, or guidance cut again",
         "Sell or re-tenant preparation", "SEC-Q4"],
        ["Restaurant closures", "Announced California closures in this trade area, or a unit-count guide below 2,050",
         "Sell while the lease is still performing", "SEC-Q4"],
        ["Renewal rent", "Operator offers rent below your comp-supported market rent with no escalations",
         "Take the sale process to market instead", "LA-ZIMAS"],
        ["Capitalisation rate", "A bid implies 6.25% or tighter (a price at or above the model's break-even)",
         "Sell into strength", "FRED-DGS10"],
        ["Debt cost", "Ten-year Treasury above about 5.5% while your asset is unencumbered",
         "Hold; do not refinance into it", "FRED-DGS10"],
        ["Insurance", "Premium increase above 25% at renewal, or any coverage exclusion for fire or quake",
         "Re-underwrite the hold; consider exit", "LACO-ASSESSOR-HOME"],
        ["Parcel hazard", "Parcel falls in a Very High FHSZ, an Alquist-Priolo zone, or a seismic hazard zone",
         "Price it in, mitigate, or sell to a buyer who will", "OSFM-FHSZ"],
    ]

    body = hero(
        "Analysis &middot; decision",
        "Verdict: renew on market terms, hold, sell on a trigger",
        "Renew, hold, and let a priced bid - not a hunch - decide the sale.",
        "Five to nine years of remaining term is the asset's main value. Everything verified here points the same way: keep "
        "the contractual income, negotiate from evidence, and refuse to sell into a number nobody has supported. The risks "
        "that would change this answer are named, with thresholds, below.",
        '<a class="button" href="model.html">Check the arithmetic <span aria-hidden="true">&rarr;</span></a>'
        '<a class="button button-secondary" href="risks.html">Read the risks</a>',
    )

    def _src(x):
        return source_link(x) if x else '<span class="muted">See the linked page</span>'

    _ = None
    rec_rows = [[row[0], row[1], row[2], _src(row[4])] for row in rec_rows]
    body += section("The plan", "Five moves, in order", simple_table(
        ["Move", "What to do", "Why - evidence", "Source"], rec_rows, cls="calc",
        foot="Basis: " + source_link("SEC-Q4") + " &middot; " + source_link("LA-ULA") + " &middot; " + source_link("FRED-DGS10") + " &middot; " + source_link("BLS-EAG") + " &middot; " + source_link("OSFM-FHSZ") + ". Moves are recommendations drawn from the verified rows; they are not themselves sourced facts."))

    trigger_rows = [[c if i < 3 else source_link(c) for i, c in enumerate(row)] for row in trigger_rows]
    body += section("Triggers", "What would change the answer",
        simple_table(["Signal", "Threshold", "Action", "Evidence source"], trigger_rows,
                     '<p class="caption">Thresholds are decision rules set in this brief, not market forecasts. Each is tied to a verified data series that can be re-checked at the linked source.</p>'))

    body += section("Risk balance", "Wealth preservation versus growth", f"""
<div class="two-col">
<div class="callout"><h3>What holding protects</h3>
<ul class="findings">
<li>Contractual NNN rent and the tax treatment of an income asset, with no forced sale date.</li>
<li>Optionality: a re-based rent at renewal, a re-tenanting play at expiry, or a land-value exit.</li>
<li>No transfer tax now. At a $5.4m price the city tax alone is {money(city_transfer_tax(ULA_LOW))}; at $5.4m+1 it is {money(city_transfer_tax(ULA_LOW+1))}.</li>
<li>Section 1031 remains available later: 45 days to identify and 180 days to close once you do sell (REG-09).</li>
</ul></div>
<div class="callout"><h3>What holding costs</h3>
<ul class="findings">
<li>Concentration: one tenant, one parcel, one insurance market.</li>
<li>Credit drift: systemwide same-store sales of -7.4% in Q4 FY2025 and 86 closures in the year.</li>
<li>Cost inflation the lease may not fully pass through: Los Angeles CPI +3.7%, energy +20.3% (PRI-01, PRI-06).</li>
<li>Rate risk: a widening from 5.25% to 7.25% cuts value by roughly 28% at constant NOI (see the model grid).</li>
</ul></div>
</div>
<p class="prose"><strong>How to keep the risk manageable while keeping the upside:</strong> sign the renewal with escalations and
a guaranty (raises the numerator), keep or obtain insurance that actually responds to fire and quake (removes the
uninsurable tail), hold a capital reserve sized to a realistic re-leasing period (absorbs the vacancy scenario), and set the
sale decision in advance with the triggers above (removes the emotional sale). None of those steps requires knowing today's
capitalisation rate; all of them improve what a buyer will pay if you do sell.</p>""")

    body += section("Black swans", "Low-frequency, high-impact events", simple_table(
        ["Event", "Verified precedent or scenario", "How it reaches this asset", "Preparation"],
        [
            ["Urban wildfire and smoke", "Palisades Fire, January 2025: 23,448 acres, 6,845 structures destroyed, 12 deaths (CAL FIRE).",
             "Direct damage, smoke closure, evacuation, loss of customer traffic, and a harder insurance market countywide.",
             "Confirm the parcel's Fire Hazard Severity Zone, defensible space, roof class and coverage; know whether the lease puts restoration on the tenant."],
            ["Major earthquake", "USGS ShakeOut Mw 7.8 scenario: 1,800 deaths, 53,000 injuries, $191 billion regional economic loss.",
             "Damage and closure, water and power interruption (the scenario attributes $24 billion to water-outage business interruption), and tenant failure.",
             "Seismic retrofit status, deductible size, business-interruption limits, and the lease's damage-and-restoration clause."],
            ["Tenant insolvency or mass closure", "FY2025: 86 closures, same-store sales -7.4% in Q4, dividend discontinued.",
             "Rent stops; the building is a vacant drive-through in a market with no verified rent comp.",
             "Guaranty at renewal, security deposit, monthly financial covenants, and a written re-tenanting budget."],
            ["Rate shock", "10-year Treasury 4.84% (2026-11-05); a widening from 5.25% to 7.25% cuts value by about 28% at constant NOI.",
             "Buyers finance at a spread; a higher rate means a wider cap rate and a lower price.",
             "Fixed-rate, long-dated debt if any; sell only into a priced bid; do not assume refinancing."],
            ["Regulatory shock", "Measure ULA 4.0%/5.5%; California fast-food minimum wage $20.00/hour since 1 April 2024.",
             "Transfer tax takes cash at exit; the wage floor compresses the tenant's margin and its ability to pay rent.",
             "Model the ULA tier before pricing; monitor the Fast Food Council; negotiate rent that survives a margin squeeze."],
        ], cls="calc", foot="Basis: " + source_link("CALFIRE-PAL") + " &middot; " + source_link("USGS-SHAKEOUT") + " &middot; " + source_link("SEC-Q4") + " &middot; " + source_link("FRED-DGS10") + " &middot; " + source_link("LA-ULA") + " &middot; " + source_link("DIR-FF") + ". Preparations are recommendations, not verified facts."))
    body += """<p class="prose"><strong>What this brief will not do:</strong> assign a probability to any of these events for this
parcel. No official source publishes parcel-level wildfire, earthquake or flood probabilities for an anonymous address, and
inventing one would be worse than leaving it blank.</p>"""

    body += section("Next 90 days", "The checklist", """
<ol class="findings">
<li>Pull the executed lease and all amendments; calendar every renewal notice date. If the notice window has already passed,
get written confirmation of the tenant's intention.</li>
<li>Order title, survey and the assessor's parcel record; confirm zoning and legal use in ZIMAS.</li>
<li>Request the tenant's last eight quarters of unit-level sales and its franchisee financials if the operator is a franchisee.</li>
<li>Obtain three closed net-lease comparables and two rent comparables for central Los Angeles; derive a cap-rate range.</li>
<li>Get insurance quotes for fire, quake and business interruption; compare with what the lease requires the tenant to carry.</li>
<li>Take the renewal proposal and the comps to a tax adviser; model the sale under Section 1031 and without it.</li>
<li>Write the trigger table above into your file, with the dates you will re-check each series.</li>
</ol>""")

    return shell("decision.html", "Sell vs renew", body)


def page_risks():
    register = [
        ["Tenant sales and unit-count decline",
         "Systemwide same-store sales -7.4% in Q4 FY2025 and -4.2% for the year; 86 closures against 31 openings; dividend discontinued.",
         '<span class="badge badge-verified">Verified</span>', "Quarterly watch; require a guaranty and covenants at renewal.", "SEC-Q4"],
        ["Franchisee operating-cost shock",
         "California fast-food minimum wage $20.00/hour from 1 April 2024; Los Angeles CPI +3.7% and energy +20.3% over the year.",
         '<span class="badge badge-verified">Verified</span>', "Rent coverage test at renewal; escalations that keep pace with CPI.", "DIR-FF"],
        ["Rent reset at renewal",
         "No verified market rent exists for this parcel or its trade area.",
         '<span class="badge badge-unverified">Unverified</span>', "Two independent rent comps before agreeing any renewal rent.", "LA-ZIMAS"],
        ["Capitalisation-rate expansion",
         "10-year Treasury 4.84%; a widening from 5.25% to 7.25% cuts value by about 28% at constant NOI (model grid).",
         '<span class="badge badge-verified">Verified</span>', "Fixed-rate long debt if any; sell into a priced bid, not into a hope.", "FRED-DGS10"],
        ["Transfer-tax cliff at exit",
         "0.45% base; 4.0% ULA above $5.4m; 5.5% at $10.9m. Crossing $5.4m by one dollar costs about $216,000.",
         '<span class="badge badge-verified">Verified</span>', "Price and structure the sale with a written tax opinion.", "LA-ULA"],
        ["Property-tax reset",
         "Assessed value follows a Proposition 13 base-year value capped at 2% growth; a decline-in-value claim must be filed 2 July - 30 November.",
         '<span class="badge badge-verified">Verified</span>', "Confirm with the Assessor what a sale does to the base year and the annual bill.", "LACO-ASSESSOR"],
        ["Wildfire hazard at the parcel",
         "State Responsibility Area maps use Moderate / High / Very High classes (effective 1 April 2024); 2025 Local Responsibility Area maps were delivered to all counties.",
         '<span class="badge badge-unverified">Parcel not mapped</span>', "Run the FHSZ viewer with the address; confirm defensible space and roof class.", "OSFM-FHSZ"],
        ["Wildfire precedent loss in this county",
         "Palisades Fire: 23,448 acres, 6,845 structures destroyed, 975 damaged, 12 civilian deaths, contained after 24 days.",
         '<span class="badge badge-verified">Verified</span>', "Insurance and business-interruption review; lease restoration clause.", "CALFIRE-PAL"],
        ["Surface fault rupture",
         "Structures for human occupancy may not be placed over an active fault and generally must be at least 50 feet away; an active fault has ruptured within 11,000 years.",
         '<span class="badge badge-unverified">Parcel not mapped</span>', "Check the Alquist-Priolo zone and seismic hazard zone for the parcel.", "CGS-AP"],
        ["Regional earthquake scenario",
         "ShakeOut Mw 7.8: 1,800 deaths, 53,000 injuries, $191 billion economic loss, about 1,600 fires.",
         '<span class="badge badge-verified">Verified</span>', "Seismic retrofit status, deductibles, business-interruption limits.", "USGS-SHAKEOUT"],
        ["Regional earthquake probability",
         "USGS/UCERF3: 60% chance of M6.7+ in the Los Angeles region within 30 years, 46% for M7.0+, 31% for M7.5+.",
         '<span class="badge badge-verified">Verified (regional)</span>', "Retrofit status, deductibles and business-interruption limits; the probability is regional, not parcel-level.", "USGS-UCERF3"],
        ["Population decline",
         "Los Angeles County population -3.2% and city -0.8% since the 2020 estimate base; annualised -0.62% and -0.15%.",
         '<span class="badge badge-verified">Verified</span>', "Do not underwrite traffic growth; re-check annually.", "CEN-COUNTY"],
        ["Job-mix shift",
         "Education and health +3.8% and trade/transportation +0.3% against information -5.7% and financial activities -1.7%.",
         '<span class="badge badge-verified">Verified</span>', "Understand which daypart the site depends on before renewing at a premium.", "BLS-EAG"],
        ["Consumer price pressure",
         "Food away from home +2.8% against all items +3.7%: menu prices lag the household basket.",
         '<span class="badge badge-verified">Verified</span>', "Test rent coverage against flat, not rising, unit sales.", "BLS-CPI"],
    ]

    body = hero(
        "Analysis &middot; risk register",
        "Fourteen registered risks; none quantified for the parcel",
        "The exposures are real; the probabilities are not knowable from here.",
        "Each row links the official page that evidences the risk. Where the exposure depends on the parcel, the row says so "
        "rather than assigning a score. Items with no official source at all are on the Flagged for review page, not here.",
        '<a class="button" href="flagged.html">Flagged items <span aria-hidden="true">&rarr;</span></a>',
    )
    register = [[c if i < 4 else source_link(c) for i, c in enumerate(row)] for row in register]
    body += section("Register", "Business-as-usual and structural risks", simple_table(
        ["Risk", "Mechanism and verified evidence", "Status here", "Mitigation", "Official source"], register,
        '<p class="caption">"Parcel not mapped" means the hazard exists as a mapped category but this asset has not been located on the map, because the address is deliberately not published.</p>'))

    body += section("Hazards", "Catastrophe and insurance data", table(rows_for(["CAT"])) +
        """<p class="prose"><strong>Reading:</strong> the verified catastrophe data is regional, and it is large: a county fire
that destroyed 6,845 structures in January 2025, and a modelled southern San Andreas event with $191 billion of economic
loss. Neither number is a probability for this site. What can be verified for the site is only whether it sits in a mapped
zone - and that requires the address, which is why CAT-08, CAT-11, CAT-12 and CAT-16 are blank.</p>""")

    body += section("Insurance", "The tail that decides whether a hold is survivable", """
<p class="prose">Insurance is the mechanism that converts an uninsurable tail into a manageable one - or fails to. This brief
does not publish a premium, a deductible, a coverage limit or an availability conclusion for this parcel, because no policy
was reviewed (PRP-17, CAT-17) and no California Department of Insurance page was opened in this session. Treat that as the
single largest verification gap on this page: an owner who cannot bind affordable fire and quake cover is holding a
different asset than the one modelled here.</p>
<p class="prose">The lease question is equally concrete: under a triple-net lease the tenant typically carries insurance and
restoration, but "typically" is not a contract term. Read the insurance, damage-and-restoration and condemnation clauses
before relying on them (PRP-10, CAT-18).</p>""")
    return shell("risks.html", "Risk register", body)


def page_flagged():
    open_items = [r for r in ROWS if r["status"] in ("unverified", "withheld")]
    rows = []
    for r in open_items:
        if r["status"] == "withheld":
            close = "Exists in the owner file; excluded from publication by the privacy policy. Review offline."
        else:
            close = r["note"] or "No official source confirmed it in this session."
        rows.append([r["id"], r["metric"], badge(r["status"]), close, source_link(r["src"])])

    irregularities = [
        ["R-01", "A prior build of this repository stated ShakeOut scenario economic losses of $213 billion. The USGS abstract states $191 billion.",
         "Corrected to $191 billion (CAT-14) and the $213 billion figure is withdrawn.", "USGS-SHAKEOUT"],
        ["R-02", "A prior dataset cited <code>cityattorney.lacity.gov/homelessness</code> as the source for Measure ULA transfer-tax rates and for several withheld property fields.",
         "Replaced with the Office of Finance ULA FAQ (REG-01 to REG-05) and the Assessor / ZIMAS lookups.", "LA-ULA"],
        ["R-03", "County median household income appears as $90,112 (Census QuickFacts, 2020-2024 ACS) and $90,757 (a FRED series cited by a prior build). These are different products and vintages.",
         "This brief publishes the QuickFacts figure (INC-02) and never blends the two.", "CEN-COUNTY"],
        ["R-04", "Prior builds quoted California Department of Finance county population projections for 2030, 2035 and 2040 with specific values.",
         "The P-2 workbook could not be read in this environment, so the official projections are withheld (POP-01, POP-02) rather than copied from secondary summaries.", "DOF-PROJ"],
        ["R-07", "A prior build left county population density blank as unverified, although the Census publishes it (2,466.9 per sq mi).",
         "Filled from the official page (DEM-11). Blank is reserved for genuinely unconfirmable values.", "CEN-COUNTY"],
        ["R-08", "The Q4 FY2025 release's table shows 2,136 Jack in the Box restaurants at fiscal year end, while the same release's boilerplate says 'approximately 2,135 restaurants across 21 states'.",
         "This brief publishes the table figure (TEN-01) and notes the boilerplate difference here. Neither figure is a statement about the subject unit.", "SEC-Q4"],
        ["R-09", "Prior builds treated the CPI-indexed Measure ULA thresholds as unverifiable and published none. The Office of Finance now states $5,400,000 and $10,900,000 for closings after 30 June 2026.",
         "Published as verified (REG-02, REG-03) with the effective-date condition stated in the row.", "LA-ULA"],
        ["R-10", "No official source publishes a capitalisation rate or a market rent for this asset or its trade area.",
         "Not published (CAP-02, HOU-10). The model runs rates as labelled assumptions instead.", "FRED-DGS10"],
        ["R-11", "This brief assigns no probability to any black-swan event. Prior builds contained paragraph-level risk narrative without parcel data.",
         "Kept as a documented limitation rather than converted into a score or a probability.", "USGS-SHAKEOUT"],
    ]

    body = hero(
        "Verification &middot; flagged for review",
        f"{len(open_items)} open items, published rather than guessed",
        "Everything this brief could not verify, in one place.",
        "Each item below is either unverified (no official source confirmed it in this session) or withheld (it exists but the "
        "privacy policy excludes it). Nothing on this page blocks the rest of the brief: the recommendation is built so that "
        "these gaps change the inputs, not the method.",
        '<a class="button" href="sources.html">Sources &amp; method <span aria-hidden="true">&rarr;</span></a>',
    )

    body += section("Open items", "Unverified and withheld rows",
        f'<p class="prose">{len(open_items)} of {len(ROWS)} published rows are open: '
        f'{counts()["unverified"]} unverified and {counts()["withheld"]} withheld. A blank value is never zero.</p>' +
        simple_table(["ID", "Item", "Status", "What would close it", "Official lookup"], rows))

    irregularities = [[c if i < 3 else (source_link(c) if c else '<span class="muted">n/a</span>') for i, c in enumerate(row)] for row in irregularities]
    body += section("Irregularities", "Conflicts and corrections found while verifying",
        simple_table(["Ref", "Finding", "Resolution", "Source"], irregularities,
                     '<p class="caption">These are recorded so the owner can see what changed and why. None of them is silently removed: prior builds remain in <code>archive/</code>.</p>'))

    body += section("Repository irregularities", "Two findings that are about the repository, not about the property", """
<div class="callout">
<p><strong>R-05 - conflict markers on the shared board.</strong> <code>COORDINATION.md</code> on <code>main</code> contained
unresolved git conflict markers (<code>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</code>, <code>=======</code>,
<code>&gt;&gt;&gt;&gt;&gt;&gt;&gt; origin/main</code>) from overlapping sessions, which made the task board unreadable. It is rebuilt
as a single board on this branch; every prior session's record is preserved in its session log, and no prior work was deleted.</p>
<p><strong>R-06 - two publishers for one site.</strong> The repository's GitHub Pages source is the legacy branch build from
<code>main</code> (root), while the workflow also ran an artifact deployment, so two processes could publish the same URL. The
workflow now validates only, which makes the published site exactly the repository root. The live URL is checked after merge and
the result is recorded on the task board.</p>
</div>""")

    body += section("Prior sessions", "Preserved work from parallel sessions", """
<p class="prose">Earlier sessions published their own sites and verification ledgers on this URL. Nothing was deleted. The
build that was live on <code>main</code> before this integration - including its <em>Verification audit</em> page, which
re-checked 33 figures and corrected two - is preserved at
<a href="archive/legacy-2026-11-07/main-d2a64a9e/audit.html">archive/legacy-2026-11-07/main-d2a64a9e/audit.html</a> and
remains readable. Three of its findings that could be re-verified here were absorbed into this dataset: metropolitan GDP
(ECO-24), county GDP (ECO-25) and the USGS 30-year regional earthquake probability (CAT-19). Its FEMA National Risk Index
values were withheld there for want of a readable official page, and they are not published here either.</p>""")

    body += section("Privacy", "Privacy audit of this publication", """
<div class="callout">
<p><strong>What is published:</strong> aggregated government statistics, public-company filings, statutory rates, and the
official page each came from.</p>
<p><strong>What is not published:</strong> owner name, street address, parcel number, ownership entity, lease document, rent
figure, debt balance, assessed value, insurance details, or any individual financial circumstance. These appear in the tables
only as <em>[Withheld]</em>.</p>
<p><strong>What the site collects:</strong> nothing. No cookies, no analytics, no third-party scripts, no forms, no fonts or
assets loaded from other domains. The only external requests are the source links a reader chooses to click.</p>
<p><strong>What the repository contains:</strong> the same public data plus the build script. A validation step scans every
page for email-address and phone-number patterns and fails the build if one appears.</p>
</div>""")
    return shell("flagged.html", "Flagged for review", body)


def page_sources():
    rows = []
    for sid in sorted(SOURCES):
        s = SOURCES[sid]
        n = len([r for r in ROWS if r["src"] == sid])
        rows.append([
            sid,
            f'<a href="{s["url"]}" target="_blank" rel="noopener noreferrer">{s["title"]}<span class="ext" aria-hidden="true">&#8599;</span></a>',
            s["publisher"], s["as_of"], str(n),
        ])

    c = counts()
    body = hero(
        "Verification &middot; sources and method",
        f"{len(SOURCES)} official sources, {c['verified']} verified values, opened {ACCESSION_DATE}",
        "Every number has a page behind it, and every page was opened.",
        "This brief was assembled by reading primary sources - Census, BLS, the Federal Reserve via FRED, SEC EDGAR, the City "
        "and County of Los Angeles, California state agencies, USGS and NCES - and recording only what those pages said. Where a "
        "page did not answer a question, the field stayed blank.",
        '<a class="button" href="flagged.html">See what stayed blank <span aria-hidden="true">&rarr;</span></a>',
    )

    body += section("Register", "Sources used, and how many rows each supports", simple_table(
        ["ID", "Title and link", "Publisher", "As of", "Rows"], rows))

    body += section("Method", "How the verification was performed", f"""
<ol class="findings">
<li><strong>One primary page per claim.</strong> Each row records the URL of the page the value was read from, and the page was
opened in this session. No value was carried over from a prior build without being re-read.</li>
<li><strong>Two readings, one record.</strong> The brief distinguishes what a source states from what this brief concludes:
"verified" means quoted from the page; "derived" means arithmetic on verified values, with the formula written in the row.</li>
<li><strong>Blank over plausible.</strong> If a page did not answer the question - a county unemployment rate, a parcel's fire
zone, an official population projection that ships as an unreadable workbook - the value is blank and listed on
<a href="flagged.html">Flagged for review</a>.</li>
<li><strong>No blending.</strong> City, county and metropolitan figures are never averaged or combined into a synthetic
"central Los Angeles" number. Geography is printed in every row.</li>
<li><strong>Automated gate.</strong> <code>scripts/validate_site.py</code> fails the build if a row in an unverified or
withheld state contains a number, if any table row lacks an official source link, if a link points outside the official
allowlist, if an internal link or anchor does not resolve, or if an email or phone pattern appears.</li>
</ol>""")

    body += section("Reproduce", "Rebuild this site from the dataset", """
<div class="formula">
<p><strong>Build:</strong> <code>python3 scripts/build_site.py</code></p>
<p><strong>Validate:</strong> <code>python3 scripts/validate_site.py</code></p>
<p><strong>Preview:</strong> <code>python3 -m http.server 4173 --bind 0.0.0.0</code></p>
</div>
<p class="prose">The dataset lives in <code>scripts/site_data.py</code>; the model constants and all page templates live in
<code>scripts/build_site.py</code>. A JSON export of the published rows is written to
<code>data/published-records.json</code> on every build for audit.</p>""")

    body += section("Limits", "What this brief is not", """
<ul class="findings">
<li><strong>Not an appraisal.</strong> No property-specific value is stated. The model runs ranges of labelled assumptions.</li>
<li><strong>Not tax, legal or investment advice.</strong> Statutory rates are quoted from the agency that administers them; how
they apply to a specific transaction requires a professional opinion.</li>
<li><strong>Not parcel-specific.</strong> No parcel has been identified, by design. Where a conclusion depends on the parcel,
the row says "parcel not mapped" rather than guessing.</li>
<li><strong>Point-in-time.</strong> Values are as published on or before {ACCESSION_DATE}. Labour, price and filing data are
revised; re-read the linked page before relying on a figure.</li>
<li><strong>Not complete on tenant credit.</strong> No credit rating, no audited financial statements beyond the earnings
release, and no location-level performance were reviewed.</li>
</ul>""")

    return shell("sources.html", "Sources &amp; method", body)


CSS = """
:root{
  --ink:#12181f; --ink-2:#3b4855; --muted:#68757f; --line:#e2e7ec; --bg:#f6f8fa; --panel:#ffffff;
  --accent:#0f766e; --accent-soft:#e6f4f1; --amber:#b45309; --amber-soft:#fdf3e3;
  --grey:#5b6672; --grey-soft:#eef1f4; --blue:#1d4ed8; --blue-soft:#e8eefc; --red:#9f1239;
  --radius:12px; --shadow:0 1px 2px rgba(16,24,40,.05), 0 8px 24px rgba(16,24,40,.04);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.skip-link{position:absolute;left:-999px;top:0;background:#fff;padding:.6rem 1rem;z-index:99}
.skip-link:focus{left:1rem;top:1rem}
.app-shell{display:grid;grid-template-columns:286px minmax(0,1fr);min-height:100vh}
.sidebar{background:#0d1520;color:#e6edf3;padding:22px 18px 32px;position:sticky;top:0;height:100vh;overflow-y:auto}
.brand{display:flex;gap:12px;align-items:center;color:#fff;margin-bottom:26px}
.brand:hover{text-decoration:none}
.brand-mark{width:40px;height:40px;border-radius:10px;background:var(--accent);display:grid;place-items:center;font-weight:800;letter-spacing:.02em;color:#fff;flex:0 0 auto}
.brand-copy{display:flex;flex-direction:column;line-height:1.25}
.brand-copy strong{font-size:.95rem}
.brand-copy span{font-size:.74rem;color:#9fb0c0}
.nav-label{margin:18px 0 8px;font-size:.68rem;letter-spacing:.13em;text-transform:uppercase;color:#7d8fa0}
.site-nav{display:flex;flex-direction:column;gap:2px}
.site-nav a{display:flex;gap:10px;align-items:baseline;padding:8px 10px;border-radius:8px;color:#cfdae4;font-size:.9rem}
.site-nav a:hover{background:rgba(255,255,255,.06);text-decoration:none}
.site-nav a[aria-current="page"]{background:rgba(15,118,110,.28);color:#fff;font-weight:600}
.nav-dot{font-size:.68rem;color:#7d8fa0;font-variant-numeric:tabular-nums}
.sidebar-note{margin-top:26px;padding:12px;border-radius:10px;background:rgba(255,255,255,.05);font-size:.76rem;color:#b6c4d0;line-height:1.5}
.sidebar-note strong{display:block;color:#fff;margin-bottom:4px;font-size:.78rem}
.main-column{display:flex;flex-direction:column;min-width:0}
.topbar{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:14px 34px;background:var(--panel);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:10}
.topbar-left{display:flex;align-items:center;gap:14px;min-width:0}
.crumb{font-size:.8rem;color:var(--muted)}
.snapshot{font-size:.76rem;color:var(--muted);background:var(--grey-soft);padding:5px 10px;border-radius:999px;white-space:nowrap}
.nav-toggle{display:none;border:1px solid var(--line);background:#fff;border-radius:8px;padding:6px 10px;font-size:.8rem}
.content{padding:30px 34px 48px;max-width:1200px;width:100%}
.hero{background:linear-gradient(180deg,#fff,#fbfdfd);border:1px solid var(--line);border-radius:var(--radius);padding:28px 30px;box-shadow:var(--shadow);margin-bottom:12px}
.eyebrow{margin:0 0 8px;font-size:.7rem;letter-spacing:.13em;text-transform:uppercase;color:var(--accent);font-weight:700}
.status-pill{display:inline-block;background:var(--accent-soft);color:#0b5a54;border:1px solid #cbe8e2;padding:5px 11px;border-radius:999px;font-size:.76rem;font-weight:600;margin-bottom:14px}
.hero h1{margin:0 0 12px;font-size:1.95rem;line-height:1.22;letter-spacing:-.015em}
.lede{margin:0;color:var(--ink-2);font-size:1.02rem;max-width:74ch}
.hero-actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}
.button{display:inline-flex;align-items:center;gap:8px;background:var(--accent);color:#fff;padding:10px 16px;border-radius:9px;font-weight:600;font-size:.9rem}
.button:hover{background:#0b5a54;text-decoration:none}
.button-secondary{background:#fff;color:var(--ink);border:1px solid var(--line)}
.button-secondary:hover{background:var(--grey-soft);color:var(--ink)}
.section{margin-top:34px}
.section-heading{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;margin-bottom:12px;flex-wrap:wrap}
.section-heading h2{margin:0;font-size:1.28rem;letter-spacing:-.01em}
.card-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
.metric-card{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:16px 18px;box-shadow:var(--shadow);display:flex;flex-direction:column;gap:4px}
.metric-label{font-size:.78rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;font-weight:600}
.metric-value{font-size:1.62rem;font-weight:700;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.metric-meta{font-size:.82rem;color:var(--ink-2);flex:1}
.metric-source{font-size:.78rem;margin-top:8px}
.metric-source .ext{font-size:.7rem}
.table-wrap{overflow-x:auto;background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);margin:10px 0 16px}
.data-table{width:100%;border-collapse:collapse;font-size:.87rem;min-width:720px}
.data-table th{position:sticky;top:0;background:#f9fbfc;text-align:left;padding:11px 14px;border-bottom:1px solid var(--line);font-size:.73rem;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);white-space:nowrap}
.data-table td{padding:11px 14px;border-bottom:1px solid #eef1f4;vertical-align:top}
.data-table tr:last-child td{border-bottom:none}
.data-table tbody tr:hover{background:#fbfdfd}
.cell-metric{font-weight:600;min-width:220px}
.cell-value{font-variant-numeric:tabular-nums;white-space:normal;min-width:170px}
.cell-empty{color:var(--muted);font-style:italic}
.cell-source{white-space:nowrap;font-size:.82rem}
.row-note{display:block;font-weight:400;font-size:.76rem;color:var(--muted);margin-top:3px;line-height:1.45;white-space:normal}
.ext{display:inline-block;margin-left:3px;font-size:.72em;color:var(--muted)}
.badge{display:inline-block;padding:3px 8px;border-radius:999px;font-size:.72rem;font-weight:700;white-space:nowrap;border:1px solid transparent}
.badge-verified{background:var(--accent-soft);color:#0b5a54;border-color:#cbe8e2}
.badge-derived{background:var(--blue-soft);color:var(--blue);border-color:#d3e0fb}
.badge-unverified{background:var(--amber-soft);color:var(--amber);border-color:#f3ddb7}
.badge-withheld{background:var(--grey-soft);color:var(--grey);border-color:#dfe5ea}
ul.findings,ol.findings{margin:8px 0 0;padding-left:22px;display:flex;flex-direction:column;gap:10px;color:var(--ink-2)}
ul.findings li,ol.findings li{line-height:1.62}
ul.findings strong,ol.findings strong{color:var(--ink)}
.prose{color:var(--ink-2);max-width:88ch;margin:12px 0}
.caption{color:var(--muted);font-size:.84rem;margin:6px 0 0;max-width:88ch}
.callout{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:10px;padding:14px 18px;margin:12px 0;box-shadow:var(--shadow)}
.callout h3{margin:0 0 8px;font-size:1rem}
.callout p{margin:6px 0;color:var(--ink-2)}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.formula{background:#0d1520;color:#dbe7ef;border-radius:var(--radius);padding:16px 18px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.84rem;line-height:1.7;overflow-x:auto}
.formula p{margin:0 0 4px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
.tile{display:flex;flex-direction:column;gap:6px;background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:16px 18px;box-shadow:var(--shadow);color:var(--ink)}
.tile:hover{border-color:#bcd3d0;text-decoration:none;transform:translateY(-1px)}
.tile-title{font-weight:700}
.tile-blurb{font-size:.84rem;color:var(--ink-2);flex:1}
.tile-count{font-size:.74rem;color:var(--accent);font-weight:700;text-transform:uppercase;letter-spacing:.07em}
.muted{color:var(--muted);font-size:.84rem}
code{background:#eef1f4;border-radius:5px;padding:1px 5px;font-size:.86em}
.site-footer{border-top:1px solid var(--line);padding:20px 34px 40px;color:var(--muted);font-size:.8rem;max-width:1200px}
.site-footer p{margin:6px 0}
@media (max-width:960px){
  .app-shell{grid-template-columns:1fr}
  .sidebar{position:fixed;inset:0 auto 0 0;width:280px;transform:translateX(-100%);transition:transform .2s ease;z-index:40}
  .sidebar.open{transform:none}
  .nav-toggle{display:inline-block}
  .content{padding:22px 18px 40px}
  .topbar{padding:12px 18px}
  .two-col{grid-template-columns:1fr}
  .hero h1{font-size:1.55rem}
}
"""

SITE_JS = """(function () {
  var toggle = document.querySelector('[data-nav-toggle]');
  var sidebar = document.getElementById('site-nav');
  if (!toggle || !sidebar) return;
  toggle.addEventListener('click', function () {
    var open = sidebar.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && sidebar.classList.contains('open')) {
      sidebar.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.focus();
    }
  });
})();
"""

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Decision brief">
<rect width="64" height="64" rx="14" fill="#0f766e"/>
<text x="32" y="43" font-family="Helvetica,Arial,sans-serif" font-size="28" font-weight="700" fill="#ffffff" text-anchor="middle">JB</text>
</svg>
"""


def main():
    pages = {
        "index.html": page_index,
        "demographics.html": page_demographics,
        "economy.html": page_economy,
        "schools.html": page_schools,
        "property.html": page_property,
        "tenant.html": page_tenant,
        "model.html": page_model,
        "decision.html": page_decision,
        "risks.html": page_risks,
        "flagged.html": page_flagged,
        "sources.html": page_sources,
    }
    for name, fn in pages.items():
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as fh:
            fh.write(fn())

    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    with open(os.path.join(ROOT, "assets", "styles.css"), "w", encoding="utf-8") as fh:
        fh.write(CSS.strip() + "\n")
    with open(os.path.join(ROOT, "assets", "site.js"), "w", encoding="utf-8") as fh:
        fh.write(SITE_JS)
    with open(os.path.join(ROOT, "assets", "favicon.svg"), "w", encoding="utf-8") as fh:
        fh.write(FAVICON)
    with open(os.path.join(ROOT, ".nojekyll"), "w", encoding="utf-8") as fh:
        fh.write("")

    # machine-readable export for audit
    import json
    export = {
        "generated": ACCESSION_DATE,
        "note": "Published rows. Blank value = unverified or withheld; see status.",
        "counts": counts(),
        "sources": SOURCES,
        "records": ROWS,
    }
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    with open(os.path.join(ROOT, "data", "published-records.json"), "w", encoding="utf-8") as fh:
        json.dump(export, fh, indent=1, ensure_ascii=False)

    print(f"Built {len(pages)} pages, {len(ROWS)} rows, {len(SOURCES)} sources.")


if __name__ == "__main__":
    main()
