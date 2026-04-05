# pages/p02_know_your_city.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from theme import section_header, insight_box, BROWN, AMBER, CHART_COLS
from city_data import get_places_df, CITY_COORDS, CATEGORY_COLORS, CATEGORY_ICONS
from ml_engine import load_data


def render():
    _, df = load_data()
    places = get_places_df()

    st.markdown(
        "<h1 style='color:#6F4E37;font-size:1.8rem;margin-bottom:4px'>Know Your City</h1>"
        "<p style='color:#9E8272'>Discover dog-friendly places near you across India</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='insight-box' style='margin-bottom:18px'>"
        "&#128204; <strong>Note:</strong> Places shown are simulated for demonstration. "
        "When PawIndia launches, this will connect to live Google Places and OpenStreetMap data "
        "with real-time ratings and availability."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Controls ──────────────────────────────────────────────────────────────
    col_c, col_f, col_s = st.columns([2, 2, 2])
    with col_c:
        city = st.selectbox("Select Your City", list(CITY_COORDS.keys()), index=2)
    with col_f:
        cats = ["All"] + sorted(places["category"].unique().tolist())
        cat  = st.selectbox("Filter by Type", cats)
    with col_s:
        min_rating = st.slider("Minimum Rating", 3.5, 5.0, 4.0, 0.1)

    filtered = places[places["city"] == city].copy()
    if cat != "All":
        filtered = filtered[filtered["category"] == cat]
    filtered = filtered[filtered["rating"] >= min_rating]

    st.markdown(f"<br>", unsafe_allow_html=True)

    # ── Map ───────────────────────────────────────────────────────────────────
    if filtered.empty:
        st.warning("No places match your filters. Try lowering the minimum rating.")
        return

    filtered["icon"]  = filtered["category"].map(CATEGORY_ICONS)
    filtered["color"] = filtered["category"].map(CATEGORY_COLORS)
    filtered["label"] = filtered.apply(
        lambda r: f"{r['icon']} {r['name']} ({r['rating']}★)", axis=1)

    fig_map = px.scatter_mapbox(
        filtered,
        lat="lat", lon="lon",
        color="category",
        color_discrete_map=CATEGORY_COLORS,
        hover_name="name",
        hover_data={"rating": True, "reviews": True, "note": True,
                    "lat": False, "lon": False},
        zoom=11,
        center={"lat": CITY_COORDS[city][0], "lon": CITY_COORDS[city][1]},
        height=460,
        size_max=14,
        size=[12]*len(filtered),
    )
    fig_map.update_layout(
        mapbox_style="carto-positron",
        margin=dict(t=0, b=0, l=0, r=0),
        legend=dict(orientation="h", y=-0.05, font=dict(size=11)),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # ── Place listing cards ───────────────────────────────────────────────────
    section_header(f"Places in {city} ({len(filtered)} found)")
    cols = st.columns(3)
    for i, (_, row) in enumerate(filtered.iterrows()):
        with cols[i % 3]:
            star_color = "#D4860B" if row["rating"] >= 4.5 else "#6F4E37"
            st.markdown(
                f"""<div class="info-card" style="min-height:130px">
                  <div style="font-size:1.4rem">{row['icon']}</div>
                  <div style="font-weight:700;color:#3E2A1A;font-size:0.95rem">{row['name']}</div>
                  <div style="color:{star_color};font-weight:600;margin:4px 0">
                    {'★' * int(row['rating'])} {row['rating']}</div>
                  <div style="color:#9E8272;font-size:0.8rem">{row['reviews']} reviews</div>
                  <div style="color:#6F4E37;font-size:0.82rem;margin-top:6px">{row['note']}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    # ── City comparison: satisfaction with pet spaces ─────────────────────────
    section_header("How Satisfied Are Dog Owners With Local Spaces?")
    st.markdown(
        "<p style='color:#9E8272;font-size:0.88rem'>Based on survey responses from dog owners "
        "across India. This directly informs PawIndia's opportunity by city.</p>",
        unsafe_allow_html=True,
    )

    city_map = {
        "Q2_city_tier_Metro":"Metro Cities",
        "Q2_city_tier_Tier-2":"Tier-2 Cities",
        "Q2_city_tier_Tier-3":"Tier-3 Cities",
        "Q2_city_tier_Rural":"Rural Areas",
    }
    sat_data = []
    for col, label in city_map.items():
        if col in df.columns:
            sub = df[df[col] == 1]
            if len(sub) > 0:
                avg = sub["Q13_pet_space_satisfaction_enc"].mean()
                sat_data.append({"City Tier": label, "Avg Satisfaction (1-5)": round(avg, 2)})

    if sat_data:
        sat_df = pd.DataFrame(sat_data)
        fig_sat = go.Figure(go.Bar(
            x=sat_df["City Tier"],
            y=sat_df["Avg Satisfaction (1-5)"],
            marker_color=[BROWN, AMBER, "#C49A6C", "#DEB887"],
            text=sat_df["Avg Satisfaction (1-5)"],
            textposition="outside",
        ))
        fig_sat.add_hline(y=3, line_dash="dash", line_color="#9E8272",
                           annotation_text="Neutral (3.0)", annotation_position="left")
        fig_sat.update_layout(
            height=300, yaxis=dict(range=[0, 5.5], title="Satisfaction Score"),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#3E2A1A"),
            margin=dict(t=20, b=20),
        )
        st.plotly_chart(fig_sat, use_container_width=True)
        insight_box(
            "Dog owners in Tier-2 and Tier-3 cities report lower satisfaction with pet-friendly "
            "spaces compared to metros, indicating a significant expansion opportunity beyond the major cities."
        )

    # ── Download filtered ──────────────────────────────────────────────────────
    st.download_button(
        f"Download {city} Places Data",
        data=filtered.drop(columns=["icon","color","label"], errors="ignore").to_csv(index=False),
        file_name=f"pawindia_{city.lower()}_places.csv",
        mime="text/csv",
    )
