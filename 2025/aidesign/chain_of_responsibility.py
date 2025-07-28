import asyncio
import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent

# Load env vars
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

# ----------------------------------
# Shared Dependencies
# ----------------------------------


@dataclass
class TravelDeps:
    user_name: str


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


async def plan_trip(user_input: str, deps: TravelDeps):
    print(f"\n👤 {deps.user_name} says: {user_input}")
    ctx = TripContext()

    # Step 1: Destination
    dest_result = await destination_agent.run(prompt=user_input, deps=deps)
    ctx.destination = dest_result.output.destination
    print(f"📍 Destination: {ctx.destination}")

    # Step 2: Flight
    flight_prompt = f"Plan a flight to {ctx.destination}."
    flight_result = await flight_agent.run(prompt=flight_prompt, deps=deps)
    ctx.from_city = flight_result.output.from_city
    ctx.arrival_time = flight_result.output.arrival_time
    print(
        f"✈️ Flight: from {ctx.from_city} → {ctx.destination}, arriving at {ctx.arrival_time}"
    )

    # Step 3: Hotel
    hotel_prompt = (
        f"Recommend a hotel in {ctx.destination} for a traveler arriving at {ctx.arrival_time}. "
        f"Prefer locations near the airport or city center."
    )
    hotel_result = await hotel_agent.run(prompt=hotel_prompt, deps=deps)
    ctx.hotel_name = hotel_result.output.name
    ctx.hotel_location = hotel_result.output.location
    print(
        f"🏨 Hotel: {ctx.hotel_name}, {hotel_result.output.stars}★ at ${hotel_result.output.price_per_night_usd}/night"
    )

    # Step 4: Activities
    activities_prompt = (
        f"Suggest activities in {ctx.destination} close to {ctx.hotel_location} "
        f"and suitable for a traveler arriving at {ctx.arrival_time}."
    )
    activity_result = await activity_agent.run(prompt=activities_prompt, deps=deps)
    print(f"🎯 Activities for {activity_result.output.personalized_for}:")
    for a in activity_result.output.top_activities:
        print(f"  - {a}")


# ----------------------------------
# Main Execution
# ----------------------------------


async def main():
    deps = TravelDeps(user_name="Maria")
    await plan_trip("I want a quiet, sunny destination near the ocean.", deps)


if __name__ == "__main__":
    asyncio.run(main())
