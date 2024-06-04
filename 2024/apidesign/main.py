import json
from typing import Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel, field_serializer
from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    sessionmaker,
)


class Base(DeclarativeBase):
    pass


class DBUser(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[list["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    custom_data: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class DBAddress(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
    custom_data: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    fullname: Optional[str] = None
    addresses: list["Address"] = []
    custom_data: Optional[str] = None

    @field_serializer("custom_data")
    def custom_data_serializer(cls, custom_data: Any):
        return json.loads(custom_data)


class UserCreate(BaseModel):
    name: str
    fullname: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    fullname: Optional[str] = None


class Address(BaseModel):
    id: int
    email_address: str
    user_id: int
    custom_data: Optional[str] = None

    @field_serializer("custom_data")
    def custom_data_serializer(cls, custom_data: Any):
        return json.loads(custom_data)


class AddressCreate(BaseModel):
    user_id: str
    email_address: str


class AddressUpdate(BaseModel):
    email_address: Optional[str] = None


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


@app.get("/users/{user_id}/addresses", response_model=list[Address])
def read_addresses(user_id: int, db: Session = Depends(get_db)) -> list[Address]:
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user.addresses


@app.post("/users/{user_id}/addresses", response_model=Address)
def create_address(address: AddressCreate, db: Session = Depends(get_db)) -> Address:
    db_address = DBAddress(**address.model_dump())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return Address(**db_address.__dict__)


@app.put("/users/{user_id}/addresses/{address_id}", response_model=Address)
def update_address(
    address_id: int, address: AddressUpdate, db: Session = Depends(get_db)
) -> Address:
    db_address = db.query(DBAddress).filter(DBAddress.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    for key, value in address.model_dump().items():
        setattr(db_address, key, value)
    db.commit()
    db.refresh(db_address)
    return Address(**db_address.__dict__)


@app.delete("/users/{user_id}/addresses/{address_id}", response_model=Address)
def delete_address(address_id: int, db: Session = Depends(get_db)) -> Address:
    db_address = db.query(DBAddress).filter(DBAddress.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    return Address(**db_address.__dict__)


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
