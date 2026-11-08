# Repository review — 08 November 2026

Session `arena-9707cb4b` · branch `arena/9707cb4b-jack1`
Published summary for the owner: `repo-review.html`.

## 1. Inventory at review time (before this pass)

```
root *.html ................... 15   (8 validated pages + 5 orphan drafts + 404)
archive/arena-972c721e/ ....... 9 html + 4 json + css
archive/arena-d2137d88/ ....... 12 html + js + css
archive/arena-ffc97e4e/ ....... 11 html + 2 js + css  (7 files contain conflict markers)
pages/ ........................ 10 html
site/  ........................ 6 html
data/  ........................ 7 files incl. records.json (130 rows)
research/ ..................... 12 notes + reports
assets/ ....................... 6 style/js files (only styles.css + site.js used by the published set)
```

Navigation on every published page listed the same eight pages; five root pages were unreachable from
navigation, and the deployed host served the entire repository because Pages was building from the
branch rather than from the workflow artifact.

## 2. Findings and disposition

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| RR-01 | High | Landing page asserted metro GDP $1.355T (2024) while its own table showed $1.295T (2023) | corrected after re-reading FRED NGMP31080 |
| RR-02 | High | "#2 county economy in the U.S." with no official ranking source | removed |
| RR-03 | High | County labour rows nine months stale (Dec 2025 vintage vs Sep 2026 published) | refreshed, both vintages retained |
| RR-04 | High | 7 archived files with unresolved conflict markers publicly served | publishing restricted to a file allowlist |
| RR-05 | High | Two deploy paths (branch build + workflow) racing | single workflow path |
| RR-06 | Medium | 5 orphan root pages with superseded figures (incl. a 13×/15× model) | excluded from artifact, documented |
| RR-07 | Medium | 4 overlapping builds | only root dashboard published |
| RR-08 | Medium | 130-row JSON dataset unused by any published page | out of scope; logged |
| RR-09 | Medium | Validator made non-evidence tables impossible (every row needed an official link) | narrow `data-narrative` exemption added |
| RR-10 | Medium | 66 KB coordination board, no active-claim section | structured claim section added |
| RR-11 | Medium | ULA thresholds wrongly treated as unconfirmable | verified against the City FAQ and published |
| RR-12 | Low | README listed 8 pages; 11 now published | updated |
| RR-13 | Low | Lease-expiry range read as a contract date in places | labelled "reported range" everywhere |
| RR-14 | Low | Lookup-tool links could read as completed queries | labelled as lookups |

## 3. Commands used (reproducible)

```sh
# inventory
find . -path ./.git -prune -o -type f -print | wc -l
ls *.html
# orphan detection: nav set vs root page set
python3 - <<'EOF'
import re,glob
nav=set(re.findall(r'href="([a-z0-9-]+\.html)"',open('index.html').read()))
print([p for p in sorted(glob.glob('*.html')) if p not in nav])
EOF
# conflict markers
grep -rn '^<<<<<<<\|^=======$\|^>>>>>>>' --include='*.html' --include='*.md' .
# privacy scan of published pages
grep -EIn '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}|\b\(?\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b' \
  index.html market.html projection.html property.html decision.html risks.html \
  requirements.html repo-review.html flagged.html sources.html audit.html
# structural validation
python3 scripts/validate_site.py
```

Results: 28 files matched the conflict-marker pattern (all under `archive/`), the privacy scan returned
no matches on the published set, and the validator passed with 11 pages / 324 table-body rows after the
changes below.

## 4. Changes made in this pass

1. Three new pages: `projection.html`, `requirements.html`, `repo-review.html`.
2. Navigation normalised to 11 items on every published page, with `aria-current` set per page.
3. `scripts/validate_site.py`: required-page set extended to 11; `dir.ca.gov` and
   `wagesla.lacity.gov` added to the official allowlist; narrative-table exemption implemented so that
   narrative rows must still contain a working link while every evidence row keeps the strict
   official-source rule.
4. `.github/workflows/pages.yml`: the deploy step now assembles all 11 pages plus the two assets.
5. `index.html`: GDP contradiction and ranking removed; 2025 fire-impact card replaces a withheld
   placeholder; ranked course of action and six decision rules added.
6. `market.html`: latest county labour vintage; new "cost of capital, inflation, and wage floors" table.
7. `risks.html`: verified 2025 fire impact, derived annualised earthquake probabilities, and removal of
   unverified acreage claims that had been sitting in a limitation column.
8. `decision.html`: ranked action table, risk-by-decision table, and a recommendation banner that states
   a course rather than deferring.
9. `flagged.html`: three new review items (SCAG vs Census direction conflict; CAL FIRE text
   inconsistency; October 2025 gap in the city series) and a pass note closing two old items.
10. `sources.html` and `audit.html`: new sources and a per-figure re-read ledger for this pass.
11. `README.md`: current page set, single deploy path, and the exclusion list.

## 5. Not done, deliberately

- No file under `archive/`, `pages/`, `site/`, or `data/` was edited or deleted: those belong to other
  sessions and are preserved for traceability.
- The 130-row `data/records.json` dataset was not reconciled with the published pages; consolidation
  would require editing another session's scope and is logged as a request rather than performed.
- The five orphan root drafts were not deleted; they are excluded from the published artifact instead.
