class Person:
    def __init__(self, name: str, age: int) -> None:
        self._name = name
        self._age = age

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def get_age(self) -> int:
        return self._age

    def set_age(self, age: int) -> None:
        self._age = age


def main() -> None:
    person = Person("Arjan", 47)
    print(person.get_name())
    print(person.get_age())
    person.set_name("Bonnie")
    person.set_age(25)
    print(person.get_name())
    print(person.get_age())


if __name__ == "__main__":
    main()
