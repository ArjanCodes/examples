from fastapi import FastAPI
from src.routers.customers import customer_router

app = FastAPI()

app.include_router(customer_router)