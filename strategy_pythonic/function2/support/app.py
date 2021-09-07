import random
from typing import Callable, Optional

from support.ticket import SupportTicket

TicketOrderingStrategy = Callable[[list[SupportTicket]], list[SupportTicket]]


def fifo_strategy(tickets: list[SupportTicket]) -> list[SupportTicket]:
    return tickets.copy()


def filo_strategy(tickets: list[SupportTicket]) -> list[SupportTicket]:
    tickets_copy = tickets.copy()
    tickets_copy.reverse()
    return tickets_copy


def random_strategy_generator(seed: Optional[int] = None) -> TicketOrderingStrategy:
    use_seed = False

    def random_strategy(tickets: list[SupportTicket]) -> list[SupportTicket]:
        tickets_copy = tickets.copy()
        if use_seed:
            random.seed(seed)
        random.shuffle(tickets_copy)
        return tickets_copy

    return random_strategy


class CustomerSupport:
    def __init__(self):
        self.tickets: list[SupportTicket] = []

    def add_ticket(self, ticket: SupportTicket):
        self.tickets.append(ticket)

    def process_tickets(self, processing_strategy: TicketOrderingStrategy):
        # create the ordered list
        ticket_list = processing_strategy(self.tickets)

        # if it's empty, don't do anything
        if len(ticket_list) == 0:
            print("There are no tickets to process. Well done!")
            return

        # go through the tickets in the list
        for ticket in ticket_list:
            ticket.process()
