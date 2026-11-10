#!/usr/bin/env python3
"""Build the curated public dashboard from the verified dataset.

Default: write canonical root pages and assets/projections.json.
--out DIR: write a deployable artifact containing only curated public files.
--check: verify committed canonical pages match the dataset without writing.
"""
from __future__ import annotations

import argparse
import html
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Iterable

from projection_model import build_projection_payload, load_data

ROOT = Path(__file__).resolve().parents[1]
PAGES = ["index.html", "market.html", "property.html", "projections.html", "decision.html", "risks.html", "requirements.html", "flagged.html", "sources.html", "audit.html"]
NAV = [
    ("index.html", "Overview"),
    ("market.html", "Market & community"),
    ("property.html", "Property & tenant"),
    ("projections.html", "Projections"),
    ("decision.html", "Decision paths"),
    ("risks.html", "Risks"),
    ("requirements.html", "Requirements"),
    ("flagged.html", "Flagged for review"),
    ("sources.html", "Sources"),
    ("audit.html", "Audit"),
]


def e(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def badge(status: str) -> str:
    labels = {
        "verified": ("badge-verified", "Verified"),
        "derived": ("badge-derived", "Derived calculation"),
        "unverified": ("badge-review", "Unverified — blank"),
        "partial": ("badge-review", "Partial / open"),
        "covered": ("badge-verified", "Covered"),
        "blocked": ("badge-review", "Blocked — inputs missing"),
        "analysis": ("badge-limited", "Analysis / judgment"),
    }
    cls, label = labels.get(status, ("badge-limited", status.replace("_", " ").title()))
    return f'<span class="badge {cls}">{e(label)}</span>'


def source_links(data: dict[str, Any], ids: Iterable[str]) -> str:
    links = []
    for sid in ids:
        src = data["sources"][sid]
        links.append(f'<a class="source-link" href="{e(src["url"])}" target="_blank" rel="noopener noreferrer">{e(src["publisher"])}</a>')
    return " · ".join(links) if links else '<span class="badge badge-review">Source required</span>'


def value_cell(value: Any, status: str = "verified") -> str:
    if value is None:
        return '<td class="blank-value" aria-label="Unconfirmed value intentionally blank"></td>'
    return f"<td>{e(value)}</td>"


def table(table_id: str, caption: str, headers: list[str], rows: list[list[str]], searchable: bool = True) -> str:
    tools = ""
    if searchable:
        tools = (
            '<div class="table-tools"><label class="micro muted" for="search-' + e(table_id) + '">Filter table</label>'
            '<input id="search-' + e(table_id) + '" class="table-search" type="search" placeholder="Search rows…" '
            'aria-label="Search ' + e(caption) + '" data-table-search="' + e(table_id) + '"></div>'
        )
    head = "".join(f'<th scope="col">{e(h)}</th>' for h in headers)
    body = "\n".join("<tr>" + "".join(cell if cell.startswith("<td") else f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    return (
        tools
        + '<div class="table-wrap"><table id="' + e(table_id) + '"><caption>' + e(caption) + "</caption>"
        + "<thead><tr>" + head + "</tr></thead><tbody>\n" + body + "\n</tbody></table></div>"
    )


def observation_rows(data: dict[str, Any], categories: list[str] | None = None, ids: list[str] | None = None) -> list[list[str]]:
    rows = []
    for obs in data["observations"]:
        if categories is not None and obs["category"] not in categories:
            continue
        if ids is not None and obs["id"] not in ids:
            continue
        rows.append([
            f'<strong>{e(obs["measure"])}</strong><span class="row-note">{e(obs["category"])}</span>',
            value_cell(obs["value"], obs["status"]),
            f'{e(obs["geography"])}<span class="row-note">{e(obs["period"])}</span>',
            badge(obs["status"]) + f'<span class="row-note">{e(obs["note"])}</span>',
            source_links(data, obs["sources"]),
        ])
    return rows


def obs_table(data: dict[str, Any], table_id: str, caption: str, categories: list[str] | None = None, ids: list[str] | None = None) -> str:
    return table(table_id, caption, ["Finding", "Value", "Geography / period", "Status and decision relevance", "Official source"], observation_rows(data, categories, ids))


def layout(data: dict[str, Any], page: str, title: str, subtitle: str, body: str) -> str:
    nav_parts = []
    for href, label in NAV:
        active = " active" if href == page else ""
        current = ' aria-current="page"' if href == page else ""
        nav_parts.append(f'<a class="nav-link{active}" href="{e(href)}"{current}>{e(label)}</a>')
    nav = "\n".join(nav_parts)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)} · Jack in the Box NNN decision brief</title>
  <meta name="description" content="{e(subtitle)}">
  <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
  <div class="shell">
    <aside class="sidebar" id="site-nav" aria-label="Dashboard sections">
      <div class="brand"><span class="brand-mark">JIB</span><div><strong>Decision brief</strong><span class="micro muted">Central Los Angeles area · reported NNN</span></div></div>
      <nav class="nav">{nav}</nav>
      <div class="sidebar-note"><strong>Privacy first.</strong> No owner, parcel, or personal financial identifiers are published. Unverified values are blank and flagged.</div>
    </aside>
    <div class="main-column">
      <header class="topbar">
        <button class="nav-toggle" type="button" data-nav-toggle aria-controls="site-nav" aria-expanded="false">☰ <span>Sections</span></button>
        <span class="crumb">Verified dashboard · {e(data['meta']['date'])}{(' · re-verified ' + e(data['meta']['reverified'])) if data['meta'].get('reverified') else ''}</span>
      </header>
      <main id="main-content" class="content">
        <header class="page-intro"><p class="eyebrow">{e(data['meta']['title'])}</p><h1>{e(title)}</h1><p class="lead">{e(subtitle)}</p></header>
        {body}
      </main>
      <footer class="footer">Decision support, not legal, tax, appraisal, or brokerage advice. Every table row links to an official source. <a href="sources.html">Source registry</a> · <a href="flagged.html">Flagged for review</a> · <a href="audit.html">Audit</a></footer>
    </div>
  </div>
  <script src="assets/site.js"></script>
</body>
</html>
"""


def card(title: str, value: str, note: str, href: str, link_label: str) -> str:
    return f'<article class="metric-card"><div class="metric-label">{e(title)}</div><div class="metric-value">{e(value)}</div><p class="metric-meta">{e(note)}</p><a class="metric-source" href="{e(href)}" target="_blank" rel="noopener noreferrer">{e(link_label)}</a></article>'


def build_index(data: dict[str, Any], payload: dict[str, Any]) -> str:
    s = data["sources"]
    cards = "".join([
        card("Recommendation", "Dual-track", "Prepare sale and renewal in parallel; preserve notice/option rights.", s["sec_10k"]["url"], "SEC lease-context source"),
        card("Tenant ARD debt wall", "95.8% ('29–'32)", "$1.430B of $1.492B principal matures ARDs Aug 2029–Feb 2032; 7.624% refi.", s["sec_10q_debt"]["url"], "SEC Q3 FY2026 Debt Note"),
        card("Latest labor & yields", "4.5% / 4.88%", "Sep 2026 LA NSA unemployment 4.5%; Nov 9 10Y Treasury 4.88%.", s["treasury"]["url"], "U.S. Treasury Nov 9 yield curve"),
        card("Tenant operating trend", "SSS −1.1%", "Jack Q3 FY26 system −1.1%; franchise allowance +70.3% to $(7.61)M.", s["sec_10q_ar"]["url"], "SEC Q3 FY2026 credit allowance"),
        card("LA exit tax tiers", "0.56–6.06%", "County 0.11% + City 0.45% + ULA 4%/5.5% ($5.4M/$10.9M thresholds).", s["lavote_dtt"]["url"], "LA County DTT & ULA schedule"),
        card("Property inputs", "Blank", "Parcel, lease, rent, value, debt, tax basis, insurance remain unverified.", s["assessor"]["url"], "Official parcel lookup"),
    ])
    categories = "".join(
        f'<a class="category-card" href="{e(href)}"><strong>{e(label)}</strong><span>{e(desc)}</span></a>'
        for href, label, desc in [
            ("market.html", "Market & community", "Geography, population, income, jobs, schools, drivers."),
            ("property.html", "Property & tenant", "Blank asset fields, issuer credit, taxes, lease gates."),
            ("projections.html", "Projections", "Official DOF/SCAG paths, derived arithmetic, gated property model."),
            ("decision.html", "Decision paths", "Sell, renew, hold, exchange, refinance, re-tenant + local worksheet."),
            ("risks.html", "Risks", "Ordinary, rare high-impact, and black-swan stresses."),
            ("requirements.html", "Requirements", "Coverage checklist and open evidence."),
            ("flagged.html", "Flagged for review", "Unconfirmed values and irregularities."),
            ("sources.html", "Sources", "Official registry with access dates."),
            ("audit.html", "Audit", "Verification, privacy, deployment, and method."),
        ]
    )
    body = f"""
<section class="hero" aria-labelledby="recommendation">
  <p class="eyebrow">Executive decision</p>
  <h2 id="recommendation">Prepare sale and renewal in parallel. Do not drift to expiry.</h2>
  <p>{e(data['meta']['recommendation'])}</p>
  <div class="hero-actions"><a class="button" href="decision.html">Open decision paths &amp; worksheet</a><a class="button button-secondary" href="flagged.html">See what is still unverified</a></div>
</section>
<div class="callout warning"><h3>Working premise, not a verified asset</h3><p>{e(data['meta']['premise'])}</p></div>
<section class="card-grid" aria-label="Key findings">{cards}</section>
{table("executive-snapshot", "Executive evidence snapshot.", ["Finding", "Value", "Status", "Decision meaning", "Official source"], [
    ["Course of action", "<strong>Dual-track sale + renewal</strong>", badge("analysis"), "Preserve optionality until verified lease, value, tax, and risk evidence supports a choice.", source_links(data, ["sec_10k", "irs_544", "treasury"])],
    ["Property-specific inputs", value_cell(None, "unverified"), badge("unverified"), "Parcel, lease, rent, value, debt, condition, insurance, and tax basis remain blank.", source_links(data, ["assessor", "zimas"])],
    ["Tenant 2029–2032 ARD wall", "95.8% ($1,429.6M) of principal", badge("derived"), "Refinancing cliffs (Aug 2029, May 2031 at 7.624%, Feb 2032) overlap the 2030–2035 expiry window.", source_links(data, ["sec_10q_debt", "sec_10q_ar"])],
    ["Official population paths", "DOF declines; SCAG grows", badge("derived"), "DOF E-1 (Jan 2026) and P-2A decline while SCAG grows; do not blend or assign to parcel.", source_links(data, ["dof_e1", "dof_p2a", "scag_appendix"])],
    ["County hazard & insurance", "FEMA NRI 100 / $20M FAIR cap", badge("verified"), "88 FEMA declarations (61 fire); CDI FAIR Plan commercial cap raised to $20M/$100M through 2028.", source_links(data, ["fema_county_query", "openfema_la", "cdi_fairplan_2025"])],
])}
<div class="section-heading"><div><p class="eyebrow">Navigate</p><h2>Category subpages</h2><p>Clean tables, official row sources, and explicit blank fields.</p></div></div>
<section class="category-grid">{categories}</section>
<div class="section-heading"><div><p class="eyebrow">Immediate actions</p><h2>What can be done without guessing</h2></div></div>
<ol class="action-list">
  <li>Calendar every lease notice, option, estoppel, and assignment deadline from the executed lease.</li>
  <li>Identify the legal tenant and guarantor; obtain financials and default history.</li>
  <li>Order title, parcel/hazard/zoning match, condition report, insurance review, and tax-basis workup.</li>
  <li>Request executable sale pricing and extension terms; compare after-tax net proceeds with risk-adjusted hold value.</li>
  <li>Fund a re-tenanting fallback before expiry; keep sale and renewal options open until evidence supports a choice.</li>
</ol>
"""
    return layout(data, "index.html", "Wealth preservation first, growth second, no invented inputs.", "A verified, privacy-safe decision dashboard for a reported Jack in the Box NNN property near central Los Angeles.", body)


def build_market(data: dict[str, Any]) -> str:
    body = f"""
<div class="callout"><h3>Geography discipline</h3><p>City, county, metro, school district, and plan-area statistics are not interchangeable. None is a parcel trade-area study. Values below keep the publisher's geography, period, units, and adjustment basis.</p></div>
<div class="section-heading"><div><p class="eyebrow">Geography · population · income · housing</p><h2>Community fundamentals</h2></div></div>
{obs_table(data, "market-fundamentals", "Census city/county fundamentals.", ["Geography", "Population", "Income", "Housing"])}
<div class="section-heading"><div><p class="eyebrow">Economy · labor · inflation · financing</p><h2>Demand and cost context</h2></div></div>
{obs_table(data, "market-economy", "Official economic and labor context.", ["Economy", "Labor", "Inflation", "Financing", "Economic drivers"])}
<div class="section-heading"><div><p class="eyebrow">Schools · planning · public safety</p><h2>Community and land-use context</h2></div></div>
{obs_table(data, "market-community", "Schools, planning, and public-safety context.", ["Schools", "Planning", "Public safety"])}
"""
    return layout(data, "market.html", "Market and community fundamentals", "Official city/county/metro context with explicit geography and period labels; no parcel catchment is inferred.", body)


def build_property(data: dict[str, Any]) -> str:
    rows = []
    for field in data["property_fields"]:
        rows.append([
            f'<strong>{e(field["field"])}</strong>',
            value_cell(field["value"], field["status"]),
            badge(field["status"]) + f'<span class="row-note">{e(field["note"])}</span>',
            source_links(data, field["sources"]),
        ])
    gates = [
        ["Identity gate", "Parcel, title, situs, and lease must match before any property-specific value or hazard conclusion.", badge("unverified"), source_links(data, ["assessor", "zimas"])],
        ["Credit gate", "Legal tenant/guarantor and enforceable recourse must be verified; brand and issuer filings are not enough.", badge("unverified"), source_links(data, ["sec_10q", "sec_release"])],
        ["Cash-flow gate", "Rent, escalations, unrecovered owner costs, capital plan, and downtime must be evidence-backed.", badge("unverified"), source_links(data, ["sec_10k", "prop13"])],
        ["Exit gate", "Executable sale price, debt payoff, transaction costs, taxes, and buyer financing must be verified.", badge("unverified"), source_links(data, ["treasury", "ula", "irs_544"])],
    ]
    body = f"""
<div class="callout warning"><h3>Reported premise only</h3><p>{e(data['meta']['premise'])}</p></div>
<div class="section-heading"><div><p class="eyebrow">Asset and contract facts</p><h2>Unverified property-level fields</h2><p>Blank cells are intentional. Official lookup links are not substitutes for the private lease, title, inspection, or tax file.</p></div><span class="badge badge-review">Review required</span></div>
{table("asset-fields", "Property fields remain blank until official/private evidence is matched.", ["Field", "Value", "Status / diligence needed", "Official reference"], rows)}
<div class="section-heading"><div><p class="eyebrow">Decision gates</p><h2>What must be true before a property verdict</h2></div></div>
{table("property-gates", "Evidence gates for any sell/extend/hold decision.", ["Gate", "Requirement", "Status", "Official source"], gates)}
<div class="section-heading"><div><p class="eyebrow">Tenant / issuer context</p><h2>Jack in the Box public-company credit context</h2><p>These are issuer-wide disclosures, not confirmation of the subject restaurant, operator, or lease.</p></div></div>
{obs_table(data, "tenant-context", "SEC issuer context.", ["Tenant"])}
<div class="section-heading"><div><p class="eyebrow">Taxes · wages · financing</p><h2>Rules that change net proceeds and tenant capacity</h2></div></div>
{obs_table(data, "property-tax-wage", "Tax, wage, and financing rules.", ["Taxes", "Labor costs", "Financing"])}
"""
    return layout(data, "property.html", "The lease—not the logo—determines the credit.", "Asset-specific fields stay blank until the executed lease, parcel, title, condition, insurance, and tax basis are verified.", body)


def build_projections(data: dict[str, Any], payload: dict[str, Any]) -> str:
    dof = payload["dof"]
    dof_rows = [[str(r["year"]), r["display"]["population"], r["display"]["yoy"], r["display"]["change"], r["display"]["index"], source_links(data, [dof["source"]])] for r in dof["rows"]]
    milestone_rows = [[str(r["year"]), r["display"]["population"], r["display"]["change"], r["display"]["cagr"], source_links(data, [dof["source"]])] for r in dof["milestones"]]
    scag = payload["scag"]
    scag_tables = []
    for name, label in [("population", "Population"), ("households", "Households"), ("employment", "Employment")]:
        rows = [[str(r["year"]), r["display"]["value"], r["display"]["change"], r["display"]["cagr"], source_links(data, [scag["source"]])] for r in scag["series"][name]["rows"]]
        scag_tables.append(table(f"scag-{name}", f"SCAG Los Angeles County {label.lower()} milestones; no interpolation.", ["Year", label, "Change from 2019", "CAGR from 2019", "Official source"], rows))
    comp_rows = [[str(r["year"]), r["display"]["dof"], r["display"]["scag"], r["display"]["difference"], r["display"]["difference_pct"], source_links(data, ["dof_p2a", "scag_appendix"])] for r in payload["agency_comparison"]]
    sector_rows = [[e(r["name"]), f'{r["display"]["start"]} → {r["display"]["end"]}', r["display"]["change"], r["display"]["cagr"], e(r["display"]["published"]) + (f'<span class="row-note">{e(r["flag"])}</span>' if r.get("flag") else ""), source_links(data, r["sources"])] for r in payload["sectors"]]
    stress_rows = [[f'<strong>{e(r["name"])}</strong>', e(r["symbol"]), value_cell(None, "unverified"), e(r["formula"]), source_links(data, r["sources"])] for r in payload["stress"]]
    pm = payload["property_model"]
    pm_rows = [[e(k.replace("_", " ").title()), value_cell(v, "unverified"), badge("blocked"), "Requires verified property inputs; no zero-fill or inferred assumptions.", source_links(data, ["sec_10k", "irs_544", "treasury"])] for k, v in pm["outputs"].items()]
    body = f"""
<div class="callout"><h3>Method</h3><p>Official DOF and SCAG projections are published separately. Derived columns are transparent arithmetic from cited official inputs, not official observations. No interpolation, agency blending, parcel extrapolation, cap-rate assumption, rent-growth assumption, or invented probability is used. Property outputs remain blank because required inputs are unverified.</p></div>
<div class="callout"><h3>Caution: DOF level vs Census estimate</h3><p>DOF lists 9,853,435 for Los Angeles County in 2025; Census lists 9,694,934 for July 1, 2025 (DOF +158,501, +1.63%). The two are different series and the cause of the gap is not stated on the pages read. Read the DOF path below for direction and rate of change, not as an absolute head-count, until reconciled. See <a href="flagged.html">Flagged for review</a>.</p></div>
<div class="section-heading"><div><p class="eyebrow">California DOF · {e(dof['vintage'])}</p><h2>Los Angeles County annual population, 2026–2035</h2><p>Index base: 2026 = 100. Year-over-year and cumulative changes are derived calculations.</p></div></div>
{table("dof-annual", "DOF P-2A annual county population and derived changes.", ["Year", "Population", "YoY change", "Change from 2026", "Index (2026=100)", "Official source"], dof_rows)}
{table("dof-milestones", "DOF county milestones through 2050.", ["Year", "Population", "Change from 2026", "CAGR from 2026", "Official source"], milestone_rows)}
<div class="section-heading"><div><p class="eyebrow">SCAG · {e(scag['vintage'])}</p><h2>Los Angeles County milestone forecasts</h2><p>SCAG values are rounded to thousands in the official appendix. Missing years, including 2035, are not interpolated.</p></div></div>
{''.join(scag_tables)}
<div class="section-heading"><div><p class="eyebrow">Planning divergence</p><h2>DOF versus SCAG county population</h2><p>The gap is a planning-model difference, not a confidence interval and not a parcel demand forecast.</p></div></div>
{table("agency-comparison", "Official county population milestones compared.", ["Year", "DOF", "SCAG", "SCAG − DOF", "Difference vs DOF", "Official sources"], comp_rows)}
<div class="section-heading"><div><p class="eyebrow">SCAG regional sector jobs</p><h2>Six-county SCAG region, 2022–2050</h2><p>Regional sector context only. Manufacturing printed percentage is withheld because it conflicts with its endpoints.</p></div></div>
{table("sector-projection", "SCAG regional sector job endpoints and derived arithmetic.", ["Sector", "Jobs 2022 → 2050", "Derived change", "Derived CAGR", "Published change / flag", "Official source"], sector_rows)}
<div class="section-heading"><div><p class="eyebrow">Symbolic stress tests</p><h2>Lease and ownership stresses without invented magnitudes</h2><p>Magnitudes and probabilities stay blank until evidence exists. These formulas define what must be measured.</p></div></div>
{table("stress-tests", "Symbolic stress definitions; numeric shocks are unverified.", ["Stress", "Symbol / input", "Numeric magnitude", "Formula / treatment", "Official source"], stress_rows)}
<div class="section-heading"><div><p class="eyebrow">Gated property model</p><h2>Property decision outputs</h2><p>Status: {e(pm['status'])}. Missing inputs: {e(', '.join(pm['missing']))}.</p></div><span class="badge badge-review">Blank by design</span></div>
{table("property-model", "Property outputs remain null/blank until verified inputs exist.", ["Output", "Value", "Status", "Reason", "Official source"], pm_rows)}
<p class="small muted">Reproduce: <code>python3 scripts/projection_model.py</code> and <code>python3 scripts/build_public.py</code>. Generated public data: <a href="assets/projections.json">assets/projections.json</a>. To test your private verified lease, debt, and tax inputs strictly inside your own browser without publishing or saving assumptions, use the <a href="decision.html#owner-worksheet">blank-default local owner worksheet</a>.</p>
"""
    return layout(data, "projections.html", "Official projections, transparent arithmetic, gated property outputs.", "DOF and SCAG paths are kept separate; derived values are labeled; missing property inputs produce blank outputs, never zero.", body)


def build_decision(data: dict[str, Any]) -> str:
    rows = []
    for d in data["decisions"]:
        rows.append([f'<strong>{e(d["path"])}</strong>', e(d["when"]), e(d["tradeoffs"]), e(d["required"]), f'<strong>{e(d["verdict"])}</strong>', source_links(data, d["sources"])])
    balance = [
        ["Wealth preservation", "Verify after-tax net proceeds, insurance, capital reserves, and downside before chasing upside.", source_links(data, ["irs_544", "cdi_claims", "fema_county_query"])],
        ["Growth", "Keep renewal/re-tenanting and alternative-use upside only where evidence supports executable value.", source_links(data, ["sec_release", "zimas", "scag_appendix"])],
        ["Manageable risk", "Avoid single-tenant concentration, maturity cliffs, and passive expiry drift; fund fallback downtime.", source_links(data, ["sec_10k", "treasury", "sec_release"])],
    ]
    body = f"""
<section class="hero"><p class="eyebrow">Provisional recommendation</p><h2>Dual-track now; choose only after evidence.</h2><p>{e(data['meta']['recommendation'])}</p></section>
<div class="section-heading"><div><p class="eyebrow">Path comparison</p><h2>Sell, renew, hold, and related alternatives</h2></div></div>
{table("decision-paths", "Decision paths, conditions, tradeoffs, and required evidence.", ["Path", "When it can win", "Tradeoffs", "Required evidence", "Provisional view", "Official source"], rows)}
<div class="section-heading"><div><p class="eyebrow">Objective balance</p><h2>Preservation, growth, and risk control</h2></div></div>
{table("objective-balance", "How the recommendation balances the stated objectives.", ["Objective", "Application", "Official source"], balance)}
<div class="section-heading"><div><p class="eyebrow">Execution sequence</p><h2>Next steps that do not require guessing</h2></div></div>
<ol class="action-list">
  <li>Preserve rights: calendar notices/options and request estoppel/lease amendments review.</li>
  <li>Build the evidence file: title, parcel, lease, guaranty, rent roll, condition, insurance, tax basis, debt.</li>
  <li>Run two market processes: executable sale pricing and tenant extension terms.</li>
  <li>Compare after-tax net sale proceeds with risk-adjusted hold/renew/re-tenant value using verified inputs.</li>
  <li>If evidence remains incomplete, default to optionality and funded fallback—not an irreversible choice.</li>
</ol>
<section class="worksheet" id="owner-worksheet" aria-labelledby="worksheet-heading">
  <div class="ws-head">
    <div>
      <p class="eyebrow">Private local calculator · zero defaults</p>
      <h2 id="worksheet-heading">Owner decision worksheet (browser memory only)</h2>
      <p class="small muted">All fields start blank by design so no rent, cap rate, or tax basis is assumed. Calculations run locally in your browser without cookies, storage, or network requests, applying the verified LA transfer-tax tiers (0.56% / 4.56% / 6.06% city; 0.11% county-only).</p>
    </div>
    <button type="button" class="button button-secondary ws-reset" data-ws-reset>Clear inputs</button>
  </div>
  <div class="ws-grid">
    <div class="ws-field"><label for="ws-jurisdiction">Transfer-tax jurisdiction</label><select id="ws-jurisdiction"><option value="la_city">City of Los Angeles (County 0.11% + City 0.45% + ULA)</option><option value="county_only">LA County unincorporated / non-special city (0.11%)</option></select></div>
    <div class="ws-field"><label for="ws-exchange">Income tax mode</label><select id="ws-exchange"><option value="taxable">Taxable sale (apply gain basis &amp; rate)</option><option value="1031">1031 like-kind exchange deferral (IRS Form 8824)</option></select></div>
    <div class="ws-field"><label for="ws-sale-price">Executable sale price ($)</label><input id="ws-sale-price" type="number" min="0" step="any" placeholder="Enter verified quote"></div>
    <div class="ws-field"><label for="ws-debt">Debt payoff &amp; prepayment ($)</label><input id="ws-debt" type="number" min="0" step="any" placeholder="Enter payoff (0 if unencumbered)"></div>
    <div class="ws-field"><label for="ws-broker-pct">Brokerage &amp; other closing costs (%)</label><input id="ws-broker-pct" type="number" min="0" step="any" placeholder="Enter % (excl. transfer tax)"></div>
    <div class="ws-field"><label for="ws-tax-basis">Adjusted tax basis ($)</label><input id="ws-tax-basis" type="number" min="0" step="any" placeholder="Enter CPA basis (if taxable)"></div>
    <div class="ws-field"><label for="ws-tax-rate">Combined federal + CA gain/recapture rate (%)</label><input id="ws-tax-rate" type="number" min="0" step="any" placeholder="Enter blended tax %"></div>
    <div class="ws-field"><label for="ws-rent">Current annual NNN base rent ($)</label><input id="ws-rent" type="number" min="0" step="any" placeholder="Enter verified annual NOI"></div>
    <div class="ws-field"><label for="ws-years">Remaining lease years to test</label><input id="ws-years" type="number" min="0" step="any" placeholder="Enter exact years"></div>
    <div class="ws-field"><label for="ws-esc">Annual contractual rent growth (%)</label><input id="ws-esc" type="number" step="any" placeholder="Enter lease escalation %"></div>
    <div class="ws-field"><label for="ws-discount">Owner after-tax discount rate (%)</label><input id="ws-discount" type="number" min="0" step="any" placeholder="Compare vs 4.88% 10Y Treasury"></div>
    <div class="ws-field"><label for="ws-exit-val">Expected gross value at horizon ($)</label><input id="ws-exit-val" type="number" min="0" step="any" placeholder="Enter stabilized/dark exit value"></div>
  </div>
  <div class="ws-outputs" aria-live="polite">
    <div class="ws-card"><div class="metric-label">Combined DTT + ULA</div><div class="ws-val" id="ws-out-dtt">—</div><p class="micro muted" id="ws-out-dtt-note">Enter a sale price to evaluate the 0.56% / 4.56% / 6.06% LA transfer-tax tier.</p></div>
    <div class="ws-card"><div class="metric-label">Net sale proceeds</div><div class="ws-val" id="ws-out-sale">—</div><p class="micro muted" id="ws-out-sale-note">Requires sale price, debt payoff, and brokerage/other cost % locally.</p></div>
    <div class="ws-card"><div class="metric-label">Hold PV (rent + net exit)</div><div class="ws-val" id="ws-out-hold">—</div><p class="micro muted" id="ws-out-hold-note">Requires annual NNN rent, remaining years, escalation %, discount rate %, exit value, and debt.</p></div>
    <div class="ws-card ws-highlight"><div class="metric-label">Local path spread</div><div class="ws-val" id="ws-out-spread">—</div><p class="micro muted" id="ws-out-spread-note">Complete both Sale and Hold inputs above to compare paths locally.</p></div>
  </div>
</section>
"""
    return layout(data, "decision.html", "Decision paths and balanced recommendation", "A conditional, wealth-preservation-first course among selling, renewing, holding, exchanging, refinancing, and re-tenanting.", body)


def build_risks(data: dict[str, Any]) -> str:
    rows = []
    for r in data["risks"]:
        rows.append([f'<strong>{e(r["name"])}</strong><span class="row-note">{e(r["category"])}</span>', e(r["mechanism"]), e(r["context"]), badge(r["site_status"]), e(r["mitigation"]), source_links(data, r["sources"])])
    body = f"""
<div class="callout warning"><h3>County metrics are not parcel losses</h3><p>FEMA NRI, USGS probabilities, CAL FIRE acres, and CDI claims describe broad context. They do not establish this property's exposure, insurance cost, or expected loss.</p></div>
<div class="section-heading"><div><p class="eyebrow">Risk register</p><h2>Ordinary risks, rare high-impact events, and black-swan stresses</h2></div></div>
{table("risk-register", "Risk register with transmission, context, site status, mitigation, and official sources.", ["Risk", "Transmission", "Verified context", "Site status", "Mitigation", "Official source"], rows)}
<div class="section-heading"><div><p class="eyebrow">Hazard and insurance context</p><h2>Official county/regional metrics</h2></div></div>
{obs_table(data, "risk-context", "Hazard and insurance context.", ["Hazards", "Insurance"])}
"""
    return layout(data, "risks.html", "Risks that can change the decision", "Ordinary lease/market/tax risks, rare high-impact hazards, and compound black-swan stresses with official context and mitigations.", body)


def build_requirements(data: dict[str, Any]) -> str:
    rows = [[f'<strong>{e(r["requirement"])}</strong>', e(r["coverage"]), e(r["evidence"]), badge(r["status"]), source_links(data, r["sources"])] for r in data["requirements"]]
    body = f"""
<div class="callout"><h3>Coverage rule</h3><p>Covered means the public dashboard contains official-source evidence and analysis. Partial means the category is addressed but property-specific or private evidence remains open. Open items do not block publication; they are blank and flagged.</p></div>
{table("requirements-coverage", "Requirement coverage checklist.", ["Requirement", "Coverage", "Evidence", "Status", "Official source"], rows)}
"""
    return layout(data, "requirements.html", "Requirements coverage", "Checklist mapping the brief to published evidence, open items, and official sources.", body)


def build_flagged(data: dict[str, Any]) -> str:
    rows = [[f'<strong>{e(f["item"])}</strong>', e(f["reason"]), e(f["action"]), badge("unverified"), source_links(data, f["sources"])] for f in data["flags"]]
    body = f"""
<div class="callout warning"><h3>Flagged does not mean hidden</h3><p>Unconfirmed values are blank in the dashboard and listed here. Official lookup links show where evidence must come from; they do not verify a missing value.</p></div>
{table("flagged-review", "Open items, irregularities, and required evidence.", ["Item", "Why open / irregular", "Required action", "Status", "Official source"], rows)}
"""
    return layout(data, "flagged.html", "Flagged for Review", "Unconfirmed property values, source inconsistencies, stale claims, and deployment irregularities that remain open.", body)


def build_sources(data: dict[str, Any]) -> str:
    rows = []
    for sid, src in data["sources"].items():
        rows.append([f'<strong>{e(src["title"])}</strong><span class="row-note">{e(sid)}</span>', e(src["publisher"]), e(src["kind"]), e(src["accessed"]), f'<a class="source-link" href="{e(src["url"])}" target="_blank" rel="noopener noreferrer">Official source</a>'])
    body = f"""
<div class="callout"><h3>Source policy</h3><p>Only official publishers, official issuer filings, official hosted data services, or repository provenance are used. Nonofficial historical citations are preserved in Git but excluded from this curated artifact. Access date is the date this session read the source.</p></div>
{table("source-registry", "Official source registry.", ["Source", "Publisher", "Kind", "Accessed", "Link"], rows)}
"""
    return layout(data, "sources.html", "Official source registry", "Every published table row links back to one of these official sources or repository provenance records.", body)


def build_audit(data: dict[str, Any]) -> str:
    rows = [[f'<strong>{e(a["check"])}</strong>', e(a["result"]), e(a["detail"]), source_links(data, a["sources"])] for a in data["audit"]]
    body = f"""
<div class="callout"><h3>Verification standard</h3><p>Verified means the official publisher displays the value for the stated geography, period, unit, and adjustment basis. Derived means transparent arithmetic from cited inputs. Unverified means blank and flagged. Analysis is judgment, not an official fact.</p></div>
{table("audit-ledger", "Audit ledger.", ["Check", "Result", "Detail", "Official / provenance source"], rows)}
<div class="section-heading"><div><p class="eyebrow">Reproducibility</p><h2>Build and gates</h2></div></div>
<ul class="action-list">
  <li><code>python3 scripts/build_public.py --check</code> verifies canonical pages match the dataset.</li>
  <li><code>python3 -m unittest discover -s tests -p 'test_*.py'</code> tests projection arithmetic, gating, build determinism, and privacy/source rules.</li>
  <li><code>python3 scripts/validate_site.py</code> validates pages, row source links, allowlist, local links, blanks, and privacy patterns.</li>
  <li>Public artifact contains only curated pages, assets, and generated projection data. Historical builds remain in Git but are not published.</li>
</ul>
<p class="small muted">Repository: <a href="{e(data['sources']['repo']['url'])}" target="_blank" rel="noopener noreferrer">GitHub</a> · Live: <a href="{e(data['sources']['live']['url'])}" target="_blank" rel="noopener noreferrer">GitHub Pages</a> · Verification logs: <code>verification/2026-11-08-0e369d53.md</code>, <code>verification/2026-11-10-2eefc54d.md</code>, <code>verification/2026-11-10-ac5b9087.md</code>, <code>verification/2026-11-10-af77a54e.md</code>, <code>verification/2026-11-10-a8681975.md</code>, <code>verification/2026-11-10-c5e199ef.md</code>.</p>
"""
    return layout(data, "audit.html", "Verification audit", "Repository, privacy, official-source, projection, and deployment checks with reproducible gates.", body)


def build_404(data: dict[str, Any]) -> str:
    links = "".join(f'    <li><a href="{e(href)}">{e(label)}</a></li>\n' for href, label in NAV)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <title>Page not found · Jack in the Box NNN decision brief</title>
  <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
  <main class="content" style="max-width:760px;padding:3rem 1.5rem">
    <header class="page-intro">
      <p class="eyebrow">404 · Curated dashboard</p>
      <h1>That path is not part of the published decision brief</h1>
      <p class="lead">The public brief is published as ten curated pages ({e(data['meta']['date'])}). Internal coordination records, verification logs, and historical archives are intentionally excluded from publication.</p>
    </header>
    <section class="hero">
      <p class="eyebrow">Navigate</p>
      <h2>Canonical dashboard sections</h2>
      <ul class="action-list">
{links}      </ul>
      <div class="hero-actions"><a class="button" href="index.html">Return to overview</a></div>
    </section>
    <footer class="footer">Privacy-first: no owner, parcel, or personal financial identifiers are published.</footer>
  </main>
</body>
</html>
"""


def render_all(data: dict[str, Any] | None = None) -> dict[str, str]:
    data = data or load_data()
    payload = build_projection_payload(data)
    return {
        "index.html": build_index(data, payload),
        "market.html": build_market(data),
        "property.html": build_property(data),
        "projections.html": build_projections(data, payload),
        "decision.html": build_decision(data),
        "risks.html": build_risks(data),
        "requirements.html": build_requirements(data),
        "flagged.html": build_flagged(data),
        "sources.html": build_sources(data),
        "audit.html": build_audit(data),
        "404.html": build_404(data),
        "assets/projections.json": json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
    }


def write_outputs(outputs: dict[str, str], out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for rel, content in outputs.items():
        path = out / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Write a curated deployable artifact to this directory.")
    parser.add_argument("--check", action="store_true", help="Check committed canonical pages against the dataset without writing.")
    args = parser.parse_args()
    outputs = render_all()
    if args.check:
        failures = []
        for rel, content in outputs.items():
            path = ROOT / rel
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                failures.append(rel)
        if failures:
            print("Build check failed; out-of-date files: " + ", ".join(failures), file=sys.stderr)
            return 1
        print(f"Build check passed: {len(outputs)} generated files match the verified dataset.")
        return 0
    if args.out:
        write_outputs(outputs, args.out)
        for asset in ("styles.css", "site.js"):
            shutil.copyfile(ROOT / "assets" / asset, args.out / "assets" / asset)
        (args.out / ".nojekyll").write_text("", encoding="utf-8")
        print(f"Wrote curated artifact to {args.out} ({len(PAGES)} pages).")
        return 0
    write_outputs(outputs, ROOT)
    print(f"Wrote {len(PAGES)} canonical pages and assets/projections.json.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
