
import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from skypulse.database.database import setup_db_connection
from skypulse.models.storms import create, delete, index, show, update

from skypulse.schemas.storm import Storm, StormData

router = APIRouter()

@router.get("/storms/", response_model=list[Storm])
async def read_storms(cursor: sqlite3.Cursor = Depends(setup_db_connection)):
    return index(cursor)


@router.get("/storms/{storm_id}", response_model=Storm)
async def read_storm(storm_id: int, cursor: sqlite3.Cursor = Depends(setup_db_connection)):
    storm = show(cursor, storm_id)
    if not storm:
        raise HTTPException(status_code=404, detail="Storm not found")
    return storm


@router.post("/storms/", response_model=Storm)
async def create_storm(storm_data: StormData, cursor: sqlite3.Cursor = Depends(setup_db_connection)):
    create(cursor, storm_data)
    return storm_data


@router.put("/storms/{storm_id}", response_model=Storm)
async def update_storm(storm_id: int, storm_data: StormData, cursor: sqlite3.Cursor = Depends(setup_db_connection)) -> Storm:
    storm = update(cursor, storm_id, storm_data)
    if not storm:
        raise HTTPException(status_code=404, detail="Storm not found")
    return storm


@router.delete("/storms/{storm_id}", response_model=Storm)
async def delete_storm(storm_id: int, cursor: sqlite3.Cursor = Depends(setup_db_connection)) -> Storm:
    storm = delete(cursor, storm_id)
    if not storm:
        raise HTTPException(status_code=404, detail="Storm not found")
    return storm
