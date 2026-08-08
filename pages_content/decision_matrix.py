import streamlit as st
import pandas as pd
from data import decision_matrix, decision_matrix_advisor


def render():
    st.subheader("Weighted Decision Matrix")
    st.caption(
        "Scores 1-5, higher = better. Edit any score directly in the grid below, "
        "or adjust the criteria weights — the weighted totals and winner update live."
    )

    dm = decision_matrix
    options = ["As-is", "Renegotiate/Phased", "Control, no earnout",
               "Partnership", "Walk away"]

    st.markdown("**Criteria weights** (don't need to total 100 — auto-normalized)")
    c1, c2, c3, c4, c5 = st.columns(5)
    w_strategic = c1.number_input(
        "Strategic fit %", 0, 100,
        st.session_state.get("dm_weight_strategic", 25), key="dm_weight_strategic")
    w_financial = c2.number_input(
        "Financial value %", 0, 100,
        st.session_state.get("dm_weight_financial", 25), key="dm_weight_financial")
    w_culture = c3.number_input(
        "Brand/culture %", 0, 100,
        st.session_state.get("dm_weight_culture", 20), key="dm_weight_culture")
    w_reg = c4.number_input(
        "Reg. risk %", 0, 100,
        st.session_state.get("dm_weight_reg", 15), key="dm_weight_reg")
    w_exec = c5.number_input(
        "Execution %", 0, 100,
        st.session_state.get("dm_weight_exec", 15), key="dm_weight_exec")

    weights = [w_strategic, w_financial, w_culture, w_reg, w_exec]
    weight_sum = sum(weights) or 1
    norm_weights = [w / weight_sum for w in weights]

    grid_df = pd.DataFrame({
        "Criterion": dm["criteria"],
        **{opt: dm[opt] for opt in options},
    })

    st.markdown("**Scores grid** — click any cell to edit")
    edited_df = st.data_editor(
        grid_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            opt: st.column_config.NumberColumn(opt, min_value=1, max_value=5, step=1)
            for opt in options
        },
        key="dm_grid_editor",
    )

    weighted_totals = {}
    for opt in options:
        scores = edited_df[opt].tolist()
        total = sum(s * w for s, w in zip(scores, norm_weights))
        weighted_totals[opt] = round(total, 2)

    winner = max(weighted_totals, key=weighted_totals.get)

    summary_df = pd.DataFrame([{"Criterion": "Weighted score / 5", **weighted_totals}])

    def highlight_winner(col):
        return ["background-color: #D6EFE9" if col.name == winner else "" for _ in col]

    st.dataframe(
        summary_df.style.apply(highlight_winner, axis=0),
        use_container_width=True,
        hide_index=True,
    )

    st.success(f"**Highest weighted score: {winner}** ({weighted_totals[winner]}/5)")

    if st.button("🤖 Ask the AI Advisor", key="dm_advisor_btn"):
        st.info(decision_matrix_advisor(weighted_totals, norm_weights))
