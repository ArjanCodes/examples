from dataclasses import dataclass


@dataclass(kw_only=True)
class Person:
    name: str
    address: str
    email: str


def main():
    person = Person(name="John", address="123 Main St", email="john@doe.com")
    # person = Person("John", "123 Main St", "john@doe.com")
    print(person)


if __name__ == "__main__":
    main()
