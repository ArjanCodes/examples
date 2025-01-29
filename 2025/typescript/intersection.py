from typing import Protocol


class HasName(Protocol):
    name: str


class HasAge(Protocol):
    age: int


# This is the equivalent of an intersection type in Python
class Person(HasName, HasAge):
    pass


def print_person_details(person: Person) -> None:
    print(f"{person.name} is {person.age} years old.")


# Example usage
class Employee:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


employee = Employee("Arjan", 35)
print_person_details(employee)  # Works because Employee satisfies HasName and HasAge
