import timeit
from dataclasses import dataclass
from functools import partial
from statistics import median


@dataclass
class Person:
    name: str
    address: str
    email: str


def get_set_delete(person: Person):
    person.address = "123 Main St"
    _ = person.address
    del person.address


def main():
    person = Person("John", "123 Main St", "john@doe.com")
    result = timeit.repeat(partial(get_set_delete, person), number=1000000)
    print(f"Min: {min(result)}, Max: {max(result)}, Median: {median(result)}")


if __name__ == "__main__":
    main()
