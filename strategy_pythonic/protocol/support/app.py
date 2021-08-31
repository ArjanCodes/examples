import random
from typing import Protocol

from support.ticket import SupportTicket


class TicketOrderingStrategy(Protocol):
    def create_ordering(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
        """Returns an ordered list of tickets."""


class FIFOOrderingStrategy:
    def create_ordering(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
        return tickets.copy()


class FILOOrderingStrategy:
    def create_ordering(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
        tickets_copy = tickets.copy()
        tickets_copy.reverse()
        return tickets_copy


class RandomOrderingStrategy:
    def create_ordering(self, tickets: list[SupportTicket]) -> list[SupportTicket]:
        tickets_copy = tickets.copy()
        random.shuffle(tickets_copy)
        return tickets_copy


class CustomerSupport:
    def __init__(self):
        self.tickets: list[SupportTicket] = []

    def add_ticket(self, ticket: SupportTicket):
        self.tickets.append(ticket)

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
