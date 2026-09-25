from dataclasses import dataclass
from time import sleep


@dataclass
class Customer:
    id: int
    name: str

    @property
    def open_invoice_total(self) -> int:
        """Looks like a field, but performs a slow remote query."""
        sleep(0.2)  # Pretend this is a database/API call.
        return 1250


class BillingService:
    def get_open_invoice_total(self, customer_id: int) -> int:
        """The verb makes the I/O and possible failure worth noticing."""
        sleep(0.2)
        return 1250


def main() -> None:
    customer = Customer(id=1, name="Ada")
    print(f"{customer.name} owes {customer.open_invoice_total} cents")

    billing = BillingService()
    total = billing.get_open_invoice_total(customer.id)
    print(f"{customer.name} owes {total} cents")


if __name__ == "__main__":
    main()
