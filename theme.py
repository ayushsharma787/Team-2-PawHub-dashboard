# utils/theme.py

BROWN       = "#6F4E37"
AMBER       = "#D4860B"
CREAM       = "#FFF8F0"
LIGHT_BROWN = "#C49A6C"
DARK_BROWN  = "#3E2A1A"
CARD_BG     = "#FFFFFF"
MUTED       = "#9E8272"
SUCCESS     = "#4CAF50"
WARNING     = "#FF9800"
DANGER      = "#E53935"

CHART_COLS = [
    "#6F4E37", "#D4860B", "#C49A6C", "#A0522D",
    "#DEB887", "#8B4513", "#D2691E", "#CD853F",
    "#F4A460", "#BC8A5F"
]

LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 60" width="220" height="48">
  <ellipse cx="22" cy="38" rx="9" ry="11" fill="#6F4E37"/>
  <ellipse cx="10" cy="26" rx="5.5" ry="7" fill="#6F4E37"/>
  <ellipse cx="22" cy="22" rx="5.5" ry="7" fill="#6F4E37"/>
  <ellipse cx="34" cy="26" rx="5.5" ry="7" fill="#6F4E37"/>
  <text x="50" y="42" font-family="Georgia,serif" font-size="28"
        font-weight="bold" fill="#6F4E37">Paw</text>
  <text x="100" y="42" font-family="Georgia,serif" font-size="28"
        font-weight="bold" fill="#D4860B">India</text>
  <text x="50" y="56" font-family="Arial,sans-serif" font-size="8"
        fill="#9E8272" letter-spacing="1">CONNECTING EVERY DOG AND THEIR HUMAN</text>
</svg>
"""

CSS = """
<style>
  html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
    background-color: #FFF8F0;
  }
  .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
  section[data-testid="stSidebar"] { background-color: #3E2A1A !important; }
  section[data-testid="stSidebar"] * { color: #FFF8F0 !important; }
  div[data-testid="metric-container"] {
    background: #FFFFFF;
    border: 1px solid #E8D5C4;
    border-left: 4px solid #6F4E37;
    border-radius: 10px;
    padding: 14px 18px;
    box-shadow: 0 2px 8px rgba(111,78,55,0.08);
  }
  div[data-testid="metric-container"] label {
    color: #9E8272 !important; font-size: 0.78rem !important;
    font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.5px;
  }
  div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #3E2A1A !important; font-size: 1.6rem !important; font-weight: 700 !important;
  }
  .section-header {
    color: #6F4E37; font-size: 1.3rem; font-weight: 700;
    border-bottom: 2px solid #D4860B; padding-bottom: 6px;
    margin-bottom: 18px; margin-top: 28px;
  }
  .info-card {
    background: #FFFFFF; border: 1px solid #E8D5C4; border-radius: 12px;
    padding: 20px 22px; margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(111,78,55,0.06);
  }
  .insight-box {
    background: #FEF3E2; border-left: 4px solid #D4860B;
    border-radius: 0 8px 8px 0; padding: 12px 16px;
    margin: 10px 0 18px 0; color: #3E2A1A; font-size: 0.9rem;
  }
  .step-box {
    background: #FFFFFF; border: 1px solid #E8D5C4;
    border-top: 4px solid #6F4E37; border-radius: 10px;
    padding: 18px 20px; margin-bottom: 14px;
  }
  .stButton > button {
    background: #6F4E37 !important; color: #FFF8F0 !important;
    border: none !important; border-radius: 8px !important;
    font-weight: 600 !important; padding: 8px 20px !important;
  }
  .stButton > button:hover { background: #D4860B !important; }
  .stTabs [data-baseweb="tab"] { color: #6F4E37 !important; font-weight: 500; }
  .stTabs [aria-selected="true"] {
    border-bottom: 3px solid #D4860B !important;
    color: #3E2A1A !important; font-weight: 700 !important;
  }
  .stDownloadButton > button {
    background: #D4860B !important; color: white !important;
    border: none !important; border-radius: 8px !important; font-weight: 600 !important;
  }
  .styled-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
  .styled-table th {
    background: #6F4E37; color: #FFF8F0; padding: 10px 14px;
    text-align: left; font-weight: 600;
  }
  .styled-table td { padding: 9px 14px; border-bottom: 1px solid #F0E4D7; color: #3E2A1A; }
  .styled-table tr:nth-child(even) td { background: #FFF8F0; }
  .styled-table tr:hover td { background: #FEF3E2; }
</style>
"""


def apply_theme():
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)


def logo_header():
    import streamlit as st
    st.markdown(LOGO_SVG, unsafe_allow_html=True)


def section_header(title: str):
    import streamlit as st
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)


def insight_box(text: str):
    import streamlit as st
    st.markdown(f'<div class="insight-box">&#128161; {text}</div>', unsafe_allow_html=True)


def info_card(content: str):
    import streamlit as st
    st.markdown(f'<div class="info-card">{content}</div>', unsafe_allow_html=True)
