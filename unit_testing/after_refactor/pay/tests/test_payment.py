import pytest
from pay.order import LineItem, Order
from pay.payment import pay_order
from pay.processor import PaymentProcessor
from pytest import MonkeyPatch


@pytest.fixture
def payment_processor(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(PaymentProcessor, "_check_api_key", lambda _: True)
    return PaymentProcessor("")


def test_pay_order(monkeypatch: MonkeyPatch, payment_processor: PaymentProcessor):
    inputs = ["1249190007575069", "12", "2024"]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    order = Order()
    pay_order(order, payment_processor)


def test_pay_order_invalid(
    monkeypatch: MonkeyPatch, payment_processor: PaymentProcessor
):
    with pytest.raises(ValueError):
        inputs = ["1249190007575068", "12", "2024"]
        monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
        order = Order()
        pay_order(order, payment_processor)
