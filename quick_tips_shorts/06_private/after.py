from dataclasses import dataclass, field


@dataclass
class Person:
    name: str
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    zip_code: str
    email: str
    _search_string: str = field(init=False, repr=False)

    def __post_init__(self):
        self._search_string = f"{self.name} {self.city} {self.state} {self.email}"

    def greeting(self) -> str:
        return f"Hi, {self._extract_first_name()}!"

    def _extract_first_name(self) -> str:
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
