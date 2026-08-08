import streamlit as st
import plotly.graph_objects as go
from data import company_snapshot, valuation_advisor


def _waterfall(company, ev_rev, ev_ebitda, cash, debt):
    blended = round((ev_rev + ev_ebitda) / 2, 1)
    equity = round(blended + cash - debt, 1)
    fig = go.Figure(go.Waterfall(
        name=company,
        orientation="v",
        measure=["absolute", "relative", "total", "relative", "relative", "total"],
        x=["EV (Revenue basis)", "EV (EBITDA basis) delta", "Blended EV",
           "+ Cash", "- Debt", "Equity Value"],
        y=[ev_rev, ev_ebitda - ev_rev, 0, cash, -debt, 0],
        text=[f"₹{ev_rev}cr", "", f"₹{blended}cr",
              f"+₹{cash}cr", f"-₹{debt}cr", f"₹{equity}cr"],
        connector={"line": {"color": "rgb(120,120,120)"}},
        decreasing={"marker": {"color": "#C0524A"}},
        increasing={"marker": {"color": "#0F6E5C"}},
        totals={"marker": {"color": "#0A4A3E"}},
    ))
    fig.update_layout(title=f"{company}: Standalone Equity Value Build",
                       showlegend=False, height=420)
    return fig, blended, equity


def render():
    st.subheader("Valuation Bridge")
    st.caption(
        "Edit the multiples below to stress-test the valuation — both waterfalls "
        "and the fairness check recompute live. Defaults reproduce the case's "
        "original figures exactly."
    )

    cs = company_snapshot
    c1, c2, c3, c4 = st.columns(4)
    ditto_rev_mult = c1.number_input(
        "Ditto EV/Revenue x", 1.0, 10.0,
        st.session_state.get("vb_ditto_rev_mult", 4.0), 0.1, key="vb_ditto_rev_mult")
    ditto_ebitda_mult = c2.number_input(
        "Ditto EV/EBITDA x", 5.0, 80.0,
        st.session_state.get("vb_ditto_ebitda_mult", 38.0), 1.0, key="vb_ditto_ebitda_mult")
    cg_rev_mult = c3.number_input(
        "CoverGrid EV/Revenue x", 1.0, 10.0,
        st.session_state.get("vb_covergrid_rev_mult", 2.3), 0.1, key="vb_covergrid_rev_mult")
    cg_ebitda_mult = c4.number_input(
        "CoverGrid EV/EBITDA x", 5.0, 80.0,
        st.session_state.get("vb_covergrid_ebitda_mult", 18.0), 1.0, key="vb_covergrid_ebitda_mult")

    ditto_ev_rev = round(ditto_rev_mult * cs["Ditto"]["FY26 Revenue"], 1)
    ditto_ev_ebitda = round(ditto_ebitda_mult * cs["Ditto"]["FY26 EBITDA"], 1)
    cg_ev_rev = round(cg_rev_mult * cs["CoverGrid"]["FY26 Revenue"], 1)
    cg_ev_ebitda = round(cg_ebitda_mult * cs["CoverGrid"]["FY26 EBITDA"], 1)

    col1, col2 = st.columns(2)
    with col1:
        fig, ditto_blended, ditto_equity = _waterfall(
            "Ditto", ditto_ev_rev, ditto_ev_ebitda, cs["Ditto"]["Cash"], cs["Ditto"]["Debt"])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2, cg_blended, cg_equity = _waterfall(
            "CoverGrid", cg_ev_rev, cg_ev_ebitda, cs["CoverGrid"]["Cash"], cs["CoverGrid"]["Debt"])
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("Sanity Check: What the Original Ask Actually Implies")

    combined_equity = round(ditto_equity + cg_equity, 1)
    implied_equity_consideration = round(combined_equity * 0.30, 1)
    total_consideration = round(implied_equity_consideration + 25, 1)
    diff_pct = (total_consideration - cg_equity) / cg_equity

    m1, m2, m3 = st.columns(3)
    m1.metric("Combined standalone equity", f"₹{combined_equity}cr")
    m2.metric("Total implied consideration to CoverGrid",
              f"₹{total_consideration}cr",
              help="30% of combined value + ₹25cr cash")
    m3.metric("vs. CoverGrid standalone value",
              f"₹{cg_equity}cr",
              delta=f"{diff_pct:.1%}")

    if st.button("🤖 Ask the AI Advisor", key="vb_advisor_btn"):
        st.info(valuation_advisor(total_consideration, cg_equity))
