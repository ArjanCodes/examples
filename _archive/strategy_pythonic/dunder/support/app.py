import random
from typing import Protocol

from support.ticket import SupportTicket


class TicketOrderingStrategy(Protocol):
    def __call__(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
        """Returns an ordered list of tickets."""


class FIFOOrderingStrategy:
    def __call__(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
        return tickets.copy()


class FILOOrderingStrategy:
    def __call__(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
        return list(reversed(tickets))


class RandomOrderingStrategy:
    def __call__(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
        return random.sample(tickets, len(tickets))


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
