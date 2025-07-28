import asyncio
import os
from dataclasses import dataclass

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent

# Load API key
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

# -------------------------------
# Dependencies
# -------------------------------


@dataclass
class TravelDeps:
    user_name: str


# -------------------------------
# Main Response Output
# -------------------------------


class TravelResponse(BaseModel):
    message: str = Field(..., description="Response to the user")
    destination: str = Field(..., description="Suggested destination")


# -------------------------------
# Structured Log Entry
# -------------------------------


class LogEntry(BaseModel):
    level: str = Field(..., description="Log level: info, warning, error, etc.")
    message: str = Field(..., description="What the agent did")
    source: str = Field(
        ..., description="The part of the system that generated the log"
    )


# -------------------------------
# Agent: Travel Recommender
# -------------------------------

travel_agent = Agent(
    "openai:gpt-4o",
    deps_type=TravelDeps,
    output_type=TravelResponse,
    system_prompt="You are a helpful travel assistant. Recommend a good destination and respond politely.",
)


# -------------------------------
# Log Agent: Parallel Output
# -------------------------------

log_agent = Agent(
    "openai:gpt-4o",
    deps_type=TravelDeps,
    output_type=LogEntry,
    system_prompt="Log what the travel agent just did in a structured format.",
)


# -------------------------------
# Observer Interface
# -------------------------------


class Observer:
    def notify(self, log: LogEntry):
        pass


# -------------------------------
# Example Concrete Observer
# -------------------------------


class ConsoleLogger(Observer):
    def notify(self, log: LogEntry):
        print(f"[{log.level.upper()}] from {log.source}: {log.message}")


# -------------------------------
# Execution Function
# -------------------------------


async def recommend_travel(
    user_prompt: str, deps: TravelDeps, observers: list[Observer]
):
    # Step 1: Get the response from the agent
    response_result = await travel_agent.run(user_prompt, deps=deps)
    response = response_result.output

    # Step 2: Generate structured log from a separate agent
    log_prompt = (
        f"The agent suggested {response.destination} in response to a user prompt."
    )
    log_result = await log_agent.run(log_prompt, deps=deps)
    log_entry = log_result.output

    # Step 3: Notify observers
    for observer in observers:
        observer.notify(log_entry)

    # Step 4: Show user response
    print(f"\n👤 {deps.user_name} asked: {user_prompt}")
    print(f"🤖 Travel Agent says: {response.message}")
    print(f"📍 Destination Suggested: {response.destination}")


# -------------------------------
# Main
# -------------------------------


async def main():
    deps = TravelDeps(user_name="Alex")
    observers = [ConsoleLogger()]
    await recommend_travel("I want to go somewhere warm with beaches.", deps, observers)


if __name__ == "__main__":
    asyncio.run(main())
