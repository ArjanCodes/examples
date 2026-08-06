from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Order:
    order_id: str


class OrderReader(Protocol):
    def get_orders(self) -> list[Order]: ...


class OrderWriter(Protocol):
    def enqueue(self, order: Order) -> None: ...


class OrderQueue:
    def __init__(self, orders: list[Order]) -> None:
        self._orders = orders.copy()

    def enqueue(self, order: Order) -> None:
        self._orders.append(order)

    def get_orders(self) -> list[Order]:
        return self._orders.copy()


class OrderHistory:
    def __init__(self, orders: list[Order]) -> None:
        self._orders = orders.copy()

    def get_orders(self) -> list[Order]:
        return self._orders.copy()


def print_order_history(history: OrderReader) -> None:
    print([order.order_id for order in history.get_orders()])


def add_expedited_order(queue: OrderWriter) -> None:
    queue.enqueue(Order("EXPRESS-1"))


def main() -> None:
    order_history = OrderHistory([Order("ORD-1")])
    queue = OrderQueue([])

    print_order_history(order_history)
    add_expedited_order(queue)
    assert queue.get_orders() == [Order("EXPRESS-1")]


if __name__ == "__main__":
    main()
