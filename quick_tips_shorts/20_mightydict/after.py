from dataclasses import dataclass


@dataclass
class Customer:
    name: str
    email: str
    active: bool


CUSTOMERS: dict[str, Customer] = {}


def add_customer(name: str, email: str, active: bool = True):
    CUSTOMERS[email] = Customer(name, email, active)


def find_by_email(email: str) -> Customer:
    return CUSTOMERS[email]


def main():
    add_customer("Sarah", "sarah@trconsulting.com", False)
    add_customer("Tim", "tim@timsdogclub.com")
    add_customer("Chelsey", "chelsey@examtraining.org")

    print(find_by_email("tim@timsdogclub.com"))


if __name__ == "__main__":
    main()
