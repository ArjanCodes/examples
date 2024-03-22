from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.exceptions.exceptions import EntityDoesNotExistError
from app.schemas import Weather, WeatherCreate, WeatherUpdate


async def get_weather(db_session: AsyncSession, weather_id: int) -> Weather:
    weather = (
        await db_session.scalars(
            select(models.Weather).where(models.Weather.id == weather_id)
        )
    ).first()
    if not weather:
        raise EntityDoesNotExistError
    return weather


async def get_weathers(db_session: AsyncSession) -> Sequence[Weather]:
    result = await db_session.execute(select(models.Weather))
    weathers = result.scalars().all()
    return weathers


async def create_weather(db_session: AsyncSession, params: WeatherCreate) -> Weather:
    weather = models.Weather(**params.model_dump())

    db_session.add(weather)
    await db_session.commit()
    await db_session.refresh(weather)
    return weather


async def update_weather(
    db_session: AsyncSession, weather_id: int, params: WeatherUpdate
) -> Weather:
    weather = await get_weather(db_session, weather_id)
    for attr, value in params.model_dump(exclude_unset=True).items():
        setattr(weather, attr, value)
    db_session.add(weather)
    await db_session.commit()
    await db_session.refresh(weather)
    return weather


async def delete_weather(db_session: AsyncSession, weather_id: int) -> Weather:
    weather = await get_weather(db_session, weather_id)
    await db_session.delete(weather)
    await db_session.commit()
    return weather
