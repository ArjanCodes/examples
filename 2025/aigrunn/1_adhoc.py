from typing import Any

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


def book_trip_interactively() -> TravelInfo:
    print("=== Ad-Hoc Travel Booking ===")

    info: dict[str, Any] = {}

    # ------------------------------
    # Step 1 — Destination
    # ------------------------------
    answer = input("Where are you traveling? ")
    extracted = extract_structured_dict(
        model_type=DestinationOnly,
        user_answer=answer,
    )
    info.update(extracted)

    # ------------------------------
    # Step 2 — Days
    # ------------------------------
    answer = input("How many days will you stay? ")
    extracted = extract_structured_dict(
        model_type=DaysOnly,
        user_answer=answer,
    )
    info.update(extracted)

    # ------------------------------
    # Step 3 — Hotel needed
    # ------------------------------
    answer = input("Do you need a hotel (yes/no)? ")
    extracted = extract_structured_dict(
        model_type=HotelOnly,
        user_answer=answer,
    )
    info.update(extracted)

    # ------------------------------
    # Step 4 — Car rental
    # ------------------------------
    answer = input("Do you need a rental car (yes/no)? ")
    extracted = extract_structured_dict(
        model_type=CarOnly,
        user_answer=answer,
    )
    info.update(extracted)

    # Build final validated model
    return TravelInfo(**info)


def main() -> None:
    result = book_trip_interactively()
    print("\n=== Final Trip Info ===")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
