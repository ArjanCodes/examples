from collections import Counter
from typing import Optional

from event import Event, EventType


class Snapshot:
    def __init__(self, items: list[str], last_event_index: int):
        self.items = items
        self.last_event_index = last_event_index


class EventStore:
    def __init__(self, snapshot_interval: int = 5):
        self._events: list[Event] = []
        self._snapshot: Optional[Snapshot] = None
        self._snapshot_interval = snapshot_interval

    def append(self, event: Event) -> None:
        self._events.append(event)

        if self._snapshot_interval and len(self._events) % self._snapshot_interval == 0:
            self._create_snapshot()

    def _create_snapshot(self) -> None:
        counts = Counter[str]()
        for event in self._events:
            if event.type == EventType.ITEM_ADDED:
                counts[event.item] += 1
            elif event.type == EventType.ITEM_REMOVED:
                counts[event.item] -= 1

        items = [
            item for item, count in counts.items() for _ in range(count) if count > 0
        ]
        self._snapshot = Snapshot(items, len(self._events) - 1)

    def get_replay_data(self) -> tuple[list[str], list[Event]]:
        if self._snapshot:
            start_items = self._snapshot.items
            remaining = self._events[self._snapshot.last_event_index + 1 :]
            return start_items, remaining
        else:
            return [], self._events

    def get_all_events(self) -> list[Event]:
        return list(self._events)
