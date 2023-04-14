import unittest

import hypothesis.strategies as st
import pytest
from hypothesis.stateful import RuleBasedStateMachine, precondition, rule
from order import LineItem, Order


class OrderTest(RuleBasedStateMachine):
    def __init__(self) -> None:
        super().__init__()
        self.order = Order("John Doe", [])
        self.line_items: list[LineItem] = []

    @rule(
        description=st.text(),
        price=st.integers(),
        quantity=st.integers(),
    )
    def create_line_item(self, description: str, price: int, quantity: int) -> None:
        self.line_items.append(LineItem(description, price, quantity))

    @precondition(lambda self: len(self.line_items) > 0)
    @rule(data=st.data())
    def add_line_item_to_order(self, data: st.SearchStrategy) -> None:
        line_item = data.draw(st.sampled_from(self.line_items))
        self.order.add_line_item(line_item)

    # only try to remove line items if there are any in the order
    @precondition(lambda self: len(self.order.line_items) > 0)
    @rule(data=st.data())
    def remove_line_item_from_order(self, data: st.SearchStrategy) -> None:
        line_item = data.draw(st.sampled_from(self.order.line_items))
        self.order.remove_line_item(line_item)

    # check that removing a line item that is not in the order raises an exception
    @precondition(
        lambda self: len(self.order.line_items) == 0 and len(self.line_items) > 0
    )
    @rule(data=st.data())
    def remove_line_item_from_empty_order_raises_exception(
        self, data: st.SearchStrategy
    ) -> None:
        line_item = data.draw(st.sampled_from(self.line_items))
        with pytest.raises(ValueError):
            self.order.remove_line_item(line_item)

    # check that removing a line item that is not in the order raises an exception
    @precondition(
        lambda self: any(x not in self.order.line_items for x in self.line_items)
    )
    @rule(data=st.data())
    def remove_line_item_from_order_raises_exception(
        self, data: st.SearchStrategy
    ) -> None:
        unordered_items = [x for x in self.line_items if x not in self.order.line_items]
        line_item = data.draw(st.sampled_from(unordered_items))
        with pytest.raises(ValueError):
            self.order.remove_line_item(line_item)

    @precondition(lambda self: len(self.line_items) > 0)
    @rule(data=st.data(), quantity=st.integers())
    def update_line_item_quantity(self, data: st.SearchStrategy, quantity: int) -> None:
        line_item = data.draw(st.sampled_from(self.line_items))
        self.order.update_li_quantity(line_item, quantity)

    @rule()
    def total_agrees(self) -> None:
        assert sum(li.total for li in self.order.line_items) == self.order.total

    @precondition(lambda self: len(self.order.line_items) == 0)
    @rule()
    def total_agrees_zero(self) -> None:
        assert self.order.total == 0


OrderTestCase: unittest.TestCase = OrderTest.TestCase
