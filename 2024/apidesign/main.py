import json
from typing import Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel, field_serializer, model_validator
from sqlalchemy import String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)


class Base(DeclarativeBase):
    pass


class DBUser(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    custom_data: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


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

    @model_validator(mode="before")
    @classmethod
    def convert_custom_data(cls, data: dict[str, Any]) -> dict[str, Any]:
        if "custom_data" in data:
            data["custom_data"] = json.loads(data["custom_data"])
        return data


class UserCreate(BaseModel):
    name: str
    fullname: Optional[str] = None
    custom_data: Optional[dict[str, Any]] = None

    @field_serializer("custom_data")
    def serialize_custom_data(self, custom_data: Any) -> str | None:
        print(custom_data)
        if not custom_data:
            return None
        return json.dumps(custom_data)


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
    return User(**db_user.__dict__)


@app.post("/users", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    db_user = DBUser(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return User(**db_user.__dict__)


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)) -> User:
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.model_dump().items():
        if value is None:
            continue
        if key == "custom_data":
            # create JSON of current custom_data
            custom_data_json = json.loads(db_user.custom_data or "{}")
            # unset keys with value None and update the rest
            for k, v in value.items():
                if v is None:
                    del custom_data_json[k]
                else:
                    custom_data_json[k] = v
            # convert back to string
            value = json.dumps(custom_data_json)
        if value:
            setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return User(**db_user.__dict__)


@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> User:
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return User(**db_user.__dict__)


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
