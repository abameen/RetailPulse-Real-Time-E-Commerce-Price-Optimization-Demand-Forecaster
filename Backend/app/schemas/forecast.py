from datetime import date

from pydantic import BaseModel


class ForecastRequest(BaseModel):
    product_id: str
    target_date: date


class ForecastResponse(BaseModel):
    predicted_units_sold: float
    target_date: date
    product_id: str
    history_days_used: int
    feature_columns: list[str]
