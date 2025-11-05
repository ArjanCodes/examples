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


def approve_order(order: Order, user: User) -> str:
    """A tangled, messy function that we’ll clean up in the video."""
    try:
        if user.is_premium:
            if order.amount > 1000:
                if not order.has_discount:
                    if user.region != "EU":
                        for item in order.items:
                            if item.price < 0:
                                return "rejected"
                        return "approved"
                    else:
                        if order.currency == "EUR":
                            return "approved"
                        else:
                            return "rejected"
                else:
                    return "rejected"
            else:
                if order.type == "bulk" and not user.is_trial:
                    return "approved"
                else:
                    return "rejected"
        else:
            if user.is_admin:
                return "approved"
            else:
                return "rejected"
    except Exception:
        # Just to be safe
        return "rejected"


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
