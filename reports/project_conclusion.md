
# Project Conclusion

## 1. Introduction

The Supply Chain Risk Prediction project was developed to analyze historical shipment data, identify delivery performance patterns, and predict the risk of late deliveries using machine learning.

The project combines data science, SQL, machine learning, explainable AI, and interactive visualization.

## 2. Work Completed

The following activities were completed during the project:

1. Collected and explored the DataCo Smart Supply Chain dataset.
2. Performed data cleaning and preprocessing.
3. Conducted exploratory data analysis to identify shipment patterns.
4. Analyzed delivery performance across shipping modes, customer segments, and regions.
5. Created relevant features for late-delivery prediction.
6. Trained an XGBoost classification model.
7. Evaluated model performance using standard classification metrics.
8. Applied SHAP for model explainability.
9. Created a SQLite database for SQL-based business analysis.
10. Developed an interactive Streamlit dashboard.
11. Prepared technical documentation and business reports.

## 3. Model Results

The final XGBoost model achieved the following grouped test results:

| Metric    |  Score |
| --------- | -----: |
| Accuracy  | 64.61% |
| Precision | 66.82% |
| Recall    | 76.46% |
| F1-Score  | 71.32% |
| ROC-AUC   | 73.92% |

The model uses a prediction threshold of 0.40.

These results indicate useful predictive capability, although further optimization is required before production use.

## 4. Key Project Findings

- The dataset contains 180,519 original shipment records.
- Late delivery represents the largest delivery-status category.
- The late-delivery rate among valid non-canceled shipments is 57.29%.
- First Class shipping recorded a 100% late-delivery rate.
- Shipping mode and scheduled shipment duration were the most influential features in the SHAP analysis.
- Regional and monthly analysis revealed variations in delivery performance.

## 5. Technical Achievements

The project demonstrates practical implementation of:

- Python programming.
- Pandas and NumPy for data manipulation.
- Scikit-learn for preprocessing and evaluation.
- XGBoost for classification.
- SHAP for explainable AI.
- SQL and SQLite for structured analysis.
- Streamlit and Plotly for interactive dashboards.
- Git and GitHub for version control.

## 6. Business Value

The system demonstrates how historical shipment data can be transformed into useful operational insights.

It can support:

- Identification of potentially risky shipments.
- Monitoring of delivery performance.
- Comparison of shipping modes.
- Regional performance analysis.
- Data-driven shipment planning.

## 7. Limitations

The project uses historical data from 2015–2018 and does not include real-time logistics information.

The model also produces false positive and false negative predictions. Therefore, its output should be used as decision support rather than a guaranteed prediction.

## 8. Future Scope

Possible improvements include:

- Real-time shipment tracking.
- Integration with external logistics APIs.
- Advanced model optimization.
- Automated risk notifications.
- Cloud deployment.
- Model monitoring and retraining.

## 9. Final Conclusion

The Supply Chain Risk Prediction project demonstrates an end-to-end data science workflow, from dataset understanding and exploratory analysis to machine learning, explainability, SQL analysis, and dashboard development.

The project provides a foundation for data-driven supply chain risk analysis and demonstrates the practical application of machine learning to a real-world business problem.
