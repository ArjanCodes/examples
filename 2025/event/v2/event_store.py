

from event import Event


class EventStore[T]:
    def __init__(self):
        self._events: list[Event[T]] = []

    def append(self, event: Event[T]) -> None:
        self._events.append(event)

    def get_all_events(self) -> list[Event[T]]:
        return list(self._events)
