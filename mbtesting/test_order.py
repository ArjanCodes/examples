from order import LineItem, Order


def test_order() -> None:
    order = Order("John Doe", [])
    order.add_line_item(LineItem("Apple", 1, 2))
    order.add_line_item(LineItem("Banana", 3, 4))
    order.add_line_item(LineItem("Cherry", 5, 6))
    assert order.total == 44


def test_line_item() -> None:
    line_item = LineItem("Apple", 1, 2)
    assert line_item.total == 2


def test_remove_line_item() -> None:
    apple = LineItem("Apple", 1, 2)
    banana = LineItem("Banana", 3, 4)
    cherry = LineItem("Cherry", 5, 6)
    order = Order("John Doe", [apple, banana, cherry])
    order.remove_line_item(apple)
    assert order.total == 42


def test_update_li_quantity() -> None:
    apple = LineItem("Apple", 1, 2)
    banana = LineItem("Banana", 3, 4)
    cherry = LineItem("Cherry", 5, 6)
    order = Order("John Doe", [apple, banana, cherry])
    order.update_li_quantity(apple, 3)
    assert order.total == 45
