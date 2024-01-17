from fastapi import FastAPI
from routers import storms, cities

from exceptions import CityNotFoundException
from exceptions.handlers import city_not_found_exception_handler

app = FastAPI()


app.include_router(storms.router)
app.include_router(cities.router)

@app.get("/")
async def root():
    return {"message": "Skypusle is active"}


app.add_exception_handler(CityNotFoundException, city_not_found_exception_handler) #type: ignore