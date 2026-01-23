from api import router
from fastapi import FastAPI

from .db import init_db

app = FastAPI(title="Ports & adapters")

app.include_router(router)


@app.on_event("startup")
def on_startup() -> None:
    init_db("sqlite:///./before.db")
