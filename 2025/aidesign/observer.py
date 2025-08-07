import asyncio
import os
import time
from dataclasses import dataclass
from typing import Protocol

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")


# ----------------------------------
# Dependencies and Output Schema
# ----------------------------------

@dataclass
class TravelDeps:
    user_name: str
    origin_city: str


class TravelResponse(BaseModel):
    destination: str
    message: str


# ----------------------------------
# Observer Interface
# ----------------------------------

class AgentCallObserver(Protocol):
    def notify(
        self,
        agent_name: str,
        prompt: str,
        deps: TravelDeps,
        output: BaseModel,
        duration: float,
    ) -> None:
        ...


class ConsoleLogger(AgentCallObserver):
    def notify(
        self,
        agent_name: str,
        prompt: str,
        deps: TravelDeps,
        output: BaseModel,
        duration: float,
    ) -> None:
        print("\n📋 Agent Call Log")
        print(f"Agent: {agent_name}")
        print(f"Prompt: {prompt}")
        print(f"User: {deps.user_name}, Origin: {deps.origin_city}")
        print(f"Output: {output.model_dump()}")
        print(f"Duration: {duration:.2f}s")


# ----------------------------------
# Wrapper to run agent with observers
# ----------------------------------

async def run_with_observers(
    *,
    agent: Agent[TravelDeps, BaseModel],
    prompt: str,
    deps: TravelDeps,
    observers: list[AgentCallObserver],
) -> TravelResponse:
    start = time.perf_counter()
    result = await agent.run(prompt, deps=deps)
    end = time.perf_counter()
    duration = end - start

    for observer in observers:
        observer.notify(
            agent_name=agent.name or "Unnamed Agent",
            prompt=prompt,
            deps=deps,
            output=result.output,
            duration=duration,
        )

    return result.output


# ----------------------------------
# Agent Definition
# ----------------------------------

travel_agent = Agent(
    "openai:gpt-4o",
    name="TravelAgent",
    deps_type=TravelDeps,
    output_type=TravelResponse,
    system_prompt="You are a friendly travel assistant. Recommend a destination based on user preferences.",
)


# ----------------------------------
# Main Program
# ----------------------------------

async def main():
    deps = TravelDeps(user_name="Nina", origin_city="Copenhagen")

    prompt = "I want to escape to a cozy place in the mountains for the weekend."
    output = await run_with_observers(
        agent=travel_agent,
        prompt=prompt,
        deps=deps,
        observers=[ConsoleLogger()],
    )

    print(f"\n🤖 Travel Agent says: {output.message}")
    print(f"📍 Destination Suggested: {output.destination}")


if __name__ == "__main__":
    asyncio.run(main())