from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.sales_history import SalesHistory
from app.schemas.sales_history import SalesHistoryResponse

router = APIRouter()


@router.get("/{product_id}", response_model=list[SalesHistoryResponse])
def get_sales_history(product_id: str, db: Session = Depends(get_db)):
    rows = (
        db.query(SalesHistory)
        .filter(SalesHistory.product_id == product_id)
        .order_by(SalesHistory.order_date.asc())
        .all()
    )

    if not rows:
        raise HTTPException(
            status_code=404,
            detail=f"No sales history found for product_id={product_id}",
        )

    return rows
