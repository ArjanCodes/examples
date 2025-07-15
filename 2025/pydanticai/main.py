from dataclasses import dataclass
from typing import Any
import asyncio

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


# Mock database
@dataclass
class Patient:
    id: int
    name: str
    vitals: dict[str, Any]

PATIENT_DB = {
    42: Patient(id=42, name="John Doe", vitals={"heart_rate": 72, "blood_pressure": "120/80"}),
    43: Patient(id=43, name="Jane Smith", vitals={"heart_rate": 65, "blood_pressure": "110/70"}),
}

class DatabaseConn:
    async def patient_name(self, id: int) -> str:
        patient = PATIENT_DB.get(id)
        return patient.name if patient else "Unknown Patient"

    async def latest_vitals(self, id: int) -> dict[str, Any]:
        patient = PATIENT_DB.get(id)
        return patient.vitals if patient else {"heart_rate": 0, "blood_pressure": "N/A"}


@dataclass
class TriageDependencies:
    patient_id: int
    db: DatabaseConn


class TriageOutput(BaseModel):
    response_text: str = Field(description="Message to the patient")
    escalate: bool = Field(description="Should escalate to a human nurse")
    urgency: int = Field(description="Urgency level from 0 to 10", ge=0, le=10)


triage_agent = Agent(
    "openai:gpt-4o",
    deps_type=TriageDependencies,
    output_type=TriageOutput,
    system_prompt=(
        "You are a triage assistant helping patients. "
        "Provide clear advice and assess urgency."
    ),
)


@triage_agent.system_prompt
async def add_patient_name(ctx: RunContext[TriageDependencies]) -> str:
    patient_name = await ctx.deps.db.patient_name(id=ctx.deps.patient_id)
    return f"The patient's name is {patient_name!r}."


@triage_agent.tool
async def latest_vitals(ctx: RunContext[TriageDependencies]) -> dict[str, Any]:
    """Returns the patient's latest vital signs."""
    return await ctx.deps.db.latest_vitals(id=ctx.deps.patient_id)


async def main() -> None:
    deps = TriageDependencies(patient_id=43, db=DatabaseConn())

    result = await triage_agent.run(
        "I have chest pain and trouble breathing.",
        deps=deps,
    )
    print(result.output)
    """
    Example output:
    response_text='Your symptoms are serious. Please call emergency services immediately. A nurse will contact you shortly.'
    escalate=True
    urgency=10
    """

    result = await triage_agent.run(
        "I have a mild headache since yesterday.",
        deps=deps,
    )
    print(result.output)
    """
    Example output:
    response_text='It sounds like your headache is not severe, but monitor it closely. If it worsens or you develop new symptoms, contact your doctor.'
    escalate=False
    urgency=3
    """


if __name__ == "__main__":
    asyncio.run(main())