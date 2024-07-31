import os
from datetime import datetime
from typing import Any

import stripe


def compute_gross_profit(invoice: dict[str, Any]) -> float:
    return invoice["amount"] - invoice["application_fee"]


def init_stripe_api() -> None:
    # initialize the Stripe API
    stripe.api_key = os.getenv("STRIPE_KEY")


def get_application_fee(payment_intent: stripe.PaymentIntent) -> int:
    charge_id = payment_intent["latest_charge"]
    charge = stripe.Charge.retrieve(charge_id)
    if not charge:
        raise ValueError(f"Charge with id {charge_id} not found.")

    balance_transaction = stripe.BalanceTransaction.retrieve(
        charge["balance_transaction"]
    )
    if not balance_transaction:
        raise ValueError("Balance transaction not found.")

    return balance_transaction["fee"]


def construct_invoice_data_from_stripe(
    payment_intent: stripe.PaymentIntent,
) -> dict[str, Any]:
    # retrieve the customer from stripe
    customer = stripe.Customer.retrieve(payment_intent["customer"])

    # check if customer has metadata
    if "mb_contact_id" not in customer.get("metadata", {}):
        raise ValueError("Customer does not have a Moneybird contact ID.")

    # determine the application fee
    application_fee = get_application_fee(payment_intent)

    return {
        "contact_id": customer["metadata"]["mb_contact_id"],
        "invoice_date": datetime.fromtimestamp(payment_intent["created"]),
        "currency": payment_intent["currency"],
        "description": payment_intent["description"],
        "amount": payment_intent["amount"] / 100,
        "stripe_payment_intent_id": payment_intent["id"],
        "application_fee": application_fee / 100,
        "prices_are_incl_tax": True,
    }


def construct_invoice_data_from_stripe_with_errors(
    payment_intent: stripe.PaymentIntent,
) -> dict[str, Any]:
    # retrieve the customer from stripe
    customer = stripe.Customer.retrieve(payment_intent["customer"])

    # determine the application fee
    try:
        try:
            application_fee = get_application_fee(payment_intent)
        except ValueError as e:
            print(f"Failed to retrieve application fee: {e}")
            raise

        try:
            return {
                "contact_id": customer["metadata"]["mb_contact_id"],
                "invoice_date": datetime.fromtimestamp(payment_intent["created"]),
                "currency": payment_intent["currency"],
                "description": payment_intent["description"],
                "amount": payment_intent["amount"] / 100,
                "stripe_payment_intent_id": payment_intent["id"],
                "application_fee": application_fee / 100,
                "prices_are_incl_tax": True,
            }
        except KeyError as e:
            print(f"Failed to construct invoice data: {e}")
            raise
    except Exception as e:
        print(f"Failed to construct invoice data: {e}")
        raise
