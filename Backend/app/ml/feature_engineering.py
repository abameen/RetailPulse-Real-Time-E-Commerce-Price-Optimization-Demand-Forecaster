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
        "avg_freight": r.avg_freight,
        "avg_review_score": r.avg_review_score,
        "avg_payment_value": r.avg_payment_value,
        "unique_customers": r.unique_customers,
    } for r in rows])

    df["order_date"] = pd.to_datetime(df["order_date"])
    return df.sort_values("order_date").reset_index(drop=True)


def _category_median_price(db: Session, category: str, target_date: date, lookback_days: int = 30) -> Optional[float]:
    start_date = target_date - timedelta(days=lookback_days)

    # We don't have reliable cross-table category relationships in this schema
    # so return None for now (caller should handle missing median price).
    return None
    prices = [r[0] for r in rows if r[0] is not None]
    return float(np.median(prices)) if prices else None


def build_features(db: Session, product_id: str, target_date: date, lookback_days: int = 30) -> dict:
    """Build feature dict matching the model's expected feature names.

    This function pulls recent history for `product_id` and computes lags,
    rolling stats and simple change features. It returns a dict whose keys
    align with the trained model's `feature_name_`.
    """
    hist = _fetch_history(db, product_id, target_date, lookback_days=lookback_days)

    if hist.empty or len(hist) < 7:
        raise ValueError(
            f"Not enough history for product_id={product_id} to build features (found {len(hist)} rows, need >=7)."
        )

    # Basic last-observed values
    units_sold = hist["units_sold"].iloc[-1]
    avg_price = hist["avg_price"].iloc[-1]
    avg_freight = hist.get("avg_freight").iloc[-1] if "avg_freight" in hist else None
    avg_review_score = hist.get("avg_review_score").iloc[-1] if "avg_review_score" in hist else None
    avg_payment_value = hist.get("avg_payment_value").iloc[-1] if "avg_payment_value" in hist else None
    unique_customers = hist.get("unique_customers").iloc[-1] if "unique_customers" in hist else None

    # lags
    units_sold_lag_1 = hist["units_sold"].iloc[-1]
    avg_price_lag_1 = hist["avg_price"].iloc[-1]
    units_sold_lag_3 = hist["units_sold"].iloc[-3]
    avg_price_lag_3 = hist["avg_price"].iloc[-3]
    units_sold_lag_7 = hist["units_sold"].iloc[-7]
    avg_price_lag_7 = hist["avg_price"].iloc[-7]

    # changes (difference)
    price_change_1d = float(avg_price_lag_1 - hist["avg_price"].iloc[-2]) if len(hist) >= 2 else 0.0
    price_change_3d = float(avg_price_lag_1 - hist["avg_price"].iloc[-4]) if len(hist) >= 4 else 0.0
    price_change_7d = float(avg_price_lag_1 - hist["avg_price"].iloc[-8]) if len(hist) >= 8 else 0.0

    units_change_1d = float(units_sold_lag_1 - hist["units_sold"].iloc[-2]) if len(hist) >= 2 else 0.0
    units_change_3d = float(units_sold_lag_1 - hist["units_sold"].iloc[-4]) if len(hist) >= 4 else 0.0
    units_change_7d = float(units_sold_lag_1 - hist["units_sold"].iloc[-8]) if len(hist) >= 8 else 0.0

    # rolling stats over last 7 days
    tail7 = hist.tail(7)
    price_roll_mean_7 = float(tail7["avg_price"].mean())
    price_roll_std_7 = float(tail7["avg_price"].std())
    units_roll_mean_7 = float(tail7["units_sold"].mean())
    units_roll_std_7 = float(tail7["units_sold"].std())

    dt = pd.Timestamp(target_date)
    day_of_week = int(dt.dayofweek)
    month = int(dt.month)
    day_of_month = int(dt.day)
    week_of_year = int(dt.isocalendar().week)
    is_weekend = int(day_of_week >= 5)
    is_november = int(month == 11)
    is_black_friday_window = int(month == 11 and 20 <= day_of_month <= 30)

    # Try to resolve category from products table if possible
    category = None
    try:
        # attempt cast to int to match Product.id if appropriate
        from app.models.product import Product

        pid_int = None
        try:
            pid_int = int(product_id)
        except Exception:
            pid_int = None

        if pid_int is not None:
            prod = db.query(Product).filter(Product.id == pid_int).first()
            if prod is not None:
                category = getattr(prod, "category", None)
    except Exception:
        category = None

    # category_price_index uses median category price if available
    median_price = _category_median_price(db, category, target_date) if category else None
    category_price_index = float(avg_price / median_price) if median_price else np.nan

    # The trained model expects numeric-encoded category; provide numeric
    # placeholder 0.0 when category encoding is not available.
    features = {
        "product_category_name": 0.0,
        "units_sold": float(units_sold),
        "avg_price": float(avg_price),
        "avg_freight": float(avg_freight) if avg_freight is not None else np.nan,
        "avg_review_score": float(avg_review_score) if avg_review_score is not None else np.nan,
        "avg_payment_value": float(avg_payment_value) if avg_payment_value is not None else np.nan,
        "unique_customers": int(unique_customers) if unique_customers is not None else 0,
        "day_of_week": day_of_week,
        "month": month,
        "day_of_month": day_of_month,
        "week_of_year": week_of_year,
        "is_weekend": is_weekend,
        "is_november": is_november,
        "is_black_friday_window": is_black_friday_window,
        "units_sold_lag_1": float(units_sold_lag_1),
        "avg_price_lag_1": float(avg_price_lag_1),
        "units_sold_lag_3": float(units_sold_lag_3),
        "avg_price_lag_3": float(avg_price_lag_3),
        "units_sold_lag_7": float(units_sold_lag_7),
        "avg_price_lag_7": float(avg_price_lag_7),
        "price_change_1d": price_change_1d,
        "price_change_3d": price_change_3d,
        "price_change_7d": price_change_7d,
        "units_change_1d": units_change_1d,
        "units_change_3d": units_change_3d,
        "units_change_7d": units_change_7d,
        "price_roll_mean_7": price_roll_mean_7,
        "price_roll_std_7": price_roll_std_7,
        "units_roll_mean_7": units_roll_mean_7,
        "units_roll_std_7": units_roll_std_7,
        "category_price_index": category_price_index,
    }

    return features

