#!/usr/bin/env python3
"""Decision tools supplement (session 4c386ad4, 2026-11-15).

Adds one curated page to the public dashboard:

* ``aftertax.html``  — after-tax sale module: a browser-only calculator with blank inputs, using
  the verified federal, California and LA transfer-tax rules in ``data/k-4c386ad4-supplement.json``.
  It complements the sell-versus-hold worksheet on ``decision.html`` (W-02, session 1d0e4b3c), which
  takes rates as inputs; this module computes the sale side from official rules.

``merge_supplement(data)`` adds the supplement's sources, flags and audit entry to the in-memory
dataset so they appear on the Sources, Flagged for Review and Audit pages. The shared verified
dataset file is not edited. ``helpers`` is the ``build_public`` module (``e``, ``badge``, ``table``,
``layout``, ``source_links``, ``value_cell``).

Rules enforced here and in ``tests/test_decision_tools.py``:
* every table row carries at least one allowlisted official source link;
* a value that no official page states is blank (``None``), never zero or inferred;
* the calculator ships with no network, storage or cookie code, and with empty inputs.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SUPPLEMENT_PATH = ROOT / "data" / "k-4c386ad4-supplement.json"

AFTERTAX_PAGE = "aftertax.html"
PAGES = [AFTERTAX_PAGE]
NAV_ITEMS = [(AFTERTAX_PAGE, "After-tax module")]
AFTERTAX_JS = "assets/aftertax.js"


def load_supplement() -> dict[str, Any]:
    return json.loads(SUPPLEMENT_PATH.read_text(encoding="utf-8"))


def merge_supplement(data: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of ``data`` with this supplement's sources, flags and audit entries added."""
    sup = load_supplement()
    merged = copy.deepcopy(data)
    for sid, src in sup["sources"].items():
        if sid in merged["sources"]:
            raise ValueError(f"source id collision: {sid}")
        merged["sources"][sid] = src
    flag_ids = {f["id"] for f in merged["flags"]}
    for flag in sup["flags"]:
        if flag["id"] in flag_ids:
            raise ValueError(f"flag id collision: {flag['id']}")
        merged["flags"].append(flag)
    audit_ids = {a["id"] for a in merged["audit"]}
    for entry in sup["audit"]:
        if entry["id"] in audit_ids:
            raise ValueError(f"audit id collision: {entry['id']}")
        merged["audit"].append(entry)
    return merged


def _money(x: float) -> str:
    return f"${x:,.0f}"


def _pill(h: Any, label: str, cls: str) -> str:
    return f'<span class="badge {cls}">{h.e(label)}</span>'


# ---------------------------------------------------------------- after-tax module (K-4)
def aftertax_rules_json(sup: dict[str, Any]) -> str:
    """Rules as a JSON block for the page; '</' is escaped so it cannot close the script element."""
    rules = sup["rules"]
    payload = {
        "federal_ltcg_2026": {
            "zero_rate_max": rules["federal_ltcg_2026"]["zero_rate_max"],
            "fifteen_rate_max": rules["federal_ltcg_2026"]["fifteen_rate_max"],
            "top_ltcg_rate": rules["federal_ltcg_2026"]["top_ltcg_rate"],
            "mid_ltcg_rate": rules["federal_ltcg_2026"]["mid_ltcg_rate"],
            "unrecaptured_1250_max_rate": rules["federal_ltcg_2026"]["unrecaptured_1250_max_rate"],
        },
        "niit": {"rate": rules["niit"]["rate"], "threshold": rules["niit"]["threshold"]},
        "ca_schedules_2025": {
            "schedule_for_status": rules["ca_schedules_2025"]["schedule_for_status"],
            "X": rules["ca_schedules_2025"]["X"],
            "Y": rules["ca_schedules_2025"]["Y"],
            "Z": rules["ca_schedules_2025"]["Z"],
        },
        "ca_bhst": {"threshold": rules["ca_bhst"]["threshold"], "rate": rules["ca_bhst"]["rate"]},
        "dtt": {k: v for k, v in rules["dtt"].items() if not k.startswith(("quote", "source"))},
    }
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return text.replace("</", "<\\/")


def _rule_rows(data: dict[str, Any], h: Any, sup: dict[str, Any]) -> list[list[str]]:
    e, src = h.e, h.source_links
    r = sup["rules"]
    fed = r["federal_ltcg_2026"]
    zero = fed["zero_rate_max"]
    fifteen = fed["fifteen_rate_max"]
    dtt = r["dtt"]
    rows = [
        [f"<strong>Federal long-term capital gain bands, 2026</strong><span class=\"row-note\">Taxable income at which each rate starts</span>",
         e(f"0% up to ${zero['single']:,} single · ${zero['mfj']:,} MFJ/surviving spouse · ${zero['hoh']:,} HOH · ${zero['mfs']:,} MFS. "
           f"15% up to ${fifteen['single']:,} single · ${fifteen['mfj']:,} MFJ · ${fifteen['hoh']:,} HOH · ${fifteen['mfs']:,} MFS. 20% above."),
         src(data, r["federal_ltcg_2026"]["source_ids"][:1])],
        ["<strong>Unrecaptured section 1250 gain (real-property depreciation)</strong>",
         e("Taxed at a maximum 25% rate. The calculator uses the 25% ceiling, which can overstate tax."),
         src(data, ["irs_topic_409"])],
        ["<strong>Net investment income tax</strong><span class=\"row-note\">3.8% on the lesser of investment income or MAGI above the threshold</span>",
         e(f"3.8%. Thresholds: ${r['niit']['threshold']['single']:,} single/HOH · ${r['niit']['threshold']['mfj']:,} MFJ/surviving spouse · ${r['niit']['threshold']['mfs']:,} MFS (statutory, not indexed)."),
         src(data, ["irs_niit"])],
        ["<strong>California capital gains</strong>",
         e("Taxed as ordinary income; no lower individual capital-gains rate. Brackets in the table below."),
         src(data, ["ftb_capgains"])],
        ["<strong>California Behavioral Health Services Tax</strong><span class=\"row-note\">Formerly Mental Health Services Tax</span>",
         e(f"1% of taxable income over ${r['ca_bhst']['threshold']:,}."),
         src(data, r["ca_bhst"]["source_ids"])],
        ["<strong>LA County documentary transfer tax</strong>",
         e("$0.55 for each $500, or fractional part thereof, on consideration over $100 (outside the five special cities)."),
         src(data, ["lavote_dtt"])],
        ["<strong>City of Los Angeles documentary transfer tax</strong>",
         e("Base: $2.25 for each $500, or fraction. County rate inside the City: full $1.10 per $1,000 (0.11%), not rounded to $500."),
         src(data, ["lavote_dtt"])],
        ["<strong>Measure ULA additional tax (City of LA)</strong><span class=\"row-note\">Effective for transactions closing after June 30, 2026</span>",
         e("4% of total transaction value above $5,400,000 and below $10,900,000; 5.5% at or above $10,900,000. Read as a flat band rate (flagged)."),
         src(data, ["ula"])],
        ["<strong>Selling expenses reduce the amount realized</strong>",
         e("Publication 544, chapter 1, Example 1 subtracts selling expenses before adjusted basis is deducted. Whether seller-paid transfer tax counts as a selling expense is a CPA point (flagged)."),
         src(data, ["irs_544"])],
    ]
    return rows


def _ca_rows(data: dict[str, Any], h: Any, sup: dict[str, Any]) -> list[list[str]]:
    e, src = h.e, h.source_links
    cs = sup["rules"]["ca_schedules_2025"]
    rows = []
    for i in range(9):
        x, y, z = cs["X"][i], cs["Y"][i], cs["Z"][i]

        def band(row: list) -> str:
            lower, upper, base, rate = row
            top = "and over" if upper is None else f"to ${upper:,}"
            return f"{rate * 100:.1f}%: over ${lower:,} {top} (base ${base:,.2f})"

        rows.append([
            f"<strong>Band {i + 1}</strong>",
            e(band(x)),
            e(band(y)),
            e(band(z)),
            src(data, sup["rules"]["ca_schedules_2025"]["source_ids"]),
        ])
    return rows


def build_aftertax(data: dict[str, Any], h: Any) -> str:
    sup = load_supplement()
    e, table, src = h.e, h.table, h.source_links
    rules_table = table(
        "aftertax-rules",
        "Verified rules used by the calculator (each row links to its official page)",
        ["Rule", "Verified value", "Official source"],
        _rule_rows(data, h, sup),
        searchable=False,
    )
    ca_table = table(
        "aftertax-ca",
        "California 2025 tax rate schedules used for the California tax on the gain",
        ["Band", "Schedule X (single, MFS)", "Schedule Y (MFJ, QSS)", "Schedule Z (HOH)", "Official source"],
        _ca_rows(data, h, sup),
        searchable=False,
    )
    rules_json = aftertax_rules_json(sup)

    form = """
<section class="section worksheet" id="aftertax-calc" aria-labelledby="at-heading">
  <div class="ws-head">
    <div>
      <p class="eyebrow">Private browser calculator · blank by design</p>
      <h2 id="at-heading">After-tax net sale proceeds</h2>
      <p class="small muted">Every input starts blank. Nothing is sent, stored or cached: no network request, no cookie, no local storage. Reloading the page clears it. Enter figures from the CPA, the draft purchase agreement and the title company, not estimates. Leave a field blank if you do not have a verified figure; the result then shows what is missing.</p>
    </div>
    <button type="button" class="button button-secondary ws-reset" id="at-clear">Clear inputs</button>
  </div>
  <div class="ws-grid">
    <div class="ws-field"><label for="at-status">Filing status</label>
      <select id="at-status"><option value="">— choose —</option><option value="single">Single</option><option value="mfj">Married filing jointly / qualifying surviving spouse</option><option value="hoh">Head of household</option><option value="mfs">Married filing separately</option></select></div>
    <div class="ws-field"><label for="at-jurisdiction">Location of the property</label>
      <select id="at-jurisdiction"><option value="">— choose —</option><option value="la_city">City of Los Angeles (county + city + ULA)</option><option value="county_only">LA County, outside the City of Los Angeles (county only)</option></select></div>
    <div class="ws-field"><label for="at-seller">Seller pays the documentary transfer tax?</label>
      <select id="at-seller"><option value="">— choose (from the draft agreement) —</option><option value="yes">Yes, seller pays</option><option value="no">No, buyer pays</option></select></div>
    <div class="ws-field"><label for="at-held">Held more than one year?</label>
      <select id="at-held"><option value="">— choose —</option><option value="yes">Yes</option><option value="no">No (short-term: not modeled)</option></select></div>
    <div class="ws-field"><label for="at-price">Sale price (consideration) ($)</label><input id="at-price" type="number" min="0" step="any" placeholder="Enter the contract price"></div>
    <div class="ws-field"><label for="at-selling">Selling costs, excluding transfer tax ($)</label><input id="at-selling" type="number" min="0" step="any" placeholder="Enter 0 if none"></div>
    <div class="ws-field"><label for="at-debt">Debt payoff incl. prepayment charges ($)</label><input id="at-debt" type="number" min="0" step="any" placeholder="Enter 0 if unencumbered"></div>
    <div class="ws-field"><label for="at-basis">Federal adjusted basis at sale ($)</label><input id="at-basis" type="number" min="0" step="any" placeholder="From CPA"></div>
    <div class="ws-field"><label for="at-unrec">Unrecaptured section 1250 gain ($)</label><input id="at-unrec" type="number" min="0" step="any" placeholder="From CPA (enter 0 if none)"></div>
    <div class="ws-field"><label for="at-fedti">Federal taxable income before the sale ($)</label><input id="at-fedti" type="number" min="0" step="any" placeholder="From the return or CPA"></div>
    <div class="ws-field"><label for="at-magi">Federal modified AGI before the sale ($)</label><input id="at-magi" type="number" min="0" step="any" placeholder="From the return or CPA"></div>
    <div class="ws-field"><label for="at-othernii">Other net investment income, inside MAGI ($)</label><input id="at-othernii" type="number" min="0" step="any" placeholder="Enter 0 if none"></div>
    <div class="ws-field"><label for="at-cati">California taxable income before the sale ($)</label><input id="at-cati" type="number" min="0" step="any" placeholder="From Form 540 or CPA"></div>
    <div class="ws-field"><label for="at-cagain">California gain, only if it differs from federal ($)</label><input id="at-cagain" type="number" min="0" step="any" placeholder="Leave blank if the same"></div>
    <div class="ws-field"><label for="at-hold">Hold-case value on the same after-tax basis ($, optional)</label><input id="at-hold" type="number" step="any" placeholder="From your hold model, if you have one"></div>
  </div>
  <div class="ws-outputs" aria-live="polite">
    <div class="ws-card ws-highlight"><div class="metric-label">After-tax net sale proceeds (one number)</div><div class="ws-val" id="at-out-net">—</div><p class="micro muted" id="at-out-note">Enter the required fields above to compute.</p></div>
    <div class="ws-card"><div class="metric-label">Transfer tax (seller side)</div><div class="ws-val" id="at-out-tt">—</div><p class="micro muted" id="at-out-tt-note">County, City and ULA per the verified rules.</p></div>
    <div class="ws-card"><div class="metric-label">Taxable gain</div><div class="ws-val" id="at-out-gain">—</div><p class="micro muted">Amount realized minus adjusted basis.</p></div>
    <div class="ws-card"><div class="metric-label">Federal + NIIT + California tax on the gain</div><div class="ws-val" id="at-out-tax">—</div><p class="micro muted" id="at-out-tax-note">Incremental to the sale; stacking is simplified (see limits).</p></div>
    <div class="ws-card"><div class="metric-label">Net equity before income tax</div><div class="ws-val" id="at-out-pretax">—</div><p class="micro muted">Price less selling costs, transfer tax (if seller pays) and debt payoff.</p></div>
    <div class="ws-card"><div class="metric-label">After-tax sale minus hold-case value</div><div class="ws-val" id="at-out-diff">—</div><p class="micro muted">Shown only if a hold-case value is entered above. The two numbers must be on the same basis.</p></div>
  </div>
  <div id="at-breakdown" class="section small" aria-live="polite"></div>
</section>
"""

    limits = (
        '<section class="section"><div class="section-heading"><div><p class="eyebrow">Limits</p>'
        "<h2>What this module does not compute</h2></div></div>"
        '<ul>'
        "<li>Short-term gain (held one year or less): taxed at ordinary rates, which need the full bracket table. The calculator stops rather than guessing.</li>"
        "<li>Federal stacking is simplified: the long-term gain is layered above taxable income plus the unrecaptured section 1250 amount; the CPA confirms on the Schedule D worksheet (flag flag_4c386ad4_ltcg_stacking).</li>"
        "<li>The 1031 like-kind exchange path (deferral, replacement identification and receipt windows) is a separate decision and is not netted here.</li>"
        "<li>Losses, installment sales, §1245 recapture, AMT, state conformity differences, and the owner's other deductions are not modeled.</li>"
        "<li>Rates and thresholds are the values in the table above. Federal 2026 amounts apply to a 2026 sale; California is the 2025 schedule (flags flag_4c386ad4_fed_year and flag_4c386ad4_ca_schedule_year). Sale-year figures must be re-read before use.</li>"
        "<li>Who pays transfer tax and the ULA reading are open (flags flag_4c386ad4_transfer_tax_payer and flag_4c386ad4_ula_band_reading).</li>"
        "<li>The output is one input to the sell-versus-renew choice, not the choice. Do not treat it as a filing figure.</li>"
        "</ul>"
        '<p class="small">Open items: <a href="flagged.html">Flagged for review</a> · <a href="gates.html">Decision gates</a> · <a href="advisor.html">Advisor one-pager</a></p>'
        "</section>"
    )

    body = (
        '<section class="section"><div class="section-heading"><div><p class="eyebrow">After-tax module (K-4)</p>'
        "<h2>One after-tax number from verified rules</h2>"
        '<p class="lead">Turns the verified federal, California and LA transfer-tax rules into one after-tax net sale figure, so it can be set against the hold case. Only the owner and CPA can supply the inputs; the page supplies none.</p></div></div>'
        + rules_table
        + '<h3>California schedules</h3>'
        + ca_table
        + "</section>"
        + form
        + f'<script type="application/json" id="aftertax-rules">{rules_json}</script>'
        + f'<script src="{AFTERTAX_JS}"></script>'
        + limits
    )
    return h.layout(
        data,
        AFTERTAX_PAGE,
        "After-tax sale module",
        "A private, browser-only calculator: verified tax rules, blank inputs, one after-tax number to compare with the hold case.",
        body,
    )
