from dataclasses import dataclass


@dataclass
class Customer:
    id: int = 0
    name: str = ""
    address: str = ""
    postal_code: str = ""
    city: str = ""
    email: str = ""
