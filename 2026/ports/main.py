from api import router
from db import init_db
from fastapi import FastAPI

app = FastAPI(title="Ports & adapters")


@app.on_event("startup")
def on_startup() -> None:
    init_db("sqlite:///./before.db")


app.include_router(router)
