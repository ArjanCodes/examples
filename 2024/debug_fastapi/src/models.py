from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CoreModel(BaseModel):
    id: UUID
    inserted_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Customer(CoreModel):
    name: str
    email: str
    address: str

class Payment(CoreModel):
    amount: float
    currency: str
    customer_id: UUID
    description: str
