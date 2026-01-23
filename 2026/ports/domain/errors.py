class DomainError(Exception):
    """Base class for domain-level errors."""


class InvalidQuantity(DomainError):
    pass


class UnknownSku(DomainError):
    def __init__(self, sku: str) -> None:
        super().__init__(f"unknown sku: {sku}")
        self.sku = sku


class OutOfStock(DomainError):
    def __init__(self, sku: str, requested: int, available: int) -> None:
        super().__init__(
            f"out of stock: {sku}, requested {requested}, available {available}"
        )
        self.sku = sku
        self.requested = requested
        self.available = available
