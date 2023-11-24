from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers.items import router as items_router
from routers.automations import router as automations_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(items_router)
app.include_router(automations_router)


@app.get("/")
def read_root():
    return "Server is running."
