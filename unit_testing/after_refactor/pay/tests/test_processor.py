import os

import pytest
from dotenv import load_dotenv
from pay.processor import PaymentProcessor, luhn_checksum

load_dotenv()

API_KEY = os.getenv("API_KEY") or ""


def test_invalid_api_key() -> None:
    with pytest.raises(ValueError):
        payment_processor = PaymentProcessor("")
        payment_processor.charge("1249190007575069", 12, 2024, 100)


def test_card_number_valid_date() -> None:
    payment_processor = PaymentProcessor(API_KEY)
    assert payment_processor.validate_card("1249190007575069", 12, 2024)


def test_card_number_invalid_date() -> None:
    payment_processor = PaymentProcessor(API_KEY)
    assert not payment_processor.validate_card("1249190007575069", 12, 1900)


def test_card_number_invalid_luhn() -> None:
    assert not luhn_checksum("1249190007575068")


def test_card_number_valid_luhn() -> None:
    assert luhn_checksum("1249190007575069")


def test_charge_card_valid() -> None:
    payment_processor = PaymentProcessor(API_KEY)
    payment_processor.charge("1249190007575069", 12, 2024, 100)


def test_charge_card_invalid() -> None:
    with pytest.raises(ValueError):
        payment_processor = PaymentProcessor(API_KEY)
        payment_processor.charge("1249190007575068", 12, 2024, 100)
