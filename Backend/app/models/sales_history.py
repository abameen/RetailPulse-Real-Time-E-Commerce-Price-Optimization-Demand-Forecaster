from sqlalchemy import Column, Integer, ForeignKey, Float, Date, String
from ..db.base import Base


class SalesHistory(Base):
    __tablename__ = "sales_history"

    id = Column(Integer, primary_key=True, index=True)
    # product_id in the CSV is a string identifier; store as string to match source
    product_id = Column(String(128), nullable=False, index=True)
    order_date = Column(Date, nullable=False, index=True)
    units_sold = Column(Integer, nullable=False)
    avg_price = Column(Float, nullable=True)
    avg_freight = Column(Float, nullable=True)
    avg_review_score = Column(Float, nullable=True)
    avg_payment_value = Column(Float, nullable=True)
    unique_customers = Column(Integer, nullable=True)
