from typing import Any
from fastapi import APIRouter, HTTPException
from src.models import Customer
from src.repository import get_resource, get_resources, create_resource, update_resource


customer_router = APIRouter()


@customer_router.get("/customers")
async def get_customers() -> list[Customer]:
    customers = await get_resources("customers")

    if not customers:
        return []

    return customers


@customer_router.get("/customers/{customer_id}")
async def get_customer(customer_id: int) -> Customer:
    customer = await get_resource("customers", customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return Customer(name="John Doe", email="", address="")


@customer_router.post("/customers")
async def create_customer(params: dict[str, Any]) -> Customer:
    customer: Customer = await create_resource("customers", params)

    if not customer:
        raise HTTPException(status_code=400, detail="Failed to create customer")

    return customer


@customer_router.put("/customers/{customer_id}")
async def update_customer(customer_id: int, params: dict[str, Any]) -> Customer:
    customer: Customer = await update_resource("customers", customer_id, params)

    return customer
