from fastapi import APIRouter
from .routes import product as product_router
from .routes import health as health_router

router = APIRouter()
router.include_router(product_router.router, prefix="/products", tags=["products"])
router.include_router(health_router.router, prefix="", tags=["health"])
