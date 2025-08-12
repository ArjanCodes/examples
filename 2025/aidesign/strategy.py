import asyncio
from dataclasses import dataclass
from typing import Callable

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent

# Load API key
load_dotenv()

# ----------------------------------
# Common Output Model
# ----------------------------------


class TravelRecommendation(BaseModel):
    destination: str = Field(..., description="Recommended destination")
    message: str = Field(..., description="Message from the travel agent to the user")


# ----------------------------------
# Dependencies (for extensibility)
# ----------------------------------


@dataclass
class TravelDeps:
    user_name: str


# ----------------------------------
# Strategy Functions
# Each strategy returns an Agent with a specific personality
# ----------------------------------


def professional_agent() -> Agent[TravelDeps, TravelRecommendation]:
    return Agent(
        "openai:gpt-4o",
        deps_type=TravelDeps,
        output_type=TravelRecommendation,
        system_prompt=(
            "You are a highly professional and polite travel agent. "
            "You give thoughtful recommendations based on user preferences."
        ),
    )


def fun_agent() -> Agent[TravelDeps, TravelRecommendation]:
    return Agent(
        "openai:gpt-4o",
        deps_type=TravelDeps,
        output_type=TravelRecommendation,
        system_prompt=(
            "You are a fun, quirky travel agent who gets super excited about cool places. "
            "Your responses are friendly and humorous, but still helpful."
        ),
    )


def budget_agent() -> Agent[TravelDeps, TravelRecommendation]:
    return Agent(
        "openai:gpt-4o",
        deps_type=TravelDeps,
        output_type=TravelRecommendation,
        system_prompt=(
            "You are a frugal travel expert who finds great destinations with low cost. "
            "Your suggestions should highlight affordability and value."
        ),
    )


# ----------------------------------
# Function to Run Strategy
# ----------------------------------


async def run_travel_strategy(
    user_prompt: str,
    deps: TravelDeps,
    strategy_fn: Callable[[], Agent[TravelDeps, TravelRecommendation]],
):
    agent = strategy_fn()
    result = await agent.run(user_prompt, deps=deps)
    output = result.output

    # Display the structured response
    print(f"\n👤 {deps.user_name} asked: {user_prompt}")
    print(f"🤖 {agent.model}: {output.message}")
    print(f"📍 Destination: {output.destination}")


# ----------------------------------
# Run Example with Different Strategies
# ----------------------------------


async def main():
    deps = TravelDeps(user_name="Sam")

    print("=== Professional Agent ===")
    await run_travel_strategy(
        "I want a peaceful place by the sea.", deps, professional_agent
    )

    print("\n=== Fun Agent ===")
    await run_travel_strategy("I want a peaceful place by the sea.", deps, fun_agent)

    print("\n=== Budget Agent ===")
    await run_travel_strategy("I want a peaceful place by the sea.", deps, budget_agent)


if __name__ == "__main__":
    asyncio.run(main())
