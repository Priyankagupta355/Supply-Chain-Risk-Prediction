
"""
Data preprocessing utilities for the Supply Chain Risk Prediction project.
"""

import pandas as pd


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate records from the dataset."""
    return df.drop_duplicates().copy()


def remove_cancelled_shipments(
    df: pd.DataFrame,
    status_column: str = "Delivery Status"
) -> pd.DataFrame:
    """Remove canceled shipments from delivery-risk analysis."""
    if status_column not in df.columns:
        raise ValueError(f"Missing required column: {status_column}")

    return df[
        df[status_column].astype(str).str.lower() != "shipping canceled"
    ].copy()


def create_target(
    df: pd.DataFrame,
    target_column: str = "Late_delivery_risk"
) -> pd.DataFrame:
    """Create a binary target column named Target."""
    if target_column not in df.columns:
        raise ValueError(f"Missing required column: {target_column}")

    result = df.copy()
    result["Target"] = pd.to_numeric(
        result[target_column], errors="coerce"
    )

    result = result.dropna(subset=["Target"]).copy()
    result["Target"] = result["Target"].astype(int)

    return result


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values without modifying the original dataframe.
    Numeric columns use median; categorical columns use mode.
    """
    result = df.copy()

    for column in result.columns:
        if result[column].isnull().sum() == 0:
            continue

        if pd.api.types.is_numeric_dtype(result[column]):
            median_value = result[column].median()
            result[column] = result[column].fillna(median_value)
        else:
            mode_values = result[column].mode(dropna=True)

            if not mode_values.empty:
                result[column] = result[column].fillna(mode_values.iloc[0])
            else:
                result[column] = result[column].fillna("Unknown")

    return result


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Run the basic preprocessing pipeline."""
    result = remove_duplicates(df)
    result = remove_cancelled_shipments(result)
    result = create_target(result)
    result = handle_missing_values(result)

    return result
