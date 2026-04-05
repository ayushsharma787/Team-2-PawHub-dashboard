# PawIndia Market Research Dashboard

**Validating India's first super-app for dog owners — built on survey data from 2,000 respondents across India.**

---

## What This Dashboard Does

PawIndia is a proposed mobile app that brings together everything a dog owner in India needs in one place — nearby vets, dog parks, cafes, grooming services, a health tracker, and a community of fellow dog parents. This dashboard was built to answer one central question:

> **Do Indian dog owners face enough real problems that they would actually download and pay for an app like this?**

The dashboard presents findings from a synthetic survey of 2,000 Indian dog owners, designed to mirror realistic behaviour, spending patterns, and digital habits. It is built for two audiences simultaneously — a dog owner who wants to understand what the app offers, and a researcher or founder who wants to validate the business case with data.

---

## Pages at a Glance

| Page | What It Shows |
|---|---|
| **Home** | Key stats, adoption rings, top pain points, spend vs adoption signal |
| **Know Your City** | India map showing dog-friendly vets, parks, cafes and grooming in 6 cities |
| **Dog Owner Insights** | Who they are, what they spend, what problems they have, how digital they are |
| **Will They Buy?** | Conversion funnel, subscription preferences, adoption by city and profile |
| **Data Journey** | How the synthetic data was generated, noise injected, and cleaned |
| **Research & Analytics** | Full ML analysis — classification, clustering, association rules, regression |

---

## Files in This Repository

```
app.py                      — Complete dashboard (single file, dark theme)
pawindia_raw_data.csv       — Synthetic raw survey data (2,020 rows, with noise)
pawindia_cleaned_data.csv   — Cleaned and ML-ready dataset (1,966 rows, 109 columns)
requirements.txt            — Python dependencies
README.md                   — This file
```

---

## How to Run Locally

**Step 1 — Clone the repository**
```bash
git clone https://github.com/your-username/pawindia-dashboard.git
cd pawindia-dashboard
```

**Step 2 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3 — Run the app**
```bash
streamlit run app.py
```

The dashboard opens at `http://localhost:8501`

---

## Python Version

This dashboard is tested and compatible with **Python 3.8 through 3.11**. Python 3.11.8 is recommended for stability on Streamlit Cloud.

All string formatting uses `.format()` instead of f-strings for maximum compatibility. No walrus operators or other 3.10+ syntax is used.

---

## How to Deploy on Streamlit Cloud (Free)

1. Push all files to a **public GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New App**
4. Select your repository, set branch to `main`, set **Main file path** to `app.py`
5. Click **Deploy** — Streamlit Cloud installs `requirements.txt` automatically
6. Optionally set the Python version to `3.11` in Streamlit Cloud's Advanced settings

The app should be live within 2 to 3 minutes.

---

## About the Data

### Why Synthetic?

PawIndia is a new product with no existing user base. To validate the business idea, we generated 2,000 synthetic survey respondents that reflect realistic Indian dog owner behaviour, grounded in known market trends, city-level spending differences, and the digital habits of Indian millennials.

### Raw Dataset

2,020 rows of survey responses with deliberate real-world noise injected — duplicate entries, negative spend values from data entry errors, missing fields, capitalisation inconsistencies, and respondents who partially answered questions they should have skipped.

### Cleaned Dataset

1,966 rows, 109 columns. Duplicates removed, outliers nulled, missing values imputed, categorical variables encoded, multi-select questions expanded into binary flags, and three derived features added: `spend_per_dog`, `engagement_score`, and `Q25_binary`.

### Target Variable Distribution

| Outcome | Count | Share |
|---|---|---|
| Would download (Yes) | 946 | 48.1% |
| Open to trying (Maybe) | 727 | 37.0% |
| Would not download (No) | 293 | 14.9% |

---

## Machine Learning Models

### Classification — Predicting App Adoption (Q25)

Nine algorithms compared on accuracy, precision, recall, F1-score, and 5-fold cross-validation accuracy.

| Model | Notes |
|---|---|
| Logistic Regression | Baseline linear classifier |
| Decision Tree | Interpretable, depth-limited |
| Random Forest | Ensemble, balanced class weights |
| Gradient Boosting | Sequential boosting |
| AdaBoost | Adaptive boosting |
| SVM | RBF kernel, probability estimates |
| KNN | Distance-weighted, k=7 |
| Naive Bayes | Gaussian, fast baseline |
| XGBoost | High-performance gradient boosting |

### Clustering — Dog Owner Segments

K-Means with elbow and silhouette analysis. K=4 selected, producing four personas: Urban Enthusiast, Practical Parent, Casual Companion, Community Seeker.

### Association Rule Mining — Pain Points to Feature Demand

Apriori algorithm on Q10 (challenges) and Q14 (preferred features). Rules show which problems drive demand for which app features.

### Regression — Predicting Monthly Spend

Linear, Ridge (L2), and Lasso (L1) regression on Q7 (monthly dog spend). Evaluated on R², RMSE, and MAE with 5-fold cross-validation.

---

## Analytics Framework

This project follows a **CRISP-DM** structure overlaid with a **Lean Startup Validation** approach.

- Business Understanding — Why PawIndia, what gap it fills, what we are trying to prove
- Data Understanding — Survey design, synthetic generation, noise analysis
- Data Preparation — Cleaning pipeline, encoding, feature engineering
- Modelling — All four ML technique categories
- Evaluation — Performance metrics, business interpretation of results
- Deployment — Streamlit Cloud dashboard as the delivery medium

---

## Brand

**PawIndia** — Connecting Every Dog and Their Human Across India

| Element | Value |
|---|---|
| Primary accent | Amber `#D4A853` |
| Secondary accent | Honey `#E8C36A` |
| Background | Deep brown `#0D0A06` |
| Surface | Warm dark `#1A1209` |
| Body text | Cream `#EDE4D3` |
| Font | Plus Jakarta Sans |

---

## Design & Accessibility Notes

- Full dark theme with WCAG AA compliant contrast ratios across all text and UI elements
- Pie chart labels rendered outside slices to avoid dark-on-dark readability issues
- Heatmap cell text uses bright cream for readability on both light and dark cells
- Sidebar navigation text meets 4.5:1 contrast minimum
- Simulated place data is clearly marked with a distinct warning callout (red border) to prevent confusion with real data
- Adaptive column layouts — place cards adjust column count to match result count

---

## Known Limitations

- All place data in the Know Your City page is **simulated**. At launch, this would connect to the Google Places API or OpenStreetMap's Overpass API for real locations
- The survey data is synthetic. Results reflect the distributions and correlations we designed, not real user responses
- Association rule mining requires `mlxtend`. If it is not installed, the rules tab shows a fallback message

---

## Replacing Simulated Places With Real Data

The places data lives at the top of `app.py` in the `PLACES` list. To replace it with live data:

**Google Places API**
```python
import requests
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
params = {"location": "12.9716,77.5946", "radius": 5000,
          "type": "veterinary_care", "key": "YOUR_API_KEY"}
response = requests.get(url, params=params).json()
```

**OpenStreetMap (free, no key needed)**
```
https://overpass-api.de/api/interpreter?data=[amenity=veterinary](area[name="Bengaluru"]);out;
```

Replace the `PLACES` list with the API response and the map updates automatically.

---

## Academic Context

Built as part of a market research and predictive analytics course project. Survey instrument: PawIndia Dog Owner Survey (25 questions across demographics, spending, pain points, feature preferences, and adoption likelihood). Submitted to course faculty for evaluation.

*All data is synthetic and generated for educational purposes only.*
