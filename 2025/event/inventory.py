from collections import Counter
from functools import cache
from event_store import EventStore
from event import Event, EventType


class Inventory:
    def __init__(self, store: EventStore):
        self.store = store

    @cache
    def get_items(self) -> list[str]:
        start_items, events = self.store.get_replay_data()
        counts = Counter(start_items)

        for event in events:
            if event.type == EventType.ITEM_ADDED:
                counts[event.item] += 1
            elif event.type == EventType.ITEM_REMOVED:
                counts[event.item] -= 1

        return [
            item
            for item, count in counts.items()
            for _ in range(count)
            if count > 0
        ]

    def _invalidate_cache(self) -> None:
        self.get_items.cache_clear()

    def add_item(self, item: str) -> None:
        self.store.append(Event(EventType.ITEM_ADDED, item))
        self._invalidate_cache()

    def remove_item(self, item: str) -> None:
        if item not in self.get_items():
            raise ValueError(f"{item} not in inventory")
        self.store.append(Event(EventType.ITEM_REMOVED, item))
        self._invalidate_cache()
