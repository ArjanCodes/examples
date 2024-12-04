from fastapi import FastAPI
from src.routers.customers import customer_router
from src.routers.payments import payments_route

app = FastAPI()

app.include_router(customer_router)
app.include_router(payments_route)
