
# Model Evaluation Report

## Supply Chain Risk Prediction System

### 1. Model Overview

The project uses an XGBoost Classifier to predict the probability of late delivery based on historical supply chain shipment data.

**Algorithm:** XGBoost Classifier
**Problem Type:** Binary Classification
**Target Variable:** Late Delivery Risk
**Selected Threshold:** 0.40

Target classes:

- 1 = Late Delivery
- 0 = Not Late Delivery

Canceled shipments were excluded from model evaluation.

### 2. Dataset Splitting Strategy

A group-based splitting strategy using Order ID was implemented to reduce data leakage.

The dataset was divided into:

- Training dataset
- Validation dataset
- Testing dataset

The group overlap between training, validation, and testing sets was zero.

This approach helps ensure that records belonging to the same order do not appear across multiple splits.

### 3. Model Configuration

The XGBoost model used the following configuration:

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

### 4. Evaluation Metrics

The final model was evaluated on the grouped test dataset.

| Metric    | Result |
| --------- | -----: |
| Accuracy  | 64.61% |
| Precision | 66.82% |
| Recall    | 76.46% |
| F1 Score  | 71.32% |
| ROC-AUC   | 73.92% |

### 5. Confusion Matrix

The confusion matrix obtained from the test dataset:

|                 | Predicted Not Late | Predicted Late |
| --------------- | -----------------: | -------------: |
| Actual Not Late |              7,062 |          7,488 |
| Actual Late     |              4,642 |         15,080 |

Interpretation:

- True Negative: 7,062
- False Positive: 7,488
- False Negative: 4,642
- True Positive: 15,080

### 6. Performance Interpretation

**Accuracy – 64.61%**

The model correctly classified approximately 64.61% of the test records.

**Precision – 66.82%**

Among shipments predicted as late, approximately 66.82% were actually late.

**Recall – 76.46%**

The model identified approximately 76.46% of the actual late-delivery records.

**F1 Score – 71.32%**

The F1 score represents the balance between precision and recall.

**ROC-AUC – 73.92%**

The ROC-AUC score indicates the model's ability to distinguish between late and non-late delivery classes.

### 7. Classification Threshold

The classification threshold was selected as 0.40 using validation data.

Prediction rules:

- Probability below 0.40: Not Late
- Probability equal to or above 0.40: Late

The selected threshold prioritizes detecting late deliveries while balancing false-positive predictions.

### 8. Model Limitations

The evaluation identified the following limitations:

1. False-positive predictions are relatively high.
2. Some actual late deliveries are incorrectly classified as not late.
3. The model uses historical data from 2015–2018.
4. The model has not been validated on live shipment data.
5. Performance may change when applied to new operational conditions.

### 9. Conclusion

The XGBoost model achieved a ROC-AUC score of 73.92% and recall of 76.46% on the grouped test dataset.

The results demonstrate useful predictive capability for historical shipment risk analysis.

Further optimization, external validation, and monitoring are necessary before production deployment.

**Project:** Supply Chain Risk Prediction System
**Algorithm:** XGBoost Classifier
**Evaluation Type:** Grouped Test Evaluation
**Author:** Priyanka Gupta
