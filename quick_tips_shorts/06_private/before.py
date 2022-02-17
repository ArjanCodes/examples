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
    search_string: str = ""

    def __post_init__(self):
        self.search_string = f"{self.name} {self.city} {self.state} {self.email}"

    def greeting(self) -> str:
        return f"Hi, {self.extract_first_name()}!"

    def extract_first_name(self) -> str:
        return self.name.split()[0]


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
    print(person.greeting())


if __name__ == "__main__":
    main()
