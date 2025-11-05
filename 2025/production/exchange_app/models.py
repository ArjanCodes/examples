import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class Conversion(Base):
    __tablename__ = "conversions"

    id = mapped_column(Integer, primary_key=True)
    from_currency = mapped_column(String(3))
    to_currency = mapped_column(String(3))
    amount = mapped_column(Float)
    result = mapped_column(Float)
    timestamp = mapped_column(DateTime, default=datetime.datetime.now)


class ConversionRate(Base):
    __tablename__ = "conversion_rates"

    id = mapped_column(Integer, primary_key=True)
    from_currency = mapped_column(String(3))
    to_currency = mapped_column(String(3))
    rate = mapped_column(Float)
    timestamp = mapped_column(DateTime, default=datetime.datetime.now)
