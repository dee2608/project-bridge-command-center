import streamlit as st
from pages_content import decision_matrix, valuation_bridge, synergy_build, \
    deal_structure, roadmap

st.set_page_config(
    page_title="Project Bridge — Deal Command Center",
    layout="wide",
)

st.title("Project Bridge — Deal Command Center")
st.caption(
    "The Ditto–CoverGrid Merger | MnAnalyse, Finance & Economics Club, IIT Guwahati | "
    "All figures illustrative, per the case pack disclaimer."
)

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
