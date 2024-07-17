from dataclasses import dataclass


@dataclass
class Order:
    customer_email: str
    product_id: int
    quantity: int


class LogMixin:
    def log(self, message: str) -> None:
        print(f"LOG: {message}")


class SaveMixin:
    def save(self) -> None:
        print("Data saved")


class ProcessOrder(LogMixin, SaveMixin):
    def process(self, order: Order) -> None:
        self.log(f"Processing order {order}")
        self.save()


class CancelOrder(LogMixin, SaveMixin):
    def cancel(self, order: Order) -> None:
        self.log(f"Cancelling order {order}")
        self.save()


def main() -> None:
    order = Order(customer_email="hi@arjancodes.com", product_id=123, quantity=2)
    processor = ProcessOrder()
    processor.process(order)
    canceler = CancelOrder()
    canceler.cancel(order)


if __name__ == "__main__":
    main()
