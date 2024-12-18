from typing import Any

from app.email.attachment import Attachment
from app.email.sender import EmailSender

from ..config import settings


class EmailClient:
    """
    Email client to send emails using the configured email sender
    """

    def __init__(self, sender: EmailSender):
        self.sender = sender

    def send_mail(
        self,
        recipients: list[str],
        subject: str,
        data: dict[str, Any],
        template_id: str | None = None,
        attachments: list[Attachment] | None = None,
    ):
        self.sender.send_email(
            settings.NO_REPLY_EMAIL, recipients, subject, data, template_id, attachments
        )
