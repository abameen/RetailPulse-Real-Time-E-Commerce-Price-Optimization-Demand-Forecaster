from pathlib import Path

import joblib

MODEL_PATH = Path(__file__).parent / "artifacts" / "lgbm_demand_forecaster.pkl"
FEATURE_COLUMNS = [
    "lag_1_price",
    "lag_3_price",
    "lag_7_price",
    "lag_1_units_sold",
    "lag_3_units_sold",
    "lag_7_units_sold",
    "rolling_7_mean_price",
    "rolling_7_std_price",
    "rolling_7_mean_units_sold",
    "rolling_7_std_units_sold",
    "day_of_week",
    "month",
    "is_weekend",
    "category_price_index",
]

_model = None


def _load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def predict(features: dict) -> float:
    model = _load_model()
    values = [features[name] for name in FEATURE_COLUMNS]
    prediction = model.predict([values])[0]
    return float(prediction)
