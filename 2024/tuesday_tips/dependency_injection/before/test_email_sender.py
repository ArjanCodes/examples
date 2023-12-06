from email_sender import EmailSender, Service

def test_send_email_mailchimp():
    email_sender = EmailSender()
    result = email_sender.send_email(
        service=Service.MAILCHIMP,
        to_address="support@arjancodes.com",
        subject="Urgent meeting",
        body="Very siekret email",
        signature="",
        smtp_server="",
    )

    assert "MailChimp" in result


def test_send_email_sendgrid():
    email_sender = EmailSender()

    result = email_sender.send_email(
        service=Service.SENDGRID,
        to_address="support@arjancodes.com",
        subject="Urgent meeting",
        body="Very siekret email",
        signature="",
        smtp_server="",
    )

    assert "SendGrid" in result


def test_send_email_smtp():
    email_sender = EmailSender()

    result = email_sender.send_email(
        service=Service.SMTP,
        to_address="support@arjancodes.com",
        subject="Urgent meeting",
        body="Very siekret email",
        signature="",
        smtp_server="",
    )

    assert "SMTP" in result
