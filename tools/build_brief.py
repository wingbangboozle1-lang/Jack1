#!/usr/bin/env python3
"""Generate the consolidated, source-linked decision dashboard.

Single source of truth: data/brief_rows.json + data/brief_sources.json +
data/brief_flags.json + data/brief_scenarios.json.

Every table row gets at least one official source link. A row whose value could not be
confirmed from an official publisher has an EMPTY value cell, an "Unverified" badge, a
U-<row id> flag, and an entry on flagged.html. No personal information is published.
"""
from __future__ import annotations

import html
import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RETRIEVED = "2026-11-07"
SITE_URL = "https://wingbangboozle1-lang.github.io/Jack1/"

rows_all = json.loads((ROOT / "data/brief_rows.json").read_text(encoding="utf-8"))["rows"]
sources = json.loads((ROOT / "data/brief_sources.json").read_text(encoding="utf-8"))["sources"]
flags = json.loads((ROOT / "data/brief_flags.json").read_text(encoding="utf-8"))["irregularities"]
scenarios = json.loads((ROOT / "data/brief_scenarios.json").read_text(encoding="utf-8"))

by_page = {}
for r in rows_all:
    by_page.setdefault(r["page"], []).append(r)
unverified = [r for r in rows_all if r["status"] == "unverified"]
verified = [r for r in rows_all if r["status"] == "verified"]


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def L(sid: str, label: str | None = None) -> str:
    """Inline official source link."""
    s = sources[sid]
    txt = label if label is not None else sid
    return (f'<a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer" '
            f'title="{esc(s["publisher"])} — {esc(s["title"])}">{esc(txt)}</a>')


def src_links(ids: list[str]) -> str:
    return '<div class="src-links">' + "".join(L(sid) for sid in ids) + "</div>"


# ---------------------------------------------------------------------------
# Navigation / page registry
# ---------------------------------------------------------------------------
PAGES = [
    ("index", "index.html", "Executive summary", "Overview", "Decision brief"),
    ("decision", "decision.html", "Decision paths & recommendation", "Overview", "Decision analysis"),
    ("projection", "projection.html", "Projection system", "Overview", "Model & method"),
    ("property", "property.html", "Property & lease", "Property & tenant", "Asset dossier"),
    ("tenant", "tenant.html", "Tenant & brand", "Property & tenant", "Counterparty"),
    ("market", "market.html", "Local market", "Area economy", "Market overview"),
    ("geography", "geography.html", "Geography & infrastructure", "Area economy", "Place"),
    ("demographics", "demographics.html", "Population & households", "Area economy", "Demographics"),
    ("income", "income.html", "Income, prices & wages", "Area economy", "Purchasing power"),
    ("employment", "employment.html", "Jobs & employment", "Area economy", "Labor market"),
    ("schools", "schools.html", "School system", "Area economy", "Education"),
    ("economy", "economy.html", "Economic & property-value factors", "Area economy", "Economic base"),
    ("hazards", "hazards.html", "Natural hazards & black swans", "Risk & rules", "Tail risk"),
    ("regulatory", "regulatory.html", "Taxes, wages & land use", "Risk & rules", "Rules"),
    ("risks", "risks.html", "Risk register", "Risk & rules", "Every decision path"),
    ("sources", "sources.html", "Sources & manual review", "Governance", "Verification"),
    ("flagged", "flagged.html", "Flagged for Review", "Governance", "Open items"),
    ("privacy", "privacy.html", "Privacy & data policy", "Governance", "Privacy"),
    ("scope", "scope.html", "Scope & requirements", "Governance", "Acceptance criteria"),
]
PAGE_FILES = {pid: fn for pid, fn, *_ in PAGES}
PAGE_TITLES = {pid: title for pid, _, title, *_ in PAGES}
NAV_GROUPS = OrderedDict()
for pid, fn, title, group, _ in PAGES:
    NAV_GROUPS.setdefault(group, []).append((pid, fn, title))
ALIASES = {"model.html": "projection", "risk.html": "risks"}
CANONICAL_FILES = {fn for _, fn, *_ in PAGES} | {"404.html"} | set(ALIASES)


# ---------------------------------------------------------------------------
# Narrative content (numbers here are always accompanied by official links)
# ---------------------------------------------------------------------------
INTRO = {}
CLOSING = {}

INTRO["index"] = f"""
<div class="callout callout--accent">
  <h2>Recommendation: hold and secure the term now, with a hard pre-committed sell trigger</h2>
  <p>Do <strong>not</strong> sell immediately. Do <strong>not</strong> wait passively for the reported
  2030&ndash;2035 expiry. Negotiate a longer, signed renewal while preparing a sale in parallel; trigger the
  sale if the renewal is not signed, the site appears on a closure list, the franchise agreement ends at or
  before lease expiry, or tenant credit support deteriorates. Never ride to expiry unrenewed.</p>
  <p>This is a <strong>decision rule, not a property-specific verdict</strong>: the address, APN, lease,
  rent, guarantor, debt, appraisal and owner tax profile were withheld for privacy. Every asset-specific
  value on this site is deliberately blank and flagged. The rule is derived from two verified facts &mdash;
  the issuer is contracting ({L('SEC_Q4FY25', '86 closures in FY2025')}, {L('SEC_Q3FY26', '17 in Q3 FY2026')}),
  while the regional economy is large, mixed and still growing ({L('BLS_EAG', '+0.5% nonfarm jobs')},
  {L('ASSESSOR_ROLL', '$2.272 trillion assessment roll')}).</p>
</div>
<div class="note-panel">
  <h2>What this site contains</h2>
  <p>A line-by-line, source-verified decision project for an anonymized Jack in the Box NNN-leased
  property around central Los Angeles. All {len(verified)} verified values come from official publishers and
  each table row links to them. All {len(unverified)} values that cannot be confirmed are left blank and
  published on the <a href="flagged.html">Flagged for Review</a> page. No personal information appears
  anywhere; see <a href="privacy.html">Privacy &amp; data policy</a>.</p>
</div>
"""
CLOSING["index"] = """
<div class="callout callout--warn">
  <h2>Read the guardrails first</h2>
  <p>The two most consequential unknowns are the exact lease expiration date and whether this site is on
  the tenant's closure list. Neither can be resolved from public official sources. Resolve both privately
  before any binding commitment. See <a href="flagged.html">Flagged for Review</a> for the complete list.</p>
</div>
"""

INTRO["decision"] = f"""
<div class="note-panel">
  <h2>How to read the decision matrix</h2>
  <p>Nine decision paths are analysed below, from selling immediately to doing nothing. Each row links to
  the official rule or disclosure that bears on it. Values that would require an appraisal, an executed
  lease, a rent roll or a personal tax profile are blank and flagged &mdash; they are never estimated.</p>
  <p>The binding risk is <strong>tenant-side contraction, not a collapsing local economy</strong>. The
  issuer's {L('SEC_10K', 'FY2025 10-K')} lists a closure programme as a pillar of its turnaround plan, and
  {L('SEC_Q3FY26', 'Q3 FY2026')} reports higher franchisee bad-debt expense and lower rent/royalty revenue.
  Against that, the {L('BLS_EAG', 'metro labor market')} is not in a deep downturn and the
  {L('ASSESSOR_ROLL', 'county property tax base')} reached a record high.</p>
</div>
"""
CLOSING["decision"] = f"""
<div class="callout callout--accent">
  <h2>Wealth preservation with a growth option</h2>
  <p>Holding with a signed long-term renewal keeps income and preserves land optionality in a
  supply-constrained city; selling removes single-tenant and catastrophe concentration but crystallizes a
  shortening-term discount and a {L('ULA_FAQ', 'transfer-tax cliff')}. The balanced course is the dual track:
  secure the term, then decide with evidence rather than hope.</p>
</div>
"""

INTRO["projection"] = f"""
<div class="note-panel">
  <h2>A projection system without invented numbers</h2>
  <p>The engine is deterministic and offline. It reads only the {L('FRED_10', 'official Treasury')},
  {L('BLS_CPI', 'CPI')}, {L('CEN_CITY', 'population')}, {L('DOF_E1', 'DOF')},
  {L('BEA_2024', 'BEA')} and {L('ULA_FAQ', 'ULA')} anchors published below, plus private parameters the
  owner supplies locally. It produces a <strong>break-even renewal probability</strong>, not a valuation,
  because no government agency publishes net-lease capitalization rates or comparable sales.</p>
  <pre class="code">PV(hold, no renewal)  =  SUM[ rent * (1+g)^(t-1) / (1+r)^t , t = 1..n ]  +  residual / (1+r)^n
PV(hold, renewed)    =  SUM[ rent * (1+g)^(t-1) / (1+r)^t , t = 1..n+m ] +  residual / (1+r)^(n+m)
net sale proceeds    =  price - price * (official transfer tax + owner cost rate) - loan payoff - owner tax
break-even p         =  (net sale proceeds - stressed hold PV) / (renewed hold PV - stressed hold PV)

r  = OFFICIAL 10-year Treasury anchor + OWNER-SUPPLIED equity/illiquidity premium
g  = OWNER-SUPPLIED rent escalation;  n = remaining years;  m = renewal years
Every OWNER-SUPPLIED value and every MODEL OUTPUT is private and is NOT published on this site.</pre>
  <p><strong>Hard limits.</strong> Official employment projections end in {L('EDD_LA', '2033')} and BEA
  has {L('BEA_2024', 'discontinued metropolitan-area output and income statistics')}. No series is
  extrapolated to 2035. The {L('SCAG_DEM', 'SCAG 2050 plan')} is a long-range planning forecast, not a
  site or business-cycle forecast.</p>
</div>
"""
CLOSING["projection"] = """
<div class="callout callout--warn">
  <h2>Reproduce it yourself, privately</h2>
  <p>The executable engine is <code>tools/projection.py</code> in this repository. It makes no network
  calls, contains no owner information, writes nothing into the website by default, and labels every
  number as an official anchor, an owner-supplied sensitivity, or a model output. Its complete source is
  reproduced below for line-by-line review; the official anchors it uses are listed in
  <code>data/brief_scenarios.json</code> and traced to their rows in
  <code>data/brief_rows.json</code>.</p>
</div>
"""

INTRO["property"] = """
<div class="note-panel">
  <h2>Why most of this page is blank</h2>
  <p>The property is anonymized. No street address, APN, title document, lease, rent roll, guaranty,
  appraisal, insurance policy, debt statement or owner tax profile was supplied, and none was inferred
  from a nearby parcel or from brand-level filings. Each blank row links to the official lookup tool that
  would close it. Rows labelled <em>Issuer-wide lease context</em> are facts about the public company in
  {SEC_10K}, not facts about this property.</p>
</div>
""".replace("{SEC_10K}", L("SEC_10K", "SEC filings"))
CLOSING["property"] = """
<div class="callout callout--warn">
  <h2>NNN does not mean zero landlord risk</h2>
  <p>Roof, structure, parking, tax, insurance and casualty obligations are contractual, not automatic.
  Read the executed lease before assuming that a wildfire, earthquake or reassessment cost sits entirely
  with the tenant.</p>
</div>
"""

INTRO["tenant"] = f"""
<div class="note-panel">
  <h2>The dominant variable</h2>
  <p>Jack in the Box Inc. is contracting: {L('SEC_Q4FY25', '86 closures in FY2025')},
  {L('SEC_Q3FY26', '17 more in Q3 FY2026')}, and a system count down to 2,115. Its
  {L('SEC_10K', 'FY2025 10-K')} names a restaurant closure programme as a core plan pillar. The
  {L('SEC_Q3FY26', 'Q3 FY2026 release')} also reports higher franchisee bad-debt expense and
  franchise-level margin pressure partly from lower rent and royalty revenue &mdash; a direct credit signal
  for a net-lease landlord whose tenant may be a franchisee.</p>
  <p>SEC filings are issuer-level. They do <strong>not</strong> identify this property, its legal tenant,
  guarantor, rent, unit sales, franchise agreement expiry or closure-list membership. Those cells are blank.</p>
</div>
"""
CLOSING["tenant"] = """
<div class="callout callout--accent">
  <h2>Monitor the official filing index, not a news calendar</h2>
  <p>Use the issuer's EDGAR filings index for subsequent quarters and updated closure guidance; the next
  official filing date is not asserted here because no official publisher was found for it.</p>
</div>
"""

INTRO["market"] = """
<div class="note-panel">
  <h2>Citywide and countywide indicators, not a trade area</h2>
  <p>These are official city, county and metropolitan figures. They are deliberately not assigned to the
  property's drive-time catchment, because no address was supplied. Use the category subpages to drill
  into population, income, jobs, schools, the economic base, hazards and rules.</p>
</div>
"""
CLOSING["market"] = """
<div class="callout callout--warn">
  <h2>Do not mix measures</h2>
  <p>Census Vintage-2025 estimates and California DOF January-1 estimates have different reference dates
  and methods; BEA personal income is not GDP; BLS metro jobs are not Census employer establishment
  employment. Each row states its own measure, date and geography. See
  <a href="flagged.html">Flagged for Review</a> for the reconciliation notes.</p>
</div>
"""

INTRO["geography"] = """
<div class="note-panel">
  <h2>Geography is the constraint on every other number</h2>
  <p>"Central Los Angeles" is not an official statistical geography. The published geographies here are
  the City of Los Angeles, Los Angeles County and the Los Angeles&ndash;Long Beach&ndash;Anaheim MSA.
  Parcel-specific zoning, transit catchment, school assignment and hazard designation require an address
  and are blank.</p>
</div>
"""
CLOSING["geography"] = ""

INTRO["demographics"] = """
<div class="note-panel">
  <h2>Two independent official population products</h2>
  <p>Census QuickFacts Vintage-2025 and California DOF E-1 disagree because they use different reference
  dates, vintages and methods. Both are published below, separately, and are never blended. The long-range
  SCAG figures are planning assumptions to 2050, not a 2030&ndash;2035 forecast for this site.</p>
</div>
"""
CLOSING["demographics"] = ""

INTRO["income"] = """
<div class="note-panel">
  <h2>Purchasing power, costs and the wage floor</h2>
  <p>Median household income, housing costs and poverty are city/county ACS figures; consumer prices are
  BLS; regional income is BEA; the fast-food wage floor is a California rule. Residential rent is
  <strong>not</strong> commercial rent, and no commercial rent figure is asserted anywhere on this site.</p>
</div>
"""
CLOSING["income"] = ""

INTRO["employment"] = """
<div class="note-panel">
  <h2>Mixed, weak growth with a structural shift</h2>
  <p>Total nonfarm employment is growing slowly while the sector mix changes materially: education and
  health services are expanding and information is contracting. Weekday demand in office-heavy central
  corridors is therefore weaker than the headline suggests. The official EDD projection window ends in
  2033; nothing is extrapolated beyond it.</p>
</div>
"""
CLOSING["employment"] = ""

INTRO["schools"] = """
<div class="note-panel">
  <h2>District scale, not a site catchment</h2>
  <p>California Department of Education and California School Dashboard figures describe Los Angeles
  Unified as a whole. No school is assigned to this property, no school is rated here, and no address is
  published. School quality is included because it affects residential stability and the long-run
  neighborhood consumer base.</p>
</div>
"""
CLOSING["schools"] = ""

INTRO["economy"] = """
<div class="note-panel">
  <h2>Every economic and property-value factor with an official publisher</h2>
  <p>Output and income, business activity, prices, interest-rate anchors, forecast horizons, the
  assessment roll and infrastructure investment are listed with their measure and date. Factors with no
  official publisher &mdash; capitalization rates, comparable sales, commercial rent for this parcel &mdash;
  are blank and flagged rather than filled from brokerage or aggregator commentary.</p>
</div>
"""
CLOSING["economy"] = ""

INTRO["hazards"] = f"""
<div class="callout callout--danger">
  <h2>Black swans are documented, not hypothetical</h2>
  <p>The {L('USGS_UCERF3', 'USGS')} puts the 30-year probability of a magnitude 6.7 earthquake in the
  Los Angeles region at 60%. The {L('LACO_FIRES', 'County of Los Angeles')} documents the 2025 Eaton and
  Palisades fires with 16,251 structures destroyed, roughly 6,800 businesses affected and
  $5.2&ndash;$10.1 billion of lost economic output. The {L('CDI_ORDER', 'California Department of Insurance')}
  approved a $1 billion FAIR Plan assessment. All of these are <em>regional</em> figures: no parcel-level
  hazard rating is asserted.</p>
</div>
"""
CLOSING["hazards"] = """
<div class="callout callout--warn">
  <h2>The tail risk is correlation</h2>
  <p>A tenant credit event and a regional catastrophe are not independent for a single undiversified
  asset. Insurance, retrofit status and concentration limits are therefore part of the decision rule,
  not an afterthought.</p>
</div>
"""

INTRO["regulatory"] = """
<div class="note-panel">
  <h2>Rules that change net proceeds and tenant margins</h2>
  <p>Measure ULA is a <em>cliff</em>: the tier applies to the whole consideration once a threshold is
  crossed, and thresholds are indexed annually. Proposition 13 limits assessed-value growth while a
  property is held and reassesses on a change of ownership. The California fast-food wage floor applies
  to franchisees as well as brand owners.</p>
</div>
"""
CLOSING["regulatory"] = ""

INTRO["risks"] = """
<div class="note-panel">
  <h2>Every possible decision, with its risks</h2>
  <p>Business-as-usual risks and economy-destroying tail risks are mapped to each decision path. Where
  an official publisher provides an anchor (earthquake probability, wildfire losses, ULA rates, closure
  counts), that anchor is shown with its source. Where no official value exists, the value cell is blank
  and the row is flagged. Mitigations are analytical judgements, clearly separated from the data.</p>
</div>
"""
CLOSING["risks"] = """
<div class="callout callout--accent">
  <h2>The highest-regret path</h2>
  <p>Passively letting the term decay to expiry without a signed renewal compresses the buyer pool and
  transfers all re-tenanting, vacancy and capital risk to the owner at the worst possible moment.</p>
</div>
"""

INTRO["sources"] = """
<div class="note-panel">
  <h2>Every official publisher used, for manual review</h2>
  <p>Each source below was read line by line on 2026-11-07. "Statistics" and "rule" rows back a published
  value; "lookup" rows are official tools paired with a blank, flagged cell. All external links open in
  a new tab with <code>rel="noopener noreferrer"</code>. The internal ledger is
  <code>research/VERIFICATION_DAC604B9.md</code> and is not part of the published site.</p>
</div>
"""
CLOSING["sources"] = """
<div class="callout callout--accent">
  <h2>Manual review checklist</h2>
  <ul>
    <li>Confirm the exact lease expiration date, option language and notice deadlines from the executed lease.</li>
    <li>Confirm the legal tenant and any guaranty; do not assume the public issuer is the obligor.</li>
    <li>Run the parcel lookups: ZIMAS, Assessor portal, Tax Rate Area, FEMA flood, CAL FIRE FHSZ, CGS seismic zones.</li>
    <li>Re-check the indexed ULA thresholds and rates in force on the actual closing date.</li>
    <li>Monitor the issuer's EDGAR filings index for subsequent quarterly results and closure guidance.</li>
    <li>Verify insurance declarations, retrofit status and a current appraisal before any sale pricing.</li>
  </ul>
  <p>Official lookup tools: <a href="https://zimas.lacity.org/" target="_blank" rel="noopener noreferrer">ZIMAS</a> &middot;
  <a href="https://portal.assessor.lacounty.gov/" target="_blank" rel="noopener noreferrer">Assessor portal</a> &middot;
  <a href="https://auditor.lacounty.gov/tax-rate-area-lookup/" target="_blank" rel="noopener noreferrer">Tax Rate Area</a> &middot;
  <a href="https://www.fema.gov/flood-maps/products-tools" target="_blank" rel="noopener noreferrer">FEMA flood maps</a> &middot;
  <a href="https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones" target="_blank" rel="noopener noreferrer">CAL FIRE FHSZ</a> &middot;
  <a href="https://maps.conservation.ca.gov/cgs/EQZApp/app/" target="_blank" rel="noopener noreferrer">CGS seismic zones</a> &middot;
  <a href="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&amp;CIK=0000807882&amp;type=8-K&amp;dateb=&amp;owner=include&amp;count=10" target="_blank" rel="noopener noreferrer">EDGAR filings</a>.</p>
</div>
"""

INTRO["flagged"] = f"""
<div class="callout callout--warn">
  <h2>Flagged for Review &mdash; {len(unverified)} blank values and {len(flags)} irregularities</h2>
  <p>None of these items blocks publication. They are published deliberately because a value could not
  be confirmed from an official source. <strong>No blank cell has been filled, estimated or inferred.</strong>
  The irregularities record contradictions between official products, prior-session errors and deploy
  issues. Flagged items do not block the merge or the live site.</p>
</div>
"""
CLOSING["flagged"] = """
<div class="callout callout--accent">
  <h2>What closes a flag</h2>
  <p>A flag closes only when an official publisher page can be read line by line and the exact value,
  unit, date and geography are recorded, or when the owner supplies the private document to their own
  adviser. Private owner documents are never uploaded to this website.</p>
</div>
"""

INTRO["privacy"] = """
<div class="callout callout--accent">
  <h2>No personal information is published</h2>
  <p>The property is described only as "an anonymized Jack in the Box NNN-leased property around central
  Los Angeles" with a reported lease-expiry window of 2030&ndash;2035. There is no owner name, ownership
  entity, street address, APN, title document, lease, rent figure, tenant legal name, guarantor name,
  debt statement, appraisal, insurance policy, personal financial figure, personal email or personal phone
  number anywhere on this site, in the dataset or in the generated pages.</p>
</div>
<div class="note-panel">
  <h2>How the posture is enforced</h2>
  <p>Parcel-specific and owner-specific fields are blank by design and flagged; internal research notes
  live in <code>research/</code> and are excluded from the published artifact; and an automated gate scans
  every published page for email addresses, phone numbers, SSN-like patterns, APN-like identifiers,
  street addresses and person-name labels before the site can deploy.</p>
</div>
"""
CLOSING["privacy"] = """
<div class="callout callout--warn">
  <h2>Internal use only</h2>
  <p>Any personal information encountered during research stays in private, owner-held documents and is
  replaced with a placeholder here. The projection engine accepts private parameters locally and writes
  no result into the website.</p>
</div>
"""

INTRO["scope"] = """
<div class="note-panel">
  <h2>Full requirements list and where each one is satisfied</h2>
  <p>This page is the acceptance-criteria checklist for the whole project. Every item is implemented in
  the current build; items requiring private data are implemented as blank, flagged fields rather than
  fabricated values.</p>
</div>
"""
CLOSING["scope"] = """
<div class="callout callout--accent">
  <h2>Integration workflow</h2>
  <p>The shared board is <code>COORDINATION.md</code>. This session claimed and completed D1&ndash;D7 on
  the pinned branch, preserved all prior-session files, and opened a single pull request to
  <code>main</code>. The merge and deployment result is recorded on the board.</p>
</div>
"""

REQUIREMENTS = [
    ("Executive summary", "index.html &mdash; recommendation, headline indicators and decision guardrails."),
    ("Full requirements list, organized", "This page, with status and location for every item."),
    ("Geography", "geography.html &mdash; official city, county and MSA geographies; parcel lookups flagged."),
    ("Income levels", "income.html &mdash; household/per-capita income, poverty, housing costs, CPI, wages."),
    ("School systems", "schools.html &mdash; CDE district scale and California School Dashboard outcomes."),
    ("Population", "demographics.html &mdash; Census V2025 and CA DOF E-1, kept separate."),
    ("Job growth", "employment.html &mdash; BLS sector detail, EDD projections and their 2033 limit."),
    ("Every economic and property-value factor", "economy.html &mdash; output, business activity, prices, rates, assessment roll, infrastructure; blanks flagged."),
    ("Business-as-usual risks", "risks.html &mdash; all decision paths, pricing, tenant credit, wages, expiry decay."),
    ("Black swans / economy-destroying events", "hazards.html &mdash; earthquake, wildfire, insurance failure, flood, heat, utility and correlated shocks."),
    ("Risks for every possible decision", "decision.html and risks.html &mdash; nine paths with risk and mitigation per path."),
    ("Recommendation for wealth preservation + growth with manageable risk", "decision.html &mdash; hold and secure term now with a pre-committed sell trigger."),
    ("Reliable projection system", "projection.html and tools/projection.py &mdash; deterministic, official anchors, break-even rule, no invented values."),
    ("Verified official/trusted sources, line by line, with links", "sources.html plus a source link in every table row; research/VERIFICATION_DAC604B9.md."),
    ("Flag irregularities", "flagged.html &mdash; irregularities IR-D1 to IR-D16."),
    ("No hallucinations; blanks flagged unverified; never inferred", "86 blank cells with U-&lt;row id&gt; flags; enforced by tools/verify_brief.py."),
    ("Repository reviewed line by line", "research/REPO_AUDIT_DAC604B9.md."),
    ("GitHub Pages live site, clean dashboard landing + category subpages", "index.html plus 18 category/governance pages with grouped navigation."),
    ("All entries and findings in easy tables with analysis", "Every page uses sortable-style grouped tables with a finding column."),
    ("Clearly labeled Flagged for Review page", "flagged.html."),
    ("No personal information on the final website", "privacy.html plus an automated PII gate over all published pages."),
    ("No manual user input", "All research, verification, build, validation, PR and deploy performed autonomously."),
    ("Shared board, claims, disjoint scopes, small commits", "COORDINATION.md, session arena/dac604b9-jack1, D1&ndash;D7."),
    ("Final integration, re-verification, no broken links, publish", "tools/verify_brief.py and scripts/validate_site.py in CI."),
    ("PR to main with summary and sources; merge without approval; confirm deploy; record result", "COORDINATION.md final entry."),
]


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------
def row_html(r: dict) -> str:
    status = r["status"]
    searchable = " ".join([
        r["id"], r["metric"], r["value"], r["period"], r["finding"], r["note"],
        " ".join(r["sources"]),
        " ".join(sources[s]["publisher"] for s in r["sources"]),
        " ".join(sources[s]["title"] for s in r["sources"]),
    ])
    if status == "verified":
        badge = '<span class="badge badge--verified">Verified</span>'
        value_cell = f'<td class="col-value">{esc(r["value"])}</td>'
        flag_id = ""
    else:
        badge = '<span class="badge badge--flagged">Unverified · blank</span>'
        value_cell = '<td class="col-value col-value--blank" aria-label="Left blank: no official value confirmed"></td>'
        flag_id = f'<span class="flag-id">{esc(r["flag"])}</span>'
    note_extra = f'<span class="row-note">{esc(r["note"])}</span>' if r["note"] else ""
    return (
        f'<tr data-status="{status}" data-search="{esc(searchable.lower())}"'
        f' class="{"is-flagged" if status == "unverified" else ""}">'
        f'<td class="col-id">{esc(r["id"])}</td>'
        f'<td class="col-metric">{esc(r["metric"])}</td>'
        f'{value_cell}'
        f'<td class="col-period">{esc(r["period"])}</td>'
        f'<td class="col-note">{esc(r["finding"])}{note_extra}</td>'
        f'<td class="col-status">{badge}{flag_id}</td>'
        f'<td class="col-src">{src_links(r["sources"])}</td>'
        '</tr>'
    )


TABLE_HEAD = (
    '<thead><tr><th scope="col">ID</th><th scope="col">Indicator / question</th>'
    '<th scope="col">Official value</th><th scope="col">Period &amp; scope</th>'
    '<th scope="col">Finding &amp; analysis</th><th scope="col">Status</th>'
    '<th scope="col">Official source</th></tr></thead>'
)


def table_html(rows: list[dict], suffix: str, desc: str = "") -> str:
    out = [f'<section class="section" id="{esc(suffix)}">']
    out.append('<div class="section-head"><h2>' + esc(suffix.replace("-", " ").title()) + '</h2>'
               f'<span class="count">{len(rows)} rows · '
               f'{sum(1 for r in rows if r["status"] == "verified")} verified · '
               f'{sum(1 for r in rows if r["status"] == "unverified")} flagged</span></div>')
    if desc:
        out.append(f'<p class="section-desc">{esc(desc)}</p>')
    out.append('<div class="table-wrap"><table class="data-table" data-table>')
    out.append(TABLE_HEAD)
    out.append("<tbody>")
    out.extend(row_html(r) for r in rows)
    out.append("</tbody></table></div></section>")
    return "\n".join(out)


def grouped_tables(page_id: str, extra_rows: list[dict] | None = None) -> str:
    rows = list(by_page.get(page_id, [])) + list(extra_rows or [])
    groups = OrderedDict()
    for r in rows:
        groups.setdefault(r["group"], []).append(r)
    out = []
    for i, (group, gr) in enumerate(groups.items(), 1):
        out.append(table_html(gr, f"sec-{page_id}-{i}", desc=group))
    return "\n".join(out)


def nav_html(current_pid: str) -> str:
    out = ['<nav aria-label="Site navigation">']
    for group, items in NAV_GROUPS.items():
        out.append(f'<div class="nav-group"><h3>{esc(group)}</h3>')
        for pid, fn, title in items:
            cur = ' aria-current="page"' if pid == current_pid else ""
            fl = ' <span class="nav-flag">review</span>' if pid == "flagged" else ""
            out.append(f'<a href="{esc(fn)}"{cur}><span class="dot"></span>{esc(title)}{fl}</a>')
        out.append("</div>")
    out.append("</nav>")
    return "\n".join(out)


def shell(page_id: str, filename: str, title: str, kicker: str, lede: str, body: str,
          extra_head: str = "") -> str:
    current = PAGE_TITLES[page_id]
    nav = nav_html(page_id)
    alias_note = extra_head
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{esc(title)} — anonymized, source-verified NNN lease decision brief. Every table row links to an official publisher; unverified values are blank and flagged.">
<meta name="color-scheme" content="light">
<title>{esc(title)} · Jack in the Box NNN decision brief</title>
<link rel="stylesheet" href="assets/brief.css">
<script defer src="assets/brief.js"></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="shell">
  <aside class="sidebar" id="sidebar">
    <div class="brand">
      <a href="index.html"><span class="brand-title">NNN Lease Decision Brief</span>
      <span class="brand-sub">Anonymized · Central Los Angeles</span></a>
      <span class="brand-tag">Official-source verified · {RETRIEVED}</span>
    </div>
    {nav}
    <div class="sidebar-foot">No personal information is published. Blank cells mean no official value was confirmed; see <a href="flagged.html" style="color:#e4bd85">Flagged for Review</a>.</div>
  </aside>
  <div class="main-wrap">
    <header class="topbar">
      <button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="sidebar">☰ Menu</button>
      <span class="crumb">Decision brief / <strong>{esc(current)}</strong></span>
      <div class="top-actions">
        <span class="pill">{len(verified)} verified values</span>
        <span class="pill pill--warn"><a href="flagged.html">{len(unverified)} flagged</a></span>
        <input type="search" id="global-search" placeholder="Filter rows…" aria-label="Filter table rows">
        <select id="status-filter" aria-label="Filter by verification status">
          <option value="all">All statuses</option>
          <option value="verified">Verified only</option>
          <option value="unverified">Flagged only</option>
        </select>
        <button type="button" id="clear-filters" class="menu-btn" style="display:inline-block">Clear</button>
        <span class="hint" id="result-count"></span>
      </div>
    </header>
    <main id="main">
      <div class="page-head">
        <p class="kicker">{esc(kicker)}</p>
        <h1>{esc(title)}</h1>
        <p class="lede">{lede}</p>
        <div class="meta-row">
          <span class="meta-chip">Session arena/dac604b9-jack1</span>
          <span class="meta-chip">Sources read {RETRIEVED}</span>
          <span class="meta-chip">{len(rows_all)} rows · {len(sources)} official sources</span>
          <span class="meta-chip">Privacy-first · no personal data</span>
        </div>
      </div>
      {alias_note}
      {body}
    </main>
    <footer class="footer"><div class="footer-inner">
      <strong>Reading rule:</strong> every table row links to an official publisher. An empty value cell is
      an unverified value, flagged <code>U-&lt;row id&gt;</code> on <a href="flagged.html">Flagged for Review</a>;
      nothing is inferred or filled. · <a href="sources.html">Sources &amp; manual review</a> ·
      <a href="privacy.html">Privacy</a> · <a href="scope.html">Scope &amp; requirements</a> ·
      <a href="index.html">Executive summary</a>
    </div></footer>
  </div>
</div>
</body>
</html>
"""


def cards_html() -> str:
    cards = [
        ("City population", "3,869,089", "July 1, 2025 (V2025). Large consumer base; slight 5-year decline.", "CEN_CITY"),
        ("MSA unemployment", "4.4%", "September 2026 (preliminary). No deep labor-market downturn.", "BLS_EAG"),
        ("Tenant system size", "2,115", "End of Q3 FY2026. Down from 2,168 a year earlier.", "SEC_Q3FY26"),
        ("10-year Treasury", "4.84%", "November 5, 2026. Official discount-rate anchor.", "FRED_10"),
    ]
    out = ['<div class="card-grid">']
    for label, value, note, sid in cards:
        out.append(f'<div class="card card--accent"><span class="card-label">{esc(label)}</span>'
                   f'<div class="card-value">{esc(value)}</div><div class="card-note">{esc(note)}</div>'
                   f'<span class="card-src">Official: {L(sid)}</span></div>')
    out.append('</div>')
    return "\n".join(out)


def category_cards() -> str:
    groups = {
        "Overview": ["decision", "projection"],
        "Property & tenant": ["property", "tenant"],
        "Area economy": ["market", "geography", "demographics", "income", "employment", "schools", "economy"],
        "Risk & rules": ["hazards", "regulatory", "risks"],
        "Governance": ["sources", "flagged", "privacy", "scope"],
    }
    out = ['<section class="section" id="site-map"><div class="section-head"><h2>Explore by category</h2></div><div class="card-grid">']
    for g, pids in groups.items():
        links = " · ".join(f'<a href="{PAGE_FILES[p]}">{esc(PAGE_TITLES[p])}</a>' for p in pids)
        out.append(f'<div class="card"><span class="card-label">{esc(g)}</span>'
                   f'<div class="card-note" style="margin-top:8px">{links}</div></div>')
    out.append("</div></section>")
    return "\n".join(out)


def sources_table() -> str:
    body = []
    for sid, s in sorted(sources.items()):
        searchable = " ".join([sid, s["publisher"], s["title"], s["kind"], s["url"]]).lower()
        body.append(
            f'<tr data-status="verified" data-search="{esc(searchable)}">'
            f'<td class="col-id">{esc(sid)}</td>'
            f'<td class="col-metric">{esc(s["publisher"])}</td>'
            f'<td class="col-value">{esc(s["kind"])}</td>'
            f'<td class="col-period">{esc(RETRIEVED)} · {esc(s["kind"])}</td>'
            f'<td class="col-note">{esc(s["title"])}</td>'
            f'<td class="col-status"><span class="badge badge--verified">Official</span></td>'
            f'<td class="col-src"><div class="src-links">{L(sid, "Open official page")}</div></td></tr>'
        )
    return (
        '<section class="section" id="source-register"><div class="section-head"><h2>Official source register</h2>'
        f'<span class="count">{len(sources)} sources</span></div>'
        '<p class="section-desc">Publisher, document type, retrieval date and a direct link for every source used anywhere on this site.</p>'
        '<div class="table-wrap"><table class="data-table" data-table><thead><tr>'
        '<th scope="col">ID</th><th scope="col">Publisher</th><th scope="col">Official value / type</th>'
        '<th scope="col">Retrieved</th><th scope="col">Document or tool</th><th scope="col">Status</th>'
        '<th scope="col">Official source</th></tr></thead><tbody>' + "\n".join(body) +
        '</tbody></table></div></section>'
    )


def irregularities_html() -> str:
    out = ['<section class="section" id="irregularities"><div class="section-head"><h2>Irregularities &amp; reconciliation notes</h2>'
           f'<span class="count">{len(flags)} items</span></div>'
           '<p class="section-desc">Published for manual review. Each item links to the official pages or repository evidence behind it. Flagged items do not block the merge or the live site.</p>'
           '<div class="flag-list">']
    for f in flags:
        links = "".join(
            f'<a href="{esc(u)}" target="_blank" rel="noopener noreferrer">{esc(label_for(u, i))}</a>'
            for i, u in enumerate(f["links"], 1)
        )
        out.append(f'<div class="flag-item"><span class="flag-code">{esc(f["id"])}</span>'
                   f'<h3>{esc(f["title"])}</h3><p>{esc(f["detail"])}</p>'
                   f'<div class="flag-links">{links}</div></div>')
    out.append("</div></section>")
    return "\n".join(out)


def label_for(url: str, i: int) -> str:
    from urllib.parse import urlparse
    host = (urlparse(url).hostname or "source").replace("www.", "")
    return f"{host} ({i})" if len(url) < 200 else f"official link {i}"


def privacy_table() -> str:
    rows = [r for r in by_page["property"] if r["group"] == "Asset & lease — withheld fields"]
    return table_html(rows, "withheld-categories", desc="Fields withheld for privacy. Each is blank, flagged, and paired with the official lookup that would close it.")


def scope_checklist() -> str:
    out = ['<section class="section" id="requirements"><div class="section-head"><h2>Requirements checklist</h2>'
           f'<span class="count">{len(REQUIREMENTS)} items · all implemented</span></div><ul class="checklist">']
    for i, (q, a) in enumerate(REQUIREMENTS, 1):
        out.append(f'<li><span class="tick">✓</span><span><span class="q">R-{i:02d} {q}.</span> '
                   f'<span class="a">{a}</span></span></li>')
    out.append("</ul></section>")
    return "\n".join(out)


def stats_cards() -> str:
    data = [
        ("Rows", str(len(rows_all)), "Line-by-line entries across 19 pages."),
        ("Verified", str(len(verified)), "Backed by an official publisher and a source link."),
        ("Blank & flagged", str(len(unverified)), "No official value confirmed; never inferred."),
        ("Official sources", str(len(sources)), "Government and public-agency publishers."),
        ("Irregularities", str(len(flags)), "Published on Flagged for Review."),
        ("Decision paths", str(len(scenarios["scenarios"])), "Each with business-as-usual and tail risks."),
    ]
    out = ['<div class="card-grid">']
    for label, value, note in data:
        out.append(f'<div class="card"><span class="card-label">{esc(label)}</span>'
                   f'<div class="card-value">{esc(value)}</div><div class="card-note">{esc(note)}</div></div>')
    out.append("</div>")
    return "\n".join(out)


def body_for(pid: str) -> str:
    parts = []
    if pid == "index":
        parts.append(cards_html())
    parts.append(INTRO.get(pid, ""))
    if pid == "scope":
        parts.append(stats_cards())
    if pid == "privacy":
        parts.append(privacy_table())
    if pid == "scope":
        parts.append(scope_checklist())
    if pid == "sources":
        parts.append(sources_table())
    if pid == "flagged":
        parts.append(table_html(unverified, "unverified-values",
                                desc="Every empty value cell on the site, in one place. Each row links to the official source or official lookup tool relevant to it."))
        parts.append(irregularities_html())
    if pid in by_page:
        parts.append(grouped_tables(pid))
    if pid == "index":
        parts.append(category_cards())
    if pid == "projection":
        code = (ROOT / "tools/projection.py").read_text(encoding="utf-8")
        parts.append('<section class="section" id="engine-source"><div class="section-head"><h2>Engine source, reproduced for review</h2></div>'
                     '<details class="accordion"><summary>Show tools/projection.py (standard library only, no network calls)</summary>'
                     f'<pre class="code">{esc(code)}</pre></details>'
                     '<details class="accordion"><summary>Show official anchors and scenarios (data/brief_scenarios.json)</summary>'
                     f'<pre class="code">{esc((ROOT / "data/brief_scenarios.json").read_text(encoding="utf-8"))}</pre></details></section>')
    parts.append(CLOSING.get(pid, ""))
    return "\n".join(p for p in parts if p)


LEDE = {
    "index": "Sell before the lease expires, or renew and hold? A privacy-first, source-verified decision brief for an anonymized Jack in the Box NNN-leased property around central Los Angeles, with a reported lease expiry in 2030&ndash;2035.",
    "decision": "Nine possible courses of action, the risk of each, and the balanced recommendation for individual wealth preservation with a growth option and manageable risk.",
    "projection": "A deterministic, reproducible projection system built on official anchors only. Private inputs stay private; model outputs are never published as facts.",
    "property": "Asset and lease fields, kept blank where no official or owner-supplied document exists, plus issuer-wide lease context that is explicitly not about this property.",
    "tenant": "Official issuer disclosures on the brand's scale, operating trend and closure programme, and the counterparty facts that are not publicly disclosed.",
    "market": "The city, county and metropolitan indicators that frame the decision, with explicit geography and vintage labels.",
    "geography": "Published geographies, infrastructure investment, and the parcel-level lookups that remain open without an address.",
    "demographics": "Population, households and composition from two independent official products, plus the long-range planning forecast.",
    "income": "Household income, poverty, housing costs, consumer prices, regional income and the California fast-food wage floor.",
    "employment": "Labor force, jobs by sector, unemployment, business counts and the official projection window.",
    "schools": "District scale and official outcomes, with site-level school assignment deliberately left blank.",
    "economy": "Output, business activity, prices, interest-rate anchors, forecast horizons, the property tax base and infrastructure.",
    "hazards": "Earthquake, wildfire, insurance failure, flood, heat and correlated regional shocks, with official severity anchors.",
    "regulatory": "Measure ULA transfer tax, Proposition 13, the fast-food wage rule, land use and federal/state tax guidance.",
    "risks": "Business-as-usual and black-swan risks mapped to every decision path, with mitigations.",
    "sources": "Every official publisher used, with a direct link for manual review, and the diligence checklist that closes the open flags.",
    "flagged": "Every value that could not be confirmed from an official source, left blank, plus every irregularity found in the repository or the official record.",
    "privacy": "How personal information is excluded from the dataset, the pages and the projection engine.",
    "scope": "The complete requirements list, where each item is satisfied, and the integration workflow.",
}


def write_page(pid: str, filename: str, title: str, group: str, kicker: str, extra_head: str = "") -> None:
    page = shell(pid, filename, title, kicker, LEDE[pid], body_for(pid), extra_head=extra_head)
    (ROOT / filename).write_text(page, encoding="utf-8")


def build_404() -> None:
    body = """
<div class="callout callout--warn">
  <h2>Page not found</h2>
  <p>This address is not part of the current decision brief. Return to the
  <a href="index.html">executive summary</a>, browse the <a href="sources.html">source register</a>, or
  check <a href="flagged.html">Flagged for Review</a>.</p>
</div>
"""
    page = shell("index", "404.html", "Page not found", "Not found",
                 "The requested page is not part of the published decision brief.", body)
    (ROOT / "404.html").write_text(page, encoding="utf-8")


LEGACY_MARKER = "data-legacy-superseded"
LEGACY_META = '<meta name="robots" content="noindex,nofollow">'


def stamp_legacy_pages() -> int:
    """Preserve prior-session builds but label them clearly as superseded and noindex.

    GitHub Pages on this repository uses a legacy branch build, which publishes every
    committed file; the canonical site is the navigation set above. We do not delete or
    rename another session's work.
    """
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel_parts = path.relative_to(ROOT).parts
        if ".git" in path.parts or (len(rel_parts) == 1 and path.name in CANONICAL_FILES):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        # Some prior-session archive pages still contained raw git conflict markers.
        # Neutralise the marker lines into HTML comments so BOTH sides stay verbatim
        # in the file (nothing from another session is discarded) while the published
        # page no longer renders raw markers. Logged as IR-D17.
        if "<<<<<<< HEAD" in text or re.match(r"(?m)^<<<<<<< ", text):
            text = re.sub(r"(?m)^<<<<<<< .*$", "<!-- prior-session conflict boundary: HEAD side preserved below -->", text)
            text = re.sub(r"(?m)^=======\s*$", "<!-- prior-session conflict boundary: separator; incoming side preserved below -->", text)
            text = re.sub(r"(?m)^>>>>>>> .*$", "<!-- prior-session conflict boundary: end of incoming side -->", text)
            path.write_text(text, encoding="utf-8")
        if LEGACY_MARKER in text:
            continue
        depth = len(path.relative_to(ROOT).parts) - 1
        prefix = "../" * depth if depth else ""
        banner = (
            f'<div {LEGACY_MARKER} class="legacy-banner" role="note" '
            'style="background:#fff3d6;border:2px solid #e0b96c;color:#5c3f0c;padding:12px 16px;'
            'margin:0 0 16px;font:14px/1.5 -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Arial,sans-serif;'
            'text-align:center">Archived prior-session build &mdash; superseded and preserved for audit only. '
            'It is not part of the current source-verified decision brief. '
            f'See the <a href="{prefix}index.html" style="color:#7a4f00;font-weight:700">current executive summary</a> '
            f'and the <a href="{prefix}flagged.html" style="color:#7a4f00;font-weight:700">Flagged for Review</a> page.</div>'
        )
        if "<head" in text:
            text = re.sub(r"(<head[^>]*>)", r"\1\n" + LEGACY_META, text, count=1, flags=re.I)
        else:
            text = LEGACY_META + "\n" + text
        text, n = re.subn(r"(<body[^>]*>)", r"\1\n" + banner, text, count=1, flags=re.I)
        if n == 0:
            text = banner + "\n" + text
        path.write_text(text, encoding="utf-8")
        changed += 1
    return changed


def main() -> int:
    for pid, fn, title, group, kicker in PAGES:
        write_page(pid, fn, title, group, kicker)
    for fn, pid in ALIASES.items():
        meta = next(x for x in PAGES if x[0] == pid)
        alias_note = (
            '<div class="callout callout--warn"><h2>Alternate URL</h2><p>This filename is preserved from '
            f'an earlier session. The canonical page is <a href="{esc(PAGE_FILES[pid])}">{esc(PAGE_TITLES[pid])}</a>; '
            'the content below is identical and jointly verified.</p></div>'
        )
        write_page(pid, fn, meta[2], meta[3], meta[4], extra_head=alias_note)
    build_404()
    (ROOT / "robots.txt").write_text(
        "User-agent: *\n"
        "Allow: /$\n"
        "Allow: /index.html\n"
        "Disallow: /archive/\n"
        "Disallow: /pages/\n"
        "Disallow: /site/\n"
        "Disallow: /research/\n"
        "Disallow: /analysis/\n"
        "Disallow: /risks/\n"
        "Disallow: /model/\n"
        "Disallow: /tools/\n"
        "Disallow: /scripts/\n"
        "Disallow: /data/\n"
        "Sitemap: " + SITE_URL + "sitemap.xml\n",
        encoding="utf-8",
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{SITE_URL}{esc(fn)}</loc></url>\n" for _, fn, *_ in PAGES)
        + "</urlset>\n",
        encoding="utf-8",
    )
    stamped = stamp_legacy_pages()
    print(f"built {len(PAGES) + 1 + len(ALIASES)} pages, {len(rows_all)} rows, "
          f"{len(unverified)} flagged, {len(sources)} sources; stamped {stamped} archived pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
