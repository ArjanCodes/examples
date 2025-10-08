from collections import Counter
from functools import cache
from event import Event, EventType
from event_store import EventStore


class Inventory:
    def __init__(self, store: EventStore[str]):
        self.store = store

    @cache
    def get_items(self) -> list[tuple[str, int]]:
        counts = Counter[str]()
        for event in self.store.get_all_events():
            if event.type == EventType.ITEM_ADDED:
                counts[event.data] += 1
            elif event.type == EventType.ITEM_REMOVED:
                counts[event.data] -= 1

        return [
            (item, count)
            for item, count in counts.items()
            if count > 0
        ]

    def get_count(self, item: str) -> int:
        return dict(self.get_items()).get(item, 0)

    def _invalidate_cache(self) -> None:
        self.get_items.cache_clear()

    def add_item(self, item: str) -> None:
        self.store.append(Event(EventType.ITEM_ADDED, item))
        self._invalidate_cache()

    def remove_item(self, item: str) -> None:
        if self.get_count(item) <= 0:
            raise ValueError(f"{item} not in inventory")
        self.store.append(Event(EventType.ITEM_REMOVED, item))
        self._invalidate_cache()