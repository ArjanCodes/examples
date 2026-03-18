from database import get_db
from db_models import Customer, Order, Product
from fastapi import APIRouter, Depends, HTTPException, Response, status
from schemas import (
    CustomerCreate,
    CustomerPatch,
    CustomerRead,
    OrderCreate,
    OrderPatch,
    OrderRead,
    ProductCreate,
    ProductPatch,
    ProductRead,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/customers", response_model=CustomerRead, status_code=status.HTTP_201_CREATED
)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)) -> Customer:
    existing = db.scalar(select(Customer).where(Customer.email == str(payload.email)))
    if existing is not None:
        raise HTTPException(
            status_code=409, detail="Customer with this email already exists."
        )

    customer = Customer(**payload.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.get("/customers/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: int, db: Session = Depends(get_db)) -> Customer:
    customer = db.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return customer


@router.patch("/customers/{customer_id}", response_model=CustomerRead)
def patch_customer(
    customer_id: int,
    payload: CustomerPatch,
    db: Session = Depends(get_db),
) -> Customer:
    customer = db.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found.")

    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)
    return customer


@router.post(
    "/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED
)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)) -> Product:
    existing = db.scalar(select(Product).where(Product.sku == payload.sku))
    if existing is not None:
        raise HTTPException(
            status_code=409, detail="Product with this SKU already exists."
        )

    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)) -> Product:
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")
    return product


@router.patch("/products/{product_id}", response_model=ProductRead)
def patch_product(
    product_id: int,
    payload: ProductPatch,
    db: Session = Depends(get_db),
) -> Product:
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")

    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.post("/orders", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)) -> Order:
    customer = db.get(Customer, payload.customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found.")

    product = db.get(Product, payload.product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")

    data = payload.model_dump()

    order = Order(
        **data,
        total_cents=product.price_cents * data["quantity"],
    )

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("/orders/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)) -> Order:
    order = db.get(Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order


@router.patch("/orders/{order_id}", response_model=OrderRead)
def patch_order(
    order_id: int,
    payload: OrderPatch,
    db: Session = Depends(get_db),
) -> Order:
    order = db.get(Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found.")

    updates = payload.model_dump(exclude_unset=True)

    if "quantity" in updates:
        product = db.get(Product, order.product_id)
        if product is None:
            raise HTTPException(status_code=500, detail="Related product not found.")
        order.quantity = updates.pop("quantity")
        order.total_cents = product.price_cents * order.quantity

    for key, value in updates.items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)
    return order


@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)) -> Response:
    order = db.get(Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found.")

    db.delete(order)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
