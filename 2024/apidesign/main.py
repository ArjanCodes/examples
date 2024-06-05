import json
from typing import Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
    validates,
)

DATABASE_URL = "sqlite:///test.db"


class Base(DeclarativeBase):
    custom_data: Mapped[Optional[str]]

    @validates("custom_data")
    def validate_custom_data(self, _: str, custom_data: Any) -> str:
        if not custom_data:
            return "{}"
        elif isinstance(custom_data, dict):
            return json.dumps(custom_data)
        else:
            return custom_data

    def update_item(self, key: str, value: Any) -> None:
        if value is None:
            return
        if key == "custom_data":
            self.update_custom_data(value)
        else:
            setattr(self, key, value)

    def update(self, data: dict[str, Any]) -> None:
        for key, value in data.items():
            self.update_item(key, value)

    def update_custom_data(self, custom_data: dict[str, Any]) -> None:
        # create JSON of current custom_data
        custom_data_json = json.loads(self.custom_data or "{}")
        # unset keys with value None and update the rest
        for k, v in custom_data.items():
            if v is None:
                custom_data_json.pop(k, None)
            else:
                custom_data_json[k] = v
        # convert back to string
        setattr(self, "custom_data", json.dumps(custom_data_json))

    def dict(self) -> dict[str, Any]:
        export_dict: dict[str, Any] = {}
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            elif key == "custom_data":
                export_dict[key] = json.loads(value)
            else:
                export_dict[key] = value
        return export_dict


class DBUser(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


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
