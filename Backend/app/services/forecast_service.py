from sqlalchemy.orm import Session

from app.ml.feature_engineering import build_features
from app.ml.predictor import predict
from app.schemas.forecast import ForecastRequest, ForecastResponse
from fastapi import HTTPException
import joblib


def forecast_product(db: Session, request: ForecastRequest) -> ForecastResponse:
    # Build feature vector (may raise ValueError for insufficient history)
    features = build_features(db, request.product_id, request.target_date)

    try:
        predicted_units = predict(features)
    except FileNotFoundError as exc:
        # model artifact missing
        raise HTTPException(status_code=503, detail=f"Model artifact not found: {exc}")
    except joblib.externals.loky.process_executor.TerminatedWorkerError:
        raise HTTPException(status_code=503, detail="Model failed to predict")

    return ForecastResponse(
        product_id=request.product_id,
        target_date=request.target_date,
        predicted_units_sold=predicted_units,
        history_days_used=7,
        feature_columns=list(features.keys()),
    )
