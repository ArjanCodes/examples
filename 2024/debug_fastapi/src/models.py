from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CoreModel(BaseModel):
    id: UUID
    inserted_at: datetime | None
    updated_at: datetime | None

    class Config:
        from_attributes = True


class Customer(CoreModel):
    name: str
    email: str
    address: str


class Payment(BaseModel):
    amount: float
    currency: str = "USD"
    customer_id: UUID
    description: str | None = None
