#!/usr/bin/env python3
"""Build the complete static site from data/*.json.

Every table on every page is rendered from the JSON data files. Nothing is
hand-written into the HTML except prose that is itself stored in the data files
or in docs/*.md. Run this after any edit to data/*.json:

    python3 tools/model.py        # regenerate data/projection_output.json
    python3 tools/collect_sources.py   # regenerate data/sources.json
    python3 tools/build_site.py   # render every page
    python3 tools/check_links.py  # verify links, sources and privacy

Output is plain static HTML with inline CSS and no external assets, no
JavaScript dependencies and no network calls, so it renders identically on
GitHub Pages and in an offline sandbox preview.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
DOCS = os.path.join(ROOT, "docs")

RETRIEVED = "2026-11-06"
SITE_TITLE = "Central LA Jack in the Box NNN Asset"
SITE_SUB = "Sell-before-expiry vs. renew-and-hold &mdash; an evidence-only decision file"

NAV = [
    ("Overview", [
        ("index.html", "Landing Page"),
        ("executive-summary.html", "Executive Summary"),
        ("methodology.html", "Methodology & Privacy"),
        ("repo-audit.html", "Repo Audit & Irregularities"),
    ]),
    ("The Asset & The Tenant", [
        ("asset.html", "Property & Lease"),
        ("tenant.html", "Tenant Health (JACK)"),
    ]),
    ("Area Analysis", [
        ("demographics.html", "Population & Demographics"),
        ("income.html", "Income & Consumer Spending"),
        ("employment.html", "Employment & Job Growth"),
        ("schools.html", "Schools & Education"),
        ("geography.html", "Geography, Access & Transit"),
    ]),
    ("Value & Risk", [
        ("valuation.html", "Valuation & Capital Markets"),
        ("hazards.html", "Hazards & Black Swans"),
        ("regulatory.html", "Tax & Regulatory"),
        ("risks.html", "Risk Register"),
    ]),
    ("The Decision", [
        ("decisions.html", "Options & Recommendation"),
        ("projection.html", "Projection System"),
    ]),
    ("Verification", [
        ("sources.html", "Sources & Verification"),
        ("flagged.html", "Flagged for Review"),
    ]),
]
NAV_FLAT = [(h, t) for _, items in NAV for h, t in items]

CSS = """
:root{
  --bg:#f6f7f9; --panel:#ffffff; --ink:#12161c; --ink2:#4a5563; --ink3:#77828f;
  --line:#dfe3e8; --line2:#eceff3; --accent:#0b5cad; --accent2:#e8f1fb;
  --ok:#0f6b3d; --okbg:#e6f4ec; --warn:#8a5a00; --warnbg:#fdf3dc;
  --bad:#9b1c1c; --badbg:#fbeaea; --info:#3b3f8f; --infobg:#ecebfa;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
  font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1240px;margin:0 auto;padding:0 20px}
header.site{background:#0d1520;color:#fff;border-bottom:3px solid var(--accent)}
header.site .wrap{display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between;padding-top:16px;padding-bottom:16px}
header.site h1{font-size:19px;margin:0;letter-spacing:-.2px;font-weight:650}
header.site .sub{font-size:12.5px;color:#a9b6c6;margin-top:3px}
.badge-date{font-family:var(--mono);font-size:11.5px;background:#1b2735;border:1px solid #2c3b4d;
  color:#cfe0f2;padding:5px 9px;border-radius:6px;white-space:nowrap}
nav.main{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20}
nav.main .wrap{display:flex;flex-wrap:wrap;gap:2px 4px;padding-top:6px;padding-bottom:6px}
nav.main a{font-size:12.8px;color:var(--ink2);padding:6px 9px;border-radius:6px;white-space:nowrap}
nav.main a:hover{background:var(--line2);text-decoration:none}
nav.main a.on{background:var(--accent2);color:var(--accent);font-weight:650}
main{padding:26px 0 60px}
h2.pg{font-size:27px;margin:0 0 6px;letter-spacing:-.5px;line-height:1.25}
p.lede{color:var(--ink2);font-size:15.5px;margin:0 0 20px;max-width:900px}
h3{font-size:19px;margin:34px 0 10px;letter-spacing:-.2px}
h4{font-size:15.5px;margin:22px 0 8px;color:var(--ink)}
p{margin:0 0 12px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin:0 0 18px}
.card.tight{padding:14px 16px}
.grid{display:grid;gap:14px}
.g2{grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}
.g3{grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}
.g4{grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.kpi .k{font-size:11.5px;text-transform:uppercase;letter-spacing:.6px;color:var(--ink3);font-weight:650}
.kpi .v{font-size:24px;font-weight:680;letter-spacing:-.6px;margin:5px 0 2px;font-variant-numeric:tabular-nums}
.kpi .m{font-size:12.3px;color:var(--ink2);line-height:1.45}
.kpi .m a{font-size:12.3px}
table{width:100%;border-collapse:collapse;background:var(--panel);font-size:13.6px}
caption{caption-side:top;text-align:left;font-size:13px;color:var(--ink2);padding:0 0 8px}
th,td{text-align:left;padding:9px 11px;border-bottom:1px solid var(--line2);vertical-align:top}
thead th{background:#f0f3f6;border-bottom:1px solid var(--line);font-size:11.6px;
  text-transform:uppercase;letter-spacing:.5px;color:var(--ink2);font-weight:700;position:sticky;top:41px;z-index:5}
tbody tr:hover{background:#fafbfc}
td.id{font-family:var(--mono);font-size:12px;color:var(--ink3);white-space:nowrap}
td.metric{min-width:210px;font-weight:560}
td.val{font-variant-numeric:tabular-nums;min-width:150px}
td.val.blank{color:var(--ink3);font-style:italic}
td.note{color:var(--ink2);font-size:12.8px;min-width:230px}
td.src{font-size:12.4px;min-width:170px}
td.per{font-size:12.4px;color:var(--ink2);min-width:130px}
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--panel)}
.scroll table{border:0}
.pill{display:inline-block;font-size:10.6px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;
  padding:2.5px 7px;border-radius:20px;white-space:nowrap;border:1px solid transparent}
.p-ok{background:var(--okbg);color:var(--ok);border-color:#bfe3cd}
.p-no{background:var(--warnbg);color:var(--warn);border-color:#f0dfb4}
.p-blank{background:var(--badbg);color:var(--bad);border-color:#f0cccc}
.p-info{background:var(--infobg);color:var(--info);border-color:#d3d1f0}
.p-grey{background:#eef1f4;color:var(--ink2);border-color:#dde2e8}
.callout{border-left:4px solid var(--accent);background:var(--accent2);padding:13px 16px;border-radius:0 8px 8px 0;margin:0 0 18px;font-size:14.2px}
.callout.warn{border-left-color:#c98a00;background:var(--warnbg)}
.callout.bad{border-left-color:#b42318;background:var(--badbg)}
.callout.ok{border-left-color:#12854a;background:var(--okbg)}
.callout strong{font-weight:700}
.callout p:last-child{margin-bottom:0}
.small{font-size:12.6px;color:var(--ink2)}
.mono{font-family:var(--mono);font-size:12.6px}
ul.clean,ol.clean{margin:0 0 14px;padding-left:22px}
ul.clean li,ol.clean li{margin-bottom:7px}
.opt{border:1px solid var(--line);border-radius:10px;background:var(--panel);padding:16px 18px;margin-bottom:14px}
.opt h4{margin:0 0 4px;font-size:16.5px}
.opt .tag{font-family:var(--mono);font-size:11.5px;color:var(--ink3)}
.twocol{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:800px){.twocol{grid-template-columns:1fr}thead th{position:static}}
.pros h5,.cons h5{font-size:12px;text-transform:uppercase;letter-spacing:.6px;margin:0 0 7px}
.pros h5{color:var(--ok)}.cons h5{color:var(--bad)}
.pros ul,.cons ul{margin:0;padding-left:19px;font-size:13.3px}
.pros li,.cons li{margin-bottom:6px}
.rec{border:2px solid var(--accent);border-radius:12px;background:#fff;padding:20px 22px;margin-bottom:20px}
.rec h3{margin-top:0}
.step{display:flex;gap:14px;margin-bottom:14px}
.step .n{flex:0 0 30px;height:30px;border-radius:50%;background:var(--accent);color:#fff;
  display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px}
.step .b{flex:1}
.step .w{font-family:var(--mono);font-size:11.5px;color:var(--ink3);text-transform:uppercase;letter-spacing:.5px}
.scorebar{display:inline-block;height:9px;border-radius:5px;background:var(--line);min-width:74px;position:relative;vertical-align:middle}
.scorebar i{position:absolute;left:0;top:0;bottom:0;border-radius:5px;display:block}
.s-lo{background:#2e9e5b}.s-mo{background:#7bb662}.s-el{background:#e0a800}.s-hi{background:#e07000}.s-se{background:#c0261c}
footer.site{border-top:1px solid var(--line);background:#fff;padding:22px 0 34px;margin-top:20px}
footer.site .wrap{font-size:12.6px;color:var(--ink2)}
.pager{display:flex;justify-content:space-between;gap:12px;margin-top:26px;flex-wrap:wrap}
.pager a{border:1px solid var(--line);background:#fff;border-radius:8px;padding:9px 13px;font-size:13.4px}
.pager a:hover{border-color:var(--accent);text-decoration:none}
.toc{columns:2;column-gap:26px;font-size:13.6px}
@media(max-width:700px){.toc{columns:1}}
.toc a{display:block;padding:3px 0}
.bar{height:22px;border-radius:4px;background:var(--line2);overflow:hidden;display:flex;font-size:11px;line-height:22px;color:#fff;font-weight:700}
.bar i{display:block;text-align:center;font-style:normal;white-space:nowrap;overflow:hidden}
.legend{font-size:12.3px;color:var(--ink2);margin-top:6px}
.legend span{display:inline-block;margin-right:14px}
.sw{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:middle}
code{font-family:var(--mono);font-size:12.6px;background:#f0f3f6;padding:1.5px 5px;border-radius:4px}
pre{background:#0d1520;color:#dce6f2;padding:14px 16px;border-radius:8px;overflow-x:auto;font-family:var(--mono);font-size:12.6px;line-height:1.55}
@media print{nav.main,header.site,.pager{display:none}body{background:#fff}.card,.scroll{border-color:#bbb}}
"""


# --------------------------------------------------------------------- helpers
def esc(s):
    if s is None:
        return ""
    return html.escape(str(s), quote=True)


def load(name):
    path = os.path.join(DATA, name)
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load_doc(name):
    path = os.path.join(DOCS, name)
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ------------------------------------------------------------- tiny markdown
def md_inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
               r'<a href="\2" rel="noopener noreferrer external">\1</a>', s)
    s = re.sub(r"(?<!\()(https?://[^\s<)\"]+)",
               r'<a href="\1" rel="noopener noreferrer external">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def md_to_html(text):
    out, lines, i = [], text.split("\n"), 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("```"):
            buf, i = [], i + 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            out.append("<pre>" + esc("\n".join(buf)) + "</pre>")
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            lvl = len(m.group(1))
            tag = {1: "h2", 2: "h3", 3: "h4"}.get(lvl, "h4")
            out.append("<%s class='pg' id='%s'>%s</%s>" % (
                tag, re.sub(r"[^a-z0-9]+", "-", m.group(2).lower()).strip("-"),
                md_inline(m.group(2)), tag) if tag == "h2" else
                "<%s>%s</%s>" % (tag, md_inline(m.group(2)), tag))
            i += 1
            continue
        if ln.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:\-|]+\|\s*$", lines[i + 1]):
            head = [c.strip() for c in ln.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            t = ['<div class="scroll"><table><thead><tr>']
            t += ["<th>%s</th>" % md_inline(h) for h in head]
            t.append("</tr></thead><tbody>")
            for rr in rows:
                t.append("<tr>" + "".join("<td>%s</td>" % md_inline(c) for c in rr) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue
        if re.match(r"^\s*[-*]\s+", ln):
            buf = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                buf.append("<li>%s</li>" % md_inline(re.sub(r"^\s*[-*]\s+", "", lines[i].rstrip())))
                i += 1
            out.append('<ul class="clean">' + "".join(buf) + "</ul>")
            continue
        if re.match(r"^\s*\d+[.)]\s+", ln):
            buf = []
            while i < len(lines) and re.match(r"^\s*\d+[.)]\s+", lines[i]):
                buf.append("<li>%s</li>" % md_inline(re.sub(r"^\s*\d+[.)]\s+", "", lines[i].rstrip())))
                i += 1
            out.append('<ol class="clean">' + "".join(buf) + "</ol>")
            continue
        if ln.strip() in ("---", "***", "___"):
            out.append("<hr>")
            i += 1
            continue
        if ln.lstrip().startswith("> "):
            buf = []
            while i < len(lines) and lines[i].lstrip().startswith("> "):
                buf.append(md_inline(lines[i].lstrip()[2:]))
                i += 1
            out.append('<div class="callout"><p>' + "<br>".join(buf) + "</p></div>")
            continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^\s*(#{1,6}\s|[-*]\s|\d+[.)]\s|\||```|> |---$)", lines[i]):
            buf.append(lines[i].rstrip())
            i += 1
        out.append("<p>%s</p>" % md_inline(" ".join(buf)))
    return "\n".join(out)


# ------------------------------------------------------------------- chrome
def nav_html(active):
    out = ['<nav class="main"><div class="wrap">']
    for _, items in NAV:
        for href, label in items:
            cls = ' class="on"' if href == active else ""
            out.append('<a href="%s"%s>%s</a>' % (href, cls, esc(label)))
    out.append("</div></nav>")
    return "".join(out)


def pager(active):
    idx = [h for h, _ in NAV_FLAT].index(active)
    hrefs = [h for h, _ in NAV_FLAT]
    labels = [t for _, t in NAV_FLAT]
    out = ['<div class="pager">']
    out.append('<a href="%s">&larr; %s</a>' % (hrefs[idx - 1], esc(labels[idx - 1]))
               if idx > 0 else "<span></span>")
    out.append('<a href="%s">%s &rarr;</a>' % (hrefs[idx + 1], esc(labels[idx + 1]))
               if idx < len(hrefs) - 1 else "<span></span>")
    out.append("</div>")
    return "".join(out)


def page(active, title, lede, body, extra_head=""):
    """Token-replacement rather than %-formatting: the inline CSS contains literal
    percent signs, which would break a format string."""
    tpl = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@ &middot; @@SITE@@</title>
<meta name="description" content="@@DESC@@">
<meta name="robots" content="noindex, nofollow">
<style>@@CSS@@</style>
@@EXTRA@@</head>
<body>
<header class="site"><div class="wrap">
<div><h1>@@SITE@@</h1><div class="sub">@@SUB@@</div></div>
<div class="badge-date">Data retrieved @@RETRIEVED@@</div>
</div></header>
@@NAV@@
<main class="wrap">
<h2 class="pg">@@H2@@</h2>
<p class="lede">@@LEDE@@</p>
@@BODY@@
@@PAGER@@
</main>
<footer class="site"><div class="wrap">
<p><strong>Verification standard.</strong> Every table row on this site carries a link to an
official publisher &mdash; a government agency, a regulator, a central bank, a regional planning
agency, or a document filed with the U.S. Securities and Exchange Commission. Where a value
could not be confirmed from an official source, the value cell is left <em>blank</em>, the row is
marked <span class="pill p-no">Unverified</span>, and the reason is registered on the
<a href="flagged.html">Flagged for Review</a> page. No value on this site is inferred,
estimated from memory, or taken from a news article, brokerage, aggregator or wiki.</p>
<p><strong>Privacy.</strong> The subject property is deliberately anonymised. Its address, parcel
number, owner identity, purchase price, rent, net operating income and insurance details are
withheld and are not published anywhere on this site, including in the underlying data files.
Every parcel-specific and owner-specific field is therefore blank by design and flagged as such.</p>
<p><strong>Not advice.</strong> This is an analytical research file, not legal advice, tax advice,
an appraisal, or a securities recommendation. Sources retrieved @@RETRIEVED@@.
<a href="methodology.html">Methodology</a> &middot; <a href="sources.html">Sources</a> &middot;
<a href="flagged.html">Flagged for Review</a> &middot;
<a href="https://github.com/wingbangboozle1-lang/Jack1" rel="noopener noreferrer">Repository</a></p>
</div></footer>
</body>
</html>
"""
    subs = {
        "@@TITLE@@": esc(title),
        "@@SITE@@": SITE_TITLE,
        "@@SUB@@": SITE_SUB,
        "@@DESC@@": esc(re.sub(r"<[^>]+>", "", lede))[:300],
        "@@CSS@@": CSS,
        "@@EXTRA@@": extra_head,
        "@@RETRIEVED@@": RETRIEVED,
        "@@NAV@@": nav_html(active),
        "@@H2@@": title,
        "@@LEDE@@": lede,
        "@@BODY@@": body,
        "@@PAGER@@": pager(active),
    }
    for k, v in subs.items():
        tpl = tpl.replace(k, v)
    path = os.path.join(ROOT, active)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(tpl)
    return path


# ---------------------------------------------------------------- row tables
def status_pill(row):
    if row.get("k"):
        return '<span class="pill p-ok">Verified</span>'
    if row.get("v") in ("", None):
        return '<span class="pill p-blank">Blank &middot; unverified</span>'
    return '<span class="pill p-no">Unverified</span>'


def src_cell(row):
    u = (row.get("u") or "").strip()
    s = esc(row.get("s") or "")
    if not u:
        return '<td class="src">%s<br><span class="pill p-grey">No official publisher</span></td>' % (s or "&mdash;")
    return ('<td class="src">%s<br><a href="%s" rel="noopener noreferrer external">Open official source &#8599;</a></td>'
            % (s, esc(u)))


def value_cell(row):
    v = row.get("v")
    if v in ("", None):
        return '<td class="val blank">left blank</td>'
    return "<td class='val'>%s</td>" % md_inline(str(v))


def row_table(rows, caption=None, show_period=True, show_reported=True):
    head = ["ID", "Metric", "Value", "Status"]
    if show_period:
        head.append("Period / vintage")
    if show_reported:
        head.append("Official source &amp; link")
    else:
        head.append("Official source &amp; link")
    head.append("Note, derivation or reason for the gap")
    t = ['<div class="scroll"><table>']
    if caption:
        t.append("<caption>%s</caption>" % caption)
    t.append("<thead><tr>" + "".join("<th>%s</th>" % h for h in head) + "</tr></thead><tbody>")
    for row in rows:
        note = esc(row.get("n") or "")
        rep = row.get("r")
        if rep:
            if str(rep).startswith("[ENGAGEMENT BRIEF]"):
                label = "Engagement premise &mdash; not an official source, not used as a value"
                body = esc(str(rep)[len("[ENGAGEMENT BRIEF]"):].strip())
            else:
                label = "Reported by a non-official source &mdash; NOT used"
                body = esc(rep)
            note = ('<span class="pill p-info">%s</span><br><span class="small">%s</span>'
                    % (label, body)) + ("<br>" + note if note else "")
        cells = ['<td class="id">%s</td>' % esc(row.get("id")),
                 '<td class="metric">%s</td>' % md_inline(row.get("m") or ""),
                 value_cell(row),
                 "<td>%s</td>" % status_pill(row)]
        if show_period:
            cells.append('<td class="per">%s</td>' % esc(row.get("p") or ""))
        cells.append(src_cell(row))
        cells.append('<td class="note">%s</td>' % (md_inline(note) if note else "&mdash;"))
        t.append("<tr>" + "".join(cells) + "</tr>")
    t.append("</tbody></table></div>")
    return "".join(t)


def coverage_bar(doc_rows):
    tot = len(doc_rows)
    if not tot:
        return ""
    ver = sum(1 for r in doc_rows if r.get("k"))
    blank = sum(1 for r in doc_rows if not r.get("k") and r.get("v") in ("", None))
    other = tot - ver - blank
    pw, po, pb = ver * 100.0 / tot, other * 100.0 / tot, blank * 100.0 / tot
    return ('<div class="card tight"><div class="bar">'
            '<i style="width:%.2f%%;background:#12854a">%s</i>'
            '<i style="width:%.2f%%;background:#c98a00">%s</i>'
            '<i style="width:%.2f%%;background:#b42318">%s</i>'
            '</div><div class="legend">'
            '<span><span class="sw" style="background:#12854a"></span>Verified from an official source: %d of %d (%.1f%%)</span>'
            '<span><span class="sw" style="background:#c98a00"></span>Value seen only in a non-official source, withheld: %d</span>'
            '<span><span class="sw" style="background:#b42318"></span>Left blank and flagged: %d</span>'
            '</div></div>' % (pw, ("%.0f%%" % pw if pw >= 9 else ""),
                              po, ("%.0f%%" % po if po >= 9 else ""),
                              pb, ("%.0f%%" % pb if pb >= 9 else ""),
                              ver, tot, ver * 100.0 / tot, other, blank))


def data_page(active, title, lede, fname, intro_html="", outro_html=""):
    doc = load(fname)
    rows = doc["rows"]
    meta = doc.get("meta", {})
    body = [coverage_bar(rows)]
    if intro_html:
        body.append(intro_html)
    for k in ("note", "integrity_note", "source_page", "schema_note", "relevance_note",
              "calibration_note", "why_it_matters", "issuer", "filing_basis", "next_event"):
        if meta.get(k):
            body.append('<div class="callout"><strong>%s.</strong> %s</div>'
                        % (esc(k.replace("_", " ").capitalize()), md_inline(meta[k])))
    body.append("<h3>Every row, with its official source</h3>")
    body.append(row_table(rows))
    if outro_html:
        body.append(outro_html)
    return page(active, title, lede, "\n".join(body))


def write(name, content):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as fh:
        fh.write(content)


# =========================================================================
def build():
    made = []

    asset = load("asset.json")
    demo = load("demographics.json")
    inc = load("income.json")
    emp = load("employment.json")
    sch = load("schools.json")
    geo = load("geography.json")
    val = load("valuation.json")
    haz = load("hazards.json")
    reg = load("regulatory.json")
    ten = load("tenant.json")
    rsk = load("risks.json")
    dec = load("decisions.json")
    prj = load("projection.json")
    pro = load("projection_output.json")
    flg = load("flags.json")
    src = load("sources.json")

    all_rows = ([("asset", r) for r in asset["rows"]] + [("demographics", r) for r in demo["rows"]]
                + [("income", r) for r in inc["rows"]] + [("employment", r) for r in emp["rows"]]
                + [("schools", r) for r in sch["rows"]] + [("geography", r) for r in geo["rows"]]
                + [("valuation", r) for r in val["rows"]] + [("hazards", r) for r in haz["rows"]]
                + [("regulatory", r) for r in reg["rows"]] + [("tenant", r) for r in ten["rows"]])
    tot = len(all_rows)
    ver = sum(1 for _, r in all_rows if r.get("k"))
    blank = sum(1 for _, r in all_rows if not r.get("k") and r.get("v") in ("", None))
    st = src["meta"]["stats"]

    # ------------------------------------------------------------ index.html
    def find(rows, rid):
        for r in rows:
            if r["id"] == rid:
                return r
        return {}

    def kv(label, row, extra=""):
        v = row.get("v")
        disp = ("<span class='pill p-blank'>blank</span>" if v in ("", None)
                else md_inline(str(v)))
        u = row.get("u")
        link = (' &middot; <a href="%s" rel="noopener noreferrer external">source</a>' % esc(u)) if u else ""
        return ('<div class="kpi"><div class="k">%s</div><div class="v">%s</div>'
                '<div class="m">%s%s%s</div></div>'
                % (esc(label), disp, esc(row.get("p") or ""), extra, link))

    idx = []
    idx.append('<div class="rec"><h3>The decision, in one paragraph</h3><p>%s</p>'
               '<p class="small">%s</p></div>'
               % (md_inline(dec["recommendation"]["headline"]),
                  md_inline(dec["recommendation"]["rationale"])))

    idx.append("<h3>Verification coverage of this file</h3>")
    idx.append('<div class="grid g4">'
               + kv("Table rows published", {"v": "%d" % tot, "p": "across 10 data categories"}, "")
               + kv("Rows verified from an official source", {"v": "%d (%.1f%%)" % (ver, ver * 100.0 / tot), "p": "each carries an official link"}, "")
               + kv("Rows left blank and flagged", {"v": "%d" % blank, "p": "no official confirmation obtained"}, "")
               + kv("Open flags", {"v": "%d" % len(flg["flags"]), "p": "plus %d irregularities" % len(flg["irregularities"])}, "")
               + "</div>")
    idx.append('<p class="small">Distinct official URLs cited: %d across %d publishers. '
               'See <a href="sources.html">Sources &amp; Verification</a>.</p>'
               % (st["rows_total"] and sum(p["url_count"] for p in src["publishers"]),
                  len(src["publishers"])))

    idx.append("<h3>What the official data says</h3>")
    idx.append('<div class="grid g3">'
               + kv("LA city population", find(demo["rows"], "D-03"))
               + kv("LA County population change", find(demo["rows"], "D-06"))
               + kv("LA County population, 2025", find(demo["rows"], "D-12"))
               + kv("LA city households, 2035 (SCAG)", find(demo["rows"], "D-33"))
               + kv("Median household income, city", find(inc["rows"], "I-01"))
               + kv("LA CPI-U, 12 months", find(inc["rows"], "I-11"))
               + kv("MSA nonfarm employment change", find(emp["rows"], "E-11"))
               + kv("MSA unemployment rate", find(emp["rows"], "E-04"))
               + kv("Leisure &amp; Hospitality change", find(emp["rows"], "E-13"))
               + kv("Information sector change", find(emp["rows"], "E-20"))
               + kv("LAUSD enrolment 2025-26", find(sch["rows"], "S-01"))
               + kv("LAUSD 5-year graduation rate", find(sch["rows"], "S-06"))
               + kv("County assessment roll 2026", find(val["rows"], "V-18"))
               + kv("Roll growth", find(val["rows"], "V-19"))
               + kv("FHFA LA house price index, YoY", find(val["rows"], "V-13"))
               + kv("10-year Treasury par yield", find(val["rows"], "V-01"))
               + kv("JIB system restaurants", find(ten["rows"], "T-01"))
               + kv("JIB system same-store sales", find(ten["rows"], "T-03"))
               + kv("JIB franchise AUV", find(ten["rows"], "T-26"))
               + kv("Measure ULA rate", find(reg["rows"], "R-10"))
               + kv("LA City minimum wage", find(reg["rows"], "R-16"))
               + kv("M6.7+ earthquake, 30-year", find(haz["rows"], "H-01"))
               + kv("Jan 2025 fires, output lost", find(haz["rows"], "H-19"))
               + kv("Metro D Line Section 1", find(geo["rows"], "G-06"))
               + "</div>")

    idx.append("<h3>The four findings that drive the recommendation</h3>")
    order = ["FND-1", "FND-3", "FND-10", "FND-5"]
    for fid in order:
        f = next(x for x in dec["findings"] if x["id"] == fid)
        idx.append('<div class="card"><h4>%s &mdash; %s</h4><p>%s</p>'
                   '<p class="small mono">Evidence rows: %s</p></div>'
                   % (esc(f["id"]), md_inline(f["headline"]), md_inline(f["detail"]),
                      esc(", ".join(f["sources"]))))

    idx.append("<h3>Contents</h3><div class='card'><div class='toc'>")
    for group, items in NAV:
        idx.append('<h4 style="margin-top:14px">%s</h4>' % esc(group))
        for href, label in items:
            idx.append('<a href="%s">%s</a>' % (href, esc(label)))
    idx.append("</div></div>")

    idx.append('<div class="callout warn"><strong>Read this first.</strong> %s</div>'
               % md_inline(flg["meta"]["policy"]))

    made.append(page("index.html", "Landing Page",
                     "A single-tenant Jack in the Box freehold in the central Los Angeles trade "
                     "area, leased NNN, with the lease expiring somewhere in the 2030&ndash;2035 "
                     "window. This file answers one question &mdash; sell before expiry, or renew "
                     "and hold &mdash; using only official sources, and states plainly where the "
                     "official record runs out.",
                     "\n".join(idx)))

    # ------------------------------------------------- executive-summary.html
    made.append(page("executive-summary.html", "Executive Summary",
                     "The important details, the decision, and the conditions under which the "
                     "decision is wrong.",
                     md_to_html(load_doc("executive-summary.md"))))

    # ------------------------------------------------------ methodology.html
    meth = []
    meth.append(md_to_html(load_doc("methodology.md")))
    meth.append("<h3>Row schema used in every data file</h3>")
    meth.append('<div class="scroll"><table><thead><tr><th>Key</th><th>Meaning</th>'
                '<th>Rule</th></tr></thead><tbody>')
    for k, meaning, rule in [
        ("id", "Row identifier, prefixed by category (A-, D-, I-, E-, S-, G-, V-, H-, R-, T-, RK-, IN-, UX-, F-, IR-)", "Stable. Referenced from other pages."),
        ("m", "Metric name, with its geography stated explicitly", "Geography is never implied. City, county, metropolitan area and metropolitan division are distinct and are labelled as such."),
        ("v", "Verified value", "Empty string means the value is left blank. A blank is never filled by inference."),
        ("p", "Period or vintage of the value", "Mandatory. A number without a vintage is not published."),
        ("s", "Official publisher, named in full", "Must be a government agency, regulator, central bank, regional planning agency, or an SEC filing."),
        ("u", "Official URL for manual review", "Mandatory for every verified row. The build fails if a verified row has no URL."),
        ("k", "Verified true / false", "true only if the value was read from the official publisher during this session."),
        ("n", "Note, derivation, or the reason for the gap", "Also carries the flag identifier where one applies."),
        ("r", "Value reported by a NON-official source", "Never used as a verified value and never used as a model input. Shown only so a reader can see what was declined and why."),
    ]:
        meth.append("<tr><td class='id'>%s</td><td>%s</td><td class='note'>%s</td></tr>"
                    % (esc(k), esc(meaning), esc(rule)))
    meth.append("</tbody></table></div>")

    meth.append("<h3>How the projection system stays reproducible</h3>")
    meth.append("<pre>%s</pre>" % esc(
        "python3 tools/model.py            # reads data/projection.json, writes data/projection_output.json\n"
        "python3 tools/collect_sources.py  # scans every row, writes data/sources.json\n"
        "python3 tools/build_site.py       # renders all 19 pages from data/*.json\n"
        "python3 tools/check_links.py      # fails the build on a missing link, an\n"
        "                                  # unsourced verified row, or a privacy leak"))
    meth.append("<p class='small'>Every number on the Projection page is computed at build time "
                "from the declared inputs. Nothing is hand-entered into a rendered table, so the "
                "published figures cannot drift from the specification.</p>")

    meth.append("<h3>Classes of source deliberately excluded</h3><ul class='clean'>")
    for c in flg["excluded_sources"]["classes"]:
        meth.append("<li>%s</li>" % esc(c))
    meth.append("</ul>")
    meth.append('<p class="small">%s</p>' % md_inline(flg["excluded_sources"]["note"]))

    made.append(page("methodology.html", "Methodology, Verification Standard & Privacy Protocol",
                     "How every row was sourced, what was declined, what was left blank, and why "
                     "the subject property is anonymised.",
                     "\n".join(meth)))

    # ------------------------------------------------------- repo-audit.html
    ra = [md_to_html(load_doc("repo-audit.md"))]
    ra.append("<h3>Irregularities found in the official record</h3>")
    ra.append('<p class="lede">An irregularity is not a mistake in this analysis. It is a '
              'contradiction, discontinuity or silent gap in the official sources themselves, '
              'recorded so that a reader relying on them later is not misled.</p>')
    ra.append('<div class="scroll"><table><thead><tr><th>ID</th><th>Irregularity</th>'
              '<th>What the official record shows</th><th>Official source</th>'
              '<th>Impact on this analysis</th><th>Rows</th></tr></thead><tbody>')
    for ir in flg["irregularities"]:
        ra.append('<tr><td class="id">%s</td><td class="metric">%s</td>'
                  '<td class="note">%s</td>'
                  '<td class="src"><a href="%s" rel="noopener noreferrer external">%s &#8599;</a></td>'
                  '<td class="note">%s</td><td class="id">%s</td></tr>'
                  % (esc(ir["id"]), md_inline(ir["title"]), md_inline(ir["detail"]),
                     esc(ir["u"]), esc(ir["s"]), md_inline(ir["impact"]),
                     esc(", ".join(ir["rows"]))))
    ra.append("</tbody></table></div>")
    made.append(page("repo-audit.html", "Repository Audit, Line by Line",
                     "A line-by-line audit of the repository as received and as delivered, plus "
                     "the nine irregularities found in the official sources themselves.",
                     "\n".join(ra)))

    # ------------------------------------------------------ data-driven pages
    made.append(data_page(
        "asset.html", "The Property & The Lease", 
        "Everything that is known, and everything that is deliberately blank, about the subject "
        "asset. This page is almost entirely gaps &mdash; and those gaps are the reason the "
        "recommendation is a decision tree rather than a single instruction.",
        "asset.json",
        intro_html=('<div class="callout bad"><strong>Privacy protocol.</strong> The subject '
                    'property is anonymised. Its address, parcel number, owner identity and all '
                    'financial particulars are withheld from this site by design and are not '
                    'stored in the underlying data files either. Rows marked '
                    '<span class="pill p-blank">Blank</span> below are blank for one of two '
                    'reasons, and each row says which: either the information is withheld under '
                    'the privacy protocol, or it is parcel-specific and no official source can '
                    'supply it without the location.</div>'
                    '<div class="callout warn"><strong>The four premises of this engagement.</strong> '
                    'Four things were given in the brief and are treated as premises throughout, '
                    'not as verified facts: the asset is a single-tenant quick-service restaurant '
                    'freehold comprising ground and building, occupied by a Jack in the Box '
                    'restaurant; the lease is triple net, so the tenant reimburses property tax, '
                    'insurance and maintenance; the tenant operates under the Jack in the Box '
                    'brand; and the lease expires somewhere in the window 2030 to 2035. None of '
                    'the four is confirmable from an official source without the parcel record '
                    'and the lease, so all four appear below in the value column as blank with '
                    'the premise quarantined in a separate field. Everything else on this page '
                    'is a gap with a named official route to close it.</div>')))

    made.append(data_page(
        "tenant.html", "Tenant & Brand Health &mdash; Jack in the Box Inc.",
        "The credit behind the rent, read entirely from documents filed with the U.S. Securities "
        "and Exchange Commission. No brokerage research, press article or aggregator was used.",
        "tenant.json",
        intro_html=('<div class="callout warn"><strong>The single most important row on this '
                    'page is T-36.</strong> Jack in the Box Inc. has stated in SEC-filed '
                    'materials that the remaining underperforming locations in its closure '
                    'programme will close &ldquo;based on their respective franchise agreement '
                    'termination dates.&rdquo; A lease expiring in 2030&ndash;2035 therefore sits '
                    'inside a scheduled, publicly announced decision window &mdash; not merely a '
                    'rent-review date.</div>')))

    made.append(data_page(
        "demographics.html", "Population & Demographics",
        "Who lives in the trade area, how many of them there are, and which way the number is "
        "moving. The direction of travel matters more than the level for a decision that runs to "
        "2035.",
        "demographics.json",
        intro_html=('<div class="callout"><strong>Geography is never implied on this page.</strong> '
                    'The City of Los Angeles, Los Angeles County, the '
                    'Los Angeles&ndash;Long Beach&ndash;Anaheim metropolitan statistical area and '
                    'the Los Angeles&ndash;Long Beach&ndash;Glendale metropolitan division are four '
                    'different official geographies with four different numbers. Every row states '
                    'which one it is. The subject parcel is inside the central Los Angeles trade '
                    'area, so city and county figures are the operative ones.</div>')))

    made.append(data_page("income.html", "Income, Prices & Consumer Spending",
                          "What the trade area earns, what it pays for housing, and what "
                          "inflation is doing to both &mdash; and to the tenant&rsquo;s cost base.",
                          "income.json"))
    made.append(data_page("employment.html", "Employment, Job Growth & Industry Mix",
                          "The demand engine behind a drive-thru. Total employment is nearly "
                          "flat, but the composition is shifting in ways that matter more than "
                          "the headline.",
                          "employment.json"))
    made.append(data_page("schools.html", "Schools & Education System",
                          "School data is a proxy for households with children, for resident "
                          "retention, and for the local bond levies that a NNN tenant must "
                          "reimburse.",
                          "schools.json"))
    made.append(data_page("geography.html", "Geography, Access, Transit & Development Pipeline",
                          "A quick-service freehold is worth its drive-thru. Access, density, "
                          "transit and the development pipeline dominate value.",
                          "geography.json"))
    made.append(data_page("valuation.html", "Valuation & Capital-Markets Context",
                          "The official rate, price and assessment anchors &mdash; and an "
                          "explicit statement of what no official source can tell you.",
                          "valuation.json",
                          intro_html=('<div class="callout bad"><strong>No capitalisation rate is '
                                      'stated as a fact anywhere on this site.</strong> There is '
                                      'no official government publisher of single-tenant '
                                      'net-lease capitalisation rates; they are private market '
                                      'data sold by brokerages and research firms. Cap rate '
                                      'enters the projection model only as a labelled, flagged '
                                      'scenario spread over the official U.S. Treasury par '
                                      'yield.</div>')))
    made.append(data_page("hazards.html", "Natural-Hazard, Catastrophe & Black-Swan Exposure",
                          "Earthquake, wildfire, flood and the January 2025 fires &mdash; the "
                          "best-calibrated catastrophe this market has produced in living "
                          "memory, in the county&rsquo;s own official loss statistics.",
                          "hazards.json",
                          intro_html=('<div class="callout warn"><strong>One important exclusion.</strong> '
                                      'FEMA National Risk Index values for Los Angeles County '
                                      'circulate widely but could not be read from a fema.gov '
                                      'page in this session. They are held in the '
                                      '&ldquo;reported&rdquo; column only, are marked unverified, '
                                      'and are not used as inputs to the projection model. '
                                      'Catastrophe severity is anchored instead on the '
                                      'county&rsquo;s own official fire loss statistics and on '
                                      'USGS earthquake probabilities.</div>')))
    made.append(data_page("regulatory.html", "Tax, Regulatory, Insurance & Transaction-Cost Environment",
                          "For a decision to sell, transaction taxes and Proposition 13 "
                          "reassessment are first-order. For a decision to hold, the tax cap and "
                          "the tenant&rsquo;s NNN reimbursement obligation are first-order.",
                          "regulatory.json",
                          intro_html=('<div class="callout bad"><strong>Measure ULA is a cliff, '
                                      'not a bracket.</strong> It charges 4% or 5.5% of the '
                                      'ENTIRE consideration or value, only inside the City of '
                                      'Los Angeles, on top of county and city documentary '
                                      'transfer tax. Whether the parcel is inside the City is '
                                      'therefore a binary, order-of-magnitude swing in net sale '
                                      'proceeds &mdash; and it is currently unknown.</div>')))

    # ------------------------------------------------------------- risks.html
    rk = []
    rk.append('<div class="callout"><strong>%s</strong> %s</div>'
              % ("Scoring.", md_inline(rsk["meta"]["scoring"])))
    rk.append('<div class="callout warn"><strong>%s</strong> %s</div>'
              % ("Honesty rule.", md_inline(rsk["meta"]["honesty_rule"])))
    rk.append('<p class="small">%s</p>' % md_inline(rsk["meta"]["black_swan_definition"]))

    bands = ["Severe", "High", "Elevated", "Moderate", "Low"]
    counts = {b: sum(1 for x in rsk["risks"] if x["band"] == b) for b in bands}
    rk.append("<h3>Register summary</h3><div class='grid g4'>")
    for b in bands:
        cls = {"Severe": "s-se", "High": "s-hi", "Elevated": "s-el",
               "Moderate": "s-mo", "Low": "s-lo"}[b]
        rk.append('<div class="kpi"><div class="k">%s</div><div class="v">%d</div>'
                  '<div class="m"><span class="scorebar"><i class="%s" style="width:%d%%"></i></span>'
                  ' of %d risks</div></div>'
                  % (b, counts[b], cls, int(counts[b] * 100 / max(1, len(rsk["risks"]))),
                     len(rsk["risks"])))
    rk.append("</div>")
    bs = [x for x in rsk["risks"] if x.get("black_swan")]
    rk.append('<div class="callout bad"><strong>Black-swan rows.</strong> %d of %d risks are '
              'flagged as black swans: %s. Each is a low-probability event whose damage is '
              'disproportionate to the asset&rsquo;s income and is not diversifiable inside a '
              'single-asset, single-tenant position.</div>'
              % (len(bs), len(rsk["risks"]), esc(", ".join(x["id"] for x in bs))))

    rk.append("<h3>Official anchors behind the likelihood scores</h3>")
    rk.append('<div class="scroll"><table><thead><tr><th>ID</th><th>Official anchor</th>'
              '<th>What it is restated as</th><th>Official source</th></tr></thead><tbody>')
    for a in rsk["official_anchors"]:
        rk.append('<tr><td class="id">%s</td><td class="metric">%s</td><td class="note">%s</td>'
                  '<td class="src"><a href="%s" rel="noopener noreferrer external">%s &#8599;</a></td></tr>'
                  % (esc(a["id"]), md_inline(a["anchor"]), md_inline(a["derived"]),
                     esc(a["u"]), esc(a["s"])))
    rk.append("</tbody></table></div>")

    rk.append("<h3>The full register</h3>")
    rk.append('<div class="scroll"><table><thead><tr><th>ID</th><th>Decision path</th>'
              '<th>Risk</th><th>Category</th><th>L</th><th>I</th><th>Score</th><th>Band</th>'
              '<th>Evidentiary basis</th><th>Mitigant</th><th>Rows</th></tr></thead><tbody>')
    for x in sorted(rsk["risks"], key=lambda z: (-z["score"], z["id"])):
        cls = {"Severe": "s-se", "High": "s-hi", "Elevated": "s-el",
               "Moderate": "s-mo", "Low": "s-lo"}[x["band"]]
        basis = x["basis"]
        pill = ('<span class="pill p-ok">Official</span> ' if basis.startswith("OFFICIAL")
                else '<span class="pill p-no">Judgement</span> ')
        rk.append('<tr><td class="id">%s%s</td><td class="per">%s</td><td class="metric">%s</td>'
                  '<td class="per">%s</td><td class="id">%d</td><td class="id">%d</td>'
                  '<td class="val"><strong>%d</strong></td>'
                  '<td><span class="scorebar"><i class="%s" style="width:%d%%"></i></span><br>'
                  '<span class="small">%s</span></td>'
                  '<td class="note">%s%s</td><td class="note">%s</td><td class="id">%s</td></tr>'
                  % (esc(x["id"]), " &#9733;" if x.get("black_swan") else "",
                     esc(x["path"]), md_inline(x["risk"]), esc(x["category"]),
                     x["L"], x["I"], x["score"], cls, x["score"] * 4, esc(x["band"]),
                     pill, md_inline(basis), md_inline(x["mitigant"]),
                     esc(", ".join(x.get("refs", [])))))
    rk.append("</tbody></table></div>")
    rk.append('<p class="small">&#9733; = black-swan row. L = likelihood 1&ndash;5, '
              'I = impact 1&ndash;5, score = L &times; I. Risks whose basis is marked '
              '<span class="pill p-no">Judgement</span> are also listed on '
              '<a href="flagged.html">Flagged for Review</a>.</p>')
    made.append(page("risks.html", "Risk Register &mdash; Every Decision Path",
                     "Twenty-eight risks across six decision paths, each scored against an "
                     "official anchor where one exists and labelled as judgement where one does "
                     "not. Black-swan events are marked separately.",
                     "\n".join(rk)))

    # --------------------------------------------------------- decisions.html
    dc = []
    dc.append('<div class="callout"><strong>Decision question.</strong> %s</div>'
              % md_inline(dec["decision_question"]))
    dc.append('<div class="callout warn"><strong>%s</strong></div>' % md_inline(dec["meta"]["disclaimer"]))

    dc.append("<h3>Findings</h3>")
    for f in dec["findings"]:
        dc.append('<div class="card"><h4>%s &mdash; %s</h4><p>%s</p>'
                  '<p class="small mono">Evidence rows: %s</p></div>'
                  % (esc(f["id"]), md_inline(f["headline"]), md_inline(f["detail"]),
                     esc(", ".join(f["sources"]))))

    dc.append("<h3>The options</h3>")
    for o in dec["options"]:
        dc.append('<div class="opt"><span class="tag">%s</span><h4>%s</h4><p>%s</p>'
                  '<div class="twocol"><div class="pros"><h5>Strengths</h5><ul>%s</ul></div>'
                  '<div class="cons"><h5>Weaknesses</h5><ul>%s</ul></div></div>'
                  '<p class="small" style="margin-top:12px"><strong>Best when:</strong> %s</p></div>'
                  % (esc(o["id"]), md_inline(o["name"]), md_inline(o["summary"]),
                     "".join("<li>%s</li>" % md_inline(s) for s in o["strengths"]),
                     "".join("<li>%s</li>" % md_inline(s) for s in o["weaknesses"]),
                     md_inline(o["best_when"])))

    rec = dec["recommendation"]
    dc.append('<div class="rec"><h3>Recommendation</h3>'
              '<p style="font-size:17.5px;font-weight:600;letter-spacing:-.2px">%s</p>'
              '<p>%s</p></div>' % (md_inline(rec["headline"]), md_inline(rec["rationale"])))
    dc.append("<h3>The plan</h3>")
    for s in rec["plan"]:
        dc.append('<div class="step"><div class="n">%d</div><div class="b">'
                  '<div class="w">Step %d &middot; %s</div><h4 style="margin:2px 0 5px">%s</h4>'
                  '<p class="small">%s</p></div></div>'
                  % (s["step"], s["step"], esc(s["window"]), md_inline(s["action"]),
                     md_inline(s["detail"])))
    dc.append("<h3>Sell now instead, if any of these is true</h3><ol class='clean'>")
    for s in rec["sell_now_instead_if"]:
        dc.append("<li>%s</li>" % md_inline(s))
    dc.append("</ol>")
    dc.append('<div class="callout ok"><strong>Risk balance.</strong> %s</div>'
              % md_inline(rec["risk_balance"]))
    made.append(page("decisions.html", "Decision Options, Analysis & Recommendation",
                     "Six options, fourteen findings drawn only from verified rows, and a "
                     "conditional recommendation with a pre-committed sell trigger.",
                     "\n".join(dc)))

    # --------------------------------------------------------- projection.html
    pj = []
    pj.append('<div class="callout bad"><strong>Read the unit convention first.</strong> %s</div>'
              % md_inline(prj["meta"]["unit_convention"]))
    pj.append('<div class="callout warn"><strong>No official cap rate exists.</strong> %s</div>'
              % md_inline(prj["meta"]["no_official_cap_rate"]))
    pj.append('<p class="small"><strong>Reproducibility.</strong> %s</p>'
              % md_inline(prj["meta"]["reproducibility"]))
    pj.append("<p class='small'>Generated by <code>%s</code> from <code>%s</code>. "
              "Central case: %s.</p>"
              % (esc(pro["meta"]["generated_by"]), esc(prj["meta"].get("retrieved") and "data/projection.json"),
                 esc(", ".join("%s %s" % (k.replace("_", " "), v) for k, v in pro["meta"]["central_case"].items()))))

    pj.append("<h3>Model integrity check</h3>")
    pj.append('<div class="callout %s"><strong>%s</strong><br><span class="small mono">%s</span></div>'
              % ("ok" if pro["sanity"]["passed"] else "bad",
                 "PASSED" if pro["sanity"]["passed"] else "FAILED",
                 esc(pro["sanity"]["test"])))
    pj.append('<div class="scroll"><table><caption>A flat, never-ending, never-dark tenancy must '
              'return exactly 100.00 index points at every spread.</caption><thead><tr>'
              '<th>Spread over 10-yr UST</th><th>Capitalisation rate</th>'
              '<th>Closed-form perpetuity</th><th>60-year flat path</th>'
              '</tr></thead><tbody>')
    for s in pro["sanity"]["results"]:
        pj.append("<tr><td class='id'>%d bp</td><td class='val'>%.2f%%</td>"
                  "<td class='val'>%.2f</td><td class='val'>%.2f</td></tr>"
                  % (s["spread_bp"], s["cap_pct"], s["closed_form_perpetuity"],
                     s["sixty_year_flat_path"]))
    pj.append("</tbody></table></div>")

    pj.append("<h3>Fairness rules applied to both sides of the comparison</h3><ol class='clean'>")
    for f in pro["meta"]["fairness_rules"]:
        pj.append("<li>%s</li>" % md_inline(f))
    pj.append("</ol>")

    pj.append("<h3>Official model inputs</h3>")
    pj.append('<div class="scroll"><table><thead><tr><th>ID</th><th>Input</th><th>Value</th>'
              '<th>Units</th><th>Period</th><th>Role in the model</th>'
              '<th>Official source</th><th>Status</th></tr></thead><tbody>')
    for i in prj["official_inputs"]:
        pj.append('<tr><td class="id">%s</td><td class="metric"><code>%s</code></td>'
                  '<td class="val">%s</td><td class="per">%s</td><td class="per">%s</td>'
                  '<td class="note">%s</td>'
                  '<td class="src"><a href="%s" rel="noopener noreferrer external">%s &#8599;</a></td>'
                  '<td>%s</td></tr>'
                  % (esc(i["id"]), esc(i["name"]), esc(i["value"]), esc(i["units"]),
                     esc(i["period"]), md_inline(i["role"]), esc(i["u"]), esc(i["s"]),
                     '<span class="pill p-ok">Verified</span>' if i.get("k")
                     else '<span class="pill p-no">Unverified</span>'))
    pj.append("</tbody></table></div>")

    pj.append("<h3>Unverified scenario inputs</h3>")
    pj.append('<div class="callout warn">These are the only inputs in the model that are not '
              'official. Each is flagged, each is varied across a grid, and each output that '
              'depends on one is labelled. No output rests on a single unverified number.</div>')
    pj.append('<div class="scroll"><table><thead><tr><th>ID</th><th>Input</th><th>Grid</th>'
              '<th>Units</th><th>Role</th><th>Status</th></tr></thead><tbody>')
    for i in prj["unverified_inputs"]:
        pj.append('<tr><td class="id">%s</td><td class="metric"><code>%s</code></td>'
                  '<td class="val">%s</td><td class="per">%s</td><td class="note">%s</td>'
                  '<td><span class="pill p-blank">Unverified input</span><br>'
                  '<span class="small">%s</span></td></tr>'
                  % (esc(i["id"]), esc(i["name"]),
                     esc(", ".join(str(v) for v in i["values"])), esc(i["units"]),
                     md_inline(i["role"]), esc(i["s"])))
    pj.append("</tbody></table></div>")

    pj.append("<h3>Equations</h3>")
    pj.append('<div class="scroll"><table><thead><tr><th>ID</th><th>Name</th><th>Formula</th>'
              '<th>Note</th></tr></thead><tbody>')
    for e in prj["equations"]:
        pj.append('<tr><td class="id">%s</td><td class="metric">%s</td>'
                  '<td class="note mono">%s</td><td class="note">%s</td></tr>'
                  % (esc(e["id"]), esc(e["name"]), esc(e["formula"]), md_inline(e["note"])))
    pj.append("</tbody></table></div>")

    def num_table(title, caption, head, body_rows, note=None):
        pj.append("<h3>%s</h3>" % title)
        pj.append('<div class="scroll"><table>')
        if caption:
            pj.append("<caption>%s</caption>" % caption)
        pj.append("<thead><tr>" + "".join("<th>%s</th>" % h for h in head) + "</tr></thead><tbody>")
        pj.extend(body_rows)
        pj.append("</tbody></table></div>")
        if note:
            pj.append('<p class="small">%s</p>' % md_inline(note))

    num_table("Capitalisation-rate grid",
              "Anchored on the official U.S. Treasury 10-year par yield of %.2f%% on November 5, "
              "2026. The spread is an UNVERIFIED scenario input (UX-1)."
              % pro["risk_free"]["ten_year_pct"],
              ["Spread", "Cap rate", "Implied opening NOI (index)"],
              ["<tr><td class='id'>%d bp</td><td class='val'>%.2f%%</td><td class='val'>%.3f</td></tr>"
               % (g["spread_bp"], g["cap_pct"], g["implied_noi0_index"]) for g in pro["cap_grid"]],
              "Risk-free anchors: 10-year %.2f%%, 30-year %.2f%% (U.S. Treasury, November 5, 2026)."
              % (pro["risk_free"]["ten_year_pct"], pro["risk_free"]["thirty_year_pct"]))

    num_table("Tenant non-renewal probability (EQ-4)",
              "Compound survival at the company-disclosed ongoing annual closure rate of %.1f%% "
              "of system units. Programme-level bounds: %.2f%% to %.2f%% of the system."
              % (pro["closure_probability"]["official_annual_rate_pct"],
                 pro["closure_probability"]["programme_bounds_pct"]["low"],
                 pro["closure_probability"]["programme_bounds_pct"]["high"]),
              ["Years to expiry", "Expiry year", "P(non-renewal)"],
              ["<tr><td class='val'>%d</td><td class='val'>%d</td><td class='val'><strong>%.2f%%</strong></td></tr>"
               % (c["years"], c["expiry_year"], c["p_dark_pct"])
               for c in pro["closure_probability"]["by_horizon"]],
              pro["closure_probability"]["note"])

    num_table("Option A &mdash; sell now (EQ-8)",
              "Present value of selling today, net of the statutory transaction cost. Index 100.0 "
              "= current asset value.",
              ["Case", "Transaction cost", "Net index"],
              ["<tr><td class='metric'>%s</td><td class='val'>%.1f%%</td>"
               "<td class='val'><strong>%.2f</strong></td></tr>"
               % (esc(s["case"]), s["transaction_cost_pct"], s["net_index"])
               for s in pro["sell_now"]],
              pro["sell_now_note"])

    num_table("The Measure ULA dead band",
              "Pure arithmetic on the official statutory rates (IN-16, IN-17). The dollar "
              "thresholds themselves are unverified and are not stated.",
              ["Statutory rate", "Break-even multiple of threshold", "Break-even excess", "Reading"],
              ["<tr><td class='val'>%.1f%%</td><td class='val'>%.4f&times;</td>"
               "<td class='val'>%.2f%%</td><td class='note'>%s</td></tr>"
               % (d["rate_pct"], d["breakeven_multiple_of_threshold"],
                  d["breakeven_excess_pct"], esc(d["reading"]))
               for d in pro["ula_dead_band"]],
              pro["ula_dead_band_note"])

    num_table("Option C &mdash; hold to expiry, base regime (EQ-7)",
              "Present value of holding, at the central case, net of a %.1f%% exit transaction "
              "cost and one year of post-expiry downtime. The official system-wide "
              "non-renewal base rate applies."
              % pro["meta"]["central_case"]["exit_transaction_cost_pct"],
              ["Years", "Expiry", "Escalator", "Escalator %", "PV of income",
               "PV of terminal", "PV total", "P(dark)", "Range across cap grid"],
              ["<tr><td class='val'>%d</td><td class='val'>%d</td><td class='per'>%s</td>"
               "<td class='val'>%.1f%%</td><td class='val'>%.2f</td><td class='val'>%.2f</td>"
               "<td class='val'><strong>%.2f</strong></td><td class='val'>%.2f%%</td>"
               "<td class='val small'>%.2f &ndash; %.2f</td></tr>"
               % (h["years"], h["expiry_year"], esc(h["escalator"]), h["escalator_pct"],
                  h["pv_income"], h["pv_terminal"], h["pv_total"], h["p_dark_pct"],
                  h["grid_min"], h["grid_max"])
               for h in pro["hold_to_expiry"]],
              "Compare with the sell-now net index of 94.50 to 100.00 above. In the base regime "
              "holding beats selling at every point of the cap grid.")

    num_table("The decisive case &mdash; hold AFTER a non-renewal signal (EQ-7, P(dark) = 100%)",
              "The same hold path, but with site-specific non-renewal treated as certain because "
              "the tenant has refused an extension or disclosed a franchise agreement expiring at "
              "or before the lease expiry.",
              ["Years", "Expiry", "PV of income", "PV of terminal (dark)", "PV total",
               "Range across cap grid", "Sell now (lower ULA tier)", "Sell wins?"],
              ["<tr><td class='val'>%d</td><td class='val'>%d</td><td class='val'>%.2f</td>"
               "<td class='val'>%.2f</td><td class='val'><strong>%.2f</strong></td>"
               "<td class='val small'>%.2f &ndash; %.2f</td><td class='val'>%.2f</td>"
               "<td><span class='pill %s'>%s</span></td></tr>"
               % (s["years"], s["expiry_year"], s["pv_income"], s["pv_terminal"], s["pv_total"],
                  s["grid_min"], s["grid_max"], s["sell_now_index_lower_ula"],
                  "p-blank" if s["sell_now_wins"] else "p-ok",
                  "YES &mdash; sell" if s["sell_now_wins"] else "no &mdash; hold")
               for s in pro["hold_after_signal"]],
              pro["hold_after_signal_note"])

    num_table("Option B &mdash; extend the term, then hold (EQ-9)",
              "A %d-year extension granted at existing economics, against holding to the original "
              "expiry. Central case." % 10,
              ["Original years", "Extended years", "Escalator %", "PV hold", "PV extend",
               "Difference", "P(dark) hold", "P(dark) extend", "Extension wins at every spread?"],
              ["<tr><td class='val'>%d</td><td class='val'>%d</td><td class='val'>%.1f%%</td>"
               "<td class='val'>%.2f</td><td class='val'><strong>%.2f</strong></td>"
               "<td class='val'>+%.2f</td><td class='val'>%.2f%%</td><td class='val'>%.2f%%</td>"
               "<td><span class='pill %s'>%s</span></td></tr>"
               % (e["years"], e["extended_years"], e["escalator_pct"], e["pv_hold"],
                  e["pv_extend"], e["delta"], e["p_dark_hold_pct"], e["p_dark_extend_pct"],
                  "p-ok" if e["extend_wins_across_grid"] else "p-no",
                  "yes" if e["extend_wins_across_grid"] else "no")
               for e in pro["extend_then_hold"]],
              pro["extend_note"])

    num_table("Ranking stability across the whole cap grid (EQ-10)",
              "The cap-rate input is unverified, so only the RANKING of paths is meaningful. A "
              "ranking is robust only if it holds at every point of the Treasury-anchored spread "
              "grid.",
              ["Years", "Transaction-cost case", "Sell index", "Hold range", "Extend range",
               "Hold-after-signal range", "Stable?"],
              ["<tr><td class='val'>%d</td><td class='per'>%s</td><td class='val'>%.2f</td>"
               "<td class='val small'>%.2f &ndash; %.2f</td>"
               "<td class='val small'>%.2f &ndash; %.2f</td>"
               "<td class='val small'>%.2f &ndash; %.2f</td>"
               "<td><span class='pill %s'>%s</span></td></tr>"
               % (s["years"], esc(s["case"]), s["sell_index"],
                  s["hold_range"][0], s["hold_range"][1],
                  s["extend_range"][0], s["extend_range"][1],
                  s["signal_hold_range"][0], s["signal_hold_range"][1],
                  "p-ok" if s["ranking_is_stable"] else "p-no",
                  "stable" if s["ranking_is_stable"] else "flips")
               for s in pro["ranking_stability"]],
              pro["ranking_stability_note"])

    num_table("Stress case &mdash; the conditions under which this recommendation is wrong",
              "Worst declared inputs: no escalator, lowest land residual, zero official "
              "land-price growth, longest downtime, and a parcel outside the City of Los Angeles "
              "so the sell path pays no Measure ULA at all.",
              ["Years", "Expiry", "PV hold (stress)", "PV sell (best case)", "Sell wins?", "Gap"],
              ["<tr><td class='val'>%d</td><td class='val'>%d</td><td class='val'>%.2f</td>"
               "<td class='val'>%.2f</td><td><span class='pill %s'>%s</span></td>"
               "<td class='val'>%.2f</td></tr>"
               % (s["years"], s["expiry_year"], s["pv_hold_stress"], s["pv_sell_best_case"],
                  "p-blank" if s["sell_wins"] else "p-ok",
                  "YES" if s["sell_wins"] else "no", s["gap"])
               for s in pro["stress_case"]],
              pro["stress_case_note"])

    num_table("Sensitivity &mdash; post-expiry downtime",
              "Downtime is a scenario input, not an official statistic (flag F-33). It is "
              "included because omitting it would flatter the hold path.",
              ["Downtime (years)"] + ["PV at %d years" % n for n in
                                      [x["years"] for x in pro["downtime_sensitivity"][0]["pv_total_by_horizon"]]],
              ["<tr><td class='val'>%.1f</td>%s</tr>"
               % (d["downtime_years"], "".join("<td class='val'>%.2f</td>" % x["pv_total"]
                                                for x in d["pv_total_by_horizon"]))
               for d in pro["downtime_sensitivity"]],
              pro["downtime_note"])

    num_table("Sensitivity &mdash; dark-box land residual",
              "What the site retains if the restaurant closes and only land and shell value "
              "remain. Unverified input (UX-2).",
              ["Land residual (% of value)"] + ["PV at %d years" % x["years"] for x in
                                                pro["residual_sensitivity"][0]["pv_total_by_horizon"]],
              ["<tr><td class='val'>%.0f%%</td>%s</tr>"
               % (d["residual_pct"], "".join("<td class='val'>%.2f</td>" % x["pv_total"]
                                             for x in d["pv_total_by_horizon"]))
               for d in pro["residual_sensitivity"]],
              pro["residual_note"])

    num_table("Sensitivity &mdash; official land-price growth",
              "Two official FHFA assumptions, in both regimes.",
              ["Official assumption", "Growth", "Regime"] + ["%d yr" % x["years"] for x in
                                                             pro["land_growth_sensitivity"][0]["base_regime_by_horizon"]],
              ["".join(["<tr><td class='metric' rowspan='2'>%s</td><td class='val' rowspan='2'>%.1f%%</td>"
                        "<td class='per'>Base</td>%s</tr>"
                        "<tr><td class='per'>After signal</td>%s</tr>"
                        % (esc(d["label"]), d["hpi_pct"],
                           "".join("<td class='val'>%.4f</td>" % x["pv_total"] for x in d["base_regime_by_horizon"]),
                           "".join("<td class='val'>%.4f</td>" % x["pv_total"] for x in d["signal_regime_by_horizon"]))])
               for d in pro["land_growth_sensitivity"]],
              pro["land_growth_note"])

    num_table("Catastrophe overlay (EQ-11, EQ-12)",
              "Severity and frequency bands drawn from official statistics, deliberately NOT "
              "multiplied into the present values above.",
              ["Measure", "Value", "Basis"],
              ["<tr><td class='metric'>January-2025-class fire, share of one year of county "
               "economic output</td><td class='val'><strong>%.2f%% to %.2f%%</strong></td>"
               "<td class='note'>%s</td></tr>"
               "<tr><td class='metric'>M6.7+ earthquake, official 30-year probability</td>"
               "<td class='val'>%.1f%%</td><td class='note'>%s</td></tr>"
               "<tr><td class='metric'>Same event restated over a five-year window &mdash; compound</td>"
               "<td class='val'>%.2f%%</td><td class='note' rowspan='2'>%s</td></tr>"
               "<tr><td class='metric'>Same event restated over a five-year window &mdash; linear</td>"
               "<td class='val'>%.2f%%</td></tr>"
               % (pro["catastrophe_overlay"]["fire_output_loss_share_of_county_gdp_pct"]["low"],
                  pro["catastrophe_overlay"]["fire_output_loss_share_of_county_gdp_pct"]["high"],
                  esc(pro["catastrophe_overlay"]["fire_output_loss_share_of_county_gdp_pct"]["basis"]),
                  pro["catastrophe_overlay"]["earthquake_five_year_probability_pct"]["thirty_year_official_pct"],
                  esc(pro["catastrophe_overlay"]["earthquake_five_year_probability_pct"]["basis"]),
                  pro["catastrophe_overlay"]["earthquake_five_year_probability_pct"]["compound"],
                  esc(pro["catastrophe_overlay"]["earthquake_five_year_probability_pct"]["basis"]),
                  pro["catastrophe_overlay"]["earthquake_five_year_probability_pct"]["linear"])],
              pro["catastrophe_overlay"]["note"])

    pj.append("<h3>Limitations</h3><ol class='clean'>")
    for l in prj["limitations"]:
        pj.append("<li>%s</li>" % md_inline(l))
    pj.append("</ol>")
    made.append(page("projection.html", "Projection System &mdash; Specification, Inputs & Results",
                     "A documented, reproducible model built only from official inputs, with "
                     "every unverifiable input declared, gridded and labelled. Normalised to an "
                     "index: current asset value = 100.0.",
                     "\n".join(pj)))

    # ----------------------------------------------------------- sources.html
    so = []
    so.append('<div class="callout"><strong>%s</strong></div>' % md_inline(src["meta"]["policy"]))
    so.append("<h3>Coverage</h3><div class='grid g4'>"
              + kv("Table rows", {"v": str(st["rows_total"]), "p": "across 10 data categories"})
              + kv("Verified", {"v": "%d (%.1f%%)" % (st["rows_verified"], st["rows_verified"] * 100.0 / st["rows_total"]), "p": "each carries an official link"})
              + kv("Unverified", {"v": str(st["rows_unverified"]), "p": "value withheld"})
              + kv("Blank cells", {"v": str(st["rows_blank"]), "p": "no official confirmation"})
              + kv("Distinct official URLs", {"v": str(sum(p["url_count"] for p in src["publishers"])), "p": "across %d publishers" % len(src["publishers"])})
              + kv("Rows with no official publisher", {"v": str(st["rows_no_url"]), "p": "structural gaps, all flagged"})
              + "</div>")

    so.append("<h3>Per-file coverage</h3>")
    so.append('<div class="scroll"><table><thead><tr><th>Data file</th><th>Rows</th>'
              '<th>Verified</th><th>Unverified</th><th>Blank</th><th>No URL</th>'
              '<th>Coverage</th></tr></thead><tbody>')
    for f, c in src["meta"]["per_file"].items():
        if not c["rows"]:
            continue
        pct = c["verified"] * 100.0 / c["rows"]
        so.append("<tr><td class='metric mono'>data/%s</td><td class='val'>%d</td>"
                  "<td class='val'>%d</td><td class='val'>%d</td><td class='val'>%d</td>"
                  "<td class='val'>%d</td>"
                  "<td class='val'><span class='scorebar'><i class='%s' style='width:%d%%'></i></span>"
                  " <span class='small'>%.0f%%</span></td></tr>"
                  % (esc(f), c["rows"], c["verified"], c["unverified"], c["blank"], c["no_url"],
                     "s-lo" if pct >= 80 else ("s-el" if pct >= 50 else "s-se"), int(pct), pct))
    so.append("</tbody></table></div>")

    so.append("<h3>Official publishers, every URL, and what each row cites it for</h3>")
    for p in src["publishers"]:
        so.append('<div class="card"><h4>%s</h4><p class="small">%d distinct URLs &middot; '
                  'cited by %d rows</p>' % (esc(p["publisher"]), p["url_count"], p["row_citations"]))
        so.append('<div class="scroll"><table><thead><tr><th>Official URL</th>'
                  '<th>Cited by rows</th><th>Topics</th></tr></thead><tbody>')
        for u in p["urls"]:
            so.append('<tr><td class="src"><a href="%s" rel="noopener noreferrer external">'
                      '%s &#8599;</a></td><td class="id">%s</td><td class="note small">%s</td></tr>'
                      % (esc(u["url"]), esc(u["url"].replace("https://", "").replace("http://", "")),
                         esc(", ".join(u["cited_by"])),
                         esc("; ".join(t for t in u["topics"][:4]) or "&mdash;")))
        so.append("</tbody></table></div></div>")
    made.append(page("sources.html", "Sources & Verification Register",
                     "Every official publisher, every URL, and the exact rows that cite it. "
                     "Generated automatically from the data files so it cannot drift from the "
                     "tables it documents.",
                     "\n".join(so)))

    # ----------------------------------------------------------- flagged.html
    fl = []
    fl.append('<div class="callout bad"><strong>Why this page exists.</strong> %s</div>'
              % md_inline(flg["meta"]["policy"]))
    fl.append('<p class="small">%s</p>' % md_inline(flg["meta"]["status"]))
    fl.append("<div class='grid g4'>"
              + kv("Open flags", {"v": str(len(flg["flags"])), "p": "non-blocking, all disclosed"})
              + kv("Irregularities in official sources", {"v": str(len(flg["irregularities"])), "p": "contradictions and silent gaps"})
              + kv("Rows left blank", {"v": str(st["rows_blank"]), "p": "of %d published rows" % st["rows_total"]})
              + kv("Rows with no official publisher", {"v": str(st["rows_no_url"]), "p": "no government source exists"})
              + "</div>")

    sev_order = {"Structural": 0, "High": 1, "Medium": 2, "Low": 3}
    fl.append("<h3>Flag register</h3>")
    fl.append('<div class="scroll"><table><thead><tr><th>ID</th><th>Severity</th><th>Flag</th>'
              '<th>Why it could not be verified</th><th>Official route to close it</th>'
              '<th>Affected rows</th><th>Status</th></tr></thead><tbody>')
    for f in sorted(flg["flags"], key=lambda z: (sev_order.get(z["severity"], 9), z["id"])):
        route = f["official_route_to_close"]
        u = f.get("u")
        routecell = esc(route) if not u else \
            '%s<br><a href="%s" rel="noopener noreferrer external">Open the official source &#8599;</a>' % (esc(route), esc(u))
        sevcls = {"Structural": "p-grey", "High": "p-blank", "Medium": "p-no", "Low": "p-info"}[f["severity"]]
        fl.append('<tr><td class="id">%s</td><td><span class="pill %s">%s</span></td>'
                  '<td class="metric">%s</td><td class="note">%s</td><td class="note">%s</td>'
                  '<td class="id">%s</td><td><span class="pill p-no">Needs review</span></td></tr>'
                  % (esc(f["id"]), sevcls, esc(f["severity"]), md_inline(f["title"]),
                     md_inline(f["detail"]), routecell, esc(", ".join(f["rows"]))))
    fl.append("</tbody></table></div>")
    fl.append('<p class="small">No flag on this page blocks publication. Each is a disclosed gap '
              'with a named official route to close it.</p>')

    fl.append("<h3>Irregularities in the official sources themselves</h3>")
    fl.append('<div class="scroll"><table><thead><tr><th>ID</th><th>Irregularity</th>'
              '<th>What the official record shows</th><th>Official source</th>'
              '<th>Impact</th></tr></thead><tbody>')
    for ir in flg["irregularities"]:
        fl.append('<tr><td class="id">%s</td><td class="metric">%s</td><td class="note">%s</td>'
                  '<td class="src"><a href="%s" rel="noopener noreferrer external">%s &#8599;</a></td>'
                  '<td class="note">%s</td></tr>'
                  % (esc(ir["id"]), md_inline(ir["title"]), md_inline(ir["detail"]),
                     esc(ir["u"]), esc(ir["s"]), md_inline(ir["impact"])))
    fl.append("</tbody></table></div>")

    fl.append("<h3>Every unverified row, in one place</h3>")
    fl.append('<p class="lede">These are all %d rows across the ten data categories that are not '
              'marked verified. %d of them are blank in the value cell. Rows carrying a '
              '<span class="pill p-info">Reported</span> marker show what a non-official source '
              'claimed &mdash; recorded so a reader can see exactly what was declined, and never '
              'used as a value or as a model input.</p>' % (st["rows_unverified"], st["rows_blank"]))
    fl.append(row_table([dict(r, id="%s" % r["id"]) for _, r in all_rows if not r.get("k")]))

    fl.append("<h3>Source classes deliberately excluded</h3><ul class='clean'>")
    for c in flg["excluded_sources"]["classes"]:
        fl.append("<li>%s</li>" % esc(c))
    fl.append("</ul>")
    made.append(page("flagged.html", "Flagged for Review",
                     "Every unverified row, every blank cell, every open flag and every "
                     "irregularity in the official record &mdash; with the official link needed "
                     "to close each one.",
                     "\n".join(fl)))

    print("built %d pages" % len(made))
    for m in made:
        print("  ", os.path.relpath(m, ROOT), os.path.getsize(m), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(build())
