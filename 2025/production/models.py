from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import datetime

Base = declarative_base()

class Conversion(Base):
    __tablename__ = "conversions"

    id = Column(Integer, primary_key=True)
    from_currency = Column(String)
    to_currency = Column(String)
    amount = Column(Integer)
    result = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)