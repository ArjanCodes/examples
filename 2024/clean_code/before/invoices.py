from datetime import datetime
from enum import StrEnum
from typing import Any

import stripe
from moneybird import post_moneybird_request
from processing import construct_invoice_data_from_stripe
from pydantic import BaseModel

# Base currency
BASE_CURRENCY = "eur"

# Custom field id for sales invoices
STRIPE_PAYMENT_INTENT_ID_FIELD = 456789012345678901
APPLICATION_FEE_FIELD = 567890123456789012

# Ledger account id
PAYMENT_PROCESSING_FEE_LEDGER_ID = 678901234567890123

# Financial account id
STRIPE_MB_ACCOUNT_ID = 234567890123456789

# VAT id
NL_VAT_ID = 890123456789012345


class InvoiceDelivery(StrEnum):
    SKIP = "Skip"
    EMAIL = "Email"
    MANUAL = "Manual"


class InvoiceData(BaseModel):
    contact_id: int
    invoice_date: datetime
    prices_are_incl_tax: bool
    currency: str
    stripe_payment_intent_id: str
    description: str
    amount: float
    application_fee: float


def create_mb_invoice(data: InvoiceData):
    invoice_data = {
        "contact_id": data.contact_id,
        "invoice_date": data.invoice_date,
        "prices_are_incl_tax": data.prices_are_incl_tax,
        "currency": data.currency,
        "first_due_interval": 0,
        "details_attributes": [
            {
                "description": data.description,
                "price": data.amount,
                "tax_rate_id": NL_VAT_ID,
            }
        ],
        "custom_fields_attributes": {
            "0": {
                "id": STRIPE_PAYMENT_INTENT_ID_FIELD,
                "value": data.stripe_payment_intent_id,
            }
        },
    }

    return post_moneybird_request("sales_invoices", {"sales_invoice": invoice_data})


def send_mb_invoice(
    invoice_id: int, delivery_method: InvoiceDelivery = InvoiceDelivery.EMAIL
):
    return post_moneybird_request(
        f"sales_invoices/{invoice_id}/send_invoice",
        {"sales_invoice_sending": {"delivery_method": delivery_method.value}},
        method="PATCH",
    )


def create_financial_statement(
    date: str, amount: float, account_id: int, reference: str
):
    return post_moneybird_request(
        "financial_statements",
        {
            "financial_statement": {
                "financial_account_id": account_id,
                "reference": reference,
                "financial_mutations_attributes": {
                    "1": {
                        "date": date,
                        "amount": amount,
                        "message": reference,
                    }
                },
            }
        },
        method="POST",
    )


def create_and_send_invoice(
    payment_intent: stripe.PaymentIntent,
    delivery_method: InvoiceDelivery,
):
    print(f"Creating invoice for payment intent {payment_intent['id']}.")

    # construct the invoice data
    invoice_data = construct_invoice_data_from_stripe(payment_intent)
    if not invoice_data:
        print(
            f"Could not construct invoice data for payment intent {payment_intent['id']}."
        )
        return

    # create an invoice in Moneybird
    invoice = create_mb_invoice(invoice_data)

    # create a financial statement for the application fee
    financial_statement = create_financial_statement(
        invoice["invoice_date"],
        -invoice_data.application_fee,
        STRIPE_MB_ACCOUNT_ID,
        f"{payment_intent['id']}/application_fee",
    )

    # book the payment for the application fee
    mutation_id = int(financial_statement["financial_mutations"][0]["id"])
    book_payment(
        mutation_id,
        invoice_data.application_fee,
        PAYMENT_PROCESSING_FEE_LEDGER_ID,
    )

    # create a financial statement for the invoice amount
    financial_statement = create_financial_statement(
        invoice["invoice_date"],
        invoice_data.amount,
        STRIPE_MB_ACCOUNT_ID,
        f"{payment_intent['id']}",
    )

    # send the invoice to the customer
    print(f"Sending invoice {invoice['id']}.")
    print(send_mb_invoice(invoice["id"], delivery_method))

    # create payment for the invoice
    mutation_id = int(financial_statement["financial_mutations"][0]["id"])
    book_invoice_payment(invoice, STRIPE_MB_ACCOUNT_ID, mutation_id)


def book_invoice_payment(
    invoice: dict[str, Any],
    account_id: int,
    mutation_id: int,
) -> dict[str, Any]:
    return post_moneybird_request(
        f"sales_invoices/{invoice["id"]}/payments",
        {
            "payment": {
                "price": invoice["total_price_incl_tax"],
                "payment_date": invoice["invoice_date"],
                "manual_payment_action": "bank_transfer",
                "financial_account_id": account_id,
                "financial_mutation_id": mutation_id,
            }
        },
    )


def book_payment(mutation_id: int, amount: float, booking_id: int):
    return post_moneybird_request(
        f"financial_mutations/{mutation_id}/link_booking",
        {
            "booking_type": "LedgerAccount",
            "booking_id": booking_id,
            "price_base": str(amount),
        },
        method="PATCH",
    )
