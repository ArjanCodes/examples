import json
from abc import ABC, abstractmethod
from typing import Any

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.email.attachment import Attachment, SendGridAttachmentWrapper
from app.utils.logger import logger

from ..config import settings


class EmailSender(ABC):
    @abstractmethod
    def send_email(
        self,
        from_address: str,
        to_addresses: list[str],
        subject: str,
        data: dict[str, Any],
        template_id: str | None = None,
        attachments: list[Attachment] | None = None,
    ):
        """
        Send email using the configured email sender
        """


class SendGridSender(EmailSender):
    """
    SendGrid email sender client implementation using SendGrid API
    """

    def __init__(self):
        self.client = SendGridAPIClient(settings.SENDGRID_API_KEY)

    def send_email(
        self,
        from_address: str,
        to_addresses: list[str],
        subject: str,
        data: dict[str, Any],
        template_id: str | None = None,
        attachments: list[Attachment] | None = None,
    ) -> None:
        if template_id is None:
            raise ValueError("Template ID cannot be empty")

        mail = self.setup_email(
            from_address, to_addresses, subject, data, template_id, attachments
        )
        self.client.send(mail)  # type: ignore

    def setup_email(
        self,
        from_address: str,
        to_addresses: list[str],
        subject: str,
        data: dict[str, Any],
        template_id: str,
        attachments: list[Attachment] | None,
    ) -> Mail:
        if not to_addresses or not data:
            raise ValueError("Recipients and data cannot be empty")

        mail = Mail(
            from_email=from_address,
            to_emails=to_addresses,
            subject=subject,
        )

        mail.template_id = template_id
        mail.dynamic_template_data = data

        if attachments is not None:
            self.add_attachments(mail, attachments)

        return mail

    def add_attachments(self, mail: Mail, attachments: list[Attachment]) -> None:
        for attachment in attachments:
            logger.info("Adding attachment: %s", attachment.get_filename())
            mail.attachment = SendGridAttachmentWrapper(
                file_content=attachment.get_content(),
                file_name=attachment.get_filename(),
                file_type=attachment.get_file_type(),
                disposition=attachment.get_disposition(),
            )


class FakeSender(EmailSender):
    """
    Fake email sender client implementation for testing.
    """

    def send_email(
        self,
        from_address: str,
        to_addresses: list[str],
        subject: str,
        data: dict[str, Any],
        template_id: str | None = None,
        attachments: list[Attachment] | None = None,
    ) -> None:
        # Log the email details to a file or console for verification
        email_details = {
            "from": from_address,
            "to": to_addresses,
            "subject": subject,
            "data": data,
            "template_id": template_id,
            "attachments": [
                attachment.get_filename() for attachment in (attachments or [])
            ],
        }
        print(json.dumps(email_details, indent=2))  # Or write to a file
