#!/usr/bin/env python3
"""Produce `data/verified-2026-11-10.json` from `data/verified-2026-11-08.json`.

Session `cd460c3b`, 2026-11-10. The 2026-11-08 dataset is the base; every change below was
verified on an official page on 2026-11-10 and is recorded in
`verification/2026-11-10-cd460c3b.md`.

Changes:
  1. CORRECTION - California Jack in the Box restaurant count. The 2026-11-08 build published the
     Del Taco California row (351 total / 94 company-operated / 257 franchise) as if it were the
     Jack in the Box row. The FY2025 Form 10-K Item 2 "restaurant locations (by segment, by
     state)" table prints Jack in the Box California as 96 company-operated / 845 franchise /
     941 total.
  2. CORRECTION - derived California share of the Jack system: 16.4% -> 44.1% (941 / 2,136).
  3. REFRESH   - Treasury par yields to the 2026-11-09 business day (newest published).
  4. ADDITIONS - 15 verified rows (Census city/county; JACK FY2025 Form 10-K lease, property and
     franchise terms; complete FEMA NRI hazard-rating set).
  5. DISCLOSURE- new flags for the corrected California row and for the open 2026 CAL FIRE SRA
     Fire Hazard Severity Zone public comment period; new audit entry for this pass.

The script is idempotent: it always starts from the 2026-11-08 base and overwrites the target.

Usage:  python3 scripts/refresh_dataset.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "verified-2026-11-08.json"
TARGET = ROOT / "data" / "verified-2026-11-10.json"

SESSION_DATE = "2026-11-10"

# Sources re-read on 2026-11-10. Sources not listed keep their earlier access date because the
# page was not re-opened in this pass.
REREAD_SOURCES = [
    "census_city", "census_county",
    "bls_summary", "bls_city_annual", "bls_laus",
    "edd_la",
    "fred_county_gdp", "fred_metro_gdp",
    "treasury",
    "dof_landing", "dof_p2a",
    "scag_tr", "scag_appendix",
    "dtla_release",
    "ula", "prop13", "ftb_capgains", "irs_8824",
    "dir_fastfood", "dir_minwage", "la_wage",
    "dashboard_engagement", "dashboard_performance",
    "sec_10k", "sec_10q", "sec_release", "sec_8k_sept2026",
    "fema_county_query", "fema_hazard_ratings",
    "usgs_faq",
    "calfire_fhsz", "calfire_acres",
    "cdi_claims",
]

NEW_OBSERVATIONS = [
    {
        "id": "geo_county_density",
        "category": "Geography",
        "measure": "Los Angeles County population density",
        "value": "2,466.9 people/sq mi",
        "geography": "Los Angeles County",
        "period": "2020 Census",
        "status": "verified",
        "note": "Countywide average; site-level density and access require parcel review.",
        "sources": ["census_county"],
    },
    {
        "id": "geo_commute_city",
        "category": "Geography",
        "measure": "Mean travel time to work",
        "value": "30.7 minutes",
        "geography": "City of Los Angeles",
        "period": "2020-2024 ACS",
        "status": "verified",
        "note": "Commute-length proxy for customer catchment; the county figure is 30.4 minutes. Not a trade area.",
        "sources": ["census_city"],
    },
    {
        "id": "households_city",
        "category": "Population",
        "measure": "Households and household size",
        "value": "1,439,097 households; 2.61 persons per household",
        "geography": "City of Los Angeles",
        "period": "2020-2024 ACS",
        "status": "verified",
        "note": "Citywide estimate; not a trade-area or parcel figure.",
        "sources": ["census_city"],
    },
    {
        "id": "health_insurance_city",
        "category": "Population",
        "measure": "Persons without health insurance under age 65",
        "value": "10.7%",
        "geography": "City of Los Angeles",
        "period": "2020-2024 ACS",
        "status": "verified",
        "note": "Coverage-gap proxy for household budget pressure; the county rate is lower.",
        "sources": ["census_city"],
    },
    {
        "id": "education_city",
        "category": "Income",
        "measure": "Persons 25 and older with a bachelor's degree or higher",
        "value": "38.5%",
        "geography": "City of Los Angeles",
        "period": "2020-2024 ACS",
        "status": "verified",
        "note": "Citywide attainment rate; not a parcel or school-district measure.",
        "sources": ["census_city"],
    },
    {
        "id": "housing_cost_city",
        "category": "Housing",
        "measure": "Median selected monthly owner costs with a mortgage",
        "value": "$3,497/month",
        "geography": "City of Los Angeles",
        "period": "2020-2024 ACS",
        "status": "verified",
        "note": "Owner-occupied units only; excludes renters, and the city has a 36.0% owner-occupied rate.",
        "sources": ["census_city"],
    },
    {
        "id": "retail_county",
        "category": "Economy",
        "measure": "Total retail sales, county",
        "value": "$213,932,785 thousand",
        "geography": "Los Angeles County",
        "period": "2022 Economic Census",
        "status": "verified",
        "note": "Countywide Economic Census total; not attributable to the subject site.",
        "sources": ["census_county"],
    },
    {
        "id": "business_county",
        "category": "Economy",
        "measure": "Total employer establishments, employment, and annual payroll",
        "value": "304,988 establishments; 3,987,736 employees; $299,616,607 thousand annual payroll; employment +2.3% (2022-2023)",
        "geography": "Los Angeles County",
        "period": "2023",
        "status": "verified",
        "note": "All-industry employer counts: a demand base, not a site forecast. The city-level QuickFacts business rows are not published.",
        "sources": ["census_county"],
    },
    {
        "id": "tenant_franchising_mix",
        "category": "Tenant",
        "measure": "Share of the system that is franchised",
        "value": "Jack in the Box: 1,986 of 2,136 restaurants franchised (93%); 150 company-operated. Del Taco: 444 of 576 franchised (77%); 132 company-operated",
        "geography": "Jack in the Box Inc. system",
        "period": "As of September 28, 2025",
        "status": "verified",
        "note": "Most restaurants are operated by franchisees, so the landlord's counterparty is usually a franchisee rather than the issuer. Verify the actual obligor.",
        "sources": ["sec_10k"],
    },
    {
        "id": "tenant_lease_structure",
        "category": "Tenant",
        "measure": "Jack in the Box restaurant lease structure",
        "value": "Fixed rent with cost-of-living index adjustments plus real estate taxes, insurance and other expenses; about 13% of Jack leases add contingent rent of 1%-10% of gross sales above stated thresholds",
        "geography": "Jack in the Box system",
        "period": "FY2025 Form 10-K",
        "status": "verified",
        "note": "System-wide disclosure; the subject lease may differ and is unverified.",
        "sources": ["sec_10k"],
    },
    {
        "id": "tenant_property_mix",
        "category": "Tenant",
        "measure": "Restaurant building ownership and ground leases",
        "value": "729 company-owned buildings (63 company-operated, 666 franchise); 1,020 company-leased buildings on leased land (87 company, 933 franchise); 387 franchise directly owned or leased; 2,136 total",
        "geography": "Jack in the Box system",
        "period": "As of September 28, 2025",
        "status": "verified",
        "note": "Shows the ground-lease chain; the subject site may sit at any level and is unidentified.",
        "sources": ["sec_10k"],
    },
    {
        "id": "tenant_prototype_size",
        "category": "Tenant",
        "measure": "Jack in the Box restaurant building size",
        "value": "Approximately 1,372 sq ft",
        "geography": "Jack in the Box system",
        "period": "FY2025 Form 10-K",
        "status": "verified",
        "note": "Prototype size; re-tenanting capital and alternative-use feasibility scale with the actual building.",
        "sources": ["sec_10k"],
    },
    {
        "id": "tenant_franchise_terms",
        "category": "Tenant",
        "measure": "Franchise agreement terms",
        "value": "Initial franchise fee $50,000 per restaurant for a 20-year term; royalty and marketing payments generally 5.0% of gross sales",
        "geography": "Jack in the Box system",
        "period": "FY2025 Form 10-K",
        "status": "verified",
        "note": "Describes franchisee economics, not the landlord's rent or lease term.",
        "sources": ["sec_10k"],
    },
    {
        "id": "tenant_portfolio",
        "category": "Tenant",
        "measure": "Del Taco sale agreement",
        "value": "$115 million cash aggregate purchase price under a Stock Purchase Agreement entered October 15, 2025, subject to closing cash, working capital, debt and transaction expense adjustments",
        "geography": "Jack in the Box Inc.",
        "period": "FY2025 Form 10-K",
        "status": "verified",
        "note": "Single-brand issuer concentrates brand risk. Party names are deliberately not published. Closing status and final proceeds are not stated in this figure.",
        "sources": ["sec_10k"],
    },
    {
        "id": "tenant_discontinued_ops",
        "category": "Tenant",
        "measure": "Discontinued operations in Q3 FY2026",
        "value": "Loss from discontinued operations $919 thousand for the 12 weeks ended July 5, 2026; earnings from continuing operations $21,041 thousand and net earnings $20,122 thousand",
        "geography": "Jack in the Box Inc.",
        "period": "12 weeks ended July 5, 2026",
        "status": "verified",
        "note": "Del Taco results are presented as discontinued operations in the issuer's Q3 FY2026 reporting.",
        "sources": ["sec_release"],
    },
]

NRI_ALL_HAZARD_RATINGS = (
    "Avalanche Relatively High; Coastal flooding Relatively High; Cold wave Very Low; "
    "Drought Relatively Low; Earthquake Very High; Hail Relatively Moderate; "
    "Heat wave Relatively High; Hurricane No Rating; Ice storm Not Applicable; "
    "Inland flooding Very High; Landslide Relatively High; Lightning Very High; "
    "Strong wind Relatively Moderate; Tornado Relatively High; Tsunami Relatively Low; "
    "Volcanic activity Not Applicable; Wildfire Very High; Winter weather Relatively Moderate"
)

RISK_CONTEXT_UPDATES = {
    "risk_rates": (
        "Treasury 10Y 4.88% on November 9, 2026 is context, not a cap rate."
    ),
    "risk_tenant_credit": (
        "Issuer Q3 FY2026 system SSS -1.1%, franchise -1.2%; net restaurant count -13 QTD. "
        "93% of Jack restaurants are franchised, so the lease counterparty is usually a franchisee, not the issuer."
    ),
    "risk_nnn_leakage": (
        "No executed lease provided. Issuer disclosure shows its own restaurant leases carry cost-of-living "
        "index adjustments plus taxes, insurance and other expenses, with contingent rent in about 13% of Jack leases."
    ),
    "risk_rent_market": (
        "No subject rent or market rent study verified. Issuer leases index with cost of living and 13% add "
        "contingent rent of 1%-10% of gross sales."
    ),
}


def main() -> int:
    with open(BASE, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    data["meta"]["date"] = SESSION_DATE
    data["meta"]["session"] = "cd460c3b"

    obs = {o["id"]: o for o in data["observations"]}

    # 1 + 2. Correction of the California row and its derived share.
    obs["tenant_ca_2025"]["value"] = "941 total; 96 company-operated; 845 franchise"
    obs["tenant_ca_2025"]["period"] = "As of September 28, 2025 (FY2025 Form 10-K Item 2)"
    obs["tenant_ca_2025"]["note"] = (
        "California is the largest state market in the Jack in the Box system. "
        "System-wide count, not the subject site."
    )
    obs["tenant_ca_share"]["value"] = "44.1%"
    obs["tenant_ca_share"]["period"] = "As of September 28, 2025"
    obs["tenant_ca_share"]["note"] = (
        "Derived: 941 California Jack in the Box restaurants / 2,136 system total at FY2025 year end. "
        "Geographic concentration, not parcel exposure."
    )

    # 3. Refresh.
    obs["treasury_yields"]["value"] = "2Y 4.56%; 5Y 4.67%; 10Y 4.88%; 30Y 5.26%"
    obs["treasury_yields"]["period"] = "November 9, 2026"
    obs["treasury_yields"]["note"] = (
        "Latest published business day on 2026-11-10. Context for required-return discussion only; "
        "not a cap rate and not used as one."
    )

    # 4. Complete FEMA NRI hazard rating set (all 18 rated hazards).
    obs["nri_other_hazards"]["value"] = NRI_ALL_HAZARD_RATINGS
    obs["nri_other_hazards"]["note"] = (
        "Complete set of the 18 rated hazards for Los Angeles County; ratings, not parcel exposure."
    )

    for item in NEW_OBSERVATIONS:
        obs[item["id"]] = item
    data["observations"] = list(obs.values())

    for risk in data["risks"]:
        if risk["id"] in RISK_CONTEXT_UPDATES:
            risk["context"] = RISK_CONTEXT_UPDATES[risk["id"]]
    for risk in data["risks"]:
        if risk["id"] == "risk_tenant_credit" and "sec_10k" not in risk["sources"]:
            risk["sources"].append("sec_10k")

    # 5. Disclosures.
    data["flags"].append({
        "id": "flag_tenant_ca_correction",
        "item": "Corrected California Jack in the Box restaurant count",
        "reason": (
            "The 2026-11-08 build published 351 total / 94 company-operated / 257 franchise as the "
            "California Jack in the Box count. Those are the Del Taco California figures. The FY2025 "
            "Form 10-K Item 2 state table prints Jack in the Box California as 96 company-operated / "
            "845 franchise / 941 total, with table totals reconciling to 2,136 (150 company-operated, "
            "1,986 franchise) and Del Taco 576 (132 company-operated, 444 franchise)."
        ),
        "action": (
            "Corrected in the 2026-11-10 build; the derived California share changed from 16.4% to 44.1%. "
            "Re-read the 10-K state table before relying on any state-level count."
        ),
        "sources": ["sec_10k", "repo"],
    })
    data["flags"].append({
        "id": "flag_calfire_2026_sra",
        "item": "2026 State Responsibility Area Fire Hazard Severity Zone comment period",
        "reason": (
            "The Office of the State Fire Marshal page, read 2026-11-10, states the 2026 SRA FHSZ "
            "public comment period is open. The published county acreage comes from the 2024-2025 "
            "table, so mapped acres and zone status can change once the 2026 SRA map is adopted."
        ),
        "action": (
            "Re-read the OSFM acreage table after adoption and re-run the parcel FHSZ lookup once "
            "the parcel is identified."
        ),
        "sources": ["calfire_fhsz", "calfire_acres"],
    })

    data["audit"].append({
        "id": "audit_cd460c3b_pass",
        "check": "Independent official-source re-verification (session cd460c3b, 10 November 2026)",
        "result": (
            "47 figure groups re-read on their official pages and matched; 1 material error found and "
            "corrected (the California Jack in the Box restaurant count had published the Del Taco row); "
            "1 vintage refreshed (Treasury par yields to 2026-11-09); 15 verified rows added."
        ),
        "detail": (
            "Full ledger with per-row official links in verification/2026-11-10-cd460c3b.md. "
            "Unverified values remain blank; corrections are disclosed on the Flagged for Review page."
        ),
        "sources": [
            "census_city", "census_county", "bls_summary", "bls_laus", "bls_city_annual",
            "edd_la", "fred_county_gdp", "fred_metro_gdp", "treasury", "dof_p2a",
            "scag_appendix", "scag_tr", "dtla_release", "ula", "prop13", "ftb_capgains",
            "irs_8824", "dir_fastfood", "dir_minwage", "la_wage", "dashboard_engagement",
            "dashboard_performance", "sec_10k", "sec_10q", "sec_release", "sec_8k_sept2026",
            "fema_county_query", "fema_hazard_ratings", "usgs_faq", "calfire_acres",
            "calfire_fhsz", "cdi_claims", "repo",
        ],
    })

    for sid in REREAD_SOURCES:
        if sid in data["sources"]:
            data["sources"][sid]["accessed"] = SESSION_DATE

    # 6. Explicit derived-arithmetic checks so a published percentage can never drift away from
    #    the official counts it is derived from. The validator recomputes each one.
    data["derived_checks"] = [
        {
            "id": "tenant_ca_share",
            "description": "California share of the Jack in the Box system",
            "formula": "numerator / denominator * 100",
            "inputs": {"numerator": 941, "denominator": 2136},
            "input_observations": {"numerator": "tenant_ca_2025", "denominator": "tenant_franchising_mix"},
            "expected_value": 44.1,
            "unit": "percent",
            "sources": ["sec_10k"],
        },
        {
            "id": "calfire_share",
            "description": "Share of mapped Los Angeles County acres in the CAL FIRE Very High zone",
            "formula": "numerator / denominator * 100",
            "inputs": {"numerator": 769561, "denominator": 1177944},
            "input_observations": {"numerator": "calfire_acres_obs"},
            "expected_value": 65.3,
            "unit": "percent",
            "sources": ["calfire_acres"],
        },
    ]

    with open(TARGET, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False, sort_keys=False)
        fh.write("\n")
    print(f"Wrote {TARGET.relative_to(ROOT)}: {len(data['observations'])} observations, "
          f"{len(data['sources'])} sources, {len(data['flags'])} flags, {len(data['audit'])} audit entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
