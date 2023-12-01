from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers.items import router as items_router
from routers.automations import router as automations_router
from routers.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(items_router)
app.include_router(automations_router)

app.state.limiter = limiter
app = FastAPI()
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
def read_root():
    return "Server is running."
