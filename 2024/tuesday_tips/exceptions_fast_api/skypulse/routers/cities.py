from sqlite3 import Cursor
from fastapi import APIRouter, Depends, HTTPException
from exceptions import CityAlreadyExistsException, CityNotFoundException
from skypulse.database.database import setup_db_connection
from skypulse.models.cities import create, delete, index, show, update
from skypulse.schemas.city import City, CityData


router = APIRouter()


@router.get("/cities/", response_model=list[City])
async def read_cities(cursor: Cursor = Depends(setup_db_connection)):
    raise CityNotFoundException(city_id=2)
    return index(cursor)


@router.get("/cities/{city_id}", response_model=City)
async def read_city(city_id: int, cursor: Cursor = Depends(setup_db_connection)):
    city = show(cursor, city_id)
    # if not city:
    # raise CityNotFoundException(message=[{"city_id": city_id}])
    return city


@router.post("/cities/", response_model=City)
async def create_city(
    city_data: CityData, cursor: Cursor = Depends(setup_db_connection)
) -> City:
    try:
        city = create(cursor, city_data)
        return city
    except CityAlreadyExistsException:
        raise HTTPException(status_code=404, detail="City already exists")
    finally:
        print("/citites/ POST was called")


@router.put("/cities/{city_id}", response_model=City)
async def update_city(
    city_id: int, city_data: CityData, cursor: Cursor = Depends(setup_db_connection)
) -> City:
    city = update(cursor, city_id, city_data)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.delete("/cities/{city_id}", response_model=City)
async def delete_city(
    city_id: int, cursor: Cursor = Depends(setup_db_connection)
) -> City:
    city = delete(cursor, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city
