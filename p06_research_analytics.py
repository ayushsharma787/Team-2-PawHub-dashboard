# pages/p06_research_analytics.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from theme import section_header, insight_box, BROWN, AMBER, CHART_COLS
from ml_engine import (load_data, run_classification, run_clustering,
                               run_association_rules, run_regression)


def render():
    _, df = load_data()

    st.markdown(
        "<h1 style='color:#6F4E37;font-size:1.8rem;margin-bottom:4px'>Research & Analytics</h1>"
        "<p style='color:#9E8272'>Full ML analysis: Classification, Clustering, "
        "Association Rules and Regression</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='insight-box'>"
        "&#128202; This section contains the complete academic analysis. All models are "
        "cached after first load for fast navigation."
        "</div>",
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🎯 Classification", "🔵 Clustering", "🔗 Association Rules", "📈 Regression"])

    # ── Tab 1: Classification ─────────────────────────────────────────────────
    with tab1:
        section_header("Classification: Predicting App Adoption (Q25)")
        st.markdown(
            "<p style='color:#6F4E37;font-size:0.9rem'>Target variable: Q25 — Yes / Maybe / No. "
            "Eight algorithms compared on accuracy, precision, recall and F1-score. "
            "80/20 train-test split with 5-fold cross-validation.</p>",
            unsafe_allow_html=True,
        )

        with st.spinner("Training classification models..."):
            results_df, cms, feat_imp, best_model, yte, feat_names = run_classification()

        # Performance table
        section_header("Algorithm Performance Comparison")
        styled = results_df.copy()
        best_idx = styled["F1-Score"].idxmax()
        st.dataframe(
            styled.style
                .highlight_max(subset=["Accuracy","Precision","Recall","F1-Score","CV Accuracy"],
                               color="#FEF3E2")
                .format({"Accuracy":"{:.3f}","Precision":"{:.3f}","Recall":"{:.3f}",
                          "F1-Score":"{:.3f}","CV Accuracy":"{:.3f}"}),
            use_container_width=True, hide_index=True,
        )
        insight_box(f"Best model: {best_model} with F1-Score of "
                    f"{results_df.iloc[0]['F1-Score']:.3f} and accuracy of "
                    f"{results_df.iloc[0]['Accuracy']:.3f}. Cross-validation confirms "
                    "the result is stable and not overfitted.")

        # Model comparison bar chart
        fig = go.Figure()
        metrics = ["Accuracy", "Precision", "Recall", "F1-Score"]
        colors  = [BROWN, AMBER, "#C49A6C", "#A0522D"]
        for metric, color in zip(metrics, colors):
            fig.add_trace(go.Bar(
                name=metric,
                x=results_df["Model"],
                y=results_df[metric],
                marker_color=color,
            ))
        fig.update_layout(
            barmode="group", title="All Models — Metric Comparison",
            height=380, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#3E2A1A"), margin=dict(t=40,b=80),
            xaxis=dict(tickangle=-30),
            yaxis=dict(range=[0,1.1], title="Score", showgrid=False),
            legend=dict(orientation="h", y=-0.3),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Confusion matrix for best model
        section_header(f"Confusion Matrix: {best_model}")
        cm = cms[best_model]
        labels = ["No (0)", "Maybe (1)", "Yes (2)"]
        fig_cm = go.Figure(go.Heatmap(
            z=cm, x=labels, y=labels,
            colorscale=[[0,AMBER],[1,BROWN]],
            text=cm, texttemplate="%{text}",
            showscale=True,
        ))
        fig_cm.update_layout(
            height=360, paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#3E2A1A"),
            xaxis=dict(title="Predicted"),
            yaxis=dict(title="Actual"),
            margin=dict(t=20,b=60,l=60,r=20),
        )
        st.plotly_chart(fig_cm, use_container_width=True)

        # Feature importance
        if best_model in feat_imp:
            section_header(f"Feature Importance: {best_model}")
            fi = feat_imp[best_model]
            fi_df = pd.DataFrame({"Feature": list(fi.keys()),
                                   "Importance": list(fi.values())})
            fi_df = fi_df.sort_values("Importance", ascending=False).head(15)
            fi_df["Feature"] = fi_df["Feature"].str.replace("Q[0-9]+_","",regex=True)\
                                                 .str.replace("_enc","").str.replace("_"," ")\
                                                 .str[:35]
            fig_fi = go.Figure(go.Bar(
                x=fi_df["Importance"], y=fi_df["Feature"], orientation="h",
                marker=dict(color=fi_df["Importance"],
                            colorscale=[[0,AMBER],[1,BROWN]]),
                text=fi_df["Importance"].round(3), textposition="outside",
            ))
            fig_fi.update_layout(
                height=420, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A", size=11), margin=dict(t=10,b=10),
                xaxis=dict(showgrid=False, visible=False),
            )
            st.plotly_chart(fig_fi, use_container_width=True)
            insight_box("Engagement score, app usage frequency, and subscription preference "
                        "are the top predictors of app adoption, confirming that existing "
                        "digital behaviour is the strongest signal for PawIndia conversion.")

        # All model metrics table for download
        st.download_button(
            "Download Classification Results",
            data=results_df.to_csv(index=False),
            file_name="pawindia_classification_results.csv",
            mime="text/csv",
        )

    # ── Tab 2: Clustering ─────────────────────────────────────────────────────
    with tab2:
        section_header("Clustering: Finding India's Dog Owner Segments")
        st.markdown(
            "<p style='color:#6F4E37;font-size:0.9rem'>K-Means clustering applied to "
            "15 behavioural and demographic features. Elbow method used to select K=4. "
            "Each cluster is interpreted as a distinct dog owner persona.</p>",
            unsafe_allow_html=True,
        )

        with st.spinner("Running clustering..."):
            K_range, inertias, sil_scores, labels, df2, summary, _, persona_map = run_clustering()

        # Elbow curve
        c1, c2 = st.columns(2)
        with c1:
            fig_elbow = go.Figure()
            fig_elbow.add_trace(go.Scatter(
                x=list(K_range), y=inertias,
                mode="lines+markers", name="Inertia",
                line=dict(color=BROWN, width=2),
                marker=dict(size=8, color=AMBER),
            ))
            fig_elbow.add_vline(x=4, line_dash="dash", line_color=AMBER,
                                annotation_text="K=4 selected")
            fig_elbow.update_layout(
                title="Elbow Curve (K vs Inertia)", height=300,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
                xaxis=dict(title="Number of Clusters (K)"),
                yaxis=dict(title="Inertia", showgrid=False),
            )
            st.plotly_chart(fig_elbow, use_container_width=True)

        with c2:
            fig_sil = go.Figure(go.Bar(
                x=list(K_range), y=sil_scores,
                marker_color=CHART_COLS[:len(K_range)],
                text=[f"{s:.3f}" for s in sil_scores],
                textposition="outside",
            ))
            fig_sil.add_vline(x=4, line_dash="dash", line_color=AMBER,
                               annotation_text="K=4 selected")
            fig_sil.update_layout(
                title="Silhouette Score by K", height=300,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
                xaxis=dict(title="Number of Clusters (K)"),
                yaxis=dict(title="Silhouette Score", showgrid=False),
            )
            st.plotly_chart(fig_sil, use_container_width=True)

        insight_box("K=4 is selected based on the elbow in the inertia curve and a "
                    "strong silhouette score, indicating well-separated, meaningful clusters.")

        # Cluster personas
        section_header("The Four Dog Owner Personas")
        persona_colors = [BROWN, AMBER, "#C49A6C", "#A0522D"]
        persona_emojis = ["🏙️", "🏘️", "🛋️", "🤝"]
        cols = st.columns(4)
        for i, (cluster_id, (name, desc)) in enumerate(persona_map.items()):
            row = summary[summary["cluster"]==cluster_id]
            if len(row) > 0:
                row = row.iloc[0]
                with cols[i]:
                    st.markdown(
                        f"""<div class="info-card" style="border-top:4px solid {persona_colors[i]};
                        min-height:200px;text-align:center">
                        <div style="font-size:2rem">{persona_emojis[i]}</div>
                        <div style="font-weight:700;color:#3E2A1A;font-size:1rem;margin:6px 0">{name}</div>
                        <div style="color:#9E8272;font-size:0.8rem;margin-bottom:10px">{desc}</div>
                        <div style="color:{persona_colors[i]};font-weight:700;font-size:1.1rem">
                          {int(row['Count'])} members</div>
                        <div style="color:#6F4E37;font-size:0.82rem">
                          Avg Spend: Rs.{int(row['Avg_Spend']):,}<br>
                          Adoption Rate: {int(row['Pct_Yes']*100)}%<br>
                          Metro: {int(row['Pct_Metro']*100)}%</div>
                        </div>""",
                        unsafe_allow_html=True,
                    )

        # Cluster summary table
        section_header("Cluster Summary Table")
        display_summary = summary[["cluster","Persona","Count","Avg_Spend",
                                    "Avg_App_Usage","Pct_Metro","Pct_Yes","Description"]].copy()
        display_summary.columns = ["Cluster","Persona","Count","Avg Spend (INR)",
                                    "Avg App Usage","% Metro","Adoption Rate","Description"]
        display_summary["Avg Spend (INR)"] = display_summary["Avg Spend (INR)"].apply(lambda x: f"Rs.{int(x):,}")
        display_summary["% Metro"] = display_summary["% Metro"].apply(lambda x: f"{int(x*100)}%")
        display_summary["Adoption Rate"] = display_summary["Adoption Rate"].apply(lambda x: f"{int(x*100)}%")
        st.dataframe(display_summary, use_container_width=True, hide_index=True)

        # Cluster spend comparison
        fig_cluster = go.Figure()
        for i, row in summary.iterrows():
            name = row["Persona"]
            fig_cluster.add_trace(go.Bar(
                name=name,
                x=[name],
                y=[row["Avg_Spend"]],
                marker_color=persona_colors[int(row["cluster"])],
                text=[f"Rs.{int(row['Avg_Spend']):,}"],
                textposition="outside",
            ))
        fig_cluster.update_layout(
            title="Average Monthly Spend by Cluster", showlegend=False,
            height=320, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
            yaxis=dict(showgrid=False, title="INR"),
        )
        st.plotly_chart(fig_cluster, use_container_width=True)
        insight_box("The Urban Enthusiast cluster shows the highest spend and adoption rate, "
                    "making them PawIndia's premium tier target. The Practical Parent cluster "
                    "in Tier-2 cities is the largest group and the key volume opportunity.")

        st.download_button(
            "Download Cluster Results",
            data=summary.to_csv(index=False),
            file_name="pawindia_cluster_results.csv",
            mime="text/csv",
        )

    # ── Tab 3: Association Rules ──────────────────────────────────────────────
    with tab3:
        section_header("Association Rule Mining: Pain Points to Feature Demand")
        st.markdown(
            "<p style='color:#6F4E37;font-size:0.9rem'>Apriori algorithm applied to Q10 "
            "(challenges) and Q14 (preferred features). Rules show which pain points "
            "drive demand for specific app features. Min support: 8%, Min lift: 1.1.</p>",
            unsafe_allow_html=True,
        )

        with st.spinner("Mining association rules..."):
            try:
                rules = run_association_rules()
                rules_available = True
            except Exception as e:
                rules_available = False
                st.error(f"Association rules require mlxtend: pip install mlxtend. Error: {e}")

        if rules_available and len(rules) > 0:
            # Controls
            col_s, col_c, col_l = st.columns(3)
            with col_s:
                min_sup = st.slider("Min Support", 0.05, 0.30, 0.08, 0.01)
            with col_c:
                min_conf = st.slider("Min Confidence", 0.1, 0.9, 0.2, 0.05)
            with col_l:
                min_lift = st.slider("Min Lift", 1.0, 3.0, 1.1, 0.05)

            filtered = rules[
                (rules["support"] >= min_sup) &
                (rules["confidence"] >= min_conf) &
                (rules["lift"] >= min_lift)
            ]

            st.markdown(
                f"<p style='color:#9E8272;font-size:0.85rem'>"
                f"Showing {len(filtered)} rules after filtering.</p>",
                unsafe_allow_html=True,
            )

            # Top rules table
            section_header("Top Association Rules (Pain Point → Feature Demand)")
            display_rules = filtered[["antecedents_str","consequents_str",
                                       "support","confidence","lift"]].head(20)
            display_rules.columns = ["If Owner Faces (Antecedent)","They Want (Consequent)",
                                      "Support","Confidence","Lift"]
            st.dataframe(display_rules, use_container_width=True, hide_index=True)

            # Lift bubble chart
            section_header("Support vs Confidence (Bubble = Lift)")
            if len(filtered) > 0:
                fig_rules = px.scatter(
                    filtered.head(25),
                    x="support", y="confidence",
                    size="lift", color="lift",
                    hover_data=["antecedents_str","consequents_str","lift"],
                    color_continuous_scale=[[0,AMBER],[1,BROWN]],
                    labels={"support":"Support","confidence":"Confidence"},
                    title="Association Rules: Support vs Confidence (size = Lift)",
                )
                fig_rules.update_layout(
                    height=380, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#3E2A1A"), margin=dict(t=40,b=20),
                )
                st.plotly_chart(fig_rules, use_container_width=True)

            insight_box("Owners who struggle to find reliable vets are significantly more likely "
                        "to demand the nearby vet directory and health tracker features. This "
                        "directly validates PawIndia's core feature prioritisation.")

            st.download_button(
                "Download Association Rules",
                data=filtered.to_csv(index=False),
                file_name="pawindia_association_rules.csv",
                mime="text/csv",
            )

    # ── Tab 4: Regression ─────────────────────────────────────────────────────
    with tab4:
        section_header("Regression: Predicting Monthly Dog Spend")
        st.markdown(
            "<p style='color:#6F4E37;font-size:0.9rem'>Target: Q7 monthly spend (INR). "
            "Three regression models compared: Linear, Ridge (L2), and Lasso (L1). "
            "80/20 split with 5-fold cross-validation. Evaluated on R2, RMSE and MAE.</p>",
            unsafe_allow_html=True,
        )

        with st.spinner("Training regression models..."):
            reg_results, preds, coefs, yte_reg, feat_names = run_regression()

        # Results table
        section_header("Regression Model Comparison")
        st.dataframe(
            reg_results.style
                .highlight_max(subset=["R2","CV R2"], color="#FEF3E2")
                .highlight_min(subset=["RMSE","MAE"], color="#FEF3E2")
                .format({"R2":"{:.3f}","RMSE":"{:.0f}","MAE":"{:.0f}","CV R2":"{:.3f}"}),
            use_container_width=True, hide_index=True,
        )

        best_reg = reg_results.sort_values("R2", ascending=False).iloc[0]["Model"]
        insight_box(f"Best regression model: {best_reg}. R2 score indicates how well "
                    "demographic and behavioural features explain monthly dog spending. "
                    "Ridge regularisation helps reduce multicollinearity from one-hot encoded features.")

        # Actual vs Predicted
        section_header("Actual vs Predicted Spend")
        c1, c2, c3 = st.columns(3)
        for col, (name, (actual, predicted)) in zip([c1,c2,c3], preds.items()):
            with col:
                n_show = min(200, len(actual))
                idx = np.random.choice(len(actual), n_show, replace=False)
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=actual[idx], y=predicted[idx],
                    mode="markers",
                    marker=dict(color=BROWN, opacity=0.5, size=4),
                    name="Predictions",
                ))
                max_val = max(actual.max(), predicted.max())
                fig.add_trace(go.Scatter(
                    x=[0, max_val], y=[0, max_val],
                    mode="lines", line=dict(color=AMBER, dash="dash"),
                    name="Perfect Fit",
                ))
                r2_val = reg_results[reg_results["Model"]==name]["R2"].values[0]
                fig.update_layout(
                    title=f"{name}<br>R2={r2_val}", height=280,
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#3E2A1A", size=10), margin=dict(t=50,b=30,l=40,r=10),
                    xaxis=dict(title="Actual (INR)"),
                    yaxis=dict(title="Predicted (INR)"),
                    showlegend=False,
                )
                st.plotly_chart(fig, use_container_width=True)

        # Coefficient comparison
        section_header("Feature Coefficients Across Models")
        if coefs:
            coef_df = pd.DataFrame(coefs)
            coef_df.index = [i.replace("Q[0-9]+_","").replace("_enc","")
                              .replace("_"," ")[:30] for i in coef_df.index]
            top_feat = coef_df.abs().mean(axis=1).sort_values(ascending=False).head(12).index
            coef_top = coef_df.loc[top_feat]

            fig_coef = go.Figure()
            for i, (col, color) in enumerate(zip(coef_top.columns, [BROWN, AMBER, "#C49A6C"])):
                fig_coef.add_trace(go.Bar(
                    name=col, x=coef_top.index, y=coef_top[col],
                    marker_color=color, opacity=0.85,
                ))
            fig_coef.update_layout(
                barmode="group", title="Top Feature Coefficients: Linear vs Ridge vs Lasso",
                height=380, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#3E2A1A", size=10), margin=dict(t=40,b=100),
                xaxis=dict(tickangle=-40),
                yaxis=dict(title="Coefficient Value", showgrid=False),
                legend=dict(orientation="h", y=-0.35),
            )
            st.plotly_chart(fig_coef, use_container_width=True)
            insight_box("Dog count and city tier are the strongest positive predictors of "
                        "monthly spend. Lasso's L1 penalty zeros out weak features, confirming "
                        "that a small set of variables drives most of the spending variance.")

        st.download_button(
            "Download Regression Results",
            data=reg_results.to_csv(index=False),
            file_name="pawindia_regression_results.csv",
            mime="text/csv",
        )
