# Data directory status (RR-08, resolved 2026-11-10, session arena/a8681975-jack1)

Canonical dataset: **`verified-2026-11-08.json`** — the single source of truth for every published
table row. `scripts/build_public.py` reads only this file, and the live site at
https://wingbangboozle1-lang.github.io/Jack1/ is generated entirely from it. Its metadata
(`meta.date = 2026-11-08`, `meta.session = 0e369d53`) records the extraction date, not the last
review date; `meta.last_reviewed` carries the most recent full verification pass.

Legacy files in this directory are **not published and not used by any current build**:

- `records.json` — 130-row historical draft from early research sessions. Superseded; kept for
  provenance only. Do not cite or feed to builds.
- `facts.json`, `sources.json`, `assumptions.json`, `model.json`, `risks.json`, `scenarios.json` —
  early-session drafts superseded by the sections of `verified-2026-11-08.json`.
- `property_data.md` — internal-only owner/parcel capture sheet. Blank fields are intentional;
  contents may reference private identifiers and must never be published.

Rule of record: never merge values from legacy files into the canonical dataset without a fresh
official-source verification, and never publish anything from this directory except through
`scripts/build_public.py` reading `verified-2026-11-08.json`.
