from dataclasses import dataclass
from operator import itemgetter
from typing import TypedDict


@dataclass
class Customer:
    name: str
    age: int
    phone: str


class Options(TypedDict, total=False):
    age_limit: int
    valid_land_codes: list[str]


def is_eligible(data: Customer, options: Options) -> bool:
    age_limit = options.get("age_limit", 0)
    valid_land_codes = options.get("valid_land_codes", ["+91"])

    # this could work, but the types are no longer available, neither are defaults
    age_limit, valid_land_codes = itemgetter("age_limit", "valid_land_codes")(options)

    if age_limit < data.age:
        return False

    land_code = data.phone[:3]

    return land_code in valid_land_codes


@dataclass
class OptionsV2:
    age_limit: int = 0
    valid_land_codes: list[str] = ["+91"]


def is_eligible_v2(data: Customer, options: OptionsV2) -> bool:
    age_limit = options.age_limit
    valid_land_codes = options.valid_land_codes

    if age_limit < data.age:
        return False

    land_code = data.phone[:3]

    return land_code in valid_land_codes


def main() -> None:
    customer = Customer(name="John", age=25, phone="+911234567890")

    is_eligible(customer, {"age_limit": 18, "valid_land_codes": ["+91", "+92"]})
    is_eligible_v2(customer, OptionsV2(valid_land_codes=["+91", "+92"]))


if __name__ == "__main__":
    main()
