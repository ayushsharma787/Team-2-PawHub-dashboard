# PawIndia Dashboard

**India's Dog Owner Market Research Dashboard**

A Streamlit-powered analytics dashboard built to validate the PawIndia business idea — a super-app for dog owners across India. The dashboard combines market research insights, simulated location data, and end-to-end machine learning analysis to answer one core question: will Indian dog owners pay for a centralised pet care platform?

---

## Dashboard Pages

| Page | What It Shows |
|---|---|
| Home | Key stats, business context, top challenges |
| Know Your City | Simulated dog-friendly places (vets, parks, cafes, grooming) across 6 Indian cities |
| Dog Owner Insights | EDA across demographics, spending, pain points, and digital behaviour |
| Will They Buy? | Subscription preferences, adoption likelihood by city and profile, feature demand |
| Data Journey | Synthetic data generation methodology, noise injected, full cleaning pipeline |
| Research & Analytics | Classification (8 models), Clustering (K-Means), Association Rules (Apriori), Regression (Linear, Ridge, Lasso) |

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/pawindia-dashboard.git
cd pawindia-dashboard
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

---

## Deploy on Streamlit Cloud (Free)

1. Push the entire folder to a **public GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click **New App**
5. Select your repository, set branch to `main`, and set **Main file path** to `app.py`
6. Click **Deploy** — Streamlit Cloud installs `requirements.txt` automatically

---

## Project Structure

```
pawindia_dashboard/
│
├── app.py                          # Main entry point and sidebar navigation
│
├── data/
│   ├── pawindia_raw_data.csv       # Synthetic raw survey data (2,020 rows, with noise)
│   └── pawindia_cleaned_data.csv   # Cleaned and transformed data (1,966 rows, 109 cols)
│
├── utils/
│   ├── theme.py                    # Brand colours, logo SVG, shared CSS
│   ├── ml_engine.py                # All ML models with st.cache_data caching
│   └── city_data.py                # Simulated pet-friendly place data for 6 cities
│
├── pages/
│   ├── p01_home.py                 # Landing page
│   ├── p02_know_your_city.py       # Location and places map
│   ├── p03_dog_owner_insights.py   # EDA and descriptive analytics
│   ├── p04_will_they_buy.py        # Willingness to pay analysis
│   ├── p05_data_journey.py         # Data generation and cleaning story
│   └── p06_research_analytics.py  # Full ML analysis (academic requirements)
│
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## Data

### Raw Dataset (`pawindia_raw_data.csv`)
2,020 rows of synthetic survey data mimicking realistic Indian dog owner responses. Includes deliberate noise: duplicate rows, negative spend values, missing fields, capitalisation inconsistencies, and over-selection on multi-choice questions.

### Cleaned Dataset (`pawindia_cleaned_data.csv`)
1,966 rows, 109 columns. Duplicates removed, outliers nulled, missing values imputed, all categorical variables encoded, multi-select questions expanded into binary flags, and derived features engineered (spend_per_dog, engagement_score).

---

## ML Models Included

**Classification (Target: Q25 App Adoption)**
Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, AdaBoost, SVM, KNN, Naive Bayes — with accuracy, precision, recall, F1-score and cross-validation comparison.

**Clustering**
K-Means with elbow curve and silhouette score analysis. K=4 selected, producing four dog owner personas: Urban Enthusiast, Practical Parent, Casual Companion, Community Seeker.

**Association Rule Mining**
Apriori algorithm on Q10 (pain points) and Q14 (feature preferences). Shows which challenges drive demand for which features. Interactive support/confidence/lift sliders.

**Regression (Target: Q7 Monthly Spend)**
Linear Regression, Ridge (L2), and Lasso (L1) with R2, RMSE, MAE comparison and coefficient visualisation.

---

## Replacing Simulated Data With Real Data

The `utils/city_data.py` file contains the simulated places. To replace with live data:

1. Get a Google Places API key from [console.cloud.google.com](https://console.cloud.google.com)
2. Replace the `PLACES` list in `city_data.py` with an API call to:
   `https://maps.googleapis.com/maps/api/place/nearbysearch/json`
3. Filter by `type=veterinary_care`, `type=park`, or keyword `dog cafe`

Alternatively, use the free OpenStreetMap Overpass API:
```
https://overpass-api.de/api/interpreter?data=[amenity=veterinary]
```

---

## Academic Context

Built as part of a market research and analytics project for PawIndia, submitted to the course instructor. Survey instrument: PawIndia Dog Owner Survey (25 questions). Analytics framework: CRISP-DM with Lean Startup Validation overlay.

---

## Brand

**PawIndia** — Connecting Every Dog and Their Human Across India

Colours: Coffee Brown `#6F4E37` | Amber `#D4860B` | Cream `#FFF8F0`
