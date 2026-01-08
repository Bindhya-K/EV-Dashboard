import streamlit as st
import time
import pandas as pd
import numpy as np
st.markdown("# Electric Vehicle(cars) Analytics Dashboard 🚗⚡",text_alignment='center')
@st.cache_data(show_spinner=False)
def load_home_data():
    df2 = pd.read_csv("../Data/main_data.csv")
    df4 = pd.read_csv("../Data/top_models.csv")
    return df2, df4


@st.cache_data
def compute_kpis(df):
    models_by_year = df.groupby("release_year")["model"].nunique()
    brands_by_year = df.groupby("release_year")["brand"].nunique()
    return models_by_year, brands_by_year
df2, df4 = load_home_data()

col1,col2,col3=st.columns(3,gap='medium',vertical_alignment='top',border=True)

models_by_year, brands_by_year = compute_kpis(df2)
with col1:
    st.metric(
        "Total Models",
        df2['model'].nunique(),
        chart_data=models_by_year,
        chart_type="line",
        border=True
    )
with col2:
    st.metric(
        "Total brands",
        df2['brand'].nunique(),
        chart_data=brands_by_year,
        chart_type="bar",
        border=True
    )
with col3:
    st.metric(
        "Average Battery Capacity",
        f"{df2['battery_kwh'].mean():.0f} kWh",
        border=True
    )

    st.metric(
        label="Average Energy Consumption",
        value=f"{df2['energy_consumption'].mean():.2f} kWh/km",
        border=True
    )
st.markdown("## 🔝 Top EV Models")
df4_30=df4.head(30)

p1= st.empty()


for _, row in df4_30.iterrows():
    with p1.container(border=True):
        col_img, col_text = st.columns([1.2, 1])
        with col_img:
            st.image(row["image"], use_container_width=True)
        with col_text:
            st.markdown(f"""
            <div style="
                text-align:center;
                font-size:18px;
                font-weight:600;
                line-height:1.8;
            ">
                <h3 style="margin-bottom:12px;">{row['name']}</h3>
                <p><strong>Price:</strong> {row['price']}</p>
                <p><strong>Range:</strong> {row['range']} km</p>
                <p><strong>Efficiency:</strong> {row['effeciency']}</p>
                <p><strong>Battery:</strong> {row['battery']} kWh</p>
            </div>
            """, unsafe_allow_html=True)

    time.sleep(2)   # change every 2 seconds
    p1.empty()
    
