# shop_api/main.py
from __future__ import annotations

from database import engine
from db_models import Base
from fastapi import FastAPI
from routes import router


def create_app() -> FastAPI:
    app = FastAPI(title="Shop API with custom_data")
    app.include_router(router)
    return app


def main() -> FastAPI:
    Base.metadata.create_all(bind=engine)
    return create_app()


app = main()
