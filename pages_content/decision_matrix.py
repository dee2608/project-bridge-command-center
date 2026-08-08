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
    df = pd.concat([df, pd.DataFrame([totals_row])],
