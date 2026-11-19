
"""
Unit tests for feature engineering functions.
"""

import pandas as pd
import pytest

from src.features.build_features import (
    SELECTED_FEATURES,
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES,
    select_features,
    validate_features,
    separate_feature_types,
    get_feature_summary,
)


@pytest.fixture
def sample_features():
    data = {}

    for column in NUMERICAL_FEATURES:
        data[column] = [1.0, 2.0, 3.0]

    for column in CATEGORICAL_FEATURES:
        data[column] = ["A", "B", "C"]

    return pd.DataFrame(data)


def test_selected_features_count():
    assert len(SELECTED_FEATURES) == 11


def test_select_features(sample_features):
    result = select_features(sample_features)

    assert list(result.columns) == SELECTED_FEATURES
    assert result.shape == (3, 11)


def test_validate_features(sample_features):
    assert validate_features(sample_features) is None


def test_missing_feature_error(sample_features):
    incomplete = sample_features.drop(
        columns=[SELECTED_FEATURES[0]]
    )

    with pytest.raises(ValueError):
        validate_features(incomplete)


def test_separate_feature_types(sample_features):
    numerical, categorical = separate_feature_types(
        sample_features
    )

    assert len(numerical.columns) == 5
    assert len(categorical.columns) == 6


def test_feature_summary(sample_features):
    summary = get_feature_summary(sample_features)

    assert len(summary) == 11
    assert "Feature" in summary.columns
    assert "Data_Type" in summary.columns
    assert "Missing_Values" in summary.columns
    assert "Unique_Values" in summary.columns
