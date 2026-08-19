from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    email: str


@dataclass(frozen=True)
class ImportedOrder:
    order_id: str


def import_customers_from_csv(rows: list[str]) -> list[Customer]:
    return [Customer(email=row) for row in rows if "@" in row]


def import_paid_orders_from_api(records: list[str]) -> list[ImportedOrder]:
    return [
        ImportedOrder(order_id=record.removesuffix(":paid"))
        for record in records
        if record.endswith(":paid")
    ]


def main() -> None:
    customer_rows = ["ada@example.com", "not-an-email"]
    api_records = ["ORD-1:paid", "ORD-2:cancelled"]
    print(import_customers_from_csv(customer_rows))
    print(import_paid_orders_from_api(api_records))


if __name__ == "__main__":
    main()
