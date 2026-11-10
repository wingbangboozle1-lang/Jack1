# Data directory status (updated 2026-11-10 UTC)

Active canonical dataset: **`verified-2026-11-10.json`**. `scripts/projection_model.py` sets
`DATA_PATH` to this file, `scripts/build_public.py` imports that loader, and every published table
row and `assets/projections.json` is generated from it. Its metadata records the 2026-11-10
verification/integration state.

Historical baseline: **`verified-2026-11-08.json`** is preserved for provenance. It was last
reviewed and corrected on 2026-11-10 by session `a8681975` (including the California restaurant
brand-column correction). It is **not** the active builder input and is not published.

Legacy files in this directory are **not published and not used by any current build**:

- `records.json` — 130-row historical draft from early research sessions. Superseded; kept for
  provenance only. Do not cite or feed to builds.
- `facts.json`, `sources.json`, `assumptions.json`, `model.json`, `risks.json`, `scenarios.json` —
  early-session drafts superseded by the canonical dataset sections.
- `property_data.md` — internal-only owner/parcel capture sheet. Blank fields are intentional;
  contents may reference private identifiers and must never be published.

This README is an internal repository note and is excluded from the curated Pages artifact.
Rule of record: never merge values from legacy files into a canonical dataset without a fresh
official-source verification, and never publish anything from this directory except through
`scripts/build_public.py` reading the active canonical dataset named above.
