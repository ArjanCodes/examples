from pydantic import BaseModel
from typing import Optional, TypedDict

class Storm(BaseModel):
    name: str
    type: Optional[str] = None  # For example, "Hurricane", "Tornado", etc.
    severity: Optional[str] = None  # For example, "Mild", "Severe", etc.

class StormData(TypedDict):
    name: str
    type: Optional[str] | None  # For example, "Hurricane", "Tornado", etc.
    severity: Optional[str] | None  # For example, "Mild", "Severe", etc.
