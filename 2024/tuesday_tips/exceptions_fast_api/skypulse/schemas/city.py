from typing import TypedDict
from git import Optional
from pydantic import BaseModel

class City(BaseModel):
    name: str
    country: Optional[str]
    population: Optional[int]

class CityData(TypedDict):
    name: str
    country: Optional[str] 
    population: Optional[int]