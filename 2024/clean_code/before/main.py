from dotenv import load_dotenv
from invoices import (
    InvoiceDelivery,
    create_and_send_invoice,
)
from processing import can_process_pi, get_successful_payment_intents, init_stripe_api

PROCESS_INVOICES_PERIOD = 24  # hours


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
        if not can_process_pi(pi):
            continue

        create_and_send_invoice(pi, InvoiceDelivery.EMAIL)


if __name__ == "__main__":
    main()
