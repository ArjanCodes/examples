from datetime import datetime
from enum import StrEnum
from typing import Any

from mb_core import post_moneybird_request
from pydantic import BaseModel

# Base currency
BASE_CURRENCY = "eur"

# Custom field id for sales invoices
STRIPE_PAYMENT_INTENT_ID_FIELD = 397516880050390023

# Ledger account id
PAYMENT_PROCESSING_FEE_LEDGER_ID = 390625287760512749

# Financial account id
STRIPE_MB_ACCOUNT_ID = 390699078567069053

# VAT id
NL_VAT_ID = 375843957029996104


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


def create_and_send_invoice(
    invoice_data: InvoiceData,
    delivery_method: InvoiceDelivery,
) -> dict[str, Any]:
    print(
        f"Creating invoice for payment intent {invoice_data.stripe_payment_intent_id}."
    )

    # create an invoice in Moneybird
    invoice = create_mb_invoice(invoice_data)

    # send the invoice to the customer
    print(f"Sending invoice {invoice['id']}.")
    print(send_mb_invoice(invoice["id"], delivery_method))

    return invoice


def book_invoice(invoice_data: InvoiceData, invoice: dict[str, Any]):
    # create a financial statement for the application fee
    print("Creating financial statement for application fee.")
    mutation_id = create_financial_statement(
        datetime.now().strftime("%Y-%m-%d"),
        -invoice_data.application_fee,
        STRIPE_MB_ACCOUNT_ID,
        f"{invoice_data.stripe_payment_intent_id}/application_fee",
    )

    # book the payment for the application fee
    book_payment(
        mutation_id,
        -invoice_data.application_fee,
        PAYMENT_PROCESSING_FEE_LEDGER_ID,
    )

    # create payment for the invoice
    payment_data = create_transaction_for_invoice(
        invoice, STRIPE_MB_ACCOUNT_ID, invoice_data.stripe_payment_intent_id
    )

    # book the payment
    print(f"Booking payment for invoice {invoice['id']}.")
    create_payment_for_invoice(invoice["id"], payment_data)


def create_mb_invoice(data: InvoiceData):
    invoice_data = {
        "contact_id": data.contact_id,
        "invoice_date": data.invoice_date.strftime("%Y-%m-%d"),
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


def create_transaction_for_invoice(
    invoice: dict[str, Any],
    account_id: int,
    reference: str,
) -> dict[str, Any]:
    # determine the amount
    amount = float(invoice.get("total_price_incl_tax", 0))

    # create a financial statement with the transaction
    print(f"Creating transaction for {amount} {BASE_CURRENCY}.")
    mutation_id = create_financial_statement(
        invoice["invoice_date"],
        amount,
        account_id,
        reference,
    )

    return {
        "price": invoice["total_price_incl_tax"],
        "payment_date": invoice["invoice_date"],
        "manual_payment_action": "bank_transfer",
        "financial_account_id": account_id,
        "financial_mutation_id": mutation_id,
    }


def create_payment_for_invoice(invoice_id: int, payment_data: dict[str, Any]):
    return post_moneybird_request(
        f"sales_invoices/{invoice_id}/payments",
        {"payment": payment_data},
    )


def create_financial_statement(
    date: str, amount: float, account_id: int, reference: str
) -> int:
    financial_statement = post_moneybird_request(
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

    # return the financial mutation id
    return int(financial_statement["financial_mutations"][0]["id"])


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
