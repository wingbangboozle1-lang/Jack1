# Verification log — line-by-line pass

**Retrieved:** 2026-11-06 · **Method:** every figure was read directly from the issuing agency's page
(or from the official machine-readable endpoint) during this session. Nothing was carried from memory.
The generated pages are re-checked mechanically by `tools/check_site.py`, which fails the build on any
unlinked value, broken internal link, unknown source id, or privacy leak.

## Mechanical checks (last run: pass)
| Check | Result |
|---|---|
| Required pages present | 12 / 12 |
| Internal links and asset paths resolve | pass |
| Every source id used on a page is defined | pass (32 sources) |
| Every defined source is referenced somewhere | pass |
| Fact-table rows with a value have a source | 113 rows, pass |
| `P` (principal-supplied) marker confined to the deal-terms table | pass |
| All source URLs https and on a recognised host | pass |
| Privacy scan: street address / APN / email / phone | 0 hits across 12 pages |
| Navigation complete on every page | pass |

## Row-level verification notes

| Table | Rows | Verified against | Notes |
|---|---|---|---|
| T01 Property & lease | 10 | no official source can exist (deal terms are withheld) | all marked `principal-supplied`; exact dates/prices flagged F-01/F-02 |
| T02 LA city demographics | 22 | Census QuickFacts (S05) | two rows ("Building permits 2025", "employer establishments 2023") left **blank** because the Census table itself shows `X` |
| T03 LA county demographics | 21 | Census QuickFacts (S06), SAIPE via FRED (S04) | all populated |
| T04 Labour market | 12 | FRED/BLS (S01, S03), QuickFacts (S06), CAUR (S32) | NSA vs SA series kept strictly separate (S02 vs S03) |
| T05 Prices, rates, credit | 13 | FRED (S07–S11) | derived percentages are marked "(derived)" and recomputed from the published index values |
| T06 Tenant credit | 12 | SEC XBRL company-concept API (S15, S16) and the filed 8-K text (S17) | rating row left **blank** (F-06) |
| T07 Market pricing | 7 | third-party only (S28–S31) | labelled non-official on the page |
| T08 Tax & rules | 17 | BOE (S20, S21), City of LA Office of Finance (S23), LegInfo (S19), IRS (S24), CAL FIRE (S25), CGS (S26), LAC Assessor (S27) | rule text quoted, not paraphrased into numbers |

## Errors found and corrected during the pass (recorded for audit)

1. **`LAPOP` misread as Los Angeles population.** The FRED series named `LAPOP` is *Resident Population in
   Louisiana* (confirmed from its own metadata page). Discarded; Los Angeles population is taken from Census
   QuickFacts instead. Logged as Flagged **F-11** so future sessions do not repeat it.
2. **FY2023 revenue mistyped** as `1,692,851,000`. The SEC XBRL value for the FY ended 2023-10-01 is
   **`1,692,306,000`**. Corrected in `data/series.json`.
3. **FY2023 net income assumed to be a loss.** It is a **profit of `$130,826,000`**; the losses are FY2024
   (`−$36,695,000`) and FY2025 (`−$80,719,000`). This changed the narrative in R01 and on the Tenant Credit
   page; both were rewritten to "moved from profit to loss".
4. **Model normalisation bug.** Year-0 value indices initially read 20.37 instead of 1.00 (base leaked into the
   ratio). Fixed so every path is 1.000 at 2026 and the arithmetic is `(base ÷ cap) × rent multiple × decay`.
5. **`S34` citation.** A source id was used in a draft table that did not exist; replaced with a properly
   defined `S32` (FRED `CAUR`, California unemployment).
6. **Rendered stray pipe characters** (`S07|`) leaked from a builder convenience marker. Stripped in `table()`.

## Source contradictions logged rather than resolved by guesswork

- A Los Angeles JIB broker flyer (S30) states two different lease-expiry years in the same document
  (2036 in the header, 2031 in the highlights). Only its asking cap rate is used. Flagged **F-04**.
- Two Los Angeles cap rates (4.31% absolute-NNN ~15 yr vs 5.82% ground lease ~13 yr) are **not like-for-like**
  and are reported separately, never averaged. Flagged **F-05**.
- The Net Lease Advisor page (S28) lists S&P and Moody's ratings as `N/A`; no rating is asserted. Flagged **F-06**.

## Not verified, therefore not published anywhere
Exact lease dates and rent · in-place NOI · sale/appraised value · parcel FHSZ classification ·
parcel Alquist-Priolo classification · insurance premium · issuer credit rating · store-level AUV ·
forward county population projection · city-level building permits and business counts.
Every one of these appears on **Flagged for Review** with a resolution path.
