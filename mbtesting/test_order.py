import unittest

import hypothesis.strategies as st
from hypothesis.stateful import Bundle, RuleBasedStateMachine, rule
from order import LineItem, Order

LINE_ITEMS: Bundle[LineItem] = Bundle("line_items")


class OrderTest(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.order = Order("John Doe", [])

    @rule(
        target=LINE_ITEMS,
        description=st.text(),
        price=st.integers(),
        quantity=st.integers(),
    )
    def add_line_item(self, description: str, price: int, quantity: int) -> LineItem:
        return LineItem(description, price, quantity)

    @rule(line_item=LINE_ITEMS)
    def add_line_item_to_order(self, line_item: LineItem) -> None:
        self.order.add_line_item(line_item)

    @rule(line_item=LINE_ITEMS)
    def remove_line_item_from_order(self, line_item: LineItem) -> None:
        self.order.remove_line_item(line_item)

    @rule(line_item=LINE_ITEMS, quantity=st.integers())
    def update_line_item_quantity(self, line_item: LineItem, quantity: int) -> None:
        self.order.update_li_quantity(line_item, quantity)

    @rule()
    def total_agrees(self) -> None:
        assert sum(li.total for li in self.order.line_items) == self.order.total


OrderTestCase: unittest.TestCase = OrderTest.TestCase
