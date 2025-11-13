from typing import Any, Callable, Type

from pydantic import BaseModel

from ai_utils import extract_structured_dict


# -------------------------------------------------------------------
# Domain Pydantic Models
# -------------------------------------------------------------------
class TravelInfo(BaseModel):
    destination: str
    days: int
    hotel_needed: bool
    car_rental: bool


class DestinationOnly(BaseModel):
    destination: str


class DaysOnly(BaseModel):
    days: int


class HotelOnly(BaseModel):
    hotel_needed: bool


class CarOnly(BaseModel):
    car_rental: bool


# -------------------------------------------------------------------
# Observer Pattern (generic)
# -------------------------------------------------------------------
ObserverFn = Callable[[str, Any], None]
_observers: list[ObserverFn] = []


def add_observer(fn: ObserverFn) -> None:
    """Register a callback that receives (event_name, payload)."""
    _observers.append(fn)


def notify(event: str, payload: Any) -> None:
    """Notify all observers about an event."""
    for obs in _observers:
        obs(event, payload)


# -------------------------------------------------------------------
# Generic Step Runner
# -------------------------------------------------------------------
def run_step(
    info: dict[str, Any],
    prompt: str,
    model_type: Type[BaseModel],
    event_name: str,  # NEW: Event for observers
) -> dict[str, Any]:
    notify("before_step", {"step": event_name, "state": info})

    user_input = input(prompt)
    extracted = extract_structured_dict(
        model_type=model_type,
        user_answer=user_input,
    )
    info.update(extracted)

    # Notify generic event
    notify("after_field_extracted", {"step": event_name, "extracted": extracted})
    notify(f"{event_name}_completed", extracted)

    return info


# -------------------------------------------------------------------
# Step Functions (Chain of Responsibility)
# -------------------------------------------------------------------
def destination_step(info: dict[str, Any]) -> dict[str, Any]:
    return run_step(
        info,
        "Where are you traveling? ",
        DestinationOnly,
        event_name="destination",
    )


def days_step(info: dict[str, Any]) -> dict[str, Any]:
    return run_step(
        info,
        "How many days will you stay? ",
        DaysOnly,
        event_name="days",
    )


def hotel_step(info: dict[str, Any]) -> dict[str, Any]:
    return run_step(
        info,
        "Do you need a hotel (yes/no)? ",
        HotelOnly,
        event_name="hotel_needed",
    )


def car_step(info: dict[str, Any]) -> dict[str, Any]:
    return run_step(
        info,
        "Do you need a rental car (yes/no)? ",
        CarOnly,
        event_name="car_rental",
    )


# -------------------------------------------------------------------
# Chain Runner
# -------------------------------------------------------------------
HandlerFn = Callable[[dict[str, Any]], dict[str, Any]]


def run_chain(*steps: HandlerFn) -> TravelInfo:
    state: dict[str, Any] = {}

    notify("chain_started", state)

    for step in steps:
        state = step(state)

    notify("chain_completed", state)

    return TravelInfo(**state)


# -------------------------------------------------------------------
# Example Observer
# -------------------------------------------------------------------
def logger(event: str, payload: Any) -> None:
    print(f"[LOG] Event: {event} | Payload: {payload}")


def analytics(event: str, payload: Any) -> None:
    # In a real system, you would send analytics here
    if event.endswith("_completed"):
        print(f"[ANALYTICS] Step '{event}' recorded.")


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
def main() -> None:
    print("=== Chain of Responsibility + Observer Pattern ===\n")

    # Register observers
    add_observer(logger)
    add_observer(analytics)

    final_info = run_chain(
        destination_step,
        days_step,
        hotel_step,
        car_step,
    )

    print("\n=== Final Trip Info ===")
    print(final_info.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
