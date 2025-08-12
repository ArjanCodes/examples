import asyncio
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent

# Load env vars
load_dotenv()

# ----------------------------------
# Shared Dependencies
# ----------------------------------


@dataclass
class TravelDeps:
    user_name: str
    origin_city: str


# ----------------------------------
# Shared Data Passed Through the Chain
# ----------------------------------


class TripContext(BaseModel):
    destination: Optional[str] = None
    from_city: Optional[str] = None
    arrival_time: Optional[str] = None
    hotel_name: Optional[str] = None
    hotel_location: Optional[str] = None


# ----------------------------------
# Step 1: Choose Destination
# ----------------------------------


class DestinationOutput(BaseModel):
    destination: str


destination_agent = Agent(
    "openai:gpt-4o",
    deps_type=TravelDeps,
    output_type=DestinationOutput,
    system_prompt="You help users select an ideal travel destination based on their preferences.",
)


# ----------------------------------
# Step 2: Plan Flight
# ----------------------------------


class FlightPlan(BaseModel):
    from_city: str
    to_city: str
    arrival_time: str


flight_agent = Agent(
    "openai:gpt-4o",
    deps_type=TravelDeps,
    output_type=FlightPlan,
    system_prompt="Plan a realistic flight itinerary for a trip. Include origin city and arrival time.",
)


# ----------------------------------
# Step 3: Recommend Hotel
# ----------------------------------


class HotelOption(BaseModel):
    name: str
    location: str
    price_per_night_usd: int
    stars: int


hotel_agent = Agent(
    "openai:gpt-4o",
    deps_type=TravelDeps,
    output_type=HotelOption,
    system_prompt="Suggest a good hotel near the arrival airport or city center. Consider time of arrival and convenience.",
)


# ----------------------------------
# Step 4: Suggest Activities
# ----------------------------------


class Activities(BaseModel):
    personalized_for: str
    top_activities: list[str]


activity_agent = Agent(
    "openai:gpt-4o",
    deps_type=TravelDeps,
    output_type=Activities,
    system_prompt="Suggest local activities close to the hotel and suitable for arrival time (e.g., evening, morning).",
)


# ----------------------------------
# Chain Execution Logic
# ----------------------------------

async def handle_destination(
    user_input: str, deps: TravelDeps, ctx: TripContext
) -> None:
    dest_result = await destination_agent.run(user_input, deps=deps)
    ctx.destination = dest_result.output.destination
    print(f"📍 Destination: {ctx.destination}")

async def handle_flight(
    user_input: str, deps: TravelDeps, ctx: TripContext
) -> None:
    flight_prompt = f"Plan a flight from {deps.origin_city} to {ctx.destination}."
    flight_result = await flight_agent.run(flight_prompt, deps=deps)
    ctx.from_city = flight_result.output.from_city
    ctx.arrival_time = flight_result.output.arrival_time
    print(
        f"✈️ Flight: from {ctx.from_city} → {ctx.destination}, arriving at {ctx.arrival_time}"
    )

async def handle_hotel(
    user_input: str, deps: TravelDeps, ctx: TripContext
) -> None:
    hotel_prompt = (
        f"Recommend a hotel in {ctx.destination} for a traveler arriving at {ctx.arrival_time}. "
        f"Prefer locations near the airport or city center."
    )
    hotel_result = await hotel_agent.run(hotel_prompt, deps=deps)
    ctx.hotel_name = hotel_result.output.name
    ctx.hotel_location = hotel_result.output.location
    print(
        f"🏨 Hotel: {ctx.hotel_name}, {hotel_result.output.stars}★ at ${hotel_result.output.price_per_night_usd}/night"
    )

async def handle_activities(
    user_input: str, deps: TravelDeps, ctx: TripContext
) -> None:
    activities_prompt = (
        f"Suggest activities in {ctx.destination} close to {ctx.hotel_location} "
        f"and suitable for a traveler arriving at {ctx.arrival_time}."
    )
    activity_result = await activity_agent.run(activities_prompt, deps=deps)
    print(f"🎯 Activities for {activity_result.output.personalized_for}:")
    for a in activity_result.output.top_activities:
        print(f"  - {a}")

async def plan_trip(user_input: str, deps: TravelDeps):
    print(f"\n👤 {deps.user_name} says: {user_input}")
    ctx = TripContext()

    chain = [
        handle_destination,
        handle_flight,
        handle_hotel,
        handle_activities,
    ]

    for step in chain:
        await step(user_input, deps, ctx)


# ----------------------------------
# Main Execution
# ----------------------------------


async def main():
    deps = TravelDeps(user_name="Maria", origin_city="Berlin")
    await plan_trip("I want a rainy city trip within Europe.", deps)


if __name__ == "__main__":
    asyncio.run(main())
