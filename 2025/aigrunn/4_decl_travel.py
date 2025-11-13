from pydantic import BaseModel

from declarative_engine import run_declarative_flow


class TravelInfo(BaseModel):
    destination: str
    days: int
    hotel_needed: bool
    car_rental: bool


def main():
    instructions = """
        You are a travel booking assistant helping the user plan a trip.
        """

    result = run_declarative_flow(
        model_type=TravelInfo,
        domain_instructions=instructions,
        debug=True,
    )

    print("\n=== Final Result ===")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
