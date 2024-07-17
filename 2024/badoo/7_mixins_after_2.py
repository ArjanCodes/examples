from dataclasses import dataclass
from typing import Callable


@dataclass
class Order:
    customer_email: str
    product_id: int
    quantity: int


def log(message: str) -> None:
    print(f"LOG: {message}")


def save() -> None:
    print("Data saved")


type Logger = Callable[[str], None]
type Saver = Callable[[], None]


class ProcessOrder:
    def __init__(self, logger: Logger, saver: Saver) -> None:
        self.logger = logger
        self.saver = saver

    def process(self, order: Order) -> None:
        self.logger(f"Processing order {order}")
        self.saver()


class CancelOrder:
    def __init__(self, logger: Logger, saver: Saver) -> None:
        self.logger = logger
        self.saver = saver

    def cancel(self, order: Order) -> None:
        self.logger(f"Cancelling order {order}")
        self.saver()


def main() -> None:
    order = Order(customer_email="hi@arjancodes.com", product_id=123, quantity=2)
    processor = ProcessOrder(log, save)
    processor.process(order)
    canceler = CancelOrder(log, save)
    canceler.cancel(order)


if __name__ == "__main__":
    main()
