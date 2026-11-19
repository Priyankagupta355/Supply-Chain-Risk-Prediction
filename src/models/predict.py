
"""
Prediction utilities for Supply Chain Risk Prediction.
"""

from pathlib import Path
import joblib
import pandas as pd

from src.features.build_features import select_features


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "best_model.pkl"

DEFAULT_THRESHOLD = 0.40


def load_model(model_path: str | Path = MODEL_PATH):
    """Load the saved machine learning pipeline."""
    model_path = Path(model_path)

    if not model_path.exists():
        raise FileNotFoundError(
            f"Trained model not found: {model_path}"
        )

    return joblib.load(model_path)


def predict_risk(
    data: pd.DataFrame,
    model=None,
    threshold: float = DEFAULT_THRESHOLD
) -> pd.DataFrame:
    """
    Predict late-delivery probability and risk classification.

    Target:
        1 = Late delivery
        0 = Not late delivery
    """
    if not 0 <= threshold <= 1:
        raise ValueError("Threshold must be between 0 and 1.")

    if model is None:
        model = load_model()

    features = select_features(data)

    probabilities = model.predict_proba(features)[:, 1]
    predictions = (probabilities >= threshold).astype(int)

    results = data.copy()
    results["Late_Delivery_Probability"] = probabilities
    results["Predicted_Target"] = predictions
    results["Risk_Level"] = [
        "High Risk" if prediction == 1 else "Low Risk"
        for prediction in predictions
    ]

    return results


def predict_single_shipment(
    shipment: dict,
    model=None,
    threshold: float = DEFAULT_THRESHOLD
) -> dict:
    """Predict risk for one shipment."""
    shipment_df = pd.DataFrame([shipment])

    result = predict_risk(
        shipment_df,
        model=model,
        threshold=threshold
    )

    return {
        "probability": float(
            result["Late_Delivery_Probability"].iloc[0]
        ),
        "prediction": int(
            result["Predicted_Target"].iloc[0]
        ),
        "risk_level": result["Risk_Level"].iloc[0]
    }
