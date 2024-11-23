from fastapi import APIRouter, FastAPI

from src.orders.routes.orders import router as orders_router

app = FastAPI()

v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(orders_router, prefix="/orders")

app.include_router(v1_router)
