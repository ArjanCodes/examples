from support.app import CustomerSupport
from support.ticket import SupportTicket


def main():
    # create the application
    app = CustomerSupport()

    # register a few tickets
    app.add_ticket(SupportTicket("John Smith", "My computer makes strange sounds!"))
    app.add_ticket(
        SupportTicket("Linus Sebastian", "I can't upload any videos, please help.")
    )
    app.add_ticket(
        SupportTicket("Arjan Egges", "VSCode doesn't automatically solve my bugs.")
    )

    # process the tickets
    app.process_tickets("fifo")


if __name__ == "__main__":
    main()
