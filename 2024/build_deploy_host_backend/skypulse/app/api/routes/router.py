from fastapi import APIRouter

from . import cities, weathers  # Import the missing modules

base_router = APIRouter()

base_router.include_router(
    cities.router, tags=["cities"], prefix="/v1"
)  # Define the missing variable "cities"
base_router.include_router(weathers.router, tags=["weathers"], prefix="/v1")
