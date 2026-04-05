# theme.py — PawIndia v2 Hybrid Theme

# ── Palette ───────────────────────────────────────────────────────────────────
BROWN       = "#6F4E37"
AMBER       = "#D4860B"
HONEY       = "#D4A853"
CREAM       = "#FFF8F0"
DARK_BG     = "#1A1209"
DARK_CARD   = "rgba(30,22,12,0.92)"
DARK_BORDER = "rgba(212,168,83,0.18)"
LIGHT_BROWN = "#C49A6C"
MUTED       = "#9E8272"
SAGE        = "#7CB67C"
TEAL        = "#5BB8C4"
MAUVE       = "#9B7CB6"
TERRA       = "#C4704B"
CREAM_TEXT  = "#EDE4D3"
DIM         = "#7A6F5C"

CHART_COLS = [BROWN, HONEY, LIGHT_BROWN, SAGE, TEAL, MAUVE, TERRA,
              "#A0522D", "#DEB887", "#5CC4A0"]

# Plotly dark config for Research tab charts
PLOTLY_DARK = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(26,18,9,0.6)",
    font=dict(family="Plus Jakarta Sans, Inter, sans-serif", color=CREAM_TEXT, size=11),
    margin=dict(l=50, r=20, t=44, b=50),
    xaxis=dict(gridcolor="rgba(80,65,40,.15)", linecolor="rgba(80,65,40,.3)", zeroline=False),
    yaxis=dict(gridcolor="rgba(80,65,40,.15)", linecolor="rgba(80,65,40,.3)", zeroline=False),
)

# Plotly light config for main pages
PLOTLY_LIGHT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,248,240,0.5)",
    font=dict(family="Plus Jakarta Sans, Inter, sans-serif", color="#3E2A1A", size=11),
    margin=dict(l=50, r=20, t=44, b=50),
    xaxis=dict(gridcolor="rgba(111,78,55,.08)", linecolor="rgba(111,78,55,.15)", zeroline=False),
    yaxis=dict(gridcolor="rgba(111,78,55,.08)", linecolor="rgba(111,78,55,.15)", zeroline=False),
)

PCFG = {"displayModeBar": False}

# ── Animated 3D Logo SVG ──────────────────────────────────────────────────────
LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 72" width="260" height="58">
  <defs>
    <linearGradient id="pawGrad3d" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#D4A853;stop-opacity:1"/>
      <stop offset="50%" style="stop-color:#C49A6C;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#6F4E37;stop-opacity:1"/>
    </linearGradient>
    <linearGradient id="pawShadow" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#3E2A1A;stop-opacity:0.6"/>
      <stop offset="100%" style="stop-color:#1A1209;stop-opacity:0.9"/>
    </linearGradient>
    <linearGradient id="textGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#EDE4D3"/>
      <stop offset="100%" style="stop-color:#D4A853"/>
    </linearGradient>
    <filter id="glow3d" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="deepShadow">
      <feDropShadow dx="2" dy="3" stdDeviation="2" flood-color="#1A1209" flood-opacity="0.7"/>
    </filter>
  </defs>

  <!-- 3D Paw icon — shadow layer -->
  <ellipse cx="30" cy="46" rx="11" ry="13" fill="url(#pawShadow)" transform="translate(3,3)"/>
  <ellipse cx="16" cy="32" rx="7" ry="9" fill="url(#pawShadow)" transform="translate(3,3)"/>
  <ellipse cx="30" cy="27" rx="7" ry="9" fill="url(#pawShadow)" transform="translate(3,3)"/>
  <ellipse cx="44" cy="32" rx="7" ry="9" fill="url(#pawShadow)" transform="translate(3,3)"/>

  <!-- 3D Paw icon — main with gradient and glow -->
  <g filter="url(#glow3d)">
    <ellipse cx="30" cy="46" rx="11" ry="13" fill="url(#pawGrad3d)"/>
    <!-- sheen highlight for 3D effect -->
    <ellipse cx="27" cy="41" rx="5" ry="4" fill="rgba(255,248,240,0.18)" transform="rotate(-20,27,41)"/>

    <ellipse cx="16" cy="32" rx="7" ry="9" fill="url(#pawGrad3d)"/>
    <ellipse cx="14" cy="29" rx="3" ry="2.5" fill="rgba(255,248,240,0.18)" transform="rotate(-15,14,29)"/>

    <ellipse cx="30" cy="27" rx="7" ry="9" fill="url(#pawGrad3d)"/>
    <ellipse cx="28" cy="24" rx="3" ry="2.5" fill="rgba(255,248,240,0.18)" transform="rotate(-10,28,24)"/>

    <ellipse cx="44" cy="32" rx="7" ry="9" fill="url(#pawGrad3d)"/>
    <ellipse cx="42" cy="29" rx="3" ry="2.5" fill="rgba(255,248,240,0.18)" transform="rotate(-5,42,29)"/>
  </g>

  <!-- Wordmark with 3D depth -->
  <text x="66" y="48" font-family="Georgia,serif" font-size="32"
        font-weight="bold" fill="#3E2A1A" opacity="0.5" transform="translate(2,2)">PawIndia</text>
  <text x="66" y="48" font-family="Georgia,serif" font-size="32"
        font-weight="bold" fill="url(#textGrad)" filter="url(#deepShadow)">
    <tspan fill="#EDE4D3">Paw</tspan><tspan fill="#D4A853">India</tspan>
  </text>

  <!-- Tagline -->
  <text x="66" y="62" font-family="Arial,sans-serif" font-size="8.5"
        fill="#9E8272" letter-spacing="1.2">CONNECTING EVERY DOG AND THEIR HUMAN</text>

  <!-- Animated shimmer line under logo -->
  <line x1="66" y1="66" x2="280" y2="66" stroke="url(#pawGrad3d)" stroke-width="1" opacity="0.4"/>

  <!-- Animated pulse dot -->
  <circle cx="295" cy="66" r="3" fill="#D4A853" opacity="0.9">
    <animate attributeName="r" values="3;5;3" dur="2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.9;0.3;0.9" dur="2s" repeatCount="indefinite"/>
  </circle>
</svg>
"""

# ── Full CSS ──────────────────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,700;12..96,800&display=swap');

/* ── Root ── */
html, body, [class*="css"] {
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
  background-color: #FFF8F0;
}
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1400px; }

/* ── Sidebar — dark ── */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #1A1209 0%, #0D0A06 100%) !important;
  border-right: 1px solid rgba(212,168,83,0.15) !important;
}
section[data-testid="stSidebar"] * { color: #C4B99A !important; }
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 3px !important; }
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
  display: flex !important; align-items: center !important;
  background: transparent !important; border: 1px solid transparent !important;
  border-radius: 10px !important; padding: 9px 14px !important;
  margin: 0 !important; cursor: pointer !important; width: 100% !important;
  transition: all 0.25s cubic-bezier(.22,1,.36,1) !important;
  animation: fadeRight 0.5s cubic-bezier(.22,1,.36,1) both;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
  background: rgba(212,168,83,0.06) !important;
  border-color: rgba(212,168,83,0.15) !important;
  transform: translateX(4px) !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
  background: linear-gradient(135deg,rgba(160,125,58,.22),rgba(155,124,182,.1)) !important;
  border-color: rgba(212,168,83,0.3) !important;
  box-shadow: 0 0 20px rgba(212,168,83,0.06) !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label p {
  color: #7A6F5C !important; font-size: 12.5px !important; font-weight: 500 !important; margin: 0 !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) p {
  color: #D4A853 !important; font-weight: 700 !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label > div:first-child,
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] input[type="radio"] {
  display: none !important; width: 0 !important; height: 0 !important;
}

/* ── Metric cards — cream with brown left border ── */
div[data-testid="metric-container"] {
  background: #FFFFFF !important;
  border: 1px solid #E8D5C4 !important;
  border-left: 4px solid #6F4E37 !important;
  border-radius: 14px !important;
  padding: 16px 18px !important;
  box-shadow: 0 4px 16px rgba(111,78,55,0.1), 0 1px 4px rgba(111,78,55,0.06) !important;
  animation: breathe 5s ease-in-out infinite;
}
div[data-testid="metric-container"] label {
  color: #9E8272 !important; font-size: 0.72rem !important;
  font-weight: 700 !important; text-transform: uppercase !important;
  letter-spacing: 0.1em !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
  color: #3E2A1A !important; font-size: 1.6rem !important;
  font-weight: 800 !important; font-family: 'Bricolage Grotesque', sans-serif !important;
}

/* ── Info cards ── */
.info-card {
  background: #FFFFFF; border: 1px solid #E8D5C4;
  border-radius: 14px; padding: 20px 22px; margin-bottom: 14px;
  box-shadow: 0 4px 16px rgba(111,78,55,0.07);
  animation: breathe 5s ease-in-out infinite;
}

/* ── Dark card (for Research tab) ── */
.dark-card {
  background: rgba(30,22,12,0.92); border: 1px solid rgba(212,168,83,0.18);
  border-radius: 14px; padding: 20px 22px; margin-bottom: 14px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}

/* ── Section header ── */
.section-header {
  color: #6F4E37; font-size: 1.15rem; font-weight: 700;
  font-family: 'Bricolage Grotesque', sans-serif;
  border-bottom: 2px solid #D4860B; padding-bottom: 6px;
  margin: 24px 0 16px 0; display: flex; align-items: center; gap: 10px;
}
.section-header::before {
  content: ''; display: inline-block; width: 4px; height: 20px;
  background: linear-gradient(180deg, #D4860B, transparent);
  border-radius: 2px; flex-shrink: 0;
}

/* ── Insight box ── */
.insight-box {
  background: linear-gradient(135deg, rgba(212,168,83,0.08), rgba(255,248,240,0.6));
  border-left: 4px solid #D4860B; border-radius: 0 10px 10px 0;
  padding: 12px 16px; margin: 10px 0 18px 0; color: #3E2A1A; font-size: 0.88rem;
  animation: fadeUp 0.6s cubic-bezier(.22,1,.36,1) both;
}

/* ── Dark insight box ── */
.dark-insight {
  background: linear-gradient(135deg, rgba(212,168,83,0.08), transparent);
  border: 1px solid rgba(212,168,83,0.18); border-left: 4px solid #D4A853;
  border-radius: 0 10px 10px 0; padding: 12px 16px; margin: 10px 0 18px 0;
  color: #C4B99A; font-size: 0.88rem;
}

/* ── Step box ── */
.step-box {
  background: #FFFFFF; border: 1px solid #E8D5C4;
  border-top: 4px solid #6F4E37; border-radius: 10px;
  padding: 16px 20px; margin-bottom: 12px;
}

/* ── Live bar ── */
.live-bar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 9px 18px; border-radius: 12px; margin-bottom: 16px;
  background: linear-gradient(135deg, rgba(26,18,9,0.9), rgba(13,10,6,0.95));
  border: 1px solid rgba(212,168,83,0.15);
  box-shadow: 0 2px 12px rgba(0,0,0,0.25);
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: rgba(255,248,240,0.8) !important; border-radius: 12px !important;
  padding: 4px !important; border: 1px solid #E8D5C4 !important;
  box-shadow: 0 2px 8px rgba(111,78,55,0.08) !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important; border-radius: 9px !important;
  color: #9E8272 !important; font-size: 12.5px !important;
  font-weight: 600 !important; padding: 8px 18px !important;
  transition: all 0.2s cubic-bezier(.22,1,.36,1) !important;
}
.stTabs [data-baseweb="tab"]:hover { background: rgba(111,78,55,0.05) !important; color: #6F4E37 !important; }
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, #6F4E37, #D4860B) !important;
  color: #FFF8F0 !important;
  box-shadow: 0 2px 8px rgba(111,78,55,0.25) !important;
}
.stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 16px !important; }

/* ── Buttons ── */
.stButton > button {
  background: linear-gradient(135deg, #6F4E37, #D4860B) !important;
  color: #FFF8F0 !important; border: none !important;
  border-radius: 10px !important; font-weight: 700 !important;
  padding: 9px 22px !important;
  transition: all 0.3s cubic-bezier(.22,1,.36,1) !important;
}
.stButton > button:hover {
  transform: translateY(-2px) scale(1.02) !important;
  box-shadow: 0 6px 20px rgba(111,78,55,0.3) !important;
}
.stDownloadButton > button {
  background: linear-gradient(135deg, #3d6b3d, #5a9a5a) !important;
  color: white !important; border: none !important;
  border-radius: 10px !important; font-weight: 700 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: rgba(111,78,55,0.25); border-radius: 10px; }

/* ── Animations ── */
@keyframes breathe {
  0%,100% { transform: translateY(0); box-shadow: 0 4px 16px rgba(111,78,55,0.08); }
  50% { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(111,78,55,0.14); }
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeRight {
  from { opacity: 0; transform: translateX(-16px); }
  to   { opacity: 1; transform: translateX(0); }
}
@keyframes pulseGlow {
  0%,100% { box-shadow: 0 0 6px rgba(212,168,83,0.1); }
  50%     { box-shadow: 0 0 20px rgba(212,168,83,0.25); }
}
@keyframes liveDot {
  0%,100% { opacity: 1; box-shadow: 0 0 4px rgba(124,182,124,0.8); }
  50%     { opacity: 0.4; box-shadow: 0 0 12px rgba(124,182,124,0.4); }
}
@keyframes float1 {
  0%,100% { transform: translateY(0) rotate(0deg); }
  50%     { transform: translateY(-6px) rotate(0.5deg); }
}
@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

/* ── Persona badges ── */
.persona-badge {
  display: inline-block; padding: 3px 14px; border-radius: 20px;
  font-size: 0.75rem; font-weight: 700; margin-right: 6px;
  background: #6F4E37; color: #FFF8F0;
}

/* ── Styled table ── */
.styled-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.styled-table th {
  background: linear-gradient(135deg,#6F4E37,#3E2A1A); color: #FFF8F0;
  padding: 10px 14px; text-align: left; font-weight: 600;
}
.styled-table td { padding: 9px 14px; border-bottom: 1px solid #F0E4D7; color: #3E2A1A; }
.styled-table tr:nth-child(even) td { background: #FFF8F0; }
.styled-table tr:hover td { background: #FEF3E2; }
</style>
"""


def apply_theme():
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)


def logo_header(sidebar=True):
    import streamlit as st
    if sidebar:
        st.markdown(
            f'<div style="padding:16px 8px 8px;animation:float1 6s ease-in-out infinite">'
            f'{LOGO_SVG}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(LOGO_SVG, unsafe_allow_html=True)


def live_bar(n_records, page_name=""):
    import streamlit as st, time
    now = time.strftime("%H:%M:%S")
    st.markdown(
        f"""<div class="live-bar">
          <div style="display:flex;align-items:center;gap:10px">
            <div style="position:relative;width:9px;height:9px">
              <div style="position:absolute;inset:0;border-radius:50%;background:#7CB67C;animation:liveDot 2s ease-in-out infinite"></div>
            </div>
            <span style="color:#7CB67C;font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase">LIVE</span>
            <span style="color:#5a5040;font-size:10px">|</span>
            <span style="color:#C4B99A;font-size:11px;font-weight:600">{n_records:,} respondents loaded</span>
            {"<span style='color:#5a5040;font-size:10px'>|</span><span style='color:#9E8272;font-size:11px'>"+page_name+"</span>" if page_name else ""}
          </div>
          <span style="color:#D4A853;font-size:12px;font-weight:700;font-family:monospace">{now}</span>
        </div>""",
        unsafe_allow_html=True,
    )


def section_header(title: str):
    import streamlit as st
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)


def insight_box(text: str, dark=False):
    import streamlit as st
    cls = "dark-insight" if dark else "insight-box"
    st.markdown(f'<div class="{cls}">&#128161; {text}</div>', unsafe_allow_html=True)


def page_header(emoji, title, subtitle="", dark=False):
    import streamlit as st
    if dark:
        bg = "linear-gradient(135deg,rgba(30,22,12,0.95),rgba(13,10,6,0.98))"
        bc = "rgba(212,168,83,0.25)"; tc = "#EDE4D3"; sc = "#A07D3A"
    else:
        bg = "linear-gradient(135deg,#FFFFFF,#FFF8F0)"
        bc = "#E8D5C4"; tc = "#3E2A1A"; sc = "#9E8272"
    sub = f"<div style='color:{sc};font-size:0.9rem;margin-top:6px;font-weight:500'>{subtitle}</div>" if subtitle else ""
    st.markdown(
        f"""<div style="background:{bg};border:1px solid {bc};border-left:5px solid #D4860B;
        border-radius:14px;padding:22px 26px;margin-bottom:22px;
        box-shadow:0 6px 24px rgba(0,0,0,0.12);animation:fadeUp 0.5s cubic-bezier(.22,1,.36,1) both">
        <div style="display:flex;align-items:center;gap:16px">
          <div style="font-size:42px;filter:drop-shadow(0 0 10px rgba(212,168,83,0.3))">{emoji}</div>
          <div><h1 style="margin:0;font-size:1.8rem;font-family:Bricolage Grotesque,sans-serif;
          font-weight:800;color:{tc}">{title}</h1>{sub}</div>
        </div></div>""",
        unsafe_allow_html=True,
    )


def kpi_card(label, value, delta=None, color="#D4860B", animate_delay="0s"):
    import streamlit as st
    delta_html = f"<div style='color:#9E8272;font-size:0.72rem;margin-top:4px'>{delta}</div>" if delta else ""
    st.markdown(
        f"""<div style="background:#FFFFFF;border:1px solid #E8D5C4;border-top:4px solid {color};
        border-radius:14px;padding:18px 20px;text-align:center;
        box-shadow:0 4px 16px rgba(111,78,55,0.1);
        animation:fadeUp 0.5s cubic-bezier(.22,1,.36,1) {animate_delay} both, breathe 5s ease-in-out infinite">
          <div style="color:#9E8272;font-size:0.7rem;font-weight:700;letter-spacing:.1em;
          text-transform:uppercase;margin-bottom:8px">{label}</div>
          <div style="color:{color};font-size:1.8rem;font-weight:800;
          font-family:Bricolage Grotesque,sans-serif;letter-spacing:-0.02em">{value}</div>
          {delta_html}
        </div>""",
        unsafe_allow_html=True,
    )


def insight_card(emoji, title, value, detail, color="#D4860B"):
    import streamlit as st
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    st.markdown(
        f"""<div style="background:linear-gradient(145deg,rgba(255,248,240,1),rgba(254,243,226,0.6));
        border:1px solid rgba({r},{g},{b},0.25);border-left:4px solid {color};
        border-radius:14px;padding:18px 20px;margin:8px 0;
        box-shadow:0 4px 16px rgba({r},{g},{b},0.08);
        animation:fadeUp 0.6s cubic-bezier(.22,1,.36,1) both">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
            <span style="font-size:20px">{emoji}</span>
            <span style="color:{color};font-size:0.72rem;font-weight:700;
            letter-spacing:.1em;text-transform:uppercase;
            font-family:Bricolage Grotesque">{title}</span>
          </div>
          <div style="color:#3E2A1A;font-size:1.3rem;font-weight:800;
          font-family:Bricolage Grotesque;margin-bottom:4px">{value}</div>
          <div style="color:#6F4E37;font-size:0.83rem;line-height:1.6">{detail}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def ring_svg(pct, color, label, size=88, stroke=8):
    import math
    r = (size - stroke) / 2
    circ = 2 * math.pi * r
    offset = circ * (1 - pct / 100)
    return f"""<div style="text-align:center;animation:fadeUp 1s cubic-bezier(.22,1,.36,1) both">
      <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}"
           style="filter:drop-shadow(0 0 8px {color}50)">
        <circle cx="{size//2}" cy="{size//2}" r="{r}" fill="none"
                stroke="rgba(111,78,55,0.12)" stroke-width="{stroke}"/>
        <circle cx="{size//2}" cy="{size//2}" r="{r}" fill="none"
                stroke="{color}" stroke-width="{stroke}" stroke-linecap="round"
                stroke-dasharray="{circ:.1f}" stroke-dashoffset="{offset:.1f}"
                transform="rotate(-90 {size//2} {size//2})"/>
        <text x="{size//2}" y="{size//2-3}" text-anchor="middle"
              fill="{color}" font-size="15" font-weight="800"
              font-family="Bricolage Grotesque">{pct:.0f}%</text>
        <text x="{size//2}" y="{size//2+13}" text-anchor="middle"
              fill="#9E8272" font-size="8" font-weight="600">{label}</text>
      </svg></div>"""
