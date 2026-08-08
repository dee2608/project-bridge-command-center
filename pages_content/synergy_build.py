import streamlit as st
import plotly.graph_objects as go
from data import synergy_build, company_snapshot, compute_synergy


def render():
    st.subheader("Synergy Build: 3-Year Cross-Sell Model")
    st.caption("Eligible base × conversion rate × avg. revenue per converted "
               "customer × Ditto's take-rate. Drag the Year 3 conversion rate "
               "to stress-test the model.")

    sb = synergy_build
    default_y3 = int(sb["conversion_rates"][2] * 100)

    y3_rate = st.slider(
        "Year 3 conversion rate (%)",
        min_value=3, max_value=15,
        value=st.session_state.get("synergy_y3_rate", default_y3),
        step=1,
        key="synergy_y3_rate",
        help="Year 1 and Year 2 rates scale proportionally with this. "
             "Set automatically when you pick a scenario in the sidebar."
    )

    # Scale Y1/Y2 proportionally to the Y3 slider, keeping the case's ramp shape
    ratio = y3_rate / (sb["conversion_rates"][2] * 100)
    scaled_rates = [
        sb["conversion_rates"][0] * ratio,
        sb["conversion_rates"][1] * ratio,
        y3_rate / 100,
    ]

    revenues = compute_synergy(scaled_rates, sb["eligible_base"], sb["arpu"], sb["take_rate"])

    fig = go.Figure(go.Bar(
        x=[f"Year {y}" for y in sb["years"]],
        y=revenues,
        text=[f"₹{r}cr" for r in revenues],
        textposition="outside",
        marker_color="#0F6E5C",
    ))
    fig.update_layout(
        title="Incremental Revenue to Ditto (₹ crore)",
        yaxis_title="₹ crore",
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True)

    covergrid_ebitda = company_snapshot["CoverGrid"]["FY26 EBITDA"]
    year3_revenue = revenues[-1]
    pct_of_ebitda = (year3_revenue / covergrid_ebitda) * 100

    m1, m2, m3 = st.columns(3)
    m1.metric("Year 1 revenue", f"₹{revenues[0]}cr")
    m2.metric("Year 3 revenue", f"₹{revenues[2]}cr")
    m3.metric("Year 3 vs. CoverGrid's FY26 EBITDA (₹16cr)", f"{pct_of_ebitda:.0f}%")

    st.info(
        "Even at a conservative conversion range, cross-sell revenue alone "
        "approaches CoverGrid's entire current FY26 EBITDA by Year 3 — that's "
        "the number to lead with, not the phrase 'huge new revenue stream.'"
    )

    with st.expander("Other synergy levers (directional)"):
        st.markdown(
            "- **Lower blended CAC**: employer channel offers near-zero "
            "incremental acquisition cost vs. Ditto's retail paid/organic cost.\n"
            "- **Higher LTV**: capturing customers at 22-24 vs. ~35 extends the "
            "advisory relationship by 10+ years.\n"
            "- **Back-office/opex savings**: shared claims support and tech "
            "stack, realistic from Year 2 once systems integrate."
        )
