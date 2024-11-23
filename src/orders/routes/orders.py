from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_db_session
from src.orders import models
from src.orders.routes import schemas

# /api/v1/orders
router = APIRouter()


@router.post("", summary="Create a new order")
async def create_order(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    request_data: schemas.CreateOrderRequest,
) -> schemas.CreateOrderResponse:
    # TODO: add order lines
    order = models.Order(customer=request_data.customer)
    await db.commit()
    await db.refresh(order)
    return schemas.CreateOrderResponse(
        id=order.id,
        created_at=order.created_at,
        updated_at=order.updated_at,
        status=order.status,
        customer=order.customer,
    )

# TODO: create a route to retrieve all orders (look here https://berkkaraal.com/blog/2024/09/19/setup-fastapi-project-with-async-sqlalchemy-2-alembic-postgresql-and-docker/#add-listing-todos-endpoint)
# TODO: also create remove order endpoint and update order endpoint
# TODO: but for that we first need to create product and order lines.

@router.get("/{order_id}", summary="Retrieve an order by id")
async def retrieve_order(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    order_id: int,
) -> schemas.RetrieveOrderResponse:
    stmt = select(
        models.Order.id,
        models.Order.created_at,
        models.Order.updated_at,
        models.Order.status,
        models.Order.customer,
    ).where(
        models.Order.id == order_id,
    )
    result_row = (await db.execute(stmt)).first()
    
    if result_row is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    mapped_row = result_row._mapping
    return schemas.RetrieveOrderResponse(
        id=mapped_row["id"],
        created_at=mapped_row["created_at"],
        updated_at=mapped_row["updated_at"],
        status=mapped_row["status"],
        customer=mapped_row["customer"],
    )