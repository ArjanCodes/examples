from email_sender import EmailSender, Service


def main() -> None:
    sender = EmailSender()

    result = sender.send_email(
        service=Service.MAILCHIMP,
        to_address="arjan@arjancodes.com",
        subject="Urgent meeting",
        body="Very siekret email",
        signature="",
        smtp_server="",
    )

    print(result)


if __name__ == "__main__":
    main()
