import links
import webhooks
from fastapi import FastAPI

app = FastAPI()

app.include_router(links.router)
app.include_router(webhooks.router)
