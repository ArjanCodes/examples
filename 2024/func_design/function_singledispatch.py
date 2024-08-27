from functools import singledispatch
from typing import Protocol, runtime_checkable


# Define protocols
@runtime_checkable
class Describable(Protocol):
    def describe(self) -> str: ...


@runtime_checkable
class Identifiable(Protocol):
    def get_id(self) -> str: ...


@runtime_checkable
class Trackable(Protocol):
    def get_location(self) -> str: ...


# Implementations of the protocols
class User:
    def __init__(self, username: str):
        self.username = username

    def describe(self) -> str:
        return f"User: {self.username}"


class Product:
    def __init__(self, product_id: str, name: str):
        self.product_id = product_id
        self.name = name

    def get_id(self) -> str:
        return f"Product ID: {self.product_id}"


class Package:
    def __init__(self, tracking_number: str, location: str):
        self.tracking_number = tracking_number
        self.location = location

    def get_location(self) -> str:
        return f"Package Location: {self.location}"


@singledispatch
def parse(_) -> str:
    return "Unknown object"


@parse.register
def _(obj: Describable) -> str:
    return obj.describe()


@parse.register
def _(obj: Identifiable) -> str:
    return obj.get_id()


@parse.register
def _(obj: Trackable) -> str:
    return obj.get_location()


def main() -> None:
    # Examples
    user = User("Alice")
    product = Product("12345", "Laptop")
    package = Package("TRACK123", "New York")

    print(parse(user))
    print(parse(product))
    print(parse(package))


if __name__ == "__main__":
    main()
