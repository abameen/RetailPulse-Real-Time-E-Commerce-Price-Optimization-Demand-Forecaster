from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.product import router as product_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["health"])
api_router.include_router(product_router, prefix="/products", tags=["products"])

