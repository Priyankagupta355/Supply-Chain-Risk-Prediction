
"""
Unit tests for model evaluation utilities.
"""

import numpy as np
import pandas as pd
import pytest

from src.models.evaluate import (
    evaluate_model,
    get_confusion_matrix,
    get_classification_report,
    get_metrics_summary,
)


class DummyEvaluationModel:
    """Mock classifier for testing evaluation metrics."""

    def predict_proba(self, X):
        return np.array([
            [0.90, 0.10],
            [0.20, 0.80],
            [0.70, 0.30],
            [0.10, 0.90],
        ])


@pytest.fixture
def evaluation_data():
    X_test = pd.DataFrame({
        "feature": [1, 2, 3, 4]
    })

    y_test = pd.Series([0, 1, 0, 1])

    return X_test, y_test


def test_evaluate_model(evaluation_data):
    X_test, y_test = evaluation_data

    metrics = evaluate_model(
        DummyEvaluationModel(),
        X_test,
        y_test,
        threshold=0.40
    )

    assert metrics["accuracy"] == 1.0
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["f1_score"] == 1.0
    assert metrics["roc_auc"] == 1.0
    assert metrics["specificity"] == 1.0


def test_confusion_matrix():
    y_true = [0, 1, 0, 1]
    y_pred = [0, 1, 1, 1]

    matrix = get_confusion_matrix(y_true, y_pred)

    assert matrix.shape == (2, 2)
    assert matrix.iloc[0, 0] == 1
    assert matrix.iloc[0, 1] == 1
    assert matrix.iloc[1, 0] == 0
    assert matrix.iloc[1, 1] == 2


def test_classification_report():
    y_true = [0, 1, 0, 1]
    y_pred = [0, 1, 1, 1]

    report = get_classification_report(y_true, y_pred)

    assert "precision" in report.columns
    assert "recall" in report.columns
    assert "f1-score" in report.columns


def test_metrics_summary():
    metrics = {
        "accuracy": 0.85,
        "precision": 0.80,
        "recall": 0.90,
    }

    summary = get_metrics_summary(metrics)

    assert len(summary) == 3
    assert "Metric" in summary.columns
    assert "Value" in summary.columns


def test_invalid_threshold(evaluation_data):
    X_test, y_test = evaluation_data

    with pytest.raises(ValueError):
        evaluate_model(
            DummyEvaluationModel(),
            X_test,
            y_test,
            threshold=1.5
        )
