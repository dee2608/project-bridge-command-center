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
