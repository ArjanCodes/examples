from database import engine
from db_models import Base
from fastapi import FastAPI
from routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shop API")
app.include_router(router)
