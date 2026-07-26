from pydantic import BaseModel
from typing import List


class FeatureImportance(BaseModel):
    feature: str
    importance: float


class ModelMetrics(BaseModel):
    mae: float
    wape: float
    feature_importance: List[FeatureImportance]
