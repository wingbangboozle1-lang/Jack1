#!/usr/bin/env python3
"""Single source of truth for the line-by-line verification register.

Emits VERIFICATION.md (for manual review in the repository) and verification.html
(the published page). Nothing in either output is inferred: every row records what
the official source actually displayed when it was checked on 2026-11-07.

Usage:  python3 scripts/build_verification.py
"""
from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED = "2026-11-07"

CENSUS = "https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225"
BLS = "https://www.bls.gov/lau/city-annual-unemployment-rates.htm"
EDD_PROFILE = ("https://labormarketinfo.edd.ca.gov/cgi/databrowsing/localAreaProfileQSResults.asp"
               "?selectedarea=Los+Angeles+County&selectedindex=19&state=true&geogArea=0604000037"
               "&submit1=View+Local+Area+Profile")
EDD_PDF = "https://labormarketinfo.edd.ca.gov/file/lfmonth/2512pmsa.pdf"
SCAG = ("https://www.scag.ca.gov/sites/default/files/2024-05/"
        "23-2987-tr-demographics-growth-forecast-final-040424.pdf")
SCAG_PEIR = "https://scag.ca.gov/sites/default/files/2024-05/appendix_i_updated_tables_508_final.pdf"
DTLA = ("https://planning.lacity.gov/odocument/92b97b24-1978-4e0e-9eae-51f22eda9e4c/"
        "Press%20Release_%20DTLA%20New%20Zoning%20Code.pdf")
ULA = "https://finance.lacity.gov/faq/measure-ula"
TENQ = "https://www.sec.gov/Archives/edgar/data/807882/000080788226000091/jack-20260705.htm"
TENQ_INDEX = "https://www.sec.gov/Archives/edgar/data/807882/000080788226000091/0000807882-26-000091-index.htm"
TENK = "https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm"
TENK_INDEX = "https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/0000807882-25-000072-index.htm"
ZIMAS = "https://zimas.lacity.org/"
LAPD = ("https://www.lapdonline.org/office-of-the-chief-of-police/office-of-special-operations/"
        "detective-bureau/crime-mapping-and-compstat/")
CALFIRE = ("https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/"
           "fire-hazard-severity-zones")
CDI = "https://www.insurance.ca.gov/01-consumers/180-climate-change/Wildfire-Claims-Tracker.cfm"
IRS544 = "https://www.irs.gov/publications/p544"
LAUSD = "https://explore.lausd.org/"
CDE = "https://www.cde.ca.gov/ta/ac/cm/"

# (id, page(s), item, value_published, source label, source url, what_the_source_shows, status, note)
CLAIMS = [
    ("V-01", "index, market", "Los Angeles city population", "3,869,089",
     "Census QuickFacts", CENSUS,
     "QuickFacts row “Population estimates, July 1, 2025, (V2025)” displays 3,869,089.",
     "verified", ""),
    ("V-02", "index, market", "Population change, 2020 estimates base to July 1 2025", "−0.8%",
     "Census QuickFacts", CENSUS,
     "QuickFacts row “Population, percent change - April 1, 2020 (estimates base) to July 1, 2025” displays -0.8%.",
     "verified", "Source base is 3,899,342; the April 1, 2020 Census count of 3,898,747 is a different figure."),
    ("V-03", "index, market", "Median household income, 2020–2024 ACS, 2024 dollars", "$81,939",
     "Census QuickFacts", CENSUS,
     "QuickFacts row “Median households income (in 2024 dollars), 2020-2024” displays $81,939.",
     "verified", "Citywide household measure, not customer income at any site."),
    ("V-04", "market", "Median gross rent, 2020–2024 ACS", "$1,933 / month",
     "Census QuickFacts", CENSUS,
     "QuickFacts row “Median gross rent, 2020-2024” displays $1,933.",
     "verified", "Residential measure; not commercial rent."),
    ("V-05", "market", "Owner-occupied housing unit rate, 2020–2024 ACS", "36.0%",
     "Census QuickFacts", CENSUS,
     "QuickFacts row “Owner-occupied housing unit rate, 2020-2024” displays 36.0%.",
     "verified", ""),
    ("V-06", "market", "Population per square mile", "8,304.2 people / sq. mi.",
     "Census QuickFacts", CENSUS,
     "QuickFacts row “Population per square mile, 2020” displays 8,304.2 (land area 469.49 sq mi).",
     "verified", "A 2025-vintage density of 8,223 appears elsewhere; the site deliberately cites the 2020 figure."),
    ("V-07", "market", "Total retail sales, 2022", "$81.35 billion",
     "Census QuickFacts", CENSUS,
     "QuickFacts row “Total retail sales, 2022 ($1,000)” displays 81,351,523, i.e. $81.35 billion.",
     "verified", "Unit conversion $1,000 → dollars performed by this site; arithmetic checked."),
    ("V-08", "market", "Accommodation and food services sales, 2022", "$17.37 billion",
     "Census QuickFacts", CENSUS,
     "QuickFacts row “Total accommodation and food services sales, 2022 ($1,000)” displays 17,366,966, i.e. $17.37 billion.",
     "verified", "Unit conversion performed by this site; arithmetic checked."),
    ("V-09", "index, market", "Los Angeles city annual unemployment rate, 2025", "5.8%",
     "BLS LAU city rates", BLS,
     "BLS table row “Los Angeles city, CA … 2025: 5.8”. Footnote: “Estimates for 2025 are 11-month averages that exclude October… not collected due to the federal government shutdown.”",
     "verified", "The site’s caveat about the missing October matches the BLS footnote verbatim in substance."),
    ("V-10", "market", "Los Angeles County unemployment rate, December 2025", "5.0%",
     "CA EDD county profile", EDD_PROFILE,
     "EDD monthly release (2512pmsa.pdf) shows “LOS ANGELES LONG BEACH GLENDALE MD (Los Angeles Co.) … 5,148,900 4,889,600 259,300 5.0%”, December 2025 preliminary, not seasonally adjusted.",
     "verified-with-caveat",
     "On 2026-11-07 the cited county profile page rendered “Data for Los Angeles County not available for Unemployment Rate and Labor Force”. The values were therefore confirmed in EDD’s official monthly PDF, which is now linked as a second source."),
    ("V-11", "market", "County labor force / employed / unemployed, December 2025",
     "5,148,900 / 4,889,600 / 259,300", "CA EDD county profile", EDD_PROFILE,
     "Same EDD December 2025 release: labor force 5,148,900; employed 4,889,600; unemployed 259,300.",
     "verified-with-caveat", "Same profile-page caveat as V-10; see the added EDD PDF link."),
    ("V-12", "market", "Los Angeles County population, 2019 and 2050 forecast",
     "10.046 million (2019) → 10.793 million (2050)", "SCAG forecast PDF", SCAG,
     "SCAG county forecast table (Table 12) reports Los Angeles 10,046,000 (2019) … 10,793,000 (2050); the adopted PEIR Appendix I Table 3.14-8 repeats 10,046,000 / 10,793,000 with a 7.4% increase.",
     "verified", "Adopted planning forecast, not a site population forecast."),
    ("V-13", "market", "Los Angeles County employment, 2019 and 2050 forecast",
     "5.031 million (2019) → 5.461 million (2050)", "SCAG forecast PDF", SCAG,
     "SCAG Table 2 “Total Employment … Los Angeles 5,031,000 (2019) … 5,461,000 (2050)”.",
     "verified", ""),
    ("V-14", "market", "Regional job additions, health care / social assistance, 2022–2050",
     "+416,000", "SCAG forecast PDF", SCAG,
     "SCAG Table 6: 1,498 thousand (2022) → 1,914 thousand (2050) = +416 thousand.",
     "verified", "Difference computed by this site from the published table; arithmetic checked."),
    ("V-15", "market", "Regional job additions, construction, 2022–2050", "+148,000",
     "SCAG forecast PDF", SCAG,
     "SCAG Table 6: 473 thousand (2022) → 621 thousand (2050) = +148 thousand.",
     "verified", "Difference computed by this site; arithmetic checked."),
    ("V-16", "market", "Regional job additions, accommodation / food services, 2022–2050",
     "+106,000", "SCAG forecast PDF", SCAG,
     "SCAG Table 6: 832 thousand (2022) → 938 thousand (2050) = +106 thousand.",
     "verified", "Difference computed by this site; arithmetic checked."),
    ("V-17", "market", "DTLA 2040 planning expectations",
     "100,000 homes; 175,000 additional residents; 100,000 work opportunities",
     "LA City Planning · DTLA 2040", DTLA,
     "Council press release (4 Dec 2024): “expected to create 100,000 new homes, attract 100,000 more work opportunities, and draw 175,000 additional residents to Downtown through the year 2040”.",
     "verified", "Plan expectations inside a seven-square-mile boundary; no parcel match has been made."),
    ("V-18", "property", "Total revenues, 12 weeks ended July 5 2026 vs July 6 2025",
     "$257,657 vs $262,401 (thousands)", "SEC 10-Q", TENQ,
     "Condensed consolidated statements of earnings show total revenues 257,657 (quarter ended July 5, 2026) and 262,401 (quarter ended July 6, 2025), in thousands.",
     "verified", "Consolidated continuing operations; not the subject restaurant’s sales."),
    ("V-19", "property", "Earnings from continuing operations, 12-week period",
     "$21,041 vs $22,839 (thousands)", "SEC 10-Q", TENQ,
     "Same statement: “Earnings from continuing operations 21,041” and prior-year 22,839.",
     "verified", ""),
    ("V-20", "property", "Total revenues, 40 weeks ended July 5 2026 vs prior year",
     "$861,438 vs $899,196 (thousands)", "SEC 10-Q", TENQ,
     "Same statement, year-to-date columns: 861,438 and 899,196.",
     "verified", ""),
    ("V-21", "property", "Earnings from continuing operations, 40-week period",
     "$47,971 vs $74,534 (thousands)", "SEC 10-Q", TENQ,
     "Same statement, year-to-date columns: 47,971 and 74,534.",
     "verified", ""),
    ("V-22", "property", "Current maturities of long-term debt, July 5 2026", "$44,160 (thousands)",
     "SEC 10-Q", TENQ,
     "Balance sheet line “Current maturities of long-term debt 44,160” (September 28, 2025: 29,458).",
     "verified", "Issuer-level item; not the owner’s or franchisee’s debt."),
    ("V-23", "property", "Long-term debt, net of current maturities, July 5 2026",
     "$1,428,667 (thousands)", "SEC 10-Q", TENQ,
     "Balance sheet line “Long-term debt, net of current maturities 1,428,667”.",
     "verified", ""),
    ("V-24", "property", "Jack in the Box restaurants by operating model, July 5 2026",
     "149 company-operated; 1,966 franchise-operated", "SEC 10-Q", TENQ,
     "Nature of operations note: “As of July 5, 2026, there were 149 company-operated and 1,966 franchise-operated Jack in the Box restaurants.”",
     "verified", "Portfolio-wide count; it does not identify the operator of any single unit."),
    ("V-25", "property", "Del Taco presented as discontinued operations",
     "Reported as discontinued operations after the December 2025 sale", "SEC 10-Q", TENQ,
     "XBRL contexts tag Del Taco as discontinued operations disposed of by sale, with a 2025-12-22 disposal date; the income statement shows “Losses from discontinued operations, net of taxes” separately.",
     "verified", ""),
    ("V-26", "property, decision, risks", "Measure ULA thresholds and rates in force for closings after June 30 2026",
     "$5,400,000 / $10,900,000; ULA 4% and 5.5%; base rate 0.45%",
     "LA City Office of Finance", ULA,
     "FAQ note: “Effective for transactions closing after June 30, 2026, the new ULA thresholds will be $5,400,000 and $10,900,000… greater than $5,400,000 but less than $10,900,000 will be assessed a 4% tax, and transactions of $10,900,000 or greater… 5.5%.” Base Tax “$2.25 per $500” = 0.45%.",
     "verified",
     "Resolves open item U-09 from two earlier sessions, which could not confirm the indexed thresholds and withheld them. They are confirmed here on the City’s own page and are CPI-indexed annually."),
    ("V-27", "property, sources", "Identity of the cited FY2025 annual report",
     "Form 10-K, period 2025-09-28, filed 2025-11-19", "SEC EDGAR filing index", TENK_INDEX,
     "EDGAR index page states “Form 10-K — Annual report”, period of report 2025-09-28, filing date 2025-11-19, for JACK IN THE BOX INC (CIK 0000807882).",
     "verified", ""),
    ("V-28", "property, sources", "Identity and structure of the cited 2026 quarterly report",
     "Form 10-Q, period 2026-07-05, filed 2026-08-12; 12-week and 40-week periods",
     "SEC EDGAR filing index", TENQ_INDEX,
     "EDGAR index page states “Form 10-Q — Quarterly report”, period 2026-07-05, filed 2026-08-12; the statement columns are headed Quarter and Year-to-date (12 and 40 weeks).",
     "verified", ""),
    ("V-29", "sources", "SEC statements are presented in thousands of US dollars",
     "Amounts in thousands", "SEC 10-Q", TENQ,
     "Balance sheet and earnings statements are headed “(In thousands, except share and per share data)”.",
     "verified", ""),
]

LINKS = [
    ("L-01", "Census QuickFacts", CENSUS, "Reachable; full table rendered and read.", "pass"),
    ("L-02", "BLS largest-city unemployment table", BLS, "Reachable; table and footnote read.", "pass"),
    ("L-03", "CA EDD Los Angeles County profile", EDD_PROFILE,
     "Reachable, but the unemployment / labor-force block now reads “Data for Los Angeles County not available”.", "caveat"),
    ("L-04", "CA EDD December 2025 monthly release (PDF)", EDD_PDF,
     "Reachable; county table located and read.", "pass"),
    ("L-05", "SCAG Connect SoCal 2024 technical report (PDF)", SCAG,
     "Reachable; Tables 2, 6 and 12 read.", "pass"),
    ("L-06", "LA City Planning DTLA 2040 press release (PDF)", DTLA, "Reachable; figures read.", "pass"),
    ("L-07", "LA City Office of Finance Measure ULA FAQ", ULA, "Reachable; thresholds, rates and base tax read.", "pass"),
    ("L-08", "SEC 10-Q document and filing index", TENQ_INDEX, "Reachable; form type, dates and statements read.", "pass"),
    ("L-09", "SEC 10-K document and filing index", TENK_INDEX, "Reachable; form type and dates read.", "pass"),
    ("L-10", "LA City ZIMAS", ZIMAS, "Reachable; public parcel application loads.", "pass"),
    ("L-11", "LAPD Crime Mapping and COMPSTAT", LAPD,
     "Reachable; page states the CrimeMapping platform “is currently undergoing updates” — the site’s wording matches.", "pass"),
    ("L-12", "CAL FIRE / OSFM Fire Hazard Severity Zones", CALFIRE,
     "Reachable; 2025 LRA rollout and 2026 SRA comment period shown.", "pass"),
    ("L-13", "California Department of Insurance LA County wildfire claims tracker", CDI,
     "Reachable; 41,727 claims filed and $25.2 billion paid, updated 6 July 2026.", "pass"),
    ("L-14", "IRS Publication 544 (2025)", IRS544, "Reachable; disposition and like-kind exchange authority.", "pass"),
    ("L-15", "LAUSD School Explorer", LAUSD, "Reachable; school search application loads.", "pass"),
    ("L-16", "California Department of Education accountability landing page", CDE,
     "Reachable; titled “California School Dashboard and System of Support”.", "pass"),
]

NOT_RETESTED = [
    ("FTB capital gains guidance", "https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html"),
    ("LA County Assessor parcel portal", "https://portal.assessor.lacounty.gov/"),
    ("LA County Assessor Proposition 13 page", "https://assessor.lacounty.gov/real-estate-toolkit/proposition-13"),
    ("LA City Planning zoning search", "https://planning.lacity.gov/zoning/zoning-search"),
    ("CGS EQ Zapp", "https://maps.conservation.ca.gov/cgs/EQZApp/app/"),
    ("FEMA flood map products", "https://www.fema.gov/flood-maps/products-tools"),
    ("LA County DPW flood map", "https://apps.gis.lacounty.gov/dpw/m/?viewer=floodzone"),
    ("State Water Boards GeoTracker", "https://geotracker.waterboards.ca.gov/"),
    ("U.S. EPA", "https://www.epa.gov/"),
    ("NOAA Climate.gov", "https://www.climate.gov/"),
    ("LA County Public Health", "http://publichealth.lacounty.gov/eh/heat/index.htm"),
    ("LA Metro system maps", "https://www.metro.net/riding/guide/system-maps/"),
    ("LADWP", "https://www.ladwp.com/"),
    ("USGS earthquake hazards", "https://www.usgs.gov/programs/earthquake-hazards"),
]

IRREGULARITIES = [
    ("I-01", "CA EDD county profile page currently withholds the labor-force block",
     "The two EDD-sourced rows cite a page that, when read on 2026-11-07, renders “Data for Los Angeles County not available for Unemployment Rate and Labor Force”. The published values were confirmed in EDD’s own December 2025 monthly PDF instead.",
     "EDD monthly release linked beside the profile page; row marked verified-with-caveat.",
     "reviewed", "EDD monthly release", EDD_PDF),
    ("I-02", "Unresolved merge-conflict markers committed to COORDINATION.md",
     "Two blocks containing literal <<<<<<< / ======= / >>>>>>> markers were committed to the task board, meaning two sessions’ text had been merged without resolution.",
     "Both sides preserved verbatim in original order with a dated repair note. Nothing deleted.",
     "repaired", "Repository record", "https://github.com/wingbangboozle1-lang/Jack1/blob/main/COORDINATION.md"),
    ("I-03", "Eight archived build files committed with conflict markers",
     "archive/arena-ffc97e4e/ shipped seven HTML files and one stylesheet containing raw conflict markers, which broke those archived pages.",
     "Each file resolved to that archive’s own side. Verified first that 100% of the other side’s substantive lines already exist verbatim in archive/arena-d2137d88/ (59/59, 18/18, 21/21, 57/57, 23/23, 34/34, 26/26 lines; 112/112 CSS lines), so no unique work was discarded.",
     "repaired", "Repository record", "https://github.com/wingbangboozle1-lang/Jack1/blob/main/archive/arena-ffc97e4e/index.html"),
    ("I-04", "Measure ULA indexed thresholds were previously withheld as unverifiable",
     "Two earlier sessions flagged the $5.4M / $10.9M thresholds as unconfirmed and deliberately did not publish them.",
     "Confirmed on the City Office of Finance FAQ. Thresholds are CPI-indexed annually and must be re-read at closing.",
     "resolved", "City Office of Finance", ULA),
    ("I-05", "Source label precision for the school accountability link",
     "A row labelled “California School Dashboard” linked to the CDE landing page rather than the Dashboard application itself.",
     "Label rewritten to “CDE · California School Dashboard”. The link is official and works.",
     "repaired", "CDE accountability page", CDE),
    ("I-06", "Fourteen official links were not re-tested in this pass",
     "Rebuilding the site does not by itself prove that every external tool still responds; only the sixteen links in the link table were actually fetched on 2026-11-07.",
     "Listed individually below so availability is never implied. Local links are machine-checked on every push.",
     "open", "Example of an untested link", "https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html"),
    ("I-07", "The lease-expiry window is owner-reported, not verified",
     "The 2030–2035 expiry range and the NNN structure come from the owner’s description. No public record confirms either, and no parcel has been identified.",
     "Shown as a working premise on every page and left blank in the asset tables.",
     "open", "Lookup that would settle it", ZIMAS),
]


def md_claims() -> str:
    out = [f"Checked {CHECKED} against the source shown. Status vocabulary: **verified**, "
           "**verified-with-caveat**, **flagged** (not confirmed → value left blank on the site).\n"]
    out.append("| ID | Page(s) | Published item | Value as published | Official source | What the source displays | Status | Note |")
    out.append("|---|---|---|---|---|---|---|---|")
    for (vid, pages, item, value, label, url, shows, status, note) in CLAIMS:
        out.append(f"| {vid} | {pages} | {item} | {value} | [{label}]({url}) | {shows} | {status} | {note} |")
    return "\n".join(out)


def md_links() -> str:
    out = ["| ID | Link | Result on %s | Status |" % CHECKED, "|---|---|---|---|"]
    for (lid, label, url, result, status) in LINKS:
        out.append(f"| {lid} | [{label}]({url}) | {result} | {status} |")
    out.append("")
    out.append("### Not re-tested in this pass (availability not asserted)\n")
    for label, url in NOT_RETESTED:
        out.append(f"- [{label}]({url})")
    return "\n".join(out)


def md_irregularities() -> str:
    out = ["| ID | Irregularity | Detail | Disposition | State | Evidence |", "|---|---|---|---|---|---|"]
    for (iid, title, detail, fix, state, ev_label, ev_url) in IRREGULARITIES:
        out.append(f"| {iid} | {title} | {detail} | {fix} | {state} | [{ev_label}]({ev_url}) |")
    return "\n".join(out)


def write_markdown() -> None:
    body = f"""# Verification register

Line-by-line re-verification of every figure and every cited official source published by
this dashboard. Checked by session `arena/6d4bd5df-jack1` on **{CHECKED}**.

This file and `verification.html` are generated by `scripts/build_verification.py` from a single
register, so the published page and this log cannot drift apart.

**Result of this pass:** {len(CLAIMS)} published items re-checked — {sum(1 for c in CLAIMS if c[7] == 'verified')} verified exactly,
{sum(1 for c in CLAIMS if c[7] == 'verified-with-caveat')} verified with a caveat, 0 wrong values, 0 unverified values published.
{len(LINKS)} official links were fetched; {len(NOT_RETESTED)} links were not re-tested and are listed rather than assumed.

## 1. Published figures, re-checked line by line

{md_claims()}

## 2. Link availability re-test

{md_links()}

## 3. Irregularities found and their disposition

{md_irregularities()}

## 4. What this register does not claim

- It does not verify any property-specific fact: no parcel, address, APN, owner, lease, rent,
  guaranty, operating statement, or insurance policy was available.
- It does not convert area statistics into a site forecast, an appraisal, or a recommendation.
- It does not assert that a value will still be current later. Official pages change; every row
  carries the date it was read.
- Arithmetic performed by this site (unit conversions in V-07/V-08, differences in V-14 to V-16)
  is shown in the row so it can be recomputed by hand.

## 5. Privacy

No personal information appears in this register. No owner name, address, parcel number, or
individual financial detail was collected, stored, or published in producing it.
"""
    (ROOT / "VERIFICATION.md").write_text(body, encoding="utf-8")


def badge(status: str) -> str:
    if status == "verified":
        return '<span class="badge badge-verified">Verified</span>'
    if status == "verified-with-caveat":
        return '<span class="badge badge-limited">Verified · caveat</span>'
    return '<span class="badge badge-review">Flagged</span>'


NAV = [
    ("index.html", "Executive summary"),
    ("market.html", "Local market"),
    ("property.html", "Lease &amp; asset"),
    ("decision.html", "Sell / renew paths"),
    ("projection.html", "Projection model"),
    ("risks.html", "Risk register"),
    ("flagged.html", "Flagged for Review"),
    ("verification.html", "Verification log"),
    ("sources.html", "Sources &amp; method"),
]


def nav_html(current: str) -> str:
    items = []
    for i, (href, label) in enumerate(NAV, start=1):
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'        <a href="{href}"{cur}><span class="nav-dot">{i:02d}</span>{label}</a>')
    return "\n".join(items)


def page_shell(title: str, description: str, current: str, crumb: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <title>{escape(title)} | Jack in the Box Property Brief</title>
  <link rel="stylesheet" href="assets/styles.css">
  <script src="assets/site.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
  <div class="app-shell">
    <aside class="sidebar" id="site-nav" aria-label="Main navigation">
      <a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">JB</span><span class="brand-copy"><strong>Property decision brief</strong><span>Central Los Angeles · public-data review</span></span></a>
      <p class="nav-label">Research dashboard</p>
      <nav class="site-nav">
{nav_html(current)}
      </nav>
      <div class="sidebar-note"><strong>Privacy-first publication</strong>No owner name, property address, APN, lease document, or individual financial details are published or collected by this site.</div>
    </aside>
    <div class="main-column">
      <header class="topbar"><div class="topbar-left"><button class="nav-toggle" type="button" data-nav-toggle aria-controls="site-nav" aria-expanded="false">☰ <span>Sections</span></button><span class="crumb">Decision support <span aria-hidden="true">/</span> {crumb}</span></div><div class="snapshot">Evidence snapshot · 07 Nov 2026</div></header>
      <main id="main-content" class="content">
{body}
      </main>
      <footer class="site-footer"><div class="footer-privacy"><strong>Privacy-first:</strong> no personal information is collected, embedded, or published. Property identifiers are intentionally omitted.</div><div>Sources re-read {CHECKED} · no value filled without an official source</div></footer>
    </div>
  </div>
</body>
</html>
"""


def write_html() -> None:
    n_verified = sum(1 for c in CLAIMS if c[7] == "verified")
    n_caveat = sum(1 for c in CLAIMS if c[7] == "verified-with-caveat")

    rows = []
    for (vid, pages, item, value, label, url, shows, status, note) in CLAIMS:
        note_html = f'<span class="row-note">{escape(note)}</span>' if note else ""
        rows.append(
            f'              <tr><td class="no-wrap"><strong>{vid}</strong></td>'
            f'<td>{escape(item)}</td>'
            f'<td class="no-wrap">{escape(value)}</td>'
            f'<td>{badge(status)}</td>'
            f'<td>{escape(shows)}{note_html}</td>'
            f'<td><a class="source-link" href="{url}" target="_blank" rel="noopener noreferrer">{escape(label)}</a></td></tr>'
        )

    ok_badge = '<span class="badge badge-verified">ok</span>'
    caveat_badge = '<span class="badge badge-limited">caveat</span>'
    link_rows = []
    for (lid, label, url, result, status) in LINKS:
        status_html = ok_badge if status == "pass" else caveat_badge
        link_rows.append(
            f'              <tr><td class="no-wrap"><strong>{lid}</strong></td>'
            f'<td>{escape(result)}</td>'
            f'<td>{status_html}</td>'
            f'<td><a class="source-link" href="{url}" target="_blank" rel="noopener noreferrer">{escape(label)}</a></td></tr>'
        )

    untested_rows = []
    for label, url in NOT_RETESTED:
        untested_rows.append(
            f'              <tr><td>{escape(label)}</td><td class="blank-value" aria-label="Not re-tested, no result recorded"></td>'
            f'<td><span class="badge badge-review">Not re-tested</span><span class="row-note">Availability on {CHECKED} is not asserted.</span></td>'
            f'<td><a class="source-link" href="{url}" target="_blank" rel="noopener noreferrer">Official page</a></td></tr>'
        )

    irr_rows = []
    for (iid, title, detail, fix, state, ev_label, ev_url) in IRREGULARITIES:
        state_cls = "badge-verified" if state in ("repaired", "resolved") else "badge-review"
        irr_rows.append(
            f'              <tr><td class="no-wrap"><strong>{iid}</strong></td>'
            f'<td><strong>{escape(title)}</strong><span class="row-note">{escape(detail)}</span></td>'
            f'<td>{escape(fix)}</td>'
            f'<td><span class="badge {state_cls}">{escape(state)}</span></td>'
            f'<td><a class="source-link" href="{ev_url}" target="_blank" rel="noopener noreferrer">{escape(ev_label)}</a></td></tr>'
        )

    claims_html = chr(10).join(rows)
    links_html = chr(10).join(link_rows)
    untested_html = chr(10).join(untested_rows)
    irr_html = chr(10).join(irr_rows)

    body = f"""        <header class="page-intro">
          <p class="eyebrow">Line-by-line re-verification · {len(CLAIMS)} items · {CHECKED}</p>
          <h1>Every published figure, re-read at its official source.</h1>
          <p class="lead">This page records what each official source actually displayed when it was opened on 07 November 2026. It exists because a source link proves nothing on its own: a cited page can change, be withdrawn, or stop showing the figure a site quotes from it. One linked page on this site had already done exactly that.</p>
        </header>

        <section class="card-grid" aria-label="Verification totals">
          <article class="metric-card">
            <div class="metric-label">Items re-checked</div>
            <div class="metric-value">{len(CLAIMS)}</div>
            <div class="metric-meta">Every numeric or dated claim published on this site</div>
          </article>
          <article class="metric-card">
            <div class="metric-label">Verified exactly</div>
            <div class="metric-value">{n_verified}</div>
            <div class="metric-meta">Value matches the official source as displayed</div>
          </article>
          <article class="metric-card">
            <div class="metric-label">Verified with caveat</div>
            <div class="metric-value">{n_caveat}</div>
            <div class="metric-meta">Correct, but the cited page no longer shows it</div>
          </article>
          <article class="metric-card">
            <div class="metric-label">Wrong or unverifiable values published</div>
            <div class="metric-value">0</div>
            <div class="metric-meta">No value was found to be incorrect or unsourced</div>
          </article>
        </section>

        <div class="callout warning">
          <h3>What a "verified" badge does and does not mean</h3>
          <p class="small">It means the number or date shown was read at the linked official source on {CHECKED} and matched. It does <strong>not</strong> mean the source is right about the future, that the geography is the subject property's geography, or that the figure will still be current tomorrow. Area statistics remain area statistics: none of them has been converted into a site forecast, an appraisal, or a rent estimate.</p>
        </div>

        <div class="section-heading"><div><p class="eyebrow">Part 1</p><h2>Published figures, re-checked</h2><p>Each row states exactly what the source displayed, not a paraphrase of what it should say.</p></div><span class="badge badge-limited">Checked {CHECKED}</span></div>
        <div class="table-tools"><span class="micro muted">Filter these checks</span><input class="table-search" type="search" placeholder="Search verification items…" aria-label="Search verification items" data-table-search="verification-claims"></div>
        <div class="table-wrap">
          <table id="verification-claims">
            <caption>Every published figure and the official source it was re-read from on {CHECKED}.</caption>
            <thead><tr><th scope="col">ID</th><th scope="col">Published item</th><th scope="col">Value as published</th><th scope="col">Result</th><th scope="col">What the source displayed</th><th scope="col">Official source</th></tr></thead>
            <tbody>
{claims_html}
            </tbody>
          </table>
        </div>

        <div class="section-heading"><div><p class="eyebrow">Part 2</p><h2>Link availability re-test</h2><p>Sixteen official links were actually opened. Fourteen were not, and are listed separately rather than assumed to work.</p></div></div>
        <div class="table-wrap">
          <table>
            <caption>Links opened on {CHECKED}.</caption>
            <thead><tr><th scope="col">ID</th><th scope="col">Result</th><th scope="col">Status</th><th scope="col">Link</th></tr></thead>
            <tbody>
{links_html}
            </tbody>
          </table>
        </div>

        <div class="table-wrap" style="margin-top:14px">
          <table>
            <caption>Official pages carried by this site that were <strong>not</strong> re-tested in this pass. The value column is intentionally blank.</caption>
            <thead><tr><th scope="col">Link</th><th scope="col">Result</th><th scope="col">Status</th><th scope="col">Official page</th></tr></thead>
            <tbody>
{untested_html}
            </tbody>
          </table>
        </div>

        <div class="section-heading"><div><p class="eyebrow">Part 3</p><h2>Irregularities found and what was done</h2><p>Including two that were committed to this repository and had to be repaired, and one that earlier sessions correctly refused to publish until it could be confirmed.</p></div><span class="badge badge-review">Audit trail</span></div>
        <div class="table-wrap">
          <table>
            <caption>Defects found during this pass, with disposition and state.</caption>
            <thead><tr><th scope="col">ID</th><th scope="col">Irregularity</th><th scope="col">Disposition</th><th scope="col">State</th><th scope="col">Evidence</th></tr></thead>
            <tbody>
{irr_html}
            </tbody>
          </table>
        </div>

        <div class="note" style="margin-top:16px"><strong>Reproducible:</strong> this page is generated from one register by <code>scripts/build_verification.py</code>, which also writes <code>VERIFICATION.md</code>. Re-running it reproduces both outputs, and no row is edited by hand.</div>
"""
    (ROOT / "verification.html").write_text(
        page_shell(
            "Verification log",
            "Line-by-line re-verification of every published figure against its official source, checked 07 November 2026, with link tests and irregularities.",
            "verification.html",
            "Verification log",
            body,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    write_markdown()
    write_html()
    print(f"wrote VERIFICATION.md and verification.html ({len(CLAIMS)} claims, {len(LINKS)} link tests, "
          f"{len(NOT_RETESTED)} untested, {len(IRREGULARITIES)} irregularities)")
