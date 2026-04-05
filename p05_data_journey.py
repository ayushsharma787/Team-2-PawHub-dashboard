# pages/p05_data_journey.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from theme import section_header, insight_box, BROWN, AMBER, CHART_COLS
from ml_engine import load_data


def render():
    raw, df = load_data()

    st.markdown(
        "<h1 style='color:#6F4E37;font-size:1.8rem;margin-bottom:4px'>Data Journey</h1>"
        "<p style='color:#9E8272'>How we generated 2,000 realistic survey responses "
        "and prepared them for analysis</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='border-color:#E8D5C4'>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(
        ["🧪 Synthetic Generation", "🧹 Data Cleaning", "📊 Before vs After"])

    # ── Tab 1: Synthetic Generation ───────────────────────────────────────────
    with tab1:
        section_header("Why Synthetic Data?")
        st.markdown(
            """<div class="info-card">
            <p style="color:#3E2A1A;line-height:1.8;font-size:0.95rem">
            Since PawIndia is a new product with no existing user base, we generated a synthetic
            dataset of 2,000 respondents that mimics the realistic behaviour of dog owners across
            India. The data was designed to reflect known market trends, urban-rural divides in
            pet culture, and the digital behaviour of Indian millennials. Critically, real-world
            noise and inconsistencies were deliberately injected so the dataset behaves like a
            genuine survey rather than a clean simulation.
            </p></div>""",
            unsafe_allow_html=True,
        )

        section_header("How Distributions Were Designed")
        steps = [
            ("Age Skew", "35% of respondents are aged 25-34, reflecting India's millennial dog ownership boom. Under-18 and 60+ are intentionally underrepresented to match realistic survey participation patterns."),
            ("City Tier Bias", "45% Metro, 30% Tier-2, 18% Tier-3, 7% Rural. This mirrors India's pet care market concentration where metro cities drive the majority of organised pet spending."),
            ("Dog Ownership", "55% own 1 dog, 22% own 2, 11% own 3+, and 12% are non-owners who are considering adoption. Non-owners were included because they are a key future customer segment."),
            ("Monthly Spend", "Spend was generated using a triangular distribution anchored to city tier and dog count. Metro city owners receive a 1.3x multiplier. The result is a right-skewed distribution matching real consumer spending patterns."),
            ("App Adoption Target (Q25)", "The target variable was not randomly assigned. It was computed from a scoring function based on city tier, age group, current app usage, and subscription preference, producing a realistic 48% Yes / 37% Maybe / 15% No split."),
            ("Multi-Select Questions", "Q10 (challenges) and Q14 (features) allowed up to 3 selections. Probabilities were weighted based on known Indian pet owner pain points from secondary research."),
        ]
        for i, (title, desc) in enumerate(steps):
            st.markdown(
                f"""<div class="step-box">
                <span style="background:#6F4E37;color:white;border-radius:50%;
                width:26px;height:26px;display:inline-flex;align-items:center;
                justify-content:center;font-weight:700;font-size:0.85rem;
                margin-right:10px">{i+1}</span>
                <strong style="color:#3E2A1A">{title}</strong>
                <p style="color:#6F4E37;margin:8px 0 0 36px;font-size:0.9rem">{desc}</p>
                </div>""",
                unsafe_allow_html=True,
            )

        section_header("Real-World Noise Injected")
        noise_items = [
            ("Duplicate Rows", "20 rows were duplicated to simulate respondents accidentally submitting twice, a common issue in online surveys."),
            ("Negative Spend Values", "~2% of Q7 numeric entries were made negative to simulate data entry errors."),
            ("Implausibly High Spend", "~2% of spend values were multiplied by 10 (extra zero typo), creating extreme outliers."),
            ("Missing Numeric Spend", "15% of respondents left the numeric spend field blank, relying only on the range selector."),
            ("Inconsistent Capitalisation", "~3% of city tier entries were lowercased to simulate form input inconsistency."),
            ("Whitespace Padding", "~4% of spend range entries had leading and trailing spaces."),
            ("Non-Owners Answering Dog Questions", "~40% of non-dog-owners still partially answered dog-specific questions, mimicking aspirational respondents."),
            ("Over-Selection on Multi-Select", "~5% of respondents selected more than the instructed maximum of 3 options for Q10 and Q14."),
            ("Blank Target Variable", "~2% of submissions had a blank Q25, simulating incomplete form submissions."),
        ]
        for title, desc in noise_items:
            st.markdown(
                f"""<div style="display:flex;align-items:flex-start;margin-bottom:12px">
                <span style="color:#D4860B;font-size:1.2rem;margin-right:10px">&#9888;</span>
                <div>
                <strong style="color:#3E2A1A">{title}</strong>
                <p style="color:#6F4E37;margin:2px 0;font-size:0.88rem">{desc}</p>
                </div></div>""",
                unsafe_allow_html=True,
            )

        # Raw data sample
        section_header("Raw Data Sample (First 10 Rows)")
        display_cols = ["respondent_id","Q1_age_group","Q2_city_tier","Q4_num_dogs",
                        "Q7_monthly_spend_inr","Q7_spend_range","Q9_online_purchase_freq",
                        "Q25_app_adoption"]
        valid_cols = [c for c in display_cols if c in raw.columns]
        st.dataframe(raw[valid_cols].head(10), use_container_width=True, hide_index=True)

        # Missing value chart (raw)
        section_header("Missing Values in Raw Dataset")
        missing = raw.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=False)
        if not missing.empty:
            fig = go.Figure(go.Bar(
                x=missing.values, y=missing.index, orientation="h",
                marker_color=AMBER, text=missing.values, textposition="outside",
            ))
            fig.update_layout(
                height=max(250, len(missing)*28),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A", size=11), margin=dict(t=10,b=10),
                xaxis=dict(showgrid=False, visible=False),
            )
            st.plotly_chart(fig, use_container_width=True)

    # ── Tab 2: Data Cleaning ──────────────────────────────────────────────────
    with tab2:
        section_header("Cleaning & Transformation Pipeline")
        cleaning_steps = [
            ("Step 1", "Remove Duplicates",
             f"Identified and removed duplicate rows based on all columns except respondent_id. "
             f"{len(raw)-len(raw.drop_duplicates(subset=[c for c in raw.columns if c!='respondent_id']))} "
             "duplicate rows removed."),
            ("Step 2", "Drop Incomplete Target Rows",
             "Rows where Q25 (app adoption likelihood) was blank were removed entirely, "
             "as the target variable is essential for all classification models."),
            ("Step 3", "Standardise Text Columns",
             "All text columns were stripped of leading/trailing whitespace and converted "
             "to title case to eliminate capitalisation inconsistencies."),
            ("Step 4", "Fix Numeric Spend (Q7)",
             "Negative values were nulled (data entry errors). Values above Rs.50,000/month "
             "were nulled as implausible outliers. Missing numeric values were imputed from "
             "range midpoints where available, then from group medians by dog count."),
            ("Step 5", "Impute Categorical Missing Values",
             "Remaining missing categorical values were filled using mode imputation within "
             "relevant groups (e.g. Q8 spend category imputed within dog-count groups). "
             "Standalone columns used global mode imputation."),
            ("Step 6", "Ordinal Encoding",
             "Ordered categorical variables (age group, ownership duration, satisfaction "
             "scores, app usage frequency, etc.) were encoded as integers preserving their "
             "natural order for use in regression and distance-based models."),
            ("Step 7", "One-Hot Encoding",
             "Nominal categorical variables (city tier, residence type, subscription preference, "
             "etc.) were one-hot encoded into binary columns. No drop_first to preserve "
             "interpretability for association rules."),
            ("Step 8", "Multi-Select Expansion",
             "Q5 (dog types), Q10 (challenges), and Q14 (features) were pipe-separated "
             "multi-select strings, expanded into individual binary flag columns for each option."),
            ("Step 9", "Feature Engineering",
             "Three derived features were created: spend_per_dog (Q7 divided by dog count), "
             "engagement_score (sum of app usage + online frequency + reviews importance "
             "encoded scores), and Q25_binary (Yes=1, Maybe/No=0 for binary classification)."),
            ("Step 10", "Final Validation",
             f"Final cleaned dataset: {len(df):,} rows x {len(df.columns)} columns. "
             "Zero missing values confirmed across all columns."),
        ]
        for step, title, desc in cleaning_steps:
            st.markdown(
                f"""<div class="step-box">
                <span style="color:#D4860B;font-size:0.75rem;font-weight:700;
                text-transform:uppercase;letter-spacing:1px">{step}</span>
                <strong style="color:#3E2A1A;display:block;margin:4px 0">{title}</strong>
                <p style="color:#6F4E37;margin:0;font-size:0.9rem;line-height:1.6">{desc}</p>
                </div>""",
                unsafe_allow_html=True,
            )

    # ── Tab 3: Before vs After ────────────────────────────────────────────────
    with tab3:
        section_header("Dataset Comparison: Raw vs Cleaned")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Raw Rows",      f"{len(raw):,}")
        col2.metric("Cleaned Rows",  f"{len(df):,}", delta=f"-{len(raw)-len(df)} removed")
        col3.metric("Raw Columns",   str(len(raw.columns)))
        col4.metric("Clean Columns", str(len(df.columns)), delta=f"+{len(df.columns)-len(raw.columns)} engineered")

        st.markdown("<br>", unsafe_allow_html=True)

        # Missing values comparison
        section_header("Missing Values: Before and After Cleaning")
        raw_miss   = raw.isnull().sum().sum()
        clean_miss = df.isnull().sum().sum()
        fig = go.Figure(go.Bar(
            x=["Raw Dataset", "Cleaned Dataset"],
            y=[raw_miss, clean_miss],
            marker_color=[AMBER, BROWN],
            text=[raw_miss, clean_miss],
            textposition="outside",
        ))
        fig.update_layout(
            height=280, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#3E2A1A"), margin=dict(t=10,b=20),
            yaxis=dict(showgrid=False, title="Total Missing Values"),
        )
        st.plotly_chart(fig, use_container_width=True)
        insight_box(f"Cleaning reduced total missing values from {raw_miss:,} to {clean_miss}. "
                    "The cleaned dataset is fully ready for all ML algorithms with no imputation "
                    "required at model training time.")

        # Spend distribution comparison
        section_header("Spend Distribution: Raw vs Cleaned")
        c1, c2 = st.columns(2)
        with c1:
            raw_spend = pd.to_numeric(raw["Q7_monthly_spend_inr"], errors="coerce").dropna()
            fig2 = go.Figure(go.Histogram(
                x=raw_spend, nbinsx=40, marker_color=AMBER, opacity=0.8))
            fig2.update_layout(
                title=f"Raw Spend (includes negatives & outliers)", height=260,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
                xaxis=dict(title="INR"), yaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig2, use_container_width=True)
        with c2:
            clean_spend = df["Q7_monthly_spend_inr"].dropna()
            fig3 = go.Figure(go.Histogram(
                x=clean_spend, nbinsx=40, marker_color=BROWN, opacity=0.8))
            fig3.update_layout(
                title="Cleaned Spend (outliers removed & imputed)", height=260,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
                xaxis=dict(title="INR"), yaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig3, use_container_width=True)

        # Target distribution
        section_header("Target Variable Distribution (Q25)")
        target_counts = df["Q25_app_adoption"].value_counts()
        fig4 = go.Figure(go.Bar(
            x=target_counts.index, y=target_counts.values,
            marker_color=[BROWN, AMBER, "#E8D5C4"],
            text=[f"{v} ({v/len(df)*100:.1f}%)" for v in target_counts.values],
            textposition="outside",
        ))
        fig4.update_layout(
            height=280, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#3E2A1A"), margin=dict(t=10,b=20),
            yaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig4, use_container_width=True)
        insight_box("The target variable has a realistic class imbalance (48% Yes, 37% Maybe, "
                    "15% No). This was intentional and reflects genuine market conditions. "
                    "Weighted metrics are used in classification evaluation to account for this.")

        st.download_button(
            "Download Raw Data",
            data=raw.to_csv(index=False),
            file_name="pawindia_raw_data.csv",
            mime="text/csv",
        )
        st.download_button(
            "Download Cleaned Data",
            data=df.to_csv(index=False),
            file_name="pawindia_cleaned_data.csv",
            mime="text/csv",
        )
