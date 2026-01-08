
from operator import index
import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.express as px
st.markdown("# Comparative Analysis of Global and Indian EV Markets 🌍",text_alignment='center')
@st.cache_data(show_spinner=False)
def load_sales_data():
    df1 = pd.read_csv("../Data/ev_statewise_final.csv")
    df2 = pd.read_csv("../Data/evexplorer_1.csv")
    return df1, df2

df1, df2 = load_sales_data()
display_map = {
        "jan": "January", "feb": "February", "mar": "March",
        "apr": "April", "may": "May", "jun": "June",
        "jul": "July", "aug": "August", "sep": "September",
        "oct": "October", "nov": "November", "dec": "December"
    }

month_order = list(display_map.keys())

r=st.radio("Electric Vehicle Adoption: Global vs India",
           ["EV Sales by States in India","EV Sales by Year in India","Global EV Trends"],
           horizontal=True)
if r=='EV Sales by States in India':
    filtered_df = df1.copy()

    with st.container(border=True):
        st.markdown("### State-wise EV Performance in India")
        c1,c2=st.columns(2)
        year=c1.selectbox(
                "Year",
                ["All"] + sorted(filtered_df['Year'].dropna().unique(),reverse=True)
                )
        if year != "All":
            filtered_df=filtered_df[filtered_df['Year']==year]
        available_months = [
            m for m in month_order
            if m in filtered_df["Month_name"].str.lower().unique()
        ]
        display_months = ["All"] + [display_map[m] for m in available_months]

        month_display = c2.selectbox(
            "Month",
            display_months
        )
        if month_display != "All":
            month_key = [k for k, v in display_map.items() if v == month_display][0]
            filtered_df = filtered_df[filtered_df["Month_name"].str.lower() == month_key]

        if filtered_df.empty:
            st.warning("No EVs match the selected filters.")
        else:
            c3,c4=st.columns(2)
            df1_year=(
                filtered_df.groupby('State')['ELECTRIC(BOV)']
                .sum()
                .sort_values(ascending=True)
                )
            fig = px.bar(
                df1_year,
                x=df1_year.values,
                y=df1_year.index,
                orientation="h",
                labels={"x": "EV Sales", "y": "State"},
                title="EV Sales by State"
                
                )
            c3.plotly_chart(fig)
            df1_pent = (
                df1.groupby('State')['Perc']
                .mean()
                .sort_values(ascending=True)
            )

            fig1 = px.bar(
                df1_pent,
                x=df1_pent.values,
                y=df1_pent.index,
                orientation="h",
                labels={"x":"EV Penetration","y":"State"},
                title="EV Penetration by State"
            )
            fig1.update_traces(
                
                hovertemplate="State: %{y}<br>EV Penetration: %{x:.2f}%<extra></extra>",
                )

            c4.plotly_chart((fig1))

elif r=="EV Sales by Year in India":
     with st.container(border=True):
        c1,c2=st.columns(2)
        state=c1.selectbox(
                "State",
                ["All"] + sorted(df1['State'].dropna().unique().tolist(),reverse=True)
                )
        if state != "All":
            df1=df1[df1['State']==state]
        if df1.empty:
            st.warning("No EVs match the selected filters.")
        else:
            c3,c4=st.columns(2)
            df1_state=(
                df1.groupby('Year')['ELECTRIC(BOV)']
                .sum()
                .sort_values(ascending=True)
                )
            fig = px.bar(
                df1_state,
                x=df1_state.index,
                y=df1_state.values,
                labels={"x": "EV Sales", "y": "Year"},
                title="EV Sales by Year"
                
                )
            c3.plotly_chart(fig)
            df1_year = (
                df1
                .groupby("Year", as_index=False)
                .agg({
                    "ELECTRIC(BOV)": "sum",
                    "Total": "sum"
                })
            )

            df1_year["EV_Penetration"] = (
                df1_year["ELECTRIC(BOV)"] / df1_year["Total"] * 100
            )
            fig1 = px.line(
                df1_year,
                x="Year",
                y="EV_Penetration",
                markers=True,
                labels={
                    "Year": "Year",
                    "EV_Penetration": "EV Penetration (%)"
                },
                title="EV Penetration Over Time"
            )
            fig1.update_traces(
                texttemplate="%{y:.2f}%",
                textposition="top center",
                hovertemplate=(
                    "Year: %{x}<br>"
                    "EV Penetration: %{y:.2f}%<extra></extra>"
                )
            )

            c4.plotly_chart(fig1, use_container_width=True)
        
            
elif r=="Global EV Trends":
    with st.container(border=True):
        r1=st.radio("Select",["Historical","Projected"],horizontal=True)
        c1,c2=st.columns(2)
        if r1=='Historical':
            df2=df2[df2['category']=='Historical']
        else:
            df2=df2[df2['category']>='Projection-STEPS']

        show=c1.selectbox("Show",
                        sorted(df2['parameter'].dropna().unique().tolist()),index=1)
    
        df2=df2[df2['parameter']==show]
        options=sorted(df2['region_country'].dropna().unique().tolist())
        region=c2.selectbox("Region",options,
                            index=options.index("World")
        )

        df2=df2[df2['region_country']==region]
        if show=='Battery demand':

            df2_gwh = df2.groupby('year')['value'].max()
            fig=px.bar(
                df2_gwh,
                x=df2_gwh.index,
                y=df2_gwh.values,
                labels={"x": "Year","y":'GWh'},
                title=f"{show} of {region},2010-2024"
            )
        elif show=='EV sales':
            df2_sales = df2.groupby('year')['value'].sum()
            fig=px.bar(
                df2_sales,
                x=df2_sales.index,
                y=df2_sales.values,
                labels={"x": "Year","y":'Vehicles'},
                title=f"{show} of {region},2010-2024"
            )
        else:
            df2_sales = df2.groupby('year')['value'].mean()
            fig=px.bar(
                df2_sales,
                x=df2_sales.index,
                y=df2_sales.values,
                labels={"x": "Year","y":df2['unit'].unique()[0]},
                title=f"{show} of {region},2010-2024"
            )
        

        st.plotly_chart(fig,use_container_width=True)
        



