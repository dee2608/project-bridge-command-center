import streamlit as st
import plotly.graph_objects as go
from data import valuation_bridge, sanity_check


def _waterfall(company, v):
    fig = go.Figure(go.Waterfall(
        name=company,
        orientation="v",
        measure=["absolute", "relative", "total", "relative", "relative", "total"],
        x=["EV (Revenue basis)", "EV (EBITDA basis) delta", "Blended EV",
           "+ Cash", "- Debt", "Equity Value"],
        y=[v["EV_Revenue"],
           v["EV_EBITDA"] - v["EV_Revenue"],
           0,
           v["Cash"],
           -v["Debt"],
           0],
        text=[f"₹{v['EV_Revenue']}cr", "", f"₹{v['Blended_EV']}cr",
              f"+₹{v['Cash']}cr", f"-₹{v['Debt']}cr", f"₹{v['Equity_Value']}cr"],
        connector={"line": {"color": "rgb(120,120,120)"}},
        decreasing={"marker": {"color": "#C0524A"}},
        increasing={"marker": {"color": "#0F6E5C"}},
        totals={"marker": {"color": "#0A4A3E"}},
    ))
    fig.update_layout(title=f"{company}: Standalone Equity Value Build",
                       showlegend=False, height=420)
    return fig


def render():
    st.subheader("Valuation Bridge")
    st.caption("Blended 50/50 EV/Revenue and EV/EBITDA on FY26 numbers, bridged "
               "to equity value via cash and debt. Multiples are illustrative "
               "placeholders — swap in real comps before final submission.")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(_waterfall("Ditto", valuation_bridge["Ditto"]),
                         use_container_width=True)
    with col2:
        st.plotly_chart(_waterfall("CoverGrid", valuation_bridge["CoverGrid"]),
                         use_container_width=True)

    st.divider()
    st.subheader("Sanity Check: What the Original Ask Actually Implies")
    sc = sanity_check
    m1, m2, m3 = st.columns(3)
    m1.metric("Combined standalone equity", f"₹{sc['combined_standalone_equity']}cr")
    m2.metric("Total implied consideration to CoverGrid",
              f"₹{sc['total_implied_consideration']}cr",
              help="30% of combined value + ₹25cr cash")
    m3.metric("vs. CoverGrid standalone value",
              f"₹{sc['covergrid_standalone_equity']}cr",
              delta=f"{sc['implied_discount_pct']:.1%}")

    st.info(
        "The original ask actually implies a **discount** to CoverGrid's own "
        "standalone value on these multiples — not a rich price. The real issue "
        "isn't the headline price, it's that the structure pays it all upfront "
        "with no mechanism tied to whether CoverGrid's problems (falling NPS, "
        "weak culture metrics) actually get fixed. That's the case for a phased, "
        "earn-out structure rather than a straight price cut."
    )
