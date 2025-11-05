from dataclasses import dataclass, field


@dataclass
class Item:
    name: str
    price: float


@dataclass
class Order:
    amount: float
    has_discount: bool
    region: str
    currency: str
    type: str  # e.g. "bulk" or "normal"
    items: list[Item] = field(default_factory=list)


@dataclass
class User:
    is_premium: bool
    is_admin: bool
    is_trial: bool
    region: str


VALID_REGION_CURRENCY = {
    ("EU", "EUR"): True,
    ("US", "USD"): True,
    ("UK", "GBP"): True,
}


def has_valid_currency(order: Order, user: User) -> bool:
    return VALID_REGION_CURRENCY.get((user.region, order.currency), False)


def is_eligible_amount(order: Order, user: User) -> bool:
    return order.amount > 1000 or (order.type == "bulk" and not user.is_trial)


def approve_order(order: Order, user: User) -> str:
    # 1) Privilege/override gate
    if user.is_admin:
        return "approved"

    # 2) Policy gate (rejections for non-admins)
    rejection_rules = [
        lambda: not user.is_premium,
        lambda: order.amount is None,
        lambda: order.has_discount,
        lambda: not is_eligible_amount(order, user),
        lambda: not has_valid_currency(order, user),
        lambda: any(item.price < 0 for item in order.items),
    ]

    if any(rule() for rule in rejection_rules):
        return "rejected"
    return "approved"


def main() -> None:
    # Create a sample user and order that barely passes the approval rules
    user = User(
        is_premium=True,
        is_admin=False,
        is_trial=False,
        region="US",
    )

    order = Order(
        amount=1500,
        has_discount=False,
        region="EU",
        currency="USD",
        type="normal",
        items=[
            Item("Keyboard", 100.0),
            Item("Monitor", 200.0),
            Item("Mouse", 50.0),
        ],
    )

    result = approve_order(order, user)
    print(f"Order approval result: {result}")


if __name__ == "__main__":
    main()
