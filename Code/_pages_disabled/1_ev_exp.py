
import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data(show_spinner=False)
def load_ev_data():
    df1 = pd.read_csv("../Data/df3_ev_india.csv")
    df2 = pd.read_csv("../Data/top_models.csv")
    return df1, df2
@st.cache_data
def compute_ev_stats(df):
    rating_by_brand = df.groupby("name")["rating"].mean().sort_values()
    models_per_brand = df.groupby("brand")["model"].count().sort_values()
    body_counts = df["body_type"].value_counts().reset_index()
    body_counts.columns = ["body_type", "count"]
    brand_range = (
        df.groupby("brand")["range_km"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    return rating_by_brand, models_per_brand, body_counts, brand_range
st.markdown("""
<style>
/* Make tabs container full width */
div[data-baseweb="tab-list"] {
    width: 100%;
    justify-content: space-between;
}

/* Make each tab stretch equally */
button[data-baseweb="tab"] {
    flex-grow: 1;
    text-align: center;
    font-size: 18px;
    font-weight: 600;
     border-radius: 12px 12px 0 0;
}

/* Optional: active tab underline thicker */
button[data-baseweb="tab"][aria-selected="true"] {
    border-bottom: 3px solid #ff4b4b;
}
</style>
""", unsafe_allow_html=True)
st.markdown("# Electric Vehicle(cars) Analytics Dashboard 🚗⚡",text_alignment='center')


df1, df2 = load_ev_data()
tab1,tab2=st.tabs([" 🔍 Filter EVs","📊 Technical Specs"],)

with tab1:
    st.header("Filter EVs")
    filtered_df = df1.copy()
    with st.container(border=True):
        c1,c2,c3=st.columns(3)
        brand = c1.selectbox(
            "Manufacturer",
            ["All"] + sorted(df1['brand'].dropna().unique())
            )
        if brand != "All":
            filtered_df = filtered_df[filtered_df['brand'] == brand]
        body = c2.selectbox(
            "Body Type",
            ["All"] + sorted(filtered_df['body_type'].dropna().unique())
        )
        if body != "All":
            filtered_df = filtered_df[filtered_df['body_type'] == body]
        port = c3.selectbox(
            "Charging Type",
            ["All"] + sorted(filtered_df['charging_port'].dropna().unique())
        )
        if port != "All":
            filtered_df = filtered_df[filtered_df["charging_port"] == port]
        min_range=int(filtered_df['range_km'].min())
        max_range = int(filtered_df['range_km'].max())
        if min_range!=max_range:
            range=st.slider("Range in km",int(min_range),int(max_range),(int(max_range),int(min_range)))
            filtered_df = filtered_df[
                filtered_df["range_km"].between(range[0], range[1])
            ]
        else:
            range=min_range
            filtered_df=filtered_df[filtered_df['range_km']==range]
    
    filtered_df=filtered_df.head(4)
    with st.container():
        if filtered_df.empty:
            st.warning("No EVs match the selected filters.")
        else:
            cols = st.columns(2)
            col_index = 0

            for _, row in filtered_df.iterrows():
                with cols[col_index]:
                    with st.container(border=True):
                        col_img,col_text=st.columns([1.2, 1])
                        with col_img:
                            st.image(row["img"], use_container_width=True)
                        with col_text:
                            st.markdown(
                                f"""
                                <h3 style="margin-bottom:3px;">{row['model']}</h3>
                                <p>Range: <strong>{row['range_km']} km</strong></p>
                                <p>₹ {row['price in lakhs']} lakhs</p>
                                """,
                                unsafe_allow_html=True
                            )

                col_index = (col_index + 1) % 2
                if col_index == 0:
                    cols = st.columns(2)    

with tab2:
    rating_by_brand, models_per_brand, body_counts, brand_range = compute_ev_stats(df1)
    c1,c2=st.columns(2)
    
    top10_brand = models_per_brand.tail(10)
    top10 = rating_by_brand.tail(10)

    fig = px.bar(
        top10,
        x=top10.values,
        y=top10.index,
        orientation="h",
        labels={"x": "Average Rating", "y": "Manufacturer"},
        title="Top 10 Manufacturers in India by Average Rating"
    )

    fig.update_layout(
        height=350,
        yaxis=dict(title=""),
        xaxis=dict(range=[0, 5])  # assuming rating out of 5
    )

    c1.plotly_chart(fig)
    fig1 = px.bar(
        top10_brand,
        x=top10_brand.values,
        y=top10_brand.index,
        orientation="h",
        labels={"x": "EV Models", "y": "Manufacturer"},
        title="Top 10 Manufacturers in India by number of models "
    )

    fig1.update_layout(
        height=350,
        yaxis=dict(title=""),
        xaxis=dict(range=[0, 9])  # assuming rating out of 5
    )
    c2.plotly_chart(fig1)

    c3,c4=st.columns(2)
    # Battery Capacity Distribution
    c3.plotly_chart(
        px.histogram(df1, x="battery_kWh", nbins=20,
                     title="Battery Capacity Distribution"),
        use_container_width=True
    )
    c4.plotly_chart(
        px.scatter(df1, x="battery_kWh", y="range_km", color="brand",
                   title="Range vs Battery"),
        use_container_width=True
    )
    


    c5,c6,c7=st.columns(3)
    c5.plotly_chart(
        px.pie(body_counts, names="body_type", values="count",
               hole=0.55, title="Body Type Distribution"),
        use_container_width=True
    )
    c6.plotly_chart(
        px.histogram(df1, x="price in lakhs", nbins=10,
                     title="Price Distribution"),
        use_container_width=True
    )

    c7.plotly_chart(
        px.bar(brand_range, x="brand", y="range_km",
               title="Average Range by Brand"),
        use_container_width=True
    )
            