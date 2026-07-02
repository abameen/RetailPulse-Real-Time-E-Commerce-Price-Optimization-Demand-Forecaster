from fastapi import APIRouter
from ...schemas.product import ProductCreate, Product as ProductSchema
from ...services.product_service import ProductService

router = APIRouter()


@router.get("/", response_model=list[ProductSchema])
def list_products():
    return ProductService.list_products()


@router.post("/", response_model=ProductSchema)
def create_product(payload: ProductCreate):
    return ProductService.create_product(payload)
