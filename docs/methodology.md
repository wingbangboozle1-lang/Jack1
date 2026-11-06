## What this file is

A decision file for one commercial property: a single-tenant Jack in the Box freehold, ground and building, in the central Los Angeles trade area, leased triple-net, with the lease expiring somewhere between 2030 and 2035. The decision is binary in form — sell before expiry, or renew and hold — and is complicated by the fact that almost every property-specific input is unknown.

The file is organised so that a reader can check any single number against its official publisher without reading anything else. Every row is self-contained: metric, geography, value, period, publisher, URL, verification status, and a note.

## The verification standard

**Every table row carries a source link to an official publisher.** Official means one of:

- a United States federal statistical or regulatory agency (Census, BLS, BEA, FHFA, FEMA, USGS, NCES, NOAA, Treasury, SEC, IRS);
- a Federal Reserve Bank republishing an official federal series with the originating agency named on the series page;
- a State of California agency (Department of Finance, Department of Insurance, Department of Education, Department of Industrial Relations, Employment Development Department, Department of Forestry and Fire Protection, Geological Survey, State Board of Equalization);
- a California regional planning agency acting under federal designation (Southern California Association of Governments);
- Los Angeles County (Assessor, Auditor-Controller, Treasurer and Tax Collector, Registrar-Recorder, Fire Department, open-data portal);
- the City of Los Angeles (Department of City Planning, Office of Finance, Office of Wage Standards, Housing Department, Fire Department, Police Department, Department of Transportation, Department of Building and Safety, open-data portal);
- a document filed with the U.S. Securities and Exchange Commission by the tenant's parent, Jack in the Box Inc.

**If a value could not be confirmed from an official source, the value cell is left blank.** It is never filled from memory, never filled by inference from a neighbouring geography, never filled from a news article, and never filled from a data aggregator. The row is marked unverified and registered on the Flagged for Review page with the official link needed to close it.

**A distinction is drawn between blank and withheld.** Some cells are blank because the information is parcel-specific and no official source can supply it without a location, which is withheld. Some are blank because the official publisher does not release the series at that geography at all — Census QuickFacts publishes no business or employment fields for the City of Los Angeles, for example. Some are blank because the value exists only in private market data that no government agency publishes, such as capitalisation rates. Each row states which case applies.

**Values seen only in non-official sources are recorded separately and never used.** Where a figure was encountered in a secondary source and could not be confirmed officially, it is stored in a distinct `r` field, rendered under a *Reported by a non-official source — NOT used* marker, and excluded from every model input and from the recommendation. It is published only so a reader can see precisely what was declined, and can go and confirm or refute it. That is more useful than silence.

## Sources deliberately excluded

The following classes of source were encountered during research and were excluded from the verified dataset in every case:

- commercial hazard and risk aggregators that republish FEMA National Risk Index data;
- real-estate brokerages, investment platforms and capitalisation-rate research providers;
- credit-rating agencies;
- local and national news outlets, including television stations and newspapers;
- encyclopedias and wikis;
- earnings calendars, stock-screeners and financial data aggregators;
- legal-information and tax-calculator websites;
- insurance comparison and lead-generation websites;
- real-estate listing portals and neighbourhood-score providers.

Two exclusions deserve specific mention because they were tempting. **Capitalisation rates** are published only by private brokerages and research firms; no government agency produces them, so none is stated as fact anywhere on this site. **Credit ratings** are issued by private Nationally Recognized Statistical Rating Organizations; none is quoted. Tenant credit is instead assessed entirely from the company's own SEC-filed disclosures — restaurant count trajectory, same-store sales, franchise-level margin, franchisee bad-debt expense, average unit volume, and leadership status.

## The privacy protocol

Privacy was treated as the highest-priority constraint. The subject property is anonymised throughout.

**Not published anywhere on this site, and not stored in the underlying data files either:** the property's street address, cross streets or parcel number; the owner's name, entity structure or contact details; the purchase price, basis or holding period; the contract rent, net operating income or market value; the tenant's or franchisee's identity at site level; and the insurance carrier, limits or premium.

**Consequence, stated plainly:** every parcel-specific and owner-specific analysis is impossible, and this file says so rather than working around it. Traffic counts, assigned schools, zoning, flood zone, fire hazard severity zone, earthquake fault zone, Tax Rate Area, assessed value and competing-site density all require a location. They are left blank, flagged, and paired with the official lookup tool a reader would use to obtain them. The recommendation is therefore structured as a decision tree whose branches are resolved by facts the owner can obtain, rather than as a single instruction that pretends those facts are known.

## Geography discipline

Los Angeles has four official geographies that are routinely confused, and confusing them produces wrong numbers. Every row on this site states which one it uses:

- **City of Los Angeles** — Census QuickFacts, City Planning community plan areas, the Office of Wage Standards minimum wage, Measure ULA.
- **Los Angeles County** — Census QuickFacts, the County Assessor's roll, Department of Finance population estimates, BEA county GDP, County Fire Department hazard zones.
- **Los Angeles–Long Beach–Anaheim metropolitan statistical area** — BLS local area unemployment statistics and current employment statistics.
- **Los Angeles–Long Beach–Glendale metropolitan division** — BLS metropolitan area employment and unemployment releases; FHFA house price index. This division is coterminous with Los Angeles County and is the closest official geography to "central Los Angeles" for price series.

County values are never substituted for city values, and metropolitan-area values are never presented as county values. Where a series simply does not exist at the needed geography, the row is blank and the reason is stated.

## Vintage discipline

No number is published without a period. Several are explicitly preliminary — BLS marks September 2026 metropolitan figures `(p)` — and that marking is carried through to the rendered table rather than dropped. Where two official sources disagree about the same quantity, both are published with their vintages and the disagreement is logged as an irregularity; the analysis does not silently choose one.

Two structural vintage problems were encountered and are disclosed rather than smoothed over. The State of California's official occupational projection window runs 2022 to 2032, which **ends before the lease expiry window**, so no official employment projection covers the final years of the decision. And the Bureau of Economic Analysis has **discontinued** metropolitan-area GDP and personal income statistics, so metropolitan-level income projections can no longer be sourced at all; the analysis was rebuilt on county GDP.

## The projection system

The model is specified entirely in `data/projection.json` and computed at build time by `tools/model.py`, which writes `data/projection_output.json`. `tools/build_site.py` renders those outputs. No number in a rendered table is hand-entered, so published figures cannot drift from the specification.

Four design choices matter:

**Normalisation.** The property's value, rent and net operating income were never supplied. The model therefore runs on an index in which the asset's value on the retrieval date equals 100.0. Outputs are index points and must be read as relative comparisons between decision paths, never as valuations.

**Only official inputs drive it.** The risk-free anchor is the U.S. Treasury par yield, read directly from the Treasury table. Rent-escalation scenarios are the low, median and high of the five official BLS Los Angeles CPI-U twelve-month readings published in 2026. Land-value growth is the official FHFA index. Tenant non-renewal probability compounds at the company-disclosed 1% ongoing annual closure rate. Catastrophe severity is the County's own official January 2025 fire loss statistics divided by official BEA county GDP.

**Unverifiable inputs are gridded, not chosen.** The capitalisation spread, the dark-box land residual, the years to expiry and the post-expiry downtime have no official publisher. Each is declared as an unverified input, varied across a grid, and every dependent output is labelled. The conclusion is drawn from the **ranking** of paths and from whether that ranking is **stable across the whole grid** — not from any single unverified number.

**Both sides of the comparison are charged the same frictions.** The sell path bears Measure ULA up front. The hold path bears the same statutory transaction cost on its terminal sale, plus a post-expiry vacancy scenario. Without that symmetry, holding would win by construction and the comparison would be meaningless. The model also runs a **stress case** built only from already-declared worst inputs, which identifies the conditions under which the recommendation is wrong. Those conditions are published on the Projection page rather than buried.

A model integrity check is rendered on the page: a flat, never-ending, never-dark tenancy must return exactly 100.00 index points at every point of the spread grid. If it does not, the build is wrong.

## The risk register

Twenty-eight risks are scored across six decision paths, each on likelihood and impact from 1 to 5, giving a score from 1 to 25. Where a likelihood is anchored in an official published statistic, the anchor is named and the row is marked **Official**. Where no official statistic exists, the row is marked **Judgement** and is also listed on the Flagged for Review page. No judgement-based likelihood is presented anywhere on this site as a verified number.

Five rows are marked as black swans, using a definition stated up front: a low-probability event producing damage disproportionate to the asset's income, where the loss is not diversifiable inside a single-asset, single-tenant position.

## The coordination protocol

Work was coordinated through `COORDINATION.md` in the repository root: a task board with status and owning session, a session registry, a change-request log, a conflict log, and the privacy rules. Claims were written and pushed before work began. Commits were small and frequent, with `git pull --rebase` before every push. Nine other `arena/*` branches were found to have written competing whole-repository claims; none contained any deliverable, so the conflict was logged and resolved rather than honoured, and no work was duplicated or discarded. The full inventory and the resolution are on the Repo Audit page.

## Reproducing this site

```
python3 tools/model.py            # data/projection.json -> data/projection_output.json
python3 tools/collect_sources.py  # every data/*.json row -> data/sources.json
python3 tools/audit_repo.py       # repository state -> docs/repo-audit.md
python3 tools/build_site.py       # data/*.json -> all 19 HTML pages
python3 tools/check_links.py      # fails on a missing internal link, an unsourced
                                  # verified row, a non-official host in a verified
                                  # row, or a privacy-pattern leak
```

`check_links.py` is a gate, not a report. It exits non-zero if any verified row lacks a URL, if any internal link is broken, if any verified row cites a host outside the official allowlist, or if any rendered page matches a privacy pattern such as a street address or a parcel-number format. The site is not published while it fails.
