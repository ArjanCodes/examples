from sqlalchemy.orm import Session
from .models import ConversionRate
from .database import SessionLocal

sample_rates = [
    {"from_currency": "USD", "to_currency": "EUR", "rate": 0.91},
    {"from_currency": "EUR", "to_currency": "USD", "rate": 1.10},
    {"from_currency": "USD", "to_currency": "JPY", "rate": 150.0},
    {"from_currency": "GBP", "to_currency": "USD", "rate": 1.28},
    {"from_currency": "USD", "to_currency": "GBP", "rate": 0.78},
]

def main():
    db: Session = SessionLocal()
    for entry in sample_rates:
        rate = ConversionRate(**entry)
        db.add(rate)
    db.commit()
    db.close()
    print("Seeded exchange rates.")

if __name__ == "__main__":
    main()