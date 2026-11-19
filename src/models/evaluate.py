
"""
Model evaluation utilities for Supply Chain Risk Prediction.
"""

import numpy as np
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)


def evaluate_model(
    model,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    threshold: float = 0.40
) -> dict:
    """Evaluate a trained classification pipeline."""

    if not 0 <= threshold <= 1:
        raise ValueError("Threshold must be between 0 and 1.")

    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= threshold).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1]
    ).ravel()

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(
            y_test, predictions, zero_division=0
        ),
        "recall": recall_score(
            y_test, predictions, zero_division=0
        ),
        "f1_score": f1_score(
            y_test, predictions, zero_division=0
        ),
        "roc_auc": roc_auc_score(y_test, probabilities),
        "specificity": (
            tn / (tn + fp) if (tn + fp) > 0 else 0.0
        ),
        "true_negative": int(tn),
        "false_positive": int(fp),
        "false_negative": int(fn),
        "true_positive": int(tp),
        "threshold": threshold,
    }

    return metrics


def get_confusion_matrix(
    y_true,
    y_pred
) -> pd.DataFrame:
    """Return confusion matrix as a labeled DataFrame."""

    matrix = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1]
    )

    return pd.DataFrame(
        matrix,
        index=["Actual Not Late", "Actual Late"],
        columns=["Predicted Not Late", "Predicted Late"]
    )


def get_classification_report(
    y_true,
    y_pred
) -> pd.DataFrame:
    """Return detailed classification report."""

    report = classification_report(
        y_true,
        y_pred,
        output_dict=True,
        zero_division=0
    )

    return pd.DataFrame(report).transpose()


def get_metrics_summary(metrics: dict) -> pd.DataFrame:
    """Convert evaluation metrics into a readable table."""

    return pd.DataFrame([
        {"Metric": key, "Value": value}
        for key, value in metrics.items()
    ])
