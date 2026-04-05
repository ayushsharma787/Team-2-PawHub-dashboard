# pages/p01_home.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from theme import section_header, insight_box, BROWN, AMBER, CHART_COLS, CREAM
from ml_engine import load_data


def render():
    raw, df = load_data()

    st.markdown(
        "<h1 style='color:#6F4E37;font-size:2rem;margin-bottom:0'>Welcome to PawIndia</h1>"
        "<p style='color:#9E8272;font-size:1rem;margin-top:4px'>"
        "India's first super-app for dog owners — validated by real market research</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='border-color:#E8D5C4'>", unsafe_allow_html=True)

    # ── KPI Cards ─────────────────────────────────────────────────────────────
    total   = len(df)
    pct_yes = round((df["Q25_app_adoption"] == "Yes").sum() / total * 100, 1)
    pct_maybe = round((df["Q25_app_adoption"] == "Maybe").sum() / total * 100, 1)
    avg_spend = int(df["Q7_monthly_spend_inr"].mean())
    top_city  = df[[c for c in df.columns if "Q2_city_tier_" in c]].sum().idxmax().replace("Q2_city_tier_","")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Survey Respondents",  f"{total:,}")
    c2.metric("Would Download App",  f"{pct_yes}%",  delta="Definite Yes")
    c3.metric("Open to Trying",      f"{pct_maybe}%", delta="Conditional")
    c4.metric("Avg Monthly Spend",   f"Rs.{avg_spend:,}")
    c5.metric("Strongest Market",    top_city)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── What is PawIndia ──────────────────────────────────────────────────────
    section_header("What is PawIndia?")
    col_l, col_r = st.columns([3, 2])
    with col_l:
        st.markdown(
            """
            <div class="info-card">
            <p style="color:#3E2A1A;font-size:0.95rem;line-height:1.7">
            PawIndia is a proposed mobile super-app designed specifically for dog owners across India.
            The platform brings together everything a dog parent needs in one place: nearby vet clinics,
            grooming services, dog-friendly parks and cafes, a health tracker for vaccinations and
            medical history, a lost-and-found community alert system, and a network of fellow dog owners.
            </p>
            <p style="color:#3E2A1A;font-size:0.95rem;line-height:1.7">
            This dashboard presents the findings from a survey of <strong>{:,} dog owners and pet lovers
            across India</strong>, designed to validate whether PawIndia solves a real problem and
            whether people are willing to pay for it.
            </p>
            </div>
            """.format(total),
            unsafe_allow_html=True,
        )
    with col_r:
        # Adoption donut
        labels = ["Would Download", "Open to Trying", "Would Not Download"]
        values = [
            (df["Q25_app_adoption"] == "Yes").sum(),
            (df["Q25_app_adoption"] == "Maybe").sum(),
            (df["Q25_app_adoption"] == "No").sum(),
        ]
        fig = go.Figure(go.Pie(
            labels=labels, values=values, hole=0.6,
            marker_colors=[BROWN, AMBER, "#E8D5C4"],
            textinfo="percent", textfont_size=13,
        ))
        fig.update_layout(
            showlegend=True, height=260, margin=dict(t=10, b=10, l=0, r=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(font=dict(size=11)),
            annotations=[dict(text=f"<b>{pct_yes+pct_maybe}%</b><br>Open",
                               x=0.5, y=0.5, showarrow=False,
                               font=dict(size=14, color=BROWN))]
        )
        st.plotly_chart(fig, use_container_width=True)

    insight_box(
        f"{pct_yes + pct_maybe}% of surveyed dog owners in India are open to downloading PawIndia. "
        f"That represents a substantial addressable audience for an early-stage launch."
    )

    # ── The Problem ───────────────────────────────────────────────────────────
    section_header("The Problem We Are Solving")
    st.markdown(
        """
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px">
          <div class="info-card" style="text-align:center">
            <div style="font-size:2rem">🏥</div>
            <div style="font-weight:700;color:#6F4E37;margin:6px 0">Finding a Vet</div>
            <div style="color:#9E8272;font-size:0.85rem">Most dog owners rely on word of mouth
            or Google to find emergency vet care — with no ratings or availability info</div>
          </div>
          <div class="info-card" style="text-align:center">
            <div style="font-size:2rem">🌳</div>
            <div style="font-weight:700;color:#6F4E37;margin:6px 0">Pet-Friendly Spaces</div>
            <div style="color:#9E8272;font-size:0.85rem">Dog owners struggle to find parks,
            cafes, and hotels that genuinely welcome dogs, especially in Tier-2 cities</div>
          </div>
          <div class="info-card" style="text-align:center">
            <div style="font-size:2rem">💉</div>
            <div style="font-weight:700;color:#6F4E37;margin:6px 0">Health Tracking</div>
            <div style="color:#9E8272;font-size:0.85rem">Over 30% of dog owners rely on memory
            alone to track vaccinations — a risk to their pet and a gap PawIndia can fill</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Top Challenges bar ────────────────────────────────────────────────────
    section_header("What Dog Owners Struggle With Most")
    ch_cols = {c: c.replace("Q10_challenges__","").replace("_"," ").title()
               for c in df.columns if c.startswith("Q10_challenges__")}
    ch_counts = {label: df[col].sum() for col, label in ch_cols.items()}
    ch_df = pd.DataFrame({"Challenge": list(ch_counts.keys()),
                           "Count": list(ch_counts.values())}).sort_values("Count", ascending=True).tail(7)
    fig2 = go.Figure(go.Bar(
        x=ch_df["Count"], y=ch_df["Challenge"], orientation="h",
        marker_color=BROWN, text=ch_df["Count"], textposition="outside",
    ))
    fig2.update_layout(
        height=320, margin=dict(t=10, b=10, l=0, r=40),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(tickfont=dict(size=12)),
        font=dict(color="#3E2A1A"),
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ── Download ──────────────────────────────────────────────────────────────
    st.markdown("<hr style='border-color:#E8D5C4;margin-top:30px'>", unsafe_allow_html=True)
    col_d1, col_d2, _ = st.columns([1,1,3])
    with col_d1:
        st.download_button(
            "Download Raw Data",
            data=raw.to_csv(index=False),
            file_name="pawindia_raw_data.csv",
            mime="text/csv",
        )
    with col_d2:
        st.download_button(
            "Download Cleaned Data",
            data=df.to_csv(index=False),
            file_name="pawindia_cleaned_data.csv",
            mime="text/csv",
        )
