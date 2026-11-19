
# Supply Chain Risk Prediction - Project Workflow

## 1. Project Overview

The Supply Chain Risk Prediction project uses data science and machine learning techniques to analyze shipment performance and predict the risk of late delivery.

The project workflow consists of data understanding, preprocessing, exploratory analysis, feature engineering, model development, evaluation, explainability, SQL analysis, and dashboard development.

## 2. End-to-End Workflow

### Step 1: Dataset Collection

- Source: DataCo Smart Supply Chain Dataset.
- Original records: 180,519.
- Historical period: 2015–2018.
- Data format: CSV.

### Step 2: Dataset Understanding

- Inspected dataset dimensions and column names.
- Identified numerical and categorical features.
- Examined data types and missing values.
- Understood delivery status categories.

### Step 3: Data Cleaning

- Removed the Product Description column because it was entirely missing.
- Excluded Order Zipcode because of its high missing-value percentage.
- Checked remaining missing values.
- Prepared the cleaned dataset for analysis.

### Step 4: Exploratory Data Analysis

Analyzed:

- Delivery status distribution.
- Shipping mode performance.
- Customer segment performance.
- Regional shipment performance.
- Monthly delivery trends.
- Scheduled shipment duration.

### Step 5: Feature Engineering

Selected relevant features for model development and created a binary target:

- `1` = Late delivery
- `0` = Not late delivery

Canceled shipments were excluded from the prediction dataset.

### Step 6: Data Preprocessing

- Applied median imputation to numerical features.
- Applied one-hot encoding to categorical features.
- Applied standard scaling to numerical features.
- Used a preprocessing pipeline to maintain consistent transformations.

### Step 7: Model Training

- Algorithm: XGBoost Classifier.
- Used grouped train-validation-test splitting based on Order Id.
- Trained the model using selected shipment features.
- Saved the trained model as `best_model.pkl`.

### Step 8: Model Evaluation

Evaluated the model using:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion matrix

The selected prediction threshold was 0.40.

### Step 9: Model Explainability

Used SHAP TreeExplainer to understand feature contributions.

The analysis identified Shipping Mode - First Class and scheduled shipment duration as the most influential features.

### Step 10: SQL Analysis

Created a SQLite database and performed business analysis using SQL queries.

Analyzed delivery performance, shipping modes, customer segments, and regional trends.

### Step 11: Dashboard Development

Developed an interactive Streamlit dashboard with four pages:

1. Overview
2. Delivery Analysis
3. Risk Prediction
4. Model Insights

### Step 12: Documentation

Prepared project documentation, including:

- README
- EDA summary
- Model evaluation report
- Feature importance report
- SQL analysis report
- Business recommendations
- Project limitations and future scope

## 3. Final Project Outputs

| Component        | Output                         |
| ---------------- | ------------------------------ |
| Dataset          | Cleaned supply chain dataset   |
| EDA              | Data analysis notebooks        |
| Machine Learning | Trained XGBoost model          |
| Preprocessing    | Saved preprocessor             |
| Explainability   | SHAP analysis                  |
| SQL              | SQLite database and queries    |
| Dashboard        | Streamlit application          |
| Reports          | Project analysis documentation |

## 4. Conclusion

The project follows an end-to-end data science workflow, transforming historical shipment records into meaningful analytical insights and late-delivery risk predictions. It combines data analysis, machine learning, SQL, explainable AI, and interactive visualization in one application.
