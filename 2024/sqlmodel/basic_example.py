from typing import List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select


# Define the Hero model
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


# Create the FastAPI app
app = FastAPI()

# Create the SQLite database engine
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)


# Dependency: Get the session
def get_session():
    with Session(engine) as session:
        yield session


# Create a Hero
@app.post("/heroes/", response_model=Hero)
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


# Read all heroes
@app.get("/heroes/", response_model=List[Hero])
def read_heroes(skip: int = 0, limit: int = 10):
    with Session(engine) as session:
        heroes = session.exec(select(Hero).offset(skip).limit(limit)).all()
        return heroes


# Read a hero by ID
@app.get("/heroes/{hero_id}", response_model=Hero)
def read_hero(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        return hero


# Update a Hero
@app.put("/heroes/{hero_id}", response_model=Hero)
def update_hero(hero_id: int, hero_data: Hero):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")

        # Update the hero's attributes
        hero.name = hero_data.name
        hero.secret_name = hero_data.secret_name
        hero.age = hero_data.age
        session.commit()
        session.refresh(hero)
        return hero


# Delete a Hero
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")

        session.delete(hero)
        session.commit()
        return hero


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
