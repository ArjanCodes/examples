import os

import stripe
from dotenv import load_dotenv
from invoices import (
    can_process_pi,
    create_and_send_invoice,
    get_successful_payment_intents,
)
from mb_invoice import InvoiceDelivery

# load environment variables
load_dotenv()


# initialize the Stripe API
stripe.api_key = os.getenv("STRIPE_KEY")

PROCESS_INVOICES_PERIOD = 24  # hours


def main() -> None:
    # Create invoices for successful payment intents
    successful_payment_intents = get_successful_payment_intents(PROCESS_INVOICES_PERIOD)
    if not successful_payment_intents:
        print("No successful payment intents in the last period.")
        return

    invoice_count = 0

    for pi in successful_payment_intents.auto_paging_iter():
        if not can_process_pi(pi):
            continue

        create_and_send_invoice(pi, InvoiceDelivery.EMAIL)
        invoice_count += 1


if __name__ == "__main__":
    main()
