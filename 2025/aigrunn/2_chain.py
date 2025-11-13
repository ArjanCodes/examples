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
# Generic handler helper
# -------------------------------------------------------------------
def run_step(
    info: dict[str, Any],
    prompt: str,
    model_type: Type[BaseModel],
) -> dict[str, Any]:
    """Generic LLM-powered structured extraction step."""
    answer = input(prompt)
    extracted = extract_structured_dict(
        model_type=model_type,
        user_answer=answer,
    )
    info.update(extracted)
    return info


# -------------------------------------------------------------------
# Step functions (Chain of Responsibility style)
# -------------------------------------------------------------------
def destination_step(info: dict[str, Any]) -> dict[str, Any]:
    return run_step(info, "Where are you traveling? ", DestinationOnly)


def days_step(info: dict[str, Any]) -> dict[str, Any]:
    return run_step(info, "How many days will you stay? ", DaysOnly)


def hotel_step(info: dict[str, Any]) -> dict[str, Any]:
    return run_step(info, "Do you need a hotel (yes/no)? ", HotelOnly)


def car_step(info: dict[str, Any]) -> dict[str, Any]:
    return run_step(info, "Do you need a rental car (yes/no)? ", CarOnly)


# -------------------------------------------------------------------
# Chain executor
# -------------------------------------------------------------------
HandlerFn = Callable[[dict[str, Any]], dict[str, Any]]


def run_chain(*steps: HandlerFn) -> TravelInfo:
    state: dict[str, Any] = {}

    for step in steps:
        state = step(state)

    return TravelInfo(**state)


def main() -> None:
    print("=== Chain of Responsibility (Using Generic Handler) ===\n")

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
