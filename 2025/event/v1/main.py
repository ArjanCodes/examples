from event_store import EventStore
from inventory import Inventory


def main() -> None:
    store = EventStore[str]()
    inventory = Inventory(store)

    inventory.add_item("sword")
    inventory.add_item("potion")
    inventory.add_item("bow")
    inventory.add_item("shield")
    inventory.add_item("torch")
    inventory.remove_item("potion")

    print(inventory.get_items())  # ['sword', 'bow', 'shield', 'torch']


if __name__ == "__main__":
    main()
