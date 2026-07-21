from sqlalchemy import Column, Integer, ForeignKey, Float, Date
from ..db.base import Base


class SalesHistory(Base):
    __tablename__ = "sales_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    order_date = Column(Date, nullable=False, index=True)
    units_sold = Column(Integer, nullable=False)
    avg_price = Column(Float, nullable=True)
    avg_freight = Column(Float, nullable=True)
    avg_review_score = Column(Float, nullable=True)
    avg_payment_value = Column(Float, nullable=True)
    unique_customers = Column(Integer, nullable=True)
