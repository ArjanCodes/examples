import pytest
from pay.processor import PaymentProcessor, luhn_checksum

API_KEY = "6cfb67f3-6281-4031-b893-ea85db0dce20"


def test_card_number_valid_date():
    payment_processor = PaymentProcessor(API_KEY)
    assert payment_processor.validate_card("1249190007575069", 12, 2024)


def test_card_number_invalid_date():
    payment_processor = PaymentProcessor(API_KEY)
    assert not payment_processor.validate_card("1249190007575069", 12, 1900)


def test_card_number_invalid_luhn():
    payment_processor = PaymentProcessor(API_KEY)
    assert not luhn_checksum("1249190007575068")


def test_card_number_valid_luhn():
    payment_processor = PaymentProcessor(API_KEY)
    assert luhn_checksum("1249190007575069")


def test_charge_card_valid():
    print("API KEYU ", API_KEY)
    payment_processor = PaymentProcessor(API_KEY)
    payment_processor.charge("1249190007575069", 12, 2024, 100)


def test_charge_card_invalid():
    with pytest.raises(ValueError):
        payment_processor = PaymentProcessor(API_KEY)
        payment_processor.charge("1249190007575068", 12, 2024, 100)
