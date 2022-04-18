from dataclasses import dataclass, field


@dataclass
class LineItem:
    name: str
    price: int
    quantity: int = 1

    @property
    def total(self) -> int:
        return self.price * self.quantity


@dataclass
class Order:
    line_items: list[LineItem] = field(default_factory=list)

    @property
    def total(self) -> int:
        return sum(item.total for item in self.line_items)
