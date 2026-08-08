import streamlit as st
from data import scenarios, match_prompt_to_scenario
from pages_content import (
    decision_matrix,
    valuation_bridge,
    synergy_build,
    deal_structure,
    roadmap,
)

st.set_page_config(
    page_title="Project Bridge — Deal Command Center",
    layout="wide",
)


def apply_scenario():
    """Push a scenario's preset values into every editable widget's state.
    Rules-based — no external API call."""
    name = st.session_state.get("scenario_select", "Base Case")
    s = scenarios[name]
    st.session_state["dm_weight_strategic"] = int(s["weights"][0] * 100)
    st.session_state["dm_weight_financial"] = int(s["weights"][1] * 100)
    st.session_state["dm_weight_culture"] = int(s["weights"][2] * 100)
    st.session_state["dm_weight_reg"] = int(s["weights"][3] * 100)
    st.session_state["dm_weight_exec"] = int(s["weights"][4] * 100)
    st.session_state["vb_ditto_rev_mult"] = s["ditto_ev_revenue_mult"]
    st.session_state["vb_ditto_ebitda_mult"] = s["ditto_ev_ebitda_mult"]
    st.session_state["vb_covergrid_rev_mult"] = s["covergrid_ev_revenue_mult"]
    st.session_state["vb_covergrid_ebitda_mult"] = s["covergrid_ev_ebitda_mult"]
    st.session_state["synergy_y3_rate"] = s["y3_conversion"]


st.title("Project Bridge — Deal Command Center")
st.caption(
    "The Ditto–CoverGrid Merger | MnAnalyse, Finance & Economics Club, IIT Guwahati | "
    "All figures illustrative, per the case pack disclaimer."
)

with st.sidebar:
    st.header("🤖 AI Scenario Assistant")
    st.caption(
        "Offline, rules-based assistant — no API key required. Pick a scenario "
        "or describe one, and the assumptions update across every tab."
    )
    st.selectbox(
        "Choose a scenario",
        list(scenarios.keys()),
        key="scenario_select",
        on_change=apply_scenario,
    )

    prompt = st.text_input(
        "...or describe one in your own words",
        placeholder="e.g. assume a recession hits",
    )
    if st.button("Apply scenario from prompt"):
        matched = match_prompt_to_scenario(prompt) if prompt else "Base Case"
        st.session_state["scenario_select"] = matched
        apply_scenario()
        st.success(f"Matched to: **{matched}**")

    if st.button("Reset to Base Case"):
        st.session_state["scenario_select"] = "Base Case"
        apply_scenario()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Decision Matrix",
    "Valuation Bridge",
    "Synergy Build",
    "Deal Structure",
    "Roadmap",
])

with tab1:
    decision_matrix.render()

with tab2:
    valuation_bridge.render()

with tab3:
    synergy_build.render()

with tab4:
    deal_structure.render()

with tab5:
    roadmap.render()
