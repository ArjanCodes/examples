from support.app import CustomerSupport, random_strategy_generator
from support.ticket import SupportTicket


class BlackHoleStrategy:
    def __call__(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
        return []


def main():
    # create the application
    app = CustomerSupport()

    # create a few tickets
    app.add_ticket(SupportTicket("John Smith", "My computer makes strange sounds!"))
    app.add_ticket(
        SupportTicket("Linus Sebastian", "I can't upload any videos, please help.")
    )
    app.add_ticket(
        SupportTicket("Arjan Codes", "VSCode doesn't automatically solve my bugs.")
    )

    # process the tickets
    app.process_tickets(random_strategy_generator(1))


if __name__ == "__main__":
    main()
