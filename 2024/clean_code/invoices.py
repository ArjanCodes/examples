from datetime import datetime, timedelta

import stripe
from mb_invoice import (
    InvoiceDelivery,
    book_payment,
    create_financial_statement,
    create_mb_invoice,
    create_payment_for_invoice,
    create_transaction_for_invoice,
    send_mb_invoice,
)
from processing import construct_invoice_data_from_stripe
from settings import PAYMENT_PROCESSING_FEE_LEDGER_ACCOUNT_ID, STRIPE_MB_ACCOUNT_ID


def get_successful_payment_intents(hours_ago: int) -> stripe.ListObject:
    # Calculate the timestamp for 'hours_ago'
    timestamp = int((datetime.now() - timedelta(hours=hours_ago)).timestamp())

    # Retrieve payment intents created since 'timestamp'
    payment_intents = stripe.PaymentIntent.list(created={"gte": timestamp})

    return payment_intents


def can_process_pi(payment_intent: stripe.PaymentIntent) -> bool:
    # check that the payment intent is successful
    if not payment_intent["status"] == "succeeded":
        print(f"Payment intent {payment_intent['id']} is not successful.")
        return False
    return True


def create_and_send_invoice(
    payment_intent: stripe.PaymentIntent,
    delivery_method: InvoiceDelivery,
):
    print(f"Creating invoice for payment intent {payment_intent['id']}.")

    # construct the invoice data
    invoice_data = construct_invoice_data_from_stripe(payment_intent)

    # create an invoice in Moneybird
    invoice = create_mb_invoice(invoice_data)

    # create a financial statement for the application fee
    print("Creating financial statement for application fee.")
    application_fee = invoice_data.get("application_fee", 0.0)

    financial_statement = create_financial_statement(
        datetime.now().strftime("%Y-%m-%d"),
        -application_fee,
        STRIPE_MB_ACCOUNT_ID,
        f"{payment_intent['id']}/application_fee",
    )

    # book the payment for the application fee
    mutation_id = financial_statement["financial_mutations"][0]["id"]
    book_payment(
        mutation_id,
        application_fee,
        PAYMENT_PROCESSING_FEE_LEDGER_ACCOUNT_ID,
    )

    # create payment for the invoice
    payment_data = create_transaction_for_invoice(
        invoice, STRIPE_MB_ACCOUNT_ID, payment_intent["id"]
    )

    # send the invoice to the customer
    print(f"Sending invoice {invoice['id']}.")
    print(send_mb_invoice(invoice["id"], delivery_method))

    # book the payment
    print(f"Booking payment for invoice {invoice['id']}.")
    create_payment_for_invoice(invoice["id"], payment_data)
