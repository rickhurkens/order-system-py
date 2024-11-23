from datetime import datetime

from pydantic import BaseModel


class CreateOrderRequest(BaseModel):
    customer: str
    # TODO: add order lines
    
class CreateOrderResponse(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    status: str
    customer: str

class RetrieveOrderResponse(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    status: str
    customer: str
    # TODO: add order lines


