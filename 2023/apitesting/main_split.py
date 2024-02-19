from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends

from operations import (
    Item,
    Base,
    NotFoundError,
    ItemCreate,
    db_create_item,
    db_delete_item,
    db_read_item,
    db_update_item,
)


DATABASE_URL = "sqlite:///test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

app = FastAPI()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)


@app.post("/items")
def create_item(item: ItemCreate, db: Session = Depends(get_db)) -> Item:
    return db_create_item(item, db)


@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    try:
        return db_read_item(item_id, db)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")


@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)) -> Item:
    try:
        return db_update_item(item_id, item, db)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    try:
        return db_delete_item(item_id, db)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")
