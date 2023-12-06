from typing import Protocol


class EmailService(Protocol):
    def send_email(self, to_address: str, subject: str, body: str) -> str:
        """
        Send an email.
        """
        ...
