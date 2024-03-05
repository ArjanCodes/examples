from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exceptions import EntityDoesNotExistError
import app.models as models
from app.schemas.city import City, CityCreate, CityUpdate


async def get_city(db_session: AsyncSession, city_id: int) -> City:
    city = (
        await db_session.scalars(select(models.City).where(models.City.id == city_id))
    ).first()
    if not city:
        raise EntityDoesNotExistError(message="City not found")
    return city


async def get_cities(db_session: AsyncSession) -> Sequence[City]:
    result = await db_session.execute(select(models.City))
    cities = result.scalars().all()
    return cities


async def create_city(db_session: AsyncSession, params: CityCreate) -> City:
    city = models.City(**params.model_dump())
    db_session.add(city)
    await db_session.commit()
    await db_session.refresh(city)
    return city


async def update_city(
    db_session: AsyncSession, city_id: int, params: CityUpdate
) -> City:
    city = await get_city(db_session, city_id)

    for attr, value in params.model_dump(exclude_unset=True).items():
        setattr(city, attr, value)
    db_session.add(city)
    await db_session.commit()
    await db_session.refresh(city)
    return city


async def delete_city(db_session: AsyncSession, city_id: int) -> City:
    city = await get_city(db_session, city_id)
    await db_session.delete(city)
    await db_session.commit()
    return city
