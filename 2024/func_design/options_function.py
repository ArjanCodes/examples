from typing_extensions import Unpack
from dataclasses import dataclass
from typing import TypedDict


class Options(TypedDict, total=False):
    age_limit: int
    valid_land_codes: list[str]


@dataclass
class Customer:
    name: str
    age: int
    phone: str


def is_elligible(data: Customer, **options: Unpack[Options]) -> bool:
    age_limit = options.get("age_limit", 0)
    valid_land_codes = options.get("valid_land_codes", ["+91"])

    if age_limit < data.age:
        return False

    land_code = data.phone[:3]

    return land_code in valid_land_codes


def main() -> None:
    customer = Customer(name="John", age=25, phone="+911234567890")

    is_elligible(customer, age_limit=18, valid_land_codes=["+91", "+92"])


if __name__ == "__main__":
    main()
