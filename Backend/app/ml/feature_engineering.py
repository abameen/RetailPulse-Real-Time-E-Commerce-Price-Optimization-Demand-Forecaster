from datetime import date, timedelta
from typing import Optional

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

from app.models.sales_history import SalesHistory
from app.models.product import Product  # for category lookup


def _fetch_history(db: Session, product_id: str, target_date: date, lookback_days: int = 30) -> pd.DataFrame:
    start_date = target_date - timedelta(days=lookback_days)

    rows = (
        db.query(SalesHistory)
        .filter(
            SalesHistory.product_id == product_id,
            SalesHistory.order_date >= start_date,
            SalesHistory.order_date < target_date,
        )
        .order_by(SalesHistory.order_date.asc())
        .all()
    )

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame([{
        "order_date": r.order_date,
        "units_sold": r.units_sold,
        "avg_price": r.avg_price,
    } for r in rows])

    df["order_date"] = pd.to_datetime(df["order_date"])
    return df.sort_values("order_date").reset_index(drop=True)


def _category_median_price(db: Session, category: str, target_date: date, lookback_days: int = 30) -> Optional[float]:
    start_date = target_date - timedelta(days=lookback_days)

    rows = (
        db.query(SalesHistory.avg_price)
        .join(Product, Product.id == SalesHistory.product_id)  # ADJUST join condition to your real FK/PK names
        .filter(
            Product.product_category_name == category,  # ADJUST if column name differs
            SalesHistory.order_date >= start_date,
            SalesHistory.order_date < target_date,
        )
        .all()
    )
    prices = [r[0] for r in rows if r[0] is not None]
    return float(np.median(prices)) if prices else None


def build_features(
    db: Session,
    product_id: str,
    product_category_name: str,
    target_date: date,
    current_price: float,
) -> dict:
    hist = _fetch_history(db, product_id, target_date)

    if hist.empty or len(hist) < 7:
        raise ValueError(
            f"Not enough history for product_id={product_id} to build lag_7 features "
            f"(found {len(hist)} prior rows, need at least 7)."
        )

    units_sold_lag_1 = hist["units_sold"].iloc[-1]
    avg_price_lag_1 = hist["avg_price"].iloc[-1]
    units_sold_lag_3 = hist["units_sold"].iloc[-3]
    avg_price_lag_3 = hist["avg_price"].iloc[-3]
    units_sold_lag_7 = hist["units_sold"].iloc[-7]
    avg_price_lag_7 = hist["avg_price"].iloc[-7]

    rolling_window = hist.tail(7)
    units_sold_rolling_mean_7 = rolling_window["units_sold"].mean()
    units_sold_rolling_std_7 = rolling_window["units_sold"].std()
    avg_price_rolling_mean_7 = rolling_window["avg_price"].mean()
    avg_price_rolling_std_7 = rolling_window["avg_price"].std()

    dt = pd.Timestamp(target_date)
    day_of_week = dt.dayofweek
    month = dt.month
    day_of_month = dt.day
    week_of_year = dt.isocalendar().week
    is_weekend = int(day_of_week >= 5)
    is_november = int(month == 11)
    is_black_friday_window = int(month == 11 and 20 <= day_of_month <= 30)  # ADJUST to match notebook

    median_price = _category_median_price(db, product_category_name, target_date)
    price_index = (current_price / median_price) if median_price else np.nan

    return {
        "avg_price": current_price,
        "day_of_week": day_of_week,
        "month": month,
        "day_of_month": day_of_month,
        "week_of_year": week_of_year,
        "is_weekend": is_weekend,
        "is_november": is_november,
        "is_black_friday_window": is_black_friday_window,
        "units_sold_lag_1": units_sold_lag_1,
        "avg_price_lag_1": avg_price_lag_1,
        "units_sold_lag_3": units_sold_lag_3,
        "avg_price_lag_3": avg_price_lag_3,
        "units_sold_lag_7": units_sold_lag_7,
        "avg_price_lag_7": avg_price_lag_7,
        "units_sold_rolling_mean_7": units_sold_rolling_mean_7,
        "units_sold_rolling_std_7": units_sold_rolling_std_7,
        "avg_price_rolling_mean_7": avg_price_rolling_mean_7,
        "avg_price_rolling_std_7": avg_price_rolling_std_7,
        "price_index": price_index,
        "product_category_name": product_category_name,
    }

