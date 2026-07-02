from typing import List
from ..models.product import Product
from ..schemas.product import ProductCreate


class ProductService:
    @staticmethod
    def list_products() -> List[Product]:
        return []

    @staticmethod
    def create_product(payload: ProductCreate) -> Product:
        return Product(id=1, name=payload.name, price=payload.price)
