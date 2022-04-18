import pytest
from pay.order import LineItem, Order
from pay.payment import pay_order
from pytest import MonkeyPatch


def test_pay_order(monkeypatch: MonkeyPatch):
    inputs = ["1249190007575069", "12", "2024"]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    order = Order()
    pay_order(order)


def test_pay_order_invalid(monkeypatch: MonkeyPatch):
    with pytest.raises(ValueError):
        inputs = ["1249190007575068", "12", "2024"]
        monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
        order = Order()
        pay_order(order)
