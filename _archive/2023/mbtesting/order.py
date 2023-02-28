from dataclasses import dataclass, field


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
    line_items: list[LineItem] = field(default_factory=list)
    _total_cache: int = 0

    def __post_init__(self) -> None:
        self._update_total_cache()

    def add_line_item(self, line_item: LineItem) -> None:
        self.line_items.append(line_item)
        self._update_total_cache()

    def remove_line_item(self, line_item: LineItem) -> None:
        if not line_item in self.line_items:
            return
        self.line_items.remove(line_item)
        self._update_total_cache()

    def update_li_quantity(self, line_item: LineItem, quantity: int) -> None:
        if not line_item in self.line_items:
            return
        line_item.quantity = quantity
        self._update_total_cache()

    def _update_total_cache(self) -> None:
        self._total_cache = sum(li.total for li in self.line_items)

    @property
    def total(self) -> int:
        return self._total_cache
