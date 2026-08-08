"""
All model numbers for the Project Bridge Deal Command Center.
Source: Project Bridge case analysis doc (Sections 2.1, 3.4, 4.1-4.4, 5.5).
All figures illustrative, per the case pack disclaimer.
"""

company_snapshot = {
    "Ditto": {
        "FY25 Revenue": 103, "FY26 Revenue": 149,
        "FY25 EBITDA": 3, "FY26 EBITDA": 11,
        "NPS": 74, "Employee Satisfaction": 91,
        "Retention": 88, "Cash": 42, "Debt": 0,
    },
    "CoverGrid": {
        "FY25 Revenue": 121, "FY26 Revenue": 174,
        "FY25 EBITDA": 8, "FY26 EBITDA": 16,
        "NPS": 42, "Employee Satisfaction": 68,
        "Retention": 92, "Cash": 14, "Debt": 28,
    },
}

decision_matrix = {
    "criteria": [
        "Strategic fit",
        "Financial value",
        "Brand/culture preservation",
        "Regulatory risk (inverted)",
        "Execution complexity (inverted)",
    ],
    "weights": [0.25, 0.25, 0.20, 0.15, 0.15],
    "As-is":               [3, 2, 2, 2, 2],
    "Renegotiate/Phased":  [5, 5, 4, 4, 3],
    "Control, no earnout": [4, 4, 4, 4, 4],
    "Partnership":         [2, 3, 5, 5, 5],
    "Walk away":           [1, 2, 5, 5, 5],
}
# Weighted totals (for reference): As-is 2.25, Phased 4.35, Control 4.00,
# Partnership 3.75, Walk away 3.25

valuation_bridge = {
    "Ditto": {
        "EV_Revenue": 596, "EV_EBITDA": 418, "Blended_EV": 507,
        "Cash": 42, "Debt": 0, "Equity_Value": 549,
    },
    "CoverGrid": {
        "EV_Revenue": 400.2, "EV_EBITDA": 288, "Blended_EV": 344.1,
        "Cash": 14, "Debt": 28, "Equity_Value": 330.1,
    },
}

sanity_check = {
    "combined_standalone_equity": 879.1,
    "proposed_stake_pct": 0.30,
    "implied_equity_consideration": 263.7,
    "proposed_cash": 25.0,
    "total_implied_consideration": 288.7,
    "covergrid_standalone_equity": 330.1,
    "implied_discount_pct": -0.125,
}

phase1_sizing = {
    "covergrid_standalone_equity": 330.1,
    "control_premium_pct": 0.10,
    "value_of_51pct_stake": 185.2,
    "cash_portion": 10.0,
    "primary_equity_issuance": 175.2,
}

synergy_build = {
    "years": [1, 2, 3],
    "eligible_base": 580000,
    "conversion_rates": [0.02, 0.05, 0.08],  # default Year1/2/3 rates
    "arpu": 6500,
    "take_rate": 0.22,
}


def compute_synergy(conversion_rates, eligible_base=580000, arpu=6500, take_rate=0.22):
    """Recompute incremental revenue to Ditto for given conversion rates (list of 3)."""
    results = []
    for rate in conversion_rates:
        converted = eligible_base * rate
        gross_revenue_cr = (converted * arpu) / 1e7  # convert to crore
        incremental_cr = gross_revenue_cr * take_rate
        results.append(round(incremental_cr, 2))
    return results


deal_structure_comparison = [
    {"Term": "Structure",
     "Original proposal": "100% merger, day 1",
     "Recommended structure": "Phase 1: acquire 51% (control). Phase 2 (18-24mo): "
                               "call option on remaining 49%, linked to KPIs"},
    {"Term": "Equity to CoverGrid holders",
     "Original proposal": "30% of combined entity, upfront",
     "Recommended structure": "13-15% now; further 8-10% only if Phase-2 KPIs hit"},
    {"Term": "Cash consideration",
     "Original proposal": "₹25cr upfront",
     "Recommended structure": "₹10cr at Phase-1 close + ₹15cr staged against Phase-2"},
    {"Term": "Founder role",
     "Original proposal": "Full 3-yr leadership, unchanged",
     "Recommended structure": "Business Unit Heads under joint governance committee "
                               "with a Ditto co-lead"},
    {"Term": "Brand",
     "Original proposal": "CoverGrid brand for 18 months, undefined after",
     "Recommended structure": "Dual-brand (\"CoverGrid, a Ditto company\") for 18 "
                               "months, hard migration date set at signing"},
]

roadmap_milestones = [
    {"milestone": "Phase-1 close (51% stake)", "timing": "Day 0",
     "owner": "Joint deal team"},
    {"milestone": "Governance committee stood up; BU Heads confirmed",
     "timing": "Day 0-30", "owner": "Ditto + CoverGrid leadership"},
    {"milestone": "Advisory-standards training for CoverGrid sales teams",
     "timing": "Day 30-90", "owner": "Ditto L&D"},
    {"milestone": "Incentive structure redesign live", "timing": "Day 90",
     "owner": "HR / RevOps"},
    {"milestone": "Cross-sell pilot (Year 1 conversion cohort)",
     "timing": "Month 3-6", "owner": "Growth team"},
    {"milestone": "KPI review - NPS, retention, cross-sell vs. Phase-2 targets",
     "timing": "Month 12-18", "owner": "Governance committee"},
    {"milestone": "Phase-2 decision (exercise call option or not)",
     "timing": "Month 18-24", "owner": "Ditto Board"},
]
