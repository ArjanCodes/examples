from dataclasses import dataclass


@dataclass
class Person:
    name: str
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    zip_code: str
    email: str


def main() -> None:
    person = Person(
        name="John Smith",
        address_line_1="123 Main St.",
        address_line_2="Apt. 1",
        city="Anytown",
        state="CA",
        zip_code="12345",
        email="john@email.com",
    )
    print(person)


if __name__ == "__main__":
    main()
