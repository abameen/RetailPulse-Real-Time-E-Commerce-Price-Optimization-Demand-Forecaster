"""
One-time backfill: loads the processed Phase 2 feature CSV and inserts
unique products into the products table.

Run from Backend/ with: python -m scripts.backfill_products
"""

import pandas as pd
from sqlalchemy import inspect

from app.db.database import SessionLocal, engine
from app.db.base import Base
from app.models.product import Product

CSV_PATH = "../data/processed/olist_phase2_features.csv"


def run():
    inspector = inspect(engine)
    if "products" not in inspector.get_table_names():
        Base.metadata.create_all(bind=engine)

    df = pd.read_csv(CSV_PATH)
    if "avg_price" not in df.columns or "product_id" not in df.columns:
        raise ValueError("CSV must contain product_id and avg_price columns")

    db = SessionLocal()
    inserted = 0
    try:
        product_groups = (
            df.groupby(["product_id", "product_category_name"], dropna=False)
            ["avg_price"].mean().reset_index()
        )

        for _, row in product_groups.iterrows():
            product_name = str(row["product_id"])
            category = row["product_category_name"] if pd.notna(row["product_category_name"]) else None
            current_price = float(row["avg_price"])

            existing = (
                db.query(Product)
                .filter(Product.name == product_name, Product.category == category)
                .first()
            )

            if existing:
                continue

            product = Product(
                name=product_name,
                description=f"Product from sales_history with product_id={product_name}",
                current_price=current_price,
                category=category,
            )
            db.add(product)
            inserted += 1

        db.commit()
        print(f"Inserted {inserted} unique products into products.")
    except Exception as exc:
        db.rollback()
        print(f"Backfill failed, rolled back: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run()
