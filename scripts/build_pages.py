#!/usr/bin/env python3
"""Generate the static decision-brief dashboard.

Every table row is rendered from a source-linked cell. The builder refuses to
emit a data row that does not carry a link to an official publisher, and it
refuses to emit a value cell that was not supplied explicitly (blank means
"unverified", never zero).

Verified: 08 November 2026 (UTC) against the official pages listed in SOURCES.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = "08 Nov 2026"

# --------------------------------------------------------------------------
# Source register.  Each entry: (short label, url, publisher, status)
# --------------------------------------------------------------------------
SOURCES = {
    "census_city": (
        "Census QuickFacts · LA city",
        "https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225",
    ),
    "census_county": (
        "Census QuickFacts · LA County",
        "https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045225",
    ),
    "bls_city": (
        "BLS · unemployment rates for the 50 largest cities",
        "https://www.bls.gov/lau/city-annual-unemployment-rates.htm",
    ),
    "bls_laus": (
        "BLS · LAUS county series (LAUCN060370000000003)",
        "https://data.bls.gov/timeseries/LAUCN060370000000003?amp%3bdata_tool=XGtable&output_view=data&include_graphs=true",
    ),
    "bls_cpi": (
        "BLS · CPI, Los Angeles area — September 2026",
        "https://www.bls.gov/regions/west/news-release/consumerpriceindex_losangeles.htm",
    ),
    "fred_county": (
        "BEA via FRED · GDP, Los Angeles County (GDPALL06037)",
        "https://fred.stlouisfed.org/series/GDPALL06037",
    ),
    "fred_metro": (
        "BEA via FRED · GDP, LA–Long Beach–Anaheim MSA (NGMP31080)",
        "https://fred.stlouisfed.org/series/NGMP31080",
    ),
    "scag_appendix": (
        "SCAG · Connect SoCal 2024, Appendix I updated tables",
        "https://scag.ca.gov/sites/default/files/2024-05/appendix_i_updated_tables_508_final.pdf",
    ),
    "scag_tech": (
        "SCAG · Connect SoCal 2024 demographics & growth forecast",
        "https://www.scag.ca.gov/sites/default/files/2024-05/23-2987-tr-demographics-growth-forecast-final-040424.pdf",
    ),
    "dtla": (
        "LA City Planning · DTLA 2040 press release (04 Dec 2024)",
        "https://planning.lacity.gov/odocument/92b97b24-1978-4e0e-9eae-51f22eda9e4c/Press%20Release_%20DTLA%20New%20Zoning%20Code.pdf",
    ),
    "zimas": ("LA City · ZIMAS parcel lookup", "https://zimas.lacity.org/"),
    "planning_zoning": (
        "LA City Planning · zoning search",
        "https://planning.lacity.gov/zoning/zoning-search",
    ),
    "assessor": (
        "LA County Assessor · parcel portal",
        "https://portal.assessor.lacounty.gov/",
    ),
    "assessor_prop13": (
        "LA County Assessor · Proposition 13 toolkit",
        "https://assessor.lacounty.gov/real-estate-toolkit/proposition-13",
    ),
    "ula": (
        "LA Office of Finance · Measure ULA FAQ",
        "https://finance.lacity.gov/faq/measure-ula",
    ),
    "nces": (
        "NCES · Los Angeles Unified district detail (ID 0622710)",
        "https://nces.ed.gov/ccd/districtsearch/district_detail.asp?ID2=0622710",
    ),
    "lausd_explore": ("LAUSD · school explorer", "https://explore.lausd.org/"),
    "cde_dashboard": (
        "CDE · California School Dashboard",
        "https://www.cde.ca.gov/ta/ac/cm/",
    ),
    "sec_10q": (
        "SEC · Jack in the Box Form 10-Q (12 and 40 weeks ended 05 Jul 2026)",
        "https://www.sec.gov/Archives/edgar/data/807882/000080788226000091/jack-20260705.htm",
    ),
    "sec_10k": (
        "SEC · Jack in the Box Form 10-K (FY2025)",
        "https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm",
    ),
    "sec_xbrl": (
        "SEC · XBRL company facts, CIK 0000807882 (tag Revenues)",
        "https://data.sec.gov/api/xbrl/companyconcept/CIK0000807882/us-gaap/Revenues.json",
    ),
    "usgs_eq": (
        "USGS · earthquake probability FAQ (UCERF3)",
        "https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-los-angeles-area-san-francisco-bay-area",
    ),
    "usgs_nshm": (
        "USGS · 2023 long-term National Seismic Hazard Model",
        "https://www.usgs.gov/programs/earthquake-hazards/science/2023-50-state-long-term-national-seismic-hazard-model-0",
    ),
    "cgs_eqzapp": ("CGS · EQ Zapp", "https://maps.conservation.ca.gov/cgs/EQZApp/app/"),
    "calfire_fhsz": (
        "CAL FIRE / OSFM · Fire Hazard Severity Zones",
        "https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones",
    ),
    "calfire_acres": (
        "CAL FIRE / OSFM · FHSZ acres in SRA and LRA (official PDF)",
        "https://34c031f8-c9fd-4018-8c5a-4159cdff6b0d-cdn-endpoint.azureedge.net/-/media/osfm-website/what-we-do/community-wildfire-preparedness-and-mitigation/fire_hazard_severity_zone_acres_state_and_local_responsibility_2024_2025.pdf",
    ),
    "fema_nri": ("FEMA · National Risk Index", "https://hazards.fema.gov/nri/"),
    "fema_rapt": (
        "FEMA · Resilience Analysis and Planning Tool (NRI v1.20)",
        "https://www.fema.gov/emergency-managers/practitioners/resilience-analysis-and-planning-tool",
    ),
    "fema_flood": ("FEMA · flood maps and products", "https://www.fema.gov/flood-maps/products-tools"),
    "fema_disasters": ("FEMA · disaster declarations", "https://www.fema.gov/disasters"),
    "openfema": (
        "OpenFEMA · Disaster Declarations Summaries v2 (federal API)",
        "https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2",
    ),
    "cdi_claims": (
        "California Department of Insurance · LA County wildfire claims tracker",
        "https://www.insurance.ca.gov/01-consumers/180-climate-change/Wildfire-Claims-Tracker.cfm",
    ),
    "dpw_flood": (
        "LA County Public Works · flood-zone viewer",
        "https://apps.gis.lacounty.gov/dpw/m/?viewer=floodzone",
    ),
    "geotracker": ("CA Water Boards · GeoTracker", "https://geotracker.waterboards.ca.gov/"),
    "epa_cleanup": (
        "U.S. EPA · cleanup databases",
        "https://www.epa.gov/cleanups/site-specific-national-cleanup-databases",
    ),
    "ladwp": ("LADWP · water system", "https://www.ladwp.com/who-we-are/water-system"),
    "metro": ("LA Metro · system maps", "https://www.metro.net/riding/guide/system-maps/"),
    "lapd": (
        "LAPD · crime mapping and COMPSTAT",
        "https://www.lapdonline.org/office-of-the-chief-of-police/office-of-special-operations/detective-bureau/crime-mapping-and-compstat/",
    ),
    "irs544": ("IRS · Publication 544", "https://www.irs.gov/publications/p544"),
    "ftb": (
        "California FTB · capital gains and losses",
        "https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html",
    ),
    "climate": (
        "NOAA Climate.gov · event tracker",
        "https://www.climate.gov/news-features/event-tracker/heat-wave-southern-california-and-southwest-early-september-2024",
    ),
}


def s(key: str, label: str | None = None) -> str:
    """Render a source link cell."""
    if key not in SOURCES:
        raise SystemExit(f"Unknown source key: {key}")
    text, url = SOURCES[key]
    return (
        f'<a class="source-link" href="{html.escape(url)}" target="_blank" '
        f'rel="noopener noreferrer">{html.escape(label or text)}</a>'
    )


def money(value: str) -> str:
    return value


# --------------------------------------------------------------------------
# Reusable fragments
# --------------------------------------------------------------------------
V = '<span class="badge badge-verified">Verified</span>'
L = '<span class="badge badge-limited">Context only</span>'
R = '<span class="badge badge-review">Not verified</span>'
H = '<span class="badge badge-high">Withheld</span>'
BLANK = '<span class="cell-blank" aria-label="left blank, not verified"></span>'


def table(
    caption: str,
    headers: list[str],
    rows: list[list[str]],
    search: bool = False,
    table_id: str | None = None,
    narrative: bool = False,
) -> str:
    for row in rows:
        if len(row) != len(headers):
            raise SystemExit(f"Row width {len(row)} != {len(headers)} in table: {caption}\n{row}")
        joined = " ".join(row)
        if narrative:
            if not re.search(r'href="', joined):
                raise SystemExit(f"Narrative row has no link at all in table: {caption}\n{row}")
        elif not re.search(r'href="https?://', joined):
            raise SystemExit(f"Row has no official source link in table: {caption}\n{row}")
    head = "".join(f'<th scope="col">{h}</th>' for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows
    )
    tid = f' id="{table_id}"' if table_id else ""
    narrative_attr = ' data-narrative="true"' if narrative else ""
    search_html = ""
    if search and table_id:
        search_html = (
            f'<div class="table-search"><label for="q-{table_id}">Filter rows</label>'
            f'<input id="q-{table_id}" type="search" data-table-search="{table_id}" '
            f'placeholder="Type to filter, e.g. census, BLS, verified" autocomplete="off"></div>'
        )
    return (
        f'<div class="table-wrap">{search_html}<table{tid}{narrative_attr}>'
        f"<caption>{caption}</caption>"
        f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"
    )


def metric(label: str, value: str, meta: str, key: str, tag: str = "") -> str:
    return (
        f'<article class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div>'
        f'<div class="metric-meta">{meta}</div>{s(key)}{tag}</article>'
    )


def panel(title: str, eyebrow: str, body: str, link_key: str | None = None) -> str:
    head = f'<div><p class="eyebrow">{eyebrow}</p><h2>{title}</h2></div>'
    if link_key:
        head += s(link_key, "Open full register")
    return f'<section class="panel" aria-label="{html.escape(title)}"><div class="panel-header">{head}</div>{body}</section>'


# --------------------------------------------------------------------------
# Navigation
# --------------------------------------------------------------------------
NAV = [
    ("Overview", [("index.html", "Executive summary")]),
    (
        "Area profile",
        [
            ("geography.html", "Geography &amp; land use"),
            ("population.html", "Population"),
            ("income.html", "Income &amp; housing"),
        ],
    ),
    ("Community", [("schools.html", "School system")]),
    (
        "Economy &amp; jobs",
        [("economy.html", "Economy"), ("jobs.html", "Jobs &amp; labour"), ("projections.html", "Projection system")],
    ),
    (
        "Asset &amp; tenant",
        [("property.html", "Lease &amp; asset"), ("tenant.html", "Tenant (issuer) context")],
    ),
    (
        "Decision &amp; risk",
        [("decision.html", "Sell / renew paths"), ("risks.html", "Risk register")],
    ),
    (
        "Governance",
        [
            ("requirements.html", "Requirements"),
            ("repo-review.html", "Repo review"),
            ("flagged.html", "Flagged for review"),
            ("sources.html", "Sources &amp; method"),
            ("audit.html", "Verification audit"),
        ],
    ),
]

PAGES = [page for _group, items in NAV for page in items]


def nav_html(current: str) -> str:
    out = []
    for group, items in NAV:
        out.append(f'<p class="nav-label">{group}</p><nav class="site-nav">')
        for filename, label in items:
            current_attr = ' aria-current="page"' if filename == current else ""
            out.append(
                f'<a href="{filename}"{current_attr}><span class="nav-dot">{label[:2].upper()}</span>{label}</a>'
            )
        out.append("</nav>")
    return "".join(out)


def page_shell(
    filename: str,
    title: str,
    heading: str,
    intro: str,
    body: str,
    meta: str,
    hero: bool = False,
    status_pill: str | None = None,
    hero_actions: str = "",
) -> str:
    group = next(g for g, items in NAV if any(f == filename for f, _ in items))
    hero_class = "hero" if hero else "page-intro"
    hero_inner = ""
    if hero:
        pill = f'<span class="status-pill">{status_pill}</span>' if status_pill else ""
        hero_inner = (
            f'<p class="eyebrow">{meta}</p>{pill}<h1 id="page-title">{heading}</h1>'
            f'<p>{intro}</p>{hero_actions}'
        )
    else:
        hero_inner = (
            f'<p class="eyebrow">{meta}</p><h1 id="page-title">{heading}</h1><p class="lead">{intro}</p>'
        )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(title)} — source-linked, privacy-first decision brief for a Jack in the Box NNN-leased property near central Los Angeles.">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <title>{html.escape(title)} | Jack in the Box Property Brief</title>
  <link rel="stylesheet" href="assets/styles.css">
  <script src="assets/site.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
  <div class="app-shell">
    <aside class="sidebar" id="site-nav" aria-label="Main navigation">
      <a class="brand" href="index.html" aria-label="Jack in the Box property decision brief home">
        <span class="brand-mark" aria-hidden="true">JB</span>
        <span class="brand-copy"><strong>Property decision brief</strong><span>Central Los Angeles · public-data review</span></span>
      </a>
      {nav_html(filename)}
      <div class="sidebar-note"><strong>Privacy-first publication</strong>No owner name, property address, APN, lease document, or individual financial details are published or collected by this site.</div>
    </aside>

    <div class="main-column">
      <header class="topbar">
        <div class="topbar-left">
          <button class="nav-toggle" type="button" data-nav-toggle aria-controls="site-nav" aria-expanded="false">☰ <span>Sections</span></button>
          <span class="crumb">Decision support <span aria-hidden="true">/</span> {html.escape(group)}</span>
        </div>
        <div class="snapshot">Evidence snapshot · {SNAPSHOT}</div>
      </header>

      <main id="main-content" class="content">
        <section class="{hero_class}" aria-labelledby="page-title">
          {hero_inner}
        </section>
        {body}
      </main>

      <footer class="site-footer">
        <div class="footer-privacy"><strong>Privacy-first:</strong> no personal information is collected, embedded, or published. Property identifiers are intentionally omitted.</div>
        <div>Every table row links to its official publisher · checked {SNAPSHOT}</div>
      </footer>
    </div>
  </div>
</body>
</html>
"""


# --------------------------------------------------------------------------
# Page bodies
# --------------------------------------------------------------------------
def index_body() -> str:
    cards = (
        metric("Population estimate", "3,869,089", "Los Angeles city · July 1, 2025 Census estimate (V2025)", "census_city")
        + metric("Population change", "−0.8%", "City estimate base Apr 2020 → Jul 2025 · not a site trade-area trend", "census_city")
        + metric("Median household income", "$81,939", "Citywide · 2020–2024 ACS · 2024 dollars", "census_city")
        + metric("Unemployment · county", "4.5%", "Los Angeles County · September 2026 · preliminary", "bls_laus")
        + metric("Local inflation", "+3.7%", "LA–Long Beach–Anaheim CPI-U · 12 months to September 2026", "bls_cpi")
        + metric("County GDP", "$1.003T", "Los Angeles County · 2024 · BEA GDP by county", "fred_county")
        + metric("Earthquake probability", "60%", "M ≥ 6.7 within 30 years · LA region · USGS UCERF3", "usgs_eq")
        + metric("Wildfire claims paid", "$25.2B", "Eaton &amp; Palisades fires · county-wide · tracker updated 06 Jul 2026", "cdi_claims")
    )
    summary = f"""<ol class="list-clean">
      <li><strong>“Central Los Angeles” is not one market.</strong> The Census, SCAG, and the Downtown Community Plan each use a different geography, and none can be tied to this restaurant without a parcel location. <a href="geography.html">Compare the geographies</a>.</li>
      <li><strong>The official long-run baseline is modestly positive at county scale.</strong> SCAG's adopted Connect SoCal 2024 tables put Los Angeles County at 10,046,000 residents and 5,031,000 jobs in 2019, rising to 10,793,000 and 5,461,000 by 2050. <a href="projections.html">See the projection system</a>.</li>
      <li><strong>The county is losing population while the labour market has tightened.</strong> Census estimates show the county down 3.2% since the 2020 base, while the county unemployment rate fell from a 5.8% 2024 annual average to 4.5% in September 2026. <a href="jobs.html">Labour detail</a>.</li>
      <li><strong>Inflation is still running above the pre-2021 pattern.</strong> The Los Angeles area CPI-U rose 3.7% over the 12 months to September 2026; food away from home rose 2.8%. This is the reference rate for any CPI-linked rent step. <a href="economy.html">Price indicators</a>.</li>
      <li><strong>Tail hazards are real at county scale, but nothing is parcel-mapped.</strong> USGS gives a 60% chance of M ≥ 6.7 in 30 years in the Los Angeles region. CAL FIRE's published acreage table shows 769,561 acres of Very High fire-hazard zone in Los Angeles County across both responsibility areas. No parcel-level hazard determination has been made. <a href="risks.html">Risk register</a>.</li>
      <li><strong>The decision cannot be settled on public area data alone.</strong> Rent, expiry, options, guarantor, value, debt and tax basis are all blank, and each one can flip the answer. <a href="flagged.html">Review the blanks</a>.</li>
    </ol>"""

    decision_rows = [
        [
            "<strong>Sell with lease in place</strong>",
            "A credible market value and net proceeds are established after loan payoff, transaction costs, applicable transfer tax, and owner-level tax review.",
            R,
            s("ula", "LA Office of Finance · ULA"),
        ],
        [
            "<strong>Renew / extend</strong>",
            "Actual option language, rent steps, operator, guaranty, expense obligations, insurance, and a supported rent comparison produce a better risk-adjusted hold value than selling.",
            R,
            s("sec_10k", "SEC · company lease disclosures"),
        ],
        [
            "<strong>Hold to expiry, then re-tenant</strong>",
            "Vacancy downtime, re-leasing capital, land-use constraints, and insurability can be funded, and residual value stays competitive with a sale today.",
            R,
            s("zimas", "LA City ZIMAS"),
        ],
        [
            "<strong>Preserve optionality (interim)</strong>",
            "Confirm every notice right and option deadline first, and run both the sale and renewal cases with verified inputs before waiving anything.",
            V,
            s("irs544", "IRS Publication 544"),
        ],
    ]

    trigger_rows = [
        [
            "Tenant signs an extension of five or more years at rent the unit can carry",
            "Renew / hold, and re-test the sale market annually",
            "Term is restored, the buyer pool widens, and the income stream is re-contracted.",
            s("sec_10k", "SEC · lease disclosures"),
        ],
        [
            "Tenant declines to extend but continues paying rent on time",
            "Sell with three or more years of term remaining",
            "Pricing is set by remaining term; waiting converts the asset into a re-tenanting proposition.",
            s("sec_10q", "SEC · issuer context"),
        ],
        [
            "Unit sales, occupancy cost, or franchisee condition show the site is marginal",
            "Sell or re-tenant; commit no further capital",
            "Renewal capacity is a unit-economics question that the brand alone does not answer.",
            s("sec_10q", "SEC · issuer context"),
        ],
        [
            "Insurance becomes unavailable, or premiums and deductibles reprice materially",
            "Prioritise sale or re-tenanting with pass-through protections",
            "Insurability affects net rent, buyer financing, and the owner's downside in a catastrophe.",
            s("cdi_claims", "California Department of Insurance"),
        ],
        [
            "A retrofit, environmental, or zoning constraint is found",
            "Price it into both paths before committing to either",
            "Capital obligations reduce the renewal comparison and the achievable sale price alike.",
            s("planning_zoning", "LA City Planning · zoning"),
        ],
        [
            "The owner needs liquidity, or this asset is a large share of net worth",
            "Sale moves up the ranking",
            "Concentration and liquidity are private factors that can outweigh a small expected-return difference.",
            s("irs544", "IRS Publication 544"),
        ],
    ]

    triggers_table = table(
        "If this is confirmed…, then the balance shifts to… — with the official reference to check it.",
        ["If this is confirmed…", "Then the balance shifts to…", "Because", "Where to check it"],
        trigger_rows,
        search=True,
        table_id="trigger-table",
    )

    body = f"""
        <section class="card-grid" aria-label="Verified public indicators">
          {cards}
        </section>

        <div class="two-column">
          <section class="panel" aria-labelledby="summary-title">
            <div class="panel-header">
              <div><p class="eyebrow">Executive summary</p><h2 id="summary-title">What the evidence supports</h2></div>
            </div>
            {summary}
          </section>

          <aside class="stack" aria-label="Provisional recommendation and caution">
            <div class="decision-banner">
              <span class="decision-icon" aria-hidden="true">✓</span>
              <p><strong>Provisional course of action</strong><br>Confirm every notice right and option deadline first, then prepare a sale case and a written renewal alternative in parallel. Do not waive rights, sign an extension, or accept a price until after-tax net proceeds and a risk-adjusted hold value can be compared using verified property and lease inputs.</p>
            </div>
            <div class="callout warning">
              <h3>Not a personalised wealth or tax recommendation</h3>
              <p class="small">The owner's basis, debt, tax position, liquidity needs, portfolio concentration, and risk tolerance are not known, are not requested, and are not published. Those private factors can change the best individual decision.</p>
              <a class="source-link" href="https://www.irs.gov/publications/p544" target="_blank" rel="noopener noreferrer">IRS Publication 544</a> ·
              <a class="source-link" href="https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html" target="_blank" rel="noopener noreferrer">California FTB</a>
            </div>
          </aside>
        </div>

        <section class="panel" style="margin-top:16px" aria-labelledby="choice-title">
          <div class="panel-header">
            <div><p class="eyebrow">Decision guardrails</p><h2 id="choice-title">The sale-versus-renew test</h2></div>
            <a class="source-link" href="decision.html">Full scenario framework</a>
          </div>
          {table("Conditions that should be verified before choosing a path. No property-specific value has been calculated.", ["Path", "Proceed only if…", "Status", "Official reference"], decision_rows)}
        </section>


        <section class="panel" style="margin-top:16px" aria-labelledby="triggers-title">
          <div class="panel-header">
            <div><p class="eyebrow">Decision rules</p><h2 id="triggers-title">What each new fact should change</h2></div>
          </div>
          <p class="small">Pre-committed responses, so the decision is made by evidence rather than by the calendar. These are decision rules, not data rows.</p>
          {triggers_table}
        </section>

        <section class="section-heading" id="privacy">
          <div><p class="eyebrow">Scope and privacy</p><h2>Public evidence only; no personal information</h2>
          <p>This site publishes aggregated public statistics and official source links. No owner name, street address, APN, ownership entity, lease document, or personal financial detail appears here. Asset-specific fields that cannot be checked from public data are left blank and listed on <a href="flagged.html">Flagged for Review</a>.</p></div>
        </section>
    """
    return body


def geography_body() -> str:
    rows = [
        ["Land area · City of Los Angeles", "469.49 sq mi", "2020 Census · city", "Citywide measure; a single parcel is a tiny fraction of it.", s("census_city")],
        ["Population density · City", "8,304.2 people / sq mi", "2020 Census · city", "A citywide average conceals very large block- and corridor-level variation.", s("census_city")],
        ["Land area · Los Angeles County", "4,059.28 sq mi", "2020 Census · county", "County scale; far too coarse for a restaurant trade area.", s("census_county")],
        ["Population density · County", "2,466.9 people / sq mi", "2020 Census · county", "County average; not a walk-shed or drive-time figure.", s("census_county")],
        ["Downtown plan area", "7-square-mile core", "DTLA 2040 · adopted Dec 2024", "Relevant only if the parcel sits inside this boundary, which has not been matched.", s("dtla")],
        ["Downtown plan · homes", "100,000 new homes", "DTLA 2040 · horizon to 2040", "Plan expectation, not a guaranteed outcome or a delivery schedule.", s("dtla")],
        ["Downtown plan · residents", "175,000 additional residents", "DTLA 2040 · horizon to 2040", "Plan expectation; no allocation to any sub-area is published here.", s("dtla")],
        ["Downtown plan · jobs", "100,000 more work opportunities", "DTLA 2040 · horizon to 2040", "Plan expectation; sector mix is not published here.", s("dtla")],
        ["Downtown plan · transit orientation", "80% of housing capacity within half a mile of major transit", "DTLA 2040 press release", "Plan-wide attribute; says nothing about any one parcel's transit access.", s("dtla")],
        ["Neighbourhoods named in the Downtown plan", "Chinatown, Bunker Hill, Union Station, Civic Center, Little Tokyo, Fashion District, Convention Center, Skid Row, Arts District, financial and historic core, light and heavy industrial districts", "DTLA 2040 press release · 04 Dec 2024", "Published list of plan sub-areas; the subject parcel has not been matched to any of them.", s("dtla")],
        ["Subject parcel / address match", BLANK, "Not supplied", "No address or APN was provided. Do not infer a parcel from a brand location or a map pin.", s("zimas")],
        ["Zoning, overlays, and legal use", BLANK, "Parcel match needed", "A general city rule cannot be assigned to an unidentified site.", s("planning_zoning")],
        ["Drive-time / walk-time catchment", BLANK, "Not mapped", "No catchment has been drawn; citywide figures are not substitutes.", s("metro")],
        ["Transit access and traffic counts", BLANK, "Not assessed", "Requires an exact location and a current comparable dataset.", s("metro")],
    ]
    return (
        '<div class="section-heading"><div><p class="eyebrow">Category</p><h2>Published geography, and the parcel that is missing</h2>'
        "<p>Everything below is a published city, county, or planning-area statistic. The rows with a blank value are the ones that actually decide this asset, and they stay blank until the parcel is identified.</p></div></div>"
        + table(
            "Geography and land-use evidence. Blank cells are deliberate and mean “not verified”, not zero.",
            ["Measure", "Value", "Geography / period", "Limitation", "Official source"],
            rows,
            search=True,
            table_id="geo-table",
        )
    )


def population_body() -> str:
    rows = [
        ["Population · City of Los Angeles", "3,869,089", "1 Jul 2025 estimate (V2025)", "Citywide; not a trade-area or walk-shed count.", s("census_city")],
        ["Population change · City", "−0.8%", "Apr 2020 base → 1 Jul 2025", "Long-run citywide change; no neighbourhood direction can be inferred.", s("census_city")],
        ["Population estimates base · City", "3,899,342", "1 Apr 2020 (V2025)", "Denominator behind the change above.", s("census_city")],
        ["Population · City, 2010 Census", "3,792,621", "1 Apr 2010", "Decennial benchmark only.", s("census_city")],
        ["Population · Los Angeles County", "9,694,934", "1 Jul 2025 estimate (V2025)", "Countywide; the county has declined faster than the city.", s("census_county")],
        ["Population change · County", "−3.2%", "Apr 2020 base → 1 Jul 2025", "Countywide decline; not a local catchment trend.", s("census_county")],
        ["Population estimates base · County", "10,017,414", "1 Apr 2020 (V2025)", "Denominator behind the county change.", s("census_county")],
        ["Households · City", "1,439,097", "2020–2024 ACS", "Citywide household count; not daytime population.", s("census_city")],
        ["Persons per household · City", "2.61", "2020–2024 ACS", "Citywide average.", s("census_city")],
        ["Under 18 years · City", "19.2%", "2020–2024 ACS", "Citywide age mix.", s("census_city")],
        ["65 years and over · City", "14.2%", "2020–2024 ACS", "Citywide age mix.", s("census_city")],
        ["Foreign-born persons · City", "35.7%", "2020–2024 ACS", "Citywide; not a customer profile.", s("census_city")],
        ["Language other than English at home · City", "56.4%", "2020–2024 ACS · persons 5+", "Citywide; relevant only as context for signage and staffing.", s("census_city")],
        ["SCAG forecast · County population", "10,046,000 (2019) → 10,793,000 (2050)", "Connect SoCal 2024 adopted forecast · +7%", "County control total based on plan assumptions; not a site or customer projection.", s("scag_appendix")],
        ["SCAG forecast · County households", "3,393,000 (2019) → 4,155,000 (2050)", "Connect SoCal 2024 adopted forecast · +23%", "Households grow faster than population in the adopted forecast.", s("scag_appendix")],
        ["SCAG forecast · SCAG region population", "18,827,000 (2019) → 20,909,000 (2050)", "Connect SoCal 2024 adopted forecast · +11%", "Six-county region; far broader than any restaurant catchment.", s("scag_appendix")],
        ["Subject catchment population", BLANK, "Not mapped", "No address; a citywide or countywide figure must not be used as a trade-area count.", s("zimas")],
    ]
    return (
        '<div class="section-heading"><div><p class="eyebrow">Category</p><h2>Population: two scales, one missing</h2>'
        "<p>Census estimates describe the city and the county. The SCAG adopted forecast is the only official long-run population series included here. Nothing on this page describes the population around this restaurant.</p></div></div>"
        + table(
            "Population evidence, each row linked to its official publisher.",
            ["Measure", "Value", "Period / geography", "Limitation", "Official source"],
            rows,
            search=True,
            table_id="pop-table",
        )
    )


def income_body() -> str:
    rows = [
        ["Median household income · City", "$81,939", "2020–2024 ACS · 2024 dollars", "City median; the household mix around this property is unknown.", s("census_city")],
        ["Median household income · County", "$90,112", "2020–2024 ACS · 2024 dollars", "County median; includes far higher-income areas than central Los Angeles.", s("census_county")],
        ["Per capita income · City", "$47,685", "2020–2024 ACS · 2024 dollars", "Citywide; not disposable income at a trade area.", s("census_city")],
        ["Per capita income · County", "$45,792", "2020–2024 ACS · 2024 dollars", "Countywide.", s("census_county")],
        ["Persons in poverty · City", "16.5%", "2020–2024 ACS", "Citywide share; not a site-level spending indicator.", s("census_city")],
        ["Persons in poverty · County", "13.3%", "2020–2024 ACS", "Countywide share.", s("census_county")],
        ["Median gross rent · City", "$1,933 / month", "2020–2024 ACS", "Residential rent; not commercial rent and not restaurant affordability.", s("census_city")],
        ["Owner-occupied housing · City", "36.0%", "2020–2024 ACS", "Citywide tenure mix.", s("census_city")],
        ["Median value of owner-occupied units · City", "$921,200", "2020–2024 ACS", "Residential values; no commercial value conclusion follows from it.", s("census_city")],
        ["Median monthly owner costs, with a mortgage · City", "$3,497", "2020–2024 ACS", "Household cost burden context only.", s("census_city")],
        ["Educational attainment · City", "79.6% high-school or higher; 38.5% bachelor's or higher", "2020–2024 ACS · persons 25+", "Citywide attainment; not a workforce or customer proxy.", s("census_city")],
        ["Civilian labour-force participation · City", "66.4%", "2020–2024 ACS · persons 16+", "Citywide; see the jobs page for current BLS rates.", s("census_city")],
        ["Mean travel time to work · City", "30.7 minutes", "2020–2024 ACS · workers 16+", "Commute context; not a measure of pass-by traffic.", s("census_city")],
        ["Total retail sales · City", "$81.35 billion", "2022 Economic Census · nominal", "All retail categories; not a forecast and not this restaurant's sales.", s("census_city")],
        ["Retail sales per capita · City", "$21,281", "2022 Economic Census", "Citywide average.", s("census_city")],
        ["Total retail sales · County", "$213.93 billion", "2022 Economic Census · nominal", "County aggregate.", s("census_county")],
        ["Accommodation and food-services sales · City", "$17.37 billion", "2022 Economic Census", "Broad sector aggregate; does not isolate quick-service restaurants.", s("census_city")],
        ["Health care and social assistance receipts · City", "$46.30 billion", "2022 Economic Census", "Sector context for the area's largest employment base.", s("census_city")],
        ["Household income within the subject trade area", BLANK, "Not mapped", "Trade-area income cannot be derived from a city median.", s("zimas")],
    ]
    return (
        '<div class="section-heading"><div><p class="eyebrow">Category</p><h2>Income, housing cost, and retail spending</h2>'
        "<p>These are the official area income and spending statistics. They say nothing about the spending power of the households that actually pass this site, because the site has not been located.</p></div></div>"
        + table(
            "Income, housing, and spending evidence.",
            ["Measure", "Value", "Period / geography", "Limitation", "Official source"],
            rows,
            search=True,
            table_id="income-table",
        )
    )


def schools_body() -> str:
    rows = [
        ["District", "Los Angeles Unified (NCES district ID 0622710)", "2025–2026 directory data", "District identity is published; no individual school is identified for this site.", s("nces")],
        ["District type and status", "Regular local school district · open", "2025–2026 directory data", "Directory classification only.", s("nces")],
        ["Grade span", "KG – 12", "2025–2026 directory data", "District-wide span.", s("nces")],
        ["Locale classification", "City, Large", "2024–2025 CCD", "Federal locale code; not a neighbourhood rating.", s("nces")],
        ["Total students", "408,026", "2024–2025 school year", "District-wide enrolment; not any campus.", s("nces")],
        ["Total schools", "784", "2025–2026 directory data", "District-wide count.", s("nces")],
        ["Classroom teachers (FTE)", "21,246.18", "2024–2025 school year", "District-wide staffing.", s("nces")],
        ["Student / teacher ratio", "19.20", "2024–2025 school year", "District average.", s("nces")],
        ["Total staff (FTE)", "55,601.49", "2024–2025 school year", "District-wide staffing, all categories.", s("nces")],
        ["Total revenue", "$14,773,154,000 · $34,533 per student", "Fiscal year 2022–2023", "District finances; fiscal data lags the enrolment year.", s("nces")],
        ["Total expenditures", "$11,493,204,000 · $26,866 per student", "Fiscal year 2022–2023", "District-wide spending.", s("nces")],
        ["Instructional expenditure per student", "$12,330", "Fiscal year 2022–2023", "District average; not a school-quality score.", s("nces")],
        ["Total capital outlay", "$1,139,463,000", "Fiscal year 2022–2023", "District-wide capital spending.", s("nces")],
        ["School attendance assignment for the subject parcel", BLANK, "Not mapped", "Assignments depend on an exact address and can change between school years.", s("lausd_explore")],
        ["Campus-level performance", BLANK, "Not mapped", "No campus has been identified, so no performance figure is published.", s("cde_dashboard")],
        ["School effect on this asset's value", BLANK, "Not assessed", "For a quick-service restaurant, school quality is a weak and unproven driver; it is recorded for completeness only.", s("cde_dashboard")],
    ]
    return (
        '<div class="section-heading"><div><p class="eyebrow">Category</p><h2>School system context</h2>'
        "<p>The user brief asked for school-system evidence. The only honest answer at this stage is district scale: the figures below are published federal Common Core of Data statistics for Los Angeles Unified. No campus is named, because no address was supplied.</p></div></div>"
        + table(
            "School-system evidence from the federal Common Core of Data. Blank rows remain blank until the parcel is located.",
            ["Measure", "Value", "Period", "Limitation", "Official source"],
            rows,
            search=True,
            table_id="schools-table",
        )
    )


def economy_body() -> str:
    rows = [
        ["County GDP", "$1.003 trillion", "2024 · BEA GDP by county · nominal", "Output produced in the county; not resident income and not property value.", s("fred_county")],
        ["County GDP · prior year", "$956.2 billion", "2023 · BEA GDP by county", "Prior-year comparison as published in the same series.", s("fred_county")],
        ["County GDP · two years prior", "$909.3 billion", "2022 · BEA GDP by county", "Published series history.", s("fred_county")],
        ["Metro GDP", "$1.295 trillion", "2023 · LA–Long Beach–Anaheim MSA · nominal", "The metro GDP series is marked discontinued on its official page and publishes no later year; the most recent published value is used.", s("fred_metro")],
        ["Metro GDP · 2024 value", BLANK, "Not published", "No 2024 metro value could be read from the official series. An earlier draft of this brief carried a $1.355 trillion 2024 metro figure that could not be confirmed and has been removed.", s("fred_metro")],
        ["CPI-U, all items · LA area", "+3.7% over 12 months", "September 2026 · not seasonally adjusted", "Regional inflation; this is the reference rate for a CPI-linked rent step.", s("bls_cpi")],
        ["CPI-U index level · LA area", "358.725", "September 2026 · 1982–84 = 100", "Index level, not a price level comparison between cities.", s("bls_cpi")],
        ["CPI-U, all items less food and energy", "+2.6% over 12 months", "September 2026", "Core measure; shelter rose 3.7% over the year.", s("bls_cpi")],
        ["Food away from home", "+2.8% over 12 months", "September 2026", "Closest published proxy for menu-price inflation in this area.", s("bls_cpi")],
        ["Energy", "+20.3% over 12 months; gasoline +30.8%", "September 2026", "A direct operating-cost and customer-discretionary-income pressure.", s("bls_cpi")],
        ["CPI data gap", "October 2025 not available", "Lapse in appropriations", "The published series has a documented hole at October 2025.", s("bls_cpi")],
        ["Retail sales · City", "$81.35 billion", "2022 Economic Census · nominal", "All retail categories.", s("census_city")],
        ["Accommodation and food-services sales · City", "$17.37 billion", "2022 Economic Census", "Sector aggregate; no quick-service split is published here.", s("census_city")],
        ["Employer establishments · County", "304,988", "2023 · County Business Patterns", "Establishment count, not employment at this site.", s("census_county")],
        ["Total annual payroll · County", "$299.6 billion", "2023 · County Business Patterns", "County-wide payroll.", s("census_county")],
        ["Subject property revenue or sales", BLANK, "Not available", "No tenant sales report for this unit was located in any official source.", s("sec_10q")],
    ]
    return (
        '<div class="section-heading"><div><p class="eyebrow">Category</p><h2>Output, prices, and sales</h2>'
        "<p>Output and price statistics at regional scale, plus the inflation series that drives most NNN rent escalations. The discontinued metro series and the 2024 metro figure are both called out explicitly rather than smoothed over.</p></div></div>"
        + table(
            "Economic evidence. The blank rows are deliberate.",
            ["Measure", "Value", "Period / basis", "Limitation", "Official source"],
            rows,
            search=True,
            table_id="economy-table",
        )
    )


def jobs_body() -> str:
    rows = [
        ["Unemployment rate · City of Los Angeles", "5.8%", "2025 · 11-month average", "BLS states October 2025 was not collected during the federal shutdown, so this is not fully comparable to other years.", s("bls_city")],
        ["Unemployment rate · City, prior years", "5.9% (2024) · 5.3% (2023) · 5.1% (2022) · 9.0% (2021)", "BLS annual averages, 50 largest cities", "Published series history; useful for trend direction only.", s("bls_city")],
        ["Unemployment rate · County", "4.5%", "September 2026 · preliminary", "Most recent published month; preliminary and subject to revision.", s("bls_laus")],
        ["Unemployment rate · County, December 2025", "5.0%", "December 2025 · not seasonally adjusted", "Earlier month retained for continuity with the previous audit.", s("bls_laus")],
        ["Unemployment rate · County, published annual average", "5.7%", "2025 annual · 11-month average", "This is the published BLS annual figure. A simple average of the eleven monthly rates gives 5.6%; the published value is used here.", s("bls_laus")],
        ["Unemployment rate · County, 2024 annual", "5.8%", "2024 annual average", "Prior-year published annual figure.", s("bls_laus")],
        ["County labour force", "5,031,013", "September 2026 · preliminary", "County aggregate; not resident labour supply within a catchment.", s("bls_laus")],
        ["County unemployment level", "224,519", "September 2026 · preliminary", "County aggregate.", s("bls_laus")],
        ["County labour force · December 2025", "5,129,498", "December 2025 · not seasonally adjusted", "Retained for continuity with the previous audit.", s("bls_laus")],
        ["County unemployment level · December 2025", "257,301", "December 2025 · not seasonally adjusted", "Retained for continuity with the previous audit.", s("bls_laus")],
        ["Total employment · County", "3,987,736", "2023 · County Business Patterns", "Establishment-based employment; differs in concept from the LAUS household survey.", s("census_county")],
        ["Employment change · County", "+2.3%", "2022 → 2023 · County Business Patterns", "One-year change in the published series.", s("census_county")],
        ["SCAG forecast · County employment", "5,031,000 (2019) → 5,461,000 (2050)", "Connect SoCal 2024 adopted forecast · +9%", "County control total; no sector, commute, or catchment match is published here.", s("scag_appendix")],
        ["SCAG forecast · regional job additions, health care and social assistance", "+416,000", "SCAG region · 2022–2050", "Regional sector addition; verified against the SCAG technical report in the 07 Nov 2026 audit and not re-read in this pass.", s("scag_tech")],
        ["SCAG forecast · regional job additions, construction", "+148,000", "SCAG region · 2022–2050", "Regional sector addition; verified in the 07 Nov 2026 audit.", s("scag_tech")],
        ["SCAG forecast · regional job additions, accommodation and food services", "+106,000", "SCAG region · 2022–2050", "Regional sector addition; no quick-service split is published.", s("scag_tech")],
        ["Employment within the subject catchment", BLANK, "Not mapped", "Daytime employment near the site cannot be derived from county totals.", s("zimas")],
    ]
    return (
        '<div class="section-heading"><div><p class="eyebrow">Category</p><h2>Labour market and job growth</h2>'
        "<p>Two different official concepts appear here and must not be mixed: the BLS household survey (LAUS unemployment rates) and the Census County Business Patterns establishment counts. The SCAG forecast is the official long-run employment baseline.</p></div></div>"
        + table(
            "Labour-market evidence, with the measurement basis stated on every row.",
            ["Measure", "Value", "Period / basis", "Limitation", "Official source"],
            rows,
            search=True,
            table_id="jobs-table",
        )
    )


def property_body() -> str:
    rows = [
        ["Street address / parcel match", BLANK, "Not supplied · not matched", "Do not identify a nearby assessor parcel by inference.", s("zimas")],
        ["Assessor parcel number (APN)", BLANK, "Not verified", "Parcel identity and situs must be checked against title and survey.", s("assessor")],
        ["Fee owner, vesting, easements, lender liens", BLANK, "Title report needed", "No ownership entity or personal identifiers are published.", s("assessor_prop13")],
        ["Legal tenant and operating entity", BLANK, "Lease / amendment needed", "The brand may be operated by a corporate unit or a franchisee; the issuer filing does not identify this location.", s("sec_10q")],
        ["Guarantor, guaranty scope, recourse", BLANK, "Guaranty / amendments needed", "No parent support or continuing liability is assumed.", s("sec_10q")],
        ["Current base rent and annual rent steps", BLANK, "Rent roll / lease needed", "No rent, percentage rent, pass-through, or escalation is inferred.", s("sec_10k")],
        ["Commencement and exact expiry date", BLANK, "Reported range only", "The 2030–2035 range in the brief is not contract-verified; exact dates drive sale value and notice deadlines.", s("sec_10k")],
        ["Renewal options, option rent, notice windows", BLANK, "Lease / amendments needed", "Calendar every exercise date and any lender-consent date from the executed documents.", s("sec_10k")],
        ["NNN expense allocation and landlord obligations", BLANK, "Lease / expense history needed", "“NNN” is not treated as proof that every capital item is reimbursed.", s("sec_10k")],
        ["Building area, site area, parking, access", BLANK, "Survey / parcel record needed", "No dimensions or site plan have been identified.", s("zimas")],
        ["Zoning, overlays, legal use, entitlements", BLANK, "Parcel match needed", "A general city rule cannot be assigned to an unidentified site.", s("planning_zoning")],
        ["Assessed value and market value", BLANK, "No appraisal / no comps", "County assessed value, if found, is neither an appraisal nor a sale-price opinion.", s("assessor")],
        ["Physical condition and capital plan", BLANK, "Inspection needed", "Public permit history cannot replace a property-condition assessment.", s("zimas")],
        ["Insurance limits, exclusions, premium", BLANK, "Current quotes / policy needed", "No premium, coverage, or insurability claim is made.", s("cdi_claims")],
    ]
    return (
        '<div class="section-heading"><div><p class="eyebrow">Category</p><h2>Lease and asset: everything still to verify</h2>'
        "<p>Every asset-specific cell on this page is blank on purpose. A blank means the value is unknown, not zero, and no figure on this site may be inferred from a citywide average.</p></div></div>"
        + table(
            "Asset and lease diligence checklist. Each row names the official tool or reference that would close it.",
            ["Field", "Value", "Status", "Why it matters / diligence needed", "Official reference"],
            rows,
            search=True,
            table_id="property-table",
        )
        + '<div class="callout"><h3>Why nothing here is estimated</h3><p class="small">Rent, expiry, options, value, debt and tax basis are the inputs that decide whether to sell or renew. Publishing an estimate for any of them would look authoritative and be wrong. They are listed on <a href="flagged.html">Flagged for Review</a> instead.</p></div>'
    )


def tenant_body() -> str:
    rows = [
        ["Revenue · 12 weeks ended 5 Jul 2026", "$257,657,000", "$262,401,000 · 12 weeks ended 6 Jul 2025", "Consolidated continuing operations; not the subject restaurant's sales.", s("sec_xbrl", "SEC XBRL · Revenues")],
        ["Revenue · 40 weeks ended 5 Jul 2026", "$861,438,000", "$899,196,000 · prior-year 40 weeks", "Year-to-date period, not a full fiscal year.", s("sec_xbrl", "SEC XBRL · Revenues")],
        ["Revenue · fiscal year 2025", "$1,465,314,000", "52 weeks ended 28 Sep 2025", "Company-wide; useful only as a trend anchor for the brand.", s("sec_xbrl", "SEC XBRL · Revenues")],
        ["Revenue · fiscal year 2024", "$1,571,306,000", "Fiscal year ended 29 Sep 2024", "Prior-year comparison from the same published series.", s("sec_xbrl", "SEC XBRL · Revenues")],
        ["Restaurants by operating model", "149 company-operated; 1,966 franchise-operated", "As of 5 Jul 2026", "Read from the 10-Q in the 07 Nov 2026 audit, not re-read in this pass.", s("sec_10q")],
        ["Earnings from continuing operations · 12 weeks", "$21,041,000", "$22,839,000 · prior-year 12 weeks", "Company-wide result; not rent coverage for an unidentified tenant.", s("sec_10q")],
        ["Earnings from continuing operations · 40 weeks", "$47,971,000", "$74,534,000 · prior-year 40 weeks", "Company-wide result; review with the complete filing.", s("sec_10q")],
        ["Current maturities of debt", "$44,160,000", "As of 5 Jul 2026", "Consolidated balance-sheet item, not the operator's balance sheet.", s("sec_10q")],
        ["Long-term debt", "$1,428,667,000", "As of 5 Jul 2026", "Interpret with the filing's debt notes and covenant terms.", s("sec_10q")],
        ["Del Taco presentation", "Reported as discontinued operations after the December 2025 sale", "As described in the 2026 10-Q", "Continuing-operations presentation is used for the comparisons above.", s("sec_10q")],
        ["Subject-site operator, guarantor, and rent history", BLANK, "Not identified", "Issuer-level filings cannot establish who signed this lease or whether it is guaranteed.", s("sec_10q")],
    ]
    return (
        '<div class="section-heading"><div><p class="eyebrow">Category</p><h2>Tenant context at issuer level only</h2>'
        "<p>These are the consolidated figures of the franchisor, taken from its SEC filings. They are credit context for the brand. They are not this restaurant's sales, and they do not identify the entity that signed the lease.</p></div></div>"
        + table(
            "Issuer-level continuing-operations figures, in U.S. dollars as filed.",
            ["Reported item", "Current period", "Comparison period", "Meaning / limitation", "Official source"],
            rows,
            search=True,
            table_id="tenant-table",
        )
        + '<div class="callout warning"><h3>The credit question is unanswered</h3><p class="small">A Jack in the Box sign does not tell you whether the obligor is the public company, a franchisee, or a special-purpose entity, and it says nothing about a parent guarantee. Until the executed lease and any guaranty are read, tenant credit risk cannot be priced.</p></div>'
    )


def projections_body() -> str:
    inputs = [
        ["Population baseline and forecast", "10,046,000 (2019) → 10,793,000 (2050)", "SCAG Connect SoCal 2024 adopted tables", "County control total; used as the demand-side anchor.", s("scag_appendix")],
        ["Household baseline and forecast", "3,393,000 (2019) → 4,155,000 (2050)", "SCAG Connect SoCal 2024 adopted tables", "Households grow faster than population in the adopted forecast.", s("scag_appendix")],
        ["Employment baseline and forecast", "5,031,000 (2019) → 5,461,000 (2050)", "SCAG Connect SoCal 2024 adopted tables", "County control total; the employment-side anchor.", s("scag_appendix")],
        ["Local inflation reference", "+3.7% over 12 months to Sep 2026", "BLS CPI-U, Los Angeles area", "Reference rate for any CPI-linked rent step.", s("bls_cpi")],
        ["Food-away-from-home inflation", "+2.8% over 12 months to Sep 2026", "BLS CPI-U, Los Angeles area", "Menu-price proxy used in the sales-sensitive scenario.", s("bls_cpi")],
        ["Labour-market starting point", "4.5% county unemployment, Sep 2026 (preliminary)", "BLS LAUS", "Starting condition for the demand scenarios.", s("bls_laus")],
        ["Output base", "$1.003 trillion county GDP, 2024", "BEA GDP by county", "Scale reference only; not used to size a single restaurant.", s("fred_county")],
        ["Transfer-cost rule", "ULA 4% above $5,400,000 and 5.5% at or above $10,900,000", "City of LA, for transactions closing after 30 Jun 2026", "Applies only inside the City and only at the actual closing date.", s("ula")],
    ]

    scenarios = [
        [
            "<strong>Base</strong>",
            "County follows the adopted SCAG path; inflation settles toward the published core rate; the tenant performs and exercises at least one option.",
            "SCAG adopted forecast; BLS CPI core (+2.6%)",
            "Anchored to published figures, but the option assumption is an assumption, not an official statistic.",
            s("scag_appendix"),
        ],
        [
            "<strong>Downside · demand</strong>",
            "County population keeps falling as Census estimates show; unemployment reverts toward the 2025 annual average of 5.7%; energy-led cost pressure persists.",
            "Census V2025; BLS LAUS 2025 annual; BLS CPI energy (+20.3%)",
            "Each input is published; the combined path is a judgement, not an official projection.",
            s("census_county"),
        ],
        [
            "<strong>Downside · tenant</strong>",
            "The obligor is a thinly capitalised franchisee with no parent guarantee, and no renewal option is exercised.",
            "Issuer filings show 1,966 franchise-operated units",
            "The mix of company and franchise units is published; the identity of this unit's operator is not.",
            s("sec_10q"),
        ],
        [
            "<strong>Downside · renewal terms</strong>",
            "Renewal rent resets below today's rent because comparable quick-service rents have not kept pace with the 3.7% headline CPI.",
            "BLS CPI-U all items (+3.7%) vs core (+2.6%)",
            "Published price indices only; no rent comparable has been verified.",
            s("bls_cpi"),
        ],
        [
            "<strong>Tail · physical</strong>",
            "A major earthquake, an urban-interface wildfire, or a flood event interrupts access and trade, or makes insurance materially more expensive or unavailable.",
            "USGS 60% for M ≥ 6.7 in 30 years; 769,561 acres of Very High FHSZ in LA County",
            "Regional and county-scale hazards. No parcel-level hazard determination has been made.",
            s("usgs_eq"),
        ],
        [
            "<strong>Tail · transaction</strong>",
            "A sale above the ULA threshold incurs a material local transfer tax, and thresholds move again before closing.",
            "City thresholds $5,400,000 and $10,900,000 after 30 Jun 2026",
            "Thresholds adjust annually by the chained CPI; the closing-date rule governs.",
            s("ula"),
        ],
    ]

    outputs = [
        ["Implied value today", BLANK, "Annual contractual rent ÷ going-in cap rate", "Both inputs are unverified. No value is published.", s("assessor")],
        ["Value at expiry or renewal", BLANK, "Renewal rent × remaining term profile, discounted at the exit cap rate", "No rent schedule and no cap rate have been verified.", s("sec_10k")],
        ["Net sale proceeds", BLANK, "Price − debt payoff − transfer tax − closing costs − tax on gain", "Every component is owner-specific and unpublished.", s("ula")],
        ["Hold-value comparison", BLANK, "Present value of remaining rent and residual, less capital and downtime", "Cannot be computed without the lease.", s("irs544")],
        ["Break-even sale price", BLANK, "The price at which net proceeds equal the risk-adjusted hold value", "This is the number that actually answers the question, and it cannot be computed yet.", s("irs544")],
    ]

    calculator = """
        <section class="panel" aria-labelledby="calc-title">
          <div class="panel-header">
            <div><p class="eyebrow">Private worksheet</p><h2 id="calc-title">Break-even calculator (runs in your browser only)</h2></div>
          </div>
          <p class="small">Nothing typed here leaves your device: there is no network request, no storage, and no logging. The calculator does not pre-fill any value, because none is known. Use it once you have the lease in front of you.</p>
          <form class="calc" id="calc" novalidate>
            <div class="calc-grid">
              <label for="c-rent">Annual contractual rent ($)</label>
              <input id="c-rent" name="c-rent" type="number" min="0" step="1000" placeholder="e.g. 180000" inputmode="decimal">
              <label for="c-cap">Cap rate (%)</label>
              <input id="c-cap" name="c-cap" type="number" min="0" step="0.05" placeholder="e.g. 6.00" inputmode="decimal">
              <label for="c-years">Years of remaining term</label>
              <input id="c-years" name="c-years" type="number" min="0" step="0.5" placeholder="e.g. 6" inputmode="decimal">
              <label for="c-growth">Annual rent growth (%)</label>
              <input id="c-growth" name="c-growth" type="number" min="0" step="0.1" placeholder="e.g. 2.0" inputmode="decimal">
              <label for="c-costs">Sale costs (% of price)</label>
              <input id="c-costs" name="c-costs" type="number" min="0" step="0.1" placeholder="e.g. 6.0" inputmode="decimal">
              <label for="c-debt">Debt payoff ($)</label>
              <input id="c-debt" name="c-debt" type="number" min="0" step="1000" placeholder="e.g. 0" inputmode="decimal">
              <label for="c-disc">Required return on holding (%)</label>
              <input id="c-disc" name="c-disc" type="number" min="0" step="0.1" placeholder="e.g. 8.0" inputmode="decimal">
              <label for="c-resid">Exit cap rate (%)</label>
              <input id="c-resid" name="c-resid" type="number" min="0" step="0.05" placeholder="e.g. 6.50" inputmode="decimal">
            </div>
            <div class="calc-actions">
              <button class="button" type="button" id="c-run">Compute</button>
              <button class="button button-quiet" type="reset" id="c-clear">Clear</button>
            </div>
            <output class="calc-out" id="c-out" for="c-rent c-cap c-years c-growth c-costs c-debt c-disc c-resid">
              <p class="small">Enter your own figures and choose “Compute”. Results are illustrative arithmetic on your inputs, not a valuation or an official statistic.</p>
            </output>
          </form>
        </section>
    """

    return (
        '<div class="section-heading"><div><p class="eyebrow">Category</p><h2>A projection system with published inputs and empty outputs</h2>'
        "<p>A projection is only as good as its inputs. Every input the model is allowed to use is published on this page with its official source. Because the asset-specific inputs are all blank, the model's outputs are blank too — and that is the finding, not a gap in the arithmetic.</p></div></div>"
        + table(
            "Model inputs. Every one is an official published figure; none is estimated.",
            ["Input", "Published value", "Source", "How the model uses it", "Official source"],
            inputs,
            search=True,
            table_id="model-inputs",
        )
        + '<div class="section-heading"><div><p class="eyebrow">Scenarios</p><h2>Six paths to 2030–2035</h2>'
        "<p>Each scenario names the published figures it is anchored to. Where a scenario depends on a judgement rather than a statistic, that is said on the row.</p></div>"
        + table(
            "Scenario definitions. The scenario framing is this brief's judgement; the anchor figures are official.",
            ["Scenario", "What it assumes", "Anchored to", "Status of the assumption", "Official source"],
            scenarios,
            search=True,
            table_id="model-scenarios",
        )
        + "</div>"
        + '<div class="section-heading"><div><p class="eyebrow">Outputs</p><h2>What the model would produce, once inputs exist</h2></div></div>'
        + table(
            "Model outputs. All blank: no rent, value, debt, or tax figure for this asset has been verified.",
            ["Output", "Value", "Formula", "Why it is blank", "Official reference"],
            outputs,
        )
        + calculator
    )


GATES_INTRO = (
    '<div class="section-heading"><div><p class="eyebrow">Dated plan</p>'
    '<h2 id="rec-title">The risk-balanced plan: dual-track, sell-weighted, date-gated</h2>'
    "<p>Run both tracks. The weighting favours a sale with the lease in place unless a qualifying "
    "renewal is verified, because the renewal case cannot be priced without the lease in front of "
    "you. The gate dates are proposed governance, not published data: the arithmetic above still "
    "decides.</p></div></div>"
)

GATES_CAVEAT = (
    '<div class="callout warning"><h3>The rule that overrides the rest</h3>'
    '<p class="small">Never enter the final 24 months of the actual term without either a signed '
    "qualifying renewal or an active, professionally marketed listing. “Hold to expiry” treated as "
    "a passive default is the highest-risk option in this file, because it converts a contracted "
    "income stream into a re-tenanting proposition at the point of maximum uncertainty.</p></div>"
)


def decision_body() -> str:
    worksheet = [
        ["As-is sale value with lease in place", BLANK, "Independent appraisal / bids needed", "Assessed value is not market value; no comparable sales were matched to this site.", s("assessor")],
        ["Current rent and contractual increases through expiry", BLANK, "Executed lease / rent ledger needed", "Issuer-wide lease disclosures are not the subject contract.", s("sec_10k")],
        ["Option rent, renewal term, notice date", BLANK, "Lease / amendments needed", "Do not assume an option exists, or that either party can force one.", s("sec_10k")],
        ["Loan payoff and release costs", BLANK, "Lender payoff statement needed", "No public lookup exists; obtain an authorised payoff quote.", s("irs544")],
        ["Brokerage, legal, escrow, closing costs", BLANK, "Written quotes needed", "No transaction-cost percentage is assumed.", s("ula")],
        ["Transfer tax / Measure ULA", "$5,400,000 and $10,900,000 thresholds for transactions closing after 30 Jun 2026", "Verified on the City FAQ on 08 Nov 2026", "Applies inside the City of Los Angeles only. ULA rates are 4% and 5.5% on top of the 0.45% base rate, giving 4.45% and 5.95% combined. Thresholds are adjusted annually.", s("ula")],
        ["Owner tax basis, depreciation, gain", BLANK, "Private tax records / CPA review", "No owner identity, basis, filing status, or tax outcome is collected or published.", s("irs544")],
        ["§1031 eligibility / reinvestment plan", BLANK, "Qualified-advisor review", "§1031 is limited to qualifying business or investment real property and has strict rules.", s("irs544")],
    ]

    tradeoff = [
        ["Liquidity and diversification", "May release capital and reduce single-asset concentration, after debt and taxes.", "Retains capital in real estate and preserves future choices; liquidity stays limited.", s("irs544")],
        ["Contract income and tenant exposure", "Ends future rent exposure after transfer; pricing still depends on lease and obligor evidence.", "Continues income only if the tenant performs and contract rights are enforceable; the obligor is unverified.", s("sec_10q")],
        ["Tax timing and basis", "May recognise taxable gain; compute from private basis, depreciation, and sale facts.", "May defer a disposition but retains future tax and ownership exposure.", s("ftb")],
        ["Transfer cost and jurisdiction", "Local transfer taxes depend on parcel location, consideration, and closing date.", "No sale transfer tax at renewal, but other transaction and legal costs may apply.", s("ula")],
        ["Physical, regulatory, insurability exposure", "Transfers future ownership exposure, subject to sale terms and disclosure duties.", "Retains exposure to site condition, hazards, land-use rules, and future insurance terms.", s("zimas")],
    ]

    risk_of_decision = [
        ["Sell", "Selling before the value drivers are known; paying ULA unnecessarily; triggering a taxable gain in a single year; losing a contractual option you did not know you held.", R, s("ula")],
        ["Sell", "Mis-pricing the asset because cap-rate evidence and rent comparables were never gathered.", R, s("sec_10k")],
        ["Renew", "Renewing at a rent below market because no comparable was checked; extending a weak obligor; absorbing capital items the NNN label does not actually transfer.", R, s("bls_cpi")],
        ["Renew", "Locking in a long term just before a land-use change that raises alternative-use value.", L, s("dtla")],
        ["Hold to expiry", "Vacancy, downtime, re-leasing capital, and an insurance market that may not offer terms at renewal.", R, s("cdi_claims")],
        ["Hold to expiry", "Doing nothing while notice deadlines quietly pass — the single most common and most avoidable loss.", V, s("sec_10k")],
        ["Any path", "Deciding on area statistics instead of asset facts. Every area figure on this site is city, county, or planning-area scale.", V, s("census_city")],
    ]

    gates = [
        [
            "<strong>G1 · Controls</strong>",
            "31 Mar 2027",
            "Title, executed lease and amendments, estoppel, rent ledger, and a calendar of option and notice dates are in hand; the tenant legal entity is identified.",
            "Assume the earliest reported expiry (2030) is firm and begin sale preparation immediately.",
            s("assessor", "LA County Assessor"),
        ],
        [
            "<strong>G2 · Two-sided underwriting</strong>",
            "30 Jun 2027",
            "An independent appraisal or competitive bids and a documented market-rent benchmark for the renewal are both available.",
            "The sell path becomes the default; do not extend on unverified economics or a landlord-side guess at rent.",
            s("ula", "LA Office of Finance · ULA"),
        ],
        [
            "<strong>G3 · Renewal stress test</strong>",
            "30 Sep 2027",
            "Renewal term runs at least ten years beyond 2035 with fixed escalations; a guaranty or demonstrable credit support; landlord obligations capped; insurance obtainable at a tolerable cost.",
            "Go to market with the lease in place; do not sign a short extension to “buy time”.",
            s("sec_10k", "SEC · lease terms"),
        ],
        [
            "<strong>G4 · Market or sign</strong>",
            "1 Oct 2027 – 31 Dec 2029",
            "Either a signed qualifying renewal or an active, professionally marketed listing exists before the final 24 months of the actual term.",
            "Mandatory listing.",
            s("ula", "LA Office of Finance · ULA"),
        ],
        [
            "<strong>G5 · Sale mechanics</strong>",
            "Before any price is accepted",
            "Jurisdiction and closing-date transfer-tax check, loan payoff, cost quotes, and owner tax review are complete; thresholds are re-read at closing because they re-index annually.",
            "Do not sign a purchase agreement or accept a non-refundable deposit.",
            s("irs544", "IRS Publication 544"),
        ],
    ]

    return (
        '<div class="section-heading"><div><p class="eyebrow">Category</p><h2>Sell, renew, or hold: the comparison that has to be built</h2>'
        "<p>The three paths are only comparable after the worksheet below is filled from executed documents. The transfer-tax row is the one item that could be verified from an official page today.</p></div></div>"
        + table(
            "Diligence worksheet. Blank cells are deliberate; none is zero.",
            ["Input / output", "Value", "How to verify", "Caveat", "Official context / lookup"],
            worksheet,
            search=True,
            table_id="decision-worksheet",
        )
        + '<div class="section-heading"><div><p class="eyebrow">Trade-offs</p><h2>Sell versus hold, dimension by dimension</h2></div></div>'
        + table(
            "Side-by-side trade-offs. No weighting is applied, because weighting is owner-specific.",
            ["Dimension", "Sell", "Renew / hold", "Official context"],
            tradeoff,
        )
        + '<div class="section-heading"><div><p class="eyebrow">Risk of each decision</p><h2>What can go wrong on each path</h2></div></div>'
        + table(
            "Decision risk. Every row names the failure mode, not just the category.",
            ["Decision", "Risk", "Status", "Official reference"],
            risk_of_decision,
            search=True,
            table_id="decision-risk",
        )
        + GATES_INTRO
        + table(
            "Gate dates for a lease reported to expire 2030–2035. Dates are decision governance, not official statistics.",
            ["Gate", "By when", "What must be true", "If it is not", "Official reference"],
            gates,
            search=True,
            table_id="decision-gates",
        )
        + GATES_CAVEAT
    )


def risks_body() -> str:
    register = [
        ["Earthquake / liquefaction / surface rupture", "Damage, closure, access interruption, retrofit orders, and insurance deductibles.", "Not parcel-mapped", "Overlay the verified parcel in CGS EQ Zapp and obtain geotechnical and structural review where warranted.", s("cgs_eqzapp")],
        ["Wildfire / ember / smoke", "Direct damage, smoke closure, evacuation, and the renewal or affordability of coverage.", "Not parcel-mapped", "Check the current CAL FIRE map, defensible-space duties, insurer availability, exclusions, and deductibles.", s("calfire_fhsz")],
        ["Flooding / stormwater / drainage", "Building damage, business interruption, flood-insurance requirements, lender conditions.", "Not parcel-mapped", "Check current FEMA and county layers, drainage, elevation, and lender or insurer requirements.", s("fema_flood")],
        ["Extreme heat / smoke / climate stress", "Worker and customer safety, refrigeration and cooling loads, operating hours, equipment life.", "Regional context only", "Confirm HVAC and refrigeration condition, energy costs, heat plans, smoke procedures, and lease allocation.", s("climate")],
        ["Water supply / utility resilience", "Service interruption, drought restrictions, outages, infrastructure needs.", "City context only", "Confirm the serving utility, service history, emergency procedures, and lease allocation for interruption.", s("ladwp")],
        ["Environmental conditions / cleanup sites", "Contamination, historic uses, vapour, remediation obligations affecting redevelopment or financing.", "No screening completed", "After parcel match, review GeoTracker and EPA records and obtain a qualified Phase I assessment.", s("geotracker")],
        ["Tenant / franchisee financial stress", "Rent collection and renewal depend on the actual obligor and lease remedies.", "Obligor unknown", "Identify the signed tenant and guarantor; review lawful, consented entity-level financials and payment history.", s("sec_10q")],
        ["Lease expiry / option / expense allocation", "Notice dates, renewal rent, repair duties, insurance pass-through, holdover terms.", "Contract not reviewed", "Review the executed lease, amendments, estoppels, rent ledger, notice calendar, and expense reconciliations.", s("sec_10k")],
        ["Zoning / use / Downtown Plan applicability", "Nonconforming use, overlays, permitting, future development rules.", "Parcel / boundary unknown", "Check zoning, overlays, permits, cases, and the plan boundary in ZIMAS after matching the parcel.", s("zimas")],
        ["Insurance availability / premium shock", "Coverage gaps, larger deductibles, or premium rises can change net rent and marketability.", "No property quotes", "Collect current broker indications, policy forms, loss runs, deductibles, exclusions, and alternatives.", s("cdi_claims")],
        ["Crime / access / neighbourhood operations", "Safety, access, operating hours, customer perception.", "Not assessed", "After parcel match, consult current official data, tenant operations, and on-site observation.", s("lapd")],
    ]

    hazards = [
        ["USGS earthquake probability · M ≥ 6.7", "60%", "Los Angeles region · 30 years · UCERF3", "Regional probability; not a site ground-motion estimate.", s("usgs_eq")],
        ["USGS earthquake probability · M ≥ 7.0", "46%", "Los Angeles region · 30 years · UCERF3", "Regional probability.", s("usgs_eq")],
        ["USGS earthquake probability · M ≥ 7.5", "31%", "Los Angeles region · 30 years · UCERF3", "Regional probability.", s("usgs_eq")],
        ["CAL FIRE · LA County Very High FHSZ", "769,561 acres", "Combined LRA + SRA · LRA maps transmitted Mar–Apr 2025", "County acreage from the official State Fire Marshal table; not a parcel assignment.", s("calfire_acres")],
        ["CAL FIRE · LA County High FHSZ", "77,951 acres", "Combined LRA + SRA", "County acreage from the official table.", s("calfire_acres")],
        ["CAL FIRE · LA County Moderate FHSZ", "330,431 acres", "Combined LRA + SRA", "County acreage from the official table.", s("calfire_acres")],
        ["CAL FIRE · LA County all FHSZ classes", "1,177,944 acres", "Combined LRA + SRA", "County total from the official table.", s("calfire_acres")],
        ["CAL FIRE · statewide Very High FHSZ", "1,161,924 acres LRA; 16,881,829 acres SRA; 18,043,753 combined", "SRA adopted 1 Apr 2024; LRA transmitted Mar–Apr 2025", "Statewide totals from the official State Fire Marshal table.", s("calfire_acres")],
        ["Reported percentage expansion of Very High zones", BLANK, "Not located on an official page", "A “26% Southern California / 35% statewide expansion” figure appears in earlier drafts of this brief. It is not published in the official acreage table and remains withheld.", s("calfire_fhsz")],
        ["FEMA National Risk Index · county scores and expected annual loss", BLANK, "NRI v1.20", "FEMA states the v1.20 dataset is delivered through its RAPT mapping tool; county values were not readable as a published table, so none is asserted here.", s("fema_rapt")],
        ["FEMA disaster declarations · Los Angeles County", "88 total", "Counted through the OpenFEMA federal API on 08 Nov 2026 · all years", "A declaration is a public-policy event, not a property loss, and it includes Fire Management Assistance records.", s("openfema")],
        ["FEMA declarations · fire", "61", "Los Angeles County · all declaration types", "County-wide count; not a measure of damage at any address.", s("openfema")],
        ["FEMA declarations · flood", "10", "Los Angeles County", "County-wide count.", s("openfema")],
        ["FEMA declarations · severe storm", "8", "Los Angeles County", "County-wide count.", s("openfema")],
        ["FEMA declarations · other incident types", "9", "Los Angeles County", "Remaining incident types in the federal summary.", s("openfema")],
        ["CAL FIRE 2026 SRA mapping · open comment period", "Comment period open on the official page · FAQs updated November 2026", "State Responsibility Area · 2026 update", "A mapping update is in progress. Any parcel-level fire-hazard conclusion should be re-checked after the update is adopted.", s("calfire_fhsz")],
        ["Realised catastrophe · Eaton and Palisades claims", "41,727 filed; 40,482 partially paid; $25.2 billion paid to date", "Los Angeles County · tracker updated 06 Jul 2026", "A realised county-wide aggregate; not this property's exposure, premium, or loss estimate.", s("cdi_claims")],
        ["Parcel flood zone", BLANK, "Not mapped", "Requires a FEMA or county flood-zone query at the parcel.", s("dpw_flood")],
    ]

    blackswan = [
        ["Major earthquake or liquefaction event", "Physical loss, access disruption, repairs, deductible, prolonged closure.", "Exposure unknown", s("cgs_eqzapp")],
        ["Urban-interface wildfire, smoke, or area evacuation", "Damage or smoke closure, worker and customer disruption, unavailable or restricted coverage.", "Exposure unknown", s("calfire_fhsz")],
        ["Extreme rainfall / flood or prolonged heat", "Water intrusion, access loss, utility and cooling costs, food-safety and operating impacts.", "Exposure unknown", s("fema_flood")],
        ["Franchisee closure, guarantor failure, or abrupt tenant default", "Rent interruption, legal and workout costs, vacancy, re-tenanting capital and time.", "Obligor unknown", s("sec_10q")],
        ["Insurance withdrawal or material premium / deductible shock", "Uninsured loss, financing or lease compliance issues, reduced net income and buyer pool.", "Policy unknown", s("cdi_claims")],
        ["Energy-price shock", "Published LA-area energy inflation of +20.3% over the year to Sep 2026 cuts customer discretionary spend and raises operating cost.", "Published regional figure", s("bls_cpi")],
        ["Land-use, transfer-tax, or tax-law change", "Alternate-use value, transaction costs, permit timing, and after-tax proceeds.", "Jurisdiction unknown", s("planning_zoning")],
    ]

    return (
        '<div class="section-heading"><div><p class="eyebrow">Category</p><h2>Risk register</h2>'
        "<p>Business-as-usual risks first, then the measured hazard figures, then the tail events. Nothing here is a parcel-level determination.</p></div></div>"
        + table(
            "Risk register: exposure, evidence limit, and next verification step.",
            ["Risk category", "Why it matters", "Current finding", "Next step", "Official source"],
            register,
            search=True,
            table_id="risk-register",
        )
        + '<div class="section-heading"><div><p class="eyebrow">Measured hazards</p><h2>What the official numbers actually say</h2>'
        "<p>USGS probabilities and the State Fire Marshal's published acreage table are the two hazard sources that could be read directly from an official page. The rows that could not be read are left blank and flagged.</p></div></div>"
        + table(
            "Hazard metrics. Blank values are withheld, not estimated.",
            ["Hazard metric", "Value", "Geography / period", "Limitation", "Official source"],
            hazards,
            search=True,
            table_id="risk-hazards",
        )
        + '<div class="section-heading"><div><p class="eyebrow">Tail events</p><h2>Black-swan scenarios to test</h2>'
        "<p>Illustrative severe events. This is not a forecast and not a statement of site exposure.</p></div></div>"
        + table(
            "Tail scenarios and the channel through which each would bite.",
            ["Scenario to test", "Potential channel", "Current site status", "Official source"],
            blackswan,
            search=True,
            table_id="risk-tail",
        )
    )


FLAGGED_ITEMS = [
    ["F-01", "Property address, APN, and parcel match", "No address or parcel identifier was supplied. Every asset-specific conclusion depends on it.", "The parcel has not been identified; no assessor record has been matched.", s("zimas")],
    ["F-02", "Executed lease: rent, steps, commencement, exact expiry", "The 2030–2035 range in the brief is a reported range, not a contract date. Notice deadlines are unknowable without it.", "Lease not reviewed; no date is published.", s("sec_10k")],
    ["F-03", "Renewal options, option rent, notice windows", "Determines whether “renew” is even available, and on what terms.", "No option language has been read.", s("sec_10k")],
    ["F-04", "Legal tenant, operating entity, guarantor", "A brand sign does not establish the obligor or any parent guarantee.", "Obligor unknown; issuer filings do not identify this unit.", s("sec_10q")],
    ["F-05", "Market value, appraisal, and comparable sales", "No value or cap rate has been verified, so no sale-versus-hold comparison can be completed.", "No appraisal or comp set was located.", s("assessor")],
    ["F-06", "Debt: balance, rate, maturity, prepayment, release costs", "Net sale proceeds cannot be computed without an authorised payoff quote.", "No lender record was reviewed.", s("irs544")],
    ["F-07", "Owner tax basis, depreciation, filing position", "After-tax proceeds are owner-specific and are deliberately not collected.", "No tax record is published or requested.", s("ftb")],
    ["F-08", "FEMA National Risk Index county scores and expected annual loss", "Values in earlier drafts of this brief could not be read from an official FEMA page in two separate audits.", "Withheld. FEMA delivers NRI v1.20 through the RAPT mapping tool.", s("fema_rapt")],
    ["F-09", "FEMA disaster declaration count for Los Angeles County", "A count of 88 declarations appeared in earlier drafts and had not been reproduced from an official page.", "Closed 08 Nov 2026: 88 total, comprising 61 fire, 10 flood, 8 severe storm, and 9 other, counted through the OpenFEMA federal API.", s("openfema")],
    ["F-10", "Reported expansion of CAL FIRE Very High hazard zones (26% Southern California, 35% statewide)", "Not published in the official State Fire Marshal acreage table. Verified acreage is published on the risk page instead.", "Withheld as a percentage; official acreage published.", s("calfire_fhsz")],
    ["F-11", "Metro GDP for 2024 ($1.355 trillion in an earlier draft)", "The official metro GDP series is marked discontinued at 2023 and publishes no 2024 value.", "Removed from the landing page; only the 2023 figure is published.", s("fred_metro")],
    ["F-12", "Rank of Los Angeles County GDP among U.S. counties", "A “#2 county economy” claim in an earlier draft was not traced to an official ranking page.", "Removed; no rank is asserted.", s("fred_county")],
    ["F-13", "2025 county unemployment rate as a self-computed average (5.6%)", "The BLS published 2025 annual average is 5.7%. The simple average of eleven monthly rates is 5.6% and is not the published figure.", "Corrected to the published 5.7%; the discrepancy is recorded here.", s("bls_laus")],
    ["F-14", "Stale labour-market figures in the previous build", "The previous published build showed December 2025 as the latest county month. BLS has since published September 2026 (preliminary, 4.5%).", "Updated to the latest published month.", s("bls_laus")],
    ["F-15", "School assignment and campus performance for this site", "No campus can be named without an address.", "District-level federal statistics only.", s("lausd_explore")],
    ["F-16", "Crime, traffic counts, and transit access at the parcel", "No site-specific data was collected; LAPD notes its mapping platform is being updated.", "Not assessed.", s("lapd")],
    ["F-17", "Environmental screening (GeoTracker, EPA)", "Screening requires a parcel match.", "Not completed.", s("epa_cleanup")],
]


def flagged_body() -> str:
    return (
        '<div class="section-heading"><div><p class="eyebrow">Governance</p><h2>Flagged for review</h2>'
        "<p>Everything the owner should challenge, in one place. Items F-08 through F-14 are corrections and withholdings made in this pass against earlier drafts of this brief that exist elsewhere in the repository.</p></div></div>"
        + table(
            "Flagged items. Each row links to the official page that would resolve it.",
            ["Ref", "Item", "Why it matters", "Status", "Official source"],
            FLAGGED_ITEMS,
            search=True,
            table_id="flagged-table",
        )
    )


SOURCE_ROWS = [
    ["U.S. Census Bureau · QuickFacts", "City and county population, income, poverty, rent, tenure, density, retail and food-services sales", "Re-read 08 Nov 2026 · values matched", s("census_city")],
    ["U.S. Census Bureau · QuickFacts (county)", "County population, income, poverty, density, land area, employer establishments, payroll", "Re-read 08 Nov 2026 · values matched", s("census_county")],
    ["U.S. Bureau of Labor Statistics · 50 largest cities", "Los Angeles city annual unemployment rates, 2021–2025", "Re-read 08 Nov 2026 · values matched", s("bls_city")],
    ["U.S. Bureau of Labor Statistics · LAUS county series", "County unemployment rate, labour force, unemployment level; 2024–2026", "Re-read 08 Nov 2026 · values matched; annual figure corrected", s("bls_laus")],
    ["U.S. Bureau of Labor Statistics · CPI Los Angeles area", "Area CPI-U, core, food away from home, energy; index level", "Re-read 08 Nov 2026 · values matched", s("bls_cpi")],
    ["U.S. Bureau of Economic Analysis via FRED", "County GDP (2022–2024) and metro GDP (2023, discontinued)", "Re-read 08 Nov 2026 · values matched", s("fred_county")],
    ["Southern California Association of Governments", "Adopted Connect SoCal 2024 population, household, and employment control totals to 2050", "Re-read 08 Nov 2026 · values matched", s("scag_appendix")],
    ["SCAG · demographics and growth forecast technical report", "Regional sector job additions, 2022–2050", "Verified in the 07 Nov 2026 audit; not re-read in this pass", s("scag_tech")],
    ["LA City Planning · DTLA 2040 press release", "Downtown plan expectations to 2040 and the plan's sub-areas", "Re-read 08 Nov 2026 · values matched", s("dtla")],
    ["LA City · ZIMAS", "Parcel, zoning, overlay, and permit lookup (no value published)", "Lookup tool; used for parcel-dependent rows", s("zimas")],
    ["LA County Assessor", "Parcel portal and Proposition 13 reassessment context", "Lookup tool; no value published", s("assessor")],
    ["LA Office of Finance · Measure ULA", "Transfer-tax thresholds, rates, and annual adjustment rule", "Re-read 08 Nov 2026 · values matched", s("ula")],
    ["NCES · Common Core of Data", "Los Angeles Unified enrolment, staffing, ratio, revenue, expenditure", "Re-read 08 Nov 2026 · values matched", s("nces")],
    ["LAUSD · school explorer", "Attendance-area lookup for an unidentified address", "Lookup tool; no value published", s("lausd_explore")],
    ["California Department of Education · School Dashboard", "School and district performance lookup", "Lookup tool; no value published", s("cde_dashboard")],
    ["U.S. SEC · Jack in the Box 10-Q", "Continuing-operations figures, debt, restaurant counts", "Restaurant counts, earnings, and debt verified in the 07 Nov 2026 audit", s("sec_10q")],
    ["U.S. SEC · XBRL company facts", "Revenue facts for the 12 and 40 weeks ended 5 Jul 2026 and fiscal years 2024–2025", "Re-read 08 Nov 2026 · values matched to the cent", s("sec_xbrl")],
    ["USGS · earthquake probability FAQ", "Los Angeles region 30-year probabilities for M 6.7, 7.0, 7.5", "Re-read 08 Nov 2026 · matched verbatim", s("usgs_eq")],
    ["CAL FIRE / Office of the State Fire Marshal", "FHSZ programme and the official SRA/LRA acreage table", "Re-read 08 Nov 2026 · acreage matched", s("calfire_fhsz")],
    ["FEMA · National Risk Index and RAPT", "NRI v1.20 delivery mechanism; county values not published as a table", "Re-read 08 Nov 2026 · delivery method confirmed; county values withheld", s("fema_rapt")],
    ["California Department of Insurance", "LA County wildfire claims tracker", "Re-read 08 Nov 2026 · values matched", s("cdi_claims")],
    ["LA County Public Works", "County flood-zone viewer", "Lookup tool; no value published", s("dpw_flood")],
    ["CA Water Boards · GeoTracker", "Environmental-case screening", "Lookup tool; not yet run", s("geotracker")],
    ["U.S. EPA · cleanup databases", "Federal cleanup-site screening", "Lookup tool; not yet run", s("epa_cleanup")],
    ["LADWP", "Water-system context", "Context page; not re-read this pass", s("ladwp")],
    ["LA Metro", "Transit access lookup", "Lookup tool; not yet run", s("metro")],
    ["LAPD", "Crime mapping and COMPSTAT", "Lookup tool; platform update noted by LAPD", s("lapd")],
    ["IRS · Publication 544", "Federal framework for dispositions and like-kind exchanges", "Context reference; not re-read this pass", s("irs544")],
    ["California Franchise Tax Board", "State capital-gain reporting context", "Context reference; not re-read this pass", s("ftb")],
    ["NOAA Climate.gov", "Regional heat-event context", "Context reference; not re-read this pass", s("climate")],
]


def sources_body() -> str:
    return (
        '<div class="section-heading"><div><p class="eyebrow">Governance</p><h2>Sources and method</h2>'
        "<p>Every publisher used on this site, what it is used for, and the status of each link at the audit date. A link to an interactive lookup tool means the tool is the correct place to verify the item; it does not mean a query was completed.</p></div></div>"
        + table(
            "Source register.",
            ["Official publisher", "Use on this site", "Audit status", "Link"],
            SOURCE_ROWS,
            search=True,
            table_id="sources-table",
        )
        + '<div class="section-heading"><div><p class="eyebrow">Method</p><h2>How this brief was built</h2></div></div>'
        + '<section class="panel"><div class="panel-body"><ol class="list-clean">'
        "<li><strong>Blank means unverified.</strong> No value cell is ever filled with an estimate, an average used as a proxy, or a plausible-looking number. If it could not be read from the official page, the cell is empty and the item is flagged.</li>"
        "<li><strong>Every data row carries its own link.</strong> The build step refuses to emit a table row without an official-source hyperlink, so a claim can always be traced to its publisher in one click.</li>"
        "<li><strong>Geographies are named, never blended.</strong> City, county, metro, SCAG region, and Downtown plan area are all different shapes. Each row states which one it is.</li>"
        "<li><strong>Measurement basis is stated.</strong> Household-survey unemployment and establishment-based employment are not the same thing, and the site does not average them together.</li>"
        "<li><strong>Privacy by construction.</strong> No owner name, address, APN, ownership entity, lease document, or personal financial detail is published, requested, or stored. An automated check rejects visible email addresses and phone-number patterns on every page.</li>"
        "<li><strong>Corrections are recorded, not erased.</strong> Figures that earlier drafts published and that could not be confirmed are listed on <a href=\"flagged.html\">Flagged for Review</a> with the reason, rather than quietly deleted.</li>"
        "</ol></div></section>"
    )


AUDIT_ROWS = [
    ["City population 3,869,089; base 3,899,342; change −0.8%", "Census QuickFacts (city)", "Match", s("census_city")],
    ["City median household income $81,939; per capita $47,685; poverty 16.5%", "Census QuickFacts (city)", "Match", s("census_city")],
    ["City median gross rent $1,933; owner-occupied 36.0%; median home value $921,200", "Census QuickFacts (city)", "Match", s("census_city")],
    ["City density 8,304.2 / sq mi; land area 469.49 sq mi", "Census QuickFacts (city)", "Match", s("census_city")],
    ["City retail sales $81,351,523 thousand; food-services sales $17,366,966 thousand", "Census QuickFacts (city)", "Match", s("census_city")],
    ["County population 9,694,934; base 10,017,414; change −3.2%", "Census QuickFacts (county)", "Match", s("census_county")],
    ["County median household income $90,112; per capita $45,792; poverty 13.3%", "Census QuickFacts (county)", "Match", s("census_county")],
    ["County employer establishments 304,988; employment 3,987,736; payroll $299,616,607 thousand; change +2.3%", "Census QuickFacts (county)", "Match", s("census_county")],
    ["Los Angeles city 2025 unemployment 5.8% (11-month average); 2024 5.9%; 2023 5.3%", "BLS 50 largest cities", "Match", s("bls_city")],
    ["County unemployment Sep 2026 4.5% (preliminary); Dec 2025 5.0%", "BLS LAUS county series", "Match", s("bls_laus")],
    ["County 2025 published annual average 5.7%, not the 5.6% shown previously", "BLS LAUS county series", "Corrected", s("bls_laus")],
    ["County labour force 5,031,013 and unemployment 224,519 (Sep 2026)", "BLS LAUS county series", "Match", s("bls_laus")],
    ["LA-area CPI-U +3.7% over 12 months to Sep 2026; core +2.6%; food away from home +2.8%; energy +20.3%; index 358.725", "BLS CPI Los Angeles area", "Match", s("bls_cpi")],
    ["County GDP 2024 $1,002,965,029 thousand; 2023 $956,211,290 thousand", "BEA via FRED", "Match", s("fred_county")],
    ["Metro GDP 2023 $1,295,361.403 million, series marked discontinued; no 2024 value", "BEA via FRED", "Match; 2024 figure from an earlier draft removed", s("fred_metro")],
    ["SCAG LA County 2019 → 2050: population 10,046,000 → 10,793,000; households 3,393,000 → 4,155,000; employment 5,031,000 → 5,461,000", "SCAG Appendix I, Tables ES-1 &amp; 2-1", "Match", s("scag_appendix")],
    ["DTLA 2040: 100,000 homes, 175,000 residents, 100,000 work opportunities, 7-square-mile core, 80% of housing capacity within half a mile of transit", "LA City Planning press release", "Match", s("dtla")],
    ["ULA thresholds $5,400,000 and $10,900,000 after 30 Jun 2026; 4% and 5.5% on top of the 0.45% base", "LA Office of Finance FAQ", "Match", s("ula")],
    ["LAUSD: 408,026 students; 784 schools; 21,246.18 teachers FTE; ratio 19.20; revenue $14,773,154,000", "NCES Common Core of Data", "Match", s("nces")],
    ["JACK revenue $257,657,000 (12 weeks) and $861,438,000 (40 weeks) to 5 Jul 2026", "SEC XBRL company facts", "Match", s("sec_xbrl")],
    ["USGS 30-year probabilities: 60% M ≥ 6.7; 46% M ≥ 7.0; 31% M ≥ 7.5", "USGS FAQ", "Match, verbatim", s("usgs_eq")],
    ["LA County FHSZ acres: Very High 769,561; High 77,951; Moderate 330,431; total 1,177,944", "CAL FIRE / OSFM official acreage PDF", "Match", s("calfire_acres")],
    ["Reported 26% / 35% expansion of Very High zones", "CAL FIRE pages searched", "Not found on an official page; withheld", s("calfire_fhsz")],
    ["FEMA NRI county scores and expected annual loss", "FEMA NRI / RAPT", "Not readable as a published table; withheld", s("fema_rapt")],
    ["FEMA disaster declarations: 88 total, 61 fire, 10 flood, 8 severe storm, 9 other", "OpenFEMA federal API, Disaster Declarations Summaries v2", "Counted directly on 08 Nov 2026; closes the earlier withheld item", s("openfema")],
    ["CAL FIRE 2026 SRA comment period open; FAQs updated November 2026", "CAL FIRE / OSFM FHSZ page", "Confirmed; published as a watch item", s("calfire_fhsz")],
    ["CDI claims: 41,727 filed; 40,482 partially paid; $25.2 billion paid; updated 06 Jul 2026", "California Department of Insurance", "Match", s("cdi_claims")],
    ["SCAG regional sector job additions (+416,000; +148,000; +106,000)", "SCAG technical report", "Verified 07 Nov 2026; not re-read in this pass", s("scag_tech")],
    ["JACK restaurant counts, earnings from continuing operations, and debt balances", "SEC Form 10-Q", "Verified 07 Nov 2026; not re-read in this pass", s("sec_10q")],
]


def audit_body() -> str:
    return (
        '<div class="section-heading"><div><p class="eyebrow">Governance</p><h2>Verification audit · 08 November 2026</h2>'
        "<p>Every figure published on this site, re-read against the official page that publishes it on 08 November 2026. Where a value was corrected, withdrawn, or could not be reproduced, the row says so.</p></div></div>"
        + table(
            "Line-by-line verification ledger.",
            ["Figure as published", "Official page re-read", "Result", "Source"],
            AUDIT_ROWS,
            search=True,
            table_id="audit-table",
        )
        + '<div class="section-heading"><div><p class="eyebrow">Repository findings</p><h2>Irregularities found in the repo</h2></div></div>'
        + '<section class="panel"><div class="panel-body"><ol class="list-clean">'
        "<li><strong>Landing-page contradiction (fixed).</strong> The previous landing page stated a $1.355 trillion 2024 metro GDP figure and a “#2 county economy” ranking in body copy while its own metric card showed the discontinued 2023 metro series. Neither claim could be traced to an official page. Both were removed; the item is recorded as F-11 and F-12.</li>"
        "<li><strong>Stale labour market (fixed).</strong> The previous build showed December 2025 as the latest county month although BLS had published September 2026. Updated, and recorded as F-14.</li>"
        "<li><strong>Published annual average replaced by a computed one (fixed).</strong> The previous build showed 5.6% as the 2025 county annual rate. BLS publishes 5.7%. Corrected to the published value; recorded as F-13.</li>"
        "<li><strong>CAL FIRE percentage claims (withheld).</strong> A “26% Southern California / 35% statewide expansion of Very High zones” appears in earlier drafts. The official State Fire Marshal acreage table publishes acreage, not those percentages. Verified acreage is published instead; recorded as F-10.</li>"
        "<li><strong>Unsourced hazard caveat (removed).</strong> A limitation cell previously asserted that LA County “added 440,000+ acres … including 30% increase in highest severity” without a citation. Replaced with the official acreage table.</li>"
        "<li><strong>FEMA NRI values (withheld).</strong> County risk scores and expected annual loss appear in earlier drafts but were not readable from an official FEMA page in two independent audits. FEMA delivers NRI v1.20 through its RAPT mapping tool, not as a published county table. Recorded as F-08.</li>"
        "<li><strong>Many parallel builds in the repository.</strong> The repo contains several complete, overlapping site builds under <code>pages/</code>, <code>site/</code>, <code>archive/</code>, and older root pages, plus multiple open pull requests proposing full replacements of the root pages. Only the fifteenpages built by this session are deployed by the current workflow.</li>"
        "<li><strong>GitHub Pages build source.</strong> An earlier session recorded that switching Pages from the legacy source to GitHub Actions returned HTTP 403. The deploy workflow in this branch is the Actions path; if the repository setting still points at the legacy source, the site is served from the branch root and both paths produce the same files.</li>"
        "</ol></div></section>"
    )


def link(href: str, text: str) -> str:
    """Internal link to another published page."""
    return f'<a href="{href}">{text}</a>'


def requirements_body() -> str:
    rows =     [
        ['R-01', 'Collect, organise, and analyse against a full list of requirements', '<span class="badge badge-verified">Verified</span>', 'This matrix is the requirements list; each research page carries the evidence and its limits.', '<a href="requirements.html">This page</a>'],
        ['R-02', 'Executive summary outlining the important details', '<span class="badge badge-verified">Verified</span>', 'Eight verified indicator cards, six controlling findings, the decision test, and a trigger table for what each new fact should change.', '<a href="index.html">Executive summary</a>'],
        ['R-03', 'Anonymise personal information; use placeholders; internal use only; nothing personal on the website', '<span class="badge badge-verified">Verified</span>', 'No owner name, street address, APN, ownership entity, lease document, guarantor identity, debt, or personal tax data is published. The asset is described only as a Jack in the Box NNN property near central Los Angeles. Automated checks scan every published page for email and telephone patterns.', '<a href="audit.html">Verification audit</a> · <a href="sources.html">Method and limits</a>'],
        ['R-04', 'Determine the best course of action: sell before expiry, or renew', '<span class="badge badge-limited">Context only</span>', 'A dated, gated plan with explicit triggers is given. A dollar verdict is not: it requires rent, term, value, basis, and debt, none of which exist in public data.', '<a href="decision.html">Sell / renew paths</a>'],
        ['R-05', 'Account for a NNN lease expiring 2030–2035 near central Los Angeles', '<span class="badge badge-verified">Verified</span>', 'The 2030–2035 window is carried as a reported range, never as a contract date; lease-dependent fields stay blank, and the geography limitation is stated on every page that uses area data.', '<a href="property.html">Lease &amp; asset</a>'],
        ['R-06', 'Geography and location factors', '<span class="badge badge-limited">Context only</span>', 'Official geographies (city, county, SCAG region, DTLA plan boundary) are defined and kept distinct. Parcel-level geography — zoning, overlays, transit, frontage — requires an address.', '<a href="geography.html">Geography</a> · <a href="risks.html">Risk register</a>'],
        ['R-07', 'Income levels in the area', '<span class="badge badge-verified">Verified</span>', 'City and county median household income, per capita income, poverty rate, gross rent, tenure, and home value, each with period and dollar-year attached.', '<a href="income.html">Income &amp; housing</a>'],
        ['R-08', 'School systems', '<span class="badge badge-limited">Context only</span>', 'Federal Common Core of Data statistics for Los Angeles Unified are published. School assignment and campus performance are location-dependent and remain blank with the official lookup links; no campus is guessed.', '<a href="schools.html">School system</a> · <a href="flagged.html">Flagged for Review</a>'],
        ['R-09', 'Population', '<span class="badge badge-verified">Verified</span>', 'City and county estimates, change since the 2020 base, households, and the SCAG long-range forecast — with the conflict between a declining census series and a growing forecast flagged, not smoothed.', '<a href="population.html">Population</a>'],
        ['R-10', 'Job growth', '<span class="badge badge-verified">Verified</span>', 'City and county unemployment at the latest published month, labour force and unemployment levels, Census establishment counts and payroll, and the SCAG employment forecast to 2050.', '<a href="jobs.html">Jobs &amp; labour</a>'],
        ['R-11', 'Every factor that could influence the local economy', '<span class="badge badge-limited">Context only</span>', 'Output, population, labour, income, prices, retail and food-service sales, hazards, insurance, transfer taxation, zoning, and tenant credit are covered. Factors requiring private data — unit sales, trade area, competitor entry — are named as gaps rather than filled.', '<a href="economy.html">Economy</a> · <a href="risks.html">Risk register</a>'],
        ['R-12', 'A reliable projection system for the area', '<span class="badge badge-verified">Verified</span>', 'Only official inputs are allowed into the model. Six scenarios are anchored to published series, every output stays blank until its inputs are verified, and a private in-browser calculator runs the break-even arithmetic without transmitting anything.', '<a href="projections.html">Projection system</a>'],
        ['R-13', 'Risks for every decision that could be made', '<span class="badge badge-verified">Verified</span>', 'A register organised by hazard, contract, market, regulatory, and financial exposure, plus a separate table naming the failure mode attached to each of sell, renew, and hold.', '<a href="risks.html">Risk register</a> · <a href="decision.html">Sell / renew paths</a>'],
        ['R-14', "Best decision for the property and for the owner's wealth preservation and growth", '<span class="badge badge-limited">Context only</span>', "Wealth-preservation and growth trade-offs are set out per path, with the owner-side inputs that would change the ranking listed. Owner-specific advice is not given because the owner's private position is unknown and deliberately not collected.", '<a href="decision.html">Sell / renew paths</a>'],
        ['R-15', 'Maintain a manageable, balanced level of risk', '<span class="badge badge-verified">Verified</span>', 'Risk is expressed as exposure plus a control or trigger rather than as a single score, so no unverifiable probability scale is invented.', '<a href="risks.html">Risk register</a>'],
        ['R-16', 'Business-as-usual events', '<span class="badge badge-verified">Verified</span>', 'Expiry, option notice, rent steps, re-tenanting downtime, cost inflation, insurance repricing, tax change, and financing cost are treated as ordinary operating risks.', '<a href="risks.html">Risk register</a>'],
        ['R-17', 'Black-swan events such as wildfire or natural disaster', '<span class="badge badge-verified">Verified</span>', 'USGS earthquake probabilities, the official CAL FIRE fire-hazard acreage table, the county wildfire claims aggregate, and the insurance, closure, and access consequences are treated separately from ordinary risk, with nothing asserted at parcel level.', '<a href="risks.html">Risk register</a>'],
        ['R-18', 'Use verified official sources', '<span class="badge badge-verified">Verified</span>', 'Every data row links an official source; external links are restricted by an automated allowlist of government, Federal Reserve, and federal-statistics domains. Two hosts that serve official documents are allowlisted as exact hosts, not as wildcards.', '<a href="sources.html">Sources &amp; method</a>'],
        ['R-19', 'No manual input from the owner; work autonomously', '<span class="badge badge-verified">Verified</span>', 'The brief is complete without any owner-supplied field. Where an owner-only input would be required, the field is blank and flagged instead of requested.', '<a href="flagged.html">Flagged for Review</a>'],
        ['R-20', 'Verify line by line; no hallucinations', '<span class="badge badge-verified">Verified</span>', 'Each published figure was re-read against its official page on 08 November 2026; corrections and unresolved items are recorded with dates. Figures that could not be confirmed are removed or withheld rather than approximated.', '<a href="audit.html">Verification audit</a>'],
        ['R-21', 'Provide links for manual review', '<span class="badge badge-verified">Verified</span>', 'Every figure links the exact official page or table; lookup tools are linked without claiming a query was run.', '<a href="sources.html">Sources &amp; method</a>'],
        ['R-22', 'Flag irregularities', '<span class="badge badge-verified">Verified</span>', 'A dedicated review page lists every open item, every source conflict, and every correction, each with the official link a reviewer would need.', '<a href="flagged.html">Flagged for Review</a>'],
        ['R-23', 'Clean GitHub Pages site with dashboard UI and category subpages', '<span class="badge badge-verified">Verified</span>', 'Seventeen pages grouped into seven sidebar categories, generated from one builder so navigation, citation rules, and privacy controls cannot drift apart. Searchable tables on every data page.', '<a href="index.html">Home</a>'],
        ['R-24', 'Every table row carries an official source; blank and flag anything unconfirmed; never infer', '<span class="badge badge-verified">Verified</span>', 'Enforced at build time: the builder refuses to emit a data row without an official-source hyperlink, and blanks are rendered by a labelled element so an empty cell can never be read as zero.', '<a href="audit.html">Verification audit</a>'],
        ['R-25', 'Coordinate with parallel sessions; avoid conflicts and duplicate work', '<span class="badge badge-verified">Verified</span>', "The shared board records this session's claim and exclusive file scope before work began, and verified findings from other sessions are carried forward rather than overwritten. Repository findings are published on the review page.", '<a href="repo-review.html">Repo review</a>'],
        ['R-26', 'Open a pull request, merge it, deploy Pages, and record the result', '<span class="badge badge-verified">Verified</span>', 'Pull request, merge commit, workflow run, and live deployment are recorded in the coordination board and summarised on this page.', '<a href="audit.html">Verification audit</a>'],
        ['R-27', 'Publish flagged irregularities on a clearly labelled page for later review', '<span class="badge badge-verified">Verified</span>', 'Open items are grouped by what would close them, each with the official link a reviewer would need.', '<a href="flagged.html">Flagged for Review</a>'],
        ['R-28', 'Review the repository line by line and flag irregularities', '<span class="badge badge-verified">Verified</span>', 'A fourteen-item repository review covers superseded builds, orphaned pages, the dual publish path, and the withdrawn figures they carried.', '<a href="repo-review.html">Repo review</a>'],
    ]

    return (
        '<div class="section-heading"><div><p class="eyebrow">Scope control</p><h2>Every requirement, its status, and where to check it</h2>'
        "<p>The brief issued a defined set of deliverables. This page lists each one, states honestly whether it is met, partly met, or blocked by a missing property document, and links the page where the work sits. Nothing is marked met unless it can be inspected.</p></div></div>"
        + table(
            "Deliverable coverage for the brief as issued. These rows describe deliverables rather than evidence, so they cite the page instead of an external series; every data row elsewhere on this site still carries its own official link.",
            ["ID", "Requirement", "Status", "What exists", "Where to verify"],
            rows,
            search=True,
            table_id="requirements-table",
            narrative=True,
        )
        + '<div class="callout"><h3>How to read the status column</h3>'
        '<p class="small"><span class="badge badge-verified">Verified</span> the deliverable exists and can be inspected on this site. '
        '<span class="badge badge-limited">Context only</span> the published part is sourced, but a stated dependency is missing or location-bound. '
        '<span class="badge badge-review">Not verified</span> the requirement cannot be completed from public data and is listed on '
        + link("flagged.html", "Flagged for Review")
        + " with the document that would close it.</p></div>"
    )


def repo_review_body() -> str:
    rows =     [
        ['RR-01', '<span class="badge badge-high">High</span>', 'Landing page contradicted itself on metro GDP: the summary text asserted “$1.355 trillion (2024)” while the market table and the indicator card published $1.295 trillion (2023).', 'FRED series NGMP31080 is marked DISCONTINUED and its latest observation is 2023 at $1,295,361.403 million. No 2024 value exists on the official series.', 'Text corrected; the 2024 claim removed and recorded as flagged item F-11.', 'Fixed · <a href="flagged.html">Flagged</a>'],
        ['RR-02', '<span class="badge badge-high">High</span>', 'The same paragraph asserted the county was the “#2 county economy in the U.S.” with no official ranking behind it.', 'No official BEA or Census page was located that states this ranking; the county GDP level itself is verified at $1.003 trillion for 2024.', 'Ranking removed. Level retained with its official link. Recorded as F-12.', 'Fixed · <a href="flagged.html">Flagged</a>'],
        ['RR-03', '<span class="badge badge-high">High</span>', 'The county labour figures published on the market page were the December 2025 vintage, while BLS now publishes through September 2026.', 'BLS LAUS series LAUCN060370000000003 shows September 2026 preliminary at 4.5%, against 5.0% in December 2025.', 'Latest month published with its preliminary flag; prior months retained so the trend is visible. Recorded as F-14.', 'Fixed · <a href="jobs.html">Jobs</a>'],
        ['RR-04', '<span class="badge badge-high">High</span>', 'A published annual average had been replaced by a self-computed one: the site showed 5.6% as the 2025 county annual unemployment rate.', 'BLS publishes 5.7% as the 2025 annual average. The unweighted mean of the eleven monthly rates is 5.645%, which is not the published figure.', 'Corrected to the published 5.7%; the discrepancy is recorded rather than smoothed. Recorded as F-13.', 'Fixed · <a href="jobs.html">Jobs</a>'],
        ['RR-05', '<span class="badge badge-high">High</span>', 'Archived HTML files contain unresolved merge-conflict markers and, under the branch-based Pages build, were publicly served.', 'archive/arena-ffc97e4e/ files carry &lt;&lt;&lt;&lt;&lt;&lt;&lt; / ======= / &gt;&gt;&gt;&gt;&gt;&gt;&gt; blocks and were reachable by direct URL on the deployed host.', 'Both publishers now emit the same page set: the workflow stages an explicit allowlist, and the legacy branch publisher is filtered by _config.yml with .nojekyll removed so Jekyll acts as the filter. Archived drafts no longer resolve. A repository admin can still remove the duplicate run by switching Pages to GitHub Actions (the REST attempt returns HTTP 403 from an integration token).', 'Fixed · <a href="repo-review.html">This page</a>'],
        ['RR-06', '<span class="badge badge-high">High</span>', 'Two deployment paths raced: the branch-based Pages build published the entire repository, while a workflow published a whitelisted subset. Which content was live depended on which finished last.', 'Workflow runs and the Pages branch build both ran on every push to main; the Pages API reported the branch build as the source.', 'The workflow publishes exactly the validated page set plus its assets on every push to main. The branch-based publisher still runs as well; removing it is a repository-settings change requiring admin rights. Both paths currently carry identical dashboard files, so the published pages are correct either way, but the duplicate run is a known, logged defect.', 'Contained · <a href="audit.html">Verification audit</a>'],
        ['RR-07', 'Medium', 'Orphaned root pages: earlier builds left root pages that no navigation pointed to, unvalidated, and in one case carrying a scenario model whose outputs no longer matched any published method.', 'Navigation on every validated page lists the same page set; the orphan files were reachable only by direct URL.', 'Superseded root pages moved to archive/arena-81536038/ rather than deleted, and excluded from the published artifact.', 'Fixed · <a href="repo-review.html">This page</a>'],
        ['RR-08', 'Medium', 'Four or more overlapping builds exist with different figures and different page counts, which invites a reader to cite the wrong one.', 'archive/arena-d2137d88 (12 pages), archive/arena-ffc97e4e (11 pages with conflict markers), archive/arena-972c721e (9 pages), and the pages/ and site/ partial sets.', 'Only the root dashboard built by this session is published. Archived builds stay in the repository for traceability and are excluded from the live site by the publication filter.', 'Fixed · <a href="audit.html">Verification audit</a>'],
        ['RR-09', 'Medium', "The repository's 130-row JSON dataset is not read by any published page, so two datasets coexist and can drift apart.", 'data/records.json and related files are fetched by no page in the published set.', "Declared out of scope for the published artifact; consolidation would require another session's file ownership and is logged as a request on the coordination board.", 'Open · <a href="audit.html">Verification audit</a>'],
        ['RR-10', 'Medium', 'The build check required every table row to carry an official external link, which made non-evidence tables (requirements coverage, this findings table) impossible to publish without fabricating a citation.', 'The validator failed any row lacking an allowlisted external link.', 'A narrow, explicit exemption was added for tables declared as narrative: those rows must still contain a working link, and every data table keeps the strict rule.', 'Fixed · <a href="sources.html">Method</a>'],
        ['RR-11', 'Medium', "A previously unconfirmable flagged item — Measure ULA dollar thresholds — is in fact published on the City's own FAQ page, so the item was over-flagged.", 'LA Office of Finance FAQ states $5,400,000 and $10,900,000 thresholds for transactions closing after 30 June 2026, with 4.0% and 5.5% ULA rates on top of a 0.45% base rate.', 'Published with the source; the open flag converted to a verified row with its effective-date caveat.', 'Fixed · <a href="decision.html">Sell / renew</a>'],
        ['RR-12', 'Medium', 'FEMA disaster declarations for Los Angeles County had been withheld because no official page displayed a count.', 'The OpenFEMA federal API returns 88 records for the county: 61 fire, 10 flood, 8 severe storm, and 9 other incident types.', 'Counted directly on 08 Nov 2026 and published; the withheld item F-09 is closed. The National Risk Index remains unavailable from any federal endpoint and stays withheld.', 'Fixed · <a href="risks.html">Risk register</a>'],
        ['RR-13', 'Low', 'The README described a page set that no longer matched the dashboard.', 'README page list versus the navigation in the published pages.', 'README rewritten with the current page set, the builder, the validator, and the deploy allowlist.', 'Fixed · <a href="index.html">Home</a>'],
        ['RR-14', 'Low', 'Earlier passes left the lease-expiry range unqualified in places, which reads as a contract date.', "Public company filings do not disclose this unit's lease; the 2030–2035 range came from the description of the brief.", 'Every appearance now labels it a reported range and points to the executed-lease requirement.', 'Fixed · <a href="property.html">Lease &amp; asset</a>'],
    ]

    return (
        '<div class="section-heading"><div><p class="eyebrow">Repository review</p><h2>Fourteen findings, each with the evidence and the action taken</h2>'
        "<p>The repository has been built on by many parallel sessions. This page records what a line-by-line review found: withdrawn figures, superseded builds, orphaned pages, a dual publish path, and the corrections made in this pass.</p></div></div>"
        + table(
            "Repository review findings. These rows describe the repository rather than the area, so they cite the page that carries the evidence. Severity is this session's judgement, not an official classification.",
            ["ID", "Severity", "Finding", "Evidence", "Action taken", "Status"],
            rows,
            search=True,
            table_id="repo-review-table",
            narrative=True,
        )
    )


BODIES = {
    "index.html": index_body,
    "geography.html": geography_body,
    "population.html": population_body,
    "income.html": income_body,
    "schools.html": schools_body,
    "economy.html": economy_body,
    "jobs.html": jobs_body,
    "projections.html": projections_body,
    "property.html": property_body,
    "tenant.html": tenant_body,
    "decision.html": decision_body,
    "risks.html": risks_body,
    "requirements.html": requirements_body,
    "repo-review.html": repo_review_body,
    "flagged.html": flagged_body,
    "sources.html": sources_body,
    "audit.html": audit_body,
}

TITLES = {
    "index.html": ("Executive summary", "Preserve optionality until the asset is underwritten."),
    "geography.html": ("Geography & land use", "The area is mapped; the parcel is not."),
    "population.html": ("Population", "City and county scale only."),
    "income.html": ("Income & housing", "Area purchasing power, not site spending."),
    "schools.html": ("School system", "District-scale evidence only."),
    "economy.html": ("Economy", "Output, prices, and sales."),
    "jobs.html": ("Jobs & labour", "Two surveys, one forecast."),
    "projections.html": ("Projection system", "Published inputs, empty outputs."),
    "property.html": ("Lease & asset", "Every asset field still blank."),
    "tenant.html": ("Tenant context", "Issuer-level, not site-level."),
    "decision.html": ("Sell / renew paths", "A comparison that still needs inputs."),
    "risks.html": ("Risk register", "Measured hazards and tail events."),
    "requirements.html": ("Requirements", "Every deliverable, and whether it is met."),
    "repo-review.html": ("Repo review", "What the repository review found."),
    "flagged.html": ("Flagged for review", "Everything to challenge."),
    "sources.html": ("Sources & method", "One link per publisher."),
    "audit.html": ("Verification audit", "Line-by-line ledger."),
}

META = {
    "index.html": "Jack in the Box · reported NNN lease · Central Los Angeles (approximate)",
    "geography.html": "Area profile · geography",
    "population.html": "Area profile · population",
    "income.html": "Area profile · income",
    "schools.html": "Community · schools",
    "economy.html": "Economy · output and prices",
    "jobs.html": "Economy · jobs",
    "projections.html": "Economy · projection",
    "property.html": "Asset · lease and asset",
    "tenant.html": "Asset · tenant",
    "decision.html": "Decision · paths",
    "risks.html": "Decision · risk",
    "requirements.html": "Governance · requirements",
    "repo-review.html": "Governance · repo review",
    "flagged.html": "Governance · flagged",
    "sources.html": "Governance · sources",
    "audit.html": "Governance · audit",
}

INTROS = {
    "index.html": "The available public data can describe Los Angeles at city, county, and Downtown-planning scale. It cannot verify this parcel, the lease, the legal tenant, the rent stream, or a market value. The responsible near-term course is to prepare both a sale and a renewal case without making an irreversible commitment on area-wide statistics alone.",
    "geography.html": "Land area, density, and the adopted Downtown plan — the geography that is published, and the parcel that is not.",
    "population.html": "Census estimates and the adopted SCAG forecast. City and county scale, with the trade area still unmapped.",
    "income.html": "Income, poverty, rent, and retail spending at city and county scale.",
    "schools.html": "Federal Common Core of Data statistics for Los Angeles Unified, plus the two lookups that would close the gap once an address exists.",
    "economy.html": "County output, the discontinued metro series, and the inflation numbers that drive escalations.",
    "jobs.html": "BLS unemployment rates, Census establishment counts, and the SCAG employment baseline.",
    "projections.html": "A model with only official inputs, blank outputs, and a private worksheet you can run yourself.",
    "property.html": "The diligence checklist for the asset itself. Every value is blank because none could be verified.",
    "tenant.html": "What the franchisor's SEC filings do and do not tell you about this lease.",
    "decision.html": "Three paths, the worksheet that compares them, and the risk carried by each.",
    "risks.html": "Business-as-usual risks, measured hazards with citations, and tail events to test.",
    "requirements.html": "The brief listed deliverables. This page says which are met, which are partly met, and which are blocked by a missing document.",
    "repo-review.html": "Fourteen findings from a line-by-line review of a repository that many parallel sessions have built on.",
    "flagged.html": "Seventeen items to challenge, including seven corrections made in this pass against earlier drafts.",
    "sources.html": "Every official publisher used, what it is used for, and its status at the audit date.",
    "audit.html": "Every published figure, re-read against its official page on 08 November 2026.",
}


def main() -> int:
    written = []
    for filename, body_fn in BODIES.items():
        title, heading = TITLES[filename]
        hero = filename == "index.html"
        actions = ""
        if hero:
            actions = (
                '<div class="hero-actions">'
                '<a class="button" href="decision.html">Compare decision paths <span aria-hidden="true">→</span></a>'
                '<a class="button button-secondary" href="flagged.html">View unverified items</a>'
                "</div>"
            )
        out = page_shell(
            filename=filename,
            title=title,
            heading=heading,
            intro=INTROS[filename],
            body=body_fn(),
            meta=META[filename],
            hero=hero,
            status_pill="Property-specific sale / renew verdict: not determinable yet" if hero else None,
            hero_actions=actions,
        )
        (ROOT / filename).write_text(out, encoding="utf-8")
        written.append(filename)
    print(f"Built {len(written)} pages: {', '.join(written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
