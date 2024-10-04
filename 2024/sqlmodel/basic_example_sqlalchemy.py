from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# SQLAlchemy model
Base = declarative_base()


class DBHero(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    secret_name = Column(String)
    age = Column(Integer, nullable=True)


# Pydantic models
class Hero(BaseModel):
    id: Optional[int] = None
    name: str
    secret_name: str
    age: Optional[int] = None


# FastAPI app
app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# Dependency
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a Hero
@app.post("/heroes/", response_model=Hero)
def create_hero(hero: Hero, session: Session = Depends(get_session)):
    db_hero = DBHero(**hero.model_dump())
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


# Read all heroes
@app.get("/heroes/", response_model=list[Hero])
def read_heroes(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    heroes = session.query(DBHero).offset(skip).limit(limit).all()
    return heroes


# Read a hero by ID
@app.get("/heroes/{hero_id}", response_model=Hero)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.query(DBHero).filter(DBHero.id == hero_id).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


# Update a Hero
@app.put("/heroes/{hero_id}", response_model=Hero)
def update_hero(hero_id: int, hero_data: Hero, session: Session = Depends(get_session)):
    hero = session.query(DBHero).filter(DBHero.id == hero_id).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    # Update the hero's attributes
    for field, value in hero_data.model_dump().items():
        setattr(hero, field, value)

    session.commit()
    session.refresh(hero)
    return hero


# Delete a Hero
@app.delete("/heroes/{hero_id}", response_model=Hero)
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.query(DBHero).filter(DBHero.id == hero_id).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    session.delete(hero)
    session.commit()
    return hero


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
