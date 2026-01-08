import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pickle
df=pd.read_csv("../Data/df3_ev_india.csv")
@st.cache_resource
def load_models():
    with open("range_model.pkl", "rb") as f:
        range_model = pickle.load(f)
    with open("price_model.pkl", "rb") as f:
        price_model = pickle.load(f)
    return range_model, price_model

range_model, price_model = load_models()

st.markdown("""
### 🔮 EV Range & Price Prediction

Lightweight regression models were trained using limited real-world EV data available in India.

• **Range prediction** shows moderate accuracy, as EV range is primarily driven by battery capacity and motor power.  
• **Price prediction** is more challenging due to brand premiums and feature variations, and is presented as an indicative estimate.

> ⚠️ *Predictions are approximate and intended for analytical insights, not exact valuations.*
""")

c1, c2 = st.columns(2)
with c1:
    st.subheader("🔋 EV Range Prediction")
    with st.container(border=True):
        c11, c12 = st.columns(2)

        with c11:
            battery = st.slider("Battery Capacity (kWh)", 20, 120, 50)
            motor = st.slider("Motor Power (kW)", 50, 500, 150)
            seater = st.selectbox("Seater", sorted(df["seater"].unique()))

        with c12:
            body = st.selectbox("Body Type", sorted(df["body_type"].dropna().unique()))
            drive = st.selectbox("Drive Type", sorted(df["drive_type"].dropna().unique()))

        input_range = pd.DataFrame([{
            "battery_kWh": battery,
            "motor_power_kW": motor,
            "seater": seater,
            "body_type": body,
            "drive_type": drive
        }])
        pred_range = range_model.predict(input_range)[0]
        b1=st.button("Predict Range",width='stretch')
        if b1:
            st.metric("Estimated Driving Range", f"~{int(pred_range)} km")
with c2:
    st.subheader("💰 EV Price Estimate")
    with st.container(border=True):
        c21, c22 = st.columns(2)
    
        with c21:
            battery1 = st.slider("Battery Capacity (kWh)", 20, 120, 50,key="price_battery")
            motor1 = st.slider("Motor Power (kW)", 50, 500, 150,key="price_motor")
            seater1 = st.selectbox("Seater", sorted(df["seater"].unique()),key="price_seater")

        with c22:
            body = st.selectbox("Body Type", sorted(df["body_type"].dropna().unique()),key="price_body")

            brand = st.selectbox("Brand", sorted(df["brand"].unique()))
            range_km = st.slider("Range (km)", 150, 900, 400)

        input_price = pd.DataFrame([{
            "battery_kWh": battery1,
            "motor_power_kW": motor1,
            "range_km": range_km,
            "seater": seater1,
            "brand": brand,
            "body_type": body
        }])
        b2=st.button("Predict Price",width='stretch')
        if b2:
            pred_price = price_model.predict(input_price)[0]

            st.metric("Estimated Price", f"₹ {round(pred_price, 0):,.0f} Lakhs")

