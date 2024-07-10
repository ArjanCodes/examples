from typing import Any, Optional

import uvicorn
from db import Base, DBUser
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    Session,
    sessionmaker,
)

DATABASE_URL = "sqlite:///test.db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    fullname: Optional[str] = None
    custom_data: Optional[dict[str, Any]] = None


class UserCreate(BaseModel):
    name: str
    fullname: Optional[str] = None
    custom_data: Optional[dict[str, Any]] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    fullname: Optional[str] = None
    custom_data: Optional[dict[str, Any]] = None


# Dependency to get the database session
def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)) -> User:
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**db_user.dict())


@app.post("/users", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    db_user = DBUser(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return User(**db_user.dict())


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)) -> User:
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.update(user.model_dump())
    db.commit()
    db.refresh(db_user)
    return User(**db_user.dict())


@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> User:
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return User(**db_user.dict())


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
