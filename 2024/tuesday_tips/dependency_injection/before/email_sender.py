from enum import Enum
from services import MailChimp, SendGrid, Smtp


class Service(Enum):
    SENDGRID = "sendgrid"
    MAILCHIMP = "mailchimp"
    SMTP = "smtp"


class EmailSender:
    def send_email(
        self,
        service: Service,
        to_address: str,
        subject: str,
        body: str,
        smtp_server: str,
        signature: str,
    ) -> str:
        if service == Service.MAILCHIMP:
            email_sender = MailChimp()
            return email_sender.send_email(
                to_address=to_address, subject=subject, body=body
            )

        elif service == Service.SENDGRID:
            email_sender = SendGrid()
            return email_sender.send_email(
                to_address=to_address, subject=subject, body=body
            )
        elif service == Service.SMTP:
            email_sender = Smtp(smtp_server=smtp_server, signature=signature)
            return email_sender.send_email(
                to_address=to_address, subject=subject, body=body
            )
        

        return MailChimp().send_email(
            to_address=to_address, subject=subject, body=body
        )
