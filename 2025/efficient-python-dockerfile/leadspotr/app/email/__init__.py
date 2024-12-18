from app.email.client import EmailClient
from app.email.sender import FakeSender, SendGridSender

from ..config import settings

fake_email_client = FakeSender()
sendgrid_sender = SendGridSender()
email_client = EmailClient(
    sendgrid_sender
    if settings.SENDGRID_API_KEY and settings.ENVIRONMENT == "production"
    else fake_email_client
)
