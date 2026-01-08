import pandas as pd
import numpy as np
import streamlit as st
st.set_page_config(
    page_title="EV Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded")

# ---Page Setup ---
home_page = st.Page(
    page="_pages_disabled/0_home.py",
    title ="Home",
    icon= ":material/home:")

ev_exp=st.Page(
    page="_pages_disabled/1_ev_exp.py",
    title="EV Explorer",
    icon=":material/explore:"
)
ev_sales = st.Page(
    page="_pages_disabled/2_ev_sales.py",
    title="EV Market Trends",
    icon=":material/grouped_bar_chart:"
)
charg_ins = st.Page(
    page = "_pages_disabled/3_charge_insights.py",
    title="Charge Insights",
    icon=":material/mobile_charge:"
)
pred=st.Page(
    page="_pages_disabled/4_prediction.py",
    title="Prediction",
    icon=":material/label:"
)

# --- Navigation setup--
pg=st.navigation(pages=[home_page,ev_exp,ev_sales,charg_ins,pred])

# --- Run navigation---
pg.run()

