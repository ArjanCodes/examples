from dataclasses import dataclass


@dataclass
class SupportTicket:
    customer: str
    issue: str

    def process(self):
        print("==================================")
        print(f"Customer: {self.customer}")
        print(f"Issue: {self.issue}")
        print("==================================")


def process_tickets(tickets: list[SupportTicket]):
    # if it's empty, don't do anything
    if not tickets:
        print("There are no tickets to process. Well done!")
        return

    # go through the tickets in the list
    for ticket in tickets:
        ticket.process()


def main():
    # create a few support tickets
    tickets = [
        SupportTicket("John Smith", "My computer makes strange sounds!"),
        SupportTicket("Linus Sebastian", "I can't upload any videos, please help."),
        SupportTicket("Arjan Codes", "VSCode doesn't automatically solve my bugs."),
    ]

    # process the tickets
    process_tickets(tickets)


if __name__ == "__main__":
    main()
