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
    if order.amount <= 1000 and order.type != "bulk" or user.is_trial:
        return "rejected"
    if order.has_discount:
        return "rejected"
    if user.region == "EU" and order.currency != "EUR":
        return "rejected"
    for item in order.items:
        if item.price < 0:
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
