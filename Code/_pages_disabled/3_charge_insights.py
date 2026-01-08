from operator import index
import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.markdown("# ⚡ Powering the EV Ecosystem: Charging Insights",text_alignment='center')
df1= pd.read_excel('../Data/chargingstation_india.xlsx')
df3=pd.read_csv("../Data/df3_ev_india.csv")
y_max = df1["No. of Operational PCS"].max()
c1,c2=st.columns(2)
fig=px.bar(
    df1,
    x=df1['State Name'],
    y=df1['No. of Operational PCS'],
    labels={"x": "States / UTs","y":" No. of PCS"},
    title="⚡ State-wise Operational Public EV Charging Stations in India"


)
fig.update_layout(
    xaxis_tickangle=-45,
    yaxis=dict(
        range=[0, 6000* 1.1],
        tickformat="~s"
    )
    
)
c1.plotly_chart(fig, use_container_width=True)

top_20_brands = (
    df3
    .groupby("brand")["rating"]
    .mean()
    .sort_values(ascending=False)
    .head(20)
    .index
)
df_top = df3[df3["brand"].isin(top_20_brands)]
df_charge = (
    df_top
    .groupby("brand", as_index=False)
    .agg(
        ac_time_hr=("charging_time_hours", "mean"),
        dc_time_min=("dc_charge_time_mins", "mean")
    )
)
df_charge["dc_time_hr"] = df_charge["dc_time_min"] / 60
    
fig1 = go.Figure()

fig1.add_trace(
    go.Scatter(
        x=df_charge["brand"],
        y=df_charge["ac_time_hr"],
        mode="lines+markers",
        name="AC Charging Time (hrs)"
    )
)

fig1.add_trace(
    go.Scatter(
        x=df_charge["brand"],
        y=df_charge["dc_time_hr"],
        mode="lines+markers",
        name="DC Charging Time (hrs)"
    )
)

fig1.update_layout(
    title="AC vs DC Charging Time for Top 20 EV Brands",
    xaxis_title="EV Brands",
    yaxis_title="Charging Time (Hours)",
    hovermode="x unified"
)

fig1.update_xaxes(tickangle=-45)

c2.plotly_chart(fig1, use_container_width=True)

state_ev_tariff = {
            "Andaman & Nicobar": 12.0,
            "Andhra Pradesh": 6.7,
            "Arunachal Pradesh": 5.0,
            "Assam": 6.0,
            "Bihar": 8.72,
            "Chandigarh": 3.8,
            "Chhattisgarh": 6.92,
            "Dadra & Nagar Haveli and Daman & Diu": 5.5,
            "Delhi": 4.5,
            "Goa": 4.75,
            "Gujarat": 4.2,
            "Haryana": 6.48,
            "Himachal Pradesh": 5.5,
            "Jharkhand": 6.2,
            "Jammu & Kashmir": 5.2,
            "Karnataka": 5.0,
            "Kerala": 5.0,
            "Ladakh": 5.5,
            "Lakshadweep": 7.8,
            "Madhya Pradesh": 6.9,
            "Maharashtra": 4.3,
            "Manipur": 6.0,
            "Meghalaya": 8.5,
            "Mizoram": 6.0,
            "Nagaland": 6.0,
            "Odisha": 5.0,
            "Puducherry": 5.75,
            "Punjab": 6.28,
            "Rajasthan": 6.0,
            "Sikkim": 5.5,       
    "       Tamil Nadu": 7.0,
            "Telangana": 6.0,
            "Tripura": 5.8,   
            "Uttar Pradesh": 6.5,
            "Uttarakhand": 7.0,
            "West Bengal": 6.0
        }
charger_efficiency = {
            "Level 1 (Slow Charging)": 0.87,
            "Level 2(Fast Charging)": 0.92,
            "Level 3(DC Fast Charging)": 0.95
        }
charger_power={
            'Level 1 (Slow Charging)': 3.5,
            'Level 2(Fast Charging)':7.2,
            'Level 3(DC Fast Charging)':65
        }
st.markdown("## Charging Time/Cost Calculator")
c11,c12=st.columns(2)
with c11:
    with st.container(border=True):
        battery_capacity=st.selectbox("Battery Capacity",["Vehicle","Battery Capacity"],help="Choose Vehicle name if you want to enter Battery Capacity automatically," \
            "or enter battery capacity manually",placeholder="Choose an option",index=None)
        if battery_capacity=="Vehicle":
            vehicle=st.selectbox("Car",
                    sorted(df3['name'].dropna().unique().tolist()),index=None)
            if vehicle:
            
                battery_cap=df3[df3["name"]==vehicle]['battery_kWh'].values[0]
                st.metric("Battery Capacity",f"{battery_cap} kWh")
        elif battery_capacity=="Battery Capacity":
            battery_cap = st.number_input("Battery Capacity in kWh",min_value=10, value=40,step=1)
        batt_level1=st.number_input("Current Battery Level %",min_value=0,max_value=100,value=20)
        batt_level2=st.number_input("Target Battery Level %",min_value=0,max_value=100,value=80)
    
        if batt_level1>=batt_level2:
                st.error("Target Battery Level should be higher than Current level")
        
                
            

with c12:
    with st.container(border=True):
        char_type = st.selectbox("EV Charger Types",["Level 1 (Slow Charging)","Level 2(Fast Charging)","Level 3(DC Fast Charging)"],
                             help="Efficiency losses are considered for realistic cost estimation",index=None)

        
        selected_state = st.selectbox(
            "Select State / UT",
            sorted(state_ev_tariff.keys()),
            help="Electricity tariff used to estimate EV charging cost",index=None
        )
        st.caption("ℹ️ Values may vary by operator and time-of-day")
        


b1,b2=st.columns(2)
button1=b1.button("Calculate Charging Time",use_container_width=True)
button2=b2.button("Calculate Charging Cost",width='stretch')


if button1:
        
    if battery_capacity is None:
        st.error("Please select Battery Capacity option")
    elif battery_capacity == "Vehicle" and 'battery_cap' not in locals():
        st.error("Please select a vehicle")
    elif char_type is None:
        st.error("Please select charger type")
    elif batt_level1 >= batt_level2:
        st.error("Target Battery Level must be higher than Current level")
    else:
        battery_needed = (batt_level2 - batt_level1) / 100
        charge_needed = battery_cap * battery_needed
        charging_time = charge_needed / (charger_power[char_type] * 0.9)
        st.metric("Charging Time", f"{charging_time:.1f} hrs")

elif button2:
    try:

        price_per_kwh = state_ev_tariff[selected_state]
        st.metric("Base EV Tariff (₹/kWh)", f"₹ {price_per_kwh}")
        efficiency = charger_efficiency[char_type]
        battery_energy = battery_cap * (batt_level2 - batt_level1) / 100
        grid_energy = battery_energy / efficiency
        charging_cost = grid_energy * price_per_kwh
        st.metric(
        "Charging Cost (₹) to charge for given target battery level",
        f"{charging_cost:.2f}",
        help="Estimated cost based on selected tariff and energy required"
    )
    except:
        st.error("Please enter all the required fields")


