#!/usr/bin/env python3
"""Build projection.html.

The projection system is deliberately arithmetic-only. Every rate that drives it is
taken from an official publication that was read on 2026-11-07; every derived rate is
recomputed here so the arithmetic can be audited. No property-level value is invented:
the calculator's inputs are typed by the reader, are never stored, and are never sent
anywhere.

Usage:  python3 scripts/build_projection.py
"""
from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED = "2026-11-07"

SCAG = ("https://www.scag.ca.gov/sites/default/files/2024-05/"
        "23-2987-tr-demographics-growth-forecast-final-040424.pdf")
SCAG_PEIR = "https://scag.ca.gov/sites/default/files/2024-05/appendix_i_updated_tables_508_final.pdf"
EDD_PROFILE = ("https://labormarketinfo.edd.ca.gov/cgi/databrowsing/localAreaProfileQSResults.asp"
               "?selectedarea=Los+Angeles+County&selectedindex=19&state=true&geogArea=0604000037"
               "&submit1=View+Local+Area+Profile")
EDD_PDF = "https://labormarketinfo.edd.ca.gov/file/lfmonth/2512pmsa.pdf"
BLS = "https://www.bls.gov/lau/city-annual-unemployment-rates.htm"
CENSUS = "https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225"
DTLA = ("https://planning.lacity.gov/odocument/92b97b24-1978-4e0e-9eae-51f22eda9e4c/"
        "Press%20Release_%20DTLA%20New%20Zoning%20Code.pdf")
ULA = "https://finance.lacity.gov/faq/measure-ula"


def cagr(start: float, end: float, years: int) -> float:
    return (end / start) ** (1 / years) - 1


POP_19, POP_50 = 10_046_000, 10_793_000
EMP_19, EMP_50 = 5_031_000, 5_461_000
HC_22, HC_50 = 1_498, 1_914
CN_22, CN_50 = 473, 621
AF_22, AF_50 = 832, 938
CPI_US_24, CPI_US_25 = 313.7, 321.9
CPI_CA_24, CPI_CA_25 = 342.0, 352.5

pop_cagr = cagr(POP_19, POP_50, 31)
emp_cagr = cagr(EMP_19, EMP_50, 31)
hc_cagr = cagr(HC_22, HC_50, 28)
cn_cagr = cagr(CN_22, CN_50, 28)
af_cagr = cagr(AF_22, AF_50, 28)
cpi_us = CPI_US_25 / CPI_US_24 - 1
cpi_ca = CPI_CA_25 / CPI_CA_24 - 1

# (label, published figures, derived rate, how derived, source label, source url, limit)
RATES = [
    ("Los Angeles County population", "10,046,000 (2019) → 10,793,000 (2050)", f"{pop_cagr*100:+.2f}% a year",
     "Compound annual rate over 31 years, computed here from the two published endpoints.",
     "SCAG Connect SoCal 2024", SCAG,
     "Plan forecast; a county aggregate that says nothing about a corridor or a parcel."),
    ("Los Angeles County employment", "5,031,000 (2019) → 5,461,000 (2050)", f"{emp_cagr*100:+.2f}% a year",
     "Compound annual rate over 31 years from the published endpoints.",
     "SCAG Connect SoCal 2024", SCAG_PEIR,
     "Jobs, not sales. Restaurant demand is not implied."),
    ("Health care and social assistance jobs, SCAG region", "1,498,000 (2022) → 1,914,000 (2050)", f"{hc_cagr*100:+.2f}% a year",
     "Compound annual rate over 28 years from SCAG Table 6.",
     "SCAG Connect SoCal 2024", SCAG,
     "Regional sector total; the fastest-growing large sector in the forecast."),
    ("Construction jobs, SCAG region", "473,000 (2022) → 621,000 (2050)", f"{cn_cagr*100:+.2f}% a year",
     "Compound annual rate over 28 years from SCAG Table 6.",
     "SCAG Connect SoCal 2024", SCAG,
     "Regional sector total; does not establish delivery of any nearby project."),
    ("Accommodation and food services jobs, SCAG region", "832,000 (2022) → 938,000 (2050)", f"{af_cagr*100:+.2f}% a year",
     "Compound annual rate over 28 years from SCAG Table 6.",
     "SCAG Connect SoCal 2024", SCAG,
     "The sector a quick-service site sits in — but a sector total is not a unit's sales."),
    ("Consumer price index, United States, annual averages", "313.7 (2024) → 321.9 (2025)", f"{cpi_us*100:+.1f}% a year",
     "Published annual averages; year-over-year change computed here.",
     "CA EDD (BLS CPI series)", EDD_PROFILE,
     "A national index. Rent escalation in a lease is contractual, not indexed automatically."),
    ("Consumer price index, California, annual averages", "342.0 (2024) → 352.5 (2025)", f"{cpi_ca*100:+.1f}% a year",
     "Published annual averages; year-over-year change computed here.",
     "CA EDD (BLS / DIR CPI series)", EDD_PDF,
     "A state index; it is not a commercial rent index."),
]

SCENARIOS = [
    ("Downside", "Sustained out-migration, weak job growth, insurance or rate shock",
     "Hold the SCAG county rates but assume they are not achieved, and that exit cap rates widen. The test is whether contractual rent still covers debt service and carried costs after a wider exit yield.",
     "SCAG Connect SoCal 2024 low-growth assumptions", SCAG),
    ("Baseline", "The adopted plan forecast is broadly achieved",
     f"County population {pop_cagr*100:+.2f}%/yr and employment {emp_cagr*100:+.2f}%/yr, with food-service sector jobs {af_cagr*100:+.2f}%/yr. Contractual rent growth is set by the lease, not by these rates.",
     "SCAG Connect SoCal 2024 adopted forecast", SCAG),
    ("Upside", "Faster in-migration and job capture, as in the high scenario",
     "Higher growth supports the trade area, but the same warning applies: a county-level upside case cannot be booked as this restaurant's sales.",
     "SCAG Connect SoCal 2024 forecast assumptions, Table 8", SCAG_PEIR),
]

CALC_JS = """
(function () {
  var form = document.querySelector('[data-projection-calc]');
  if (!form) return;
  var out = document.querySelector('[data-projection-output]');
  var money = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });

  function read(name) {
    var el = form.elements[name];
    var v = el ? parseFloat(el.value) : NaN;
    return isFinite(v) ? v : NaN;
  }

  function compute() {
    var rent = read('baseRent');
    var esc = read('escalation') / 100;
    var years = read('years');
    var disc = read('discount') / 100;
    var infl = read('inflation') / 100;
    if (!isFinite(rent) || !isFinite(esc) || !isFinite(years) || !isFinite(disc) || !isFinite(infl) || years < 1) {
      out.innerHTML = '<p class="small muted">Enter a rent figure, an escalation, a hold period and two rates to run the arithmetic.</p>';
      return;
    }
    years = Math.min(Math.round(years), 60);
    var pv = 0, nominal = rent, lastYearRent = rent;
    for (var t = 1; t <= years; t++) {
      nominal = rent * Math.pow(1 + esc, t - 1);
      lastYearRent = nominal;
      pv += nominal / Math.pow(1 + disc, t);
    }
    var realLast = lastYearRent / Math.pow(1 + infl, years);
    var pvReal = pv / Math.pow(1 + infl, years);
    var totalNominal = 0;
    for (var y = 1; y <= years; y++) { totalNominal += rent * Math.pow(1 + esc, y - 1); }
    out.innerHTML =
      '<dl class="calc-results">' +
      '<div><dt>Rent in final hold year</dt><dd>' + money.format(lastYearRent) + '</dd></div>' +
      '<div><dt>Same rent, in today\\'s purchasing power</dt><dd>' + money.format(realLast) + '</dd></div>' +
      '<div><dt>Nominal rent collected over ' + years + ' years</dt><dd>' + money.format(totalNominal) + '</dd></div>' +
      '<div><dt>Present value of that rent stream</dt><dd>' + money.format(pv) + '</dd></div>' +
      '<div><dt>Present value, deflated to today\\'s money</dt><dd>' + money.format(pvReal) + '</dd></div>' +
      '</dl>' +
      '<p class="small muted">Arithmetic only: rent compounded at the escalation you typed, discounted at the rate you typed. No sale price, no expenses, no taxes, no vacancy, no capital expenditure and no value conclusion are produced.</p>';
  }

  form.addEventListener('input', compute);
  form.addEventListener('submit', function (e) { e.preventDefault(); compute(); });
  compute();
})();
"""

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


def build() -> None:
    rate_rows = []
    for (label, figures, rate, how, src_label, src_url, limit) in RATES:
        rate_rows.append(
            f'              <tr><td><strong>{escape(label)}</strong></td>'
            f'<td class="no-wrap">{escape(figures)}</td>'
            f'<td class="no-wrap"><strong>{escape(rate)}</strong></td>'
            f'<td>{escape(how)}<span class="row-note">{escape(limit)}</span></td>'
            f'<td><a class="source-link" href="{src_url}" target="_blank" rel="noopener noreferrer">{escape(src_label)}</a></td></tr>'
        )

    scen_rows = []
    for (name, premise, mechanics, src_label, src_url) in SCENARIOS:
        scen_rows.append(
            f'              <tr><td><strong>{escape(name)}</strong><span class="row-note">{escape(premise)}</span></td>'
            f'<td>{escape(mechanics)}</td>'
            f'<td><a class="source-link" href="{src_url}" target="_blank" rel="noopener noreferrer">{escape(src_label)}</a></td></tr>'
        )

    body = f"""        <header class="page-intro">
          <p class="eyebrow">Projection system · official growth anchors · auditable arithmetic</p>
          <h1>A projection you can recompute by hand.</h1>
          <p class="lead">This model is built the only way an area model can be built honestly without a parcel: every growth rate comes from a published official forecast, every derived rate is shown with the arithmetic that produced it, and the property-level inputs are left for you to type because they are not public.</p>
        </header>

        <div class="callout warning">
          <h3>What this model refuses to do</h3>
          <p class="small">It does not produce a sale price, a market rent, an appraisal, a cash-flow forecast or a recommendation for this asset. Those need the executed lease, the rent roll, the site, the condition report and the owner's tax position — none of which are public. A model that output a value anyway would be inventing it. What follows is the defensible part: official area growth, contractual rent arithmetic, and the explicit list of what is still missing.</p>
        </div>

        <div class="section-heading"><div><p class="eyebrow">Layer 1</p><h2>Official growth anchors</h2><p>Published endpoints on the left, the implied compound rate in the middle, and the arithmetic stated in full so it can be checked with a calculator.</p></div><span class="badge badge-limited">Rates re-read {CHECKED}</span></div>
        <div class="table-tools"><span class="micro muted">Filter the anchors</span><input class="table-search" type="search" placeholder="Search growth anchors…" aria-label="Search growth anchors" data-table-search="growth-anchors"></div>
        <div class="table-wrap">
          <table id="growth-anchors">
            <caption>Every rate this model uses, with its published endpoints and the derivation.</caption>
            <thead><tr><th scope="col">Measure</th><th scope="col">Published endpoints</th><th scope="col">Implied rate</th><th scope="col">Derivation and limit</th><th scope="col">Official source</th></tr></thead>
            <tbody>
{chr(10).join(rate_rows)}
            </tbody>
          </table>
        </div>

        <div class="section-heading"><div><p class="eyebrow">Layer 2</p><h2>Contractual rent arithmetic</h2><p>The one part of the value case that is knowable from documents you already hold: what the lease says the rent does, and what that is worth in today's money. Type your own figures — nothing is stored, transmitted or published.</p></div></div>
        <div class="two-column">
          <section class="panel" aria-labelledby="calc-title">
            <h3 id="calc-title">Run the arithmetic</h3>
            <form data-projection-calc novalidate>
              <p class="small"><label for="baseRent">Current annual base rent (your figure)</label><br>
                <input id="baseRent" name="baseRent" type="number" min="0" step="1000" value="100000" inputmode="decimal" style="width:100%"></p>
              <p class="small"><label for="escalation">Annual escalation stated in the lease (%)</label><br>
                <input id="escalation" name="escalation" type="number" step="0.1" value="2" inputmode="decimal" style="width:100%"></p>
              <p class="small"><label for="years">Years remaining / hold period</label><br>
                <input id="years" name="years" type="number" min="1" max="60" step="1" value="8" inputmode="numeric" style="width:100%"></p>
              <p class="small"><label for="discount">Discount rate (%)</label><br>
                <input id="discount" name="discount" type="number" step="0.1" value="7" inputmode="decimal" style="width:100%"></p>
              <p class="small"><label for="inflation">Inflation used to deflate to today's money (%)</label><br>
                <input id="inflation" name="inflation" type="number" step="0.1" value="2.6" inputmode="decimal" style="width:100%"></p>
              <p class="micro muted">The prefilled values are placeholders to show the arithmetic, not estimates for this asset. Replace them with your lease terms. This page runs entirely in your browser: no figure is sent, saved or logged.</p>
            </form>
          </section>
          <section class="panel" aria-label="Model output">
            <h3>Result</h3>
            <div data-projection-output aria-live="polite"></div>
            <a class="source-link" href="verification.html">How each rate above was verified</a>
          </section>
        </div>

        <div class="section-heading"><div><p class="eyebrow">Layer 3</p><h2>Three scenarios, and what each one tests</h2><p>Scenarios are framed as questions to answer with documents, not as probabilities. No weighting is assigned, because a weighting would be a guess dressed as analysis.</p></div></div>
        <div class="table-wrap">
          <table>
            <caption>Scenario frames anchored on the adopted forecast and its published alternate assumptions.</caption>
            <thead><tr><th scope="col">Scenario</th><th scope="col">What the model does with it</th><th scope="col">Official anchor</th></tr></thead>
            <tbody>
{chr(10).join(scen_rows)}
            </tbody>
          </table>
        </div>

        <div class="section-heading"><div><p class="eyebrow">Layer 4</p><h2>The inputs that decide the outcome are not in this model</h2><p>Because they are not public. Each one is a document request, not a research gap.</p></div></div>
        <div class="three-column">
          <article class="panel"><p class="kicker">Contract</p><h3>Lease and rent</h3><p class="small">Executed lease, all amendments, estoppels, rent ledger, options and notice windows. Without these the escalation input above is a placeholder, not a forecast.</p></article>
          <article class="panel"><p class="kicker">Transfers</p><h3>Value and proceeds</h3><p class="small">Independent valuation or real bids, loan payoff, brokerage and closing costs, and — inside City of LA — the transfer tax measured at closing. <a href="{ULA}">Current ULA rules</a>.</p></article>
          <article class="panel"><p class="kicker">Resilience</p><h3>Hazard, coverage, condition</h3><p class="small">Parcel-level hazard overlays, insurance quotes and exclusions, roof and equipment condition, and seismic or retrofit obligations. See the <a href="risks.html">risk register</a>.</p></article>
        </div>

        <div class="note" style="margin-top:16px"><strong>Reproducible:</strong> this page is generated by <code>scripts/build_projection.py</code>. It recomputes every compound rate from the published endpoints at build time, so the page cannot silently drift from the official figures.</div>

        <script>{CALC_JS}</script>
"""

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Projection model for a Central Los Angeles Jack in the Box NNN decision: official SCAG and CPI growth anchors with auditable arithmetic and a local-only rent calculator. No property value is invented.">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <title>Projection model | Jack in the Box Property Brief</title>
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
{nav_html("projection.html")}
      </nav>
      <div class="sidebar-note"><strong>Privacy-first publication</strong>No owner name, property address, APN, lease document, or individual financial details are published or collected by this site.</div>
    </aside>
    <div class="main-column">
      <header class="topbar"><div class="topbar-left"><button class="nav-toggle" type="button" data-nav-toggle aria-controls="site-nav" aria-expanded="false">☰ <span>Sections</span></button><span class="crumb">Decision support <span aria-hidden="true">/</span> Projection model</span></div><div class="snapshot">Evidence snapshot · 07 Nov 2026</div></header>
      <main id="main-content" class="content">
{body}
      </main>
      <footer class="site-footer"><div class="footer-privacy"><strong>Privacy-first:</strong> no personal information is collected, embedded, or published. Calculator inputs stay in your browser and are never stored.</div><div>Rates recomputed from official endpoints at build time</div></footer>
    </div>
  </div>
</body>
</html>
"""
    (ROOT / "projection.html").write_text(html, encoding="utf-8")
    print("wrote projection.html")
    print(f"  pop CAGR {pop_cagr*100:.3f}%/yr, emp {emp_cagr*100:.3f}%/yr, food-service {af_cagr*100:.3f}%/yr")
    print(f"  CPI US {cpi_us*100:.2f}%, CA {cpi_ca*100:.2f}%")


if __name__ == "__main__":
    build()
