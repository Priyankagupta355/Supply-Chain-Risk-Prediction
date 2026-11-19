
# Model Selection and Comparison Report

## 1. Introduction

The objective of model development was to predict whether a shipment is likely to experience late delivery.

The project uses supervised binary classification with the XGBoost algorithm.

## 2. Problem Type

| Property              | Description           |
| --------------------- | --------------------- |
| Machine Learning Type | Supervised Learning   |
| Problem Type          | Binary Classification |
| Target Variable       | Target                |
| Positive Class        | Late Delivery (1)     |
| Negative Class        | Not Late Delivery (0) |
| Selected Algorithm    | XGBoost Classifier    |

Canceled shipments were excluded from model training and evaluation.

## 3. Selected Model: XGBoost

XGBoost (Extreme Gradient Boosting) is an ensemble learning algorithm based on gradient-boosted decision trees.

It builds multiple decision trees sequentially, where each new tree helps improve the predictions of the previous trees.

### Reasons for Selection

- Supports classification problems.
- Captures nonlinear relationships.
- Handles interactions between features.
- Works with numerical and encoded categorical features.
- Provides feature importance capabilities.
- Supports SHAP-based model explainability.

## 4. Model Configuration

The selected XGBoost model uses the following parameters:

| Parameter        |   Value |
| ---------------- | ------: |
| n_estimators     |     300 |
| max_depth        |       6 |
| learning_rate    |    0.05 |
| subsample        |     0.8 |
| colsample_bytree |     0.8 |
| random_state     |      42 |
| eval_metric      | logloss |
| n_jobs           |      -1 |

## 5. Data Splitting Strategy

The project uses GroupShuffleSplit based on Order Id.

This approach ensures that records belonging to the same order do not appear across training, validation, and testing datasets.

The overlap between groups was verified to be zero across all three splits.

## 6. Model Evaluation Results

The selected XGBoost model achieved the following grouped test results:

| Evaluation Metric |  Score |
| ----------------- | -----: |
| Accuracy          | 64.61% |
| Precision         | 66.82% |
| Recall            | 76.46% |
| F1-Score          | 71.32% |
| ROC-AUC           | 73.92% |

The prediction threshold selected using validation data was 0.40.

## 7. Model Performance Interpretation

- Accuracy measures the proportion of correct predictions.
- Precision measures how many predicted late deliveries were actually late.
- Recall measures how many actual late deliveries were detected.
- F1-score balances precision and recall.
- ROC-AUC measures the model's ability to distinguish between the two classes.

The recall score of 76.46% indicates that the model detected a substantial proportion of actual late deliveries.

However, the model also produced false positive predictions.

## 8. Model Limitations

- The model is trained on historical data from 2015–2018.
- False positives and false negatives remain significant.
- The model does not use live logistics information.
- Its predictions should not be treated as guaranteed delivery outcomes.
- Further validation and optimization are required before production deployment.

## 9. Conclusion

XGBoost was selected for its ability to model complex relationships in structured shipment data and support explainability through SHAP.

The evaluation results demonstrate useful predictive capability, although additional improvements are required for reliable real-world deployment.
