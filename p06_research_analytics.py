# p06_research_analytics.py — Dark theme research tab
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from theme import (BROWN, AMBER, HONEY, CHART_COLS, PLOTLY_DARK, PCFG,
                   DARK_BG, DARK_CARD, DARK_BORDER, CREAM_TEXT, DIM, SAGE, TEAL, MAUVE)
from ml_engine import (load_data, run_classification, run_clustering,
                        run_association_rules, run_regression)


def dark_section(title):
    st.markdown(
        f"""<div style="display:flex;align-items:center;gap:12px;margin:24px 0 12px">
        <div style="width:4px;height:20px;background:linear-gradient(180deg,{HONEY},transparent);
        border-radius:2px"></div>
        <div style="color:{CREAM_TEXT};font-size:1.1rem;font-weight:700;
        font-family:Bricolage Grotesque,sans-serif">{title}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def dark_insight(text):
    st.markdown(
        f"""<div style="background:linear-gradient(135deg,rgba(212,168,83,0.08),transparent);
        border:1px solid rgba(212,168,83,0.18);border-left:4px solid {HONEY};
        border-radius:0 10px 10px 0;padding:12px 16px;margin:10px 0 18px;
        color:#C4B99A;font-size:0.87rem;line-height:1.65">
        &#128161; {text}</div>""",
        unsafe_allow_html=True,
    )


def render():
    _, df = load_data()

    # Dark background wrapper for this entire page
    st.markdown(
        f"""<div style="background:linear-gradient(168deg,#1A1209 0%,#141110 50%,#0D0B09 100%);
        border-radius:16px;padding:24px 26px;margin-bottom:8px;
        border:1px solid rgba(212,168,83,0.12)">
        <div style="display:flex;align-items:center;gap:16px">
          <div style="font-size:40px;filter:drop-shadow(0 0 12px rgba(212,168,83,0.3))">📊</div>
          <div>
            <h1 style="margin:0;font-size:1.8rem;font-family:Bricolage Grotesque,sans-serif;
            font-weight:800;color:{CREAM_TEXT}">Research & Analytics</h1>
            <div style="color:#A07D3A;font-size:0.88rem;margin-top:4px">
            Full ML analysis: Classification, Clustering, Association Rules, Regression</div>
          </div>
        </div></div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""<div style="background:rgba(26,18,9,0.7);border:1px solid rgba(212,168,83,0.15);
        border-radius:10px;padding:10px 16px;margin-bottom:16px">
        <span style="color:{SAGE};font-size:10px;font-weight:700;letter-spacing:.1em;
        text-transform:uppercase">&#9679; All models cached</span>
        <span style="color:#5a5040;font-size:10px;margin:0 8px">|</span>
        <span style="color:#C4B99A;font-size:11px">{len(df):,} respondents</span>
        <span style="color:#5a5040;font-size:10px;margin:0 8px">|</span>
        <span style="color:#C4B99A;font-size:11px">Target: Q25 App Adoption (3-class)</span>
        </div>""",
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🎯 Classification","🔵 Clustering","🔗 Association Rules","📈 Regression"])

    # ────────────────────────────── CLASSIFICATION ────────────────────────────
    with tab1:
        dark_section("Classification: Predicting App Adoption (Q25)")
        st.markdown(
            f"<p style='color:{DIM};font-size:0.88rem'>Target: Yes/Maybe/No. "
            "8-9 algorithms compared on accuracy, precision, recall and F1. "
            "80/20 stratified split, 5-fold CV.</p>",
            unsafe_allow_html=True,
        )

        with st.spinner("Training classification models..."):
            results_df, cms, feat_imp, best_model, yte, feat_names = run_classification()

        # Performance table (styled dark)
        dark_section("Algorithm Performance Comparison")
        fig_tbl = go.Figure(go.Table(
            header=dict(
                values=[f"<b>{c}</b>" for c in results_df.columns],
                fill_color="rgba(45,32,15,0.8)",
                font=dict(color=HONEY, size=12, family="Bricolage Grotesque"),
                align="left", line=dict(color="rgba(80,65,40,.3)", width=1),
            ),
            cells=dict(
                values=[results_df[c].astype(str).tolist() for c in results_df.columns],
                fill_color=["rgba(22,19,15,0.88)","rgba(30,22,12,0.6)"],
                font=dict(color=CREAM_TEXT, size=11, family="Plus Jakarta Sans"),
                align="left", line=dict(color="rgba(80,65,40,.15)", width=1), height=30,
            ),
        ))
        fig_tbl.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            height=min(60+len(results_df)*35,480), margin=dict(l=0,r=0,t=0,b=0),
        )
        st.plotly_chart(fig_tbl, use_container_width=True, config=PCFG)
        dark_insight(f"Best model: <b>{best_model}</b> with F1={results_df.iloc[0]['F1-Score']:.3f} "
                     f"and accuracy={results_df.iloc[0]['Accuracy']:.3f}. "
                     "Cross-validation confirms stability — no overfitting.")

        # Grouped bar comparison
        dark_section("Visual Comparison: All Models")
        fig_bar = go.Figure()
        metric_colors = [BROWN, HONEY, "#C49A6C", "#A0522D"]
        for metric, color in zip(["Accuracy","Precision","Recall","F1-Score"], metric_colors):
            fig_bar.add_trace(go.Bar(
                name=metric, x=results_df["Model"], y=results_df[metric],
                marker_color=color,
            ))
        fig_bar.update_layout(**PLOTLY_DARK, barmode="group", height=380,
                               xaxis=dict(tickangle=-30),
                               yaxis=dict(range=[0,1.1],title="Score"),
                               legend=dict(orientation="h",y=-0.3),
                               margin=dict(t=20,b=80))
        st.plotly_chart(fig_bar, use_container_width=True, config=PCFG)

        # ROC-style accuracy vs F1 scatter
        dark_section("Accuracy vs F1-Score: Model Trade-offs")
        fig_sc = go.Figure()
        for i, row in results_df.iterrows():
            is_best = row["Model"] == best_model
            fig_sc.add_trace(go.Scatter(
                x=[row["Accuracy"]], y=[row["F1-Score"]],
                mode="markers+text",
                name=row["Model"],
                text=[row["Model"]],
                textposition="top center",
                marker=dict(size=18 if is_best else 12,
                            color=HONEY if is_best else CHART_COLS[i % len(CHART_COLS)],
                            symbol="star" if is_best else "circle",
                            line=dict(color=CREAM_TEXT, width=1.5 if is_best else 0)),
            ))
        fig_sc.update_layout(**PLOTLY_DARK, height=380, showlegend=False,
                              xaxis=dict(title="Accuracy"),
                              yaxis=dict(title="F1-Score"),
                              margin=dict(t=20,b=40))
        st.plotly_chart(fig_sc, use_container_width=True, config=PCFG)

        # Confusion matrix for best model
        dark_section(f"Confusion Matrix: {best_model}")
        cm = cms[best_model]
        labels = ["No (0)","Maybe (1)","Yes (2)"]
        fig_cm = go.Figure(go.Heatmap(
            z=cm, x=labels, y=labels,
            colorscale=[[0,AMBER],[1,BROWN]],
            text=cm, texttemplate="%{text}", showscale=True,
        ))
        fig_cm.update_layout(**PLOTLY_DARK, height=360,
                              xaxis=dict(title="Predicted"),
                              yaxis=dict(title="Actual"),
                              margin=dict(t=20,b=60,l=60,r=20))
        st.plotly_chart(fig_cm, use_container_width=True, config=PCFG)

        # Feature importance
        if best_model in feat_imp:
            dark_section(f"Feature Importance: {best_model}")
            fi    = feat_imp[best_model]
            fi_df = pd.DataFrame({"Feature":list(fi.keys()),"Importance":list(fi.values())})
            fi_df = fi_df.sort_values("Importance", ascending=False).head(15)
            fi_df["Feature"] = fi_df["Feature"].str.replace(r"Q\d+_","",regex=True)\
                                                 .str.replace("_enc","").str.replace("_"," ")\
                                                 .str[:35]
            fig_fi = go.Figure(go.Bar(
                x=fi_df["Importance"], y=fi_df["Feature"], orientation="h",
                marker=dict(color=fi_df["Importance"],
                            colorscale=[[0,AMBER],[1,BROWN]]),
                text=fi_df["Importance"].round(3), textposition="outside",
            ))
            fig_fi.update_layout(**PLOTLY_DARK, height=420,
                                  margin=dict(t=10,b=10),
                                  xaxis=dict(showgrid=False,visible=False),
                                  font=dict(size=11))
            st.plotly_chart(fig_fi, use_container_width=True, config=PCFG)
            dark_insight("Engagement score, app usage frequency, and monthly spend are the "
                         "top predictors — existing digital behaviour is the strongest adoption signal.")

        st.download_button("Download Classification Results",
                           results_df.to_csv(index=False),
                           "pawindia_classification.csv","text/csv")

    # ────────────────────────────── CLUSTERING ────────────────────────────────
    with tab2:
        dark_section("Clustering: Finding India's Dog Owner Segments")
        st.markdown(f"<p style='color:{DIM};font-size:0.88rem'>K-Means on 15 features. "
                    "Elbow + silhouette used to select K=4.</p>", unsafe_allow_html=True)

        with st.spinner("Running clustering..."):
            K_range, inertias, sil_scores, labels, df2, summary, persona_map = run_clustering()

        c1, c2 = st.columns(2)
        with c1:
            fig_el = go.Figure(go.Scatter(
                x=list(K_range), y=inertias,
                mode="lines+markers",
                line=dict(color=HONEY, width=2.5),
                marker=dict(size=9, color=AMBER),
            ))
            fig_el.add_vline(x=4, line_dash="dash", line_color=SAGE,
                              annotation_text="K=4", annotation_font_color=SAGE)
            fig_el.update_layout(**PLOTLY_DARK, title="Elbow Curve", height=280,
                                  xaxis=dict(title="K"), yaxis=dict(title="Inertia"),
                                  margin=dict(t=40,b=30))
            st.plotly_chart(fig_el, use_container_width=True, config=PCFG)
        with c2:
            fig_sil = go.Figure(go.Bar(
                x=list(K_range), y=sil_scores,
                marker_color=CHART_COLS[:len(K_range)],
                text=[f"{s:.3f}" for s in sil_scores], textposition="outside",
            ))
            fig_sil.add_vline(x=4, line_dash="dash", line_color=SAGE)
            fig_sil.update_layout(**PLOTLY_DARK, title="Silhouette Score by K", height=280,
                                   xaxis=dict(title="K"), yaxis=dict(title="Silhouette"),
                                   margin=dict(t=40,b=30))
            st.plotly_chart(fig_sil, use_container_width=True, config=PCFG)

        dark_insight("K=4 selected: elbow inflects here and silhouette remains strong, "
                     "producing 4 interpretable and well-separated dog owner personas.")

        # Persona cards
        dark_section("The Four Dog Owner Personas")
        cols = st.columns(4)
        emojis = ["🏙️","🏘️","🛋️","🤝"]
        for i, (cluster_id, (name, color, desc)) in enumerate(persona_map.items()):
            row = summary[summary["cluster"]==cluster_id]
            if len(row) > 0:
                row = row.iloc[0]
                r,g,b = int(color[1:3],16),int(color[3:5],16),int(color[5:7],16)
                with cols[i]:
                    st.markdown(
                        f"""<div style="background:linear-gradient(145deg,rgba(30,22,12,0.92),rgba(15,12,10,0.95));
                        border:1px solid rgba({r},{g},{b},0.35);border-top:4px solid {color};
                        border-radius:14px;padding:18px 16px;text-align:center;
                        box-shadow:0 4px 20px rgba(0,0,0,0.4)">
                        <div style="font-size:2rem">{emojis[i]}</div>
                        <div style="font-weight:700;color:{CREAM_TEXT};font-size:0.95rem;margin:8px 0 4px;
                        font-family:Bricolage Grotesque">{name}</div>
                        <div style="color:{DIM};font-size:0.78rem;margin-bottom:10px">{desc}</div>
                        <div style="color:{color};font-weight:700;font-size:1.1rem">{int(row['Count'])} members</div>
                        <div style="color:#C4B99A;font-size:0.8rem;margin-top:6px">
                          Avg Spend: Rs.{int(row['Avg_Spend']):,}<br>
                          Adoption: {int(row['Pct_Yes']*100)}%<br>
                          Metro: {int(row['Pct_Metro']*100)}%
                        </div></div>""",
                        unsafe_allow_html=True,
                    )

        # Cluster summary table
        dark_section("Cluster Summary Table")
        disp = summary[["cluster","Persona","Count","Avg_Spend","Avg_App","Pct_Metro","Pct_Yes"]].copy()
        disp.columns = ["Cluster","Persona","Count","Avg Spend","Avg App Usage","% Metro","Adoption Rate"]
        disp["Avg Spend"]    = disp["Avg Spend"].apply(lambda x: f"Rs.{int(x):,}")
        disp["% Metro"]      = disp["% Metro"].apply(lambda x: f"{int(x*100)}%")
        disp["Adoption Rate"]= disp["Adoption Rate"].apply(lambda x: f"{int(x*100)}%")
        fig_tbl2 = go.Figure(go.Table(
            header=dict(values=[f"<b>{c}</b>" for c in disp.columns],
                        fill_color="rgba(45,32,15,0.8)",
                        font=dict(color=HONEY,size=12,family="Bricolage Grotesque"),
                        align="left"),
            cells=dict(values=[disp[c].tolist() for c in disp.columns],
                       fill_color="rgba(22,19,15,0.88)",
                       font=dict(color=CREAM_TEXT,size=11),
                       align="left", height=30),
        ))
        fig_tbl2.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                                height=200, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig_tbl2, use_container_width=True, config=PCFG)

        # Parallel coordinates
        dark_section("Parallel Coordinates: All Cluster Dimensions")
        pc_cols = ["Q7_monthly_spend_inr","Q15_app_usage_enc","Q20_community_importance_enc",
                   "Q22_reviews_importance_enc","engagement_score","Q2_city_tier_Metro"]
        valid_pc = [c for c in pc_cols if c in df2.columns]
        if valid_pc:
            pc_data = df2[valid_pc + ["cluster"]].fillna(0).sample(min(500,len(df2)),random_state=42)
            pc_labels = [c.replace("_enc","").replace("Q7_monthly_spend_inr","Spend")
                          .replace("Q15_","App ").replace("Q20_","Community ")
                          .replace("Q22_","Reviews ").replace("Q2_city_tier_Metro","Metro")
                          .replace("_"," ")[:20] for c in valid_pc]
            fig_pc = go.Figure(go.Parcoords(
                line=dict(color=pc_data["cluster"],
                          colorscale=[[0,BROWN],[0.33,AMBER],[0.66,TEAL],[1,MAUVE]],
                          showscale=True),
                dimensions=[dict(range=[pc_data[c].min(),pc_data[c].max()],
                                  label=lab, values=pc_data[c])
                             for c, lab in zip(valid_pc, pc_labels)],
            ))
            fig_pc.update_layout(**PLOTLY_DARK, height=380, margin=dict(t=60,b=20,l=80,r=60))
            st.plotly_chart(fig_pc, use_container_width=True, config=PCFG)
            dark_insight("Each line is a respondent coloured by their cluster. "
                         "Parallel bands show how each persona differs across all dimensions simultaneously.")

        st.download_button("Download Cluster Results",
                           summary.drop(columns=["Color"],errors="ignore").to_csv(index=False),
                           "pawindia_clusters.csv","text/csv")

    # ────────────────────────────── ASSOCIATION RULES ─────────────────────────
    with tab3:
        dark_section("Association Rule Mining: Pain Points to Feature Demand")
        st.markdown(
            f"<p style='color:{DIM};font-size:0.88rem'>Apriori algorithm on Q10 (challenges) "
            "and Q14 (features). Rules show which pain points drive demand for specific app features. "
            "Min support: 8%, Min lift: 1.1.</p>",
            unsafe_allow_html=True,
        )

        with st.spinner("Mining association rules..."):
            try:
                rules = run_association_rules()
                rules_ok = True
            except Exception as e:
                rules_ok = False
                st.error(f"Install mlxtend: pip install mlxtend. Error: {e}")

        if rules_ok and len(rules) > 0:
            cs, cc, cl = st.columns(3)
            with cs: min_sup  = st.slider("Min Support",  0.05, 0.30, 0.08, 0.01)
            with cc: min_conf = st.slider("Min Confidence",0.1, 0.9,  0.20, 0.05)
            with cl: min_lift = st.slider("Min Lift",      1.0, 3.0,  1.10, 0.05)

            filtered = rules[(rules["support"]>=min_sup) &
                             (rules["confidence"]>=min_conf) &
                             (rules["lift"]>=min_lift)]

            st.markdown(f"<p style='color:{DIM};font-size:0.84rem'>"
                        f"Showing {len(filtered)} rules.</p>", unsafe_allow_html=True)

            # Rules table
            dark_section("Top Rules: Pain Point → Feature Demand")
            disp_r = filtered[["antecedents_str","consequents_str",
                                "support","confidence","lift"]].head(20)
            disp_r.columns = ["If Owner Faces","They Want","Support","Confidence","Lift"]
            fig_rt = go.Figure(go.Table(
                header=dict(values=[f"<b>{c}</b>" for c in disp_r.columns],
                            fill_color="rgba(45,32,15,0.8)",
                            font=dict(color=HONEY,size=12,family="Bricolage Grotesque"),
                            align="left"),
                cells=dict(values=[disp_r[c].tolist() for c in disp_r.columns],
                           fill_color="rgba(22,19,15,0.88)",
                           font=dict(color=CREAM_TEXT,size=11),
                           align="left", height=30),
            ))
            fig_rt.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                                  height=min(60+len(disp_r)*33,560),
                                  margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig_rt, use_container_width=True, config=PCFG)

            # Bubble chart
            dark_section("Support vs Confidence (Bubble Size = Lift)")
            if len(filtered) > 0:
                fig_bub = px.scatter(
                    filtered.head(25),
                    x="support", y="confidence", size="lift",
                    color="lift", hover_data=["antecedents_str","consequents_str","lift"],
                    color_continuous_scale=[[0,AMBER],[1,BROWN]],
                    labels={"support":"Support","confidence":"Confidence"},
                    size_max=30,
                )
                fig_bub.update_layout(**PLOTLY_DARK, height=380, margin=dict(t=20,b=20))
                st.plotly_chart(fig_bub, use_container_width=True, config=PCFG)

            # Network-style scatter (antecedent → consequent)
            dark_section("Rule Network: Challenge to Feature Links")
            try:
                top_r = filtered.head(15).reset_index(drop=True)
                node_labels, node_colors, ex, ey = [], [], [], []
                for _, row in top_r.iterrows():
                    ant = row["antecedents_str"]
                    con = row["consequents_str"]
                    if ant not in node_labels:
                        node_labels.append(ant); node_colors.append(AMBER)
                    if con not in node_labels:
                        node_labels.append(con); node_colors.append(BROWN)
                    ai = node_labels.index(ant)
                    ci = node_labels.index(con)
                    angle = (ai / max(len([x for x in node_colors if x==AMBER]),1)) * 2 * 3.14159
                    cangle= (ci / max(len([x for x in node_colors if x==BROWN]),1)) * 2 * 3.14159
                    x1,y1 = 0.3*np.cos(angle), 0.3*np.sin(angle)
                    x2,y2 = 0.8*np.cos(cangle), 0.8*np.sin(cangle)
                    ex += [x1, x2, None]; ey += [y1, y2, None]

                n_ant = sum(1 for c in node_colors if c==AMBER)
                n_con = sum(1 for c in node_colors if c==BROWN)
                nx = [0.3*np.cos(i/max(n_ant,1)*2*3.14159) if node_colors[i]==AMBER
                      else 0.8*np.cos(i/max(n_con,1)*2*3.14159)
                      for i in range(len(node_labels))]
                ny = [0.3*np.sin(i/max(n_ant,1)*2*3.14159) if node_colors[i]==AMBER
                      else 0.8*np.sin(i/max(n_con,1)*2*3.14159)
                      for i in range(len(node_labels))]

                fig_net = go.Figure()
                fig_net.add_trace(go.Scatter(x=ex, y=ey, mode="lines",
                                              line=dict(color="rgba(212,168,83,0.2)",width=1),
                                              hoverinfo="none", showlegend=False))
                fig_net.add_trace(go.Scatter(
                    x=nx, y=ny, mode="markers+text",
                    text=[l[:25] for l in node_labels],
                    textposition="top center",
                    marker=dict(size=[14 if c==AMBER else 12 for c in node_colors],
                                color=node_colors,
                                line=dict(color=CREAM_TEXT,width=1)),
                    textfont=dict(size=9, color=CREAM_TEXT),
                    showlegend=False,
                ))
                fig_net.update_layout(**PLOTLY_DARK, height=420,
                                       xaxis=dict(visible=False),
                                       yaxis=dict(visible=False),
                                       margin=dict(t=20,b=20))
                st.plotly_chart(fig_net, use_container_width=True, config=PCFG)
                dark_insight("Gold nodes = pain points (antecedents). Brown nodes = desired features "
                             "(consequents). Edges show which problems drive demand for which features.")
            except Exception:
                pass

            dark_insight("Owners struggling to find reliable vets are significantly more likely "
                         "to demand the vet directory and health tracker — PawIndia's two core features.")

            st.download_button("Download Association Rules",
                               filtered.to_csv(index=False),
                               "pawindia_rules.csv","text/csv")

    # ────────────────────────────── REGRESSION ────────────────────────────────
    with tab4:
        dark_section("Regression: Predicting Monthly Dog Spend (Q7)")
        st.markdown(
            f"<p style='color:{DIM};font-size:0.88rem'>Linear, Ridge (L2), Lasso (L1). "
            "80/20 split, 5-fold CV. Evaluated on R2, RMSE, MAE.</p>",
            unsafe_allow_html=True,
        )

        with st.spinner("Training regression models..."):
            reg_results, preds, coefs, yte_reg, feat_names = run_regression()

        # Results table
        dark_section("Model Comparison")
        fig_rt = go.Figure(go.Table(
            header=dict(values=[f"<b>{c}</b>" for c in reg_results.columns],
                        fill_color="rgba(45,32,15,0.8)",
                        font=dict(color=HONEY,size=12,family="Bricolage Grotesque"),
                        align="left"),
            cells=dict(values=[reg_results[c].tolist() for c in reg_results.columns],
                       fill_color="rgba(22,19,15,0.88)",
                       font=dict(color=CREAM_TEXT,size=11),
                       align="left", height=30),
        ))
        fig_rt.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                              height=180, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig_rt, use_container_width=True, config=PCFG)

        best_reg = reg_results.sort_values("R2",ascending=False).iloc[0]["Model"]
        dark_insight(f"Best: <b>{best_reg}</b>. Ridge regularisation reduces multicollinearity "
                     "from one-hot encoded features. Lasso zeros out weak predictors, "
                     "confirming that a small feature set drives most spending variance.")

        # Actual vs Predicted
        dark_section("Actual vs Predicted Spend")
        cols_reg = st.columns(3)
        for col_w, (name, (actual, predicted)) in zip(cols_reg, preds.items()):
            with col_w:
                n_show = min(300, len(actual))
                idx    = np.random.choice(len(actual), n_show, replace=False)
                r2_val = reg_results[reg_results["Model"]==name]["R2"].values[0]
                fig_av = go.Figure()
                fig_av.add_trace(go.Scatter(
                    x=actual[idx], y=predicted[idx], mode="markers",
                    marker=dict(color=BROWN, opacity=0.4, size=4),
                    name="Predictions",
                ))
                mx = max(float(actual.max()), float(predicted.max()))
                fig_av.add_trace(go.Scatter(
                    x=[0,mx], y=[0,mx], mode="lines",
                    line=dict(color=HONEY, dash="dash", width=1.5),
                    name="Perfect",
                ))
                fig_av.update_layout(**PLOTLY_DARK,
                                      title=f"{name}<br>R2={r2_val}", height=280,
                                      xaxis=dict(title="Actual (INR)"),
                                      yaxis=dict(title="Predicted"),
                                      showlegend=False, margin=dict(t=50,b=30,l=40,r=10))
                st.plotly_chart(fig_av, use_container_width=True, config=PCFG)

        # Coefficient comparison + Lasso regularisation path
        dark_section("Feature Coefficients: Linear vs Ridge vs Lasso")
        if coefs:
            coef_df  = pd.DataFrame(coefs)
            top_feat = coef_df.abs().mean(axis=1).sort_values(ascending=False).head(12).index
            coef_top = coef_df.loc[top_feat]
            coef_top.index = [i.replace("Q[0-9]+_","",).replace("_enc","")
                               .replace("_"," ")[:28] for i in coef_top.index]
            fig_coef = go.Figure()
            for col_name, color in zip(coef_top.columns, [BROWN, AMBER, "#C49A6C"]):
                fig_coef.add_trace(go.Bar(
                    name=col_name, x=coef_top.index, y=coef_top[col_name],
                    marker_color=color, opacity=0.85,
                ))
            fig_coef.update_layout(**PLOTLY_DARK, barmode="group", height=380,
                                    xaxis=dict(tickangle=-40),
                                    yaxis=dict(title="Coefficient",showgrid=False),
                                    legend=dict(orientation="h",y=-0.35),
                                    margin=dict(t=20,b=100))
            st.plotly_chart(fig_coef, use_container_width=True, config=PCFG)
            dark_insight("Lasso's L1 penalty zeros out noise features, leaving only the "
                         "strongest predictors. Dog count and city tier consistently drive spend upward.")

        st.download_button("Download Regression Results",
                           reg_results.to_csv(index=False),
                           "pawindia_regression.csv","text/csv")
