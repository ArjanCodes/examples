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

    @property
    def total(self) -> Decimal:
        return sum((item.price * item.quantity for item in self.items), Decimal("0"))


@dataclass(frozen=True)
class CustomerSummary:
    customer_name: str
    paid_orders: int
    total_spent: Decimal


def group_orders_by_customer(
    orders: list[Order],
) -> dict[int, list[Order]]:
    orders_by_customer: dict[int, list[Order]] = {}

    for order in orders:
        orders_by_customer.setdefault(order.customer_id, []).append(order)

    return orders_by_customer


def paid_orders(orders: list[Order]) -> list[Order]:
    return [order for order in orders if order.status == "paid"]


def apply_discount(customer: Customer, total: Decimal) -> Decimal:
    if customer.tier == "premium" and total > Decimal("100"):
        return total * Decimal("0.9")

    return total


def build_customer_summary(
    customer: Customer,
    orders: list[Order],
) -> CustomerSummary:
    totals = [apply_discount(customer, order.total) for order in paid_orders(orders)]

    return CustomerSummary(
        customer_name=customer.name,
        paid_orders=len(totals),
        total_spent=sum(totals, Decimal("0")),
    )


def generate_customer_report(
    customers: list[Customer],
    orders: list[Order],
) -> list[CustomerSummary]:
    orders_by_customer = group_orders_by_customer(orders)
    summaries: list[CustomerSummary] = []

    for customer in customers:
        customer_orders = orders_by_customer.get(customer.id, [])

        if not customer_orders:
            continue

        summary = build_customer_summary(customer, customer_orders)
        summaries.append(summary)

    return summaries


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
