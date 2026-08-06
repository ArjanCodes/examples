from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class StandardCheckout:
    tax_rate: Decimal = Decimal("0.21")
    retry_count: int = 3

    def total_for(self, subtotal: Decimal) -> Decimal:
        return subtotal * (Decimal(1) + self.tax_rate)


@dataclass(frozen=True)
class GermanCheckout(StandardCheckout):
    tax_rate: Decimal = Decimal("0.19")


@dataclass(frozen=True)
class ReliableGermanCheckout(GermanCheckout):
    retry_count: int = 10


def main() -> None:
    checkout = ReliableGermanCheckout()
    print(f"Total: {checkout.total_for(Decimal('100.0'))} EUR")
    print(f"Payment retries: {checkout.retry_count}")


if __name__ == "__main__":
    main()
