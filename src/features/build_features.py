
"""
Feature engineering utilities for Supply Chain Risk Prediction.
"""

import pandas as pd


SELECTED_FEATURES = [
    "Shipping Mode",
    "Days for shipment (scheduled)",
    "Customer Segment",
    "Market",
    "Order Region",
    "Department Name",
    "Category Name",
    "Order Item Quantity",
    "Order Item Discount",
    "Order Item Discount Rate",
    "Order Item Product Price",
]

NUMERICAL_FEATURES = [
    "Days for shipment (scheduled)",
    "Order Item Quantity",
    "Order Item Discount",
    "Order Item Discount Rate",
    "Order Item Product Price",
]

CATEGORICAL_FEATURES = [
    "Shipping Mode",
    "Customer Segment",
    "Market",
    "Order Region",
    "Department Name",
    "Category Name",
]


def validate_features(df: pd.DataFrame) -> None:
    """Check whether all required model features exist."""
    missing_features = [
        feature for feature in SELECTED_FEATURES
        if feature not in df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )


def select_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return only the selected model features."""
    validate_features(df)
    return df[SELECTED_FEATURES].copy()


def separate_feature_types(df: pd.DataFrame):
    """Separate numerical and categorical model features."""
    features = select_features(df)

    numerical = features[NUMERICAL_FEATURES].copy()
    categorical = features[CATEGORICAL_FEATURES].copy()

    return numerical, categorical


def get_feature_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Generate a summary of selected model features."""
    features = select_features(df)

    summary = pd.DataFrame({
        "Feature": features.columns,
        "Data_Type": [
            str(features[column].dtype)
            for column in features.columns
        ],
        "Missing_Values": [
            features[column].isnull().sum()
            for column in features.columns
        ],
        "Unique_Values": [
            features[column].nunique()
            for column in features.columns
        ]
    })

    return summary
