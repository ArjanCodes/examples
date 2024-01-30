from email_sender import EmailSender
from services import SendGrid


def main() -> None:
    email_service = SendGrid()

    sender = EmailSender(email_service=email_service)

    sender.send_email("arjan@arjancodes.com", ":)", "You have a meeting!!")


if __name__ == "__main__":
    main()
