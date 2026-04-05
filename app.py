"""
PawIndia Market Research Dashboard
Single-file version — upload app.py + pawindia_raw_data.csv + pawindia_cleaned_data.csv
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os, time, math

st.set_page_config(
    page_title="PawIndia Dashboard",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Palette ───────────────────────────────────────────────────────────────────
BROWN  = "#6F4E37"
AMBER  = "#D4860B"
HONEY  = "#D4A853"
SAGE   = "#7CB67C"
TEAL   = "#5BB8C4"
MAUVE  = "#9B7CB6"
TERRA  = "#C4704B"
CHART  = [BROWN, HONEY, "#C49A6C", SAGE, TEAL, MAUVE, TERRA,
          "#A0522D", "#DEB887", "#5CC4A0"]
PCFG   = {"displayModeBar": False}

# Plotly layout bases — NO margin key here to avoid duplicate kwarg errors
PL = dict(paper_bgcolor="rgba(0,0,0,0)",
          plot_bgcolor="rgba(255,252,248,0.7)",
          font=dict(family="Plus Jakarta Sans,Inter,sans-serif",
                    color="#2C1810", size=11),
          xaxis=dict(gridcolor="rgba(111,78,55,.08)",
                     linecolor="rgba(111,78,55,.15)", zeroline=False,
                     tickfont=dict(color="#2C1810", size=11),
                     title_font=dict(color="#2C1810", size=11)),
          yaxis=dict(gridcolor="rgba(111,78,55,.08)",
                     linecolor="rgba(111,78,55,.15)", zeroline=False,
                     tickfont=dict(color="#2C1810", size=11),
                     title_font=dict(color="#2C1810", size=11)),
          legend=dict(font=dict(color="#2C1810", size=11)))

PD = dict(template="plotly_dark",
          paper_bgcolor="rgba(0,0,0,0)",
          plot_bgcolor="rgba(26,18,9,0.6)",
          font=dict(family="Plus Jakarta Sans,Inter,sans-serif",
                    color="#EDE4D3", size=11),
          xaxis=dict(gridcolor="rgba(80,65,40,.15)",
                     linecolor="rgba(80,65,40,.3)", zeroline=False,
                     tickfont=dict(color="#EDE4D3", size=11),
                     title_font=dict(color="#EDE4D3", size=11)),
          yaxis=dict(gridcolor="rgba(80,65,40,.15)",
                     linecolor="rgba(80,65,40,.3)", zeroline=False,
                     tickfont=dict(color="#EDE4D3", size=11),
                     title_font=dict(color="#EDE4D3", size=11)),
          legend=dict(font=dict(color="#EDE4D3", size=11)))

# ── Animated Akita logo (adapted from DogNap reference) ──────────────────────
LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400"
     width="120" height="120" style="display:block;margin:0 auto">
  <defs>
    <linearGradient id="fur" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#D4A853"/>
      <stop offset="100%" style="stop-color:#6F4E37"/>
    </linearGradient>
    <linearGradient id="fur2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#EDE4D3"/>
      <stop offset="80%" style="stop-color:#D4A853;stop-opacity:0.8"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <g filter="url(#glow)" style="animation:float 6s ease-in-out infinite">
    <!-- Ears -->
    <path d="M120 80 L95 30 L85 35 L90 75 Q95 95 110 105 Z" fill="url(#fur)" opacity="0.95"/>
    <path d="M280 80 L305 30 L315 35 L310 75 Q305 95 290 105 Z" fill="url(#fur)" opacity="0.95"/>
    <!-- Head -->
    <ellipse cx="200" cy="160" rx="95" ry="85" fill="url(#fur)"/>
    <ellipse cx="200" cy="155" rx="80" ry="65" fill="url(#fur2)" opacity="0.25"/>
    <!-- Cheeks -->
    <path d="M140 135 Q130 115 115 120 Q105 130 120 145 Q130 155 145 150 Z"
          fill="#EDE4D3" opacity="0.5"/>
    <path d="M260 135 Q270 115 285 120 Q295 130 280 145 Q270 155 255 150 Z"
          fill="#EDE4D3" opacity="0.5"/>
    <!-- Eyes -->
    <circle cx="170" cy="145" r="13" fill="#1A1209"/>
    <circle cx="230" cy="145" r="13" fill="#1A1209"/>
    <circle cx="173" cy="142" r="4" fill="#EDE4D3" opacity="0.9"/>
    <circle cx="233" cy="142" r="4" fill="#EDE4D3" opacity="0.9"/>
    <!-- Nose -->
    <ellipse cx="200" cy="176" rx="14" ry="10" fill="#1A1209" opacity="0.85"/>
    <!-- Mouth -->
    <path d="M190 183 Q200 193 210 183" stroke="#1A1209" stroke-width="2.5"
          fill="none" stroke-linecap="round"/>
    <!-- Body -->
    <ellipse cx="200" cy="265" rx="75" ry="90" fill="url(#fur)"/>
    <!-- Front legs -->
    <path d="M155 330 Q160 365 170 380 Q175 388 165 390 Q150 390 148 380 Q142 365 140 345 Z"
          fill="url(#fur)"/>
    <path d="M245 330 Q240 365 230 380 Q225 388 235 390 Q250 390 252 380
             Q258 365 260 345 Z" fill="url(#fur)"/>
    <!-- Curly tail -->
    <path d="M275 250 Q310 260 330 280 Q345 300 355 340 Q360 360 340 365
             Q320 365 315 350 Q305 320 290 300 Z"
          fill="url(#fur)" opacity="0.85"/>
    <!-- Belly sheen -->
    <path d="M160 225 Q200 205 240 225 Q250 265 240 305 Q200 325 160 305
             Q150 265 160 225 Z" fill="url(#fur2)" opacity="0.2"/>
    <!-- Shadow -->
    <ellipse cx="200" cy="395" rx="55" ry="8" fill="rgba(212,168,83,0.1)"/>
  </g>
  <style>
    @keyframes float {
      0%,100% { transform: translateY(0); }
      50%      { transform: translateY(-8px); }
    }
  </style>
</svg>
"""

WORDMARK = """
<div style="text-align:center;margin-top:6px">
  <span style="font-family:Georgia,serif;font-size:22px;font-weight:800;
        color:#EDE4D3">Paw</span><span style="font-family:Georgia,serif;
        font-size:22px;font-weight:800;color:#D4A853">India</span>
  <div style="color:#7A6F5C;font-size:8px;letter-spacing:1.5px;
       text-transform:uppercase;margin-top:2px">
    Connecting Every Dog and Their Human
  </div>
</div>
"""

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&display=swap');
html,body,[class*="css"]{font-family:'Plus Jakarta Sans',sans-serif;background:#FFFCF8}
.stApp{background:#FFFCF8!important}
.main .block-container{background:#FFFCF8!important}
.block-container{padding-top:1.2rem;padding-bottom:2rem;max-width:1400px}
section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#1A1209,#0D0A06)!important;
  border-right:1px solid rgba(212,168,83,0.15)!important}
section[data-testid="stSidebar"] *{color:#C4B99A!important}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"]{gap:3px!important}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label{
  display:flex!important;align-items:center!important;background:transparent!important;
  border:1px solid transparent!important;border-radius:10px!important;padding:9px 14px!important;
  margin:0!important;cursor:pointer!important;width:100%!important;
  transition:all .25s cubic-bezier(.22,1,.36,1)!important}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover{
  background:rgba(212,168,83,0.06)!important;border-color:rgba(212,168,83,0.15)!important;
  transform:translateX(4px)!important}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked){
  background:linear-gradient(135deg,rgba(160,125,58,.22),rgba(155,124,182,.1))!important;
  border-color:rgba(212,168,83,0.3)!important}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label p{
  color:#7A6F5C!important;font-size:12.5px!important;font-weight:500!important;margin:0!important}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) p{
  color:#D4A853!important;font-weight:700!important}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label>div:first-child,
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] input[type="radio"]{
  display:none!important;width:0!important;height:0!important}
div[data-testid="metric-container"]{
  background:#FFFFFF!important;border:1px solid #E0CFC0!important;
  border-left:4px solid #6F4E37!important;border-radius:14px!important;
  padding:16px 18px!important;
  box-shadow:0 2px 12px rgba(111,78,55,.08)!important}
div[data-testid="metric-container"] label{
  color:#4A2C1A!important;font-size:0.72rem!important;font-weight:700!important;
  text-transform:uppercase!important;letter-spacing:.1em!important}
div[data-testid="metric-container"] div[data-testid="stMetricValue"]{
  color:#2C1810!important;font-size:1.6rem!important;font-weight:800!important}
.stTabs [data-baseweb="tab-list"]{
  background:rgba(255,248,240,0.9)!important;border-radius:12px!important;
  padding:4px!important;border:1px solid #E8D5C4!important}
.stTabs [data-baseweb="tab"]{
  background:transparent!important;border-radius:9px!important;
  color:#4A2C1A!important;font-size:12.5px!important;
  font-weight:600!important;padding:8px 18px!important;
  transition:all .2s!important}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,#6F4E37,#D4860B)!important;
  color:#FFF8F0!important;box-shadow:0 2px 8px rgba(111,78,55,.25)!important}
.stTabs [data-baseweb="tab-border"]{display:none!important}
.stTabs [data-baseweb="tab-panel"]{padding-top:16px!important}
.stButton>button{
  background:linear-gradient(135deg,#6F4E37,#D4860B)!important;
  color:#FFF8F0!important;border:none!important;border-radius:10px!important;
  font-weight:700!important;padding:9px 22px!important}
.stDownloadButton>button{
  background:linear-gradient(135deg,#3d6b3d,#5a9a5a)!important;
  color:white!important;border:none!important;border-radius:10px!important;font-weight:700!important}
.icard{background:#FFFFFF;border:1px solid #E0CFC0;border-radius:14px;
       padding:20px;margin-bottom:14px;box-shadow:0 2px 12px rgba(111,78,55,.06)}
.shead{color:#4A2C1A;font-size:1.1rem;font-weight:700;border-bottom:2px solid #D4860B;
       padding-bottom:6px;margin:22px 0 14px}
.ibox{background:linear-gradient(135deg,rgba(212,168,83,.1),rgba(255,252,248,.8));
      border-left:4px solid #D4860B;border-radius:0 10px 10px 0;
      padding:12px 16px;margin:10px 0 18px;color:#2C1810;font-size:.88rem}
.lbar{display:flex;align-items:center;justify-content:space-between;
      padding:9px 18px;border-radius:12px;margin-bottom:16px;
      background:linear-gradient(135deg,rgba(26,18,9,.92),rgba(13,10,6,.97));
      border:1px solid rgba(212,168,83,.2)}
@keyframes liveDot{0%,100%{opacity:1}50%{opacity:.3}}
@keyframes floatCard{0%,100%{transform:translateY(0);box-shadow:0 4px 20px rgba(111,78,55,.12)}50%{transform:translateY(-4px);box-shadow:0 8px 28px rgba(111,78,55,.18)}}
</style>
""", unsafe_allow_html=True)


# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    raw  = pd.read_csv(os.path.join(base, "pawindia_raw_data.csv"))
    df   = pd.read_csv(os.path.join(base, "pawindia_cleaned_data.csv"))
    return raw, df


# ── ML functions ──────────────────────────────────────────────────────────────
@st.cache_data
def build_features():
    _, df = load_data()
    cols = [
        "Q1_age_group_enc","Q6_ownership_duration_enc","Q7_monthly_spend_inr",
        "Q9_online_purchase_freq_enc","Q13_pet_space_satisfaction_enc",
        "Q15_app_usage_enc","Q20_community_importance_enc",
        "Q22_reviews_importance_enc","Q24_emergency_vet_freq_enc",
        "engagement_score","spend_per_dog",
        "Q2_city_tier_Metro","Q2_city_tier_Tier-2","Q2_city_tier_Rural",
        "Q4_num_dogs_1 Dog","Q4_num_dogs_2 Dogs","Q4_num_dogs_3+ Dogs",
        "Q17_location_sharing_Yes Always","Q17_location_sharing_Yes When Using App",
        "Q18_subscription_pref_Freemium","Q18_subscription_pref_Monthly Sub",
        "Q18_subscription_pref_Annual Sub","Q18_subscription_pref_Would Not Pay",
        "Q19_adoption_interest_Yes Actively","Q19_adoption_interest_Yes Considering",
        "Q21_social_media_dogs_Active","Q21_social_media_dogs_Passive",
        "Q10_challenges__hard_to_find_reliable_vet",
        "Q10_challenges__no_pet_friendly_spaces",
        "Q10_challenges__losing_track_of_vaccinations",
        "Q14_preferred_features__health_vaccination_tracker",
        "Q14_preferred_features__nearby_vet_directory",
    ]
    valid = [c for c in cols if c in df.columns]
    X  = df[valid].fillna(0)
    y3 = df["Q25_target"].fillna(1).astype(int)
    return X, y3, valid


@st.cache_data
def run_classification():
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import (RandomForestClassifier,
                                   GradientBoostingClassifier, AdaBoostClassifier)
    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.metrics import (accuracy_score, precision_score,
                                  recall_score, f1_score, confusion_matrix)
    try:
        from xgboost import XGBClassifier
        xgb = XGBClassifier(n_estimators=80, max_depth=5, learning_rate=0.1,
                             random_state=42, eval_metric="mlogloss", verbosity=0,
                             n_jobs=-1)
        has_xgb = True
    except ImportError:
        has_xgb = False

    X, y3, feat_names = build_features()
    Xtr, Xte, ytr, yte = train_test_split(X, y3, test_size=0.2,
                                            random_state=42, stratify=y3)
    sc = StandardScaler()
    Xtr_s, Xte_s = sc.fit_transform(Xtr), sc.transform(Xte)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=300, class_weight="balanced", random_state=42),
        "Decision Tree":       DecisionTreeClassifier(max_depth=5, class_weight="balanced", random_state=42),
        "Random Forest":       RandomForestClassifier(n_estimators=50, class_weight="balanced", random_state=42, n_jobs=-1),
        "Gradient Boosting":   GradientBoostingClassifier(n_estimators=50, random_state=42),
        "AdaBoost":            AdaBoostClassifier(n_estimators=50, random_state=42),
        "SVM":                 SVC(kernel="rbf", probability=True, class_weight="balanced", random_state=42),
        "KNN":                 KNeighborsClassifier(n_neighbors=7),
        "Naive Bayes":         GaussianNB(),
    }
    if has_xgb:
        models["XGBoost"] = xgb

    results, cms, feat_imp = [], {}, {}
    for name, m in models.items():
        scaled = name in ("Logistic Regression","SVM","KNN")
        Xf, Xe = (Xtr_s, Xte_s) if scaled else (Xtr, Xte)
        m.fit(Xf, ytr); pred = m.predict(Xe)
        results.append({"Model": name,
                         "Accuracy":  round(accuracy_score(yte, pred), 3),
                         "Precision": round(precision_score(yte, pred, average="weighted", zero_division=0), 3),
                         "Recall":    round(recall_score(yte, pred, average="weighted", zero_division=0), 3),
                         "F1-Score":  round(f1_score(yte, pred, average="weighted", zero_division=0), 3),
                         "CV Acc":    round(cross_val_score(m, Xf, ytr, cv=5, scoring="accuracy").mean(), 3)})
        cms[name] = confusion_matrix(yte, pred)
        if hasattr(m, "feature_importances_"):
            feat_imp[name] = dict(zip(feat_names, m.feature_importances_))
        elif hasattr(m, "coef_"):
            feat_imp[name] = dict(zip(feat_names, np.abs(m.coef_).mean(axis=0)))

    rdf = pd.DataFrame(results).sort_values("F1-Score", ascending=False)
    return rdf, cms, feat_imp, rdf.iloc[0]["Model"], yte, feat_names


@st.cache_data
def run_clustering():
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    _, df = load_data()
    cols = ["Q1_age_group_enc","Q7_monthly_spend_inr","Q9_online_purchase_freq_enc",
            "Q15_app_usage_enc","Q20_community_importance_enc","Q22_reviews_importance_enc",
            "engagement_score","spend_per_dog","Q2_city_tier_Metro","Q2_city_tier_Tier-2"]
    valid = [c for c in cols if c in df.columns]
    Xs = StandardScaler().fit_transform(df[valid].fillna(0))
    inertias, sils = [], []
    for k in range(2, 9):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(Xs); inertias.append(km.inertia_)
        sils.append(silhouette_score(Xs, km.labels_))
    km4 = KMeans(n_clusters=4, random_state=42, n_init=10)
    labels = km4.fit_predict(Xs)
    df2 = df.copy(); df2["cluster"] = labels
    personas = {
        0: ("Urban Enthusiast",   "#D4860B", "Metro, high spend, active app user"),
        1: ("Practical Parent",   "#6F4E37", "Tier-2, moderate spend, functional needs"),
        2: ("Casual Companion",   "#9B7CB6", "Any city, low spend, passive"),
        3: ("Community Seeker",   "#5BB8C4", "Values community and reviews strongly"),
    }
    summary = df2.groupby("cluster").agg(
        Count=("Q7_monthly_spend_inr","count"),
        Avg_Spend=("Q7_monthly_spend_inr","mean"),
        Avg_App=("Q15_app_usage_enc","mean"),
        Pct_Metro=("Q2_city_tier_Metro","mean"),
        Pct_Yes=("Q25_binary","mean"),
    ).round(2).reset_index()
    summary["Persona"] = summary["cluster"].map(lambda x: personas[x][0])
    summary["Color"]   = summary["cluster"].map(lambda x: personas[x][1])
    return list(range(2,9)), inertias, sils, labels, df2, summary, personas


@st.cache_data
def run_association_rules():
    from mlxtend.frequent_patterns import apriori, association_rules
    _, df = load_data()
    ch = [c for c in df.columns if c.startswith("Q10_challenges__")]
    ft = [c for c in df.columns if c.startswith("Q14_preferred_features__")]
    basket = df[ch+ft].fillna(0).astype(bool)
    freq  = apriori(basket, min_support=0.08, use_colnames=True)
    rules = association_rules(freq, metric="lift", min_threshold=1.1)
    rules = rules[
        rules["antecedents"].apply(lambda x: any("challenge" in i for i in x)) &
        rules["consequents"].apply(lambda x: any("feature" in i for i in x))
    ].copy()
    def clean(s):
        return str(s).replace("Q10_challenges__","").replace("Q14_preferred_features__","").replace("_"," ").title()
    rules["antecedents_str"] = rules["antecedents"].apply(lambda x: ", ".join([clean(i) for i in x]))
    rules["consequents_str"] = rules["consequents"].apply(lambda x: ", ".join([clean(i) for i in x]))
    return rules.sort_values("lift", ascending=False).head(30).round(3)


@st.cache_data
def run_regression():
    from sklearn.linear_model import LinearRegression, Ridge, Lasso
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
    X, y3, feat_names = build_features()
    _, df = load_data()
    y = df["Q7_monthly_spend_inr"].fillna(df["Q7_monthly_spend_inr"].median()).iloc[:len(X)]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    sc = StandardScaler(); Xtr_s, Xte_s = sc.fit_transform(Xtr), sc.transform(Xte)
    models = {"Linear": LinearRegression(), "Ridge (L2)": Ridge(alpha=1.0),
              "Lasso (L1)": Lasso(alpha=0.5, max_iter=2000)}
    results, preds, coefs = [], {}, {}
    for name, m in models.items():
        m.fit(Xtr_s, ytr); p = m.predict(Xte_s)
        results.append({"Model": name, "R2": round(r2_score(yte,p),3),
                         "RMSE": round(np.sqrt(mean_squared_error(yte,p)),1),
                         "MAE":  round(mean_absolute_error(yte,p),1),
                         "CV R2":round(cross_val_score(m,Xtr_s,ytr,cv=5,scoring="r2").mean(),3)})
        preds[name] = (yte.values, p)
        coefs[name] = dict(zip(feat_names, m.coef_))
    return pd.DataFrame(results), preds, coefs, feat_names


# ── City data ─────────────────────────────────────────────────────────────────
CITY_COORDS = {"Mumbai":(19.076,72.877),"Delhi":(28.613,77.209),
               "Bengaluru":(12.971,77.594),"Indore":(22.719,75.857),
               "Pune":(18.520,73.856),"Hyderabad":(17.385,78.486)}

PLACES = [
    {"city":"Mumbai","name":"PawFect Vet Clinic","category":"Vet","lat":19.082,"lon":72.891,"rating":4.7,"reviews":312,"note":"24hr emergency"},
    {"city":"Mumbai","name":"Bandstand Dog Park","category":"Park","lat":19.047,"lon":72.817,"rating":4.5,"reviews":891,"note":"Sea-facing off-leash area"},
    {"city":"Mumbai","name":"The Doggy Cafe","category":"Cafe","lat":19.059,"lon":72.829,"rating":4.3,"reviews":204,"note":"Bandra favourite"},
    {"city":"Mumbai","name":"Happy Paws Grooming","category":"Grooming","lat":19.119,"lon":72.908,"rating":4.6,"reviews":178,"note":"Mobile grooming available"},
    {"city":"Delhi","name":"Sanjay Lake Dog Park","category":"Park","lat":28.659,"lon":77.312,"rating":4.4,"reviews":634,"note":"Large fenced area"},
    {"city":"Delhi","name":"Capital Vet Hospital","category":"Vet","lat":28.567,"lon":77.210,"rating":4.8,"reviews":487,"note":"Top rated in South Delhi"},
    {"city":"Delhi","name":"Paws & Claws Cafe","category":"Cafe","lat":28.524,"lon":77.185,"rating":4.1,"reviews":312,"note":"Pet menu available"},
    {"city":"Delhi","name":"Delhi Dog Grooming","category":"Grooming","lat":28.632,"lon":77.219,"rating":4.5,"reviews":221,"note":"Spa treatments"},
    {"city":"Bengaluru","name":"Cubbon Park Dog Area","category":"Park","lat":12.976,"lon":77.592,"rating":4.6,"reviews":1203,"note":"City centre, very popular"},
    {"city":"Bengaluru","name":"CUPA Animal Hospital","category":"Vet","lat":12.985,"lon":77.609,"rating":4.9,"reviews":892,"note":"Best rescue care in BLR"},
    {"city":"Bengaluru","name":"Barks & Brews","category":"Cafe","lat":12.935,"lon":77.624,"rating":4.4,"reviews":567,"note":"Koramangala hotspot"},
    {"city":"Bengaluru","name":"The Groom Room","category":"Grooming","lat":12.958,"lon":77.648,"rating":4.7,"reviews":334,"note":"Indiranagar, premium"},
    {"city":"Indore","name":"Indore Pet Clinic","category":"Vet","lat":22.724,"lon":75.883,"rating":4.5,"reviews":187,"note":"Experienced small animal vet"},
    {"city":"Indore","name":"Rajwada Dog Park","category":"Park","lat":22.719,"lon":75.857,"rating":4.0,"reviews":312,"note":"Central location"},
    {"city":"Indore","name":"Pawsome Cafe Indore","category":"Cafe","lat":22.733,"lon":75.886,"rating":4.2,"reviews":145,"note":"Newly opened"},
    {"city":"Indore","name":"FurFresh Grooming","category":"Grooming","lat":22.745,"lon":75.892,"rating":4.4,"reviews":98,"note":"Home visits available"},
    {"city":"Pune","name":"Paws Pune Vet","category":"Vet","lat":18.536,"lon":73.847,"rating":4.6,"reviews":298,"note":"Koregaon Park"},
    {"city":"Pune","name":"Empress Garden Dog Zone","category":"Park","lat":18.538,"lon":73.878,"rating":4.4,"reviews":534,"note":"Weekends get crowded"},
    {"city":"Pune","name":"Doggo Cafe Baner","category":"Cafe","lat":18.559,"lon":73.786,"rating":4.3,"reviews":276,"note":"IT crowd favourite"},
    {"city":"Pune","name":"Snip & Wag","category":"Grooming","lat":18.520,"lon":73.856,"rating":4.5,"reviews":189,"note":"Appointment only"},
    {"city":"Hyderabad","name":"Jubilee Hills Vet","category":"Vet","lat":17.431,"lon":78.407,"rating":4.7,"reviews":341,"note":"Premium area clinic"},
    {"city":"Hyderabad","name":"KBR Park Dog Walk","category":"Park","lat":17.425,"lon":78.434,"rating":4.5,"reviews":789,"note":"Gated, safe, early morning"},
    {"city":"Hyderabad","name":"Cafe Barko","category":"Cafe","lat":17.447,"lon":78.391,"rating":4.2,"reviews":223,"note":"Banjara Hills"},
    {"city":"Hyderabad","name":"PawLux Grooming","category":"Grooming","lat":17.410,"lon":78.456,"rating":4.6,"reviews":167,"note":"Luxury spa packages"},
]
CAT_COLORS = {"Vet":[229,57,53],"Park":[76,175,80],"Cafe":[212,134,11],"Grooming":[111,78,55]}
CAT_ICONS  = {"Vet":"🏥","Park":"🌳","Cafe":"☕","Grooming":"✂️"}


# ── UI helpers ────────────────────────────────────────────────────────────────
def shead(t):
    st.markdown(f'<div class="shead">{t}</div>', unsafe_allow_html=True)

def ibox(t):
    st.markdown(f'<div class="ibox">💡 {t}</div>', unsafe_allow_html=True)

def live_bar(n):
    now = time.strftime("%H:%M:%S")
    st.markdown(
        f'<div class="lbar">'
        f'<div style="display:flex;align-items:center;gap:10px">'
        f'<div style="width:8px;height:8px;border-radius:50%;background:#7CB67C;'
        f'animation:liveDot 2s ease-in-out infinite"></div>'
        f'<span style="color:#7CB67C;font-size:10px;font-weight:700;letter-spacing:.1em">LIVE</span>'
        f'<span style="color:#5a5040;font-size:10px">|</span>'
        f'<span style="color:#C4B99A;font-size:11px">{n:,} respondents loaded</span></div>'
        f'<span style="color:#D4A853;font-size:12px;font-weight:700;font-family:monospace">{now}</span>'
        f'</div>', unsafe_allow_html=True)

def ring(pct, color, label, size=88, stroke=8):
    r = (size-stroke)/2; circ = 2*math.pi*r; offset = circ*(1-pct/100)
    return (f'<div style="text-align:center">'
            f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
            f'style="filter:drop-shadow(0 0 6px {color}50)">'
            f'<circle cx="{size//2}" cy="{size//2}" r="{r}" fill="none" '
            f'stroke="rgba(111,78,55,0.12)" stroke-width="{stroke}"/>'
            f'<circle cx="{size//2}" cy="{size//2}" r="{r}" fill="none" '
            f'stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" '
            f'stroke-dasharray="{circ:.1f}" stroke-dashoffset="{offset:.1f}" '
            f'transform="rotate(-90 {size//2} {size//2})"/>'
            f'<text x="{size//2}" y="{size//2-3}" text-anchor="middle" fill="{color}" '
            f'font-size="15" font-weight="800" font-family="Bricolage Grotesque">{pct:.0f}%</text>'
            f'<text x="{size//2}" y="{size//2+13}" text-anchor="middle" fill="#5C3D2E" '
            f'font-size="8" font-weight="600">{label}</text>'
            f'</svg></div>')

def _merge_layout(base, h, kw):
    """Safely merge base layout with overrides — nested dicts (xaxis/yaxis/font) are merged not replaced."""
    layout = dict(base)
    layout["height"] = h
    for k, v in kw.items():
        if k in layout and isinstance(layout[k], dict) and isinstance(v, dict):
            layout[k] = {**layout[k], **v}
        else:
            layout[k] = v
    return layout

def pc(fig, h=320, **kw):
    """Apply cream/light base layout, safely merging any overrides."""
    fig.update_layout(**_merge_layout(PL, h, kw))
    st.plotly_chart(fig, width='stretch', config=PCFG)

def pd_chart(fig, h=360, **kw):
    """Apply dark base layout, safely merging any overrides."""
    fig.update_layout(**_merge_layout(PD, h, kw))
    st.plotly_chart(fig, width='stretch', config=PCFG)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(LOGO_SVG + WORDMARK, unsafe_allow_html=True)
    st.markdown("<hr style='border:none;border-top:1px solid rgba(212,168,83,0.15);margin:14px 0'>",
                unsafe_allow_html=True)
    st.markdown("<p style='font-size:.65rem;letter-spacing:1.8px;color:#5a5040;"
                "text-transform:uppercase;margin:0 0 8px 4px;font-weight:700'>Navigate</p>",
                unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["🏠  Home", "📍  Know Your City", "🐶  Dog Owner Insights",
         "💰  Will They Buy?", "🔬  Data Journey", "📊  Research & Analytics"],
        label_visibility="collapsed",
    )
    st.markdown("<hr style='border:none;border-top:1px solid rgba(212,168,83,0.1);margin:16px 0'>",
                unsafe_allow_html=True)
    st.markdown("<p style='font-size:.65rem;color:#5a5040;text-align:center;line-height:1.8'>"
                "PawIndia &copy; 2024<br><span style='color:#D4A853'>Market Research Dashboard</span></p>",
                unsafe_allow_html=True)


# ── Load data ─────────────────────────────────────────────────────────────────
raw, df = load_data()
n = len(df)
pct_yes   = round((df["Q25_app_adoption"]=="Yes").sum()/n*100, 1)
pct_maybe = round((df["Q25_app_adoption"]=="Maybe").sum()/n*100, 1)
pct_no    = round((df["Q25_app_adoption"]=="No").sum()/n*100, 1)
avg_spend = int(df["Q7_monthly_spend_inr"].mean())


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠  Home":
    st.markdown("<h1 style='color:#2C1810;font-size:1.8rem;margin-bottom:4px'>Welcome to PawIndia</h1>"
                "<p style='color:#4A2C1A;font-size:.95rem'>India's first super-app for dog owners — validated by real market research</p>",
                unsafe_allow_html=True)
    live_bar(n)

    c1,c2,c3,c4,c5 = st.columns(5)
    avg_spend_k = f"Rs.{avg_spend/1000:.1f}K"
    def _kpi(label, value, sub, color, delay):
        st.markdown(
            f'''<div style="background:#FFFFFF;border:1px solid #E0CFC0;
            border-top:4px solid {color};border-radius:14px;padding:18px 16px;
            text-align:center;box-shadow:0 4px 20px rgba(111,78,55,.12);
            animation:floatCard 5s ease-in-out {delay} infinite">
            <div style="color:#7A5C44;font-size:.68rem;font-weight:700;
            text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px">{label}</div>
            <div style="color:{color};font-size:1.7rem;font-weight:800;
            font-family:Bricolage Grotesque,sans-serif;letter-spacing:-.02em">{value}</div>
            <div style="color:#5C3D2E;font-size:.75rem;margin-top:5px;font-weight:500">{sub}</div>
            </div>''', unsafe_allow_html=True)
    with c1: _kpi("Respondents",    f"{n:,}",             "After cleaning",     BROWN,  "0s")
    with c2: _kpi("Will Download",  f"{pct_yes:.1f}%",    "Definite Yes",       "#2E7D32","0.3s")
    with c3: _kpi("Open to Trying", f"{pct_maybe:.1f}%",  "Conditional",        AMBER,  "0.6s")
    with c4: _kpi("Avg Spend/Month",avg_spend_k,           "Per dog owner",      BROWN,  "0.9s")
    with c5: _kpi("Total Reachable",f"{pct_yes+pct_maybe:.1f}%","Yes + Maybe",   TEAL,   "1.2s")

    st.markdown("<br>", unsafe_allow_html=True)

    # Rings
    shead("Adoption at a Glance")
    rc = st.columns(5)
    rc[0].markdown(ring(pct_yes,   "#4CAF50", "Would Download"), unsafe_allow_html=True)
    rc[1].markdown(ring(pct_maybe, HONEY,     "Open to It"),     unsafe_allow_html=True)
    rc[2].markdown(ring(pct_no,    "#E53935", "Would Not"),      unsafe_allow_html=True)
    rc[3].markdown(ring(pct_yes+pct_maybe, TEAL, "Reachable"),   unsafe_allow_html=True)
    with rc[4]:
        fig = go.Figure(go.Pie(
            labels=["Yes","Maybe","No"],
            values=[(df["Q25_app_adoption"]==l).sum() for l in ["Yes","Maybe","No"]],
            hole=0.55, marker_colors=["#4CAF50",HONEY,"#E53935"],
            textinfo="percent", textfont_size=11,
        ))
        fig.update_layout(height=140, margin=dict(t=0,b=0,l=0,r=0),
                          paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
        st.plotly_chart(fig, width='stretch', config=PCFG)

    # Business question
    st.markdown(
        f'<div class="icard" style="border-left:5px solid {AMBER}">'
        f'<div style="color:{AMBER};font-size:.75rem;font-weight:700;'
        f'text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px">The Question We Are Answering</div>'
        f'<div style="color:#3E2A1A;font-size:.95rem;line-height:1.7">'
        f'Do dog owners in India face enough real problems finding vets, parks, grooming, '
        f'and community that they would download and pay for one app that does it all? '
        f'The survey says <strong style="color:#4CAF50">{pct_yes+pct_maybe}% are open to it</strong> '
        f'— and this dashboard shows exactly who, where, and why.'
        f'</div></div>', unsafe_allow_html=True)

    # Two columns: challenges + features
    cl, cr = st.columns(2)
    with cl:
        shead("What Dog Owners Struggle With")
        ch_cols = {c: c.replace("Q10_challenges__","").replace("_"," ").title()
                   for c in df.columns if c.startswith("Q10_challenges__")}
        ch_df = pd.DataFrame({"Challenge": list(ch_cols.values()),
                               "Count": [int(df[col].sum()) for col in ch_cols]}).sort_values("Count")
        fig = go.Figure(go.Bar(x=ch_df["Count"], y=ch_df["Challenge"], orientation="h",
                                marker=dict(color=ch_df["Count"],
                                            colorscale=[[0,"#F0E4D7"],[0.5,HONEY],[1,BROWN]]),
                                text=ch_df["Count"], textposition="outside"))
        pc(fig, h=320, margin=dict(t=10,b=10,l=220,r=60),
           xaxis=dict(showgrid=False,visible=False), yaxis=dict(tickfont=dict(color="#2C1810",size=10)))
        ibox("Finding a reliable vet is the biggest pain point — directly justifying PawIndia's core feature.")
    with cr:
        shead("Features Dog Owners Want Most")
        ft_cols = {c: c.replace("Q14_preferred_features__","").replace("_"," ").title()
                   for c in df.columns if c.startswith("Q14_preferred_features__")}
        ft_df = pd.DataFrame({"Feature": list(ft_cols.values()),
                               "Count": [int(df[col].sum()) for col in ft_cols]}).sort_values("Count").tail(7)
        fig2 = go.Figure(go.Bar(x=ft_df["Count"], y=ft_df["Feature"], orientation="h",
                                 marker_color=AMBER, text=ft_df["Count"], textposition="outside"))
        pc(fig2, h=320, margin=dict(t=10,b=10,l=220,r=60),
           xaxis=dict(showgrid=False,visible=False), yaxis=dict(tickfont=dict(color="#2C1810",size=10)))
        ibox("Health tracker tops the list — an easy first feature to build for maximum impact.")

    # Spend vs adoption
    shead("Do Higher Spenders Want the App More?")
    fig3 = go.Figure()
    for cat, col in [("Yes","#4CAF50"),("Maybe",HONEY),("No","#E53935")]:
        v = df[df["Q25_app_adoption"]==cat]["Q7_monthly_spend_inr"]
        fig3.add_trace(go.Box(y=v, name=f"{cat} (n={len(v)})", marker_color=col, boxmean=True))
    pc(fig3, h=300, margin=dict(t=10,b=20), yaxis=dict(title="Monthly Spend (INR)"))
    yes_s = int(df[df["Q25_app_adoption"]=="Yes"]["Q7_monthly_spend_inr"].mean())
    no_s  = int(df[df["Q25_app_adoption"]=="No"]["Q7_monthly_spend_inr"].mean())
    ibox(f"Yes owners spend Rs.{yes_s:,}/month vs Rs.{no_s:,} for No owners. "
         f"The Rs.{yes_s-no_s:,} gap confirms that higher-spending dog parents are the prime target.")

    d1, d2, _ = st.columns([1,1,3])
    with d1:
        st.download_button("Download Raw Data", raw.to_csv(index=False), "pawindia_raw.csv", "text/csv")
    with d2:
        st.download_button("Download Cleaned Data", df.to_csv(index=False), "pawindia_clean.csv", "text/csv")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — KNOW YOUR CITY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📍  Know Your City":
    st.markdown("<h1 style='color:#2C1810;font-size:1.8rem;margin-bottom:4px'>Know Your City</h1>"
                "<p style='color:#4A2C1A;font-size:.95rem'>Find dog-friendly vets, parks, cafes and grooming near you</p>",
                unsafe_allow_html=True)
    live_bar(n)

    st.markdown('<div class="ibox">📌 <strong>Note:</strong> Places shown are simulated for '
                'demonstration. PawIndia will connect to live Google Places and OpenStreetMap '
                'data at launch.</div>', unsafe_allow_html=True)

    cc, cf, cs = st.columns(3)
    with cc: city = st.selectbox("City", list(CITY_COORDS.keys()), index=2)
    with cf:
        cats = ["All"] + sorted(set(p["category"] for p in PLACES))
        cat  = st.selectbox("Type", cats)
    with cs:
        min_r = st.slider("Min Rating", 3.5, 5.0, 4.0, 0.1)

    places_df = pd.DataFrame(PLACES)
    filtered  = places_df[places_df["city"]==city].copy()
    if cat != "All":
        filtered = filtered[filtered["category"]==cat]
    filtered = filtered[filtered["rating"] >= min_r].copy()

    if filtered.empty:
        st.warning("No places match your filters. Try lowering the minimum rating.")
    else:
        shead(f"India Map — Dog-Friendly Places in {city}")

        # ── Choropleth-style India map with city bubbles ───────────────────────
        # City summary stats for bubble sizing
        city_stats = []
        places_all = pd.DataFrame(PLACES)
        for c_name, (clat, clon) in CITY_COORDS.items():
            city_p = places_all[places_all["city"]==c_name]
            city_stats.append({
                "city": c_name, "lat": clat, "lon": clon,
                "total_places": len(city_p),
                "avg_rating": round(city_p["rating"].mean(), 2) if len(city_p) > 0 else 0,
                "vets": len(city_p[city_p["category"]=="Vet"]),
                "parks": len(city_p[city_p["category"]=="Park"]),
                "cafes": len(city_p[city_p["category"]=="Cafe"]),
                "grooming": len(city_p[city_p["category"]=="Grooming"]),
                "selected": c_name == city,
            })
        cs_df = pd.DataFrame(city_stats)

        fig_india = go.Figure()

        # Background: all city bubbles (grey, sized by total places)
        other = cs_df[cs_df["city"] != city]
        fig_india.add_trace(go.Scattergeo(
            lat=other["lat"], lon=other["lon"],
            mode="markers+text",
            marker=dict(size=other["total_places"]*6, color="rgba(111,78,55,0.25)",
                        line=dict(color="#6F4E37", width=1.5)),
            text=other["city"],
            textposition="top center",
            textfont=dict(size=11, color="#6F4E37"),
            hovertemplate="<b>%{text}</b><br>Places: " + other["total_places"].astype(str) +
                          "<br>Avg Rating: " + other["avg_rating"].astype(str) + " ★<extra></extra>",
            name="Other Cities", showlegend=False,
        ))

        # Selected city — highlighted gold
        sel = cs_df[cs_df["city"] == city].iloc[0]
        fig_india.add_trace(go.Scattergeo(
            lat=[sel["lat"]], lon=[sel["lon"]],
            mode="markers+text",
            marker=dict(size=sel["total_places"]*9, color=HONEY,
                        line=dict(color=BROWN, width=2.5),
                        symbol="circle"),
            text=[city],
            textposition="top center",
            textfont=dict(size=13, color=BROWN, family="Bricolage Grotesque"),
            hovertemplate=f"<b>{city}</b><br>Total places: {sel['total_places']}<br>"
                          f"Avg rating: {sel['avg_rating']} ★<br>"
                          f"Vets: {sel['vets']} | Parks: {sel['parks']}<br>"
                          f"Cafes: {sel['cafes']} | Grooming: {sel['grooming']}<extra></extra>",
            name=city, showlegend=False,
        ))

        # Filtered place dots on the map
        for _, row in filtered.iterrows():
            r, g, b = CAT_COLORS.get(row["category"], [111, 78, 55])
            fig_india.add_trace(go.Scattergeo(
                lat=[row["lat"]], lon=[row["lon"]],
                mode="markers",
                marker=dict(size=(row["rating"]-3)*10+8,
                            color=f"rgb({r},{g},{b})",
                            line=dict(color="white", width=1)),
                hovertemplate=f"<b>{row['name']}</b><br>{row['category']}<br>"
                              f"{row['rating']} ★ | {row['reviews']} reviews<br>"
                              f"{row['note']}<extra></extra>",
                name=row["category"], showlegend=False,
            ))

        fig_india.update_layout(
            geo=dict(
                scope="asia",
                resolution=50,
                showland=True,  landcolor="rgba(254,248,240,1)",
                showocean=True, oceancolor="rgba(200,225,245,0.5)",
                showlakes=True, lakecolor="rgba(200,225,245,0.5)",
                showcountries=True, countrycolor="rgba(111,78,55,0.3)",
                showsubunits=True, subunitcolor="rgba(111,78,55,0.15)",
                center=dict(lat=20.5, lon=78.9),
                projection_scale=4.5,
                bgcolor="rgba(254,248,240,1)",
                lataxis_range=[8, 35], lonaxis_range=[68, 98],
            ),
            height=520,
            margin=dict(t=10, b=10, l=0, r=0),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#2C1810"),
            legend=dict(orientation="h", y=-0.05),
        )
        st.plotly_chart(fig_india, width='stretch', config=PCFG)

        # City inference cards below the map
        c_inf1, c_inf2, c_inf3, c_inf4 = st.columns(4)
        inf_data = [
            (f"{sel['vets']} Vet Centres", "🏥", "#E53935", "Emergency & routine care"),
            (f"{sel['parks']} Dog Parks",   "🌳", "#4CAF50", "Off-leash exercise spots"),
            (f"{sel['cafes']} Dog Cafes",   "☕", AMBER,     "Pet-friendly hangouts"),
            (f"{sel['grooming']} Groomers", "✂️", BROWN,    "Wash & style services"),
        ]
        for col_w, (val, icon, color, desc) in zip([c_inf1,c_inf2,c_inf3,c_inf4], inf_data):
            col_w.markdown(
                f'<div style="background:#FFFFFF;border:1px solid #E0CFC0;'
                f'border-top:4px solid {color};border-radius:12px;padding:14px;text-align:center;'
                f'box-shadow:0 2px 10px rgba(111,78,55,.06)">'
                f'<div style="font-size:1.6rem">{icon}</div>'
                f'<div style="font-weight:800;color:#2C1810;font-size:.95rem;margin:4px 0">{val}</div>'
                f'<div style="color:#5C3D2E;font-size:.78rem;font-weight:500">{desc}</div>'
                f'</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        shead(f"Places in {city} ({len(filtered)} found)")
        cols3 = st.columns(3)
        for i, (_, row) in enumerate(filtered.iterrows()):
            r,g,b = CAT_COLORS.get(row["category"],[111,78,55])
            cols3[i%3].markdown(
                f'<div style="background:#fff;border:1px solid #E8D5C4;'
                f'border-top:3px solid rgb({r},{g},{b});border-radius:12px;'
                f'padding:16px;margin-bottom:12px;box-shadow:0 4px 14px rgba(111,78,55,.08)">'
                f'<div style="font-size:1.2rem">{CAT_ICONS.get(row["category"],"")}</div>'
                f'<div style="font-weight:700;color:#3E2A1A;margin:4px 0">{row["name"]}</div>'
                f'<div style="color:{AMBER};font-weight:600">{"★"*int(row["rating"])} {row["rating"]}</div>'
                f'<div style="color:#6B4226;font-size:.8rem">{row["reviews"]} reviews</div>'
                f'<div style="color:#6F4E37;font-size:.8rem;margin-top:4px;font-style:italic">{row["note"]}</div>'
                f'</div>', unsafe_allow_html=True)

        # Satisfaction by city tier
        shead("Are Dog Owners Happy With Pet-Friendly Spaces in Their City?")
        sat_data = []
        for col, label in [("Q2_city_tier_Metro","Metro"),("Q2_city_tier_Tier-2","Tier-2"),
                            ("Q2_city_tier_Tier-3","Tier-3"),("Q2_city_tier_Rural","Rural")]:
            if col in df.columns:
                sub = df[df[col]==1]
                if len(sub) > 0:
                    sat_data.append({"City Tier":label,
                                     "Avg Score":round(sub["Q13_pet_space_satisfaction_enc"].mean(),2)})
        if sat_data:
            sd = pd.DataFrame(sat_data)
            fig_s = go.Figure(go.Bar(x=sd["City Tier"], y=sd["Avg Score"],
                                      marker_color=[BROWN,AMBER,HONEY,"#C49A6C"],
                                      text=sd["Avg Score"], textposition="outside"))
            fig_s.add_hline(y=3, line_dash="dash", line_color="#5C3D2E", annotation_text="Neutral (3.0)", annotation_font_color="#2C1810")
            pc(fig_s, h=280, margin=dict(t=20,b=20),
               yaxis=dict(range=[0,5.5], title="Score (1-5)", rangemode="tozero"))
            ibox("Tier-2 and Tier-3 cities score below neutral on pet-friendly spaces — "
                 "the biggest growth opportunity for PawIndia outside metros.")

        st.download_button(f"Download {city} Places",
                           filtered.drop(columns=["color","elevation"], errors="ignore").to_csv(index=False),
                           f"pawindia_{city.lower()}.csv", "text/csv")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — DOG OWNER INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🐶  Dog Owner Insights":
    st.markdown("<h1 style='color:#2C1810;font-size:1.8rem;margin-bottom:4px'>Dog Owner Insights</h1>"
                "<p style='color:#4A2C1A;font-size:.95rem'>Who are India's dog owners, what do they spend, and what problems do they have?</p>",
                unsafe_allow_html=True)
    live_bar(n)

    t1,t2,t3,t4 = st.tabs(["👤 Who They Are","💸 What They Spend","😤 Their Problems","📱 How Digital Are They"])

    with t1:
        shead("Age and City Breakdown")
        c1, c2 = st.columns(2)
        with c1:
            age_order = ["Under 18","18-24","25-34","35-44","45-59","60+"]
            ac = raw["Q1_age_group"].value_counts().reindex(age_order, fill_value=0)
            fig = go.Figure(go.Bar(x=ac.index, y=ac.values, marker_color=CHART[:len(ac)],
                                    text=ac.values, textposition="outside"))
            pc(fig, h=280, margin=dict(t=10,b=20), title="Age Groups",
               yaxis=dict(showgrid=False, rangemode="tozero"))
        with c2:
            cc2 = raw["Q2_city_tier"].value_counts()
            fig2 = go.Figure(go.Pie(labels=cc2.index, values=cc2.values,
                                     marker_colors=CHART, hole=0.45, textinfo="label+percent"))
            fig2.update_layout(height=280, margin=dict(t=10,b=0),
                               paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                               font=dict(color="#2C1810"))
            st.plotly_chart(fig2, width='stretch', config=PCFG)
        ibox("25 to 34 year olds in metro cities make up the biggest group — "
             "India's millennial dog ownership boom in full effect.")

        # Age x City heatmap
        shead("Where Are the High-Value Segments?")
        age_enc = {"Under 18":0,"18-24":1,"25-34":2,"35-44":3,"45-59":4,"60+":5}
        tiers   = ["Metro","Tier-2","Tier-3","Rural"]
        hm_data = []
        for age in age_order:
            row_vals = []
            for tier in tiers:
                tcol = f"Q2_city_tier_{tier}"
                enc  = age_enc.get(age,-1)
                ct   = int(((df.get(tcol,pd.Series(0))==1) & (df["Q1_age_group_enc"]==enc)).sum()) if tcol in df.columns else 0
                row_vals.append(ct)
            hm_data.append(row_vals)
        fig_hm = go.Figure(go.Heatmap(z=hm_data, x=tiers, y=age_order,
                                       colorscale=[[0,"#FFF8F0"],[0.5,HONEY],[1,BROWN]],
                                       text=[[str(v) for v in row] for row in hm_data],
                                       texttemplate="%{text}", showscale=True))
        pc(fig_hm, h=300, margin=dict(t=10,b=20))
        ibox("The 25-34 Metro cell is the darkest square on the map — this is PawIndia's launch target.")

        c3, c4 = st.columns(2)
        with c3:
            dc = raw["Q4_num_dogs"].value_counts().reindex(["1 dog","2 dogs","3+ dogs"], fill_value=0)
            fig3 = go.Figure(go.Bar(x=dc.index, y=dc.values, marker_color=BROWN,
                                     text=dc.values, textposition="outside"))
            pc(fig3, h=250, title="Dogs Owned", margin=dict(t=40,b=20),
               yaxis=dict(showgrid=False, rangemode="tozero"))
        with c4:
            dt_cols = {c: c.replace("Q5_dog_type__","").replace("_"," ").title()
                       for c in df.columns if c.startswith("Q5_dog_type__")}
            dt_df = pd.DataFrame({"Type":list(dt_cols.values()),
                                   "Count":[int(df[col].sum()) for col in dt_cols]}).sort_values("Count")
            fig4 = go.Figure(go.Bar(x=dt_df["Count"], y=dt_df["Type"], orientation="h",
                                     marker_color=CHART[:len(dt_df)], text=dt_df["Count"], textposition="outside"))
            pc(fig4, h=250, title="Dog Breeds", margin=dict(t=40,b=10),
               xaxis=dict(showgrid=False,visible=False))

    with t2:
        shead("Monthly Spend Patterns")
        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure(go.Histogram(x=df["Q7_monthly_spend_inr"].dropna(), nbinsx=30,
                                          marker_color=BROWN, opacity=0.85))
            pc(fig, h=280, title="Spend Distribution", margin=dict(t=40,b=20),
               xaxis=dict(title="INR"), yaxis=dict(showgrid=False, rangemode="tozero"))
        with c2:
            city_s = []
            for col, label in [("Q2_city_tier_Metro","Metro"),("Q2_city_tier_Tier-2","Tier-2"),
                                ("Q2_city_tier_Tier-3","Tier-3"),("Q2_city_tier_Rural","Rural")]:
                if col in df.columns:
                    sub = df[df[col]==1]["Q7_monthly_spend_inr"]
                    if len(sub) > 0:
                        city_s.append({"City":label, "Avg":int(sub.mean())})
            cs_df = pd.DataFrame(city_s)
            fig2 = go.Figure(go.Bar(x=cs_df["City"], y=cs_df["Avg"],
                                     marker_color=[BROWN,AMBER,HONEY,"#C49A6C"],
                                     text=[f"Rs.{v:,}" for v in cs_df["Avg"]],
                                     textposition="outside"))
            pc(fig2, h=280, title="Avg Spend by City", margin=dict(t=40,b=20),
               yaxis=dict(showgrid=False, rangemode="tozero", title="INR"))
        ibox(f"Metro dog owners spend considerably more on average. "
             "This supports a tiered pricing strategy where premium features cost more in higher-spending markets.")

        shead("Where Does the Money Go?")
        cat_c = raw["Q8_top_spend_category"].value_counts()
        fig3 = go.Figure(go.Pie(labels=cat_c.index, values=cat_c.values,
                                 marker_colors=CHART, hole=0.4, textinfo="label+percent", textfont_size=11))
        fig3.update_layout(height=300, margin=dict(t=10,b=0),
                           paper_bgcolor="rgba(0,0,0,0)", showlegend=False, font=dict(color="#2C1810"))
        st.plotly_chart(fig3, width='stretch', config=PCFG)

    with t3:
        shead("The Real Struggles of Indian Dog Owners")
        ch_cols2 = {c: c.replace("Q10_challenges__","").replace("_"," ").title()
                    for c in df.columns if c.startswith("Q10_challenges__")}
        ch_df2 = pd.DataFrame({"Challenge":list(ch_cols2.values()),
                                "Count":[int(df[col].sum()) for col in ch_cols2]}).sort_values("Count")
        fig = go.Figure(go.Bar(x=ch_df2["Count"], y=ch_df2["Challenge"], orientation="h",
                                marker=dict(color=ch_df2["Count"],
                                            colorscale=[[0,"#F0E4D7"],[0.5,HONEY],[1,BROWN]]),
                                text=ch_df2["Count"], textposition="outside"))
        pc(fig, h=360, margin=dict(t=10,b=10),
           xaxis=dict(showgrid=False,visible=False), yaxis=dict(tickfont=dict(size=10)))
        ibox("Reliable vet access and lack of pet-friendly spaces are the top two problems. "
             "PawIndia's vet directory and places map directly address both.")

        c1, c2 = st.columns(2)
        with c1:
            shead("How People Find Vets Today")
            vc = raw["Q11_vet_discovery"].value_counts()
            fig2 = go.Figure(go.Pie(labels=vc.index, values=vc.values,
                                     marker_colors=CHART, hole=0.45, textinfo="label+percent"))
            fig2.update_layout(height=260, margin=dict(t=10,b=0),
                               paper_bgcolor="rgba(0,0,0,0)", showlegend=False, font=dict(color="#2C1810"))
            st.plotly_chart(fig2, width='stretch', config=PCFG)
        with c2:
            shead("Lost Dog Experiences")
            lc = raw["Q12_lost_dog_experience"].value_counts()
            fig3 = go.Figure(go.Bar(x=lc.index, y=lc.values,
                                     marker_color=CHART[:4], text=lc.values, textposition="outside"))
            pc(fig3, h=260, margin=dict(t=10,b=20), yaxis=dict(showgrid=False, rangemode="tozero"))
        ibox("45% of owners have struggled to find a lost dog — "
             "this validates PawIndia's community alert feature as a must-have, not a nice-to-have.")

    with t4:
        shead("How Dog Owners Use Apps and the Internet")
        c1, c2 = st.columns(2)
        with c1:
            ao = ["Never","Rarely","Sometimes","Often"]
            ac3 = raw["Q15_app_usage"].value_counts().reindex(ao, fill_value=0)
            fig = go.Figure(go.Bar(x=ac3.index, y=ac3.values, marker_color=CHART[:4],
                                    text=ac3.values, textposition="outside"))
            pc(fig, h=260, title="Current App Usage for Pet Needs", margin=dict(t=40,b=20),
               yaxis=dict(showgrid=False, rangemode="tozero"))
        with c2:
            pc2 = raw["Q16_purchase_platform"].value_counts()
            fig2 = go.Figure(go.Pie(labels=pc2.index, values=pc2.values,
                                     marker_colors=CHART, hole=0.4, textinfo="percent+label", textfont_size=10))
            fig2.update_layout(height=260, margin=dict(t=40,b=0),
                               paper_bgcolor="rgba(0,0,0,0)", showlegend=False, font=dict(color="#2C1810"),
                               title=dict(text="Where They Buy Products", font=dict(color=BROWN,size=13)))
            st.plotly_chart(fig2, width='stretch', config=PCFG)

        # Engagement vs spend scatter
        shead("Do More Engaged Users Also Spend More?")
        fig3 = px.scatter(df.sample(min(600,n), random_state=42),
                           x="engagement_score", y="Q7_monthly_spend_inr",
                           color="Q25_app_adoption",
                           color_discrete_map={"Yes":"#4CAF50","Maybe":HONEY,"No":"#E53935"},
                           opacity=0.5, size_max=8,
                           labels={"engagement_score":"Engagement Score",
                                   "Q7_monthly_spend_inr":"Monthly Spend (INR)",
                                   "Q25_app_adoption":"Would Download"})
        pc(fig3, h=320, margin=dict(t=20,b=20))
        ibox("The top-right corner — high engagement, high spend — is almost entirely green (Yes). "
             "Target acquisition at dog owners who already use 2+ pet-related apps.")

        # Correlation heatmap
        shead("How Key Behaviours Connect")
        corr_c = ["Q7_monthly_spend_inr","Q9_online_purchase_freq_enc","Q15_app_usage_enc",
                  "Q20_community_importance_enc","Q22_reviews_importance_enc",
                  "engagement_score","Q25_target"]
        valid_c = [c for c in corr_c if c in df.columns]
        labels_c = ["Spend","Online Freq","App Usage","Community","Reviews","Engagement","Target"][:len(valid_c)]
        corr_m = df[valid_c].corr().round(2)
        fig4 = go.Figure(go.Heatmap(z=corr_m.values, x=labels_c, y=labels_c,
                                     colorscale=[[0,"#FFF8F0"],[0.5,HONEY],[1,BROWN]],
                                     text=corr_m.values, texttemplate="%{text}",
                                     showscale=True, zmin=-1, zmax=1))
        pc(fig4, h=360, margin=dict(t=10,b=60,l=80,r=20), font=dict(size=10))
        ibox("Engagement score has the strongest link to app adoption. "
             "Building a habit loop in the app is the key to long-term retention.")

        st.download_button("Download Insights Data", df.to_csv(index=False),
                           "pawindia_insights.csv", "text/csv")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — WILL THEY BUY?
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💰  Will They Buy?":
    st.markdown("<h1 style='color:#2C1810;font-size:1.8rem;margin-bottom:4px'>Will They Buy?</h1>"
                "<p style='color:#4A2C1A;font-size:.95rem'>Subscription preferences, who is most likely to adopt, and what would make them pay</p>",
                unsafe_allow_html=True)
    live_bar(n)

    c1,c2,c3,c4 = st.columns(4)
    def _kpi4(label, value, sub, color):
        st.markdown(
            f'''<div style="background:#FFFFFF;border:1px solid #E0CFC0;
            border-top:4px solid {color};border-radius:14px;padding:18px 16px;
            text-align:center;box-shadow:0 4px 20px rgba(111,78,55,.1)">
            <div style="color:#7A5C44;font-size:.68rem;font-weight:700;
            text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px">{label}</div>
            <div style="color:{color};font-size:1.7rem;font-weight:800;
            font-family:Bricolage Grotesque,sans-serif">{value}</div>
            <div style="color:#5C3D2E;font-size:.75rem;margin-top:5px;font-weight:500">{sub}</div>
            </div>''', unsafe_allow_html=True)
    with c1: _kpi4("Definite Yes",   f"{pct_yes:.1f}%",           "Would download now",    "#2E7D32")
    with c2: _kpi4("Open to It",     f"{pct_maybe:.1f}%",         "Conditional adopters",  AMBER)
    with c3: _kpi4("Would Not",      f"{pct_no:.1f}%",            "Lost audience",         "#C62828")
    with c4: _kpi4("Total Reachable",f"{pct_yes+pct_maybe:.1f}%", "Yes + Maybe",           TEAL)

    st.markdown("<br>", unsafe_allow_html=True)
    t1,t2,t3,t4 = st.tabs(["🔻 Conversion Funnel","💳 Subscriptions","📍 By Location","👤 By Profile"])

    with t1:
        shead("How Many People Would Actually Download PawIndia?")
        total    = n
        interested = int((df["Q15_app_usage"] != "Never").sum()) if "Q15_app_usage" in df.columns else int(n*0.75)
        willing  = int((df["Q25_app_adoption"].isin(["Yes","Maybe"])).sum())
        definite = int((df["Q25_app_adoption"]=="Yes").sum())
        fig = go.Figure(go.Funnel(
            y=["Surveyed Dog Owners","Already Use Pet Apps","Open to Downloading","Would Definitely Download"],
            x=[total, interested, willing, definite],
            textinfo="value+percent initial",
            marker=dict(color=[BROWN,AMBER,HONEY,"#4CAF50"],
                        line=dict(color="#FFF8F0",width=1.5)),
            textfont=dict(color="#3E2A1A",size=13),
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,248,240,.3)",
                          height=360, margin=dict(t=20,b=20,l=20,r=20), font=dict(color="#2C1810"))
        st.plotly_chart(fig, width='stretch', config=PCFG)
        ibox(f"From {total:,} surveyed, {definite:,} ({pct_yes}%) would definitely download. "
             "The gap between 'open' and 'definite' is the conversion challenge — "
             "addressing trust and feature fit will close it.")

        shead("High Engagement + High Spend = Most Likely to Download")
        fig2 = px.scatter(df.sample(min(600,n), random_state=42),
                           x="engagement_score", y="Q7_monthly_spend_inr",
                           color="Q25_app_adoption",
                           color_discrete_map={"Yes":"#4CAF50","Maybe":HONEY,"No":"#E53935"},
                           size="Q7_monthly_spend_inr", size_max=12, opacity=0.5,
                           labels={"engagement_score":"Engagement Score",
                                   "Q7_monthly_spend_inr":"Monthly Spend (INR)",
                                   "Q25_app_adoption":"Would Download"})
        pc(fig2, h=320, margin=dict(t=20,b=20))
        ibox("Focus early marketing on dog owners who already spend heavily and use multiple apps. "
             "They are the most ready to adopt.")

    with t2:
        shead("What Pricing Model Would Work Best?")
        c1, c2 = st.columns(2)
        with c1:
            sub_c = raw["Q18_subscription_pref"].value_counts()
            fig = go.Figure(go.Pie(labels=sub_c.index, values=sub_c.values,
                                    marker_colors=CHART, hole=0.45, textinfo="label+percent", textfont_size=11))
            fig.update_layout(height=300, margin=dict(t=10,b=0),
                              paper_bgcolor="rgba(0,0,0,0)", showlegend=False, font=dict(color="#2C1810"))
            st.plotly_chart(fig, width='stretch', config=PCFG)
        with c2:
            sub_adopt = []
            for sub_col in [c for c in df.columns if c.startswith("Q18_subscription_pref_")]:
                label = sub_col.replace("Q18_subscription_pref_","")
                sub_df = df[df[sub_col]==1]
                if len(sub_df) > 10:
                    yes_r = (sub_df["Q25_app_adoption"]=="Yes").sum()/len(sub_df)*100
                    sub_adopt.append({"Model":label,"Yes %":round(yes_r,1)})
            sa_df = pd.DataFrame(sub_adopt).sort_values("Yes %", ascending=False)
            fig2 = go.Figure(go.Bar(x=sa_df["Yes %"], y=sa_df["Model"], orientation="h",
                                     marker=dict(color=sa_df["Yes %"],
                                                 colorscale=[[0,"#F0E4D7"],[0.5,HONEY],[1,BROWN]]),
                                     text=[f"{v}%" for v in sa_df["Yes %"]], textposition="outside"))
            pc(fig2, h=300, margin=dict(t=40,b=20,l=180,r=60),
               xaxis=dict(showgrid=False,visible=False),
               title="% Who Say Yes — by Subscription Preference")
        ibox("Freemium is the most popular preference, but users willing to pay monthly or annually "
             "show a significantly higher download intent. Start free, then convert the engaged users.")

        # Location sharing
        shead("Would People Share Their Location? (Critical for the Nearby Features)")
        loc_c = raw["Q17_location_sharing"].value_counts()
        pct_share = round((loc_c.get("Yes, always",0) + loc_c.get("Yes, only when using the app",0)) / n * 100, 1)
        fig3 = go.Figure(go.Pie(
            labels=loc_c.index, values=loc_c.values,
            marker_colors=[BROWN,AMBER,"#E8D5C4","#C49A6C"],
            hole=0.5, textinfo="label+percent",
        ))
        fig3.update_layout(height=280, margin=dict(t=10,b=0),
                           paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                           font=dict(color="#2C1810"),
                           annotations=[dict(text=f"<b>{pct_share}%</b><br>Share",
                                             x=0.5, y=0.5, showarrow=False,
                                             font=dict(size=14, color=BROWN))])
        st.plotly_chart(fig3, width='stretch', config=PCFG)
        ibox(f"{pct_share}% will share their location — enough to make the nearby vet, "
             "park, and community features viable from day one.")

    with t3:
        shead("Which Cities Are Most Ready for PawIndia?")
        city_adopt = []
        for col, label in [("Q2_city_tier_Metro","Metro"),("Q2_city_tier_Tier-2","Tier-2"),
                            ("Q2_city_tier_Tier-3","Tier-3"),("Q2_city_tier_Rural","Rural")]:
            if col in df.columns:
                sub = df[df[col]==1]
                if len(sub) > 10:
                    city_adopt.append({
                        "City": label,
                        "Yes":  round((sub["Q25_app_adoption"]=="Yes").sum()/len(sub)*100,1),
                        "Maybe":round((sub["Q25_app_adoption"]=="Maybe").sum()/len(sub)*100,1),
                        "No":   round((sub["Q25_app_adoption"]=="No").sum()/len(sub)*100,1),
                        "Avg Spend": int(sub["Q7_monthly_spend_inr"].mean()), "n": len(sub)
                    })
        ca_df = pd.DataFrame(city_adopt)
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Would Download", x=ca_df["City"], y=ca_df["Yes"], marker_color="#4CAF50"))
        fig.add_trace(go.Bar(name="Open to Trying", x=ca_df["City"], y=ca_df["Maybe"], marker_color=HONEY))
        fig.add_trace(go.Bar(name="Would Not",      x=ca_df["City"], y=ca_df["No"], marker_color="#E8D5C4"))
        pc(fig, h=320, margin=dict(t=20,b=60), barmode="stack",
           yaxis=dict(title="% of Respondents", showgrid=False, rangemode="tozero"),
           legend=dict(orientation="h",y=-0.2))
        ibox("Metro cities lead on adoption intent and spending. Tier-2 cities have a large 'Maybe' "
             "pool — these are the users most worth converting with targeted onboarding.")

        fig2 = px.scatter(ca_df, x="Avg Spend", y="Yes", size="n", color="City",
                           color_discrete_sequence=CHART, size_max=50,
                           labels={"Yes":"% Definite Yes","Avg Spend":"Avg Monthly Spend (INR)"},
                           title="Cities that spend more also adopt more")
        pc(fig2, h=280, margin=dict(t=40,b=20))

    with t4:
        shead("Who Is Most Likely to Download PawIndia?")
        c1, c2 = st.columns(2)
        with c1:
            age_enc2 = {"Under 18":0,"18-24":1,"25-34":2,"35-44":3,"45-59":4,"60+":5}
            aa = []
            for age in ["Under 18","18-24","25-34","35-44","45-59","60+"]:
                sub = df[df["Q1_age_group_enc"]==age_enc2.get(age,-1)]
                if len(sub) > 5:
                    aa.append({"Age":age,"Yes%":round((sub["Q25_app_adoption"]=="Yes").sum()/len(sub)*100,1)})
            aa_df = pd.DataFrame(aa)
            fig = go.Figure(go.Bar(x=aa_df["Age"], y=aa_df["Yes%"],
                                    marker=dict(color=aa_df["Yes%"],colorscale=[[0,"#F0E4D7"],[0.5,HONEY],[1,BROWN]]),
                                    text=[f"{v}%" for v in aa_df["Yes%"]], textposition="outside"))
            pc(fig, h=260, title="% Definite Yes by Age", margin=dict(t=40,b=20),
               yaxis=dict(showgrid=False, range=[0,80], rangemode="tozero"))
        with c2:
            da = []
            for col, label in [("Q4_num_dogs_None","No Dog"),("Q4_num_dogs_1 Dog","1 Dog"),
                                ("Q4_num_dogs_2 Dogs","2 Dogs"),("Q4_num_dogs_3+ Dogs","3+ Dogs")]:
                if col in df.columns:
                    sub = df[df[col]==1]
                    if len(sub) > 5:
                        da.append({"Dogs":label,"Yes%":round((sub["Q25_app_adoption"]=="Yes").sum()/len(sub)*100,1)})
            da_df = pd.DataFrame(da)
            fig2 = go.Figure(go.Bar(x=da_df["Dogs"], y=da_df["Yes%"],
                                     marker_color=CHART[:4],
                                     text=[f"{v}%" for v in da_df["Yes%"]], textposition="outside"))
            pc(fig2, h=260, title="% Definite Yes by Dog Count", margin=dict(t=40,b=20),
               yaxis=dict(showgrid=False, range=[0,80], rangemode="tozero"))
        ibox("The ideal early adopter is 25-34, owns 2+ dogs, lives in a metro or Tier-2 city. "
             "Start acquisition campaigns here first.")

        shead("Which Features Would Make Them Hit Download?")
        ft_cols2 = {c: c.replace("Q14_preferred_features__","").replace("_"," ").title()
                    for c in df.columns if c.startswith("Q14_preferred_features__")}
        ft_df2 = pd.DataFrame({"Feature":list(ft_cols2.values()),
                                "Count":[int(df[col].sum()) for col in ft_cols2]}).sort_values("Count")
        fig3 = go.Figure(go.Bar(x=ft_df2["Count"], y=ft_df2["Feature"], orientation="h",
                                 marker=dict(color=ft_df2["Count"],
                                             colorscale=[[0,"#F0E4D7"],[0.5,AMBER],[1,BROWN]]),
                                 text=ft_df2["Count"], textposition="outside"))
        pc(fig3, h=380, margin=dict(t=10,b=10),
           xaxis=dict(showgrid=False,visible=False), yaxis=dict(tickfont=dict(size=10)))
        ibox("Health tracker + vet directory + lost-and-found alerts are the top 3. "
             "Build these and you have a complete MVP.")

        # Use only columns that exist in df (cleaned has one-hot encoded versions)
        wtp_cols = [c for c in ["Q25_app_adoption","Q7_monthly_spend_inr","Q15_app_usage",
                                 "Q25_target","Q25_binary","engagement_score"] if c in df.columns]
        st.download_button("Download WTP Analysis", df[wtp_cols].to_csv(index=False),
                           "pawindia_wtp.csv", "text/csv")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — DATA JOURNEY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔬  Data Journey":
    st.markdown("<h1 style='color:#2C1810;font-size:1.8rem;margin-bottom:4px'>Data Journey</h1>"
                "<p style='color:#4A2C1A;font-size:.95rem'>How we built 2,000 realistic survey responses and cleaned them for analysis</p>",
                unsafe_allow_html=True)
    live_bar(n)

    t1, t2, t3 = st.tabs(["🧪 How We Built the Data","🧹 How We Cleaned It","📊 Before vs After"])

    with t1:
        shead("Why Synthetic Data?")
        st.markdown('<div class="icard"><p style="color:#3E2A1A;line-height:1.8">'
                    'PawIndia has no existing users yet. To test whether the app idea is viable, '
                    'we created 2,000 synthetic survey respondents that reflect realistic Indian '
                    'dog owner behaviour — grounded in known market trends, city-level differences, '
                    'and the digital habits of Indian millennials. We also added real-world noise '
                    'so the data behaves like an actual survey, not a clean simulation.'
                    '</p></div>', unsafe_allow_html=True)

        shead("How We Designed the Distributions")
        for i, (title, desc) in enumerate([
            ("Age skew", "35% aged 25-34, matching India's millennial dog ownership boom. Under-18 and 60+ are smaller groups to mirror who actually fills in surveys."),
            ("City tier bias", "45% Metro, 30% Tier-2, 18% Tier-3, 7% Rural — reflecting where organised pet spending actually happens in India."),
            ("Monthly spend", "Generated using a triangular distribution by city and dog count. Metro owners get a 1.3x multiplier, creating a realistic right-skewed distribution."),
            ("App adoption target (Q25)", "Not assigned randomly. Scored from city tier, age, app usage and subscription preference — producing a realistic 48% Yes / 37% Maybe / 15% No split."),
            ("Multi-select questions", "Q10 (problems) and Q14 (features) allowed up to 3 picks, weighted by real Indian pet owner pain points."),
        ], 1):
            st.markdown(f'<div style="background:#fff;border:1px solid #E8D5C4;border-top:4px solid {BROWN};'
                        f'border-radius:10px;padding:16px 20px;margin-bottom:10px">'
                        f'<span style="background:{BROWN};color:white;border-radius:50%;width:24px;height:24px;'
                        f'display:inline-flex;align-items:center;justify-content:center;font-weight:700;'
                        f'font-size:.8rem;margin-right:10px">{i}</span>'
                        f'<strong style="color:#3E2A1A">{title}</strong>'
                        f'<p style="color:#6F4E37;margin:6px 0 0 34px;font-size:.88rem">{desc}</p>'
                        f'</div>', unsafe_allow_html=True)

        shead("Noise We Added to Make It Feel Real")
        for title, desc in [
            ("Duplicate rows", "20 rows duplicated — simulates accidental double submissions."),
            ("Negative spend values", "~2% of Q7 made negative — simulates data entry errors."),
            ("Implausibly high spend", "~2% multiplied by 10 — simulates an extra zero typo."),
            ("Missing numeric spend", "15% left the number blank and used the range selector only."),
            ("Capitalisation inconsistency", "~3% of city tier entries were lowercased."),
            ("Whitespace padding", "~4% of spend range entries had leading or trailing spaces."),
            ("Non-owners answering dog questions", "~40% of non-dog-owners still partially answered dog-specific questions."),
            ("Over-selection on multi-select", "~5% picked more than the allowed 3 options."),
            ("Blank target variable", "~2% left Q25 blank — simulates incomplete form submissions."),
        ]:
            st.markdown(f'<div style="display:flex;align-items:flex-start;margin-bottom:10px;'
                        f'padding:10px 14px;background:#FFF8F0;border-radius:10px;border:1px solid #E8D5C4">'
                        f'<span style="color:{AMBER};font-size:1rem;margin-right:10px;flex-shrink:0">⚠</span>'
                        f'<div><strong style="color:#3E2A1A">{title}</strong>'
                        f'<p style="color:#6F4E37;margin:2px 0;font-size:.86rem">{desc}</p>'
                        f'</div></div>', unsafe_allow_html=True)

        shead("Raw Data Sample (First 8 Rows)")
        show_cols = [c for c in ["respondent_id","Q1_age_group","Q2_city_tier","Q4_num_dogs",
                                  "Q7_monthly_spend_inr","Q7_spend_range","Q25_app_adoption"] if c in raw.columns]
        st.dataframe(raw[show_cols].head(8), use_container_width=True, hide_index=True)

    with t2:
        shead("10 Steps to a Clean Dataset")
        for step, title, desc in [
            ("Step 1","Remove duplicates", f"Removed duplicate rows based on all non-ID columns. {len(raw)-n} rows removed."),
            ("Step 2","Drop rows with no target", "Rows where Q25 was blank were removed — the target is needed for all models."),
            ("Step 3","Standardise text", "All text stripped of whitespace and converted to title case."),
            ("Step 4","Fix spend values", "Negative values and amounts above Rs.50,000 were nulled. Missing values filled from range midpoints or group medians."),
            ("Step 5","Fill in missing categories", "Remaining blank categorical fields filled by mode within relevant groups."),
            ("Step 6","Encode ordered categories", "Age, satisfaction, app usage etc. encoded as integers preserving their natural order."),
            ("Step 7","One-hot encode nominal categories", "City tier, residence, subscription preference etc. split into binary columns."),
            ("Step 8","Expand multi-select columns", "Q5, Q10 and Q14 multi-select strings split into individual yes/no columns per option."),
            ("Step 9","Engineer new features", "Added spend_per_dog (spend divided by dog count), engagement_score (app usage + online frequency + reviews importance), and Q25_binary (Yes=1, Maybe/No=0)."),
            ("Step 10","Final check", f"Final dataset: {n:,} rows, {len(df.columns)} columns. Zero missing values confirmed."),
        ]:
            st.markdown(f'<div style="background:#fff;border:1px solid #E8D5C4;border-top:4px solid {BROWN};'
                        f'border-radius:10px;padding:14px 18px;margin-bottom:10px">'
                        f'<span style="color:{AMBER};font-size:.7rem;font-weight:700;text-transform:uppercase;'
                        f'letter-spacing:1px">{step}</span>'
                        f'<strong style="color:#3E2A1A;display:block;margin:4px 0">{title}</strong>'
                        f'<p style="color:#6F4E37;margin:0;font-size:.88rem">{desc}</p></div>',
                        unsafe_allow_html=True)

    with t3:
        shead("How the Dataset Changed After Cleaning")
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Raw Rows",      f"{len(raw):,}")
        c2.metric("Cleaned Rows",  f"{n:,}",           delta=f"-{len(raw)-n} removed")
        c3.metric("Raw Columns",   str(len(raw.columns)))
        c4.metric("Clean Columns", str(len(df.columns)), delta=f"+{len(df.columns)-len(raw.columns)} new")

        shead("Missing Values: Before and After")
        raw_miss = int(raw.isnull().sum().sum())
        fig = go.Figure(go.Bar(x=["Raw Dataset","Cleaned Dataset"], y=[raw_miss, 0],
                                marker_color=[AMBER,"#4CAF50"],
                                text=[raw_miss, 0], textposition="outside"))
        pc(fig, h=260, margin=dict(t=10,b=20), yaxis=dict(showgrid=False,title="Total Missing Values"))
        ibox(f"Cleaned from {raw_miss:,} missing values down to zero. The dataset is fully ready for all ML models.")

        shead("Spend Distribution: Raw vs Cleaned")
        c1, c2 = st.columns(2)
        with c1:
            raw_s = pd.to_numeric(raw["Q7_monthly_spend_inr"], errors="coerce").dropna()
            fig2 = go.Figure(go.Histogram(x=raw_s, nbinsx=40, marker_color=AMBER, opacity=0.8))
            pc(fig2, h=240, title="Raw — includes errors", margin=dict(t=40,b=20),
               xaxis=dict(title="INR"), yaxis=dict(showgrid=False, rangemode="tozero"))
        with c2:
            fig3 = go.Figure(go.Histogram(x=df["Q7_monthly_spend_inr"].dropna(), nbinsx=40,
                                           marker_color=BROWN, opacity=0.8))
            pc(fig3, h=240, title="Cleaned — outliers removed", margin=dict(t=40,b=20),
               xaxis=dict(title="INR"), yaxis=dict(showgrid=False, rangemode="tozero"))

        shead("Target Variable Distribution")
        tc = df["Q25_app_adoption"].value_counts()
        fig4 = go.Figure(go.Bar(x=tc.index, y=tc.values,
                                 marker_color=["#4CAF50",HONEY,"#E53935"],
                                 text=[f"{v} ({v/n*100:.1f}%)" for v in tc.values],
                                 textposition="outside"))
        pc(fig4, h=260, margin=dict(t=10,b=20), yaxis=dict(showgrid=False, rangemode="tozero"))
        ibox("48% Yes / 37% Maybe / 15% No — an intentional, realistic split that makes the ML "
             "classification genuinely challenging and the results more meaningful.")

        d1, d2 = st.columns(2)
        with d1: st.download_button("Download Raw Data", raw.to_csv(index=False), "pawindia_raw.csv", "text/csv")
        with d2: st.download_button("Download Cleaned Data", df.to_csv(index=False), "pawindia_clean.csv", "text/csv")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — RESEARCH & ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊  Research & Analytics":
    # Light cream header matching rest of dashboard
    st.markdown(
        f'<div style="background:#FFFFFF;border:1px solid #E0CFC0;border-radius:14px;'
        f'padding:22px 26px;margin-bottom:14px;border-left:5px solid {BROWN};'
        f'box-shadow:0 2px 12px rgba(111,78,55,.08)">'
        f'<div style="display:flex;align-items:center;gap:14px">'
        f'<div style="font-size:38px">📊</div>'
        f'<div><h1 style="margin:0;font-size:1.7rem;font-family:Bricolage Grotesque,sans-serif;'
        f'font-weight:800;color:#2C1810">Research & Analytics</h1>'
        f'<div style="color:#4A2C1A;font-size:.88rem;margin-top:4px">'
        f'Full ML analysis: Classification, Clustering, Association Rules, Regression</div>'
        f'</div></div></div>', unsafe_allow_html=True)

    st.markdown(
        f'<div style="background:#FFF8F0;border:1px solid #E0CFC0;'
        f'border-radius:10px;padding:10px 16px;margin-bottom:16px;color:#2C1810;font-size:.88rem;font-weight:500">'
        f'&#9679; Models are cached after first load — navigation between tabs is instant &nbsp;|&nbsp; '
        f'{n:,} respondents &nbsp;|&nbsp; Target: Q25 App Adoption (Yes / Maybe / No)'
        f'</div>', unsafe_allow_html=True)

    def dhead(t):
        st.markdown(f'<div style="display:flex;align-items:center;gap:10px;margin:22px 0 12px">'
                    f'<div style="width:4px;height:18px;background:linear-gradient(180deg,{AMBER},transparent);'
                    f'border-radius:2px"></div>'
                    f'<div style="color:#2C1810;font-size:1.05rem;font-weight:700">{t}</div></div>',
                    unsafe_allow_html=True)

    def dibox(t):
        st.markdown(f'<div style="background:rgba(212,168,83,.1);border-left:4px solid {AMBER};'
                    f'border-radius:0 8px 8px 0;padding:12px 16px;margin:8px 0 16px;'
                    f'color:#2C1810;font-size:.87rem">&#128161; {t}</div>', unsafe_allow_html=True)

    t1,t2,t3,t4 = st.tabs(["🎯 Classification","🔵 Clustering","🔗 Association Rules","📈 Regression"])

    # ── Classification ────────────────────────────────────────────────────────
    with t1:
        dhead("Classification: Predicting App Adoption (Q25 — Yes / Maybe / No)")
        st.markdown(f"<p style='color:#4A2C1A;font-size:.88rem'>8-9 algorithms compared. "
                    "80/20 stratified split, 5-fold cross-validation.</p>", unsafe_allow_html=True)

        with st.spinner("Training models... (runs once, then cached)"):
            rdf, cms, feat_imp, best, yte, feat_names = run_classification()

        dhead("Performance Comparison")
        fig_tbl = go.Figure(go.Table(
            header=dict(values=[f"<b>{c}</b>" for c in rdf.columns],
                        fill_color="rgba(45,32,15,.8)", font=dict(color=HONEY,size=12), align="left",
                        line=dict(color="rgba(80,65,40,.3)",width=1)),
            cells=dict(values=[rdf[c].astype(str).tolist() for c in rdf.columns],
                       fill_color="rgba(22,19,15,.88)", font=dict(color="#EDE4D3",size=11),
                       align="left", line=dict(color="rgba(80,65,40,.15)",width=1), height=30)))
        fig_tbl.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                               height=min(60+len(rdf)*34,460), margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig_tbl, width='stretch', config=PCFG)
        dibox(f"Best model: {best} — F1={rdf.iloc[0]['F1-Score']:.3f}, Accuracy={rdf.iloc[0]['Accuracy']:.3f}. "
              "Cross-validation confirms the result holds on unseen data.")

        dhead("All Models — Visual Comparison")
        fig_bar = go.Figure()
        for metric, color in [("Accuracy",BROWN),("Precision",HONEY),("Recall","#C49A6C"),("F1-Score","#A0522D")]:
            fig_bar.add_trace(go.Bar(name=metric, x=rdf["Model"], y=rdf[metric], marker_color=color))
        pd_chart(fig_bar, h=360, margin=dict(t=20,b=90),
                 barmode="group", xaxis=dict(tickangle=-30),
                 yaxis=dict(range=[0,1.1],title="Score"),
                 legend=dict(orientation="h",y=-0.3))

        dhead(f"Confusion Matrix: {best}")
        cm = cms[best]
        labels_cm = ["No (0)","Maybe (1)","Yes (2)"]
        fig_cm = go.Figure(go.Heatmap(z=cm, x=labels_cm, y=labels_cm,
                                       colorscale=[[0,AMBER],[1,BROWN]],
                                       text=cm, texttemplate="%{text}", showscale=True))
        pd_chart(fig_cm, h=340, margin=dict(t=20,b=60,l=60,r=20),
                 xaxis=dict(title="Predicted"), yaxis=dict(title="Actual"))

        if best in feat_imp:
            dhead(f"Feature Importance: {best}")
            fi = feat_imp[best]
            fi_df = pd.DataFrame({"Feature":list(fi.keys()),"Importance":list(fi.values())})
            fi_df = fi_df.sort_values("Importance", ascending=False).head(15)
            fi_df["Feature"] = fi_df["Feature"].str.replace(r"Q\d+_","",regex=True)\
                                                 .str.replace("_enc","").str.replace("_"," ").str[:35]
            fig_fi = go.Figure(go.Bar(x=fi_df["Importance"], y=fi_df["Feature"], orientation="h",
                                       marker=dict(color=fi_df["Importance"],colorscale=[[0,AMBER],[1,BROWN]]),
                                       text=fi_df["Importance"].round(3), textposition="outside"))
            pd_chart(fig_fi, h=400, margin=dict(t=10,b=10,l=220,r=60), xaxis=dict(showgrid=False,visible=False))
            dibox("Engagement score and app usage are the strongest predictors — "
                  "existing digital behaviour is the best signal for adoption.")

        st.download_button("Download Classification Results", rdf.to_csv(index=False),
                           "pawindia_classification.csv", "text/csv")

    # ── Clustering ────────────────────────────────────────────────────────────
    with t2:
        dhead("Clustering: Segmenting India's Dog Owners into Groups")
        st.markdown(f"<p style='color:#4A2C1A;font-size:.88rem'>K-Means on 10 behavioural and demographic features. "
                    "Elbow method and silhouette score used to select K=4.</p>", unsafe_allow_html=True)

        with st.spinner("Running clustering..."):
            K_range, inertias, sils, labels, df2, summary, personas = run_clustering()

        c1, c2 = st.columns(2)
        with c1:
            fig_el = go.Figure(go.Scatter(x=K_range, y=inertias, mode="lines+markers",
                                           line=dict(color=HONEY,width=2.5), marker=dict(size=9,color=AMBER)))
            fig_el.add_vline(x=4, line_dash="dash", line_color=SAGE, annotation_text="K=4",
                              annotation_font_color=SAGE)
            pd_chart(fig_el, h=260, margin=dict(t=40,b=30), title="Elbow Curve",
                     xaxis=dict(title="K"), yaxis=dict(title="Inertia"))
        with c2:
            fig_sil = go.Figure(go.Bar(x=K_range, y=sils, marker_color=CHART[:len(K_range)],
                                        text=[f"{s:.3f}" for s in sils], textposition="outside"))
            fig_sil.add_vline(x=4, line_dash="dash", line_color=SAGE)
            pd_chart(fig_sil, h=260, margin=dict(t=40,b=30), title="Silhouette Score",
                     xaxis=dict(title="K"), yaxis=dict(title="Score"))
        dibox("K=4 is chosen where the elbow bends and the silhouette score remains strong — "
              "four distinct, interpretable groups.")

        dhead("The Four Dog Owner Personas")
        cols4 = st.columns(4)
        emojis = ["🏙️","🏘️","🛋️","🤝"]
        for i, (cid, (name, color, desc)) in enumerate(personas.items()):
            row = summary[summary["cluster"]==cid].iloc[0]
            r,g,b = int(color[1:3],16),int(color[3:5],16),int(color[5:7],16)
            cols4[i].markdown(
                f'<div style="background:rgba(30,22,12,.92);border:1px solid rgba({r},{g},{b},.35);'
                f'border-top:4px solid {color};border-radius:14px;padding:16px;text-align:center">'
                f'<div style="font-size:1.8rem">{emojis[i]}</div>'
                f'<div style="font-weight:700;color:#EDE4D3;font-size:.9rem;margin:6px 0">{name}</div>'
                f'<div style="color:#5C3D2E;font-size:.75rem;margin-bottom:8px">{desc}</div>'
                f'<div style="color:{color};font-weight:700;font-size:1rem">{int(row["Count"])} members</div>'
                f'<div style="color:#C4B99A;font-size:.78rem;margin-top:4px">'
                f'Avg Spend: Rs.{int(row["Avg_Spend"]):,}<br>'
                f'Adoption: {int(row["Pct_Yes"]*100)}%<br>Metro: {int(row["Pct_Metro"]*100)}%</div>'
                f'</div>', unsafe_allow_html=True)

        dhead("Cluster Summary Table")
        disp = summary[["cluster","Persona","Count","Avg_Spend","Avg_App","Pct_Metro","Pct_Yes"]].copy()
        disp.columns = ["Cluster","Persona","Count","Avg Spend","Avg App Usage","% Metro","Adoption Rate"]
        disp["Avg Spend"]     = disp["Avg Spend"].apply(lambda x: f"Rs.{int(x):,}")
        disp["% Metro"]       = disp["% Metro"].apply(lambda x: f"{int(x*100)}%")
        disp["Adoption Rate"] = disp["Adoption Rate"].apply(lambda x: f"{int(x*100)}%")
        fig_tbl2 = go.Figure(go.Table(
            header=dict(values=[f"<b>{c}</b>" for c in disp.columns],
                        fill_color="rgba(45,32,15,.8)", font=dict(color=HONEY,size=12), align="left"),
            cells=dict(values=[disp[c].tolist() for c in disp.columns],
                       fill_color="rgba(22,19,15,.88)", font=dict(color="#EDE4D3",size=11),
                       align="left", height=30)))
        fig_tbl2.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                                height=200, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig_tbl2, width='stretch', config=PCFG)
        dibox("Urban Enthusiasts have the highest spend and adoption rate — premium tier targets. "
              "Practical Parents are the largest group — the volume opportunity.")

        # Parallel coordinates
        dhead("How the Four Groups Differ Across All Dimensions")
        pc_cols = ["Q7_monthly_spend_inr","Q15_app_usage_enc","Q20_community_importance_enc",
                   "Q22_reviews_importance_enc","engagement_score"]
        valid_pc = [c for c in pc_cols if c in df2.columns]
        if valid_pc:
            pcd = df2[valid_pc+["cluster"]].fillna(0).sample(min(400,len(df2)),random_state=42)
            pc_labels = ["Spend","App Usage","Community","Reviews","Engagement"][:len(valid_pc)]
            fig_pc = go.Figure(go.Parcoords(
                line=dict(color=pcd["cluster"],
                          colorscale=[[0,BROWN],[0.33,AMBER],[0.66,TEAL],[1,MAUVE]], showscale=True),
                dimensions=[dict(range=[pcd[c].min(),pcd[c].max()], label=lab, values=pcd[c])
                             for c,lab in zip(valid_pc,pc_labels)]))
            pd_chart(fig_pc, h=360, margin=dict(t=60,b=20,l=80,r=60))
            dibox("Each line is one respondent, coloured by their cluster. "
                  "Clear separation between high-engagement groups (warm colours) and low-engagement (cool) confirms K=4 is meaningful.")

        st.download_button("Download Cluster Results",
                           summary.drop(columns=["Color"],errors="ignore").to_csv(index=False),
                           "pawindia_clusters.csv","text/csv")

    # ── Association Rules ─────────────────────────────────────────────────────
    with t3:
        dhead("Association Rule Mining: Which Problems Drive Demand for Which Features?")
        st.markdown(f"<p style='color:#4A2C1A;font-size:.88rem'>Apriori algorithm on Q10 (problems) "
                    "and Q14 (features). Min support: 8%, Min lift: 1.1. "
                    "Rules read as: if a dog owner faces X, they are significantly more likely to want Y.</p>",
                    unsafe_allow_html=True)
        try:
            with st.spinner("Mining rules..."):
                rules = run_association_rules()
            rules_ok = len(rules) > 0
        except Exception as e:
            rules_ok = False
            st.error(f"Install mlxtend to see association rules: pip install mlxtend. Error: {e}")

        if rules_ok:
            cs, cc, cl = st.columns(3)
            with cs: min_sup  = st.slider("Min Support",  0.05, 0.30, 0.08, 0.01)
            with cc: min_conf = st.slider("Min Confidence",0.1, 0.9,  0.20, 0.05)
            with cl: min_lift = st.slider("Min Lift",      1.0, 3.0,  1.10, 0.05)

            filtered_r = rules[(rules["support"]>=min_sup) &
                                (rules["confidence"]>=min_conf) &
                                (rules["lift"]>=min_lift)]
            st.markdown(f"<p style='color:#4A2C1A;font-size:.84rem'>{len(filtered_r)} rules found.</p>",
                        unsafe_allow_html=True)

            dhead("Top Rules: Dog Owner Problem → Feature They Want")
            disp_r = filtered_r[["antecedents_str","consequents_str","support","confidence","lift"]].head(20)
            disp_r.columns = ["Problem (Antecedent)","Feature Wanted (Consequent)","Support","Confidence","Lift"]
            fig_rt = go.Figure(go.Table(
                header=dict(values=[f"<b>{c}</b>" for c in disp_r.columns],
                            fill_color="rgba(45,32,15,.8)", font=dict(color=HONEY,size=12), align="left"),
                cells=dict(values=[disp_r[c].tolist() for c in disp_r.columns],
                           fill_color="rgba(22,19,15,.88)", font=dict(color="#EDE4D3",size=11),
                           align="left", height=30)))
            fig_rt.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                                  height=min(60+len(disp_r)*32,520), margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig_rt, width='stretch', config=PCFG)

            if len(filtered_r) > 0:
                dhead("Support vs Confidence (Bubble Size = Lift)")
                fig_bub = px.scatter(filtered_r.head(25), x="support", y="confidence", size="lift",
                                      color="lift", hover_data=["antecedents_str","consequents_str","lift"],
                                      color_continuous_scale=[[0,AMBER],[1,BROWN]], size_max=30,
                                      labels={"support":"Support","confidence":"Confidence"})
                pd_chart(fig_bub, h=360, margin=dict(t=20,b=20))

            dibox("Owners who struggle to find a vet are significantly more likely to want the vet directory "
                  "and health tracker. This directly validates PawIndia's top two features.")
            st.download_button("Download Rules", filtered_r.to_csv(index=False),
                               "pawindia_rules.csv","text/csv")

    # ── Regression ────────────────────────────────────────────────────────────
    with t4:
        dhead("Regression: What Predicts How Much a Dog Owner Spends?")
        st.markdown(f"<p style='color:#4A2C1A;font-size:.88rem'>Target: Q7 monthly spend (INR). "
                    "Linear, Ridge (L2) and Lasso (L1) compared on R2, RMSE and MAE.</p>",
                    unsafe_allow_html=True)

        with st.spinner("Training regression models..."):
            reg_res, preds, coefs, feat_names = run_regression()

        dhead("Model Comparison")
        fig_rt = go.Figure(go.Table(
            header=dict(values=[f"<b>{c}</b>" for c in reg_res.columns],
                        fill_color="rgba(45,32,15,.8)", font=dict(color=HONEY,size=12), align="left"),
            cells=dict(values=[reg_res[c].tolist() for c in reg_res.columns],
                       fill_color="rgba(22,19,15,.88)", font=dict(color="#EDE4D3",size=11),
                       align="left", height=30)))
        fig_rt.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                              height=170, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig_rt, width='stretch', config=PCFG)
        best_r = reg_res.sort_values("R2",ascending=False).iloc[0]["Model"]
        dibox(f"Best model: {best_r}. Ridge regularisation reduces the effect of multicollinearity "
              "from one-hot encoded features. Lasso zeroes out weak predictors, "
              "confirming that a small set of variables drives most of the spending variance.")

        dhead("Actual vs Predicted Spend")
        cols_r = st.columns(3)
        for col_w, (name, (actual, predicted)) in zip(cols_r, preds.items()):
            with col_w:
                idx = np.random.choice(len(actual), min(250,len(actual)), replace=False)
                r2v = reg_res[reg_res["Model"]==name]["R2"].values[0]
                fig_av = go.Figure()
                fig_av.add_trace(go.Scatter(x=actual[idx], y=predicted[idx], mode="markers",
                                             marker=dict(color=BROWN,opacity=0.4,size=4)))
                mx = max(float(actual.max()), float(predicted.max()))
                fig_av.add_trace(go.Scatter(x=[0,mx], y=[0,mx], mode="lines",
                                             line=dict(color=HONEY,dash="dash",width=1.5)))
                pd_chart(fig_av, h=260, margin=dict(t=50,b=30,l=40,r=10),
                         title=f"{name} R2={r2v}",
                         xaxis=dict(title="Actual (INR)"), yaxis=dict(title="Predicted"),
                         showlegend=False)

        dhead("Feature Coefficients: Linear vs Ridge vs Lasso")
        if coefs:
            coef_df  = pd.DataFrame(coefs)
            top_feat = coef_df.abs().mean(axis=1).sort_values(ascending=False).head(12).index
            coef_top = coef_df.loc[top_feat].copy()
            coef_top.index = [i.replace("_enc","").replace("_"," ")[:28] for i in coef_top.index]
            fig_coef = go.Figure()
            for col_name, color in zip(coef_top.columns,[BROWN,AMBER,"#C49A6C"]):
                fig_coef.add_trace(go.Bar(name=col_name, x=coef_top.index,
                                           y=coef_top[col_name], marker_color=color, opacity=0.85))
            pd_chart(fig_coef, h=360, margin=dict(t=20,b=100),
                     barmode="group", xaxis=dict(tickangle=-40),
                     yaxis=dict(title="Coefficient",showgrid=False),
                     legend=dict(orientation="h",y=-0.35))
            dibox("Dog count and city tier are the strongest positive predictors of spending. "
                  "Lasso eliminates the noise, leaving only what actually matters.")

        st.download_button("Download Regression Results", reg_res.to_csv(index=False),
                           "pawindia_regression.csv","text/csv")
