"""
One-time backfill: loads the processed Phase 2 feature CSV and inserts
the raw sales columns into the new sales_history table.

Run from Backend/ with: python -m scripts.backfill_sales_history
"""

import pandas as pd

from app.db.database import SessionLocal, engine  # ADJUST if your session factory has a different name
from app.db.base import Base
from sqlalchemy import inspect
from app.models.sales_history import SalesHistory
from app.models.product import Product


CSV_PATH = "../data/processed/olist_phase2_features.csv"  # ADJUST path relative to where you run this


def run():
    # ensure tables exist in the target database before inserting
    # If a previous table exists with an incompatible schema (e.g. product_id int),
    # drop and recreate to match the current model definitions.
    inspector = inspect(engine)
    if "sales_history" in inspector.get_table_names():
        try:
            SalesHistory.__table__.drop(bind=engine)
        except Exception:
            # ignore drop failures and attempt create_all anyway
            pass

    Base.metadata.create_all(bind=engine)
    df = pd.read_csv(CSV_PATH)
    df["order_date"] = pd.to_datetime(df["order_date"]).dt.date

    db = SessionLocal()
    inserted = 0
    try:
        for _, row in df.iterrows():
            record = SalesHistory(
                product_id=row["product_id"],
                order_date=row["order_date"],
                units_sold=row["units_sold"],
                avg_price=row["avg_price"],
                avg_freight=row["avg_freight"],
                avg_review_score=row["avg_review_score"],
                avg_payment_value=row["avg_payment_value"],
                unique_customers=row["unique_customers"],
            )
            db.add(record)
            inserted += 1

        db.commit()
        print(f"Inserted {inserted} rows into sales_history.")
    except Exception as e:
        db.rollback()
        print(f"Backfill failed, rolled back: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run()