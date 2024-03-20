from dataclasses import dataclass, field
from datetime import datetime
from time import sleep


@dataclass
class PersistentStorage:
    """Storage records in dictionary."""

    storage: dict[str, int] = field(default_factory=dict)

    def save(self, key: str, value: int) -> None:
        """Add a record to the storage."""
        self.storage[key] = value

    def load(self, key: str) -> int:
        """Get and amout from the storage."""
        return self.storage[key]

    def show(self) -> None:
        """Shows all stored records."""
        print(self.storage)


@dataclass
class Payment:
    """Payment in an store."""

    amount: int
    persistent_storage: PersistentStorage

    def pay(self) -> None:
        """Process payment."""
        # code to process payment
        print("Payment processed.")


@dataclass
class PaymentHandler:
    """Handle the entire payment process."""

    persistent_storage: PersistentStorage

    def handle_payment(self, payment: Payment) -> None:
        """Apply payment and store it at the end."""
        payment.pay()
        self.persistent_storage.save(datetime.now().isoformat(), payment.amount)


def main() -> None:
    persistent_storage = PersistentStorage()
    payment_handler = PaymentHandler(persistent_storage)

    payment1 = Payment(100, persistent_storage)
    payment2 = Payment(200, persistent_storage)

    payment_handler.handle_payment(payment1)
    sleep(1)  # just to get a different timestamp
    payment_handler.handle_payment(payment2)

    persistent_storage.show()


if __name__ == "__main__":
    main()
