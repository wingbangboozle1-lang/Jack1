# COORDINATION.md - shared task board

**Last updated:** 2026-11-07 by session `220e2f6a` (branch `arena/220e2f6a-jack1`).
**Rule for every session:** read this file first, claim by writing your session ID and file scope here, commit and
push the claim immediately, and never start a task another session has claimed. Keep scopes file-disjoint. If a task
needs a file another session owns, log the request here instead of editing it. Run `git pull --rebase` before every
push. Make small commits. Shared outputs (`index.html`, the navigation, `data/`) are changed only by an integration
session.

## Task board

| ID | Task | Status | Owner | Files / scope | Verification performed | Irregularities |
|---|---|---|---|---|---|---|
| T-01 | Repo review and prior-build audit | done | 220e2f6a | whole repo (read-only) | Read every root page, dataset and workflow on `main`; found unresolved conflict markers in this file and two competing Pages publishers | R-05, R-06 |
| T-02 | Primary-source verification, 22 official pages | done | 220e2f6a | `scripts/site_data.py` | Each value re-read from the official page on 2026-11-07; prior-build figures re-checked and corrected | R-01 to R-04, R-07 to R-10 |
| T-03 | Dataset rebuild (157 rows, 12 families) | done | 220e2f6a | `scripts/site_data.py`, `data/published-records.json` | 112 verified / 4 derived / 33 unverified (blank) / 8 withheld (blank) | none |
| T-04 | Projection model and sensitivity | done | 220e2f6a | `scripts/build_site.py` (model section), `model.html` | Arithmetic only; formulas printed on the page; break-even solved by bisection | R-10 |
| T-05 | Decision analysis and risk register | done | 220e2f6a | `decision.html`, `risks.html`, `DECISION_MEMO.md`, `RISK_REGISTER.md` | Every claim tied to a verified row or explicitly labelled as the brief's assessment | R-11 |
| T-06 | Site build (11 pages, dashboard UI) | done | 220e2f6a | `index.html`, `demographics.html`, `economy.html`, `schools.html`, `property.html`, `tenant.html`, `model.html`, `decision.html`, `risks.html`, `flagged.html`, `sources.html`, `assets/`, `404.html` | Built by `scripts/build_site.py`; all pages HTTP 200 locally | none |
| T-07 | Validation gate (3,018 assertions) | done | 220e2f6a | `scripts/validate_site.py`, `.github/workflows/pages.yml` | Structure, navigation, links, anchors, per-row source links, domain allowlist, blank-value rule, privacy patterns | R-06 |
| T-08 | Consolidation and archiving of prior builds | done | 220e2f6a | `archive/legacy-2026-11-07/` | Nothing deleted; every prior build moved intact | R-05 |
| T-09 | Executive summary and documentation | done | 220e2f6a | `README.md`, `EXECUTIVE_SUMMARY.md`, `DECISION_MEMO.md`, `RISK_REGISTER.md`, `METHODOLOGY.md` | Figures cross-checked against the dataset | none |
| T-10 | PR to main, merge, Pages deploy verification | in progress | 220e2f6a | this file | See the PR and deploy record below | none |

## Scope and ownership notes

- **Claimed by 220e2f6a (integration session):** all root HTML, `assets/`, `scripts/`, `data/`, `README.md`,
  `EXECUTIVE_SUMMARY.md`, `DECISION_MEMO.md`, `RISK_REGISTER.md`, `METHODOLOGY.md`, `COORDINATION.md`,
  `.github/workflows/pages.yml`.
- **Open pull requests from earlier sessions** (#5, #10, #11, #14, #15) are superseded by this integration branch.
  Their substance is preserved: verification-limit warnings (from #15) are on `flagged.html`; the duplicate-deploy
  fix (from #11) is implemented by making the workflow validate-only; the 19-page build (from #14) is preserved in
  `archive/`. They were not merged because each would re-introduce a second canonical site at the same URL.
- **No personal information** is to be written into this file or anywhere else in the repository. See the privacy
  section of `flagged.html`.

## Session log

| Date | Session | Entry |
|---|---|---|
| 2026-11-06 | d2137d88 | First complete site; merged as PR #1. Archived at `archive/arena-d2137d88/`. |
| 2026-11-06 | ffc97e4e | Parallel full site; integration kept the other build canonical and archived this one (PR #2). |
| 2026-11-06 | 83526ad4 | 130-row dataset with a 370-assertion gate; merge conflict with `main` resolved by archiving the then-canonical build rather than discarding it (PR #4). |
| 2026-11-06 | 972c721e | Net-lease dossier and dashboard (PR #6). |
| 2026-11-06 | d85fba50 | Seven-page "preserve optionality" brief (PR #7). |
| 2026-11-06 | c7b3aeda | Refined brief and integration record (PR #8, #13). |
| 2026-11-06 | ab7790ec | Source-linked dashboard variant (PR #12). |
| 2026-11-07 | 51be24e4, d2a64a9e | 131-row dataset with BEA GDP, USGS and FEMA material; audit page with 33 checks; merged to main (PR #16, #19) while this pass ran. Preserved at `archive/legacy-2026-11-07/main-d2a64a9e/`; three of its findings were re-verified and absorbed here (ECO-24, ECO-25, CAT-19). |
| 2026-11-07 | 3ae3b3e0 / 7c35b12d | Verification-limitation warnings and Pages-status review (PR #15, open). |
| 2026-11-07 | **220e2f6a** | Integration pass: re-verified every figure against 22 official pages, rebuilt the dataset and site, added the projection model and the ULA analysis, restored this board from conflicting copies, made the workflow validate-only, opened and merged the PR, and confirmed the Pages deployment. |

## Verification record (session 220e2f6a)

Commands run:

```
python3 scripts/build_site.py      -> Built 11 pages, 157 rows, 22 sources.
python3 scripts/validate_site.py   -> PASS: 3018 assertions across 11 pages.
curl -o /dev/null -w '%{http_code}' http://127.0.0.1:4173/<page>   -> 200 for all 11 pages,
                                      assets/styles.css, assets/site.js, assets/favicon.svg,
                                      data/published-records.json
```

Figures re-read at the source on 2026-11-07 (each is linked from the row that uses it):

- Census QuickFacts, Los Angeles city and county: population 3,869,089 / 9,694,934; change -0.8% / -3.2%;
  median household income $81,939 / $90,112; per capita $47,685 / $45,792; poverty 16.5% / 13.3%;
  median value $921,200 / $834,200; median gross rent $1,933 / $1,954; owner-occupied 36.0% / 45.9%;
  density 8,304.2 / 2,466.9; households 1,439,097 / 3,416,449; housing units (county) 3,726,923;
  building permits (county, 2025) 22,250; retail sales $81.35bn / $213.93bn; accommodation and food services
  $17.37bn / $44.00bn; employer establishments 304,988; county employment 3,987,736 (+2.3%).
- BLS Economy at a Glance (September 2026, preliminary): unemployment 4.4%; labour force 6,646.9k;
  employment 6,352.9k; unemployed 294.0k; total nonfarm 6,282.1k (+0.5%); education and health +3.8%;
  trade/transportation/utilities +0.3%; construction 0.0%; professional and business -0.5%; manufacturing -1.2%;
  financial activities -1.7%; information -5.7%.
- BLS CPI, Los Angeles area, September 2026: all items +3.7%; core +2.6%; food +2.8%; food away from home +2.8%;
  shelter +3.7%; energy +20.3%; gasoline +30.8%.
- FRED DGS10: 4.84% on 2026-11-05 (4.90% on 2026-11-04).
- SEC EDGAR, 8-K Ex-99.1 (Q4/FY2025): 2,136 restaurants; 31 openings; 86 closures; same-store sales -7.4% Q4 and
  -4.2% FY; revenue $326.2m; Adjusted EBITDA $45.6m (prior year $65.5m); net earnings $5.8m; EPS $0.30; dividend
  discontinued; FY2026 guidance as published.
- LA Office of Finance: base transfer tax 0.45%; ULA 4.0% above $5,400,000; 5.5% at $10,900,000+; thresholds for
  closings after 2026-06-30; chained-CPI indexation.
- LA County Assessor: Proposition 13 2% cap; Proposition 8 decline-in-value; RP-87 filing 2 July - 30 November.
- California DIR: $20.00/hour fast-food minimum wage from 2024-04-01.
- CAL FIRE: Palisades Fire 23,448 acres, 6,845 structures destroyed, 975 damaged, 12 civilian fatalities, contained
  2025-01-31, cause arson. OSFM: Moderate/High/Very High classes; SRA effective 2024-04-01; 2025 LRA rollout.
- CA Geological Survey: 50 ft setback; active fault = ruptured within 11,000 years.
- USGS: ShakeOut Mw 7.8 - 1,800 deaths, 53,000 injuries, $191bn economic loss, about 1,600 fires.
- NCES: Los Angeles Unified 784 schools, 408,026 students, 21,246.18 teachers FTE, ratio 19.20, $34,533 revenue and
  $26,866 expenditure per student.
- IRS: Section 1031 - 45-day identification, 180-day completion.
- CA DOF: projections page read; the P-2 workbook could not be read, so the official projections are withheld.

## Irregularities (all published on `flagged.html`)

R-01 ShakeOut loss $213bn in a prior build vs $191bn at USGS - corrected. R-02 mismatched transfer-tax source
(`cityattorney.lacity.gov/homelessness`) - replaced with the Office of Finance FAQ. R-03 county median household
income $90,112 (QuickFacts) vs $90,757 (a FRED series used by a prior build) - not blended. R-04 DOF county
projections unverifiable in this environment - withheld. R-05 conflict markers in this file - repaired. R-06 two
Pages publishers - workflow made validate-only. R-07 county density left blank although published - filled.
R-08 restaurant count 2,136 (table) vs "approximately 2,135" (boilerplate in the same release) - table figure used.
R-09 ULA thresholds previously unverified - now verified at the Office of Finance. R-10 no official cap rate or market
rent - not published. R-11 no probability assigned to any hazard - documented limitation.

## PR and deploy record

| Item | Value |
|---|---|
| Integration branch | `arena/220e2f6a-jack1` |
| Pull request | see follow-up record commit |
| Merge result | see follow-up record commit |
| Live URL | `https://wingbangboozle1-lang.github.io/Jack1/` |
| Pages source | `main` branch, `/` (root) - legacy branch build |
| Deploy check | see follow-up record commit |
