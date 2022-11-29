import unittest

import hypothesis.strategies as st
from hypothesis.stateful import Bundle, RuleBasedStateMachine, precondition, rule
from order import LineItem, Order


class OrderTest(RuleBasedStateMachine):
    line_items: Bundle[LineItem] = Bundle("line_items")

    def __init__(self) -> None:
        super().__init__()
        self.order = Order("John Doe", [])

    @rule(
        target=line_items,
        description=st.text(),
        price=st.integers(),
        quantity=st.integers(),
    )
    def create_line_item(self, description: str, price: int, quantity: int) -> LineItem:
        return LineItem(description, price, quantity)

    @rule(line_item=line_items)
    def add_line_item_to_order(self, line_item: LineItem) -> None:
        self.order.add_line_item(line_item)

    @rule(line_item=line_items)
    def remove_line_item_from_order(self, line_item: LineItem) -> None:
        self.order.remove_line_item(line_item)

    @rule(line_item=line_items, quantity=st.integers())
    def update_line_item_quantity(self, line_item: LineItem, quantity: int) -> None:
        self.order.update_li_quantity(line_item, quantity)

    @rule()
    def total_agrees(self) -> None:
        assert sum(li.total for li in self.order.line_items) == self.order.total

    @precondition(lambda self: len(self.order.line_items) == 0)
    @rule()
    def total_agrees_zero(self) -> None:
        assert self.order.total == 0


OrderTestCase: unittest.TestCase = OrderTest.TestCase
