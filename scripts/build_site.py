#!/usr/bin/env python3
"""Generate the dashboard pages. Run: python3 scripts/build_site.py"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location("site_base", ROOT / "scripts/site_base.py")
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)

ds, an, M = B.ds, B.an, B.MODEL
esc, source_link, status_pill = B.esc, B.source_link, B.status_pill
C = B.counts()
TOTAL = len(ds.ROWS)

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<rect width="32" height="32" rx="7" fill="#12263f"/><rect x="6" y="7" width="20" height="18" rx="3" fill="#b3282d"/>
<path d="M11 12h10M11 16h10M11 20h6" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg>"""


ANCHOR_PAGE = {
    "demographics": "market.html", "income": "market.html", "housing": "market.html",
    "economy": "market.html", "projections": "projections.html", "schools": "market.html",
    "tenant": "tenant.html", "property": "property.html", "tax": "decision.html",
    "hazards": "property.html", "capital": "decision.html",
}
ROW_PAGE = {r[0]: ANCHOR_PAGE[r[1]] for r in ds.ROWS}


def ref(key):
    """Link a row id (e.g. T-27) or a flag id (F-11) to its anchor, wherever it lives."""
    key = key.strip()
    if key in ROW_PAGE:
        return f'<a href="{ROW_PAGE[key]}#{key.lower()}">{esc(key)}</a>'
    if re.fullmatch(r"F-\d{2}", key):
        return f'<a href="flagged.html#{key.lower()}">{esc(key)}</a>'
    return esc(key)


def pct(x, d=0):
    return f"{x*100:.{d}f}%"


def money(x):
    return f"{x:,.0f}"


# =========================================================== index / overview
def page_index():
    d = {r[0]: r for r in ds.ROWS}

    def card(rid, label=None, suffix="", note=None):
        r = d[rid]
        val = r[3]
        unit = r[4]
        return f"""<article class="card">
  <div class="k">{esc(label or r[2])}</div>
  <div class="v">{esc(val)}{esc(suffix)}</div>
  <div class="m">{esc(note or (unit + ' · ' + r[5] + ' · ' + r[6]))}</div>
  <a class="src" href="{esc(ds.SOURCES[r[7]][2])}" target="_blank" rel="noopener noreferrer">{esc(ds.SOURCES[r[7]][0])} ↗</a>
</article>"""

    kpi = "".join([
        card("D-02", "Los Angeles County population", note="July 1, 2025 · down 3.2% since 2020"),
        card("J-06", "DOF projected county change to 2035", note="Official state baseline · −1.47%"),
        card("E-06", "Metro nonfarm jobs, 12-month change", note="September 2026, preliminary"),
        card("P-07", "Gasoline, 12-month change", note="September 2026 · hits drive-thru traffic"),
        card("T-11", "Tenant's guided FY2026 closures", note="It is closing, not expanding"),
        card("C-01", "10-year Treasury", note="November 5, 2026 · sets the buyer's floor"),
    ])

    steps = [
        ("Confirm the counterparty before anything else.",
         "The lease may be with Jack in the Box Inc., with a franchisee, or with a brand affiliate that subleases to a "
         f"franchisee. The 10-K says the company leases or subleases to franchisees for most franchised sites. {status_pill('unverified')} "
         'See <a href="property.html#pr-02">PR-02</a> and <a href="flagged.html#F-11">F-11</a>.'),
        ("Read the lease for the four clauses that decide this case.",
         "Renewal options, rent escalations, the casualty and rent-abatement clause, and the assignment and guaranty "
         'language. Until those are read, every rent comparison is speculative. '
         'See <a href="property.html#pr-09">PR-09</a>, <a href="property.html#pr-10">PR-10</a>.'),
        ("Get two numbers, not one.",
         "A broker opinion of value for the asset as it stands today, and an after-tax net-proceeds figure. The city "
         "transfer tax alone is 4.45% of price in the $5.4m–$10.9m band, before income tax on the gain."),
        ("Open the renewal conversation early and price the alternative.",
         "Renewal leverage decays as expiry approaches. Approach the tenant 24–30 months out, with a re-use or "
         "redevelopment plan in hand so that a weak offer can be declined."),
        ("Pre-commit a sell trigger now, in writing.",
         "Example: sell if the tenant will not extend beyond 2030 on acceptable terms by a stated date, or if the "
         "parcel's insurance quote exceeds a stated level. A pre-committed trigger prevents a decision made under pressure."),
    ]
    steps_html = "".join(
        f'<li><strong>{s[0]}</strong> {s[1]}</li>' for s in steps)

    body = f"""
<section class="hero">
  <p class="eyebrow">Jack in the Box · reported NNN lease · central Los Angeles (approximate)</p>
  <h1>Hold the asset, but negotiate the term now — and pre-commit the exit.</h1>
  <p class="lede">Official data cannot price this parcel, because the parcel, the lease and the counterparty are
  private. What the official data <em>can</em> do is rule out two of the four available paths and rank the
  remainder. The county is losing population on the state's own baseline, the tenant is closing restaurants and
  selling real estate, and rates are high. That combination argues against an open-ended hold and against an
  opportunistic sale — and for converting an expiring lease into a longer one while simultaneously preparing a
  sale file.</p>
  <p class="lede" style="margin-bottom:0"><strong>Recommended path: renew, then decide.</strong> Not because the
  area is strong, but because the lease term is the only asset the owner fully controls, and it is worth more
  than the price a buyer would pay for a lease with five years left on it.</p>
  <div class="actions">
    <a class="btn" href="decision.html">Compare the four paths →</a>
    <a class="btn ghost" href="flagged.html">See what is not verified ({C['unverified']} items)</a>
  </div>
</section>

<div class="grid g3">{kpi}</div>

<div class="grid g2" style="margin-top:18px">
  <section class="panel" style="margin:0">
    <div class="hd"><div><p class="eyebrow">Executive summary</p><h2>What the evidence actually says</h2></div></div>
    <ol class="steps">
      <li><strong>The area is shrinking, not growing.</strong> Los Angeles County lost 3.2% of its population
      between 2020 and 2025 and the Department of Finance projects a further 1.47% decline to 2035, while
      California as a whole grows 2.23% over the same period. A volume-driven restaurant in a shrinking county
      is fighting its own catchment. <a href="market.html#demographics">Population rows →</a></li>
      <li><strong>The tenant is contracting.</strong> System same-store sales fell 4.2% in FY2025 and 7.4% in the
      fourth quarter. It closed 86 restaurants against 31 openings, guides another 50–100 closures, discontinued
      its dividend, and states that its turnaround plan includes <em>selling real estate</em>. A renewal is
      therefore a negotiation with a counterparty that has alternatives. <a href="tenant.html">Tenant rows →</a></li>
      <li><strong>The jobs picture is flat, with one growing sector.</strong> Metro nonfarm employment is up 0.5%
      year over year. Information is down 5.7%, financial activities 1.7%, professional services 0.5%; education
      and health services is up 3.8% and leisure and hospitality 1.5%. The durable daypart base is health and
      education, not office workers. <a href="market.html#economy">Jobs rows →</a></li>
      <li><strong>The cost picture is hostile to the customer.</strong> Gasoline is up 30.8% year over year and
      energy 20.3%, while restaurant menu prices are up 2.8%. A drive-thru customer paying a third more at the
      pump and a restaurant raising prices below headline inflation is a margin squeeze in both directions.
      <a href="market.html#economy">Price rows →</a></li>
      <li><strong>The sell case is real, but smaller than the headline price.</strong> A city transfer tax of
      4.45% (or 5.95% above $10.9m) plus commission plus income tax on the gain plus loan payoff is a large
      deduction from gross proceeds. An owner who compares a gross price to a hold value will overstate the sale.
      <a href="decision.html#after-tax">Net-proceeds section →</a></li>
      <li><strong>Hazards are diligence items, not probabilities.</strong> This brief assigns no probability to
      wildfire, earthquake or flood for the parcel. It does record what a realised event looks like: the
      Palisades Fire destroyed 6,845 structures; the ShakeOut scenario models $191bn of regional loss. The
      material channel for a central-LA box is insurance-market contagion, not ember exposure.
      <a href="property.html#hazards">Hazard rows →</a></li>
    </ol>
  </section>

  <aside style="display:grid;gap:14px;align-content:start">
    <div class="verdict">
      <p class="eyebrow">Recommended course of action</p>
      <h2>Renew, then decide — with a written trigger</h2>
      <p style="margin:0 0 8px">Ask the tenant for a <strong>10-year extension with a creditworthy guaranty</strong>
      and a rent no lower than the current rent, in exchange for a defined capital contribution (roof, HVAC,
      drive-thru lane). In parallel, assemble the sale file: appraisal, rent roll, lease abstract, insurance
      quote, and a §1031 replacement search.</p>
      <p style="margin:0"><strong>Do not</strong> sign a long extension at a weak rent with no guaranty.
      <strong>Do not</strong> hold to expiry with no re-use plan. <strong>Do not</strong> sell today at a price
      struck off a declining same-store-sales trend unless liquidity is needed.</p>
    </div>
    <div class="callout warn">
      <b>Why "it depends" is the honest answer on price</b>
      No official source publishes a cap rate, an appraisal or a comparable sale for an individual
      single-tenant restaurant. The {C['unverified']} blank rows on this site are not gaps in the research —
      they are fields that cannot be sourced officially and therefore must not be filled in
      (<a href="flagged.html">full list</a>).
    </div>
    <div class="callout">
      <b>What would change the recommendation</b>
      Three findings would move this answer: (1) the lease is guaranteed by Jack in the Box Inc. — that raises
      the value of holding and of a renewal; (2) the tenant already holds renewal options below market — that
      destroys the landlord's leverage and pushes toward an early sale; (3) the owner needs liquidity within
      36 months — that overrides the asset analysis entirely.
    </div>
  </aside>
</div>

<section class="panel">
  <div class="hd"><div><p class="eyebrow">Five steps, in order</p><h2>What to do in the next 90 days</h2></div>
  <a class="small" href="decision.html">Full path comparison →</a></div>
  <ol class="steps">{steps_html}</ol>
</section>

<section class="panel">
  <div class="hd"><div><p class="eyebrow">Dataset at a glance</p><h2>{TOTAL} rows, every one source-linked</h2></div></div>
  <div class="grid g4">
    <div class="card"><div class="k">Verified</div><div class="v">{C['verified']}</div>
      <div class="m">Read on the cited official page during this session</div></div>
    <div class="card"><div class="k">Derived</div><div class="v">{C['derived']}</div>
      <div class="m">Arithmetic on verified rows; formula shown in the note</div></div>
    <div class="card"><div class="k">Unverified</div><div class="v">{C['unverified']}</div>
      <div class="m">Blank by rule. Published on Flagged for review</div></div>
    <div class="card"><div class="k">Withheld</div><div class="v">{C['withheld']}</div>
      <div class="m">Private property or financial data, never published</div></div>
  </div>
  <p class="small muted" style="margin-bottom:0">Nothing on this site is estimated.
  Where an official page did not publish a value, the cell shows an em dash. Where the value is private, the
  cell shows <em>[WITHHELD]</em>. See <a href="sources.html#rules">the verification rules</a>.</p>
</section>
"""
    return B.layout("index.html", "Overview | Jack in the Box NNN decision brief", body,
                    "Source-linked decision brief for a Jack in the Box triple-net-leased property in central Los Angeles: sell, renew, hold, or exchange.")


# =========================================================== market
def page_market():
    groups = [
        ("demographics", "Population &amp; demographics",
         "Population change is the first-order demand driver for a restaurant. The county figure is the one that matters here, because no trade-area figure can be computed without the address."),
        ("income", "Income, poverty &amp; workforce",
         "A drive-thru needs households with discretionary income who are time-poor. These are citywide and countywide medians, not trade-area medians."),
        ("housing", "Housing &amp; construction",
         "Housing value and rents proxy land scarcity — which is what actually holds value in a built-out urban parcel when the building is only 1,372 sq ft."),
        ("schools", "Schools &amp; education",
         "District-scale education indicators for Los Angeles Unified. No campus can be assigned to the parcel, so "
         "campus-level performance is not shown and never will be without an address."),
        ("economy", "Economy, jobs &amp; prices",
         "Current labour-market and price conditions for the Los Angeles metro. Every number here is a level or a 12-month change; none is a forecast."),
    ]
    parts = []
    for cat, title, blurb in groups:
        rows = B.rows_for(cat)
        anchor = {"demographics": "demographics", "income": "income", "housing": "housing",
                  "economy": "economy", "schools": "schools"}[cat]
        parts.append(f"""
<section class="panel" id="{anchor}">
  <div class="hd"><div><p class="eyebrow">{title}</p><h2>{len(rows)} published measures</h2></div>
  <span class="pill neutral">Official sources only</span></div>
  <p class="small muted" style="margin-top:0">{blurb}</p>
  {B.data_table(rows, anchor + '-table', f'{title} — each row links to the official page it was read from.')}
</section>""")

    body = f"""
<section class="hero">
  <p class="eyebrow">Market &amp; area</p>
  <h1>The area is not growing. The question is whether the corner is.</h1>
  <p class="lede">Central Los Angeles is not one market. Census, SCAG and the Department of Finance each
  publish at a different geography, and none of them publishes at the scale of a restaurant trade area. The
  figures below describe the city and the county. They establish the direction of travel; they do not describe
  the corner this box stands on.</p>
  <div class="actions">
    <a class="btn ghost" href="projections.html">Official projections to 2035 →</a>
    <a class="btn ghost" href="flagged.html">What is missing →</a>
  </div>
</section>

<div class="grid g4">
  <div class="card"><div class="k">County population change</div><div class="v">−3.2%</div>
    <div class="m">2020 estimate base to July 2025</div>
    <a class="src" href="{esc(ds.SOURCES['censusCounty'][2])}" target="_blank" rel="noopener noreferrer">Census QuickFacts ↗</a></div>
  <div class="card"><div class="k">Median household income</div><div class="v">$90,112</div>
    <div class="m">County · 2020–2024 ACS 5-year</div>
    <a class="src" href="{esc(ds.SOURCES['censusCounty'][2])}" target="_blank" rel="noopener noreferrer">Census QuickFacts ↗</a></div>
  <div class="card"><div class="k">Metro unemployment</div><div class="v">4.4%</div>
    <div class="m">September 2026, preliminary</div>
    <a class="src" href="{esc(ds.SOURCES['blsEag'][2])}" target="_blank" rel="noopener noreferrer">BLS ↗</a></div>
  <div class="card"><div class="k">Gasoline, 12-month change</div><div class="v">+30.8%</div>
    <div class="m">September 2026 · LA area CPI</div>
    <a class="src" href="{esc(ds.SOURCES['blsCpi'][2])}" target="_blank" rel="noopener noreferrer">BLS ↗</a></div>
</div>

<div class="callout" style="margin-top:18px">
  <b>Read the geographies before reading the numbers</b>
  City of Los Angeles, Los Angeles County, the LA–Long Beach–Santa Ana metro area, and the
  LA–Long Beach–Anaheim CPI area are <em>four different boundaries</em>. This site labels every row with its
  geography. Two unemployment rates appear in the tables below and they are not comparable: 4.4% is the metro
  area in September 2026, 5.8% is the city's 2025 annual average excluding October, and 4.5% is the county's
  September 2026 reading.
</div>
{"".join(parts)}
"""
    return B.layout("market.html", "Market &amp; area | Jack in the Box NNN decision brief", body,
                    "Population, income, housing, jobs and prices for Los Angeles city and county, each row linked to the official source.")


# =========================================================== projections
def page_projections():
    grid_rows = []
    for row in M["grid"]:
        cells = "".join(f'<td class="num">{row["values"][r]:,.0f}</td>' for r in M["rates"])
        grid_rows.append(f'<tr><td class="num">{row["growth"]*100:.0f}%</td>{cells}</tr>')
    grid_html = "".join(grid_rows)
    rate_heads = "".join(f'<th scope="col">{r*100:.0f}% discount rate</th>' for r in M["rates"])

    proj_rows = "".join(
        f"<tr><td><strong>{esc(a)}</strong></td><td>{esc(b)}</td><td class='src'>{esc(c)}</td><td class='note'>{esc(d)}</td></tr>"
        for a, b, c, d in an.PROJECTION_METHOD)

    proj_table = f"""
<div class="tablewrap"><table id="proj-method">
<caption>How each category is projected, and how much confidence the official data supports.</caption>
<thead><tr><th scope="col">Category</th><th scope="col">Method</th><th scope="col">Source basis</th><th scope="col">Confidence</th></tr></thead>
<tbody>{proj_rows}</tbody></table></div>"""

    body = f"""
<section class="hero">
  <p class="eyebrow">Projections &amp; model</p>
  <h1>The only official projection is a demographic one — and it points down.</h1>
  <p class="lede">This page separates three things that are usually blurred together: what the State of
  California actually projects, what this brief calculates from it, and what the scenario model assumes. The first
  is a fact, the second is arithmetic on that fact, and the third is an assumption set that the reader can see
  and challenge.</p>
</section>

<section class="panel" id="official">
  <div class="hd"><div><p class="eyebrow">Official projection</p><h2>Department of Finance baseline, Los Angeles County</h2></div>
  {source_link('dofP2A', 'CA Dept. of Finance P-2A ↗')}</div>
  <p class="small muted" style="margin-top:0">Report P-2A, Baseline 2024, Vintage 2026 (published March 2026).
  This is the state's own demographic baseline. It is a <strong>county</strong> projection and cannot be
  attributed to a neighbourhood.</p>
  {B.data_table([r for r in ds.ROWS if r[1]=='projections'], 'proj-table', 'Official projection rows. Derived percentages show their formula in the note.')}
</section>

<section class="panel" id="divergence">
  <div class="hd"><div><p class="eyebrow">The single most important chart on this site</p><h2>The county shrinks while the state grows</h2></div></div>
  <div class="grid g3">
    <div class="card"><div class="k">Los Angeles County, 2025 → 2035</div><div class="v" style="color:#8c2f19">−1.47%</div>
      <div class="m">9,853,435 → 9,708,647 (DOF P-2A)</div></div>
    <div class="card"><div class="k">California, 2025 → 2035</div><div class="v" style="color:#1d6b45">+2.23%</div>
      <div class="m">39,528,899 → 40,410,843 (DOF P-2A)</div></div>
    <div class="card"><div class="k">County decline 2030 → 2035</div><div class="v">−0.19%</div>
      <div class="m">The decline decelerates but does not reverse</div></div>
  </div>
  <p class="small" style="margin-bottom:0">Both percentages are computed here from the published DOF series; the
  formula is in each row's note. The implication for the property is <em>not</em> that the location is doomed.
  It is that a restaurant whose sales depend on local volume cannot rely on catchment growth to bail it out,
  so the value of this asset rests on the parcel and the lease rather than on the market.</p>
</section>

<section class="panel" id="projection-system">
  <div class="hd"><div><p class="eyebrow">Projection system</p><h2>What can be projected, and from what</h2></div></div>
  <p class="small muted" style="margin-top:0">A projection is only as good as its official input. Where no
  official projection exists at the required geography, this brief publishes the current level and says so,
  rather than manufacturing a trend line.</p>
  {proj_table}
</section>

<section class="panel" id="model">
  <div class="hd"><div><p class="eyebrow">Scenario model</p><h2>Hold versus sell, in index units</h2></div>
  {source_link('fredDgs10', 'Risk-free rate basis ↗')}</div>
  <p class="small muted" style="margin-top:0">No rent, price or cap rate for this asset is public, so the model
  runs in <strong>index units</strong>: one year of current rent = 100 units. Every output is a ratio, which is
  valid for comparing paths and invalid as a valuation. It answers one question: <em>how much has to be assumed
  for the hold case to beat the sell case?</em></p>
  <div class="tablewrap"><table id="model-grid">
  <caption>Present value of the rent stream plus residual, {M['years']}-year hold, per 100 units of current annual rent.</caption>
  <thead><tr><th scope="col">Renewal rent growth</th>{rate_heads}</tr></thead>
  <tbody>{grid_html}</tbody></table></div>
  <div class="grid g3" style="margin-top:14px">
    <div class="card"><div class="k">Hold case, base assumptions</div><div class="v">{M['pv_with_residual']:,.0f}</div>
      <div class="m">5% rent growth · 7% discount · {M['residual_multiple']:.0f}× exit multiple</div></div>
    <div class="card"><div class="k">Sell case, net proceeds</div><div class="v">{M['net_proceeds_units']:,.0f}</div>
      <div class="m">{M['gross_multiple']:.0f}× gross, less {M['transfer_tax']*100:.2f}% transfer tax and {M['commission']*100:.0f}% commission</div></div>
    <div class="card"><div class="k">Hold-to-sell ratio</div><div class="v">{M['hold_advantage']:.2f}×</div>
      <div class="m">Above 1.0 the hold case wins on these assumptions</div></div>
  </div>
  <div class="callout warn" style="margin-top:14px">
    <b>The honest break-even</b>
    On the base assumptions the hold case needs the exit multiple in 2035 to be at least
    <strong>{M['break_even_multiple']:.1f}×</strong> the year-{M['years']} rent for the hold present value to match
    the net proceeds of selling today. That is a plausible multiple, which is why the answer is not obvious — and
    why the recommendation is to keep both paths open rather than to commit to either on the current data.
    {pct(M['residual_share'],0)} of the hold case's present value comes from the residual, so the exit assumption
    dominates the result. An owner who believes the residual will be weak should sell.
  </div>
</section>

<section class="panel" id="assumptions">
  <div class="hd"><div><p class="eyebrow">Transparency</p><h2>Every model assumption, named</h2></div></div>
  <div class="tablewrap"><table id="assump">
  <caption>These are assumptions, not facts. Each one is a lever; change it and the answer moves.</caption>
  <thead><tr><th scope="col">Ref</th><th scope="col">Assumption</th><th scope="col">Value used</th><th scope="col">Why</th></tr></thead>
  <tbody>{"".join(f"<tr><td class='id'>{esc(a)}</td><td>{esc(b)}</td><td class='num'>{esc(c)}</td><td class='note'>{esc(d)}</td></tr>" for a,b,c,d in an.ASSUMPTIONS)}</tbody>
  </table></div>
</section>
"""
    return B.layout("projections.html", "Projections &amp; model | Jack in the Box NNN decision brief", body,
                    "California Department of Finance projections for Los Angeles County to 2035, plus the scenario model's assumptions and break-even.")


# =========================================================== tenant
TENANT_CAPTION = ("Tenant and brand rows. Values are as filed with the SEC; "
                  "guidance is management's own forward-looking statement.")


def page_tenant():
    rows = B.rows_for("tenant")
    body = f"""
<section class="hero">
  <p class="eyebrow">Tenant credit</p>
  <h1>The logo is not the obligor.</h1>
  <p class="lede">A Jack in the Box sign over the door tells you the brand, not who owes the rent. The company's
  own 10-K states that for a majority of franchised sites it leases or subleases the real property
  <em>to the franchisee</em>. So the landlord's counterparty could be the brand, a franchisee, or a brand
  affiliate that subleases. Which one it is here is the largest unverified input in this brief — and it changes
  the credit quality of the rent more than any market statistic on this site.</p>
  <div class="grid g4" style="margin-top:16px">
    <div class="card"><div class="k">System restaurants</div><div class="v">2,136</div>
      <div class="m">September 28, 2025 · 93% franchised</div></div>
    <div class="card"><div class="k">FY2025 same-store sales</div><div class="v" style="color:#8c2f19">−4.2%</div>
      <div class="m">Q4 alone was −7.4%</div></div>
    <div class="card"><div class="k">FY2025 net unit change</div><div class="v">−55</div>
      <div class="m">31 opened against 86 closed</div></div>
    <div class="card"><div class="k">Guided FY2026 closures</div><div class="v">50–100</div>
      <div class="m">Most expected to be franchise units</div></div>
  </div>
</section>

<section class="panel">
  <div class="hd"><div><p class="eyebrow">Credit assessment in one paragraph</p><h2>What the filings add up to</h2></div></div>
  <div class="grid g2">
    <div class="callout ok">
      <b>Arguments that the rent is safe</b>
      <ul class="clean" style="margin-bottom:0">
        <li>A national brand with 2,136 restaurants across 21 states and a 75-year operating history.</li>
        <li>The prototype box is small and cheap to operate, and the drive-thru entitlement is scarce in built-out Los Angeles.</li>
        <li>Rent is typically a modest share of restaurant sales for quick-service units, so a unit can stay profitable through a sales decline.</li>
        <li>Guide-level Adjusted EBITDA of $225–240m for FY2026 is a solvent enterprise.</li>
      </ul>
    </div>
    <div class="callout bad">
      <b>Arguments that the rent is at risk</b>
      <ul class="clean" style="margin-bottom:0">
        <li>Same-store sales deteriorating into the fourth quarter of FY2025 (−7.4%).</li>
        <li>Net closures of 55 units in one year, with 50–100 more guided.</li>
        <li>The dividend was discontinued — cash is being conserved.</li>
        <li>Management states its plan includes <strong>selling real estate</strong>: the counterparty is monetising property, not adding it.</li>
        <li>An active proxy contest with an activist shareholder, disclosed in the 10-K.</li>
        <li>~70% of the system sits in California and Texas, which the company itself flags as a concentration.</li>
      </ul>
    </div>
  </div>
  <p class="small" style="margin-top:14px;margin-bottom:0"><strong>Balance:</strong> the enterprise is solvent;
  the <em>site</em> is not guaranteed. A brand can be healthy and still close a specific underperforming unit —
  and a closure list of 50–100 sites a year is exactly the mechanism by which that happens. Underwriting the
  site means underwriting the operator's unit-level economics, which are not public.</p>
</section>

<section class="panel">
  <div class="hd"><div><p class="eyebrow">Franchise terms</p><h2>Why a 20-year franchise term is not a 20-year lease</h2></div></div>
  <p class="small" style="margin-top:0">The company's standard <em>franchise</em> agreement runs 20 years with a
  $50,000 initial fee and a 5.0% royalty. A landlord reading "20-year term" could wrongly assume a 20-year rent
  obligation. The franchise agreement is between the brand and the operator. The <em>lease</em> is a separate
  contract with separate dates, and its term may be shorter, longer, or renewed on different cycles. The
  owner's stated 2030–2035 expiry window is the lease, not the franchise agreement.</p>
</section>

<section class="panel">
  <div class="hd"><div><p class="eyebrow">Source data</p><h2>Every tenant row, with the filing it came from</h2></div></div>
  {B.data_table(rows, 'tenant-table', TENANT_CAPTION)}
</section>
"""
    return B.layout("tenant.html", "Tenant credit | Jack in the Box NNN decision brief", body,
                    "Jack in the Box Inc. SEC disclosures: restaurant counts, same-store sales, closures, guidance and real-estate strategy.")


# =========================================================== property
def page_property():
    prop = B.rows_for("property")
    haz = B.rows_for("hazards")
    body = f"""
<section class="hero">
  <p class="eyebrow">Property &amp; hazards</p>
  <h1>Eleven private facts are doing all the work.</h1>
  <p class="lede">The recommendation on this site depends on facts that are not public and were not supplied:
  the lease, the counterparty, the rent, the options, the basis and the parcel. Those fields are marked
  <em>[WITHHELD]</em> or left blank. This page sets out exactly what is needed and why each item changes the
  answer, so the owner can assemble it in one pass.</p>
</section>

<div class="grid g3">
  <div class="callout"><b>What the box actually is</b>A 1,372 sq ft prototype with a Y-lane drive-thru on a
  commercially zoned parcel. The building is not the value; the land and the conditional-use entitlement for a
  drive-thru are.</div>
  <div class="callout"><b>What the lease actually is</b>An absolute-net lease shifts tax, insurance and
  maintenance to the tenant while the term runs. It does not shift them forever; after expiry they come back.</div>
  <div class="callout"><b>What the parcel actually is</b>Unknown for hazard purposes. The Fire Hazard Severity
  Zone, the Alquist-Priolo status and the flood zone are all parcel-level queries that require an address.</div>
</div>

<section class="panel" id="property-rows">
  <div class="hd"><div><p class="eyebrow">Asset-specific fields</p><h2>Lease and parcel</h2></div>
  <span class="pill held">Withheld or unverified</span></div>
  <p class="small muted" style="margin-top:0">Nothing in this table is estimated. <em>[WITHHELD]</em> means the
  information exists but is private and deliberately not published. An em dash means the value could not be
  confirmed from an official source.</p>
  {B.data_table(prop, 'property-table', 'Property and lease fields. Private values are withheld; unverified values are blank and flagged.')}
</section>

<section class="panel" id="hazards">
  <div class="hd"><div><p class="eyebrow">Catastrophe</p><h2>Realised severity, not assigned probability</h2></div>
  {source_link('usgs', 'USGS ShakeOut ↗')}</div>
  <p class="small" style="margin-top:0">This brief assigns <strong>no probability</strong> to any hazard for this
  parcel. Doing so would require data that does not exist at parcel level, and any number would be fabricated.
  What is published is what a realised event looked like, so the owner can size the tail without being sold a
  false precision.</p>
  <div class="grid g3" style="margin-bottom:16px">
    <div class="card"><div class="k">Palisades Fire, structures destroyed</div><div class="v">6,845</div>
      <div class="m">+975 damaged · 12 fatalities · 23,448 acres</div></div>
    <div class="card"><div class="k">ShakeOut scenario, total loss</div><div class="v">$191bn</div>
      <div class="m">Mw 7.8 southern San Andreas · modelled</div></div>
    <div class="card"><div class="k">FAIR Plan commercial limit</div><div class="v">$20m</div>
      <div class="m">Per building · insurer of last resort</div></div>
  </div>
  {B.data_table(haz, 'hazard-table', 'Hazard rows: published event and scenario figures, plus the parcel checks that remain open.')}
</section>

<section class="panel" id="hazard-logic">
  <div class="hd"><div><p class="eyebrow">How to read the tail</p><h2>Three channels, three different answers</h2></div></div>
  <ol class="steps">
    <li><strong>Direct physical damage.</strong> A single-storey, 1,372 sq ft box on a surface parking field is
    at the resilient end of building stock. Shaking damage is real but unlikely to be structural
    collapse. The mitigation is the tenant's insurance and the lease's casualty clause.</li>
    <li><strong>Business interruption.</strong> A closed store stops generating sales, and a sales-based
    percentage-rent clause (if any) stops paying. Under a true NNN lease, base rent normally continues, and the
    tenant — not the landlord — carries the interruption cover. Confirm this in the lease.</li>
    <li><strong>Insurance-market contagion.</strong> This is the channel that actually threatens value. The
    Palisades Fire did not touch central Los Angeles, but a regional event reprices cover across the region,
    and the Department of Insurance itself describes insurers withdrawing as FAIR Plan enrolment grows. A parcel
    that cannot be insured cannot easily be sold or financed.</li>
  </ol>
  <div class="callout warn" style="margin-top:12px"><b>The check that costs the least and tells you the most</b>
  Get a current commercial property insurance quote for the parcel this month. Under an NNN lease the tenant pays
  it, so the quote is diagnostic rather than a cost to the owner — and it is the fastest way to find out whether
  this asset is in a market at all.</div>
</section>
"""
    return B.layout("property.html", "Property &amp; hazards | Jack in the Box NNN decision brief", body,
                    "Lease and parcel fields for the subject property, withheld where private and blank where unverified, plus hazard severity references.")


# =========================================================== decision
def page_decision():
    path_cards = []
    for p in an.PATHS:
        verify = ", ".join(ref(v) for v in p["verify_first"])
        path_cards.append(f"""
<article class="card" id="path-{p['id']}">
  <div class="k">{esc(p['summary'])}</div>
  <h2 style="margin:4px 0 10px">{esc(p['name'])}</h2>
  <dl class="kv">
    <dt>Keeps</dt><dd>{p['keeps']}</dd>
    <dt>Gives up</dt><dd>{p['gives_up']}</dd>
    <dt>Costs</dt><dd>{p['costs']}</dd>
    <dt>Best if</dt><dd>{p['best_if']}</dd>
    <dt>Fails if</dt><dd>{p['fails_if']}</dd>
    <dt>Verify first</dt><dd>{verify}</dd>
  </dl>
</article>""")

    body = f"""
<section class="hero">
  <p class="eyebrow">Decision paths</p>
  <h1>Four paths. One recommendation, with the conditions attached.</h1>
  <p class="lede">Selling, renewing, holding to expiry and exchanging are not ranked by price — they are ranked by
  what they do to the owner's wealth and options. The ranking below follows from the official data plus one
  judgement: in a county that is losing population and a tenant that is closing units, <strong>term is worth
  more than price</strong>.</p>
  <div class="verdict" style="margin-top:16px">
    <p class="eyebrow">Recommendation</p>
    <h2>1. Renew, then decide — preferred</h2>
    <p style="margin:6px 0 0">Secure a long extension at a rent no lower than today, with a creditworthy
    guaranty, in exchange for defined landlord capital. Then sell the re-rated asset when the owner chooses, not
    when the lease forces it. <strong>Fallback:</strong> if the tenant will not extend on acceptable terms by a
    pre-committed date, sell — and sell to a §1031 buyer if the basis is low. <strong>Rejected:</strong> holding
    to expiry with no re-use plan, because a dark box on an entitled parcel in a shrinking county is the worst
    of the four outcomes.</p>
  </div>
</section>

<section class="panel" id="after-tax">
  <div class="hd"><div><p class="eyebrow">The arithmetic everyone skips</p><h2>Net proceeds are not the sale price</h2></div>
  {source_link('lafinanceUla', 'LA Office of Finance ↗')}</div>
  <p class="small muted" style="margin-top:0">Published rates only. The percentages below are from the City of
  Los Angeles Office of Finance; brokerage and income tax are named as assumptions because no official source
  publishes them for a private owner.</p>
  <div class="tablewrap"><table id="proceeds">
  <caption>Illustrative deduction stack. The $6.5m price is a placeholder chosen to sit inside the lower ULA band; it is not a valuation of this asset.</caption>
  <thead><tr><th scope="col">Line</th><th scope="col">Basis</th><th scope="col">Amount on a $6,500,000 price</th><th scope="col">Source</th></tr></thead>
  <tbody>
    <tr><td>Gross sale price</td><td>Placeholder for illustration</td><td class="num">$6,500,000</td><td class="src">—</td></tr>
    <tr><td>City transfer tax (base + ULA)</td><td>4.45% in the $5.4m–$10.9m band</td><td class="num">−$289,250</td>
      <td class="src">{source_link('lafinanceUla', 'LA Finance ↗')}</td></tr>
    <tr><td>Brokerage commission</td><td>4.0% (assumption A-08)</td><td class="num">−$260,000</td><td class="src">Assumption</td></tr>
    <tr><td>Loan payoff / defeasance</td><td>Unknown — withheld (PR-21)</td><td class="num">—</td><td class="src">Owner data</td></tr>
    <tr><td>Federal and California tax on gain</td><td>Depends on basis (withheld, PR-22) and owner's rate</td><td class="num">—</td><td class="src">{source_link('irsP544', 'IRS Pub. 544 ↗')}</td></tr>
    <tr><td><strong>Net before income tax</strong></td><td>Price less known transaction costs</td><td class="num"><strong>≈ $5,950,750</strong></td><td class="src">Computed</td></tr>
  </tbody></table></div>
  <div class="callout warn" style="margin-top:12px"><b>Two traps in this arithmetic</b>
  First, the ULA thresholds are indexed annually to the Chained CPI, so the 4.45% band moves — re-check before
  any letter of intent. Second, the income-tax line is usually the largest single deduction, and it is the one
  the owner controls through basis, structure and timing. No rate is asserted for it here because the owner's
  position is private and unknown.</div>
</section>

<section class="panel" id="tax">
  <div class="hd"><div><p class="eyebrow">Tax &amp; regulation</p><h2>Every rate and threshold that affects the arithmetic</h2></div></div>
  <p class="small muted" style="margin-top:0">Each row links to the page it was read from. Rows that could not be
  confirmed are blank and listed on <a href="flagged.html">Flagged for review</a> — including the state treatment of
  the gain, which this brief deliberately does not quote a rate for.</p>
  {B.data_table(B.rows_for('tax'), 'tax-table', 'Tax and regulatory rows: transaction costs, assessment rules, wage floors and exchange eligibility.')}
</section>

<section class="panel" id="capital">
  <div class="hd"><div><p class="eyebrow">Capital markets</p><h2>The rate that sets the buyer's floor</h2></div></div>
  <p class="small muted" style="margin-top:0">The only official number available here is the risk-free rate. No
  official source publishes a cap rate for an individual single-tenant restaurant, so no cap rate appears on this
  site — a broker survey is not an official source.</p>
  {B.data_table(B.rows_for('capital'), 'capital-table', 'Capital-market rows: the published risk-free rate, and the valuation inputs that cannot be sourced officially.')}
</section>

<section class="panel" id="paths">
  <div class="hd"><div><p class="eyebrow">Path by path</p><h2>The four options, with what each one costs</h2></div></div>
  <div class="grid g2">{''.join(path_cards)}</div>
</section>

<section class="panel" id="matrix">
  <div class="hd"><div><p class="eyebrow">Trade-off matrix</p><h2>Which path wins on which objective</h2></div></div>
  <div class="tablewrap"><table id="matrix-table">
  <caption>Qualitative scoring against each objective, derived from the analysis above. Not a numeric score.</caption>
  <thead><tr><th scope="col">Objective</th><th scope="col">Sell now</th><th scope="col">Renew, then decide</th><th scope="col">Hold to expiry</th><th scope="col">Sell &amp; §1031</th></tr></thead>
  <tbody>
    <tr><td>Immediate liquidity</td><td><span class="pill ok">Best</span></td><td><span class="pill neutral">Low</span></td><td><span class="pill bad">Worst</span></td><td><span class="pill ok">Good</span></td></tr>
    <tr><td>Preserves rental income</td><td><span class="pill bad">Ends it</span></td><td><span class="pill ok">Yes</span></td><td><span class="pill neutral">Until expiry</span></td><td><span class="pill neutral">Replaced</span></td></tr>
    <tr><td>Preserves Prop 13 basis</td><td><span class="pill bad">Loses it</span></td><td><span class="pill ok">Keeps it</span></td><td><span class="pill ok">Keeps it</span></td><td><span class="pill bad">Loses it</span></td></tr>
    <tr><td>Defers tax on the gain</td><td><span class="pill bad">No</span></td><td><span class="pill ok">Yes</span></td><td><span class="pill ok">Yes</span></td><td><span class="pill ok">Yes, if executed</span></td></tr>
    <tr><td>Removes single-tenant concentration</td><td><span class="pill ok">Immediately</span></td><td><span class="pill bad">Increases it</span></td><td><span class="pill bad">No</span></td><td><span class="pill ok">Yes</span></td></tr>
    <tr><td>Exposure to a tenant closure</td><td><span class="pill ok">Transferred</span></td><td><span class="pill bad">Retained</span></td><td><span class="pill bad">Held through expiry</span></td><td><span class="pill ok">Transferred</span></td></tr>
    <tr><td>Execution risk</td><td><span class="pill neutral">Market timing</span></td><td><span class="pill ok">Lowest</span></td><td><span class="pill bad">Highest</span></td><td><span class="pill bad">Deadline pressure</span></td></tr>
    <tr><td>Needs the counterparty to cooperate</td><td><span class="pill ok">No</span></td><td><span class="pill bad">Yes</span></td><td><span class="pill ok">No</span></td><td><span class="pill ok">No</span></td></tr>
  </tbody></table></div>
</section>

<section class="panel" id="trigger">
  <div class="hd"><div><p class="eyebrow">Pre-commitment</p><h2>The sell trigger, written down before it is needed</h2></div></div>
  <p class="small" style="margin-top:0">A decision made under pressure at expiry is a bad decision. The owner
  should write the trigger now, while calm. A workable set:</p>
  <ol class="steps">
    <li><strong>Renewal test.</strong> If the tenant has not signed an extension of at least 10 years, at a rent
    no lower than today, with a creditworthy guaranty, by <em>[date 30 months before expiry]</em>, then the asset
    is listed for sale.</li>
    <li><strong>Insurance test.</strong> If a commercial property quote for the parcel exceeds <em>[owner's
    threshold]</em>, or cover cannot be bound on standard terms, then the asset is listed for sale.</li>
    <li><strong>Capital test.</strong> If required landlord capital at renewal (roof, HVAC, drive-thru, ADA)
    exceeds <em>[owner's threshold]</em>, the sale case is re-run before agreeing.</li>
    <li><strong>Personal test.</strong> If liquidity is needed inside 36 months, the sale case dominates and the
    market view is secondary.</li>
    <li><strong>Buyer test.</strong> If a credible unsolicited offer arrives at or above the after-tax hold value
    computed on <a href="projections.html#model">the model page</a>, take it seriously rather than treating it as a
    floor to negotiate from.</li>
  </ol>
</section>
"""
    return B.layout("decision.html", "Decision paths | Jack in the Box NNN decision brief", body,
                    "Sell, renew, hold or exchange: costs, trade-offs, net-proceeds arithmetic and a pre-committed sell trigger.")


# =========================================================== risks
def page_risks():
    order = {"Business as usual": 0, "Black swan": 1, "Personal": 2}
    risks = sorted(an.RISKS, key=lambda r: (order.get(r[2], 9), r[0]))
    cards = []
    for rid, title, cls, trig, mech, mit, so, resid in risks:
        tag = {"Business as usual": "ba", "Black swan": "bs", "Personal": "personal"}.get(cls, "")
        cards.append(f"""
<article class="card" id="{esc(rid)}" style="margin-bottom:14px">
  <div style="display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;margin-bottom:6px">
    <span class="pill neutral">{esc(rid)}</span>
    <span class="tag {tag}">{esc(cls)}</span>
    <h2 style="margin:0;font-size:17px">{esc(title)}</h2>
  </div>
  <dl class="kv">
    <dt>Trigger evidence</dt><dd>{trig}</dd>
    <dt>How it reaches the owner</dt><dd>{mech}</dd>
    <dt>Mitigation</dt><dd>{mit}</dd>
    <dt>Residual exposure</dt><dd>{esc(resid)}</dd>
  </dl>
  <p class="small" style="margin:8px 0 0;padding-top:8px;border-top:1px solid var(--line)">
  <strong>So what:</strong> {so}</p>
</article>""")

    counts = {}
    for r in an.RISKS:
        counts[r[2]] = counts.get(r[2], 0) + 1

    matrix_rows = "".join(
        f"<tr><td class='id'>{esc(r[0])}</td><td>{esc(r[1])}</td><td><span class='tag "
        f"{'ba' if r[2]=='Business as usual' else 'bs' if r[2]=='Black swan' else 'personal'}'>{esc(r[2])}</span></td>"
        f"<td class='note'>{esc(r[7])}</td></tr>"
        for r in risks)

    body = f"""
<section class="hero">
  <p class="eyebrow">Risk register</p>
  <h1>{len(an.RISKS)} risks, ranked by whether the owner can act on them.</h1>
  <p class="lede">Two of these risks — the counterparty's identity and the lease's terms — dominate everything
  else on this page. A catastrophe model on a parcel whose lease you have not read is decoration. The register is
  therefore ordered by <em>controllability</em>, not by drama: what the owner can negotiate, then what the market
  will do to them, then the tail that nobody can price.</p>
  <div class="grid g3" style="margin-top:16px">
    <div class="card"><div class="k">Business as usual</div><div class="v">{counts.get('Business as usual',0)}</div>
      <div class="m">High-probability, manageable, mostly negotiable</div></div>
    <div class="card"><div class="k">Black swan</div><div class="v">{counts.get('Black swan',0)}</div>
      <div class="m">Low-probability, high-severity. No probability assigned</div></div>
    <div class="card"><div class="k">Personal</div><div class="v">{counts.get('Personal',0)}</div>
      <div class="m">Owner-specific and, in practice, often decisive</div></div>
  </div>
</section>

<div class="callout warn">
  <b>The honest limitation on this register</b>
  No probability is attached to any black-swan event for this parcel. Parcel-level hazard data requires an
  address that is withheld, and no official source publishes a per-parcel event probability. The register
  describes <em>how</em> each event would reach the owner's cash flow and what to check, which is actionable.
  Inventing a probability would not be.
</div>

<section class="panel" style="margin-top:18px">
  <div class="hd"><div><p class="eyebrow">Summary matrix</p><h2>Every risk at a glance</h2></div></div>
  <div class="tablewrap"><table id="risk-matrix">
  <caption>Full register. Detail for each item follows below.</caption>
  <thead><tr><th scope="col">Ref</th><th scope="col">Risk</th><th scope="col">Class</th><th scope="col">Residual exposure</th></tr></thead>
  <tbody>{matrix_rows}</tbody></table></div>
</section>

<section class="panel">
  <div class="hd"><div><p class="eyebrow">Detail</p><h2>Trigger, transmission and mitigation</h2></div></div>
  {''.join(cards)}
</section>
"""
    return B.layout("risks.html", "Risk register | Jack in the Box NNN decision brief", body,
                    "Sixteen property risks: business-as-usual, black swan and personal, with transmission mechanics and mitigations.")


# =========================================================== flagged
def page_flagged():
    unver = [r for r in ds.ROWS if r[8] == "unverified"]
    held = [r for r in ds.ROWS if r[8] == "withheld"]

    f_rows = []
    for i, r in enumerate(unver, start=1):
        anchor = f"F-{i:02d}"
        f_rows.append((anchor, r))
    f_html = "".join(
        f"""<tr id="{a}"><td class="id">{a}</td><td class="id">{esc(r[0])}</td><td>{esc(r[2])}</td>
        <td class="small">{esc(r[6])}</td><td class="blank">—</td>
        <td>{status_pill('unverified')}</td>
        <td class="note">{esc(r[9])}</td>
        <td class="src">{source_link(r[7], 'Lookup')}</td></tr>"""
        for a, r in f_rows)

    h_html = "".join(
        f"<tr id='{esc(r[0].lower())}'><td class='id'>{esc(r[0])}</td><td>{esc(r[2])}</td>"
        f"<td class='blank'>[WITHHELD]</td><td class='note'>{esc(r[9])}</td></tr>"
        for r in held)

    body = f"""
<section class="hero">
  <p class="eyebrow">Flagged for review</p>
  <h1>{len(unver)} unverified values and {len(held)} withheld fields.</h1>
  <p class="lede">This page exists so that nothing on this site is quietly assumed. Every row below is either a
  value that could not be confirmed from an official source (and is therefore blank) or a private field that is
  deliberately not published. Each one names what would close it and which official lookup would do it.</p>
  <div class="actions">
    <a class="btn ghost" href="#unverified">Unverified values ({len(unver)})</a>
    <a class="btn ghost" href="#withheld">Withheld fields ({len(held)})</a>
    <a class="btn ghost" href="#conflicts">Source conflicts</a>
  </div>
</section>

<section class="panel" id="unverified">
  <div class="hd"><div><p class="eyebrow">Cannot be confirmed officially</p><h2>Unverified values, left blank by rule</h2></div>
  <span class="pill bad">Blank, not estimated</span></div>
  <p class="small muted" style="margin-top:0">A blank here is a finding, not an omission. For most of these rows
  the value exists in the owner's files or requires a parcel query; a few genuinely have no official public
  source at this geography, and for those no value will ever be published on this site.</p>
  <div class="tablewrap"><table id="flagged-table">
  <caption>Every unverified row. The "lookup" column links to the official tool or page that could resolve it.</caption>
  <thead><tr><th scope="col">Flag</th><th scope="col">Ref</th><th scope="col">Metric</th><th scope="col">Geography</th>
  <th scope="col">Value</th><th scope="col">Status</th><th scope="col">What would close it</th><th scope="col">Official lookup</th></tr></thead>
  <tbody>{f_html}</tbody></table></div>
</section>

<section class="panel" id="withheld">
  <div class="hd"><div><p class="eyebrow">Privacy</p><h2>Withheld fields, never published</h2></div>
  <span class="pill held">Internal use only</span></div>
  <p class="small muted" style="margin-top:0">These fields are private. They are listed so the owner knows what they
  are, not so their values can be inferred. Nothing in this repository, its data files or its pages contains an
  owner name, a street address, a parcel number, an ownership entity, a rent figure, a loan figure, a cost basis
  or any personal financial detail.</p>
  <div class="tablewrap"><table id="withheld-table">
  <caption>Withheld fields and why each one matters to the decision.</caption>
  <thead><tr><th scope="col">Ref</th><th scope="col">Field</th><th scope="col">Value</th><th scope="col">Why it matters</th></tr></thead>
  <tbody>{h_html}</tbody></table></div>
</section>

<section class="panel" id="conflicts">
  <div class="hd"><div><p class="eyebrow">Integrity</p><h2>Official sources that disagree, and defects found</h2></div></div>
  <p class="small muted" style="margin-top:0">Where two official sources conflict, both are published and the
  conflict is named. Neither is discarded and neither is averaged.</p>
  <div class="tablewrap"><table id="conflict-table">
  <caption>Conflicts and corrected defects. All are also recorded in verification/VERIFICATION-LOG.md.</caption>
  <thead><tr><th scope="col">Ref</th><th scope="col">Issue</th><th scope="col">Resolution</th></tr></thead>
  <tbody>
    <tr><td class="id">F-06</td><td>Los Angeles County 2025 building permits: Census QuickFacts shows
      <strong>22,250</strong>; the State EDD profile shows <strong>20,192</strong> construction permits for the same
      year and county.</td><td>Both published as separate rows (H-09, H-10). They count different things — permit
      documents versus permitted units — and the two pages are different publications. No figure is netted or
      chosen.</td></tr>
    <tr><td class="id">D-15</td><td>An earlier build of this repository published county population density as
      blank, stating the value was "not displayed" on QuickFacts.</td><td><strong>Defect corrected.</strong>
      QuickFacts does publish it: <strong>2,466.9</strong> per square mile. It is now a verified row.</td></tr>
    <tr><td class="id">I-02</td><td>An earlier build substituted a FRED SAIPE figure for county median household
      income, stating QuickFacts did not display one.</td><td><strong>Defect corrected.</strong> QuickFacts
      publishes <strong>$90,112</strong> for 2020–2024. Both that and the SAIPE 2024 figure ($90,757) are now
      published as separate rows, with the difference between the series stated.</td></tr>
    <tr><td class="id">I-07</td><td>An earlier build labelled city poverty as a "2025 estimate".</td>
      <td><strong>Defect corrected.</strong> The Census methodology note states sub-county poverty comes from ACS
      5-year data, so the period is <strong>2020–2024</strong>.</td></tr>
    <tr><td class="id">X-01</td><td>An earlier build cited the City Attorney's <em>homelessness</em> page as the
      source for the 4.0% and 5.5% Measure ULA rates. That page does not contain the rates.</td>
      <td><strong>Defect corrected.</strong> The rates and the current dollar thresholds are now sourced to the
      City of Los Angeles Office of Finance, which publishes them, and the thresholds are labelled as annually
      indexed.</td></tr>
    <tr><td class="id">X-12</td><td>An earlier build cited the state DIR page for a "City of Los Angeles minimum
      wage (2026)" row.</td><td><strong>Defect corrected.</strong> The DIR page covers the state fast-food wage
      under AB 1228, not a city minimum wage. The row is blank and flagged rather than filled.</td></tr>
    <tr><td class="id">PR-04</td><td>The owner describes the lease as triple-net. No lease document has been
      reviewed.</td><td>Recorded as <em>[WITHHELD]</em>, not as <em>verified</em>. An NNN label asserted by an
      owner and an NNN label read from a lease are different levels of evidence.</td></tr>
  </tbody></table></div>
</section>
"""
    return B.layout("flagged.html", "Flagged for review | Jack in the Box NNN decision brief", body,
                    "Every unverified and withheld item in the dataset, the official lookup that would close it, and the source conflicts found.")


# =========================================================== sources
def page_sources():
    src_rows = []
    used_by = {}
    for r in ds.ROWS:
        used_by.setdefault(r[7], []).append(r[0])
    for key, (pub, title, url) in ds.SOURCES.items():
        ids = used_by.get(key, [])
        tools = "Official lookup tool" if key in ds.TOOLS else "Statistical / filing source"
        src_rows.append(
            f"<tr><td><strong>{esc(pub)}</strong></td><td>{esc(title)}</td>"
            f"<td class='small'>{esc(tools)}</td><td class='id'>{len(ids)}</td>"
            f"<td class='src'><a href='{esc(url)}' target='_blank' rel='noopener noreferrer'>Open ↗</a></td></tr>")
    src_html = "".join(src_rows)

    body = f"""
<section class="hero">
  <p class="eyebrow">Sources &amp; method</p>
  <h1>{len(ds.SOURCES)} official sources. Nothing else.</h1>
  <p class="lede">Every value on this site was read on the page linked below during this session, and the figure
  was compared character by character against what the page displayed. Where the page did not publish a value,
  no value was published here. Reproduced excerpts for each source are committed under
  <code>verification/captures/</code> so the reading can be audited without re-fetching.</p>
</section>

<section class="panel" id="register">
  <div class="hd"><div><p class="eyebrow">Register</p><h2>Every source used, and how many rows depend on it</h2></div></div>
  <div class="tablewrap"><table id="source-table">
  <caption>Official publishers only: government bodies, central-bank and Federal Reserve data, and the registrant's own SEC filings.</caption>
  <thead><tr><th scope="col">Publisher</th><th scope="col">Document</th><th scope="col">Type</th><th scope="col">Rows</th><th scope="col">Link</th></tr></thead>
  <tbody>{src_html}</tbody></table></div>
</section>

<section class="panel" id="rules">
  <div class="hd"><div><p class="eyebrow">Rules</p><h2>The verification rules this site is built on</h2></div></div>
  <ol class="steps">
    <li><strong>One row, one sourced metric.</strong> No row aggregates several figures or blends periods.</li>
    <li><strong>Verified means read.</strong> The value was displayed on the cited official page during this
    session and is reproduced in <code>verification/captures/</code>.</li>
    <li><strong>Derived means arithmetic, and the formula is shown.</strong> Derived rows list both operands and
    the operation in the note. {C['derived']} rows are derived.</li>
    <li><strong>Unverified means blank.</strong> If an official source does not publish the value, the cell shows
    an em dash. No estimate, no interpolation, no third-party aggregator, no "approximately". {C['unverified']} rows
    are blank on this basis and are listed on <a href="flagged.html">Flagged for review</a>.</li>
    <li><strong>Withheld means private.</strong> Owner, address, parcel, rent, loan and basis data are never
    published. {C['withheld']} rows are withheld.</li>
    <li><strong>Conflicts are published, not resolved by preference.</strong> Where two official sources differ,
    both appear and the difference is named.</li>
    <li><strong>Assumptions are labelled.</strong> The scenario model runs on seven named assumptions (A-01 to
    A-08) on <a href="projections.html#assumptions">the model page</a>. No assumption is presented as data.</li>
  </ol>
  <div class="callout" style="margin-top:12px"><b>What this site is not</b>
  It is not an appraisal, a broker opinion of value, a tax opinion, or a personal financial recommendation.
  It does not know the owner's basis, debt, liquidity needs, estate plan or risk tolerance, and it does not ask.
  Those private factors can override every conclusion here.</div>
</section>

<section class="panel" id="audit">
  <div class="hd"><div><p class="eyebrow">Audit trail</p><h2>Where to check the work</h2></div></div>
  <dl class="kv">
    <dt>Reproduced excerpts</dt><dd><code>verification/captures/</code> — one file per source family, with the exact
      published figures and the retrieval date.</dd>
    <dt>Line-by-line log</dt><dd><code>verification/VERIFICATION-LOG.md</code> — every row, its value, and the result
      of the check.</dd>
    <dt>Dataset</dt><dd><code>scripts/dataset.py</code> — the single source of truth for every table on this site.</dd>
    <dt>Analysis</dt><dd><code>scripts/analysis.py</code> — the risk register, the four paths, the assumptions and the model.</dd>
    <dt>Automated gate</dt><dd><code>scripts/check_site.py</code> — fails the build if any table row lacks an official
      source link, if any unverified row carries a value, or if any internal link is broken.</dd>
    <dt>Coordination</dt><dd><code>COORDINATION.md</code> — the shared task board, including prior sessions' boards
      preserved verbatim.</dd>
  </dl>
</section>
"""
    return B.layout("sources.html", "Sources &amp; method | Jack in the Box NNN decision brief", body,
                    "Every official source used, the verification rules applied, and the audit trail for each figure.")


def main():
    pages = {
        "index.html": page_index,
        "market.html": page_market,
        "projections.html": page_projections,
        "tenant.html": page_tenant,
        "property.html": page_property,
        "decision.html": page_decision,
        "risks.html": page_risks,
        "flagged.html": page_flagged,
        "sources.html": page_sources,
    }
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    (assets / "favicon.svg").write_text(FAVICON)
    for name, fn in pages.items():
        html_out = fn()
        (ROOT / name).write_text(html_out, encoding="utf-8")
        print(f"wrote {name} ({len(html_out):,} bytes)")

    # machine-readable dataset, kept for auditability
    payload = {
        "generated_on": ds.GENERATED_ON,
        "session": ds.SESSION,
        "sources": {k: {"publisher": v[0], "title": v[1], "url": v[2]} for k, v in ds.SOURCES.items()},
        "categories": [{"id": c[0], "name": c[1], "description": c[2]} for c in ds.CATEGORIES],
        "records": [
            {
                "id": r[0], "category": r[1], "metric": r[2], "value": r[3], "unit": r[4],
                "period": r[5], "geography": r[6],
                "source_key": r[7], "source_name": ds.SOURCES[r[7]][0], "url": ds.SOURCES[r[7]][2],
                "status": r[8], "note": r[9],
            }
            for r in ds.ROWS
        ],
        "counts": C,
    }
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data/dataset.json").write_text(json.dumps(payload, indent=1, ensure_ascii=False))
    print(f"wrote data/dataset.json ({len(payload['records'])} records)")


if __name__ == "__main__":
    main()
