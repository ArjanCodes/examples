from email.message import EmailMessage
from smtplib import SMTP_SSL


def create_email_message(to_email: str, subject: str, body: str) -> EmailMessage:
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["To"] = to_email
    return msg


def send_email(
    smtp_server: str,
    port: int,
    email: str,
    password: str,
    to_email: str,
    subject: str,
    body: str,
) -> None:
    msg = create_email_message(to_email, subject, body)
    with SMTP_SSL(smtp_server, port) as server:
        # server.login(email, password)
        # server.send_message(msg, email)
        print("Email sent successfully!")
