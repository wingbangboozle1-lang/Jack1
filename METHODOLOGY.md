# Methodology

## The rule this project runs on

Every value is one of four things, and the site says which:

| Badge | Meaning |
|---|---|
| `verified` | Read from an official government, legislative or SEC page, with the URL recorded and the page's own as-of date noted |
| `derived` | Arithmetic on verified figures, with the arithmetic shown |
| `flagged` | Could not be confirmed. Published **blank**, with a note saying what would fill it |
| `industry` | Non-government. Kept in a separate table, never mixed with verified rows. Currently empty. |

Nothing is estimated. Nothing is inferred from a similar property. A missing value stays missing —
that is why 12 rows on this site are blank.

## Collection

22 sources were opened and read on 2026-11-06. Each is in `data/sources.json` with:

* the exact URL,
* the publisher,
* the data as-of date as printed on the page,
* a note recording what was actually seen — including qualifying language ("preliminary", "pending",
  "archival", "most of which will be franchise restaurants").

Where a page was paginated or split (the US Treasury par-yield table renders 25 rows at a time), the
underlying official series was taken from its authoritative release (the Fed's H.15) rather than
scraping a truncated view.

## Verification

`research/` holds the working logs: every figure transcribed with its source and vintage. The
machine-readable equivalent is `data/facts.json` — 121 rows, each with an ID, a source list and a status.

`tools/check.py` enforces, on every build:

1. every internal link resolves, including anchors;
2. every verified or derived row carries at least one source ID, and every source ID exists in the ledger;
3. every unverified row is blank or `[WITHHELD]`;
4. no personal information patterns appear in any page, data file, asset or document;
5. HTML structure is valid: exactly one `<h1>`, balanced tags, no external asset requests;
6. no placeholder tokens;
7. model sanity: all five strategies present in all nine scenarios, net proceeds never exceed gross price,
   no negative tax.

## Modelling

The model is deterministic — no randomness, no Monte Carlo, no black box. Run `python3 model/model.py`
and every number on the Valuation page reproduces.

Two structural choices matter:

* **Cap rate is a function of lease term, not a constant.** 7.25% at ≤3 years, 6.50% at 5 years, 6.00% at
  9+ years, linearly interpolated. This is what makes the "term is the price" finding visible rather than
  asserted.
* **The expiry window is treated as three assets, not one.** 2030, 2032 and 2035 are modelled separately,
  because a five-year uncertainty in remaining term is a five-year uncertainty in value.

Every assumption is published with a stated basis in `data/assumptions.json` and rendered on the
Valuation page. Verified inputs (risk-free rate, inflation, transfer taxes, ULA tiers, Prop 13 cap) are
separated from assumptions (`A1`–`A16`) in both the data and the display.

**NPV** is measured against a sell-today baseline at a 7.40% required return, so zero means "no better or
worse than selling now". **Wealth 2035** reinvests every dollar received at the moment it is received at
the verified 4.90% Treasury yield, so strategies with different cash-flow timing are compared like for
like. **IRR** is computed by bisection on the same flows.

Strategy C is probability-weighted: 60% renewal, 40% vacancy, with the band (35–75%) published so the
reader can re-price it. That weighting exists precisely so the "do nothing" path is not flattered by
assuming the good outcome.

## Privacy

The subject property is `SP-01` everywhere. No address, parcel number, owner name, rent, NOI, tenant
identity or contact detail exists in this repository or in any published page. The PII scanner in
`tools/check.py` enforces that on every build across the site, the data, the assets and the documents.

The published site requests nothing from third parties — no fonts, analytics, CDN or trackers. The
valuation calculator is inline JavaScript; nothing typed into it leaves the browser.

## Limitations

* City-, county- and metro-level data cannot substitute for a trade-area analysis. The address would
  change the granularity; it is withheld by requirement.
* Cap rates, retail rents and property-specific credit are assumptions, not observations. No official
  series exists for the first two, and the third is private.
* The risk-weighting in the decision matrix is analyst judgement. The weights and every cell are
  published so it can be challenged cell by cell.
* This is analysis, not legal, tax or investment advice.
