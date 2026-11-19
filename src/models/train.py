
"""
Model training utilities for Supply Chain Risk Prediction.
"""

from pathlib import Path
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from xgboost import XGBClassifier

from src.features.build_features import (
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_ROOT / "models"


def create_preprocessor() -> ColumnTransformer:
    """Create preprocessing pipeline for numerical and categorical data."""

    numerical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numerical_pipeline, NUMERICAL_FEATURES),
        ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
    ])

    return preprocessor


def create_model() -> XGBClassifier:
    """Create XGBoost classifier with project configuration."""

    return XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="logloss",
        n_jobs=-1,
    )


def create_training_pipeline() -> Pipeline:
    """Combine preprocessing and XGBoost classifier."""

    pipeline = Pipeline(steps=[
        ("preprocessor", create_preprocessor()),
        ("classifier", create_model()),
    ])

    return pipeline


def train_model(
    X_train,
    y_train,
    save_path: str | Path | None = None
):
    """Train the pipeline and optionally save the trained model."""

    pipeline = create_training_pipeline()
    pipeline.fit(X_train, y_train)

    if save_path is not None:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(pipeline, save_path)

    return pipeline


def save_model(model, save_path: str | Path | None = None) -> Path:
    """Save a trained model pipeline."""

    if save_path is None:
        save_path = MODEL_DIR / "best_model.pkl"

    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, save_path)

    return save_path
