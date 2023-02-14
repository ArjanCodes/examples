from datetime import datetime
from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.types import DateTime, Integer, Numeric, String


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "Customer"

    CustomerId: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    FirstName: Mapped[str] = mapped_column(String(40))
    LastName: Mapped[Optional[str]] = mapped_column(String(20))
    Company: Mapped[str] = mapped_column(String(80))
    Address: Mapped[str] = mapped_column(String(70))
    City: Mapped[str] = mapped_column(String(40))
    State: Mapped[str] = mapped_column(String(40))
    Country: Mapped[str] = mapped_column(String(40))
    PostalCode: Mapped[str] = mapped_column(String(10))
    Phone: Mapped[str] = mapped_column(String(24))
    Fax: Mapped[str] = mapped_column(String(24))
    Email: Mapped[str] = mapped_column(String(60), nullable=False)
    SupportRepId: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return (
            f"CustomerId(CustomerId={self.CustomerId!r}, "
            f"FirstName={self.FirstName!r}, "
            f"LastName={self.LastName!r})"
        )


class Invoice(Base):
    __tablename__ = "Invoice"

    InvoiceId: Mapped[int] = mapped_column(
        primary_key=True, nullable=False
    )  # INTEGER  NOT NULL,
    CustomerId: Mapped[int] = mapped_column(nullable=False)
    InvoiceDate: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    BillingAddress: Mapped[str] = mapped_column(String(70))
    BillingCity: Mapped[str] = mapped_column(String(40))
    BillingState: Mapped[str] = mapped_column(String(40))
    BillingCountry: Mapped[str] = mapped_column(String(40))
    BillingPostalCode: Mapped[str] = mapped_column(String(10))
    Total: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    def __repr__(self) -> str:
        return (
            f"Invoice(InvoiceId={self.InvoiceId!r}, "
            f"CustomerId={self.CustomerId!r}, "
            f"InvoiceDate={self.InvoiceDate!r})"
        )


db_path = Path("orm\database\sample_database.db").absolute()

engine = create_engine(rf"sqlite:///{db_path}")
session = Session(engine)
stmt = (
    select(
        Customer.CustomerId,
        Customer.FirstName,
        func.sum(Invoice.Total).label("Total"),
    )
    .join(Invoice, Customer.CustomerId == Invoice.CustomerId)
    .group_by(Customer.CustomerId, Customer.FirstName)
    .order_by(func.sum(Invoice.Total).label("Total").desc())
    .limit(10)
)

for customer in session.execute(stmt):
    print(customer)
