# earthquake_analysis.py

import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set page settings
st.set_page_config(page_title=" Earthquake Dashboard", layout="wide")

# Title
st.title("Global Earthquake Data Analysis")

# Load the data
@st.cache_data
def load_data():
    file_path = "earthquake_data.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path, parse_dates=["Date"])
    else:
        st.error(" 'earthquake_data.csv' file not found.")
        return pd.DataFrame()

df = load_data()

# Show the raw data
if not df.empty:
    st.subheader("📄 Raw Earthquake Data")
    st.dataframe(df.head())

    # Summary statistics
    st.subheader(" Summary Statistics")
    st.write(df.describe())

    # Filter by Magnitude
    st.subheader("🔍 Filter by Magnitude")
    min_mag, max_mag = st.slider("Select magnitude range", 0.0, 10.0, (4.0, 7.0), 0.1)
    filtered_df = df[(df["Magnitude"] >= min_mag) & (df["Magnitude"] <= max_mag)]

    st.write(f"Showing earthquakes with magnitude between {min_mag} and {max_mag}")
    st.dataframe(filtered_df)

    # Map of Earthquakes
    st.subheader("🗺️ Earthquake Locations Map")
    fig = px.scatter_geo(filtered_df,
                         lat="Latitude",
                         lon="Longitude",
                         color="Magnitude",
                         size="Magnitude",
                         hover_name="Region",
                         projection="natural earth",
                         title="Earthquake Locations")
    st.plotly_chart(fig, use_container_width=True)

    # Histogram of Magnitudes
    st.subheader("📈 Earthquake Magnitude Distribution")
    fig2 = px.histogram(filtered_df, x="Magnitude", nbins=20, color="Region", title="Magnitude Histogram")
    st.plotly_chart(fig2)

    # Earthquake Count by Region
    st.subheader(" Earthquake Count by Region")
    region_count = filtered_df["Region"].value_counts().reset_index()
    region_count.columns = ["Region", "Count"]
    fig3 = px.bar(region_count, x="Region", y="Count", title="Earthquake Frequency by Region")
    st.plotly_chart(fig3)

    st.markdown("---")
    st.caption("Data Source: USGS Earthquake Catalog")
