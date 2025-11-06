import logging

import uvicorn
from api import limiter, router
from config import get_settings
from database import engine
from fastapi import FastAPI
from models import Base

Base.metadata.create_all(bind=engine)

logging.basicConfig(level=get_settings().log_level)

app = FastAPI()
app.include_router(router)
app.state.limiter = limiter

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
