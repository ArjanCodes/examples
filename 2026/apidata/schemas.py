from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomDataSchema(BaseModel):
    custom_data: dict[str, Any] = Field(default_factory=dict)


class CustomerCreate(CustomDataSchema):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)


class CustomerPatch(BaseModel):
    email: EmailStr | None = None
    name: str | None = Field(default=None, min_length=1, max_length=100)
    custom_data: dict[str, Any] | None = None


class CustomerRead(CustomDataSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    name: str


class ProductCreate(CustomDataSchema):
    sku: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=120)
    price_cents: int = Field(ge=0)


class ProductPatch(BaseModel):
    sku: str | None = Field(default=None, min_length=1, max_length=64)
    name: str | None = Field(default=None, min_length=1, max_length=120)
    price_cents: int | None = Field(default=None, ge=0)
    custom_data: dict[str, Any] | None = None


class ProductRead(CustomDataSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sku: str
    name: str
    price_cents: int


class OrderCreate(CustomDataSchema):
    customer_id: int
    product_id: int
    quantity: int = Field(default=1, ge=1)
    status: Literal["pending", "paid", "shipped", "cancelled"] = "pending"


class OrderPatch(BaseModel):
    quantity: int | None = Field(default=None, ge=1)
    status: Literal["pending", "paid", "shipped", "cancelled"] | None = None
    custom_data: dict[str, Any] | None = None


class OrderRead(CustomDataSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    product_id: int
    quantity: int
    status: str
    total_cents: int
