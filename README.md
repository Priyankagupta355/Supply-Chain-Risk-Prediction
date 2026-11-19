

# Supply Chain Risk Prediction System

An end-to-end Machine Learning project that analyzes
supply chain delivery performance and predicts the risk
of late shipments using historical shipment data.

## Project Overview

The Supply Chain Risk Prediction System helps analyze
historical delivery patterns, identify shipment risk
factors, and predict whether a shipment is likely to
experience late delivery.

The project combines data analytics, SQL, machine
learning, explainable AI, and an interactive Streamlit
dashboard.

## Problem Statement

Late deliveries can negatively affect customer
satisfaction, logistics operations, and supply chain
efficiency.

This project uses historical shipment information to:

- Analyze delivery performance.
- Identify high-risk shipping patterns.
- Understand factors associated with late deliveries.
- Predict potential late-delivery risk.
- Present insights through an interactive dashboard.

## Dataset

**Dataset:** DataCo Smart Supply Chain Dataset

**Source:** Kaggle

https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis

Dataset details:

- Original records: 180,519
- Cleaned records: 180,519
- Historical data period: 2015–2018
- Cleaned dataset columns: 51

Canceled shipments were excluded from delivery
prediction and evaluation.

## Technologies Used

### Programming

- Python
- SQL

### Data Analysis

- Pandas
- NumPy
- Matplotlib
- Seaborn

### Machine Learning

- Scikit-learn
- XGBoost

### Explainable AI

- SHAP

### Dashboard

- Streamlit
- Plotly

### Model Management

- Joblib

## Project Workflow

1. Data Collection
2. Data Cleaning
3. Exploratory Data Analysis
4. SQL-Based Analysis
5. Feature Selection
6. Feature Preprocessing
7. Model Training
8. Model Evaluation
9. SHAP Explainability
10. Interactive Dashboard Development

## Machine Learning Model

**Algorithm:** XGBoost Classifier

Selected input features:

- Shipping Mode
- Days for shipment (scheduled)
- Customer Segment
- Market
- Order Region
- Department Name
- Category Name
- Order Item Quantity
- Order Item Discount
- Order Item Discount Rate
- Order Item Product Price

Target Variable:

- 1 = Late Delivery
- 0 = Not Late Delivery

Canceled shipments are excluded from the modeling dataset.

## Model Performance

Evaluation was performed using a grouped test split
to reduce data leakage between shipment orders.

| Metric    |  Score |
| --------- | -----: |
| Accuracy  | 64.61% |
| Precision | 66.82% |
| Recall    | 76.46% |
| F1 Score  | 71.32% |
| ROC-AUC   | 73.92% |

Classification threshold: 0.40

## Explainable AI - SHAP

SHAP was used to understand the features influencing
model predictions.

Important features identified:

1. Shipping Mode - First Class
2. Scheduled Shipping Days
3. Shipping Mode - Second Class
4. Shipping Mode - Standard Class
5. Order Item Discount

SHAP importance represents model associations and
does not establish causation.

## Dashboard Modules

The Streamlit dashboard contains four modules:

### 1. Overview

- Shipment KPIs
- Delivery status distribution
- Monthly delivery trends
- Regional performance

### 2. Delivery Analysis

- Shipping mode analysis
- Regional delivery performance
- Customer segment analysis
- Department-level insights
- Interactive filters

### 3. Risk Prediction

- Shipment information input
- Predicted late-delivery probability
- High-risk and lower-risk classification
- Operational recommendations

### 4. Model Insights

- Model evaluation metrics
- Confusion matrix
- SHAP feature importance
- Prediction threshold analysis

## Project Structure

Supply_Chain_Risk_Prediction/
│
├── dashboard/
│   ├── app.py
│   ├── pages/
│   │   ├── 1_Overview.py
│   │   ├── 2_Delivery_Analysis.py
│   │   ├── 3_Risk_Prediction.py
│   │   └── 4_Model_Insights.py
│   └── components/
│       └── charts.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
│
├── models/
│   ├── best_model.pkl
│   └── preprocessor.pkl
│
├── notebooks/
├── reports/
├── sql/
├── src/
├── tests/
├── README.md
└── requirements.txt

## Installation and Setup

### 1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL

### 2. Navigate to project directory

cd Supply_Chain_Risk_Prediction

### 3. Create virtual environment

python -m venv venv

### 4. Activate virtual environment

Windows:

venv\Scripts\activate

### 5. Install dependencies

pip install -r requirements.txt

### 6. Run Streamlit dashboard

streamlit run dashboard/app.py

## Important Notes

- The project uses historical shipment data from
  2015–2018.
- Predictions are based on learned historical patterns.
- The model is a portfolio/research prototype and is
  not validated for production deployment.
- Model performance can vary on new operational data.
- False positives and false negatives remain limitations.

## Future Improvements

- Improve model performance through hyperparameter tuning.
- Evaluate additional machine learning algorithms.
- Add real-time shipment tracking integration.
- Develop automated risk alerts.
- Deploy the dashboard online.
- Monitor model performance and data drift.

## Author

Priyanka Gupta

B.Tech - Artificial Intelligence and Data Science
