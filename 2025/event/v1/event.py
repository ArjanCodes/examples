from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class EventType(StrEnum):
    ITEM_ADDED = "item_added"
    ITEM_REMOVED = "item_removed"


@dataclass(frozen=True)
class Event[T = str]:
    type: EventType
    data: T
    timestamp: datetime = datetime.now()
