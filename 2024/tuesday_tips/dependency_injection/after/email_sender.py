from email_service import EmailService
from services import MailChimp


class EmailSender:
    def __init__(self, email_service: EmailService = MailChimp()) -> None:
        self.email_service = email_service

    def send_email(self, to_address: str, subject: str, body: str) -> str:
        return self.email_service.send_email(to_address, subject, body)
