from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Customer:
    id: int
    name: str
    tier: str


@dataclass(frozen=True)
class OrderItem:
    price: Decimal
    quantity: int


@dataclass(frozen=True)
class Order:
    customer_id: int
    status: str
    items: list[OrderItem]


@dataclass(frozen=True)
class CustomerSummary:
    customer_name: str
    paid_orders: int
    total_spent: Decimal


def generate_customer_report(
    customers: list[Customer],
    orders: list[Order],
) -> list[CustomerSummary]:
    report: list[CustomerSummary] = []

    for customer in customers:
        total_spent = Decimal("0")
        paid_order_count = 0

        for order in orders:
            if order.customer_id == customer.id:
                if order.status == "paid":
                    order_total = Decimal("0")

                    for item in order.items:
                        order_total += item.price * item.quantity

                    if customer.tier == "premium" and order_total > Decimal("100"):
                        order_total *= Decimal("0.9")

                    total_spent += order_total
                    paid_order_count += 1

        if paid_order_count > 0:
            report.append(
                CustomerSummary(
                    customer_name=customer.name,
                    paid_orders=paid_order_count,
                    total_spent=total_spent,
                )
            )

    return report


def main() -> None:
    customers = [
        Customer(id=1, name="Alice", tier="premium"),
        Customer(id=2, name="Bob", tier="standard"),
    ]

    orders = [
        Order(
            customer_id=1,
            status="paid",
            items=[
                OrderItem(price=Decimal("30"), quantity=2),
                OrderItem(price=Decimal("50"), quantity=1),
            ],
        ),
        Order(
            customer_id=1,
            status="pending",
            items=[
                OrderItem(price=Decimal("20"), quantity=1),
            ],
        ),
        Order(
            customer_id=2,
            status="paid",
            items=[
                OrderItem(price=Decimal("40"), quantity=1),
            ],
        ),
    ]

    report = generate_customer_report(customers, orders)

    for summary in report:
        print(
            f"{summary.customer_name}: "
            f"{summary.paid_orders} orders, "
            f"total spent = {summary.total_spent}"
        )


if __name__ == "__main__":
    main()
