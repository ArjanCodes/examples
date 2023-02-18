from datetime import datetime
from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.types import DateTime, Integer, String


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "Customer"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(40))
    last_name: Mapped[Optional[str]] = mapped_column(String(20))
    company: Mapped[str] = mapped_column(String(80))
    address: Mapped[str] = mapped_column(String(70))
    city: Mapped[str] = mapped_column(String(40))
    state: Mapped[str] = mapped_column(String(40))
    country: Mapped[str] = mapped_column(String(40))
    postal_code: Mapped[str] = mapped_column(String(10))
    phone: Mapped[str] = mapped_column(String(24))
    fax: Mapped[str] = mapped_column(String(24))
    email: Mapped[str] = mapped_column(String(60), nullable=False)
    support_id: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return (
            f"Customer(id={self.id!r}, "
            f"first_name={self.first_name!r}, "
            f"last_name={self.LastName!r})"
        )


class Invoice(Base):
    __tablename__ = "Invoice"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, nullable=False)
    customer_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    billing_address: Mapped[str] = mapped_column(String(70))
    billing_city: Mapped[str] = mapped_column(String(40))
    billing_state: Mapped[str] = mapped_column(String(40))
    billing_country: Mapped[str] = mapped_column(String(40))
    billing_postal_code: Mapped[str] = mapped_column(String(10))
    total: Mapped[int] = mapped_column(Integer(), nullable=False)

    def __repr__(self) -> str:
        return (
            f"Invoice(id={self.id!r}, "
            f"customer_id={self.customer_id!r}, "
            f"date={self.date!r})"
        )


def main() -> None:
    db_path = Path("orm\database\sample_database.db").absolute()

    engine = create_engine(rf"sqlite:///{db_path}")
    session = Session(engine)
    stmt = (
        select(
            Customer.id,
            Customer.first_name,
            func.sum(Invoice.total).label("Total"),
        )
        .join(Invoice, Customer.id == Invoice.customer_id)
        .group_by(Customer.id, Customer.first_name)
        .order_by(func.sum(Invoice.total).label("Total").desc())
        .limit(10)
    )

    for customer in session.execute(stmt):
        print(customer)


if __name__ == "__main__":
    main()
