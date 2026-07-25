from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def _build_category_price_index(db: Session) -> dict[str | None, float | None]:
    prices_by_category: dict[str | None, list[float]] = {}
    products = db.query(Product.category, Product.current_price).all()
    for category, price in products:
        prices_by_category.setdefault(category, []).append(price)

    medians: dict[str | None, float | None] = {}
    for category, prices in prices_by_category.items():
        prices.sort()
        count = len(prices)
        if count == 0:
            medians[category] = None
            continue
        mid = count // 2
        if count % 2 == 1:
            medians[category] = prices[mid]
        else:
            medians[category] = (prices[mid - 1] + prices[mid]) / 2.0

    return medians


def _annotate_category_price_index(products: list[Product], medians: dict[str | None, float | None]) -> list[Product]:
    for product in products:
        median = medians.get(product.category)
        if median and median > 0:
            product.category_price_index = product.current_price / median
        else:
            product.category_price_index = None
    return products


def get_product(db: Session, product_id: int) -> Product | None:
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        return None

    medians = _build_category_price_index(db)
    _annotate_category_price_index([product], medians)
    return product


def get_products(db: Session, skip: int = 0, limit: int = 100) -> list[Product]:
    products = db.query(Product).offset(skip).limit(limit).all()
    medians = _build_category_price_index(db)
    return _annotate_category_price_index(products, medians)


def update_product(db: Session, product_id: int, product: ProductUpdate) -> Product | None:
    db_product = get_product(db, product_id)
    if db_product is None:
        return None

    update_data = product.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)

    medians = _build_category_price_index(db)
    _annotate_category_price_index([db_product], medians)
    return db_product


def delete_product(db: Session, product_id: int) -> Product | None:
    db_product = get_product(db, product_id)
    if db_product is None:
        return None

    db.delete(db_product)
    db.commit()
    return db_product

