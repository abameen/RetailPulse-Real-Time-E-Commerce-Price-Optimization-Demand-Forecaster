from pathlib import Path

import joblib

MODEL_PATH = Path(__file__).parent / "artifacts" / "lgbm_demand_forecaster.pkl"
_model = None


def _load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def predict(features: dict) -> float:
    model = _load_model()

    # Determine expected feature order from the model if possible
    try:
        expected = list(model.feature_name_)
    except Exception:
        # fallback to a small sensible default ordered list
        expected = list(features.keys())

    # Build the input vector by pulling values from features with defaults
    row = []
    for name in expected:
        if name in features:
            row.append(features[name])
        else:
            # default numeric replacement
            row.append(0.0)

    prediction = model.predict([row])[0]
    return float(prediction)
