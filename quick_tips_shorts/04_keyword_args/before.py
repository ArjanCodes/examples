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
        "John Smith",
        "123 Main St.",
        "Apt. 1",
        "Anytown",
        "CA",
        "12345",
        "john@email.com",
    )
    print(person)


if __name__ == "__main__":
    main()
