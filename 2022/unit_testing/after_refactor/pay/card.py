from dataclasses import dataclass


@dataclass
class CreditCard:
    number: str
    expiry_month: int
    expiry_year: int
