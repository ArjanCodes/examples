import links
from fastapi import FastAPI

app = FastAPI()

app.include_router(links.router)
