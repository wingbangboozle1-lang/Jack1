# Jack1 — Central Los Angeles Jack in the Box NNN Asset: Decision File

**Live site:** <https://wingbangboozle1-lang.github.io/Jack1/>

A single-tenant Jack in the Box freehold — ground and building — in the central Los Angeles
trade area, leased triple-net, with the lease expiring somewhere in the window **2030 to 2035**.
This repository answers one question: **sell before expiry, or renew and hold**, balancing wealth
preservation, growth opportunity and manageable risk.

## The recommendation

**Hold and secure the term now, with a hard, pre-committed sell trigger. Do not sell immediately.
Do not wait passively for 2030–2035.**

Approach the tenant within twelve months and convert the ambiguous 2030–2035 window into a
signed, longer firm term. If an extension is granted, hold. If the tenant refuses, or discloses a
franchise agreement expiring at or before the lease expiry, sell immediately — while four to nine
years of firm term still remain.

The binding risk is not the Los Angeles economy. It is the tenant's own contraction programme:
Jack in the Box Inc. announced on 23 April 2025 that approximately 150–200 underperforming
restaurants would close, and that the remaining locations would close **based on their respective
franchise agreement termination dates**. A 2030–2035 expiry sits inside that scheduled window.

Full reasoning, all evidence rows and the reproducible model are on the
[Decision](https://wingbangboozle1-lang.github.io/Jack1/decisions.html) and
[Projection](https://wingbangboozle1-lang.github.io/Jack1/projection.html) pages, and in
[`docs/executive-summary.md`](docs/executive-summary.md).

## Verification standard

**Every table row carries a link to an official publisher** — a United States federal statistical
or regulatory agency, the U.S. Treasury, a Federal Reserve Bank republishing a federal series, a
State of California agency, Los Angeles County, the City of Los Angeles, a federally designated
regional planning agency, or a document filed with the U.S. Securities and Exchange Commission.

**If a value could not be confirmed from an official source, the value cell is left blank.** It is
never filled from memory, never inferred from a neighbouring geography, and never taken from a
news article, brokerage, rating agency, data aggregator or wiki. Each blank is registered on the
[Flagged for Review](https://wingbangboozle1-lang.github.io/Jack1/flagged.html) page with the
official route to close it.

Where a figure was seen only in a non-official source it is quarantined in a separate `reported`
field, rendered under an explicit *not used* marker, and excluded from the model and from the
recommendation. Publishing what was declined is more useful than silence.

Two quantities are stated nowhere on this site because **no official government publisher exists**
for them: net-lease capitalisation rates and credit ratings. Cap rate enters the projection model
only as a labelled, flagged sensitivity spread over the official U.S. Treasury par yield.

| Coverage | Count |
| --- | --- |
| Table rows published | 318 |
| Verified from an official source | 238 (74.8%) |
| Left blank and flagged | 75 |
| No official publisher exists | 26 |
| Distinct official URLs cited | 79 across 20 publishers |
| Open flags (non-blocking) | 33 |
| Irregularities in the official record | 9 |

Counts are generated, not asserted — run `python3 tools/collect_sources.py`.

## Privacy

Privacy is the highest-priority constraint. The subject property is **anonymised**. Not published
anywhere on the site, and not stored in the underlying data files either: the street address,
cross streets or parcel number; the owner's name, entity structure or contact details; the
purchase price, basis or holding period; the contract rent, net operating income or market value;
site-level tenant or franchisee identity; and the insurance carrier, limits or premium.

The consequence is stated plainly rather than worked around: every parcel-specific analysis is
impossible, so traffic counts, assigned schools, zoning, flood zone, fire hazard severity zone,
earthquake fault zone, Tax Rate Area and assessed value are all left blank, flagged, and paired
with the official lookup tool a reader would use. The recommendation is therefore a decision tree
whose branches are resolved by facts the owner can obtain — not a single instruction pretending
those facts are known.

`tools/check_links.py` enforces this mechanically: the build fails if any rendered page or data
file matches a street-address pattern, a Los Angeles County Assessor parcel-number pattern, or any
token on the forbidden list.

## Repository layout

| Path | Contents |
| --- | --- |
| `*.html` (19 pages) | The published site. Plain static HTML with inline CSS, no JavaScript, no external assets, no network calls. Renders identically on GitHub Pages and offline. |
| `data/*.json` | The single source of truth. Every table on every page is rendered from these files. |
| `tools/model.py` | The projection system. Reads `data/projection.json`, writes `data/projection_output.json`. |
| `tools/collect_sources.py` | Walks every row and builds `data/sources.json` and `docs/SOURCES.md`. |
| `tools/audit_repo.py` | Inspects the working tree and git object store to generate `docs/repo-audit.md`. |
| `tools/build_site.py` | Renders all 19 pages from `data/*.json` and `docs/*.md`. |
| `tools/check_links.py` | Build gate. Links, source integrity, official-host allowlist, privacy patterns. Exits non-zero if the site must not be published. |
| `docs/executive-summary.md` | The executive summary (also rendered as a page). |
| `docs/methodology.md` | Verification standard, privacy protocol, geography and vintage discipline, model design. |
| `docs/repo-audit.md` | Line-by-line repository audit, data-layer rule audit, flag audit, coordination audit. |
| `docs/SOURCES.md` | Generated citation register. |
| `COORDINATION.md` | Parallel-session task board, session registry, conflict log, verification policy. |
| `.nojekyll` | Serves the site as-is; no Jekyll processing. |

## Reproducing the site

```
python3 tools/model.py            # data/projection.json -> data/projection_output.json
python3 tools/collect_sources.py  # every data/*.json row -> data/sources.json + docs/SOURCES.md
python3 tools/audit_repo.py       # repository state -> docs/repo-audit.md
python3 tools/build_site.py       # data/*.json -> all 19 HTML pages
python3 tools/check_links.py      # gate: exit 0 = publishable
```

Standard library only. No dependencies, no build toolchain, no network access required.

To preview locally:

```
python3 -m http.server 8080 --bind 0.0.0.0
```

## Data row schema

Identical in every data file, and documented in each file's `meta` block.

| Key | Meaning | Rule |
| --- | --- | --- |
| `id` | Row identifier, prefixed by category | Stable; referenced across pages |
| `m` | Metric, with its geography stated explicitly | City, county, metropolitan statistical area and metropolitan division are four different official geographies and are never conflated |
| `v` | Verified value | Empty string means left blank. A blank is never filled by inference |
| `p` | Period or vintage | Mandatory. A number without a vintage is not published |
| `s` | Official publisher, named in full | Government agency, regulator, central bank, regional planning agency, or SEC filing |
| `u` | Official URL for manual review | Mandatory for every verified row; the gate fails otherwise |
| `k` | Verified `true` / `false` | `true` only if read from the official publisher during this session |
| `n` | Note, derivation, or reason for the gap | Carries the flag identifier where one applies |
| `r` | Value reported by a **non-official** source | Never used as a verified value and never used as a model input |

## Not advice

This is an analytical research file, not legal advice, tax advice, an appraisal, or a securities
recommendation. All sources retrieved **2026-11-06**.
