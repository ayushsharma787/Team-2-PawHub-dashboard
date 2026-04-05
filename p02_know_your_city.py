# p02_know_your_city.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from theme import (section_header, insight_box, page_header, live_bar,
                   BROWN, AMBER, HONEY, CHART_COLS, PLOTLY_LIGHT, PCFG)
from city_data import get_places_df, CITY_COORDS, CATEGORY_COLORS, CATEGORY_ICONS
from ml_engine import load_data


def render():
    _, df = load_data()
    places = get_places_df()
    n = len(df)

    page_header("📍","Know Your City",
                "Discover dog-friendly places near you across India")
    live_bar(n, "Know Your City")

    st.markdown(
        "<div class='insight-box' style='margin-bottom:18px'>"
        "&#128204; <strong>Note:</strong> Places shown are simulated for demonstration. "
        "When PawIndia launches, this connects to live Google Places and OpenStreetMap data "
        "with real-time ratings and availability.</div>",
        unsafe_allow_html=True,
    )

    # ── Controls ──────────────────────────────────────────────────────────────
    cc, cf, cs = st.columns([2,2,2])
    with cc: city = st.selectbox("Select Your City", list(CITY_COORDS.keys()), index=2)
    with cf:
        cats = ["All"] + sorted(places["category"].unique().tolist())
        cat  = st.selectbox("Filter by Type", cats)
    with cs:
        min_rating = st.slider("Minimum Rating", 3.5, 5.0, 4.0, 0.1)

    filtered = places[places["city"]==city].copy()
    if cat != "All": filtered = filtered[filtered["category"]==cat]
    filtered = filtered[filtered["rating"] >= min_rating].copy()

    if filtered.empty:
        st.warning("No places match your filters. Try lowering the minimum rating.")
        return

    # ── 3D Pydeck map ─────────────────────────────────────────────────────────
    section_header("3D Map View — Column Height = Rating")
    try:
        import pydeck as pdk

        filtered["color"]  = filtered["category"].apply(
            lambda c: CATEGORY_COLORS.get(c, [111,78,55]) + [200])
        filtered["elevation"] = (filtered["rating"] - 3.5) * 2000
        filtered["tooltip_text"] = filtered.apply(
            lambda r: f"{CATEGORY_ICONS.get(r['category'],'')} {r['name']}\n"
                      f"Rating: {r['rating']} ★  |  {r['reviews']} reviews\n"
                      f"{r['note']}", axis=1)

        lat0, lon0 = CITY_COORDS[city]

        column_layer = pdk.Layer(
            "ColumnLayer",
            data=filtered,
            get_position=["lon","lat"],
            get_elevation="elevation",
            elevation_scale=1,
            radius=120,
            get_fill_color="color",
            pickable=True,
            auto_highlight=True,
        )
        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=filtered,
            get_position=["lon","lat"],
            get_color="color",
            get_radius=80,
            pickable=True,
        )

        view = pdk.ViewState(
            latitude=lat0, longitude=lon0,
            zoom=12, pitch=55, bearing=15,
        )

        tooltip = {
            "html": "<div style='background:rgba(26,18,9,0.95);border:1px solid rgba(212,168,83,0.3);"
                    "border-radius:10px;padding:12px 16px;font-family:Plus Jakarta Sans,sans-serif'>"
                    "<b style='color:#D4A853;font-size:13px'>{name}</b><br>"
                    "<span style='color:#C4B99A;font-size:11px'>{category}</span><br>"
                    "<span style='color:#EDE4D3;font-size:12px'>Rating: {rating} ★  |  {reviews} reviews</span><br>"
                    "<span style='color:#9E8272;font-size:11px'>{note}</span></div>",
            "style": {"background": "transparent", "border": "none"},
        }

        deck = pdk.Deck(
            layers=[column_layer, scatter_layer],
            initial_view_state=view,
            tooltip=tooltip,
            map_style="mapbox://styles/mapbox/dark-v10",
        )
        st.pydeck_chart(deck, use_container_width=True)
        st.markdown(
            "<p style='color:#9E8272;font-size:0.8rem;text-align:center;margin-top:6px'>"
            "Taller columns = higher rated. Hover over any column for details. "
            "Drag to rotate, scroll to zoom.</p>",
            unsafe_allow_html=True,
        )
    except Exception as e:
        # Fallback to 2D plotly map if pydeck fails
        import plotly.express as px
        color_map = {k: f"rgb({v[0]},{v[1]},{v[2]})" for k,v in CATEGORY_COLORS.items()}
        fig_map = px.scatter_mapbox(
            filtered, lat="lat", lon="lon", color="category",
            color_discrete_map={k: f"#{v[0]:02x}{v[1]:02x}{v[2]:02x}" for k,v in CATEGORY_COLORS.items()},
            hover_name="name", hover_data={"rating":True,"reviews":True,"note":True,"lat":False,"lon":False},
            zoom=11, center={"lat":CITY_COORDS[city][0],"lon":CITY_COORDS[city][1]}, height=460,
            size=[12]*len(filtered),
        )
        fig_map.update_layout(mapbox_style="carto-positron",
                               margin=dict(t=0,b=0,l=0,r=0),
                               paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_map, use_container_width=True, config=PCFG)

    # ── Place cards ───────────────────────────────────────────────────────────
    section_header(f"Places in {city} ({len(filtered)} found)")
    card_cols = st.columns(3)
    for i, (_, row) in enumerate(filtered.iterrows()):
        col = card_cols[i % 3]
        star_color = AMBER if row["rating"] >= 4.5 else BROWN
        r,g,b = CATEGORY_COLORS.get(row["category"],[111,78,55])[:3]
        col.markdown(
            f"""<div style="background:#FFFFFF;border:1px solid #E8D5C4;
            border-top:3px solid rgb({r},{g},{b});border-radius:12px;
            padding:16px 18px;margin-bottom:12px;
            box-shadow:0 4px 14px rgba(111,78,55,0.08);
            transition:transform 0.2s;animation:fadeUp 0.5s ease both">
              <div style="font-size:1.3rem">{CATEGORY_ICONS.get(row['category'],'')}</div>
              <div style="font-weight:700;color:#3E2A1A;font-size:0.93rem;margin:4px 0">{row['name']}</div>
              <div style="color:{star_color};font-weight:600;font-size:0.85rem">
                {'★'*int(row['rating'])} {row['rating']}</div>
              <div style="color:#9E8272;font-size:0.78rem">{row['reviews']} reviews</div>
              <div style="color:#6F4E37;font-size:0.8rem;margin-top:6px;
              font-style:italic">{row['note']}</div>
            </div>""",
            unsafe_allow_html=True,
        )

    # ── Satisfaction radar by city ────────────────────────────────────────────
    section_header("How Satisfied Are Dog Owners With Their City's Pet Spaces?")
    city_map = {"Q2_city_tier_Metro":"Metro","Q2_city_tier_Tier-2":"Tier-2",
                "Q2_city_tier_Tier-3":"Tier-3","Q2_city_tier_Rural":"Rural"}
    sat_data = []
    for col, label in city_map.items():
        if col in df.columns:
            sub = df[df[col]==1]
            if len(sub) > 0:
                sat_data.append({
                    "City Tier": label,
                    "Avg Satisfaction": round(sub["Q13_pet_space_satisfaction_enc"].mean(), 2),
                    "n": len(sub),
                })
    if sat_data:
        sd = pd.DataFrame(sat_data)
        c1, c2 = st.columns(2)
        with c1:
            fig_sat = go.Figure(go.Bar(
                x=sd["City Tier"], y=sd["Avg Satisfaction (out of 5)"] if "Avg Satisfaction (out of 5)" in sd else sd["Avg Satisfaction"],
                marker=dict(color=[BROWN, AMBER, HONEY, "#C49A6C"]),
                text=sd["Avg Satisfaction"], textposition="outside",
            ))
            fig_sat.add_hline(y=3, line_dash="dash", line_color="#9E8272",
                               annotation_text="Neutral (3.0)")
            fig_sat.update_layout(**PLOTLY_LIGHT, height=300,
                                   yaxis=dict(range=[0,5.5], title="Score (1-5)"),
                                   margin=dict(t=20,b=20))
            st.plotly_chart(fig_sat, use_container_width=True, config=PCFG)
            insight_box("Tier-2 and Tier-3 cities consistently rate pet-friendly "
                        "spaces below neutral, signalling the largest untapped opportunity.")

        with c2:
            # Category radar for selected city
            city_tier = "Metro" if city in ["Mumbai","Delhi","Bengaluru","Hyderabad","Pune"] else "Tier-2"
            tier_col  = f"Q2_city_tier_{city_tier}"
            if tier_col in df.columns:
                sub = df[df[tier_col]==1]
                cats_radar = ["Vet Centre","Dog Park","Dog Cafe","Grooming","Pet Store"]
                # Simulated satisfaction by category from places data
                city_places = places[places["city"]==city]
                scores = [city_places[city_places["category"]==c]["rating"].mean()
                          if len(city_places[city_places["category"]==c]) > 0 else 3.5
                          for c in cats_radar]
                fig_radar = go.Figure(go.Scatterpolar(
                    r=scores + [scores[0]],
                    theta=cats_radar + [cats_radar[0]],
                    fill="toself",
                    fillcolor=f"rgba(212,134,11,0.15)",
                    line=dict(color=AMBER, width=2),
                    name=city,
                ))
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[3,5],
                                        gridcolor="rgba(111,78,55,0.1)"),
                        angularaxis=dict(gridcolor="rgba(111,78,55,0.1)"),
                        bgcolor="rgba(255,248,240,0.5)",
                    ),
                    paper_bgcolor="rgba(0,0,0,0)",
                    height=300, margin=dict(t=20,b=20,l=40,r=40),
                    showlegend=False,
                    font=dict(color="#3E2A1A"),
                    title=dict(text=f"Service Quality Radar: {city}",
                               font=dict(color=BROWN, size=13)),
                )
                st.plotly_chart(fig_radar, use_container_width=True, config=PCFG)

    st.download_button(
        f"Download {city} Places Data",
        data=filtered.drop(columns=["color","elevation","tooltip_text"], errors="ignore").to_csv(index=False),
        file_name=f"pawindia_{city.lower()}_places.csv",
        mime="text/csv",
    )
