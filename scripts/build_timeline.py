#!/usr/bin/env python3
"""Decision timeline and monitoring triggers (session dcb5495c, 2026-11-12).

Self-contained supplement to the curated dashboard. The data lives in its own file,
``data/timeline-2026-11-12-dcb5495c.json``, so the shared verified dataset is not edited.

``merge_supplement(data)`` adds this file's sources, flags and audit entry to the in-memory
dataset so they appear on the Sources, Flagged for Review and Audit pages.
``build_timeline(data, helpers)`` renders ``timeline.html`` with the same layout and table
helpers as every other page. ``helpers`` is the ``build_public`` module (or any object that
provides ``e``, ``badge``, ``table``, ``layout`` and ``source_links``).

Rules enforced here and in ``tests/test_timeline.py``:
* every row carries at least one official source link;
* a date or value that no official page states is ``None`` and renders as a blank cell;
* derived figures are recomputed from the stored official inputs at build time.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TIMELINE_PATH = ROOT / "data" / "timeline-2026-11-12-dcb5495c.json"
PAGE = "timeline.html"
NAV_LABEL = "Timeline & triggers"
CARD_TEXT = "Dated official milestones around the 2030–2035 window, statutory clocks, what to watch."


def load_timeline(path: Path | str = TIMELINE_PATH) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def merge_supplement(data: dict[str, Any], timeline: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return a copy of ``data`` with the timeline supplement attached. Idempotent."""
    if "timeline" in data:
        return data
    timeline = timeline or load_timeline()
    merged = copy.deepcopy(data)
    for sid, src in timeline["sources"].items():
        if sid in merged["sources"]:
            raise ValueError(f"timeline source id collides with dataset: {sid}")
        merged["sources"][sid] = src
    existing_flags = {f["id"] for f in merged["flags"]}
    existing_audit = {a["id"] for a in merged["audit"]}
    for flag in timeline["flags"]:
        if flag["id"] in existing_flags:
            raise ValueError(f"timeline flag id collides with dataset: {flag['id']}")
        merged["flags"].append(flag)
    for entry in timeline["audit"]:
        if entry["id"] in existing_audit:
            raise ValueError(f"timeline audit id collides with dataset: {entry['id']}")
        merged["audit"].append(entry)
    merged["timeline"] = timeline
    return merged


def schedule_rows(timeline: dict[str, Any]) -> list[dict[str, Any]]:
    """Issuer's scheduled principal by fiscal year with derived share and running share."""
    sched = timeline["principal_schedule"]
    total = sched["total_thousands"]
    if sum(r["thousands"] for r in sched["rows"]) != total:
        raise ValueError("principal schedule does not sum to the stated total")
    out, running = [], 0
    for row in sched["rows"]:
        running += row["thousands"]
        out.append({
            "period": row["period"],
            "thousands": row["thousands"],
            "share": row["thousands"] / total * 100.0,
            "cumulative": running / total * 100.0,
        })
    return out


def _blank(h: Any, value: Any) -> str:
    if value is None:
        return '<td class="blank-value" aria-label="Unconfirmed value intentionally blank"></td>'
    return f"<td>{h.e(value)}</td>"


def build_timeline(data: dict[str, Any], h: Any) -> str:
    data = merge_supplement(data)
    t = data["timeline"]
    e, badge, table, src = h.e, h.badge, h.table, h.source_links

    milestones = sorted(t["milestones"], key=lambda r: r["sort"])
    milestone_rows = [[
        _blank(h, m["when"]),
        f'<strong>{e(m["milestone"])}</strong>',
        _blank(h, m["value"]),
        badge(m["status"]) + f'<span class="row-note">{e(m["note"])}</span>',
        e(m["meaning"]),
        src(data, m["sources"]),
    ] for m in milestones]

    sched_sources = t["principal_schedule"]["sources"]
    sched_rows = [[
        e(r["period"]),
        e(f'${r["thousands"]:,} thousand'),
        badge("derived") + f'<span class="row-note">{r["share"]:.1f}% of total</span>',
        e(f'{r["cumulative"]:.1f}%'),
        src(data, sched_sources),
    ] for r in schedule_rows(t)]

    clock_rows = [[
        f'<strong>{e(c["clock"])}</strong>',
        e(c["starts"]),
        e(c["length"]),
        badge(c["status"]) + f'<span class="row-note">{e(c["note"])}</span>',
        src(data, c["sources"]),
    ] for c in t["clocks"]]

    lease_rows = [[
        f'<strong>{e(f["finding"])}</strong>',
        e(f["value"]),
        badge(f["status"]) + f'<span class="row-note">{e(f["note"])}</span>',
        src(data, f["sources"]),
    ] for f in t["lease_facts"]]

    monitor_rows = [[
        f'<strong>{e(m["indicator"])}</strong>',
        e(m["latest"]),
        badge("analysis") + f'<span class="row-note">{e(m["watch"])}</span>',
        e(m["moves"]),
        src(data, m["sources"]),
    ] for m in t["monitors"]]

    window_rows = [[
        f'<strong>{e(w["phase"])}</strong>',
        e(w["action"]),
        badge("analysis") + f'<span class="row-note">{e(w["why"])}</span>',
        src(data, w["sources"]),
    ] for w in t["windows"]]

    blanks = sum(1 for m in milestones if m["when"] is None or m["value"] is None)
    body = f"""
<div class="callout warning"><h3>The decision deadline itself is still blank</h3><p>The lease is reported to expire between 2030 and 2035. The exact date, the renewal options and the notice deadlines are in the executed lease, which has not been reviewed. This page shows the official, dated events that surround that window. {blanks} of {len(milestones)} milestone rows have a blank date or value because no official page states it; each is listed on <a href="flagged.html">Flagged for Review</a>.</p></div>
<p>Read at {e(t["meta"]["read_at"])}. Every row was matched to its official page at that reading and links to it. Rows marked “Analysis / judgment” are suggestions about what to watch, not official statements and not trigger levels set by any agency.</p>

<section aria-labelledby="tl-milestones"><p class="eyebrow">2026 to 2035</p><h2 id="tl-milestones">Dated official milestones</h2>
<p>In date order. Each of the tenant's four classes of fixed-rate notes has a repayment date before or inside the reported window: February 2027, August 2029, May 2031 and February 2032.</p>
{table("timeline-milestones", "Dated official milestones from 2026 to 2035, with blank cells where no official date or value exists.", ["When", "Milestone", "Official value", "Status and what the source says", "Why it matters for sell versus renew", "Official source"], milestone_rows)}
</section>

<section aria-labelledby="tl-schedule"><p class="eyebrow">Tenant debt</p><h2 id="tl-schedule">Issuer's own schedule of principal payments</h2>
<p>{e(t["principal_schedule"]["note"])} Shares are derived from the issuer's figures. The issuer's fiscal year ends in late September. The same schedule, without the shares, is listed on <a href="property.html">Property &amp; tenant</a>.</p>
{table("timeline-schedule", "Scheduled principal payments by fiscal year from the issuer's quarterly report, with derived shares.", ["Fiscal period", "Scheduled principal", "Share of total", "Cumulative share", "Official source"], sched_rows, searchable=False)}
</section>

<section aria-labelledby="tl-lease"><p class="eyebrow">Tenant real estate</p><h2 id="tl-lease">Who holds the building at Jack in the Box sites</h2>
<p>Portfolio-wide figures from the tenant's annual report. They show that “a Jack in the Box lease” can mean three different arrangements; none of these rows describes this property. The issuer's lease-terms and renewal statements are on <a href="property.html">Property &amp; tenant</a>.</p>
{table("timeline-lease", "Issuer-wide property-interest figures from the annual report.", ["Finding", "Official value", "Status and limits", "Official source"], lease_rows, searchable=False)}
</section>

<section aria-labelledby="tl-clocks"><p class="eyebrow">Clocks, not calendar dates</p><h2 id="tl-clocks">Deadlines that start when a decision is taken</h2>
{table("timeline-clocks", "Statutory and regulatory clocks that start on a sale, a transfer, or an agency action.", ["Clock", "Starts", "Length or rate", "Status and limits", "Official source"], clock_rows)}
</section>

<section aria-labelledby="tl-monitor"><p class="eyebrow">Monitoring</p><h2 id="tl-monitor">What to watch, and which way it moves the decision</h2>
<p>The “latest reading” column is official. The “watch for” and “moves” columns are analyst judgment; no numeric trigger is set because none can be verified. For which way each published figure leans today, see the signal scorecard on <a href="projections.html">Projections</a>; this table is about what would change that reading.</p>
{table("timeline-monitor", "Official indicators to monitor, with analyst judgment about what would change the decision.", ["Indicator", "Latest official reading", "Watch for", "Which way it moves the decision", "Official source"], monitor_rows)}
</section>

<section aria-labelledby="tl-windows"><p class="eyebrow">Sequence</p><h2 id="tl-windows">Three working periods</h2>
<p>A suggested order of work built only from the dated rows above. It becomes a real calendar once the lease dates are known. See also <a href="decision.html">Decision paths</a> and <a href="suggestions.html">Suggestions review</a>.</p>
{table("timeline-windows", "Suggested working periods anchored to official milestone dates.", ["Period", "Work to complete", "Why this period", "Official source"], window_rows, searchable=False)}
</section>
"""
    return h.layout(data, PAGE, "Decision timeline and monitoring triggers", "Official dated milestones from 2026 to 2035, set against the reported lease-expiry window. Unknown dates are blank.", body)


if __name__ == "__main__":
    t = load_timeline()
    for row in schedule_rows(t):
        print(f'{row["period"]:<26}{row["thousands"]:>10,}  {row["share"]:5.1f}%  {row["cumulative"]:5.1f}%')
