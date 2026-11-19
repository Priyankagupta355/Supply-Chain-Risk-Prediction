# 📦 Supply Chain Risk Prediction & Analytics

An end-to-end Machine Learning and Interactive Analytics project designed to analyze historical supply chain operations and identify patterns associated with late deliveries.

The project combines data preprocessing, exploratory data analysis, machine learning, model evaluation, explainable AI, and an interactive Streamlit dashboard.

## 🚀 Project Overview

Supply chain delays can affect customer satisfaction, logistics efficiency, and business performance.

This project analyzes historical shipment data to understand delivery performance, identify high-risk shipment patterns, and explore the factors associated with late deliveries.

It also provides an interactive analytics dashboard where users can explore shipment trends, regional performance, shipping modes, and delivery risks.

## ✨ Key Features

### 1. Data Processing

- Data cleaning and preprocessing
- Missing value analysis
- Duplicate record analysis
- Feature selection
- Data quality checks

### 2. Exploratory Data Analysis

- Delivery status distribution
- Regional shipment analysis
- Shipping mode performance
- Monthly delivery trends
- Late delivery patterns

### 3. Machine Learning

- XGBoost classification model
- Feature preprocessing pipeline
- Categorical encoding
- Numerical feature scaling
- Group-based train, validation, and test splitting

### 4. Model Evaluation

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion matrix

### 5. Explainable AI

- SHAP feature importance
- Model interpretation
- Identification of influential shipment features

### 6. Interactive Streamlit Dashboard

- Executive Overview
- Delivery Analytics
- Regional Analysis
- Shipping Analysis
- Risk Intelligence
- Ad-hoc Analysis
- Data Explorer

### 7. Data Exploration

- Global filters
- Search and sorting
- Missing value analysis
- Data quality summary
- CSV and Excel export

## 🛠️ Technology Stack

| Category         | Technologies                |
| ---------------- | --------------------------- |
| Programming      | Python                      |
| Data Processing  | Pandas, NumPy               |
| Visualization    | Matplotlib, Seaborn, Plotly |
| Machine Learning | Scikit-learn, XGBoost       |
| Explainable AI   | SHAP                        |
| Dashboard        | Streamlit                   |
| Development      | Jupyter Notebook, VS Code   |
| Version Control  | Git, GitHub                 |

## 📊 Dataset

**Dataset:** DataCo Smart Supply Chain Dataset

The project uses historical supply chain records containing shipment, customer, order, product, and delivery information.

- Records: 180,519
- Historical period: 2015–2018
- Cleaned dataset: 180,519 records
- Prediction target: Late delivery classification

Note: The dataset represents historical operations and does not provide live shipment tracking.

## 📈 Model Performance

The evaluated XGBoost model achieved the following test results:

| Metric    |  Score |
| --------- | -----: |
| Accuracy  | 64.61% |
| Precision | 66.82% |
| Recall    | 76.46% |
| F1-Score  | 71.32% |
| ROC-AUC   | 73.92% |

These results represent performance on the held-out test set using the selected classification threshold.

The model is an experimental analytical model and requires further validation before production deployment.

## 🏗️ Project Structure

```text
Supply_Chain_Risk_Prediction/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   └── visualization/
│
├── dashboard/
│   ├── app.py
│   ├── components/
│   ├── pages/
│   └── styles/
│
├── models/
│   └── best_model.pkl
│
├── reports/
│
├── tests/
│
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Priyankagupta355/Supply-Chain-Risk-Prediction.git
```

### 2. Navigate to project directory

```bash
cd Supply-Chain-Risk-Prediction
```

### 3. Create virtual environment

```bash
python -m venv venv
```

### 4. Activate environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Install Excel export dependency

```bash
pip install openpyxl
```

### 7. Run the dashboard

```bash
streamlit run dashboard/app.py
```

## 📌 Important Notes

- The cleaned dataset and trained model must be available at their expected project paths.
- Large dataset files may need to be downloaded separately.
- Model performance is based on historical data.
- SHAP explanations describe model behavior, not causal relationships.
- The dashboard's historical risk indicators are not live predictions.

## 🔮 Future Improvements

- Real-time shipment data integration
- Improved model generalization
- Advanced risk monitoring
- Automated model retraining
- Deployment through a cloud platform
- API integration for shipment risk analysis

## 👩‍💻 Author

**Priyanka Gupta**

B.Tech – Artificial Intelligence & Data Science

GitHub: [Priyankagupta355](https://github.com/Priyankagupta355)

---

⭐ If you find this project interesting, consider giving it a star!
