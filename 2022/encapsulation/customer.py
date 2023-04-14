from dataclasses import dataclass


def send_email(to: str, subject: str, body: str) -> None:
    print(f"Sending email to {to}.")
    print(f"Subject: {subject}")
    print("Body:")
    print(body)


@dataclass
class Customer:
    id: str
    name: str
    email_address: str

    def __post_init__(self):
        self._send_welcome_email()

    def _send_welcome_email(self):
        subject = "Welcome to our platform!"
        body = (
            f"Hi, {self.name}, we're so glad you joined our platform."
            f"Here's a tutorial to help you get started: https://youtu.be/LrtnLEkOwFE. Cheers, the team."
        )
        send_email(self.email_address, subject, body)
