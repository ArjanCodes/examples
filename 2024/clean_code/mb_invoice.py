from datetime import datetime
from enum import Enum
from typing import Any, TypedDict

from mb_core import post_moneybird_request
from settings import (
    NL_VAT_ID,
    STRIPE_PAYMENT_INTENT_ID_FIELD,
)

# Base currency
BASE_CURRENCY = "eur"


class ContactNotFoundError(Exception):
    pass


class InvoiceDelivery(Enum):
    SKIP = "Skip"
    EMAIL = "Email"
    MANUAL = "Manual"


class CreateInvoiceData(TypedDict):
    contact_id: int
    invoice_date: datetime
    prices_are_incl_tax: bool
    currency: str
    stripe_payment_intent_id: str
    description: str
    amount: float
    application_fee: float


def get_mb_contact(contact_id: int):
    return post_moneybird_request(f"contacts/{contact_id}", method="GET")


def create_mb_invoice(data: CreateInvoiceData):
    # find the moneybird contact associated with the email address
    contact = get_mb_contact(data.get("contact_id", 0))
    if not contact:
        # we are not able to find a contact, so abort
        raise ContactNotFoundError()

    # construct the basic invoice data
    invoice_date_str = data["invoice_date"].strftime("%Y-%m-%d")
    invoice_data = {
        "contact_id": data["contact_id"],
        "invoice_date": invoice_date_str,
        "prices_are_incl_tax": True,
        "currency": data["currency"],
        "first_due_interval": 0,
        "details_attributes": [
            {
                "description": data["description"],
                "price": data["amount"],
                "tax_rate_id": NL_VAT_ID,
            }
        ],
        "custom_fields_attributes": {
            "0": {
                "id": STRIPE_PAYMENT_INTENT_ID_FIELD,
                "value": data["stripe_payment_intent_id"],
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

    # determine the payment date
    payment_date = invoice.get("invoice_date", datetime.today().isoformat())

    # create a financial statement with the transaction
    print(f"Creating transaction for {amount} {BASE_CURRENCY}.")
    financial_statement = create_financial_statement(
        payment_date,
        amount,
        account_id,
        reference,
    )

    # return the financial mutation id
    mutation_id = financial_statement["financial_mutations"][0]["id"]

    payment_data = {
        "price": invoice["total_price_incl_tax"],
        "payment_date": payment_date,
        "manual_payment_action": "bank_transfer",
        "financial_account_id": account_id,
        "financial_mutation_id": mutation_id,
    }

    return payment_data


def create_payment_for_invoice(invoice_id: int, payment_data: dict[str, Any]):
    return post_moneybird_request(
        f"sales_invoices/{invoice_id}/payments",
        {"payment": payment_data},
    )


def create_financial_statement(
    date: str, amount: float, account_id: int, reference: str
):
    # create a financial statement with the transaction
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
