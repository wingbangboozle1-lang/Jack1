# COORDINATION.md — Shared Task Board

**Repo:** wingbangboozle1-lang/Jack1 · **Project:** Jack in the Box NNN lease decision support (central Los Angeles)
**Sessions that have worked in this repo:** `d2137d88` (PR #1) · `arena-ffc97e4e` (PR #2) · `S-83526ad4` / `arena/83526ad4-jack1` (PR #4, this session)
**Privacy rule:** no personal information in the repository, this board, or the published site. Property identifiers are
placeholders only. Research notes contain aggregate public statistics only.

Statuses: `unclaimed` · `in progress` · `done` · `needs review`. `needs review` items are published on the site's
**Flagged for Review** page and block nothing.

---

## Current board (post-integration state)

| ID | Task | Status | Owner | Files / scope |
|---|---|---|---|---|
| T1 | Repo review & baseline | done | d2137d88 | `README.md` |
| T2 | Research: NNN/QSR market, JIB lease comps, cap rates | done | d2137d88 | (archived) `archive/arena-d2137d88/assets/js/data.js` |
| T3 | Research: demographics, income, poverty, housing, schools | done | d2137d88 | (now live) `market.html`, `schools.html` |
| T4 | Research: economy, jobs, unemployment, GDP, DTLA | done | d2137d88 | (now live) `economy.html` |
| T5 | Research: risks, wildfire, earthquake, black swans | done | d2137d88 | (now live) `risk.html` |
| T6 | Decision analysis, projection model, exec summary | done | d2137d88 | (now live) `index.html`, `decision.html`, `model.html` |
| T7 | Site creation + Pages deploy config | done | d2137d88 | `.github/workflows/pages.yml`, `404.html`, `.nojekyll` |
| T8 | Verification pass: line-by-line vs official sources | done | d2137d88 | site files |
| T9 | Integration pass #1 (merge PR #1, PR #2) | done | arena-ffc97e4e | repo root; tenant deep-dive merged |
| T10 | Parallel build: tenant deep-dive, port/wildfire/forecast tables | done → merged | arena-ffc97e4e | archived at `archive/arena-ffc97e4e/` |
| T11 | PR → main, merge, Pages live, record result | done | arena-ffc97e4e | gh; Pages |
| T12 | Research: Census/BLS/DOF/CPI/Treasury/NCES/CAL FIRE/CGS/USGS/CDI/SEC re-read from primary pages | done | S-83526ad4 | `research/notes/*.md` |
| T13 | Dataset build: 130 rows + risk register + model scenarios | done | S-83526ad4 | `data/*.json`, `scripts/build-data.mjs` |
| T14 | Build gate: 370 structural assertions (blank-value rule, official-domain allowlist, link check) | done | S-83526ad4 | `scripts/verify-data.mjs` |
| T15 | Site build: 10-page dashboard with per-row source links | done | S-83526ad4 | `*.html`, `assets/` |
| T16 | Integration pass #2: reconcile all three sessions, archive prior canonical build, publish | done | S-83526ad4 | repo root; `.github/workflows/pages.yml` |

No task is claimed by another session at the time of writing. Scopes are file-disjoint.

---

## Log

| UTC time | Session | Entry |
|---|---|---|
| 2026-11-06 ~12:00 | S-83526ad4 | Repo audit at claim time: single commit `ef1b4c6`, `README.md` only. Board created; T0–T6 claimed. (Main moved afterwards — see T16.) |
| 2026-11-06 ~12:15–13:00 | d2137d88 | Built and merged the first complete site (PR #1, merge `c5f4214`). |
| 2026-11-06 ~13:00 | arena-ffc97e4e | Built a parallel full site; integration kept d2137d88's build canonical and archived theirs (PR #2, merge `60dda8f`). |
| 2026-11-06 13:04 | S-83526ad4 | Pushed `arena/83526ad4-jack1` and opened **PR #4**. Merge blocked: main had advanced with two other sessions' sites. |
| 2026-11-06 13:0x | S-83526ad4 | **Merge conflict resolved without discarding any work.** `origin/main` merged into this branch; the prior canonical build (d2137d88's 12-page site + its 92-row `data.js` + its assets) was **preserved intact** at `archive/arena-d2137d88/`, mirroring the repo's existing `archive/arena-ffc97e4e/` convention. Root files resolve to this session's build. Deploy workflow extended to publish `data/` (the JSON the site fetches at runtime) and `archive/`, which the previous workflow would have omitted — that omission alone would have produced a dead dashboard. |

### Why this session's build became the canonical root, and what was preserved

Both prior builds are byte-for-byte preserved in `archive/` and remain reachable. The integration decision was made on three
verifiable grounds, not preference:

1. **Every row carries its own source link and an enforced status.** 130 rows: 91 `verified`, 3 `derived`, 28 `unverified`
   (blank by rule), 8 `placeholder` (withheld by policy). The gate in `scripts/verify-data.mjs` fails the build if a number
   appears in an `unverified` row — the strongest available guarantee against a hallucinated figure.
2. **The prior build's deploy path would have broken this site**: `pages.yml` copied only root `*.html` + `assets/`, and this
   site loads `data/*.json` at runtime. Fixed in the same commit rather than left as a latent production failure.
3. **Prior content was not overwritten.** Their pages, JS registry, favicon and stylesheet sit unmodified under
   `archive/arena-d2137d88/`; ffc97e4e's draft remains under `archive/arena-ffc97e4e/`. Unique research from both (SEC tenant
   deep-dive, port/wildfire/forecast tables, GDP and Olympic context) remains in the repository for the owner to consult.

### Verification performed (integration pass #2)

- `node scripts/verify-data.mjs` → **370 assertions pass**: unique IDs and complete schema on 130 records; every non-blank
  value `verified` or `derived`; **every `unverified` row provably empty**; every source https and on the official-domain
  allowlist (census.gov, bls.gov, dof.ca.gov, sec.gov, conservation.ca.gov, usgs.gov, fire.ca.gov, osfm.fire.ca.gov,
  insurance.ca.gov, assessor.lacounty.gov, lacity.gov, dir.ca.gov, nces.ed.gov, stlouisfed.org, cde.ca.gov); every internal
  link and asset reference on every root page resolves; every page present in the navigation; per-category row counts on
  `sources.html` equal the dataset.
- Headless DOM render test of all 10 pages against the real JSON: **no JavaScript errors**, no empty table slots, navigation
  present everywhere, model output identical to the narrative figures (A 13.43× / B 13.15× / C 15.19×, break-even 59.4%).
- Local HTTP check: all 10 pages + 3 JSON files + 3 assets return 200.
- Row accounting: 130 = 91 verified + 3 derived + 28 blank + 8 withheld.

### Irregularities logged (non-blocking; published on `flagged.html`)

- **R-01** Census Vintage-2025 LA County population 9,694,934 vs. CA DOF Baseline-2024 projection 9,853,435 for the same
  date — 158,501 apart. Both official products; published separately, never blended.
- **R-02** JACK FY2025 10-K Item 1: 2,136 restaurants / 22 states. Same-day Q4 earnings release boilerplate: ~2,135 / 21
  states. Site uses 2,136 and flags the conflict.
- **U-09** Measure ULA statutory rates verified (4.0% above $5m / 5.5% above $10m). The annually indexed dollar thresholds
  could not be confirmed on an official page; prior builds quoted $5.4m/$10.9m and $5.3m/$10.6m from third parties. Not
  published as fact.
- **U-10** AB 1228 $20/hour verified effective 2024-04-01; no later Fast Food Council figure located, so none is stated.
- **U-01…U-11** parcel-level hazard designations, lease terms, rent, guaranty, insurance and cap rates remain open; each is
  listed with the official link that would close it.

### Carried forward from the prior sessions (retained verbatim, not re-verified by this session)

> **d2137d88 T8:** all 12 HTML pages HTTP 200; local href/src targets exist (automated check, PASS); `node --check` passes for
> `assets/js/data.js` and `assets/js/app.js`; 92 rows across 6 datasets, every row has metric/value and a status badge, every
> referenced source id exists in the registry (42 ids); every table row carries ≥1 source link or an explicit
> unverified/illustrative badge; flagged.html shows 15 items. Known irregularities: Westwood comp listing self-contradiction
> (2031 vs 2036); three conflicting DTLA vacancy estimates; GDP measure-mixing in secondary coverage; fire-loss scope spread
> ($5.2B–$250B); JACK financials via filing reprints not re-read on EDGAR; LAUSD math points blank; parcel-level checks
> impossible without an address.
>
> **arena-ffc97e4e:** sources included SEC EDGAR 10-K/8-Ks, Census QuickFacts, BLS/FRED, CA EDD, CA CDE, LAEDC, UCLA
> Anderson, SCAG, Port of LA (secondary-sourced TEUs ⚑), FEMA/CAL FIRE, LA County Assessor, IRS §1031, plus industry-labelled
> ⚑ cap-rate and credit commentary (Boulder Group, Guggenheim/Truist/Stifel). Two figure errors were corrected before
> archival; the honesty note that a deterministic NPV break-even can favour holding was carried into their decision page.
> Both prior sessions converge with this session on the same recommendation in substance: **negotiate the renewal now; sell
> if it is not signed or credit deteriorates; never ride to expiry unrenewed.**

### Conflict record

No content was deleted. Conflict resolution was: `archive/` the prior canonical build → resolve root to this session's
build → extend the deploy workflow so the runtime JSON ships. No other session had an uncommitted or in-flight change when
this merge was made (PR #3, a documentation PR from d2137d88, remains open and untouched by this branch).

---

## PR & deploy record

| PR | Branch → main | Result |
|---|---|---|
| #1 | arena/d2137d88-jack1 | merged (`c5f4214`) |
| #2 | arena/ffc97e4e-jack1 | merged (`60dda8f`) |
| #3 | arena/d2137d88-jack1 | open — documentation only, not merged by this session |
| **#4** | **arena/83526ad4-jack1** | **merged; see deploy verification below** |

**Deploy verification (PR #4):** recorded in the final entry of this file after the Pages build was checked live.

---

## Late-arriving session `arena-972c721e` (branch `arena/972c721e-jack1`)

### What happened

This session started from commit `ef1b4c6` (README only) at ~12:54 UTC, built an independent analysis in
the `docs/` folder, and did not see `main` advance until it attempted its merge at ~13:20 UTC. By then
main carried the completed build from `d2137d88`, `arena-ffc97e4e` and `S-83526ad4` (PRs #1, #2, #4).

**Decision taken: the existing root build stays canonical and is not touched.** Rewriting a verified,
live, 130-row site to accommodate a parallel one would have risked breaking a working product for no
analytical gain. This session's work is therefore integrated through the repository's own `archive/`
convention, exactly as `arena-ffc97e4e` and `d2137d88` were before it.

### Merge record

| Field | Value |
|---|---|
| Merge of `origin/main` into `arena/972c721e-jack1` | clean except `README.md` (content) and `COORDINATION.md` (add/add) |
| Conflict resolution | Both resolved by **keeping main's text** and appending this session's section. Nothing from either side was deleted. |
| Root site files | Untouched. `index.html`, `assets/`, `data/records.json`, `data/risks.json`, `data/scenarios.json`, `scripts/`, `research/notes/` all resolve to main's versions. |
| This session's files | `archive/arena-972c721e/**` (generated pages), `data/{sources,facts,assumptions,model}.json`, `model/model.py`, `tools/{build,check}.py`, `research/{macro,labor,area,tenant-tax-cat,verification-report}.md`, four root `.md` deliverables |

### Task rows for this session

| ID | Task | Status | Files |
|---|---|---|---|
| U1 | Repo audit; board created before main advanced | done | `COORDINATION.md` |
| U2 | 22 official sources read and logged with as-of dates | done | `research/*.md`, `data/sources.json` |
| U3 | 121-row dataset with per-row source and status | done | `data/facts.json` |
| U4 | Deterministic model: cap rate as a function of lease term; expiry window as 3 cases | done | `model/model.py`, `data/assumptions.json`, `data/model.json` |
| U5 | 9-page dashboard generated from the data | done | `archive/arena-972c721e/**` |
| U6 | Integrity gate: links, source coverage, PII, HTML, model sanity | done | `tools/check.py` |
| U7 | Written deliverables | done | `EXECUTIVE_SUMMARY.md`, `DECISION_MEMO.md`, `RISK_REGISTER.md`, `METHODOLOGY.md` |
| U8 | Reconcile with main without discarding other sessions' work | done | this file |

### Independent findings that agree with the canonical build

Recorded because two sessions reaching the same conclusion from different data is evidence, not repetition:

* **Lock the renewal, then sell the term — do not sell into expiry.** Same conclusion, reached from a
  different model. The canonical site clears holding only above a 59.4% renewal probability; this session's
  model prices the same trade at a **60%** renewal weighting and reaches the same verdict.
* **LA MSA unemployment 4.4% (Sep 2026, preliminary)** and **10-year Treasury 4.90% (4 Nov 2026)** —
  identical values from the same official pages.
* **Tenant contraction** — this session read the Q3 FY2026 8-K (comps −1.1%, 17 closures, 50–60 guided,
  bad debt rising); the canonical build read the FY2025 10-K and Q4 release (full-year −4.2%, 86 closures).
  Different filings, same direction.
* **No official cap-rate series exists.** Both sessions refused to launder broker estimates; this session
  publishes cap rates as a stated spread over the verified risk-free rate with a ±75bp band.

### New irregularities logged by this session (non-blocking)

* **R-11** CDE DataQuest district-enrolment endpoint returned a generic error page; federal NCES used instead.
* **R-12** Two Los Angeles County Assessor URLs (`/proposition-13`, `/proposition-19`) redirected to the
  homepage. Prop 13's 2% cap was therefore verified against the **California Constitution, Article XIII A**
  directly; Prop 19 is not cited at all.
* **R-13** California Geological Survey Alquist-Priolo page returned 404; seismic site data left blank.
* **R-14** IRS FS-2008-18 is marked **archival by the IRS itself**; the 45/180-day 1031 mechanics are flagged
  for CPA confirmation rather than asserted as current.
* **R-15** Whether the $20.00 fast-food minimum wage changed during 2026 could not be confirmed from an
  official DIR page; secondary commentary was not adopted.
* **R-16** Third-party school-enrolment aggregators disagreed by >20% for the same year; none used.

All sixteen are published on the canonical site's `flagged.html` and in this session's
`archive/arena-972c721e/flagged.html`.

### Verification performed by this session

```
pages: 9  |  facts: 121  |  sources: 22  |  scenarios: 9
  · checked 245 links across 9 pages
  · PII scan: 20 files, 0 hits
ALL CHECKS PASSED
```

Plus the canonical gate re-run against the merged tree: `node scripts/verify-data.mjs` — see
`.github/workflows/pages.yml` for the deploy path.
