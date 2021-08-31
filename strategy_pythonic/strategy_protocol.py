import random
import string
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


def generate_id(length: int = 8):
    """Helper function for generating an id."""
    return "".join(random.choices(string.ascii_uppercase, k=length))


@dataclass
class SupportTicket:
    customer: str
    issue: str
    id: str = field(init=False)

    def __post_init__(self):
        self.id = generate_id()

    def process(self):
        print("==================================")
        print(f"Processing ticket id: {self.id}")
        print(f"Customer: {self.customer}")
        print(f"Issue: {self.issue}")
        print("==================================")


class TicketOrderingStrategy(ABC):
    @abstractmethod
    def create_ordering(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
        """Returns an ordered list of tickets."""


class FIFOOrderingStrategy(TicketOrderingStrategy):
    def create_ordering(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
        return tickets.copy()


class FILOOrderingStrategy(TicketOrderingStrategy):
    def create_ordering(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
        tickets_copy = tickets.copy()
        tickets_copy.reverse()
        return tickets_copy


class RandomOrderingStrategy(TicketOrderingStrategy):
    def create_ordering(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
        tickets_copy = tickets.copy()
        random.shuffle(tickets_copy)
        return tickets_copy


class BlackHoleStrategy(TicketOrderingStrategy):
    def create_ordering(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
        return []


class CustomerSupport:
    def __init__(self):
        self.tickets: list[SupportTicket] = []

    def create_ticket(self, customer: str, issue: str):
        self.tickets.append(SupportTicket(customer, issue))

    def process_tickets(self, processing_strategy: TicketOrderingStrategy):
        # create the ordered list
        ticket_list = processing_strategy.create_ordering(self.tickets)

        # if it's empty, don't do anything
        if len(ticket_list) == 0:
            print("There are no tickets to process. Well done!")
            return

        # go through the tickets in the list
        for ticket in ticket_list:
            ticket.process()


def main():
    # create the application
    app = CustomerSupport()

    # register a few tickets
    app.create_ticket("John Smith", "My computer makes strange sounds!")
    app.create_ticket("Linus Sebastian", "I can't upload any videos, please help.")
    app.create_ticket("Arjan Egges", "VSCode doesn't automatically solve my bugs.")

    # process the tickets
    app.process_tickets(FIFOOrderingStrategy())


if __name__ == "__main__":
    main()
