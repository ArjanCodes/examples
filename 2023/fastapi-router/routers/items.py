from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from db.core import DatabaseService, NotFoundError
from db.items import (
    Item,
    ItemCreate,
    ItemUpdate,
    read_db_item,
    create_db_item,
    update_db_item,
    delete_db_item,
)


router = APIRouter(
    prefix="/items",
)


@router.post("")
def create_item(
    item: ItemCreate, db: DatabaseService = Depends(DatabaseService)
) -> Item:
    db_item = create_db_item(item, next(db.get_session()))
    return Item(**db_item.__dict__)


@router.get("/{item_id}")
def read_item(item_id: int, db: DatabaseService = Depends(DatabaseService)) -> Item:
    try:
        db_item = read_db_item(item_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Item(**db_item.__dict__)


@router.put("/{item_id}")
def update_item(
    item_id: int, item: ItemUpdate, db: DatabaseService = Depends(DatabaseService)
) -> Item:
    try:
        db_item = update_db_item(item_id, item, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Item(**db_item.__dict__)


@router.delete("/{item_id}")
def delete_item(item_id: int, db: DatabaseService = Depends(DatabaseService)) -> Item:
    try:
        db_item = delete_db_item(item_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Item(**db_item.__dict__)
