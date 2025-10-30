from fastapi import FastAPI
from .api import router, limiter
from .models import Base
from .database import engine
from .config import settings
import logging
import sentry_sdk

Base.metadata.create_all(bind=engine)

sentry_sdk.init(dsn=settings.sentry_dsn)
logging.basicConfig(level=settings.log_level)

app = FastAPI()
app.include_router(router)
app.state.limiter = limiter