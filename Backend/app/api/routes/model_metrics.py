import json
from pathlib import Path
from fastapi import APIRouter

from app.schemas.model_metrics import ModelMetrics

router = APIRouter()

SHAP_PATH = Path(__file__).parent.parent.parent / "ml" / "artifacts" / "shap_importance.json"

# Hardcoded from the held-out test set evaluation run in the shap_analysis notebook
MAE = 0.4767
WAPE = 0.3622


@router.get("/", response_model=ModelMetrics)
def get_model_metrics():
    with open(SHAP_PATH) as f:
        importance = json.load(f)

    return ModelMetrics(
        mae=MAE,
        wape=WAPE,
        feature_importance=importance,
    )

