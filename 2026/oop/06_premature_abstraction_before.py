from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    email: str


@dataclass(frozen=True)
class ImportedOrder:
    order_id: str


class BaseImporter(ABC):
    def import_records(self) -> list[object]:
        raw_records = self.load()
        return [self.transform(record) for record in raw_records if self.is_valid(record)]

    @abstractmethod
    def load(self) -> list[str]: ...

    @abstractmethod
    def is_valid(self, record: str) -> bool: ...

    @abstractmethod
    def transform(self, record: str) -> object: ...


class CustomerCsvImporter(BaseImporter):
    def load(self) -> list[str]:
        return ["ada@example.com", "not-an-email"]

    def is_valid(self, record: str) -> bool:
        return "@" in record

    def transform(self, record: str) -> Customer:
        return Customer(email=record)


class OrdersApiImporter(BaseImporter):
    def load(self) -> list[str]:
        return ["ORD-1:paid", "ORD-2:cancelled"]

    def is_valid(self, record: str) -> bool:
        return record.endswith(":paid")

    def transform(self, record: str) -> ImportedOrder:
        return ImportedOrder(order_id=record.removesuffix(":paid"))


def main() -> None:
    print(CustomerCsvImporter().import_records())
    print(OrdersApiImporter().import_records())


if __name__ == "__main__":
    main()
