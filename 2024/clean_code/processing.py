from datetime import datetime

import stripe
from mb_invoice import CreateInvoiceData


def construct_invoice_data_from_stripe(
    payment_intent: stripe.PaymentIntent,
) -> CreateInvoiceData:
    # retrieve the customer from stripe
    customer = stripe.Customer.retrieve(payment_intent["customer"])

    # if there's an invoice related to the payment intent, get the description from there
    if payment_intent["invoice"]:
        invoice = stripe.Invoice.retrieve(payment_intent["invoice"])
        data = invoice.get("lines", {}).get("data", [{}])[0]
        description = data.get("plan", {}).get("nickname", "")
        if description:
            payment_intent["description"] = description

    invoice_data = CreateInvoiceData(
        {
            "contact_id": customer["metadata"]["mb_contact_id"],
            "invoice_date": datetime.utcfromtimestamp(payment_intent["created"]),
            "currency": payment_intent["currency"],
            "description": payment_intent["description"],
            "amount": payment_intent["amount"] / 100,
            "stripe_payment_intent_id": payment_intent["id"],
        }
    )

    # get the latest charge
    charge_id = payment_intent["latest_charge"]
    charge = stripe.Charge.retrieve(charge_id)
    if not charge:
        raise ValueError(f"Charge with id {charge_id} not found.")

    # retrieve the balance transaction
    balance_transaction = stripe.BalanceTransaction.retrieve(
        charge["balance_transaction"]
    )
    if not balance_transaction:
        raise ValueError("Balance transaction not found.")

    # store the application fee
    invoice_data["application_fee"] = balance_transaction["fee"] / 100

    return invoice_data
