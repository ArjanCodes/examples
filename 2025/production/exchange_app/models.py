from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
import datetime

Base = declarative_base()

class Conversion(Base):
    __tablename__ = "conversions"

    id = Column(Integer, primary_key=True)
    from_currency = Column(String(3))
    to_currency = Column(String(3))
    amount = Column(Float)
    result = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class ConversionRate(Base):
    __tablename__ = "conversion_rates"

    id = Column(Integer, primary_key=True)
    from_currency = Column(String(3))
    to_currency = Column(String(3))
    rate = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)