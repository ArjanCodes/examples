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


def is_eligible_amount(order: Order, user: User) -> bool:
    return order.amount > 1000 or (order.type == "bulk" and not user.is_trial)


def has_valid_currency(order: Order, user: User) -> bool:
    return not (user.region == "EU" and order.currency != "EUR")


def approve_order(order: Order, user: User) -> str:
    # 1) Privilege/override gate
    if user.is_admin:
        return "approved"

    # 2) Policy gate (rejections for non-admins)
    if not user.is_premium:
        return "rejected"
    if order.amount is None:
        return "rejected"
    if not is_eligible_amount(order, user):
        return "rejected"
    if order.has_discount:
        return "rejected"
    if not has_valid_currency(order, user):
        return "rejected"
    if any(item.price < 0 for item in order.items):
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
