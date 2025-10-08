from typing import Protocol

def notify_user_no_di(user_email: str, message: str):
    print(f"Sending email to {user_email}: {message}")


# Define a Protocol (interface) for notification services
class Notifier(Protocol):
    def send(self, recipient: str, message: str) -> None:
        ...


# Concrete implementation: sends email
class EmailNotifier:
    def send(self, recipient: str, message: str) -> None:
        print(f"[Email] To: {recipient} | Message: {message}")


# Concrete implementation: sends SMS
class SMSNotifier:
    def send(self, recipient: str, message: str) -> None:
        print(f"[SMS] To: {recipient} | Message: {message}")


# Business logic function with injected dependency
def notify_user(user: str, message: str, notifier: Notifier) -> None:
    notifier.send(user, message)


def main() -> None:
    email_notifier = EmailNotifier()
    sms_notifier = SMSNotifier()

    # Send email
    notify_user("alice@example.com", "Your invoice is ready.", email_notifier)

    # Send SMS
    notify_user("+31612345678", "Your package is on the way!", sms_notifier)


if __name__ == "__main__":
    main()