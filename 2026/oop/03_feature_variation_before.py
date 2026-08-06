from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    sku: str
    price_in_cents: int


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


class ProductCatalogSynchronizer:
    def __init__(self, api: CatalogApi) -> None:
        self.api = api

    def sync(self, products: list[Product]) -> SyncResult:
        self.api.replace_products(products)
        return SyncResult(products_synced=len(products), attempts=1)


class RetryingProductCatalogSynchronizer(ProductCatalogSynchronizer):
    def sync(self, products: list[Product]) -> SyncResult:
        for attempt in range(1, 4):
            try:
                self.api.replace_products(products)
            except ConnectionError:
                if attempt == 3:
                    raise
            else:
                return SyncResult(products_synced=len(products), attempts=attempt)
        raise AssertionError("The retry loop should return or raise")


class ValidatingRetryingProductCatalogSynchronizer(
    RetryingProductCatalogSynchronizer
):
    def sync(self, products: list[Product]) -> SyncResult:
        if any(product.price_in_cents < 0 for product in products):
            raise ValueError("Product prices cannot be negative")
        return super().sync(products)


def main() -> None:
    products = [Product("SKU-1", 1299), Product("SKU-2", 2499)]
    api = CatalogApi(failures_before_success=1)
    result = ValidatingRetryingProductCatalogSynchronizer(api).sync(products)
    assert result == SyncResult(products_synced=2, attempts=2)
    assert api.products == products


if __name__ == "__main__":
    main()
