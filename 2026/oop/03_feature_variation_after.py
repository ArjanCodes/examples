from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    sku: str
    price_in_cents: int


@dataclass(frozen=True)
class SyncOptions:
    validate_products: bool = False
    max_attempts: int = 1


@dataclass(frozen=True)
class SyncResult:
    products_synced: int
    attempts: int


class CatalogApi:
    def __init__(self, failures_before_success: int = 0) -> None:
        self.failures_remaining = failures_before_success
        self.products: list[Product] = []

    def replace_products(self, products: list[Product]) -> None:
        if self.failures_remaining:
            self.failures_remaining -= 1
            raise ConnectionError("Catalog API is temporarily unavailable")
        self.products = products


def sync_catalog(
    api: CatalogApi,
    products: list[Product],
    options: SyncOptions,
) -> SyncResult:
    if options.validate_products and any(
        product.price_in_cents < 0 for product in products
    ):
        raise ValueError("Product prices cannot be negative")

    for attempt in range(1, options.max_attempts + 1):
        try:
            api.replace_products(products)
        except ConnectionError:
            if attempt == options.max_attempts:
                raise
        else:
            return SyncResult(products_synced=len(products), attempts=attempt)

    raise AssertionError("The retry loop should return or raise")


def main() -> None:
    products = [Product("SKU-1", 1299), Product("SKU-2", 2499)]
    api = CatalogApi(failures_before_success=1)
    result = sync_catalog(
        api,
        products,
        SyncOptions(validate_products=True, max_attempts=3),
    )
    assert result == SyncResult(products_synced=2, attempts=2)
    assert api.products == products


if __name__ == "__main__":
    main()
