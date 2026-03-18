from typing import Any

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    custom_data: Mapped[dict[str, Any]] = mapped_column(
        MutableDict.as_mutable(JSON),
        default=dict,
        nullable=False,
    )

    def apply_custom_data_patch(self, patch: dict[str, Any]) -> None:
        """
        Stripe-style behavior:
        - {} clears all custom_data
        - {"key": value} sets or updates a key
        - {"key": None} removes a key
        """
        if patch == {}:
            self.custom_data = {}
            return

        current = dict(self.custom_data or {})

        for key, value in patch.items():
            if value is None:
                current.pop(key, None)
            else:
                current[key] = value

        self.custom_data = current

    def apply_patch(self, data: dict[str, Any]) -> None:
        for key, value in data.items():
            if value is None and key != "custom_data":
                continue

            if key == "custom_data":
                self.apply_custom_data_patch(value)
            else:
                setattr(self, key, value)


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))

    orders: Mapped[list["Order"]] = relationship(back_populates="customer")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    price_cents: Mapped[int]

    orders: Mapped[list["Order"]] = relationship(back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    quantity: Mapped[int] = mapped_column(default=1)
    status: Mapped[str] = mapped_column(String(32), default="pending")
    total_cents: Mapped[int]

    customer: Mapped[Customer] = relationship(back_populates="orders")
    product: Mapped[Product] = relationship(back_populates="orders")
