from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from db.core import get_db, NotFoundError
from db.automations import (
    Automation,
    AutomationCreate,
    AutomationUpdate,
    create_db_automation,
    delete_db_automation,
    read_db_automation,
    update_db_automation,
)


router = APIRouter(
    prefix="/automations",
)


@router.post("")
def create_automation(
    automation: AutomationCreate, db: Session = Depends(get_db)
) -> Automation:
    db_automation = create_db_automation(automation, db)
    return Automation(**db_automation.__dict__)


@router.get("/{automation_id}")
def read_automation(automation_id: int, db: Session = Depends(get_db)) -> Automation:
    try:
        db_automation = read_db_automation(automation_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Automation(**db_automation.__dict__)


@router.put("/{automation_id}")
def update_automation(
    automation_id: int,
    automation: AutomationUpdate,
    db: Session = Depends(get_db),
) -> Automation:
    try:
        db_automation = update_db_automation(automation_id, automation, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Automation(**db_automation.__dict__)


@router.delete("/{automation_id}")
def delete_item(automation_id: int, db: Session = Depends(get_db)) -> Automation:
    try:
        db_automation = delete_db_automation(automation_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Automation(**db_automation.__dict__)
