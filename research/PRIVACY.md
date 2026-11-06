# Privacy & Anonymization Policy (binding on every page of this site)

**Status:** in force. Reviewed 2026-11-06.

## 1. What is protected
The following are treated as *personal or identifying information* and are **never published** on this site,
in any page, table, chart, filename, image, alt-text, or metadata:

| Category | Examples | Handling |
|---|---|---|
| Street address / parcel | Street number, street name, unit, APN / AIN, legal description, lat-long precise to the parcel | Replaced by placeholders |
| Owner identity | Owner name(s), trust names, LLC names tied to the individual, mailing address, contact details | Never recorded here |
| Tenant contact data | Franchisee names, store-level managers, phone/email of any person | Never recorded here |
| Lease document contents | Rent figures from the actual lease, option language, estoppel, side letters | Never transcribed; described only in generic, market-level terms |
| Financial position of the owner | Actual basis, mortgage balance, personal tax situation, net worth | Never recorded here |
| Any other natural person | Names appearing in news/disaster coverage | Not repeated; refer to the official record instead |

## 2. Placeholder scheme
| Placeholder | Meaning |
|---|---|
| `[PARCEL-REDACTED]` | The specific parcel; use the Assessor's own public search to look up a parcel by owner |
| `[CITY-CENTRAL-LA]` | The sub-market within the City of Los Angeles described generically as "Central Los Angeles" |
| `[OWNER-ENTITY]` | The owning entity (individual, trust, or LLC) |
| `[TENANT-ENTITY]` | The tenant/franchisee entity of record |
| `[LEASE-START]`, `[LEASE-EXPIRY]` | Lease dates, given only as ranges supplied by the principal |
| `[RENT]`, `[NOI]`, `[BASIS]` | Monetary terms of the actual deal |

## 3. Data that *is* published
Only non-personal, official statistical and regulatory facts, each with a link to the issuing agency:

- Census/BLS/FRED/IRS/State of California/County of Los Angeles public statistics and rules.
- Market-level capitalization-rate ranges **as quoted by third-party brokers**, clearly labelled as
  non-official market commentary and linked to the quoted page.
- Anything derived (projections, indices) is labelled *model output* and is reproducible from
  `tools/model.py` plus the inputs in `data/verified_data.json`.

## 4. Verification rule that protects accuracy as well as privacy
Every table row must carry a source URL that resolves to an official (`*.gov`, `*.ca.gov`, Federal Reserve,
SEC) or clearly-labelled third-party page. If a value cannot be confirmed, the value cell is left **blank**
and the row is listed on **Flagged for Review** with the reason. No value is ever inferred, interpolated,
or filled from memory.

## 5. Legal basis / corroboration
California itself restricts publishing certain address-linked records:
State Board of Equalization Letter To Assessors **No. 2025/010 (March 19, 2025)**, implementing AB 1785,
amends Government Code §7928.205 to bar state/local agencies from publicly posting, on the internet, an
official's home address, telephone number, or *both the name and assessor parcel number* associated with it.
Source: <https://www.boe.ca.gov/proptaxes/pdf/lta25010.pdf>
This site applies the stricter, voluntary rule in §1 above to **all** persons, not just officials.
