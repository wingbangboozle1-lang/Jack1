# Repository line-by-line audit — session `arena/dac604b9-jack1`

Retrieved and reviewed: 2026-11-07 (UTC). Internal research file; **not published on the website**.
Companion: `research/VERIFICATION_DAC604B9.md`.

## 1. Scope and method

Starting point: `809f9e1b43dc52a5e581dcf7665adfb0c10728aa` on `main`, which also equals
`origin/main` at the start of this session. The checkout is shallow/grafted, so local history
alone is not authoritative; remote refs and the GitHub API were used for PR and deployment state.

Audited, file by file:

| Path / set | What it is | Finding for this integration |
| --- | --- | --- |
| `COORDINATION.md` | Shared session board, 348 lines | Contained **raw, unresolved git conflict markers** (`<<<<<<<`, `=======`, `>>>>>>>`) with two complete prior boards on either side. Both sides were preserved verbatim inside labelled HTML comments; a new active board was prepended. No prior session text was discarded. |
| `README.md` | Build description | Describes the seven-page dashboard, privacy posture, local preview command and validator. Needed updating for the consolidated site. |
| `.github/workflows/pages.yml` | "Validate and publish the decision brief" | Runs `python scripts/validate_site.py`, then uploads only `index.html market.html property.html decision.html risks.html flagged.html sources.html`, `assets/styles.css`, `assets/site.js`, `.nojekyll` to `_site`. Any new subpages must be added to that copy list or they will not deploy. |
| `scripts/validate_site.py` | Site gate | Requires those 7 pages, unique IDs, resolvable local paths/fragments, an official-domain allowlist, `target="_blank"` + `rel="noopener noreferrer"`, an official source link in every `tbody` row, and no visible email/phone patterns. It is **not** a complete PII scan. Its `PUBLIC_FILES` list needed extending. |
| `assets/site.js` | Sidebar toggle, Escape/close-on-link, `[data-table-search]` filtering | Retained; new site uses its own `assets/brief.js` with search, filter and sort. |
| `assets/styles.css` | Prior dashboard styling | Retained for preserved prior pages; new site uses `assets/brief.css`. |
| Root published set | `index.html`, `market.html`, `property.html`, `decision.html`, `risks.html`, `flagged.html`, `sources.html` | All external links were on official domains. `tbody` row counts: index 3, market 21, property 22, decision 13, risks 18, flagged 17, sources 20. Blank asset-specific cells were already present in decision/property/flagged. |
| Other root HTML | `404.html`, `economy.html`, `model.html`, `risk.html`, `schools.html`, `tenant.html` | Orphan/earlier-session builds with inconsistent navigation. `model.html` contains non-official assumptions (`3.00%` equity/illiquidity premium, `7.00%`/`6.00%` exit caps, `55%` renewal probability); `risk.html` asserts "~6% exit cost". These are not official values and must not be carried into the consolidated site as data. |
| `pages/`, `site/`, `archive/arena-*/` | Three or more complete prior dashboards | Preserved, not deleted. They are not part of the canonical navigation. |
| `data/records.json` (130 rows, S-83526ad4), `data/facts.json`, `data/model.json`, `data/assumptions.json`, `data/sources.json` | Prior-session datasets | Preserved. Not reused without re-verification; several values conflict with official publishers (see below). |
| `EXECUTIVE_SUMMARY.md`, `DECISION_MEMO.md`, `METHODOLOGY.md`, `RISK_REGISTER.md`, `executive_summary.md`, `analysis/projection_system.md`, `risks/risk_analysis.md` | Prior prose deliverables | Preserved. Prior convergence was "negotiate the renewal now; sell if not signed or credit deteriorates; never ride to expiry unrenewed". Retained only as a qualitative decision rule, re-derived from official sources here. |
| `research/VERIFICATION-LOG.md`, `research/verification-report.md` | Prior verification notes | Preserved. Several claims in them were **not** independently confirmed here (e.g. SCAG 2025 draft `−5%` reversal, NCES `408,026` LAUSD enrollment, assumed cap rates). |
| `docs/SOURCES.md` on PR #14 branch (read via `gh api`, not checked out) | PR #14 source register | Claims 318 rows / 238 verified / 80 unverified / 75 blank / **26 rows with no official publisher at all**. That conflicts with the every-row-official-link acceptance criterion, so PR #14 was not merged as-is. |

## 2. Repo-state findings

1. PR ledger (`gh pr list --state all`): #14, #11, #10, #5 open; #13, #12, #9, #8, #7, #6, #4,
   #3, #2, #1 merged. #14 (`arena/d3fdafdd-jack1`) and #10 (`arena/119c72a5-jack1`) both claim
   broad root-HTML/data scope and had been unchanged for >60 minutes; the handoff is logged on
   the board. Their branches were left untouched.
2. Pages API: `build_type: legacy`, source `main / `, `https_enforced: true`; latest build
   `errored` at `809f9e1` (2026-11-06 13:17:47Z, "Page build failed."). A previous build
   `built` at `716c789`. `fetch_page` on `https://wingbangboozle1-lang.github.io/Jack1/`
   **succeeded** and rendered the current `index.html`, so the site was live even though the
   latest legacy build had errored — two deploy paths were racing (legacy branch build and the
   Actions `deploy-pages` workflow). PR #11 proposes removing one of them.
3. A partial PII regex pass over root HTML found only policy language about "owner name / APN"
   and similar phrases; no actual owner name, address, APN, lease document, personal financial
   figure, personal email or phone number. No full PII scan had been run before this session.
4. Prior pages cite official domains only (top counts: sec.gov 30, census.gov 13,
   finance.lacity.gov 11, zimas.lacity.org 10, planning.lacity.gov 10, irs.gov 8,
   portal.assessor.lacounty.gov 8, scag.ca.gov 7, insurance.ca.gov 6). A domain allowlist alone
   does **not** prove each cited value, hence the line-by-line re-verification.

## 3. Irregularities carried into the published "Flagged for Review" page

Recorded in `data/brief_flags.json` (17 entries IR-D1 … IR-D17) and rendered on `flagged.html`.
The most consequential are:

- **IR-D2** — prior builds labelled BEA's `$818.5 billion` 2024 figure as *GDP*. It is **personal
  income**. The last published real GDP figure located is `$802.0 billion` for 2023 (BEA 24-57).
  BEA also *discontinued* metropolitan-area GDP/personal-income statistics with the 2024 release.
- **IR-D3** — prior notes said the indexed ULA thresholds could not be confirmed officially. The
  LA Office of Finance FAQ now publishes `$5,400,000` / `$10,900,000` for conveyances after
  June 30, 2026. Verified and published here; thresholds are indexed annually.
- **IR-D4** — Census V2025 and CA DOF E-1 disagree on city/county population because of different
  reference dates and methods (e.g. Census county `−3.2%` since 2020 vs DOF county `−0.6%` in
  the year to Jan 1 2026). Both are published separately, never blended.
- **IR-D5** — the BLS 2025 LA city unemployment rate of `5.8%` is an **11-month** average excluding
  October 2025 (appropriations lapse); October 2025 LA CPI-U is likewise unavailable.
- **IR-D6** — the official EDD LA County profile displays "Data for Los Angeles County not
  available" for unemployment, labor force and employment by industry, and substitutes other
  geographies for some series.
- **IR-D7** — official occupational projections end in 2033 and BEA has discontinued MSA statistics;
  neither reaches the 2035 end of the reported lease window. No extrapolation is published.
- **IR-D9** — no government agency publishes net-lease cap rates, transaction comps or tenant
  credit ratings. Those cells are blank, flagged, and never filled from brokerage/aggregator data.
- **IR-D11** — all parcel-level conclusions (zoning, FHSZ, fault zone, flood, school assignment,
  tax rate area) require an address/APN that was not supplied; blank by design for privacy.
- **IR-D12** — multiple prior root builds plus two deploy paths; prior files preserved, canonical
  navigation defined by this build.
- **IR-D13** — Census QuickFacts shows `[X]` (not available) for city-level employer
  establishments, employment, payroll, building permits and firm ownership, while publishing them
  for the county; a city/county comparison silently mixes a missing with a present series.
- **IR-D17** — seven archived pages under `archive/arena-ffc97e4e/` still contained raw git
  conflict markers. The marker lines were converted into neutral HTML comments so both sides
  remain in the files verbatim; the pages are also stamped "superseded" and `noindex`.
- **IR-D16** — privacy scan result: no personal information in the canonical site.

## 4. Disposition

- Prior files: **preserved** (no deletions, no renames of other sessions' work).
- Canonical published set: generated from `data/brief_rows.json` by `tools/build_brief.py`; every
  table row carries at least one official source link; unverifiable values are blank and flagged.
- Verification gate: `tools/verify_brief.py` (dataset + generated HTML + links + PII + build
  artifact), called from CI via `scripts/validate_site.py`.
- This session works only on `arena/dac604b9-jack1` and opens its PR to `main`.
