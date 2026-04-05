# app.py — PawIndia Dashboard v2

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

PAGES = [
    "🏠  Home",
    "📍  Know Your City",
    "🐶  Dog Owner Insights",
    "💰  Will They Buy?",
    "🔬  Data Journey",
    "📊  Research & Analytics",
]

with st.sidebar:
    st.markdown(
        f'<div style="padding:18px 10px 10px;animation:float1 6s ease-in-out infinite">'
        f'{LOGO_SVG}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "<hr style='border:none;border-top:1px solid rgba(212,168,83,0.15);margin:10px 0'>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-size:0.65rem;letter-spacing:1.8px;color:#5a5040;"
        "text-transform:uppercase;margin:0 0 8px 4px;font-weight:700'>Navigate</p>",
        unsafe_allow_html=True,
    )
    page = st.radio("", PAGES, label_visibility="collapsed")
    st.markdown(
        "<hr style='border:none;border-top:1px solid rgba(212,168,83,0.1);margin:16px 0'>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-size:0.65rem;color:#5a5040;text-align:center;line-height:1.8'>"
        "PawIndia &copy; 2024<br>"
        "<span style='color:#D4A853'>Market Research Dashboard</span></p>",
        unsafe_allow_html=True,
    )

if   page == "🏠  Home":
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
