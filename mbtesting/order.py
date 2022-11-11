from dataclasses import dataclass


@dataclass
class LineItem:
    description: str
    price: int
    quantity: int

    @property
    def total(self) -> int:
        return self.price * self.quantity


@dataclass
class Order:
    customer: str
    line_items: list[LineItem]
    _total_cache: int = 0

    def add_line_item(self, line_item: LineItem) -> None:
        self.line_items.append(line_item)
        self._total_cache += line_item.total

    def remove_line_item(self, line_item: LineItem) -> None:
        if not line_item in self.line_items:
            return
        self._total_cache -= line_item.total
        self.line_items.remove(line_item)

    def update_li_quantity(self, line_item: LineItem, quantity: int) -> None:
        if not line_item in self.line_items:
            return
        self._total_cache -= line_item.total
        line_item.quantity = quantity
        self._total_cache += line_item.total

    @property
    def total(self) -> int:
        return self._total_cache
