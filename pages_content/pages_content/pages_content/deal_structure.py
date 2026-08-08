import streamlit as st
from data import deal_structure_comparison, phase1_sizing


def render():
    st.subheader("Deal Structure: Original Proposal vs. Recommended Structure")

    for row in deal_structure_comparison:
        st.markdown(f"**{row['Term']}**")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("Original proposal")
            st.warning(row["Original proposal"])
        with c2:
            st.markdown("Recommended structure")
            st.success(row["Recommended structure"])
        st.divider()

    st.subheader("Sizing the Recommended Phase-1 Tranche")
    ps = phase1_sizing
    m1, m2, m3 = st.columns(3)
    m1.metric("CoverGrid standalone equity value", f"₹{ps['covergrid_standalone_equity']}cr")
    m2.metric("Value of 51% stake (incl. 10% control premium)",
              f"₹{ps['value_of_51pct_stake']}cr")
    m3.metric("Funded via primary equity issuance",
              f"₹{ps['primary_equity_issuance']}cr",
              help=f"After ₹{ps['cash_portion']}cr cash portion")

    st.caption(
        "This sizing is illustrative — the real number depends on "
        "due-diligence-adjusted EBITDA and a negotiated control premium. The "
        "structure (phased, earn-out linked) is the actual recommendation; "
        "treat the rupee figures as a starting anchor for negotiation."
    )
