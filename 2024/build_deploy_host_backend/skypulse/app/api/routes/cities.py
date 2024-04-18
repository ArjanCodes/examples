from typing import Sequence
from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db_session
from app.schemas import City, CityCreate, CityUpdate
import app.models as models
import app.crud.cities as cities

router = APIRouter()


@router.post("/cities/", response_model=City)
async def create_city(
    city: CityCreate, db: AsyncSession = Depends(get_db_session)
) -> City:
    logger.info(f"Creating city: {city}")
    city_params = CityCreate(**city.model_dump())
    created_city = await cities.create_city(db, city_params)
    logger.info(f"City created: {created_city}")
    return created_city


@router.get("/cities/", response_model=list[City])
async def get_cities(db: AsyncSession = Depends(get_db_session)) -> Sequence[City]:
    logger.info("Fetching cities")
    result = await db.execute(select(models.City))
    city_list = result.scalars().all()
    logger.info(f"Fetched cities: {city_list}")
    return city_list


@router.get("/cities/{city_id}", response_model=City)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db_session)) -> City:
    logger.info(f"Fetching city with id: {city_id}")
    city = await cities.get_city(db, city_id)
    logger.info(f"Fetched city: {city}")
    return city


@router.put("/cities/{city_id}", response_model=City)
async def update_city(
    city_id: int, params: CityUpdate, db: AsyncSession = Depends(get_db_session)
) -> City:
    logger.info(f"Updating city with id: {city_id}")
    city = await cities.update_city(db, city_id, params)
    logger.info(f"Updated city: {city}")
    return city


@router.delete("/cities/{city_id}", response_model=City)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db_session)) -> City:
    logger.info(f"Deleting city with id: {city_id}")
    city = await cities.delete_city(db, city_id)
    logger.info(f"Deleted city: {city}")
    return city
