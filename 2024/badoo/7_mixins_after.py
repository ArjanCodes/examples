from dataclasses import dataclass


@dataclass
class Order:
    customer_email: str
    product_id: int
    quantity: int


class Logger:
    def log(self, message: str) -> None:
        print(f"LOG: {message}")


class Saver:
    def save(self) -> None:
        print("Data saved")


class ProcessOrder:
    def __init__(self, logger: Logger, saver: Saver) -> None:
        self.logger = logger
        self.saver = saver

    def process(self, order: Order) -> None:
        self.logger.log(f"Processing order {order}")
        self.saver.save()


class CancelOrder:
    def __init__(self, logger: Logger, saver: Saver) -> None:
        self.logger = logger
        self.saver = saver

    def cancel(self, order: Order) -> None:
        self.logger.log(f"Cancelling order {order}")
        self.saver.save()


def main() -> None:
    order = Order(customer_email="hi@arjancodes.com", product_id=123, quantity=2)
    logger = Logger()
    saver = Saver()
    processor = ProcessOrder(logger, saver)
    processor.process(order)
    canceler = CancelOrder(logger, saver)
    canceler.cancel(order)


if __name__ == "__main__":
    main()
