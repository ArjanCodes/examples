import stripe
from dotenv import load_dotenv
from invoices import (
    InvoiceDelivery,
    book_invoice,
    create_and_send_invoice,
)
from stripe_api_helpers import (
    construct_invoice_data_from_stripe,
    get_successful_payment_intents,
    init_stripe_api,
)

PROCESS_INVOICES_PERIOD = 24  # hours


def create_invoice(payment_intent: stripe.PaymentIntent) -> None:
    # construct the invoice data
    invoice_data = construct_invoice_data_from_stripe(payment_intent)

    # create and send the invoice
    invoice = create_and_send_invoice(invoice_data, InvoiceDelivery.EMAIL)

    # book the invoice
    book_invoice(invoice)


def main() -> None:
    # load environment variables
    load_dotenv()

    # initialize the Stripe API
    init_stripe_api()

    # get successful payment intents from Stripe
    payment_intents = get_successful_payment_intents(PROCESS_INVOICES_PERIOD)
    if not payment_intents:
        print("No successful payment intents in the last period.")
        return

    # create invoices from payment intents
    for pi in payment_intents:
        create_invoice(pi)


if __name__ == "__main__":
    main()
