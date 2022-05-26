from pay.order import LineItem


def test_line_item_total() -> None:
    line_item = LineItem(name="Test", price=100)
    assert line_item.total == 100


def test_line_item_total_quantity() -> None:
    line_item = LineItem(name="Test", price=100, quantity=2)
    assert line_item.total == 200
