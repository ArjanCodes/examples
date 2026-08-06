from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class SupplierSession:
    supplier_name: str
    access_token: str


@dataclass(frozen=True)
class InventoryItem:
    sku: str
    quantity: int


class Authenticated(Protocol):
    def authenticate(self, api_key: str) -> SupplierSession: ...


class InventorySource(Protocol):
    def download_inventory(self, session: SupplierSession) -> list[InventoryItem]: ...

    def download_reserved_skus(self, session: SupplierSession) -> set[str]: ...


class WarehouseSupplier:
    def authenticate(self, api_key: str) -> SupplierSession:
        if api_key != "warehouse-api-key":
            raise PermissionError("Invalid warehouse API key")
        return SupplierSession("Warehouse Supplier", "supplier-token")

    def download_inventory(self, session: SupplierSession) -> list[InventoryItem]:
        self._check_session(session)
        return [
            InventoryItem("SKU-1", 8),
            InventoryItem("SKU-2", 3),
            InventoryItem("SKU-3", 0),
        ]

    def download_reserved_skus(self, session: SupplierSession) -> set[str]:
        self._check_session(session)
        return {"SKU-2"}

    @staticmethod
    def _check_session(session: SupplierSession) -> None:
        if session.access_token != "supplier-token":
            raise PermissionError("Invalid supplier session")


def connect_to_supplier(integration: Authenticated, api_key: str) -> SupplierSession:
    session = integration.authenticate(api_key)
    if not session.access_token:
        raise PermissionError("Supplier did not return an access token")
    return session


def sync_inventory(
    source: InventorySource, session: SupplierSession
) -> list[InventoryItem]:
    inventory = source.download_inventory(session)
    reserved_skus = source.download_reserved_skus(session)
    sellable_items = [
        item
        for item in inventory
        if item.quantity > 0 and item.sku not in reserved_skus
    ]
    return sorted(sellable_items, key=lambda item: item.sku)


def main() -> None:
    supplier = WarehouseSupplier()
    session = connect_to_supplier(supplier, "warehouse-api-key")
    sellable_items = sync_inventory(supplier, session)
    print(sellable_items)


if __name__ == "__main__":
    main()
