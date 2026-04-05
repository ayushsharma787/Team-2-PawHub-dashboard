# utils/ml_engine.py
# All ML logic lives here. Cached with st.cache_data so models run once per session.

import pandas as pd
import numpy as np
import streamlit as st

# ── Data loader ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    import os
    base = os.path.dirname(__file__)
    raw  = pd.read_csv(os.path.join(base, "pawindia_raw_data.csv"))
    clean= pd.read_csv(os.path.join(base, "pawindia_cleaned_data.csv"))
    return raw, clean


# ── Feature matrix builder ────────────────────────────────────────────────────
@st.cache_data
def build_feature_matrix():
    _, df = load_data()
    feature_cols = [
        "Q1_age_group_enc", "Q6_ownership_duration_enc",
        "Q7_monthly_spend_inr", "Q9_online_purchase_freq_enc",
        "Q13_pet_space_satisfaction_enc", "Q15_app_usage_enc",
        "Q20_community_importance_enc", "Q22_reviews_importance_enc",
        "Q24_emergency_vet_freq_enc", "engagement_score", "spend_per_dog",
        "Q2_city_tier_Metro", "Q2_city_tier_Tier-2", "Q2_city_tier_Rural",
        "Q4_num_dogs_1 Dog", "Q4_num_dogs_2 Dogs", "Q4_num_dogs_3+ Dogs",
        "Q17_location_sharing_Yes Always", "Q17_location_sharing_Yes When Using App",
        "Q18_subscription_pref_Freemium", "Q18_subscription_pref_Monthly Sub",
        "Q18_subscription_pref_Annual Sub", "Q18_subscription_pref_Would Not Pay",
        "Q19_adoption_interest_Yes Actively", "Q19_adoption_interest_Yes Considering",
        "Q21_social_media_dogs_Active", "Q21_social_media_dogs_Passive",
        "Q23_vax_tracking_Dedicated Pet App", "Q23_vax_tracking_Rely On Memory",
        "Q10_challenges__hard_to_find_reliable_vet",
        "Q10_challenges__no_pet_friendly_spaces",
        "Q10_challenges__losing_track_of_vaccinations",
        "Q14_preferred_features__health_vaccination_tracker",
        "Q14_preferred_features__nearby_vet_directory",
        "Q14_preferred_features__online_marketplace",
    ]
    valid = [c for c in feature_cols if c in df.columns]
    X = df[valid].fillna(0)
    y3 = df["Q25_target"].fillna(1).astype(int)
    y2 = df["Q25_binary"].fillna(0).astype(int)
    return X, y3, y2, valid


# ── Classification ────────────────────────────────────────────────────────────
@st.cache_data
def run_classification():
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.metrics import (accuracy_score, precision_score,
                                  recall_score, f1_score, confusion_matrix,
                                  classification_report)

    X, y3, y2, feat_names = build_feature_matrix()
    Xtr, Xte, ytr, yte = train_test_split(X, y3, test_size=0.2,
                                            random_state=42, stratify=y3)
    sc = StandardScaler()
    Xtr_s = sc.fit_transform(Xtr)
    Xte_s = sc.transform(Xte)

    models = {
        "Logistic Regression":   LogisticRegression(max_iter=500, random_state=42),
        "Decision Tree":         DecisionTreeClassifier(max_depth=6, random_state=42),
        "Random Forest":         RandomForestClassifier(n_estimators=100, random_state=42),
        "Gradient Boosting":     GradientBoostingClassifier(n_estimators=100, random_state=42),
        "AdaBoost":              AdaBoostClassifier(n_estimators=100, random_state=42),
        "SVM":                   SVC(kernel="rbf", probability=True, random_state=42),
        "KNN":                   KNeighborsClassifier(n_neighbors=7),
        "Naive Bayes":           GaussianNB(),
    }

    results = []
    cms = {}
    feat_imp = {}

    for name, model in models.items():
        use_scaled = name in ("Logistic Regression", "SVM", "KNN")
        Xtr_fit = Xtr_s if use_scaled else Xtr
        Xte_fit = Xte_s if use_scaled else Xte
        model.fit(Xtr_fit, ytr)
        pred = model.predict(Xte_fit)
        acc  = accuracy_score(yte, pred)
        prec = precision_score(yte, pred, average="weighted", zero_division=0)
        rec  = recall_score(yte, pred, average="weighted", zero_division=0)
        f1   = f1_score(yte, pred, average="weighted", zero_division=0)
        cv   = cross_val_score(model, Xtr_fit, ytr, cv=5,
                                scoring="accuracy").mean()
        results.append({"Model": name, "Accuracy": round(acc,3),
                         "Precision": round(prec,3), "Recall": round(rec,3),
                         "F1-Score": round(f1,3), "CV Accuracy": round(cv,3)})
        cms[name] = confusion_matrix(yte, pred)
        if hasattr(model, "feature_importances_"):
            feat_imp[name] = dict(zip(feat_names, model.feature_importances_))
        elif hasattr(model, "coef_"):
            imp = np.abs(model.coef_).mean(axis=0)
            feat_imp[name] = dict(zip(feat_names, imp))

    results_df = pd.DataFrame(results).sort_values("F1-Score", ascending=False)
    best_model  = results_df.iloc[0]["Model"]
    return results_df, cms, feat_imp, best_model, yte, feat_names


# ── Clustering ────────────────────────────────────────────────────────────────
@st.cache_data
def run_clustering():
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score

    _, df = load_data()
    cluster_cols = [
        "Q1_age_group_enc", "Q7_monthly_spend_inr",
        "Q9_online_purchase_freq_enc", "Q15_app_usage_enc",
        "Q20_community_importance_enc", "Q22_reviews_importance_enc",
        "engagement_score", "spend_per_dog",
        "Q2_city_tier_Metro", "Q2_city_tier_Tier-2",
        "Q4_num_dogs_1 Dog", "Q4_num_dogs_2 Dogs",
        "Q17_location_sharing_Yes Always",
        "Q18_subscription_pref_Freemium",
        "Q18_subscription_pref_Would Not Pay",
    ]
    valid = [c for c in cluster_cols if c in df.columns]
    X = df[valid].fillna(0)
    sc = StandardScaler()
    Xs = sc.fit_transform(X)

    # Elbow
    inertias, sil_scores = [], []
    K_range = range(2, 9)
    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(Xs)
        inertias.append(km.inertia_)
        sil_scores.append(silhouette_score(Xs, km.labels_))

    # Final model k=4
    km4 = KMeans(n_clusters=4, random_state=42, n_init=10)
    labels = km4.fit_predict(Xs)
    df2 = df.copy()
    df2["cluster"] = labels

    # Persona names based on profile
    persona_map = {
        0: ("Urban Enthusiast", "Metro, high spend, active app user, likely to adopt"),
        1: ("Practical Parent",  "Tier-2 city, moderate spend, functional needs"),
        2: ("Casual Companion",  "Any tier, low spend, passive engagement"),
        3: ("Community Seeker",  "Mixed cities, values community & reviews strongly"),
    }

    # Cluster summary
    summary = df2.groupby("cluster").agg(
        Count=("Q7_monthly_spend_inr","count"),
        Avg_Spend=("Q7_monthly_spend_inr","mean"),
        Avg_Age_Enc=("Q1_age_group_enc","mean"),
        Avg_App_Usage=("Q15_app_usage_enc","mean"),
        Avg_Community=("Q20_community_importance_enc","mean"),
        Pct_Metro=("Q2_city_tier_Metro","mean"),
        Pct_Yes=("Q25_binary","mean"),
    ).round(2).reset_index()
    summary["Persona"] = summary["cluster"].map(lambda x: persona_map[x][0])
    summary["Description"] = summary["cluster"].map(lambda x: persona_map[x][1])

    return (list(K_range), inertias, sil_scores, labels, df2,
            summary, cluster_cols[:8], persona_map)


# ── Association Rules ─────────────────────────────────────────────────────────
@st.cache_data
def run_association_rules():
    from mlxtend.frequent_patterns import apriori, association_rules

    _, df = load_data()
    challenge_cols = [c for c in df.columns if c.startswith("Q10_challenges__")]
    feature_cols   = [c for c in df.columns if c.startswith("Q14_preferred_features__")]
    basket = df[challenge_cols + feature_cols].fillna(0).astype(bool)

    freq   = apriori(basket, min_support=0.08, use_colnames=True)
    rules  = association_rules(freq, metric="lift", min_threshold=1.1)
    rules  = rules[
        rules["antecedents"].apply(lambda x: any("challenge" in i for i in x)) &
        rules["consequents"].apply(lambda x: any("feature"   in i for i in x))
    ].copy()

    def clean_label(s):
        s = str(s).replace("Q10_challenges__","").replace("Q14_preferred_features__","")
        return s.replace("_"," ").title()

    rules["antecedents_str"] = rules["antecedents"].apply(
        lambda x: ", ".join([clean_label(i) for i in x]))
    rules["consequents_str"] = rules["consequents"].apply(
        lambda x: ", ".join([clean_label(i) for i in x]))
    rules = rules.sort_values("lift", ascending=False).head(30)
    rules[["support","confidence","lift"]] = rules[["support","confidence","lift"]].round(3)
    return rules


# ── Regression ────────────────────────────────────────────────────────────────
@st.cache_data
def run_regression():
    from sklearn.linear_model import LinearRegression, Ridge, Lasso
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

    X, y3, y2, feat_names = build_feature_matrix()
    _, df = load_data()
    y_reg = df["Q7_monthly_spend_inr"].fillna(df["Q7_monthly_spend_inr"].median())
    y_reg = y_reg.iloc[:len(X)]

    Xtr, Xte, ytr, yte = train_test_split(X, y_reg, test_size=0.2, random_state=42)
    sc = StandardScaler()
    Xtr_s = sc.fit_transform(Xtr)
    Xte_s = sc.transform(Xte)

    models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression":  Ridge(alpha=1.0),
        "Lasso Regression":  Lasso(alpha=0.5, max_iter=5000),
    }
    results, preds, coefs = [], {}, {}
    for name, m in models.items():
        m.fit(Xtr_s, ytr)
        p   = m.predict(Xte_s)
        r2  = r2_score(yte, p)
        rmse= np.sqrt(mean_squared_error(yte, p))
        mae = mean_absolute_error(yte, p)
        cv  = cross_val_score(m, Xtr_s, ytr, cv=5, scoring="r2").mean()
        results.append({"Model": name, "R2": round(r2,3),
                         "RMSE": round(rmse,1), "MAE": round(mae,1),
                         "CV R2": round(cv,3)})
        preds[name] = (yte.values, p)
        coefs[name] = dict(zip(feat_names, m.coef_))

    return pd.DataFrame(results), preds, coefs, yte, feat_names
