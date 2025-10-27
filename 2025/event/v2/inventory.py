from collections import Counter
from functools import cache
from event import Event, EventType
from item import Item
from event_store import EventStore


class Inventory:
    def __init__(self, store: EventStore[Item]):
        self.store = store

    @cache
    def get_items(self) -> list[tuple[str, int]]:
        counts = Counter[str]()
        for event in self.store.get_all_events():
            name = event.data.name
            if event.type == EventType.ITEM_ADDED:
                counts[name] += 1
            elif event.type == EventType.ITEM_REMOVED:
                counts[name] -= 1

        return [
            (name, count)
            for name, count in counts.items()
            if count > 0
        ]

    def get_count(self, item_name: str) -> int:
        return dict(self.get_items()).get(item_name, 0)

    def _invalidate_cache(self) -> None:
        self.get_items.cache_clear()

    def add_item(self, item: Item) -> None:
        self.store.append(Event(EventType.ITEM_ADDED, item))
        self._invalidate_cache()

    def remove_item(self, item: Item) -> None:
        if self.get_count(item.name) <= 0:
            raise ValueError(f"{item.name} not in inventory")
        self.store.append(Event(EventType.ITEM_REMOVED, item))
        self._invalidate_cache()