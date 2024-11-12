from typing import Any, Callable

events: dict[str, list[Callable[..., None]]] = {}


def clear_events():
    events.clear()


def register_event(event: str, listener: Callable[..., None]):
    if event not in events:
        events[event] = [listener]
    elif listener not in events[event]:
        events[event].append(listener)
    else:
        print(f"Could not add listener {listener} to {event}")


def raise_event(event: str, event_args: Any) -> None:
    # collect the listeners from * and the event
    listeners: set[Callable[..., None]] = set()
    if "*" in events:
        listeners.update(events["*"])
    if event in events:
        listeners.update(events[event])

    # call the listeners
    for listener in listeners:
        listener(event_args)
