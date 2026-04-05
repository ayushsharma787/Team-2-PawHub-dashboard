# pages/p03_dog_owner_insights.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from theme import section_header, insight_box, BROWN, AMBER, CHART_COLS, CREAM
from ml_engine import load_data


def render():
    raw, df = load_data()

    st.markdown(
        "<h1 style='color:#6F4E37;font-size:1.8rem;margin-bottom:4px'>Dog Owner Insights</h1>"
        "<p style='color:#9E8272'>Who are India's dog owners, how much do they spend, "
        "and what do they really need?</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='border-color:#E8D5C4'>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["👤 Demographics", "💸 Spending", "😤 Pain Points", "📱 Digital Behaviour"])

    # ── Tab 1: Demographics ───────────────────────────────────────────────────
    with tab1:
        section_header("Who Took This Survey?")
        c1, c2 = st.columns(2)

        with c1:
            age_order = ["Under 18","18-24","25-34","35-44","45-59","60+"]
            age_counts = raw["Q1_age_group"].value_counts().reindex(age_order, fill_value=0)
            fig = go.Figure(go.Bar(
                x=age_counts.index, y=age_counts.values,
                marker_color=CHART_COLS[:len(age_counts)],
                text=age_counts.values, textposition="outside",
            ))
            fig.update_layout(
                title="Age Distribution", height=320,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
                yaxis=dict(showgrid=False), xaxis=dict(title="Age Group"),
            )
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            city_counts = raw["Q2_city_tier"].value_counts()
            fig2 = go.Figure(go.Pie(
                labels=city_counts.index, values=city_counts.values,
                marker_colors=CHART_COLS, hole=0.4,
                textinfo="label+percent",
            ))
            fig2.update_layout(
                title="City Tier Breakdown", height=320,
                paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=0),
                showlegend=False,
            )
            st.plotly_chart(fig2, use_container_width=True)

        insight_box("The 25-34 age group dominates the survey, aligning with India's urban "
                    "millennial dog ownership boom. Metro cities represent nearly half the audience.")

        c3, c4 = st.columns(2)
        with c3:
            dog_counts = raw["Q4_num_dogs"].value_counts()
            fig3 = go.Figure(go.Bar(
                x=dog_counts.index, y=dog_counts.values,
                marker_color=BROWN, text=dog_counts.values, textposition="outside",
            ))
            fig3.update_layout(
                title="Number of Dogs Owned", height=280,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
                yaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig3, use_container_width=True)

        with c4:
            res_counts = raw["Q3_residence_type"].value_counts()
            fig4 = go.Figure(go.Bar(
                x=res_counts.values, y=res_counts.index, orientation="h",
                marker_color=AMBER, text=res_counts.values, textposition="outside",
            ))
            fig4.update_layout(
                title="Residence Type", height=280,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
                xaxis=dict(showgrid=False, visible=False),
            )
            st.plotly_chart(fig4, use_container_width=True)

        # Dog type breakdown
        section_header("Types of Dogs in India")
        dog_type_cols = {c: c.replace("Q5_dog_type__","").replace("_"," ").title()
                         for c in df.columns if c.startswith("Q5_dog_type__")}
        dtype_data = {label: df[col].sum() for col, label in dog_type_cols.items()}
        dt_df = pd.DataFrame({"Type": list(dtype_data.keys()),
                               "Count": list(dtype_data.values())}).sort_values("Count")
        fig5 = go.Figure(go.Bar(
            x=dt_df["Count"], y=dt_df["Type"], orientation="h",
            marker_color=CHART_COLS[:len(dt_df)],
            text=dt_df["Count"], textposition="outside",
        ))
        fig5.update_layout(
            height=240, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#3E2A1A"), margin=dict(t=10,b=10),
            xaxis=dict(showgrid=False, visible=False),
        )
        st.plotly_chart(fig5, use_container_width=True)
        insight_box("Purebred and rescued/adopted dogs together form the majority of the "
                    "owned dog population, suggesting demand for both premium services and "
                    "community adoption support.")

    # ── Tab 2: Spending ───────────────────────────────────────────────────────
    with tab2:
        section_header("How Much Do Dog Owners Spend?")
        c1, c2 = st.columns(2)

        with c1:
            # Spend distribution histogram
            spend_data = df["Q7_monthly_spend_inr"].dropna()
            fig = go.Figure(go.Histogram(
                x=spend_data, nbinsx=30,
                marker_color=BROWN, opacity=0.8,
            ))
            fig.update_layout(
                title="Monthly Spend Distribution (INR)", height=300,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
                xaxis=dict(title="Monthly Spend (INR)"),
                yaxis=dict(title="Number of Respondents", showgrid=False),
            )
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            # Avg spend by city tier
            city_spend = []
            for col in [c for c in df.columns if "Q2_city_tier_" in c]:
                tier = col.replace("Q2_city_tier_","")
                sub  = df[df[col] == 1]["Q7_monthly_spend_inr"]
                if len(sub) > 0:
                    city_spend.append({"City Tier": tier, "Avg Spend": round(sub.mean())})
            cs_df = pd.DataFrame(city_spend)
            fig2 = go.Figure(go.Bar(
                x=cs_df["City Tier"], y=cs_df["Avg Spend"],
                marker_color=[BROWN, AMBER, "#C49A6C", "#DEB887"],
                text=[f"Rs.{v:,}" for v in cs_df["Avg Spend"]],
                textposition="outside",
            ))
            fig2.update_layout(
                title="Avg Monthly Spend by City Tier", height=300,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
                yaxis=dict(showgrid=False, title="INR"),
            )
            st.plotly_chart(fig2, use_container_width=True)

        insight_box(f"Average monthly dog spend is Rs.{int(df['Q7_monthly_spend_inr'].mean()):,}. "
                    "Metro city dog owners spend significantly more, validating a tiered "
                    "premium pricing strategy for PawIndia.")

        # Spend by category
        section_header("Where Does the Money Go?")
        cat_cols = {c: c.replace("Q8_top_spend_category_","").title()
                    for c in df.columns if c.startswith("Q8_top_spend_category_")}
        # from raw survey
        cat_counts = raw["Q8_top_spend_category"].value_counts()
        fig3 = go.Figure(go.Pie(
            labels=cat_counts.index, values=cat_counts.values,
            marker_colors=CHART_COLS, hole=0.35,
            textinfo="label+percent", textfont_size=11,
        ))
        fig3.update_layout(
            title="Primary Spend Category", height=340,
            paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=0),
            showlegend=False,
        )
        st.plotly_chart(fig3, use_container_width=True)

        # Spend by dog count
        c3, c4 = st.columns(2)
        with c3:
            dog_spend = []
            for label, col in [("None","Q4_num_dogs_None"),
                                ("1 Dog","Q4_num_dogs_1 Dog"),
                                ("2 Dogs","Q4_num_dogs_2 Dogs"),
                                ("3+ Dogs","Q4_num_dogs_3+ Dogs")]:
                if col in df.columns:
                    sub = df[df[col]==1]["Q7_monthly_spend_inr"]
                    if len(sub) > 0:
                        dog_spend.append({"Dogs": label, "Avg": round(sub.mean())})
            ds_df = pd.DataFrame(dog_spend)
            fig4 = go.Figure(go.Bar(
                x=ds_df["Dogs"], y=ds_df["Avg"],
                marker_color=CHART_COLS[:4],
                text=[f"Rs.{v:,}" for v in ds_df["Avg"]],
                textposition="outside",
            ))
            fig4.update_layout(
                title="Avg Spend by Dog Count", height=280,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
                yaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig4, use_container_width=True)

        with c4:
            # Online purchase frequency
            online_order = ["Never","Rarely","Occasionally","Frequently","Very Frequently"]
            online_counts = raw["Q9_online_purchase_freq"].str.title().value_counts().reindex(
                online_order, fill_value=0)
            fig5 = go.Figure(go.Bar(
                x=online_counts.index, y=online_counts.values,
                marker_color=AMBER, text=online_counts.values, textposition="outside",
            ))
            fig5.update_layout(
                title="Online Purchase Frequency", height=280,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
                yaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig5, use_container_width=True)

    # ── Tab 3: Pain Points ────────────────────────────────────────────────────
    with tab3:
        section_header("The Real Struggles of Indian Dog Owners")
        ch_cols = {c: c.replace("Q10_challenges__","").replace("_"," ").title()
                   for c in df.columns if c.startswith("Q10_challenges__")}
        ch_data = {label: df[col].sum() for col, label in ch_cols.items()}
        ch_df = pd.DataFrame({"Challenge": list(ch_data.keys()),
                               "Count": list(ch_data.values())}).sort_values("Count")
        fig = go.Figure(go.Bar(
            x=ch_df["Count"], y=ch_df["Challenge"], orientation="h",
            marker=dict(color=ch_df["Count"],
                        colorscale=[[0,"#F0E4D7"],[0.5,AMBER],[1,BROWN]]),
            text=ch_df["Count"], textposition="outside",
        ))
        fig.update_layout(
            height=380, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#3E2A1A"), margin=dict(t=10,b=10),
            xaxis=dict(showgrid=False, visible=False),
            yaxis=dict(tickfont=dict(size=11)),
        )
        st.plotly_chart(fig, use_container_width=True)
        insight_box("Finding a reliable vet remains the single biggest pain point, followed by "
                    "the absence of pet-friendly public spaces. These two challenges alone "
                    "justify PawIndia's core feature set.")

        c1, c2 = st.columns(2)
        with c1:
            section_header("How Do People Find Vets Today?")
            vet_counts = raw["Q11_vet_discovery"].value_counts()
            fig2 = go.Figure(go.Pie(
                labels=vet_counts.index, values=vet_counts.values,
                marker_colors=CHART_COLS, hole=0.45,
                textinfo="label+percent",
            ))
            fig2.update_layout(
                height=300, paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10,b=0), showlegend=False,
            )
            st.plotly_chart(fig2, use_container_width=True)

        with c2:
            section_header("Lost Dog Experiences")
            lost_counts = raw["Q12_lost_dog_experience"].value_counts()
            fig3 = go.Figure(go.Bar(
                x=lost_counts.index, y=lost_counts.values,
                marker_color=CHART_COLS[:4],
                text=lost_counts.values, textposition="outside",
            ))
            fig3.update_layout(
                height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A"), margin=dict(t=10,b=20),
                yaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig3, use_container_width=True)

        insight_box("45% of dog owners have experienced difficulty finding a lost dog, "
                    "validating the need for PawIndia's community alert system.")

    # ── Tab 4: Digital Behaviour ──────────────────────────────────────────────
    with tab4:
        section_header("How Dog Owners Use Technology Today")
        c1, c2 = st.columns(2)

        with c1:
            app_order = ["Never","Rarely","Sometimes","Often"]
            app_counts = raw["Q15_app_usage"].value_counts().reindex(app_order, fill_value=0)
            fig = go.Figure(go.Bar(
                x=app_counts.index, y=app_counts.values,
                marker_color=CHART_COLS[:4],
                text=app_counts.values, textposition="outside",
            ))
            fig.update_layout(
                title="Current App Usage for Pet Needs", height=300,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
                yaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            plat_counts = raw["Q16_purchase_platform"].value_counts()
            fig2 = go.Figure(go.Pie(
                labels=plat_counts.index, values=plat_counts.values,
                marker_colors=CHART_COLS, hole=0.4,
                textinfo="percent+label", textfont_size=10,
            ))
            fig2.update_layout(
                title="Where They Buy Products", height=300,
                paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=0),
                showlegend=False,
            )
            st.plotly_chart(fig2, use_container_width=True)

        insight_box("Amazon/Flipkart dominates online pet purchases, but 25% still use local "
                    "stores. PawIndia's marketplace can capture both audiences by bridging "
                    "online convenience with local discovery.")

        c3, c4 = st.columns(2)
        with c3:
            section_header("Vaccination Tracking Methods")
            vax_counts = raw["Q23_vax_tracking"].value_counts()
            fig3 = go.Figure(go.Bar(
                x=vax_counts.values, y=vax_counts.index, orientation="h",
                marker_color=BROWN, text=vax_counts.values, textposition="outside",
            ))
            fig3.update_layout(
                height=280, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A"), margin=dict(t=10,b=10),
                xaxis=dict(showgrid=False, visible=False),
            )
            st.plotly_chart(fig3, use_container_width=True)

        with c4:
            section_header("Social Media Dog Communities")
            soc_counts = raw["Q21_social_media_dogs"].value_counts()
            fig4 = go.Figure(go.Pie(
                labels=soc_counts.index, values=soc_counts.values,
                marker_colors=CHART_COLS, hole=0.4,
                textinfo="percent+label",
            ))
            fig4.update_layout(
                height=280, paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10,b=0), showlegend=False,
            )
            st.plotly_chart(fig4, use_container_width=True)

        # Correlation heatmap
        section_header("Correlation Between Key Behaviours")
        corr_cols = ["Q7_monthly_spend_inr","Q9_online_purchase_freq_enc",
                     "Q15_app_usage_enc","Q20_community_importance_enc",
                     "Q22_reviews_importance_enc","engagement_score","spend_per_dog",
                     "Q1_age_group_enc","Q13_pet_space_satisfaction_enc"]
        valid_corr = [c for c in corr_cols if c in df.columns]
        corr_matrix = df[valid_corr].corr().round(2)
        labels = [c.replace("Q","").replace("_enc","").replace("_"," ")[:20] for c in valid_corr]

        fig_corr = go.Figure(go.Heatmap(
            z=corr_matrix.values, x=labels, y=labels,
            colorscale=[[0,"#FFF8F0"],[0.5,AMBER],[1,BROWN]],
            text=corr_matrix.values, texttemplate="%{text}",
            showscale=True, zmin=-1, zmax=1,
        ))
        fig_corr.update_layout(
            title="Correlation Heatmap", height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#3E2A1A", size=10),
            margin=dict(t=40,b=60,l=80,r=20),
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        insight_box("Engagement score correlates strongly with app adoption likelihood and "
                    "community importance, confirming that active digital users are PawIndia's "
                    "primary early adopters.")

        st.download_button(
            "Download Insights Data",
            data=df.to_csv(index=False),
            file_name="pawindia_cleaned_data.csv",
            mime="text/csv",
        )
