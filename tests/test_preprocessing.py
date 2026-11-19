
"""
Unit tests for data preprocessing functions.
"""

import pandas as pd
import pytest

from src.data.preprocess import (
    remove_duplicates,
    remove_cancelled_shipments,
    create_target,
    handle_missing_values,
    preprocess_data,
)


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "Delivery Status": [
            "Late delivery",
            "Shipping on time",
            "Shipping canceled",
            "Late delivery",
        ],
        "Late_delivery_risk": [1, 0, 0, 1],
        "Order Item Quantity": [2, 3, 1, 2],
        "Customer Segment": [
            "Consumer",
            "Corporate",
            "Home Office",
            "Consumer",
        ],
    })


def test_remove_duplicates(sample_data):
    duplicated = pd.concat(
        [sample_data, sample_data.iloc[[0]]],
        ignore_index=True
    )

    result = remove_duplicates(duplicated)

    assert len(result) == len(sample_data)


def test_remove_cancelled_shipments(sample_data):
    result = remove_cancelled_shipments(sample_data)

    assert "Shipping canceled" not in (
        result["Delivery Status"].values
    )


def test_create_target(sample_data):
    result = create_target(sample_data)

    assert "Target" in result.columns
    assert result["Target"].tolist() == [1, 0, 0, 1]


def test_handle_missing_values():
    df = pd.DataFrame({
        "Quantity": [2, None, 4],
        "Category": ["A", None, "B"],
    })

    result = handle_missing_values(df)

    assert result.isnull().sum().sum() == 0


def test_preprocess_data(sample_data):
    result = preprocess_data(sample_data)

    assert "Target" in result.columns
    assert "Shipping canceled" not in (
        result["Delivery Status"].values
    )
    assert result.isnull().sum().sum() == 0
