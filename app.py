import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os, time, math

st.set_page_config(
    page_title="PawIndia Dashboard",
    page_icon="🐾",
    layout="wide"
)

@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    raw = pd.read_csv(os.path.join(base, "pawindia_raw_data.csv"))
    df  = pd.read_csv(os.path.join(base, "pawindia_cleaned_data.csv"))
    return raw, df

raw, df = load_data()

n = len(df)

pct_yes   = round((df["Q25_app_adoption"] == "Yes").sum() / n * 100, 1)
pct_maybe = round((df["Q25_app_adoption"] == "Maybe").sum() / n * 100, 1)
pct_no    = round((df["Q25_app_adoption"] == "No").sum() / n * 100, 1)

avg_spend = int(df["Q7_monthly_spend_inr"].mean())

st.sidebar.title("🐾 PawIndia")
page = st.sidebar.radio("Navigation", [
    "Home",
    "Insights",
    "City Explorer"
])

if page == "Home":
    st.title("🐾 PawIndia Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Respondents", n)
    col2.metric("Will Download", f"{pct_yes}%")
    col3.metric("Maybe", f"{pct_maybe}%")
    col4.metric("Avg Spend", f"₹{avg_spend}")

    st.subheader("Adoption Split")

    fig = px.pie(
        names=["Yes", "Maybe", "No"],
        values=[pct_yes, pct_maybe, pct_no],
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "Insights":

    st.title("📊 Dog Owner Insights")

    st.subheader("Monthly Spend Distribution")

    fig = px.histogram(
        df,
        x="Q7_monthly_spend_inr",
        nbins=40
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Adoption vs Spend")

    fig2 = px.box(
        df,
        x="Q25_app_adoption",
        y="Q7_monthly_spend_inr",
        color="Q25_app_adoption"
    )
    st.plotly_chart(fig2, use_container_width=True)

elif page == "City Explorer":

    st.title("📍 City Explorer")

    cities = df["Q2_city"].dropna().unique()
    city = st.selectbox("Select City", cities)

    city_df = df[df["Q2_city"] == city]

    st.subheader(f"Spend in {city}")

    fig = px.histogram(
        city_df,
        x="Q7_monthly_spend_inr",
        nbins=30
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Adoption in City")

    adoption_counts = city_df["Q25_app_adoption"].value_counts()

    fig2 = px.pie(
        names=adoption_counts.index,
        values=adoption_counts.values
    )
    st.plotly_chart(fig2, use_container_width=True)

st.sidebar.download_button(
    "Download Clean Data",
    df.to_csv(index=False),
    file_name="pawindia_cleaned.csv"
)
