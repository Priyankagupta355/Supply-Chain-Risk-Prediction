
"""
Unit tests for shipment risk prediction.
"""

import pandas as pd
import pytest

from src.models.predict import (
    predict_risk,
    predict_single_shipment,
)


class DummyModel:
    """Mock model for testing prediction functions."""

    def predict_proba(self, X):
        return [
            [0.80, 0.20],
            [0.30, 0.70],
            [0.55, 0.45],
        ]


@pytest.fixture
def sample_shipments():
    return pd.DataFrame({
        "Shipping Mode": [
            "Standard Class",
            "First Class",
            "Second Class",
        ],
        "Days for shipment (scheduled)": [4, 2, 3],
        "Customer Segment": [
            "Consumer",
            "Corporate",
            "Home Office",
        ],
        "Market": ["USCA", "Europe", "LATAM"],
        "Order Region": [
            "Central America",
            "Western Europe",
            "South America",
        ],
        "Department Name": [
            "Fan Shop",
            "Apparel",
            "Fitness",
        ],
        "Category Name": [
            "Sporting Goods",
            "Women's Apparel",
            "Fitness Accessories",
        ],
        "Order Item Quantity": [2, 1, 3],
        "Order Item Discount": [10.0, 5.0, 15.0],
        "Order Item Discount Rate": [0.1, 0.05, 0.15],
        "Order Item Product Price": [50.0, 100.0, 75.0],
    })


def test_predict_risk(sample_shipments):
    model = DummyModel()

    result = predict_risk(
        sample_shipments,
        model=model,
        threshold=0.40
    )

    assert len(result) == 3
    assert "Late_Delivery_Probability" in result.columns
    assert "Predicted_Target" in result.columns
    assert "Risk_Level" in result.columns


def test_risk_classification(sample_shipments):
    result = predict_risk(
        sample_shipments,
        model=DummyModel(),
        threshold=0.40
    )

    assert result["Predicted_Target"].tolist() == [0, 1, 1]
    assert result["Risk_Level"].tolist() == [
        "Low Risk",
        "High Risk",
        "High Risk",
    ]


def test_probability_range(sample_shipments):
    result = predict_risk(
        sample_shipments,
        model=DummyModel()
    )

    probabilities = result["Late_Delivery_Probability"]

    assert probabilities.between(0, 1).all()


def test_invalid_threshold(sample_shipments):
    with pytest.raises(ValueError):
        predict_risk(
            sample_shipments,
            model=DummyModel(),
            threshold=1.5
        )


def test_predict_single_shipment(sample_shipments):
    shipment = sample_shipments.iloc[0].to_dict()

    result = predict_single_shipment(
        shipment,
        model=DummyModel()
    )

    assert "probability" in result
    assert "prediction" in result
    assert "risk_level" in result
    assert result["risk_level"] == "Low Risk"
