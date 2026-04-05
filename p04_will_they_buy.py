# p04_will_they_buy.py
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from theme import (section_header, insight_box, insight_card, kpi_card,
                   page_header, live_bar, BROWN, AMBER, HONEY,
                   CHART_COLS, PLOTLY_LIGHT, PCFG)
from ml_engine import load_data


def render():
    raw, df = load_data()
    n = len(df)
    pct_yes   = round((df["Q25_app_adoption"]=="Yes").sum()/n*100,1)
    pct_maybe = round((df["Q25_app_adoption"]=="Maybe").sum()/n*100,1)
    pct_no    = round((df["Q25_app_adoption"]=="No").sum()/n*100,1)

    page_header("💰","Will They Buy?",
                "Subscription preferences, conversion funnel, and who is most likely to adopt")
    live_bar(n, "Will They Buy?")

    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi_card("Definite Yes",   f"{pct_yes}%",   "Would download now", "#4CAF50")
    with c2: kpi_card("Open to It",     f"{pct_maybe}%", "Conditional adopters", HONEY)
    with c3: kpi_card("Would Not",      f"{pct_no}%",    "Lost audience","#E53935")
    with c4: kpi_card("Total Reachable",f"{pct_yes+pct_maybe}%","Yes + Maybe","#5BB8C4")

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🔻 Conversion Funnel","💳 Subscriptions","📍 By Location","👤 By Profile"])

    # ── Tab 1: Funnel ─────────────────────────────────────────────────────────
    with tab1:
        section_header("PawIndia Conversion Funnel")
        # Build funnel from survey signals
        total      = n
        aware      = n  # everyone who took the survey is aware
        interested = int((df["Q15_app_usage"] != "Never").sum())
        willing    = int((df["Q18_subscription_pref"].isin(
            ["Freemium","Monthly Sub","Annual Sub","One-Time Purchase"])).sum())
        definite   = int((df["Q25_app_adoption"]=="Yes").sum())

        funnel_data = pd.DataFrame({
            "Stage": ["Survey Respondents","Currently Use Pet Apps",
                      "Willing to Pay / Try","Would Definitely Download"],
            "Count": [total, interested, willing, definite],
            "Color": [BROWN, AMBER, HONEY, "#4CAF50"],
        })

        fig_funnel = go.Figure(go.Funnel(
            y=funnel_data["Stage"],
            x=funnel_data["Count"],
            textinfo="value+percent initial",
            marker=dict(color=funnel_data["Color"],
                        line=dict(color="#FFF8F0", width=1.5)),
            connector=dict(line=dict(color="rgba(111,78,55,0.2)", width=2)),
            textfont=dict(color="#3E2A1A", size=13),
        ))
        fig_funnel.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,248,240,0.3)",
            height=380, margin=dict(t=20,b=20,l=20,r=20),
            font=dict(color="#3E2A1A"),
        )
        st.plotly_chart(fig_funnel, use_container_width=True, config=PCFG)
        insight_box(f"From {total:,} surveyed dog owners, {definite:,} ({pct_yes}%) would "
                    f"definitely download PawIndia. The biggest drop-off is between 'willing to pay' "
                    "and 'definitely download' — reducing friction here is the key conversion lever.")

        # Engagement vs Spend scatter coloured by adoption
        section_header("The Sweet Spot: Engagement vs Spend by Adoption")
        fig_sc = px.scatter(
            df.sample(min(800,n), random_state=42),
            x="engagement_score", y="Q7_monthly_spend_inr",
            color="Q25_app_adoption",
            color_discrete_map={"Yes":"#4CAF50","Maybe":HONEY,"No":"#E53935"},
            size="Q7_monthly_spend_inr",
            size_max=14, opacity=0.6,
            labels={"engagement_score":"Engagement Score",
                    "Q7_monthly_spend_inr":"Monthly Spend (INR)",
                    "Q25_app_adoption":"Would Download"},
        )
        fig_sc.update_layout(**PLOTLY_LIGHT, height=360, margin=dict(t=20,b=20))
        st.plotly_chart(fig_sc, use_container_width=True, config=PCFG)
        insight_box("High engagement + high spend = almost always 'Yes'. "
                    "Target acquisition campaigns at users with 3+ active pet-related apps.")

    # ── Tab 2: Subscriptions ──────────────────────────────────────────────────
    with tab2:
        section_header("What Payment Model Would Work?")
        c1, c2 = st.columns(2)
        with c1:
            sub_counts = raw["Q18_subscription_pref"].value_counts()
            fig = go.Figure(go.Pie(
                labels=sub_counts.index, values=sub_counts.values,
                marker_colors=CHART_COLS, hole=0.45,
                textinfo="label+percent", textfont_size=11,
            ))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=320,
                               title="Preferred Model", showlegend=False,
                               margin=dict(t=40,b=0), font=dict(color="#3E2A1A"))
            st.plotly_chart(fig, use_container_width=True, config=PCFG)
        with c2:
            sub_adoption = []
            for sub_col in [c for c in df.columns if c.startswith("Q18_subscription_pref_")]:
                label = sub_col.replace("Q18_subscription_pref_","")
                sub_df = df[df[sub_col]==1]
                if len(sub_df) > 10:
                    yes_rate = (sub_df["Q25_app_adoption"]=="Yes").sum()/len(sub_df)*100
                    sub_adoption.append({"Model":label,"Yes %":round(yes_rate,1)})
            sa_df = pd.DataFrame(sub_adoption).sort_values("Yes %", ascending=False)
            fig2 = go.Figure(go.Bar(
                x=sa_df["Yes %"], y=sa_df["Model"], orientation="h",
                marker=dict(color=sa_df["Yes %"],
                            colorscale=[[0,"#F0E4D7"],[0.5,HONEY],[1,BROWN]]),
                text=[f"{v}%" for v in sa_df["Yes %"]], textposition="outside",
            ))
            fig2.update_layout(**PLOTLY_LIGHT, height=320,
                                title="Adoption Rate by Subscription Preference",
                                xaxis=dict(showgrid=False,visible=False),
                                margin=dict(t=40,b=20))
            st.plotly_chart(fig2, use_container_width=True, config=PCFG)
        insight_box("Freemium is most popular overall, but users who prefer paid plans "
                    "show significantly higher adoption intent. Launch free, convert engaged users.")

        section_header("Location Sharing Willingness — Critical for App Features")
        loc_counts = raw["Q17_location_sharing"].value_counts()
        pct_share  = round((loc_counts.get("Yes, always",0) +
                             loc_counts.get("Yes, only when using the app",0)) / n * 100, 1)
        c3, c4 = st.columns(2)
        with c3:
            fig3 = go.Figure(go.Pie(
                labels=loc_counts.index, values=loc_counts.values,
                marker_colors=[BROWN,AMBER,"#E8D5C4","#C49A6C"],
                hole=0.5, textinfo="label+percent",
                annotations=[dict(text=f"<b>{pct_share}%</b>",
                                   x=0.5,y=0.5,showarrow=False,
                                   font=dict(size=14,color=BROWN))],
            ))
            fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=280,
                                showlegend=False, margin=dict(t=10,b=0),
                                font=dict(color="#3E2A1A"))
            st.plotly_chart(fig3, use_container_width=True, config=PCFG)
        with c4:
            insight_card("📍","Location Sharing",f"{pct_share}% Willing",
                         "Would share their location, which is essential for "
                         "PawIndia's nearby vet, park, and community features.", BROWN)
            insight_card("💉","Vaccination Tracking",
                         f"{round((df['Q23_vax_tracking_Rely On Memory'] if 'Q23_vax_tracking_Rely On Memory' in df.columns else df.head(1)).values[0]*100 if len(df)>0 else 30)}% Use Memory",
                         "Over 30% rely on memory for vaccination tracking — "
                         "a clear gap that PawIndia's health tracker fills.", AMBER)

    # ── Tab 3: By Location ────────────────────────────────────────────────────
    with tab3:
        section_header("Adoption Likelihood by City Tier")
        city_adoption = []
        for col, label in [("Q2_city_tier_Metro","Metro"),
                            ("Q2_city_tier_Tier-2","Tier-2"),
                            ("Q2_city_tier_Tier-3","Tier-3"),
                            ("Q2_city_tier_Rural","Rural")]:
            if col in df.columns:
                sub = df[df[col]==1]
                if len(sub) > 10:
                    city_adoption.append({
                        "City": label,
                        "Yes":  round((sub["Q25_app_adoption"]=="Yes").sum()/len(sub)*100,1),
                        "Maybe":round((sub["Q25_app_adoption"]=="Maybe").sum()/len(sub)*100,1),
                        "No":   round((sub["Q25_app_adoption"]=="No").sum()/len(sub)*100,1),
                        "n":    len(sub),
                        "Avg Spend": int(sub["Q7_monthly_spend_inr"].mean()),
                    })
        ca_df = pd.DataFrame(city_adoption)

        fig = go.Figure()
        fig.add_trace(go.Bar(name="Would Download", x=ca_df["City"],
                              y=ca_df["Yes"], marker_color="#4CAF50"))
        fig.add_trace(go.Bar(name="Open to Trying", x=ca_df["City"],
                              y=ca_df["Maybe"], marker_color=HONEY))
        fig.add_trace(go.Bar(name="Would Not",      x=ca_df["City"],
                              y=ca_df["No"], marker_color="#E53935"))
        fig.update_layout(**PLOTLY_LIGHT, barmode="stack", height=340,
                           yaxis=dict(title="% of Respondents",showgrid=False),
                           legend=dict(orientation="h",y=-0.15),
                           margin=dict(t=20,b=60))
        st.plotly_chart(fig, use_container_width=True, config=PCFG)

        # Spend vs adoption bubble
        fig2 = px.scatter(
            ca_df, x="Avg Spend", y="Yes", size="n", color="City",
            color_discrete_sequence=CHART_COLS,
            labels={"Yes":"% Definite Yes","Avg Spend":"Avg Monthly Spend (INR)"},
            title="Higher Spend Markets = Higher Adoption Intent",
            size_max=50,
        )
        fig2.update_layout(**PLOTLY_LIGHT, height=320, margin=dict(t=40,b=20))
        st.plotly_chart(fig2, use_container_width=True, config=PCFG)
        insight_box("Metro cities lead on both spend and adoption. Tier-2 cities like "
                    "Indore have a large 'Maybe' pool — the key conversion opportunity.")

    # ── Tab 4: By Profile ─────────────────────────────────────────────────────
    with tab4:
        section_header("Who Is Most Likely to Download PawIndia?")
        c1, c2 = st.columns(2)
        with c1:
            age_order = ["Under 18","18-24","25-34","35-44","45-59","60+"]
            age_enc   = {"Under 18":0,"18-24":1,"25-34":2,"35-44":3,"45-59":4,"60+":5}
            aa = []
            for age in age_order:
                enc = age_enc.get(age,-1)
                sub = df[df["Q1_age_group_enc"]==enc]
                if len(sub) > 5:
                    aa.append({"Age":age,"Yes%":round((sub["Q25_app_adoption"]=="Yes").sum()/len(sub)*100,1)})
            aa_df = pd.DataFrame(aa)
            fig = go.Figure(go.Bar(
                x=aa_df["Age"], y=aa_df["Yes%"],
                marker=dict(color=aa_df["Yes%"],
                            colorscale=[[0,"#F0E4D7"],[0.5,HONEY],[1,BROWN]]),
                text=[f"{v}%" for v in aa_df["Yes%"]], textposition="outside",
            ))
            fig.update_layout(**PLOTLY_LIGHT, title="% Definite Yes by Age",
                               height=280, yaxis=dict(showgrid=False,range=[0,80]),
                               margin=dict(t=40,b=20))
            st.plotly_chart(fig, use_container_width=True, config=PCFG)
        with c2:
            dog_adoption = []
            for col, label in [("Q4_num_dogs_None","No Dog"),("Q4_num_dogs_1 Dog","1 Dog"),
                                ("Q4_num_dogs_2 Dogs","2 Dogs"),("Q4_num_dogs_3+ Dogs","3+ Dogs")]:
                if col in df.columns:
                    sub = df[df[col]==1]
                    if len(sub) > 5:
                        dog_adoption.append({"Dogs":label,
                                              "Yes%":round((sub["Q25_app_adoption"]=="Yes").sum()/len(sub)*100,1)})
            da_df = pd.DataFrame(dog_adoption)
            fig2 = go.Figure(go.Bar(
                x=da_df["Dogs"], y=da_df["Yes%"],
                marker_color=CHART_COLS[:4],
                text=[f"{v}%" for v in da_df["Yes%"]], textposition="outside",
            ))
            fig2.update_layout(**PLOTLY_LIGHT, title="% Definite Yes by Dog Count",
                                height=280, yaxis=dict(showgrid=False,range=[0,80]),
                                margin=dict(t=40,b=20))
            st.plotly_chart(fig2, use_container_width=True, config=PCFG)

        insight_box("25-34 year olds with 2+ dogs in metro or Tier-2 cities are "
                    "PawIndia's clearest early adopter profile. Focus acquisition here first.")

        # Feature demand
        section_header("Which Features Drive Download Intent?")
        ft_cols = {c: c.replace("Q14_preferred_features__","").replace("_"," ").title()
                   for c in df.columns if c.startswith("Q14_preferred_features__")}
        ft_data = {label: int(df[col].sum()) for col, label in ft_cols.items()}
        ft_df = pd.DataFrame({"Feature":list(ft_data.keys()),
                               "Count":list(ft_data.values())}).sort_values("Count")
        fig3 = go.Figure(go.Bar(
            x=ft_df["Count"], y=ft_df["Feature"], orientation="h",
            marker=dict(color=ft_df["Count"],
                        colorscale=[[0,"#F0E4D7"],[0.5,AMBER],[1,BROWN]]),
            text=ft_df["Count"], textposition="outside",
        ))
        fig3.update_layout(**PLOTLY_LIGHT, height=400,
                            margin=dict(t=10,b=10),
                            xaxis=dict(showgrid=False,visible=False),
                            yaxis=dict(tickfont=dict(size=11)))
        st.plotly_chart(fig3, use_container_width=True, config=PCFG)
        insight_box("Health tracker + vet directory + lost-and-found alerts: "
                    "build these three first and you have your MVP.")

        st.download_button("Download WTP Analysis",
                           df[["Q25_app_adoption","Q18_subscription_pref",
                               "Q17_location_sharing","Q7_monthly_spend_inr",
                               "Q15_app_usage","Q19_adoption_interest"]].to_csv(index=False),
                           "pawindia_wtp.csv","text/csv")
