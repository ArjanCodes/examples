from typing import Sequence
from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import weathers
from app.database.session import get_db_session
from app.schemas import Weather, WeatherUpdate, WeatherCreate
from sqlalchemy.future import select
import app.models as models


router = APIRouter()


@router.get("/weather/{weather_id}", response_model=Weather)
async def get_weather(
    weather_id: int, db: AsyncSession = Depends(get_db_session)
) -> Weather:
    logger.info(f"Fetching weather with id: {weather_id}")
    weather = await weathers.get_weather(db, weather_id)
    logger.info(f"Fetched weather: {weather}")
    return weather


@router.post("/weather/", response_model=Weather)
async def create_weather(
    weather: WeatherCreate, db: AsyncSession = Depends(get_db_session)
) -> Weather:
    logger.info(f"Creating weather: {weather}")
    weather_params = WeatherCreate(**weather.model_dump())
    created_weather = await weathers.create_weather(db, weather_params)
    logger.info(f"Created weather: {weather}")
    return created_weather


@router.get("/weather/", response_model=list[Weather])
async def get_weathers(db: AsyncSession = Depends(get_db_session)) -> Sequence[Weather]:
    logger.info("Fetching weathers")
    result = await db.execute(select(models.Weather))
    weathers = result.scalars().all()
    logger.info(f"Fetched weathers: {weathers}")
    return weathers


@router.put("/weather/{weather_id}", response_model=Weather)
async def update_weather(
    weather_id: int, params: WeatherUpdate, db: AsyncSession = Depends(get_db_session)
) -> Weather:
    logger.info(f"Updating weather with id: {weather_id}")
    weather = await weathers.update_weather(db, weather_id, params)
    logger.info(f"Updated weather: {weather}")
    return weather


@router.delete("/weather/{weather_id}", response_model=Weather)
async def delete_weather(
    weather_id: int, db: AsyncSession = Depends(get_db_session)
) -> Weather:
    logger.info(f"Deleting weather with id: {weather_id}")
    weather = await weathers.delete_weather(db, weather_id)
    logger.info(f"Deleted weather: {weather}")
    return weather
