from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from routers.items import router as items_router
from db.core import Base, DatabaseService, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(items_router)


@app.get("/")
def read_root():
    return "Server is running."
