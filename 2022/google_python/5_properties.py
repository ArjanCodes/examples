from dataclasses import dataclass, field


@dataclass
class LineItem:
    name: str
    price: int
    quantity: int = 1

    @property
    def total_price(self) -> int:
        return self.price * self.quantity


@dataclass
class Order:
    items: list[LineItem] = field(default_factory=list)

    def add_item(self, item: LineItem):
        self.items.append(item)

    @property
    def total_price(self) -> int:
        return sum(item.total_price for item in self.items)


def main():
    order = Order()
    order.add_item(LineItem("carrots", price=20, quantity=10))
    order.add_item(LineItem("self-raising flower", price=200))
    order.add_item(LineItem("eggs", price=20, quantity=5))
    order.add_item(LineItem("gingerbread spices", price=189))
    order.add_item(LineItem("sunflower oil", price=169))
    order.add_item(LineItem("brown sugar", price=99))
    order.add_item(LineItem("lemon", price=25))
    order.add_item(LineItem("ginger", price=79))
    order.add_item(LineItem("raisins", price=159))
    order.add_item(LineItem("powdered sugar", price=89))
    order.add_item(LineItem("cream cheese", price=219, quantity=2))

    print(f"Total price: ${order.total_price / 100:.2f}")


if __name__ == "__main__":
    main()
