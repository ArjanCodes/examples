from datetime import datetime

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Conversion(Base):
    __tablename__ = "conversions"

    id: Mapped[int] = mapped_column(primary_key=True)
    from_currency: Mapped[str] = mapped_column(String(3))
    to_currency: Mapped[str] = mapped_column(String(3))
    amount: Mapped[float] = mapped_column()
    result: Mapped[float] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now)


class ConversionRate(Base):
    __tablename__ = "conversion_rates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    from_currency: Mapped[str] = mapped_column(String(3))
    to_currency: Mapped[str] = mapped_column(String(3))
    rate: Mapped[float] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now)
