# pages/p04_will_they_buy.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from theme import section_header, insight_box, BROWN, AMBER, CHART_COLS
from ml_engine import load_data


def render():
    raw, df = load_data()

    st.markdown(
        "<h1 style='color:#6F4E37;font-size:1.8rem;margin-bottom:4px'>Will They Buy?</h1>"
        "<p style='color:#9E8272'>Understanding willingness to pay, subscription preferences, "
        "and which segments are most likely to adopt PawIndia</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='border-color:#E8D5C4'>", unsafe_allow_html=True)

    total = len(df)
    pct_yes   = round((df["Q25_app_adoption"]=="Yes").sum()/total*100, 1)
    pct_maybe = round((df["Q25_app_adoption"]=="Maybe").sum()/total*100, 1)
    pct_no    = round((df["Q25_app_adoption"]=="No").sum()/total*100, 1)

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Will Download", f"{pct_yes}%",   delta="Definite adopters")
    c2.metric("Open to It",    f"{pct_maybe}%", delta="Conditional adopters")
    c3.metric("Would Not",     f"{pct_no}%",    delta="Lost audience")
    c4.metric("Total Reachable", f"{pct_yes+pct_maybe}%", delta="Yes + Maybe")

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["💳 Subscription Prefs", "📍 By Location", "👤 By Profile", "⭐ Feature Demand"])

    # ── Tab 1: Subscription ───────────────────────────────────────────────────
    with tab1:
        section_header("What Payment Model Would Work?")
        c1, c2 = st.columns(2)
        with c1:
            sub_counts = raw["Q18_subscription_pref"].value_counts()
            fig = go.Figure(go.Pie(
                labels=sub_counts.index, values=sub_counts.values,
                marker_colors=CHART_COLS, hole=0.45,
                textinfo="label+percent", textfont_size=11,
            ))
            fig.update_layout(
                title="Preferred Subscription Model", height=340,
                paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=0),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            # Adoption rate by subscription preference
            sub_adoption = []
            for sub_col in [c for c in df.columns if c.startswith("Q18_subscription_pref_")]:
                label = sub_col.replace("Q18_subscription_pref_","")
                sub_df = df[df[sub_col]==1]
                if len(sub_df) > 10:
                    yes_rate = (sub_df["Q25_app_adoption"]=="Yes").sum()/len(sub_df)*100
                    sub_adoption.append({"Subscription Pref": label,
                                          "% Would Download": round(yes_rate,1),
                                          "n": len(sub_df)})
            sa_df = pd.DataFrame(sub_adoption).sort_values("% Would Download", ascending=False)
            fig2 = go.Figure(go.Bar(
                x=sa_df["% Would Download"], y=sa_df["Subscription Pref"], orientation="h",
                marker=dict(color=sa_df["% Would Download"],
                            colorscale=[[0,"#F0E4D7"],[0.5,AMBER],[1,BROWN]]),
                text=[f"{v}%" for v in sa_df["% Would Download"]],
                textposition="outside",
            ))
            fig2.update_layout(
                title="App Adoption Rate by Subscription Preference", height=340,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
                xaxis=dict(showgrid=False, visible=False),
            )
            st.plotly_chart(fig2, use_container_width=True)

        insight_box("Freemium is the preferred model overall, but respondents who prefer "
                    "paid subscriptions (monthly or annual) show a significantly higher "
                    "adoption intent. Launch free, convert the engaged users to paid.")

        # Detailed subscription table
        section_header("Subscription Preference Breakdown")
        sub_raw = raw["Q18_subscription_pref"].value_counts().reset_index()
        sub_raw.columns = ["Subscription Model", "Count"]
        sub_raw["% of Respondents"] = (sub_raw["Count"]/len(raw)*100).round(1)
        sub_raw["Revenue Potential"] = sub_raw["Subscription Model"].map({
            "Free with ads":          "Low (ad revenue only)",
            "Freemium":               "Medium (upsell opportunity)",
            "Monthly subscription (Rs.99-Rs.199/month)": "High (recurring)",
            "Annual subscription (Rs.699-Rs.999/year)":  "High (loyal users)",
            "One-time lifetime purchase": "Medium (one-off)",
            "I would not pay for a pet app": "None",
        }).fillna("Medium")
        st.dataframe(sub_raw, use_container_width=True, hide_index=True)

    # ── Tab 2: By Location ────────────────────────────────────────────────────
    with tab2:
        section_header("Adoption Likelihood by City Tier")
        city_adoption = []
        for col, label in [("Q2_city_tier_Metro","Metro"),
                            ("Q2_city_tier_Tier-2","Tier-2"),
                            ("Q2_city_tier_Tier-3","Tier-3"),
                            ("Q2_city_tier_Rural","Rural")]:
            if col in df.columns:
                sub = df[df[col]==1]
                if len(sub) > 10:
                    yes = (sub["Q25_app_adoption"]=="Yes").sum()/len(sub)*100
                    maybe = (sub["Q25_app_adoption"]=="Maybe").sum()/len(sub)*100
                    no  = (sub["Q25_app_adoption"]=="No").sum()/len(sub)*100
                    city_adoption.append({"City": label, "Yes":round(yes,1),
                                           "Maybe":round(maybe,1), "No":round(no,1),
                                           "n":len(sub)})
        ca_df = pd.DataFrame(city_adoption)

        fig = go.Figure()
        fig.add_trace(go.Bar(name="Would Download", x=ca_df["City"],
                              y=ca_df["Yes"], marker_color=BROWN))
        fig.add_trace(go.Bar(name="Open to Trying", x=ca_df["City"],
                              y=ca_df["Maybe"], marker_color=AMBER))
        fig.add_trace(go.Bar(name="Would Not", x=ca_df["City"],
                              y=ca_df["No"], marker_color="#E8D5C4"))
        fig.update_layout(
            barmode="stack", title="App Adoption by City Tier (%)", height=340,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
            yaxis=dict(title="% of Respondents", showgrid=False),
            legend=dict(orientation="h", y=-0.15),
        )
        st.plotly_chart(fig, use_container_width=True)
        insight_box("Metro city residents show the highest definite adoption rate. "
                    "However, Tier-2 cities like Indore and Jaipur have a large 'Maybe' "
                    "pool, making them a critical conversion target for PawIndia's launch.")

        # Avg spend by city with adoption overlay
        section_header("Spend vs Adoption by City Tier")
        fig2 = go.Figure()
        for i, row in ca_df.iterrows():
            spend_col = f"Q2_city_tier_{row['City']}" if row["City"] != "Tier-2" else "Q2_city_tier_Tier-2"
            # approximate
        city_spend_map = {"Metro":None,"Tier-2":None,"Tier-3":None,"Rural":None}
        for col, label in [("Q2_city_tier_Metro","Metro"),("Q2_city_tier_Tier-2","Tier-2"),
                            ("Q2_city_tier_Tier-3","Tier-3"),("Q2_city_tier_Rural","Rural")]:
            if col in df.columns:
                city_spend_map[label] = int(df[df[col]==1]["Q7_monthly_spend_inr"].mean())

        ca_df["Avg Spend"] = ca_df["City"].map(city_spend_map)
        ca_df_valid = ca_df.dropna(subset=["Avg Spend"])
        fig2 = px.scatter(ca_df_valid, x="Avg Spend", y="Yes",
                           size="n", color="City",
                           color_discrete_sequence=CHART_COLS,
                           labels={"Yes":"% Definite Yes","Avg Spend":"Avg Monthly Spend (INR)"},
                           title="Higher Spend Markets Show Higher Adoption Intent")
        fig2.update_layout(
            height=320, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Tab 3: By Profile ─────────────────────────────────────────────────────
    with tab3:
        section_header("Who Is Most Likely to Download PawIndia?")

        # By age
        age_adoption = []
        age_order = ["Under 18","18-24","25-34","35-44","45-59","60+"]
        for age in age_order:
            sub = raw[raw["Q1_age_group"]==age]
            if len(sub) > 5:
                merged = df[df.index.isin(sub.index)] if "Q25_app_adoption" in df.columns else df
                yes_r = (df.loc[df.index.isin(sub.index), "Q25_app_adoption"]=="Yes").sum()
                tot   = len(sub)
                age_adoption.append({"Age":age, "Pct Yes":round(yes_r/tot*100,1), "n":tot})
        aa_df = pd.DataFrame(age_adoption)

        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure(go.Bar(
                x=aa_df["Age"], y=aa_df["Pct Yes"],
                marker=dict(color=aa_df["Pct Yes"],
                            colorscale=[[0,"#F0E4D7"],[0.5,AMBER],[1,BROWN]]),
                text=[f"{v}%" for v in aa_df["Pct Yes"]],
                textposition="outside",
            ))
            fig.update_layout(
                title="% Definite Yes by Age Group", height=300,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
                yaxis=dict(showgrid=False, range=[0,80]),
            )
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            # By dog ownership
            dog_adoption = []
            for col, label in [("Q4_num_dogs_None","No Dog (yet)"),
                                ("Q4_num_dogs_1 Dog","1 Dog"),
                                ("Q4_num_dogs_2 Dogs","2 Dogs"),
                                ("Q4_num_dogs_3+ Dogs","3+ Dogs")]:
                if col in df.columns:
                    sub = df[df[col]==1]
                    if len(sub) > 5:
                        yes = (sub["Q25_app_adoption"]=="Yes").sum()/len(sub)*100
                        dog_adoption.append({"Dogs":label,"Pct Yes":round(yes,1),"n":len(sub)})
            da_df = pd.DataFrame(dog_adoption)
            fig2 = go.Figure(go.Bar(
                x=da_df["Dogs"], y=da_df["Pct Yes"],
                marker_color=CHART_COLS[:4],
                text=[f"{v}%" for v in da_df["Pct Yes"]],
                textposition="outside",
            ))
            fig2.update_layout(
                title="% Definite Yes by Dog Count", height=300,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
                yaxis=dict(showgrid=False, range=[0,80]),
            )
            st.plotly_chart(fig2, use_container_width=True)

        insight_box("25-34 year olds with 1-2 dogs living in metro or Tier-2 cities are "
                    "the clearest early adopter segment for PawIndia. Focus acquisition "
                    "spend here first.")

        # Location sharing willingness
        section_header("Are They Willing to Share Location?")
        loc_counts = raw["Q17_location_sharing"].value_counts()
        pct_share = round((loc_counts.get("Yes, always",0) + loc_counts.get("Yes, only when using the app",0)) / len(raw) * 100, 1)

        fig3 = go.Figure(go.Pie(
            labels=loc_counts.index, values=loc_counts.values,
            marker_colors=[BROWN, AMBER, "#E8D5C4", "#C49A6C"],
            hole=0.5, textinfo="label+percent",
        ))
        fig3.update_layout(
            height=300, paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10,b=0), showlegend=False,
            annotations=[dict(text=f"<b>{pct_share}%</b><br>Would<br>Share",
                               x=0.5, y=0.5, showarrow=False,
                               font=dict(size=13, color=BROWN))],
        )
        st.plotly_chart(fig3, use_container_width=True)
        insight_box(f"{pct_share}% of respondents are willing to share their location, "
                    "which is critical for PawIndia's nearby vet, park, and community features.")

    # ── Tab 4: Feature Demand ─────────────────────────────────────────────────
    with tab4:
        section_header("Which Features Would Make People Download PawIndia?")
        feat_cols = {c: c.replace("Q14_preferred_features__","").replace("_"," ").title()
                     for c in df.columns if c.startswith("Q14_preferred_features__")}
        feat_data = {label: df[col].sum() for col, label in feat_cols.items()}
        ft_df = pd.DataFrame({"Feature": list(feat_data.keys()),
                               "Count": list(feat_data.values())}).sort_values("Count")
        fig = go.Figure(go.Bar(
            x=ft_df["Count"], y=ft_df["Feature"], orientation="h",
            marker=dict(color=ft_df["Count"],
                        colorscale=[[0,"#F0E4D7"],[0.5,AMBER],[1,BROWN]]),
            text=ft_df["Count"], textposition="outside",
        ))
        fig.update_layout(
            height=420, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#3E2A1A"), margin=dict(t=10,b=10),
            xaxis=dict(showgrid=False, visible=False),
            yaxis=dict(tickfont=dict(size=11)),
        )
        st.plotly_chart(fig, use_container_width=True)
        insight_box("Health and vaccination tracking is the single most demanded feature, "
                    "closely followed by the nearby vet directory and lost-and-found alerts. "
                    "Build these three first.")

        # Adoption interest
        section_header("Interest in Adopting or Fostering Dogs")
        adopt_counts = raw["Q19_adoption_interest"].value_counts()
        pct_open = round((adopt_counts.get("Yes, actively looking",0) +
                           adopt_counts.get("Yes, considering it",0)) / len(raw) * 100, 1)
        fig2 = go.Figure(go.Pie(
            labels=adopt_counts.index, values=adopt_counts.values,
            marker_colors=CHART_COLS, hole=0.45,
            textinfo="label+percent",
        ))
        fig2.update_layout(
            height=300, paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10,b=0), showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)
        insight_box(f"{pct_open}% are actively considering adoption or fostering, "
                    "making PawIndia's adoption network feature a strong community growth driver.")

        st.download_button(
            "Download Willingness-to-Pay Analysis",
            data=df[["Q25_app_adoption","Q18_subscription_pref","Q17_location_sharing",
                      "Q7_monthly_spend_inr","Q15_app_usage",
                      "Q19_adoption_interest"]].to_csv(index=False),
            file_name="pawindia_wtp_analysis.csv",
            mime="text/csv",
        )
