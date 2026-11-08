# Verification audit — session b8188ee0 (08 Nov 2026)

Scope: fresh line-by-line re-verification of every published figure on the eight canonical pages, integration of newly readable official data, correction of the landing-page GDP contradiction, and autonomous PR → merge → deploy.

Method: every source below was opened with the research fetch tool on 2026-11-08 (UTC). Values were compared against the published HTML cell-for-cell. No value was inferred. No personal or property-identifying information was collected or published.

## 1. Confirmed irregularity (fixed this session)

**index.html executive-summary bullet 5** claimed: "LA metro GDP is $1.355 trillion (2024, BEA) … the #2 county economy in the U.S."
- FRED/BEA series NGMP31080 (LA–Long Beach–Anaheim MSA GDP) is **discontinued**; final observation **2023 = 1,295,361.403 $M**. No 2024 value exists. https://fred.stlouisfed.org/series/NGMP31080
- The "#2 county economy" rank is not asserted anywhere else on the site and was not verified on any official page.
- This contradicted the page's own KPI card ($1.29T, 2023, discontinued), market.html, and flagged.html. PR #23 (which fixed it) was closed unmerged on 07 Nov.
- **Fix:** bullet rewritten to the verified 2023 metro / 2024 county figures; rank claim dropped; KPI card rounded value aligned to $1.295T; unemployment reference updated to the latest BLS observation.

## 2. Previously withheld values — now verified and published

The 07 Nov audit withheld six FEMA figures and two CAL FIRE percentages because the cited landing pages carried no values. On 08 Nov the underlying **official data services** were read directly:

### FEMA National Risk Index (official FEMA ArcGIS organization)
- Service: `National_Risk_Index_Counties`, layer 0, owner **FEMA_NationalRiskIndex**, org `XG15cJAlne2vxtgt` (FEMA's ArcGIS Online organization; item metadata credits the Federal Emergency Management Agency; data version **December 2025 / 1.20.0**).
- Item ownership proof: https://www.arcgis.com/sharing/rest/content/items/39485e8035d446a5bff03259508ae355?f=json (owner `FEMA_NationalRiskIndex`, accessInformation "Federal Emergency Management Agency").
- Query (STCOFIPS 06037): https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0/query?where=STCOFIPS%3D%2706037%27&outFields=COUNTY,STATE,RISK_SCORE,RISK_RATNG,EAL_VALT,ERQK_RISKS,WFIR_RISKS,IFLD_RISKS,CFLD_RISKS,NRI_VER&returnGeometry=false&f=json
- Returned: COUNTY "Los Angeles", RISK_SCORE **100**, RISK_RATNG **"Very High"**, EAL_VALT **7,601,846,373.16** (≈ $7.60B; December 2024 dollars per item metadata), ERQK_RISKS **100**, WFIR_RISKS **99.936**, IFLD_RISKS **100**, CFLD_RISKS **90**, NRI_VER "December 2025".
- Full-record query also returned ERQK_RISKR/WFIR_RISKR/IFLD_RISKR "Very High", CFLD_RISKR "Relatively High".
- Published on risks.html. The "#1 of all U.S. counties" rank from the parallel draft is **not** asserted (score 100 = top national percentile; unique rank not verified).
- Note: NRI v1.20 splits flooding into inland (IFLD) and coastal (CFLD); the draft's single "flood 100.0" corresponds to inland flooding. Both are published.
- Validator: `scripts/validate_site.py` gained an exact-URL-prefix exception for `https://services.arcgis.com/XG15cJAlne2vxtgt/` (FEMA's org only — not a blanket arcgis.com allowance).

### FEMA disaster declarations (OpenFEMA API, fema.gov)
- Query: https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries?$filter=state%20eq%20%27CA%27%20and%20contains(designatedArea,%27Los%20Angeles%27)&$select=disasterNumber,incidentType,declarationType,declarationDate&$orderby=declarationDate%20desc&$top=300&$inlinecount=allpages
- Returned count **88** records designating Los Angeles County; earliest 1969-01-26 (DR 253, Flood), latest 2025-08-08 (FM 5605, Fire). Includes DR/EM/FM types.
- Breakdown counted from the returned records: **61 Fire, 10 Flood, 8 Severe Storm**, 3 Earthquake, 2 Biological, 2 Freezing, 1 Hurricane, 1 Coastal Storm (breakdown labeled as computed from the query result on the site).

### CAL FIRE / OSFM official acreage table
- OSFM FHSZ page (re-read 08 Nov): https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones — SRA maps effective April 1, 2024; LRA phases released Feb 10 / Feb 24 / Mar 10 / Mar 24, 2025; **2026 SRA update public comment period now open** (November 2026 FAQ).
- Official acreage PDF linked from that page: "Fire Hazard Severity Zone acres in the State Responsibility Area Adopted April 1, 2024, and Local Responsibility Area acres transmitted to Local Jurisdictions March and April, 2025" (hosted on OSFM's azureedge CDN; direct URL recorded here, row cites the official OSFM page that links it):
  https://34c031f8-c9fd-4018-8c5a-4159cdff6b0d-cdn-endpoint.azureedge.net/-/media/osfm-website/what-we-do/community-wildfire-preparedness-and-mitigation/fire_hazard_severity_zone_acres_state_and_local_responsibility_2024_2025.pdf?rev=d1f74280dd01402f841bf2da5d5fc8cd&hash=EC6CA86D1AF5094D808CB341A328C52F
- Los Angeles County: LRA Very High **314,642 ac**; SRA Very High **454,920 ac**; combined Very High **769,561 ac**; all mapped classes combined **1,177,944 ac**.
- Statewide: LRA Very High **1,161,924 ac**; SRA Very High 16,881,829 ac; combined Very High 18,043,753 ac.
- Published as new verified rows. The draft's "26% Southern California expansion vs 2011" and "35% statewide increase (860k → 1.2M)" percentages remain **unverified and flagged** (not on any official page read).

## 3. Re-verified unchanged (all read 08 Nov 2026)

| Figure group | Official source | Result |
|---|---|---|
| City population 3,869,089; −0.8% vs 2020 base | https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225 | exact |
| MHI $81,939; rent $1,933; owner-occ 36.0%; density 8,304.2 | same | exact |
| Retail sales 81,351,523 $K; accom/food 17,366,966 $K (2022) | same | exact |
| County population 9,694,934; −3.2% | https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045225 | exact |
| City unemployment 5.8% (2025, 11-mo avg; Oct not collected) | https://www.bls.gov/lau/city-annual-unemployment-rates.htm | exact incl. footnote |
| County Dec 2025: 5.0%; LF 5,129,498 / emp 4,872,197 / unemp 257,301 | https://data.bls.gov/timeseries/LAUCN060370000000003 | exact |
| County 2025 11-month computed avg 5.6% | same (62.1 / 11 = 5.645 → 5.6) | recomputed, matches |
| **New:** county Sep 2026 prelim 4.5% (Aug 2026 final 4.9%) | same | new row added |
| Metro GDP 2023 = 1,295,361.403 $M, discontinued | https://fred.stlouisfed.org/series/NGMP31080 | exact |
| County GDP 2024 = 1,002,965,029 $K | https://fred.stlouisfed.org/series/GDPALL06037 | exact |
| SCAG county pop 10,046,000 → 10,793,000; emp 5,031,000 → 5,461,000 | https://sustain.scag.ca.gov/sites/default/files/2024-05/appendix_i_updated_tables_508_final.pdf (read directly) + forecast PDF Table 2 | exact |
| SCAG sectors: health 1,498→1,914K (+416K); constr 473→621K (+148K); accom/food 832→938K (+106K) | https://www.scag.ca.gov/sites/default/files/2024-05/23-2987-tr-demographics-growth-forecast-final-040424.pdf (Table 6) | exact |
| DTLA 2040: 100k homes / 175k residents / 100k work opportunities | https://planning.lacity.gov/odocument/92b97b24-1978-4e0e-9eae-51f22eda9e4c/Press%20Release_%20DTLA%20New%20Zoning%20Code.pdf | exact |
| 10-Q (Jul 5 2026): rev 257,657/262,401 (12wk), 861,438/899,196 (40wk); earnings 21,041/22,839, 47,971/74,534 | https://www.sec.gov/Archives/edgar/data/807882/000080788226000091/R4.htm | exact |
| Debt 44,160 current / 1,428,667 LT | …/R2.htm | exact |
| 149 company / 1,966 franchise units | …/R36.htm | exact |
| Leverage >5.0x; ABS >5.25x; $23.3M cash sweep | …/R14.htm | exact |
| EDGAR: Jul 2026 10-Q still latest periodic filing; FY2026 10-K not yet filed | https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000807882&type=10-&dateb=&owner=include&count=10 | confirmed |
| **New:** 8-K 2026-09-21 — CEO transition expected within 12 months, interim CEO, board refresh, GreenWood cooperation agreement extended | https://www.sec.gov/Archives/edgar/data/807882/000080788226000098/ex991-pressreleasexbodanno.htm | new issuer-context row (no personal names published) |
| ULA $5,400,000 / $10,900,000 (closings after Jun 30 2026); 4% / 5.5% + 0.45% base | https://finance.lacity.gov/faq/measure-ula | exact |
| USGS 60% / 46% / 31% (M≥6.7/7.0/7.5, 30 yr, LA region) | https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-los-angeles-area-san-francisco-bay-area | exact verbatim |
| CDI 41,727 claims / $25.2B paid (Eaton+Palisades; tracker updated Jul 6 2026) | https://www.insurance.ca.gov/01-consumers/180-climate-change/Wildfire-Claims-Tracker.cfm | exact, unchanged |

## 4. Re-checked and still open (kept flagged)

- **CAL FIRE 26% / 35% expansion percentages** — not on the OSFM page or acreage table; withheld. Official acreage published instead.
- **LA County heat-related illness data brief** — http/https both still return page-not-found (re-checked 08 Nov). NOAA Climate.gov remains the heat source.
- **EDD county profile** — still displays "Data for Los Angeles County not available for Unemployment Rate and Labor Force"; BLS LAUS series remains the published source.
- **SCAG press-release discrepancy** — Dec 2023 press release says 10.77M for 2050; adopted tables say 10,793,000 (now read directly from the adopted PEIR appendix on sustain.scag.ca.gov). Adopted figure published; discrepancy disclosed.
- **ULA FAQ wording** — effective-date note ($5.4M/$10.9M) controls; FAQ intro still says $5M/$10M. Disclosed.
- **Metro GDP 2024 / county rank** — never published officially; removed from the landing page this session.

## 5. Deployment notes

- Attempted `PUT /repos/…/pages build_type=workflow` once: **HTTP 403** ("Resource not accessible by integration"), consistent with prior sessions. Pages remains **legacy** (main root). The Pages workflow also runs and validates on every push/PR; its deploy artifact contains only the eight canonical pages + assets. Legacy serving additionally exposes archived/internal repo files, all of which passed the privacy scans (no personal information anywhere in the repo per prior audits; re-confirmed by the validator's email/phone scan on the canonical pages).
- Validator: `python3 scripts/validate_site.py` — see COORDINATION.md completion entry for the final row count.

## 6. Privacy

No owner names, addresses, APNs, lease parties, rents, or personal financial details were collected, stored, or published. The new SEC 8-K row describes roles only (no officer names). Validator email/phone scans pass on all eight pages.

---

## 7. Post-merge addendum (same session, ~23:40 UTC)

While this audit's source reads were in flight, five other sessions merged PRs #28–#42 to main and rebuilt the canonical dashboard as **17 pages** (the former market/model/risk pages were archived under `archive/arena-81536038/`). Their merged build already contained equivalents of this session's index GDP fix, OSFM acreage rows, OpenFEMA declaration counts (88/61/10/8/9), and the BLS Sep-2026 preliminary update.

Conflict resolution followed the coordination protocol — **no session's work discarded**:
- Merged `origin/main` into `arena/b8188ee0-jack1`; kept the merged 17-page versions of all shared canonical pages, README, and the 17-page validator (this session's exact-prefix FEMA ArcGIS exception auto-merged into it).
- `COORDINATION.md`: all merged sessions' records retained in sequence; this session's record appended after them.
- Re-applied only this session's still-unique verified additions onto the 17-page build:
  1. **FEMA NRI county values** on `risks.html` (composite 100/100 Very High; EAL $7,601,846,373; earthquake 100; wildfire 99.9; inland flooding 100 / coastal 90), closing flagged item **F-08**, with the exact official query link; `sources.html` and `audit.html` updated to match.
  2. **SEC 8-K (2026-09-21)** issuer-governance row on `tenant.html` (roles only, no personal names).
  3. Audit rows recording this session's independent re-reads (SEC XBRL R2/R4/R14/R36 exact; all 20 figure groups matched).
- The earlier 8-page edits from this session remain in git history (`a5dff00`, `54c6c93`).

Final validator state after re-application: **17 pages, 362 table-body rows, PASS** (official-source link on every row; allowlist + FEMA-org prefix; local links/anchors; no email/phone patterns).

Note on the merged build's 2025 county annual average (5.7%): the labor-force-weighted average of the eleven published 2025 months recomputes to 5.65% → 5.7%, consistent with the merged page; the simple average of the rounded monthly rates is 5.6%. Both are disclosed on the merged site's flagged register (F-13). No change made.

## 8. Final integration state (second interleave)

`origin/main` advanced again through PRs #44–#45 (session 0e369d53) to a **10-page data-driven canonical build** (`data/verified-2026-11-08.json` → `scripts/build_public.py`), which independently verified and published the same FEMA NRI county values this session read (plus social vulnerability, resilience, and per-hazard EAL detail). The 17-page build is preserved under `archive/arena-main-3da3b70/`.

This session merged that build without discarding any session's work and re-applied its remaining unique verified contributions **through the dataset** (the correct path for the generated build):
- `sec_8k_sept2026` source + `tenant_governance` observation (issuer leadership transition; roles only, no personal names);
- `nri_coastal_flood` observation (score 90, Relatively High — complements the published inland score of 100);
- `audit_b8188ee0_pass` audit entry recording this session's independent re-reads.

Final gates on the merged + updated tree: `build_public.py --check` PASS (11 generated files match the dataset); `scripts/validate_site.py` PASS (**10 pages, 268 sourced table rows**); 11 unit tests PASS. All prior coordination records retained in sequence in COORDINATION.md.
