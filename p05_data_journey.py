# p05_data_journey.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from theme import (section_header, insight_box, page_header, live_bar,
                   BROWN, AMBER, HONEY, PLOTLY_LIGHT, PCFG)
from ml_engine import load_data


def render():
    raw, df = load_data()
    n = len(df)
    page_header("🔬","Data Journey",
                "How we built 2,000 realistic survey responses and cleaned them for ML")
    live_bar(n, "Data Journey")

    tab1, tab2, tab3 = st.tabs(
        ["🧪 Synthetic Generation","🧹 Cleaning Pipeline","📊 Before vs After"])

    # ── Tab 1: Generation ─────────────────────────────────────────────────────
    with tab1:
        section_header("Why Synthetic Data?")
        st.markdown(
            """<div class="info-card">
            <p style="color:#3E2A1A;line-height:1.8;font-size:0.95rem">
            PawIndia is a new product with no existing user base. We generated 2,000 synthetic
            respondents that mimic realistic Indian dog owner behaviour, grounded in known market
            trends, urban-rural divides in pet culture, and the digital behaviour patterns of
            Indian millennials. Real-world noise and inconsistencies were deliberately injected
            so the dataset behaves like a genuine survey rather than a clean simulation.
            </p></div>""",
            unsafe_allow_html=True,
        )

        section_header("Distribution Design Decisions")
        steps = [
            ("Age Skew", "35% aged 25-34, reflecting India's millennial dog ownership boom. Under-18 and 60+ intentionally underrepresented to match realistic survey participation."),
            ("City Tier Bias", "45% Metro, 30% Tier-2, 18% Tier-3, 7% Rural — mirrors India's pet care market concentration where metros drive organised pet spending."),
            ("Monthly Spend", "Generated via triangular distribution anchored to city tier and dog count. Metro owners get a 1.3x multiplier, producing a realistic right-skewed distribution."),
            ("App Adoption Target (Q25)", "Not randomly assigned. Computed from a scoring function using city tier, age, app usage, and subscription preference — producing 48% Yes / 37% Maybe / 15% No."),
            ("Multi-Select Questions", "Q10 and Q14 allowed up to 3 selections with probability weights based on known Indian pet owner pain points from secondary research."),
            ("Correlated Responses", "Higher-spend owners more likely to report vet challenges. Metro owners more likely to use apps. These correlations mirror real behaviour."),
        ]
        for i, (title, desc) in enumerate(steps):
            st.markdown(
                f"""<div class="step-box">
                <span style="background:#6F4E37;color:white;border-radius:50%;
                width:26px;height:26px;display:inline-flex;align-items:center;
                justify-content:center;font-weight:700;font-size:0.82rem;
                margin-right:10px">{i+1}</span>
                <strong style="color:#3E2A1A">{title}</strong>
                <p style="color:#6F4E37;margin:6px 0 0 36px;font-size:0.88rem;line-height:1.6">{desc}</p>
                </div>""",
                unsafe_allow_html=True,
            )

        section_header("Noise Injected to Mimic Real Surveys")
        noise_items = [
            ("Duplicate Rows", "20 rows duplicated — simulates accidental double submissions."),
            ("Negative Spend Values", "~2% of Q7 numeric entries made negative — simulates data entry errors."),
            ("Implausibly High Spend", "~2% of spend values multiplied by 10 — simulates an extra zero typo."),
            ("Missing Numeric Spend", "15% left numeric spend blank, using only the range selector."),
            ("Capitalisation Inconsistency", "~3% of city tier entries lowercased — simulates form input variation."),
            ("Whitespace Padding", "~4% of spend range entries had leading/trailing spaces."),
            ("Non-Owners Answering Dog Questions", "~40% of non-dog-owners still partially answered dog-specific questions."),
            ("Over-Selection on Multi-Select", "~5% selected more than the instructed maximum of 3 options."),
            ("Blank Target Variable", "~2% had a blank Q25 — simulates incomplete form submissions."),
        ]
        for title, desc in noise_items:
            st.markdown(
                f"""<div style="display:flex;align-items:flex-start;margin-bottom:12px;
                padding:12px 16px;background:#FFF8F0;border-radius:10px;
                border:1px solid #E8D5C4">
                <span style="color:{AMBER};font-size:1.1rem;margin-right:10px;flex-shrink:0">⚠</span>
                <div>
                <strong style="color:#3E2A1A">{title}</strong>
                <p style="color:#6F4E37;margin:2px 0;font-size:0.86rem">{desc}</p>
                </div></div>""",
                unsafe_allow_html=True,
            )

        section_header("Raw Data Sample (First 8 Rows)")
        display_cols = ["respondent_id","Q1_age_group","Q2_city_tier","Q4_num_dogs",
                        "Q7_monthly_spend_inr","Q7_spend_range","Q25_app_adoption"]
        valid = [c for c in display_cols if c in raw.columns]
        st.dataframe(raw[valid].head(8), use_container_width=True, hide_index=True)

        section_header("Missing Values in Raw Dataset")
        missing = raw.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=False)
        if not missing.empty:
            fig = go.Figure(go.Bar(
                x=missing.values, y=missing.index, orientation="h",
                marker_color=AMBER, text=missing.values, textposition="outside",
            ))
            fig.update_layout(**PLOTLY_LIGHT, height=max(250, len(missing)*28),
                               margin=dict(t=10,b=10),
                               xaxis=dict(showgrid=False,visible=False))
            st.plotly_chart(fig, use_container_width=True, config=PCFG)

    # ── Tab 2: Cleaning Pipeline ──────────────────────────────────────────────
    with tab2:
        section_header("10-Step Cleaning and Transformation Pipeline")
        steps = [
            ("Step 1","Remove Duplicates",
             f"Identified and removed duplicate rows based on all non-ID columns. "
             f"{len(raw) - len(raw.drop_duplicates(subset=[c for c in raw.columns if c!='respondent_id']))} duplicate rows removed."),
            ("Step 2","Drop Incomplete Target Rows",
             "Rows with blank Q25 removed entirely — the target variable is essential for all models."),
            ("Step 3","Standardise Text Columns",
             "All text stripped of whitespace and converted to title case, eliminating capitalisation inconsistencies."),
            ("Step 4","Fix Numeric Spend (Q7)",
             "Negative values nulled. Values above Rs.50,000 nulled as implausible. Missing values imputed from range midpoints then group medians by dog count."),
            ("Step 5","Impute Categorical Missing Values",
             "Mode imputation within relevant groups (e.g. spend category imputed within dog-count group). Global mode for standalone columns."),
            ("Step 6","Ordinal Encoding",
             "Ordered categoricals (age, satisfaction, app usage, etc.) encoded as integers preserving natural order for regression and distance-based models."),
            ("Step 7","One-Hot Encoding",
             "Nominal categoricals (city tier, residence, subscription preference, etc.) one-hot encoded into binary columns."),
            ("Step 8","Multi-Select Expansion",
             "Q5, Q10, and Q14 pipe-separated multi-select strings expanded into individual binary flag columns."),
            ("Step 9","Feature Engineering",
             "Three derived features created: spend_per_dog (Q7 / dog count), engagement_score (app usage + online freq + reviews importance), Q25_binary (Yes=1, Maybe/No=0)."),
            ("Step 10","Final Validation",
             f"Final dataset: {len(df):,} rows x {len(df.columns)} columns. Zero missing values confirmed."),
        ]
        for step, title, desc in steps:
            st.markdown(
                f"""<div class="step-box">
                <span style="color:{AMBER};font-size:0.7rem;font-weight:700;
                text-transform:uppercase;letter-spacing:1px">{step}</span>
                <strong style="color:#3E2A1A;display:block;margin:4px 0">{title}</strong>
                <p style="color:#6F4E37;margin:0;font-size:0.88rem;line-height:1.6">{desc}</p>
                </div>""",
                unsafe_allow_html=True,
            )

    # ── Tab 3: Before vs After ────────────────────────────────────────────────
    with tab3:
        section_header("Dataset Comparison: Raw vs Cleaned")
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Raw Rows",      f"{len(raw):,}")
        c2.metric("Cleaned Rows",  f"{len(df):,}", delta=f"-{len(raw)-len(df)} removed")
        c3.metric("Raw Columns",   str(len(raw.columns)))
        c4.metric("Clean Columns", str(len(df.columns)), delta=f"+{len(df.columns)-len(raw.columns)} engineered")

        st.markdown("<br>", unsafe_allow_html=True)

        section_header("Missing Values: Before and After")
        raw_miss   = int(raw.isnull().sum().sum())
        clean_miss = int(df.isnull().sum().sum())
        fig = go.Figure(go.Bar(
            x=["Raw Dataset","Cleaned Dataset"],
            y=[raw_miss, clean_miss],
            marker_color=[AMBER, "#4CAF50"],
            text=[raw_miss, clean_miss], textposition="outside",
        ))
        fig.update_layout(**PLOTLY_LIGHT, height=280,
                           yaxis=dict(showgrid=False, title="Total Missing Values"),
                           margin=dict(t=10,b=20))
        st.plotly_chart(fig, use_container_width=True, config=PCFG)
        insight_box(f"Cleaning reduced total missing values from {raw_miss:,} to {clean_miss}. "
                    "The cleaned dataset is fully ready for all ML algorithms.")

        section_header("Spend Distribution: Raw vs Cleaned")
        col1, col2 = st.columns(2)
        with col1:
            raw_spend = pd.to_numeric(raw["Q7_monthly_spend_inr"], errors="coerce").dropna()
            fig2 = go.Figure(go.Histogram(x=raw_spend, nbinsx=40,
                                           marker_color=AMBER, opacity=0.8))
            fig2.update_layout(**PLOTLY_LIGHT, title="Raw Spend (includes errors)", height=260,
                                xaxis=dict(title="INR"), yaxis=dict(showgrid=False),
                                margin=dict(t=40,b=20))
            st.plotly_chart(fig2, use_container_width=True, config=PCFG)
        with col2:
            fig3 = go.Figure(go.Histogram(x=df["Q7_monthly_spend_inr"].dropna(),
                                           nbinsx=40, marker_color=BROWN, opacity=0.8))
            fig3.update_layout(**PLOTLY_LIGHT, title="Cleaned Spend (outliers removed)", height=260,
                                xaxis=dict(title="INR"), yaxis=dict(showgrid=False),
                                margin=dict(t=40,b=20))
            st.plotly_chart(fig3, use_container_width=True, config=PCFG)

        section_header("Target Variable Distribution (Q25)")
        tc = df["Q25_app_adoption"].value_counts()
        fig4 = go.Figure(go.Bar(
            x=tc.index, y=tc.values,
            marker_color=["#4CAF50",HONEY,"#E53935"],
            text=[f"{v} ({v/len(df)*100:.1f}%)" for v in tc.values],
            textposition="outside",
        ))
        fig4.update_layout(**PLOTLY_LIGHT, height=280,
                            yaxis=dict(showgrid=False),
                            margin=dict(t=10,b=20))
        st.plotly_chart(fig4, use_container_width=True, config=PCFG)
        insight_box("The 48/37/15 class split is intentional and mirrors realistic Indian "
                    "consumer behaviour. Weighted metrics are used in all classification models.")

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.download_button("Download Raw Data", raw.to_csv(index=False),
                               "pawindia_raw.csv","text/csv")
        with col_d2:
            st.download_button("Download Cleaned Data", df.to_csv(index=False),
                               "pawindia_clean.csv","text/csv")
