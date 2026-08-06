from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CheckoutConfig:
    tax_rate: Decimal
    retry_count: int


class Checkout:
    def __init__(self, config: CheckoutConfig) -> None:
        self.config = config

    def total_for(self, subtotal: Decimal) -> Decimal:
        return subtotal * (Decimal(1) + self.config.tax_rate)


def create_german_reliable_config() -> CheckoutConfig:
    return CheckoutConfig(
        tax_rate=Decimal("0.19"),
        retry_count=10,
    )


def main() -> None:
    german_reliable_config = create_german_reliable_config()
    checkout = Checkout(german_reliable_config)
    print(f"Total: {checkout.total_for(Decimal('100.0'))} EUR")
    print(f"Payment retries: {checkout.config.retry_count}")


if __name__ == "__main__":
    main()
