from dataclasses import dataclass


@dataclass
class Order:
    customer_email: str
    product_id: int
    quantity: int


class SmtpEmailService:
    def connect_to_smtp_server(self) -> None:
        print("Connecting to SMTP server")

    def send_email(self, recipient: str, message: str) -> None:
        print(f"Sending email to {recipient}: {message}")


def process_order(order: Order) -> None:
    email_service = SmtpEmailService()
    email_service.connect_to_smtp_server()
    email_service.send_email(order.customer_email, "Your order has been processed")


def main() -> None:
    order = Order(customer_email="hi@arjancodes.com", product_id=123, quantity=2)
    process_order(order)


if __name__ == "__main__":
    main()
