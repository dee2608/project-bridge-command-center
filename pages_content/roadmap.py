import streamlit as st
import pandas as pd
from data import roadmap_milestones


def render():
    st.subheader("100-Day / Phased Integration Roadmap")
    st.caption("Milestones from Phase-1 close through the Phase-2 KPI decision.")

    df = pd.DataFrame(roadmap_milestones)
    df.columns = ["Milestone", "Timing", "Owner"]

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("#### Phase breakdown")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Phase 1 — Day 0 to Month 6**")
        st.write("Control acquired, governance stood up, training and incentive "
                 "redesign complete, cross-sell pilot launched.")
    with c2:
        st.markdown("**Phase 2 — Month 12 to Month 24**")
        st.write("KPI review against NPS recovery, retention quality and "
                 "cross-sell traction, followed by the Board's call-option "
                 "decision on the remaining 49%.")
