import os
from datetime import datetime, timedelta

import stripe
from invoices import InvoiceData


def calculate_timestamp(hours_ago: int) -> int:
    timestamp = int((datetime.now() - timedelta(hours=hours_ago)).timestamp())
    return timestamp


def init_stripe_api() -> None:
    # initialize the Stripe API
    stripe.api_key = os.getenv("STRIPE_KEY")


def get_successful_payment_intents(hours_ago: int) -> list[stripe.PaymentIntent]:
    timestamp = calculate_timestamp(hours_ago)

    # Retrieve payment intents created since 'timestamp'
    payment_intents = stripe.PaymentIntent.list(created={"gte": timestamp})

    # return filtered payment intents by succeeded status
    return [pi for pi in payment_intents if pi["status"] == "succeeded"]


def get_application_fee(charge_id: str) -> int:
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
) -> InvoiceData:
    # retrieve the customer from stripe
    customer = stripe.Customer.retrieve(payment_intent["customer"])

    # determine the application fee
    charge_id = str(payment_intent["latest_charge"])
    application_fee = get_application_fee(charge_id)

    return InvoiceData(
        contact_id=customer["metadata"]["mb_contact_id"],
        invoice_date=datetime.fromtimestamp(payment_intent["created"]),
        currency=payment_intent["currency"],
        description=payment_intent["description"],
        amount=payment_intent["amount"] / 100,
        stripe_payment_intent_id=payment_intent["id"],
        application_fee=application_fee / 100,
        prices_are_incl_tax=True,
    )
