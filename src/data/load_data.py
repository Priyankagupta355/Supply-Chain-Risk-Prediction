
from pathlib import Path

import pandas as pd


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Default cleaned dataset path
DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "supply_chain_cleaned.csv"
)


def load_data(file_path=None):
    """
    Load the cleaned supply chain dataset.

    Parameters
    ----------
    file_path : str or Path, optional
        Custom CSV file path.

    Returns
    -------
    pandas.DataFrame
        Loaded supply chain dataset.
    """

    path = Path(file_path) if file_path else DATA_PATH

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {path}\n"
            "Please check the dataset location."
        )

    try:
        df = pd.read_csv(path)

        if df.empty:
            raise ValueError("The dataset is empty.")

        print("Dataset loaded successfully!")
        print(f"File: {path.name}")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")

        return df

    except pd.errors.ParserError as error:
        raise ValueError(
            f"Unable to parse the CSV file: {error}"
        ) from error


def get_dataset_info(df):
    """
    Display basic information about the dataset.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    print("\nDataset Information")
    print("-" * 40)

    print(f"Shape: {df.shape}")
    print(f"Total Rows: {len(df)}")
    print(f"Total Columns: {len(df.columns)}")

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    return df.describe(include="all")


def validate_dataset(df, required_columns=None):
    """
    Validate the dataset and check required columns.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if df.empty:
        raise ValueError("Dataset contains no records.")

    if required_columns:
        missing_columns = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

    print("Dataset validation successful!")

    return True
