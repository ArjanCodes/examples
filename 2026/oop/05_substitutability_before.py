from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    order_id: str


class OrderQueue:
    def __init__(self, orders: list[Order]) -> None:
        self._orders = orders.copy()

    def enqueue(self, order: Order) -> None:
        self._orders.append(order)

    def get_orders(self) -> list[Order]:
        return self._orders.copy()


class ReadOnlyOrderQueue(OrderQueue):
    def enqueue(self, order: Order) -> None:
        raise RuntimeError("This order queue is read-only")


def print_order_history(queue: ReadOnlyOrderQueue) -> None:
    print([order.order_id for order in queue.get_orders()])


def add_expedited_order(queue: OrderQueue) -> None:
    queue.enqueue(Order("EXPRESS-1"))


def main() -> None:
    order_history = ReadOnlyOrderQueue([Order("ORD-1")])
    queue = OrderQueue([])

    print_order_history(order_history)
    add_expedited_order(queue)
    assert queue.get_orders() == [Order("EXPRESS-1")]


if __name__ == "__main__":
    main()
