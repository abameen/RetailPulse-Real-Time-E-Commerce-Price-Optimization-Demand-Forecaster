from sqlalchemy.orm import Session

from app.ml.feature_engineering import build_features
from app.ml.predictor import predict
from app.schemas.forecast import ForecastRequest, ForecastResponse


def forecast_product(db: Session, request: ForecastRequest) -> ForecastResponse:
    features = build_features(db, request.product_id, request.target_date)
    predicted_units = predict(features)

    return ForecastResponse(
        product_id=request.product_id,
        target_date=request.target_date,
        predicted_units_sold=predicted_units,
        history_days_used=7,
        feature_columns=list(features.keys()),
    )
