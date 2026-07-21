from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.forecast import ForecastRequest, ForecastResponse
from app.services.forecast_service import forecast_product

router = APIRouter()


@router.post("/predict", response_model=ForecastResponse)
def predict_forecast(request: ForecastRequest, db: Session = Depends(get_db)):
    try:
        return forecast_product(db, request)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
