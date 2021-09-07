from support.app import CustomerSupport
from support.ticket import SupportTicket


# This works because the __call__ makes it Callable
class BlackHoleStrategy:
    def __call__(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
        return []


# same thing but using a function
def blackHoleStrategy(tickets: list[SupportTicket]) -> list[SupportTicket]:
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
    # app.process_tickets(BlackHoleStrategy())
    app.process_tickets(blackHoleStrategy)


if __name__ == "__main__":
    main()
