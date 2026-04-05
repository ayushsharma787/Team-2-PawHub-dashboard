# app.py — PawIndia Dashboard entry point

import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

st.set_page_config(
    page_title="PawIndia Dashboard",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

from theme import apply_theme, LOGO_SVG

apply_theme()

with st.sidebar:
    st.markdown(LOGO_SVG, unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#6F4E37;margin:12px 0'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.7rem;letter-spacing:1.5px;color:#C49A6C;"
        "text-transform:uppercase;margin-bottom:8px'>Navigation</p>",
        unsafe_allow_html=True,
    )
    page = st.radio(
        label="",
        options=[
            "🏠  Home",
            "📍  Know Your City",
            "🐶  Dog Owner Insights",
            "💰  Will They Buy?",
            "🔬  Data Journey",
            "📊  Research & Analytics",
        ],
        label_visibility="collapsed",
    )
    st.markdown("<hr style='border-color:#6F4E37;margin:16px 0'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.72rem;color:#C49A6C;text-align:center'>"
        "PawIndia &copy; 2024<br>Market Research Dashboard</p>",
        unsafe_allow_html=True,
    )

if page == "🏠  Home":
    import p01_home as p;               p.render()
elif page == "📍  Know Your City":
    import p02_know_your_city as p;     p.render()
elif page == "🐶  Dog Owner Insights":
    import p03_dog_owner_insights as p; p.render()
elif page == "💰  Will They Buy?":
    import p04_will_they_buy as p;      p.render()
elif page == "🔬  Data Journey":
    import p05_data_journey as p;       p.render()
elif page == "📊  Research & Analytics":
    import p06_research_analytics as p; p.render()
