# p01_home.py
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from theme import (section_header, insight_box, insight_card, kpi_card,
                   page_header, live_bar, ring_svg, BROWN, AMBER, HONEY,
                   CHART_COLS, CREAM, PLOTLY_LIGHT, PCFG)
from ml_engine import load_data


def render():
    raw, df = load_data()
    n = len(df)
    pct_yes   = round((df["Q25_app_adoption"]=="Yes").sum()/n*100,1)
    pct_maybe = round((df["Q25_app_adoption"]=="Maybe").sum()/n*100,1)
    pct_no    = round((df["Q25_app_adoption"]=="No").sum()/n*100,1)
    avg_spend = int(df["Q7_monthly_spend_inr"].mean())

    page_header("🐾","PawIndia Market Intelligence",
                "India's first super-app for dog owners — validated by real market research")
    live_bar(n, "Home")

    # ── KPI row ───────────────────────────────────────────────────────────────
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: kpi_card("Respondents", f"{n:,}", "After cleaning", BROWN, "0s")
    with c2: kpi_card("Will Download", f"{pct_yes}%", "Definite adopters", "#4CAF50", "0.1s")
    with c3: kpi_card("Open To Try",  f"{pct_maybe}%","Conditional", HONEY, "0.2s")
    with c4: kpi_card("Avg Spend", f"Rs.{avg_spend:,}", "Monthly / owner", AMBER, "0.3s")
    with c5: kpi_card("Reachable", f"{pct_yes+pct_maybe}%","Yes + Maybe", "#5BB8C4","0.4s")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Radial rings + adoption donut ─────────────────────────────────────────
    section_header("Adoption at a Glance")
    rc1, rc2, rc3, rc4, rc5 = st.columns(5)
    with rc1: st.markdown(ring_svg(pct_yes,   "#4CAF50","Would Download"), unsafe_allow_html=True)
    with rc2: st.markdown(ring_svg(pct_maybe, HONEY,   "Open to It"),     unsafe_allow_html=True)
    with rc3: st.markdown(ring_svg(pct_no,    "#E53935","Would Not"),      unsafe_allow_html=True)
    with rc4: st.markdown(ring_svg(pct_yes+pct_maybe,"#5BB8C4","Reachable"), unsafe_allow_html=True)
    with rc5:
        # Mini donut
        fig_d = go.Figure(go.Pie(
            labels=["Yes","Maybe","No"],
            values=[(df["Q25_app_adoption"]==l).sum() for l in ["Yes","Maybe","No"]],
            hole=0.55, marker_colors=["#4CAF50", HONEY, "#E53935"],
            textinfo="percent", textfont_size=11,
        ))
        fig_d.update_layout(
            height=140, margin=dict(t=0,b=0,l=0,r=0),
            paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
            annotations=[dict(text=f"<b>{n:,}</b>",x=0.5,y=0.5,
                               showarrow=False,font=dict(size=12,color=BROWN))]
        )
        st.plotly_chart(fig_d, use_container_width=True, config=PCFG)

    # ── Central question ──────────────────────────────────────────────────────
    st.markdown(
        f"""<div class="info-card" style="border-left:5px solid {AMBER}">
        <div style="color:{AMBER};font-size:0.75rem;font-weight:700;
        text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px">
        The Central Business Question</div>
        <div style="color:#3E2A1A;font-size:1rem;line-height:1.7;font-weight:500">
        Do Indian dog owners face enough real pain around finding vets, parks, grooming
        and community that they would download and pay for a centralised app?
        The survey says <strong style="color:#4CAF50">{pct_yes+pct_maybe}% are open to it</strong>
        — and this dashboard shows exactly who, where, and why.
        </div></div>""",
        unsafe_allow_html=True,
    )

    # ── Top challenges bar ────────────────────────────────────────────────────
    col_l, col_r = st.columns([3, 2])
    with col_l:
        section_header("What Dog Owners Struggle With Most")
        ch_cols = {c: c.replace("Q10_challenges__","").replace("_"," ").title()
                   for c in df.columns if c.startswith("Q10_challenges__")}
        ch_data = {label: int(df[col].sum()) for col, label in ch_cols.items()}
        ch_df = pd.DataFrame({"Challenge":list(ch_data.keys()),
                               "Count":list(ch_data.values())}).sort_values("Count")
        fig = go.Figure(go.Bar(
            x=ch_df["Count"], y=ch_df["Challenge"], orientation="h",
            marker=dict(color=ch_df["Count"],
                        colorscale=[[0,"#F0E4D7"],[0.5,HONEY],[1,BROWN]]),
            text=ch_df["Count"], textposition="outside",
        ))
        fig.update_layout(**PLOTLY_LIGHT, height=340,
                          margin=dict(t=10,b=10,l=0,r=40),
                          xaxis=dict(showgrid=False,visible=False),
                          yaxis=dict(tickfont=dict(size=11)))
        st.plotly_chart(fig, use_container_width=True, config=PCFG)
        insight_box("Finding a reliable vet is the single biggest pain point — "
                    "validating PawIndia's core vet directory feature.")

    with col_r:
        section_header("Top Features Demanded")
        ft_cols = {c: c.replace("Q14_preferred_features__","").replace("_"," ").title()
                   for c in df.columns if c.startswith("Q14_preferred_features__")}
        ft_data = {label: int(df[col].sum()) for col, label in ft_cols.items()}
        ft_df = pd.DataFrame({"Feature":list(ft_data.keys()),
                               "Count":list(ft_data.values())}).sort_values("Count").tail(7)
        fig2 = go.Figure(go.Bar(
            x=ft_df["Count"], y=ft_df["Feature"], orientation="h",
            marker_color=AMBER, text=ft_df["Count"], textposition="outside",
        ))
        fig2.update_layout(**PLOTLY_LIGHT, height=340,
                           margin=dict(t=10,b=10,l=0,r=40),
                           xaxis=dict(showgrid=False,visible=False),
                           yaxis=dict(tickfont=dict(size=10)))
        st.plotly_chart(fig2, use_container_width=True, config=PCFG)
        insight_box("Health tracker tops feature demand, followed by vet directory "
                    "and lost-and-found alerts.")

    # ── Spend vs Adoption box plot — the money slide ──────────────────────────
    section_header("The Money Signal: Spend by Adoption Intent")
    fig3 = go.Figure()
    for cat, col in [("Yes","#4CAF50"),("Maybe",HONEY),("No","#E53935")]:
        v = df[df["Q25_app_adoption"]==cat]["Q7_monthly_spend_inr"]
        fig3.add_trace(go.Box(
            y=v, name=f"{cat} (n={len(v)})",
            marker_color=col, boxmean=True, line=dict(width=2),
        ))
    fig3.update_layout(**PLOTLY_LIGHT, height=320,
                       yaxis=dict(title="Monthly Spend (INR)"),
                       margin=dict(t=10,b=20))
    st.plotly_chart(fig3, use_container_width=True, config=PCFG)

    yes_spend = int(df[df["Q25_app_adoption"]=="Yes"]["Q7_monthly_spend_inr"].mean())
    no_spend  = int(df[df["Q25_app_adoption"]=="No"]["Q7_monthly_spend_inr"].mean())
    insight_box(f"'Yes' owners spend an average of Rs.{yes_spend:,}/month vs "
                f"Rs.{no_spend:,}/month for 'No' owners — a Rs.{yes_spend-no_spend:,} gap. "
                "High-spend dog owners are your primary conversion target.")

    # ── Insight cards ─────────────────────────────────────────────────────────
    section_header("Key Business Signals")
    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        insight_card("🏙️","Strongest Market","Metro Cities",
                     "Metro city residents show the highest definite adoption rate "
                     "and the highest avg monthly spend.", BROWN)
    with ic2:
        insight_card("💉","Top Feature","Health Tracker",
                     "The vaccination and health tracking feature is the most demanded "
                     "across all city tiers and age groups.", AMBER)
    with ic3:
        insight_card("📱","Digital Ready",f"{round((df['Q15_app_usage']!='Never').sum()/n*100)}%",
                     "Already use a mobile app for at least one pet-related need, "
                     "making adoption friction low.", "#5BB8C4")

    # ── Download ──────────────────────────────────────────────────────────────
    st.markdown("<hr style='border-color:#E8D5C4;margin-top:30px'>", unsafe_allow_html=True)
    d1, d2, _ = st.columns([1,1,3])
    with d1:
        st.download_button("Download Raw Data", raw.to_csv(index=False),
                           "pawindia_raw.csv", "text/csv")
    with d2:
        st.download_button("Download Cleaned Data", df.to_csv(index=False),
                           "pawindia_clean.csv", "text/csv")
