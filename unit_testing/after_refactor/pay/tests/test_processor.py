import os
from datetime import date

import pytest
from dotenv import load_dotenv
from pay.card import CreditCard
from pay.processor import PaymentProcessor, luhn_checksum

load_dotenv()

API_KEY = os.getenv("API_KEY") or ""

CC_YEAR = date.today().year + 2


@pytest.fixture
def payment_processor() -> PaymentProcessor:
    return PaymentProcessor(API_KEY)


def test_invalid_api_key() -> None:
    with pytest.raises(ValueError):
        card = CreditCard("1249190007575069", 12, CC_YEAR)
        PaymentProcessor("").charge(card, 100)


def test_card_number_valid_date(payment_processor: PaymentProcessor) -> None:
    card = CreditCard("1249190007575069", 12, CC_YEAR)
    assert payment_processor.validate_card(card)


def test_card_number_invalid_date(payment_processor: PaymentProcessor) -> None:
    card = CreditCard("1249190007575069", 12, 1900)
    assert not payment_processor.validate_card(card)


def test_card_number_invalid_luhn() -> None:
    assert not luhn_checksum("1249190007575068")


def test_card_number_valid_luhn() -> None:
    assert luhn_checksum("1249190007575069")


def test_charge_card_valid(payment_processor: PaymentProcessor) -> None:
    card = CreditCard("1249190007575069", 12, CC_YEAR)
    payment_processor.charge(card, 100)


def test_charge_card_invalid(payment_processor: PaymentProcessor) -> None:
    with pytest.raises(ValueError):
        card = CreditCard("1249190007575068", 12, CC_YEAR)
        payment_processor.charge(card, 100)
