import pytest
from pay.order import LineItem, Order, OrderStatus
from pay.payment import pay_order
from pay.processor import PaymentProcessor
from pytest import MonkeyPatch


@pytest.fixture
def payment_processor(monkeypatch: MonkeyPatch) -> PaymentProcessor:
    monkeypatch.setattr(PaymentProcessor, "_check_api_key", lambda _: True)
    return PaymentProcessor("")


def test_pay_order(
    monkeypatch: MonkeyPatch, payment_processor: PaymentProcessor
) -> None:
    inputs = ["1249190007575069", "12", "2024"]
    monkeypatch.setattr("builtins.input", name=lambda _: inputs.pop(0))
    order = Order()
    order.line_items.append(LineItem(name="Shoes", price=100_00, quantity=2))
    pay_order(order, payment_processor)
    assert order.status == OrderStatus.PAID


def test_pay_order_invalid(
    monkeypatch: MonkeyPatch, payment_processor: PaymentProcessor
) -> None:
    with pytest.raises(ValueError):
        inputs = ["1249190007575069", "12", "2024"]
        monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
        order = Order()
        pay_order(order, payment_processor)
