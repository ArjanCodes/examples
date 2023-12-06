from email_sender import EmailSender
from services import MailChimp, SendGrid, Smtp


def test_email_sender_with_smtp():
    smtp = Smtp("smtp.example.com", "Test Signature")
    email_sender = EmailSender(email_service=smtp)
    assert "SMTP" in email_sender.send_email(
        to_address="arjan@arjancodes.com",
        subject="Important video",
        body="Very secret video",
    )


def test_email_sender_with_sendgrid():
    sendgrid = SendGrid()
    email_sender = EmailSender(email_service=sendgrid)
    assert "SendGrid" in email_sender.send_email(
        to_address="arjan@arjancodes.com",
        subject="Important video",
        body="Very secret video",
    )


def test_email_sender_with_mailchimp():
    mailchimp = MailChimp()
    email_sender = EmailSender(email_service=mailchimp)
    assert "MailChimp" in email_sender.send_email(
        to_address="arjan@arjancodes.com",
        subject="Important video",
        body="Very secret video",
    )


def test_email_sender_with_mailchimp_attachment():
    file_path = "/path/to/pdf"

    mailchimp = MailChimp()
    mailchimp.add_attachment(file_path)
    email_sender = EmailSender(email_service=mailchimp)
    assert file_path in email_sender.send_email(
        to_address="arjan@arjancodes.com",
        subject="Important video",
        body="Very secret video",
    )


def test_email_sender_with_default():
    email_sender = EmailSender()
    assert "MailChimp" in email_sender.send_email(
        to_address="arjan@arjancodes.com",
        subject="Important video",
        body="Very secret video",
    )
