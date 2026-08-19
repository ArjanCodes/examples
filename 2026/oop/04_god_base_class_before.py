from dataclasses import dataclass


@dataclass(frozen=True)
class SupplierSession:
    supplier_name: str
    access_token: str


@dataclass(frozen=True)
class InventoryItem:
    sku: str
    quantity: int


class BaseStoreIntegration:
    def authenticate(self, api_key: str) -> SupplierSession:
        raise NotImplementedError

    def upload_product_images(self, image_urls: list[str]) -> None:
        raise NotImplementedError

    def download_inventory(self, session: SupplierSession) -> list[InventoryItem]:
        raise NotImplementedError

    def download_reserved_skus(self, session: SupplierSession) -> set[str]:
        raise NotImplementedError

    def subscribe_to_order_webhooks(self, callback_url: str) -> None:
        raise NotImplementedError

    def request_return_label(self, order_id: str) -> str:
        raise NotImplementedError


class WarehouseSupplier(BaseStoreIntegration):
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


def connect_to_supplier(
    integration: BaseStoreIntegration, api_key: str
) -> SupplierSession:
    session = integration.authenticate(api_key)
    if not session.access_token:
        raise PermissionError("Supplier did not return an access token")
    return session


def sync_inventory(
    integration: BaseStoreIntegration, session: SupplierSession
) -> list[InventoryItem]:
    inventory = integration.download_inventory(session)
    reserved_skus = integration.download_reserved_skus(session)
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
