from typing import Callable


events: dict[str, list[Callable]] = {}


def clear_events():
    events.clear()


def register_event(event: str, listener: Callable):
    if event not in events:
        events[event] = [listener]
    elif listener not in events[event]:
        events[event].append(listener)
    else:
        print(f"Could not add listener {listener} to {event}")


def raise_event(event: str, event_args):
    if event in events:
        for listener in events[event]:
            listener(event_args)
    else:
        print(f"No event {event}")
