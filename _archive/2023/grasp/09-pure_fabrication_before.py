from dataclasses import dataclass, field
from datetime import datetime
from time import sleep


@dataclass
class Payment:
    """Payment in an store."""

    storage: dict[str, int] = field(default_factory=dict)

    def pay(self, amount: int) -> None:
        # code to process payment
        print("Payment processed.")
        self.storage[datetime.now().isoformat()] = amount

    def show_storage_records(self) -> None:
        """Show all stored payment records."""
        print(self.storage)


def main() -> None:

    payment = Payment()

    payment.pay(100)
    sleep(1)  # just to get a different timestamp
    payment.pay(200)

    payment.show_storage_records()


if __name__ == "__main__":
    main()
