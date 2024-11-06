from fastapi import APIRouter

from app.api.endpoints import batch_router, inventory_router, product_router

main_router = APIRouter()
main_router.include_router(product_router, tags=['Product'], prefix='/product')
main_router.include_router(batch_router, tags=['Batch'], prefix='/batch')
main_router.include_router(inventory_router, tags=['Warehouse'], prefix='/Warehouse')
