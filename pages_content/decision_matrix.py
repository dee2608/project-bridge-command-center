import streamlit as st
import pandas as pd
from data import decision_matrix


def render():
    st.subheader("Weighted Decision Matrix")
    st.caption("Scores 1-5, higher = better. Weighted score shows which option "
               "wins once strategic fit, financial value, brand/culture, "
               "regulatory risk and execution complexity are all accounted for.")

    dm = decision_matrix
    options = ["As-is", "Renegotiate/Phased", "Control, no earnout",
               "Partnership", "Walk away"]

    df = pd.DataFrame({
        "Criterion": dm["criteria"],
        "Weight": [f"{w:.0%}" for w in dm["weights"]],
        **{opt: dm[opt] for opt in options},
    })

    weighted_totals = {}
    for opt in options:
        total = sum(score * weight for score, weight in zip(dm[opt], dm["weights"]))
        weighted_totals[opt] = round(total, 2)

    totals_row = {"Criterion": "Weighted score / 5", "Weight": ""}
    totals_row.update(weighted_totals)
    df = pd.concat([df, pd.DataFrame([totals_row])], ignore_index=True)

    winner = max(weighted_totals, key=weighted_totals.get)

    def highlight_winner(col):
        if col.name == winner:
            return ["background-color: #D6EFE9"] * len(col)
        return [""] * len(col)

    st.dataframe(
        df.style.apply(highlight_winner, axis=0),
        use_container_width=True,
        hide_index=True,
    )

    st.success(f"**Highest weighted score: {winner}** ({weighted_totals[winner]}/5) "
               f"— combines the upside of ownership with downside protection.")

    with st.expander("Try a different lens"):
        st.caption("Re-weight the criteria to see if the winner changes.")
        lens = st.radio(
            "Weighting lens",
            ["Case-brief weights (default)", "Financial-value only", "Brand/culture only"],
            horizontal=True,
        )
        if lens == "Financial-value only":
            idx = dm["criteria"].index("Financial value")
            best = max(options, key=lambda o: dm[o][idx])
            st.write(f"On financial value alone, **{best}** scores highest "
                     f"({dm[best][idx]}/5).")
        elif lens == "Brand/culture only":
            idx = dm["criteria"].index("Brand/culture preservation")
            best = max(options, key=lambda o: dm[o][idx])
            st.write(f"On brand/culture preservation alone, **{best}** scores "
                     f"highest ({dm[best][idx]}/5).")
