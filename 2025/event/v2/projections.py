from collections import Counter, defaultdict
from event import Event, EventType
from item import Item


def get_most_collected_items(events: list[Event[Item]], top_n: int = 5) -> list[tuple[str, int]]:
    """Returns a list of the most frequently added item names."""
    counts = Counter[str]()
    for event in events:
        if event.type == EventType.ITEM_ADDED:
            counts[event.data.name] += 1
    return counts.most_common(top_n)


def get_item_origins(events: list[Event[Item]]) -> dict[str, set[str]]:
    """Returns a mapping of item names to all origins they’ve appeared in."""
    origins: dict[str, set[str]] = defaultdict(set)
    for event in events:
        if event.type == EventType.ITEM_ADDED:
            origins[event.data.name].add(event.data.origin)
    return dict(origins)