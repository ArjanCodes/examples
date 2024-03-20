class Person:
    def __init__(self, name: str):
        self.name: str = name
        self._age: int

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value: int):
        if value < 0:
            raise ValueError("Age cannot be negative")
        self._age = value


def main() -> None:
    try:
        person = Person("John")
        person.age = -10
        print(f"Name: {person.name}, age: {person.age}")
    except ValueError as error:
        print(f"Error occurred: {error}")


if __name__ == "__main__":
    main()
