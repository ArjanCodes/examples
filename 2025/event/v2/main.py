from event_store import EventStore
from inventory import Inventory
from item import Item
from projections import get_most_collected_items, get_item_origins


def main() -> None:
    # Create reusable item instances
    sword1 = Item(name="sword", rarity="rare", origin="castle")
    sword2 = Item(name="sword", rarity="rare", origin="dungeon")
    potion1 = Item(name="potion", rarity="common", origin="village")
    potion2 = Item(name="potion", rarity="common", origin="village")
    bow = Item(name="bow", rarity="uncommon", origin="forest")
    torch = Item(name="torch", rarity="common", origin="dungeon")
    scroll = Item(name="scroll", rarity="epic", origin="tower")

    # Set up store and inventory
    store = EventStore[Item]()
    inventory = Inventory(store)

    # Add some items
    inventory.add_item(sword1)
    inventory.add_item(sword2)
    inventory.add_item(potion1)
    inventory.add_item(potion2)
    inventory.add_item(bow)
    inventory.add_item(torch)
    inventory.add_item(scroll)

    # Remove some items
    inventory.remove_item(potion1)
    inventory.remove_item(torch)

    # Show inventory state
    print("\n=== Current Inventory ===")
    for name, count in inventory.get_items():
        print(f"{name}: {count}")

    print(f"\nSwords in inventory: {inventory.get_count('sword')}")

    # Show projections
    events = store.get_all_events()

    print("\n=== Most Collected Items ===")
    for name, count in get_most_collected_items(events):
        print(f"{name}: {count} collected")

    print("\n=== Item Origins ===")
    origins = get_item_origins(events)
    for name, origin_set in origins.items():
        origin_list = ', '.join(sorted(origin_set))
        print(f"{name}: {origin_list}")


if __name__ == "__main__":
    main()