from datetime import date

from pydantic import BaseModel


class SalesHistoryResponse(BaseModel):
    order_date: date
    units_sold: int
    avg_price: float

    model_config = {
        "from_attributes": True,
    }
