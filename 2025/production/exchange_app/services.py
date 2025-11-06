import datetime

from fastapi import HTTPException
from models import Conversion, ConversionRate
from sqlalchemy.orm import Session


class ExchangeRateService:
    def __init__(self, db: Session):
        self.db = db

    def convert(self, from_currency: str, to_currency: str, amount: float) -> dict:
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        rate_entry = (
            self.db.query(ConversionRate)
            .filter_by(from_currency=from_currency, to_currency=to_currency)
            .order_by(ConversionRate.timestamp.desc())
            .first()
        )
        print(rate_entry)

        if not rate_entry or rate_entry.rate <= 0:
            raise HTTPException(status_code=404, detail="Exchange rate not found")

        result = amount * rate_entry.rate

        conversion = Conversion(
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            result=result,
            timestamp=datetime.datetime.now(),
        )
        self.db.add(conversion)
        self.db.commit()

        return {"rate": rate_entry.rate, "result": result}
