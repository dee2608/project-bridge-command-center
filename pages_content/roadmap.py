import streamlit as st
from data import roadmap_milestones

STATUS_OPTIONS = ["On track", "At risk", "Delayed"]


def render():
    st.subheader("100-Day / Phased Integration Roadmap")
    st.caption(
        "Set a status per milestone — the overall phase health banner below "
        "updates live."
    )

    header = st.columns([3, 2, 2, 2])
    header[0].markdown("**Milestone**")
    header[1].markdown("**Timing**")
    header[2].markdown("**Owner**")
    header[3].markdown("**Status**")

    statuses = []
    for i, m in enumerate(roadmap_milestones):
        c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
        c1.write(m["milestone"])
        c2.write(m["timing"])
        c3.write(m["owner"])
        status = c4.selectbox(
            "Status", STATUS_OPTIONS,
            key=f"roadmap_status_{i}",
            label_visibility="collapsed",
        )
        statuses.append(status)

    st.divider()
    if "Delayed" in statuses:
        st.error("🔴 Overall Phase health: **At risk** — one or more milestones are delayed.")
    elif "At risk" in statuses:
        st.warning("🟡 Overall Phase health: **Caution** — some milestones need attention.")
    else:
        st.success("🟢 Overall Phase health: **On track**")

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
