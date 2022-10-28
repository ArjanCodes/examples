from dataclasses import dataclass
from datetime import datetime


@dataclass
class Customer:
    name: str
    phone: str
    cc_number: str
    cc_exp_month: int
    cc_exp_year: int
    cc_valid: bool = False


def validate_card(customer: Customer) -> bool:
    def digits_of(number: str) -> list[int]:
        return [int(d) for d in number]

    digits = digits_of(customer.cc_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for digit in even_digits:
        checksum += sum(digits_of(str(digit * 2)))

    customer.cc_valid = (
        checksum % 10 == 0
        and datetime(customer.cc_exp_year, customer.cc_exp_month, 1) > datetime.now()
    )
    return customer.cc_valid


def main() -> None:
    alice = Customer(
        name="Alice",
        phone="2341",
        cc_number="1249190007575069",
        cc_exp_month=1,
        cc_exp_year=2024,
    )
    is_valid = validate_card(alice)
    print(f"Is Alice's card valid? {is_valid}")
    print(alice)


if __name__ == "__main__":
    main()
