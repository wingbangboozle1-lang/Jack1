#!/usr/bin/env python3
"""Builds the static dashboard site from scripts/dataset.py and scripts/analysis.py.

Design rules:
  * every table row carries an official source link
  * unverified values render as an em dash and a "unverified" pill, never as a number
  * withheld private fields render as "[WITHHELD]"
  * no external requests: no CDN, no web fonts, no analytics
  * relative links only, so the site works from a project Pages URL
"""
from __future__ import annotations

import html
import importlib.util
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ds = _load("dataset", "scripts/dataset.py")
an = _load("analysis", "scripts/analysis.py")

MODEL = an.build_model()

PAGES = [
    ("index.html", "01", "Overview", "The decision in one screen"),
    ("market.html", "02", "Market &amp; area", "Population, income, housing, jobs, prices"),
    ("projections.html", "03", "Projections &amp; model", "Official forecasts and the scenario model"),
    ("tenant.html", "04", "Tenant credit", "Jack in the Box's own SEC disclosures"),
    ("property.html", "05", "Property &amp; hazards", "Lease fields, parcel checks, catastrophe"),
    ("decision.html", "06", "Decision paths", "Sell, renew, hold, exchange"),
    ("risks.html", "07", "Risk register", f"{len(an.RISKS)} risks with severity"),
    ("flagged.html", "08", "Flagged for review", "Every unverified and withheld item"),
    ("sources.html", "09", "Sources &amp; method", "Every source, and how it was checked"),
]

STATUS_LABEL = {
    "verified": ("Verified", "ok"),
    "derived": ("Derived", "calc"),
    "unverified": ("Unverified", "bad"),
    "withheld": ("Withheld", "held"),
}

CSS = """
:root{
  --bg:#f5f6f8; --panel:#ffffff; --ink:#14181f; --muted:#5c6673; --line:#dfe3e9;
  --brand:#12263f; --accent:#b3282d; --ok:#1d6b45; --okbg:#e6f2ec;
  --bad:#8c2f19; --badbg:#fbeae4; --calc:#2f4d7a; --calcbg:#e8eef7;
  --held:#5b4a8a; --heldbg:#eeeaf7; --warnbg:#fff8e6; --warnline:#e6cf87;
  --radius:10px; --shadow:0 1px 2px rgba(16,24,40,.06),0 1px 3px rgba(16,24,40,.06);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
  font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:#1a4f8a;text-underline-offset:2px}
a:hover{color:var(--accent)}
.skip{position:absolute;left:-9999px}
.skip:focus{left:8px;top:8px;z-index:99;background:#fff;padding:8px 12px;border:2px solid var(--brand)}
.shell{display:flex;min-height:100vh}
.sidebar{width:264px;flex:0 0 264px;background:var(--brand);color:#e9eef5;padding:18px 16px 28px;
  position:sticky;top:0;height:100vh;overflow-y:auto}
.brand{display:flex;gap:10px;align-items:center;text-decoration:none;color:#fff;margin-bottom:18px}
.brand .mark{width:34px;height:34px;border-radius:8px;background:var(--accent);display:grid;place-items:center;
  font-weight:700;font-size:14px;letter-spacing:.5px;flex:0 0 34px}
.brand b{display:block;font-size:14px;line-height:1.25}
.brand span{display:block;font-size:11px;color:#a9b8ca;line-height:1.3}
.navlabel{font-size:10.5px;letter-spacing:.10em;text-transform:uppercase;color:#8ea3bb;margin:16px 0 8px}
.sidebar nav a{display:flex;gap:10px;align-items:baseline;padding:8px 10px;border-radius:8px;
  color:#dae3ee;text-decoration:none;font-size:13.5px;line-height:1.3}
.sidebar nav a .n{font-variant-numeric:tabular-nums;color:#7e94ae;font-size:11px;flex:0 0 16px}
.sidebar nav a:hover{background:#1c3350;color:#fff}
.sidebar nav a[aria-current=page]{background:#fff;color:var(--brand);font-weight:600}
.sidebar nav a[aria-current=page] .n{color:var(--accent)}
.sidebar .note{margin-top:18px;padding:10px 12px;border:1px solid #2b4763;border-radius:8px;
  font-size:11.5px;color:#b9c7d6;line-height:1.45}
.main{flex:1 1 auto;min-width:0;display:flex;flex-direction:column}
.topbar{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:12px 28px;
  background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20}
.crumb{font-size:12.5px;color:var(--muted)}
.crumb b{color:var(--ink)}
.snap{font-size:11.5px;color:var(--muted);background:var(--bg);border:1px solid var(--line);
  border-radius:999px;padding:4px 10px;white-space:nowrap}
.navtoggle{display:none;background:#fff;border:1px solid var(--line);border-radius:8px;padding:6px 10px;font:inherit;cursor:pointer}
main{padding:26px 28px 64px;max-width:1200px;width:100%}
h1{font-size:28px;line-height:1.2;letter-spacing:-.01em;margin:6px 0 10px}
h2{font-size:19px;line-height:1.3;margin:0 0 4px;letter-spacing:-.01em}
h3{font-size:15px;margin:0 0 6px}
.eyebrow{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);font-weight:700;margin:0}
.lede{font-size:15.5px;color:#333c48;max-width:74ch}
.muted{color:var(--muted)}
.small{font-size:12.5px}
.hero{background:#fff;border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:var(--radius);
  padding:22px 24px;box-shadow:var(--shadow);margin-bottom:22px}
.hero h1{margin-top:8px}
.pill{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
  padding:3px 9px;border-radius:999px;white-space:nowrap}
.pill.ok{background:var(--okbg);color:var(--ok)}
.pill.bad{background:var(--badbg);color:var(--bad)}
.pill.calc{background:var(--calcbg);color:var(--calc)}
.pill.held{background:var(--heldbg);color:var(--held)}
.pill.neutral{background:#eef1f5;color:#46505d}
.grid{display:grid;gap:14px}
.g3{grid-template-columns:repeat(3,minmax(0,1fr))}
.g4{grid-template-columns:repeat(4,minmax(0,1fr))}
.g2{grid-template-columns:repeat(2,minmax(0,1fr))}
.card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:16px 18px;box-shadow:var(--shadow)}
.card .k{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.card .v{font-size:24px;font-weight:650;letter-spacing:-.02em;line-height:1.15}
.card .v small{font-size:13px;font-weight:500;color:var(--muted)}
.card .m{font-size:12px;color:var(--muted);margin-top:6px}
.card a.src{display:inline-block;margin-top:8px;font-size:11.5px}
.panel{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:20px 22px;
  box-shadow:var(--shadow);margin:18px 0}
.panel > .hd{display:flex;justify-content:space-between;align-items:flex-end;gap:14px;flex-wrap:wrap;margin-bottom:12px}
.verdict{background:linear-gradient(180deg,#fffdf7,#fff8e6);border:1px solid var(--warnline);
  border-radius:var(--radius);padding:18px 20px}
.verdict h2{margin-bottom:8px}
.actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}
.btn{display:inline-block;background:var(--brand);color:#fff;text-decoration:none;padding:10px 16px;
  border-radius:8px;font-size:13.5px;font-weight:600}
.btn:hover{background:#1c3350;color:#fff}
.btn.ghost{background:#fff;color:var(--brand);border:1px solid var(--line)}
.btn.ghost:hover{background:#f0f3f7;color:var(--brand)}
ol.steps{margin:8px 0 0;padding-left:20px}
ol.steps li{margin-bottom:10px}
ul.clean{margin:8px 0 0;padding-left:18px}
ul.clean li{margin-bottom:7px}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:8px;background:#fff}
table{border-collapse:collapse;width:100%;font-size:13px}
caption{caption-side:top;text-align:left;font-size:12px;color:var(--muted);padding:0 0 8px}
th,td{text-align:left;padding:9px 11px;border-bottom:1px solid var(--line);vertical-align:top}
thead th{background:#f0f3f7;font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;
  color:#46505d;position:sticky;top:0;white-space:nowrap;z-index:1}
tbody tr:hover{background:#fafbfd}
tbody tr:last-child td{border-bottom:none}
td.num{font-variant-numeric:tabular-nums;white-space:nowrap;font-weight:600}
td.id{font-variant-numeric:tabular-nums;color:var(--muted);font-size:11.5px;white-space:nowrap}
td .blank{color:#9aa4b1;font-weight:500}
td.src{font-size:11.5px;min-width:150px}
td.note{font-size:11.5px;color:var(--muted);max-width:340px}
.search{display:flex;gap:10px;align-items:center;margin-bottom:10px;flex-wrap:wrap}
.search input{font:inherit;font-size:13px;padding:7px 11px;border:1px solid var(--line);border-radius:8px;
  min-width:240px;background:#fff}
.search .count{font-size:12px;color:var(--muted)}
.callout{border-radius:8px;padding:12px 14px;font-size:13px;border:1px solid var(--line);background:#f8fafc}
.callout.warn{background:var(--warnbg);border-color:var(--warnline)}
.callout.bad{background:var(--badbg);border-color:#e7bfae}
.callout.ok{background:var(--okbg);border-color:#bcdccb}
.callout b{display:block;margin-bottom:4px}
.tag{display:inline-block;font-size:10.5px;padding:1px 7px;border-radius:5px;background:#eef1f5;color:#46505d;margin:0 4px 4px 0}
.tag.ba{background:#e8eef7;color:#2f4d7a}
.tag.bs{background:#fbeae4;color:#8c2f19}
.tag.personal{background:#eeeaf7;color:#5b4a8a}
footer{border-top:1px solid var(--line);padding:18px 28px;color:var(--muted);font-size:12px;background:#fff}
.kv{display:grid;grid-template-columns:180px 1fr;gap:6px 14px;font-size:13px}
.kv dt{color:var(--muted)}
.kv dd{margin:0}
details{border:1px solid var(--line);border-radius:8px;padding:10px 14px;background:#fff;margin:10px 0}
summary{cursor:pointer;font-weight:600;font-size:13.5px}
@media(max-width:1080px){.g4{grid-template-columns:repeat(2,minmax(0,1fr))}.g3{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:820px){
  .shell{display:block}
  .sidebar{position:fixed;left:0;top:0;bottom:0;z-index:60;transform:translateX(-100%);
    transition:transform .18s ease;height:100vh}
  .sidebar.open{transform:none;box-shadow:0 0 0 100vmax rgba(10,18,28,.45)}
  .navtoggle{display:inline-flex;gap:6px;align-items:center}
  main{padding:20px 16px 56px}
  .topbar{padding:10px 16px}
  .g2,.g3,.g4{grid-template-columns:1fr}
  .kv{grid-template-columns:1fr}
  h1{font-size:23px}
}
@media print{.sidebar,.topbar,.navtoggle{display:none}main{padding:0}}
"""

JS = """
(function(){
  var b=document.querySelector('[data-nav]');
  var sb=document.querySelector('.sidebar');
  if(b&&sb){
    b.addEventListener('click',function(){
      var open=sb.classList.toggle('open');
      b.setAttribute('aria-expanded',String(open));
    });
    sb.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){sb.classList.remove('open');});});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'){sb.classList.remove('open');}});
  }
  document.querySelectorAll('[data-filter]').forEach(function(input){
    var table=document.getElementById(input.getAttribute('data-filter'));
    if(!table)return;
    var rows=Array.prototype.slice.call(table.querySelectorAll('tbody tr'));
    var count=document.querySelector('[data-count-for="'+table.id+'"]');
    function apply(){
      var q=input.value.trim().toLowerCase();
      var shown=0;
      rows.forEach(function(r){
        var hit=!q||r.textContent.toLowerCase().indexOf(q)>-1;
        r.hidden=!hit;
        if(hit)shown++;
      });
      if(count)count.textContent=shown+' of '+rows.length+' rows';
    }
    input.addEventListener('input',apply);
    apply();
  });
})();
"""


def esc(text):
    return html.escape(str(text), quote=True)


def source_link(key, label=None):
    pub, title, url = ds.SOURCES[key]
    text = label or pub
    return (f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer" '
            f'title="{esc(title)}">{esc(text)}</a>')


def status_pill(status):
    label, cls = STATUS_LABEL[status]
    return f'<span class="pill {cls}">{label}</span>'


def layout(slug, title, body, description):
    nav = []
    for href, num, name, blurb in PAGES:
        cur = ' aria-current="page"' if href == slug else ""
        nav.append(f'<a href="{href}"{cur}><span class="n">{num}</span><span>{name}</span></a>')
    nav = "\n        ".join(nav)
    page_name = next((p[2] for p in PAGES if p[0] == slug), "Overview")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{esc(description)}">
<meta name="robots" content="index,follow">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{esc(title)}</title>
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<div class="shell">
  <aside class="sidebar" id="nav" aria-label="Section navigation">
    <a class="brand" href="index.html">
      <span class="mark" aria-hidden="true">JB</span>
      <span><b>NNN decision brief</b><span>Central Los Angeles · public data</span></span>
    </a>
    <p class="navlabel">Dashboard</p>
    <nav>
        {nav}
    </nav>
    <p class="note"><b>Privacy first.</b> No owner name, street address, parcel number, lease document or
    personal financial detail is published. Those fields are marked <em>withheld</em>.</p>
  </aside>
  <div class="main">
    <div class="topbar">
      <div style="display:flex;gap:12px;align-items:center">
        <button class="navtoggle" type="button" data-nav aria-expanded="false" aria-controls="nav">☰ Sections</button>
        <span class="crumb">Decision brief <span aria-hidden="true">/</span> <b>{page_name}</b></span>
      </div>
      <span class="snap">Evidence cut-off 7 November 2026</span>
    </div>
    <main id="content">
{body}
    </main>
    <footer>
      Public-data decision brief. Every figure is linked to the official page it was read from; anything that
      could not be confirmed is blank and listed on <a href="flagged.html">Flagged for review</a>.
      Not an appraisal, not tax advice, and not a personal financial recommendation.
    </footer>
  </div>
</div>
<script>{JS}</script>
</body>
</html>
"""


# --------------------------------------------------------------------------- table builders
def data_table(rows, table_id, caption, show_category=False, search=True):
    head = ["Ref", "Metric", "Value", "Unit", "Period", "Geography"]
    if show_category:
        head.append("Category")
    head += ["Status", "Official source", "Note"]
    th = "".join(f'<th scope="col">{h}</th>' for h in head)

    trs = []
    for r in rows:
        rid, cat, metric, value, unit, period, geo, src, status, note = r
        if status in ("verified", "derived"):
            value_cell = f'<span class="num">{esc(value)}</span>'
        elif status == "withheld":
            value_cell = f'<span class="blank">{esc(value)}</span>'
        else:
            value_cell = '<span class="blank" title="Not confirmed from an official source">—</span>'
        cat_cell = f'<td class="small">{esc(dict((c[0], c[1]) for c in ds.CATEGORIES).get(cat, cat))}</td>' if show_category else ""
        trs.append(
            f'<tr id="{esc(rid.lower())}"><td class="id">{esc(rid)}</td>'
            f'<td>{esc(metric)}</td>'
            f'<td class="num">{value_cell}</td>'
            f'<td class="small">{esc(unit)}</td>'
            f'<td class="small">{esc(period)}</td>'
            f'<td class="small">{esc(geo)}</td>'
            f'{cat_cell}'
            f'<td>{status_pill(status)}</td>'
            f'<td class="src">{source_link(src)}</td>'
            f'<td class="note">{esc(note)}</td></tr>'
        )
    search_html = (f'<div class="search"><label class="small" for="{table_id}-q">Filter rows</label>'
                   f'<input id="{table_id}-q" type="search" placeholder="Type a metric, geography or status…" '
                   f'data-filter="{table_id}" aria-controls="{table_id}">'
                   f'<span class="count" data-count-for="{table_id}"></span></div>') if search else ""
    return f"""{search_html}
<div class="tablewrap">
<table id="{table_id}">
<caption>{caption}</caption>
<thead><tr>{th}</tr></thead>
<tbody>
{chr(10).join(trs)}
</tbody>
</table>
</div>"""


def rows_for(*categories):
    return [r for r in ds.ROWS if r[1] in categories]


def counts():
    out = {k: 0 for k in STATUS_LABEL}
    for r in ds.ROWS:
        out[r[8]] = out.get(r[8], 0) + 1
    return out
