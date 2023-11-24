from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from db.core import NotFoundError, get_db
from db.items import (
    Item,
    ItemCreate,
    ItemUpdate,
    read_db_item,
    create_db_item,
    update_db_item,
    delete_db_item,
    read_db_automations_for_item,
)
from db.automations import Automation


router = APIRouter(
    prefix="/items",
)


@router.post("")
def create_item(item: ItemCreate, db: Session = Depends(get_db)) -> Item:
    db_item = create_db_item(item, db)
    return Item(**db_item.__dict__)


@router.get("/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    try:
        db_item = read_db_item(item_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Item(**db_item.__dict__)


@router.get("/{item_id}/automations")
def read_item_automations(
    item_id: int, db: Session = Depends(get_db)
) -> list[Automation]:
    try:
        automations = read_db_automations_for_item(item_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return [Automation(**automation.__dict__) for automation in automations]


@router.put("/{item_id}")
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)) -> Item:
    try:
        db_item = update_db_item(item_id, item, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Item(**db_item.__dict__)


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    try:
        db_item = delete_db_item(item_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Item(**db_item.__dict__)
