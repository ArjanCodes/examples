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


def can_process_pi(payment_intent: stripe.PaymentIntent) -> bool:
    # check that the payment intent is successful
    if not payment_intent["status"] == "succeeded":
        print(f"Payment intent {payment_intent['id']} is not successful.")
        return False
    return True


def get_successful_payment_intents(hours_ago: int) -> list[stripe.PaymentIntent]:
    timestamp = calculate_timestamp(hours_ago)

    # Retrieve payment intents created since 'timestamp'
    payment_intents = stripe.PaymentIntent.list(created={"gte": timestamp})

    # return payment intents as a Python list
    return [pi for pi in payment_intents]


def construct_invoice_data_from_stripe(
    payment_intent: stripe.PaymentIntent,
) -> InvoiceData:
    # retrieve the customer from stripe
    customer = stripe.Customer.retrieve(payment_intent["customer"])

    # get the latest charge
    charge_id = str(payment_intent["latest_charge"])
    charge = stripe.Charge.retrieve(charge_id)
    if not charge:
        raise ValueError(f"Charge with id {charge_id} not found.")

    # retrieve the balance transaction
    balance_transaction = stripe.BalanceTransaction.retrieve(
        charge["balance_transaction"]
    )
    if not balance_transaction:
        raise ValueError("Balance transaction not found.")

    return InvoiceData(
        contact_id=customer["metadata"]["mb_contact_id"],
        invoice_date=datetime.fromtimestamp(payment_intent["created"]),
        currency=payment_intent["currency"],
        description=payment_intent["description"],
        amount=payment_intent["amount"] / 100,
        stripe_payment_intent_id=payment_intent["id"],
        application_fee=balance_transaction["fee"] / 100,
        prices_are_incl_tax=True,
    )
