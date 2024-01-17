from fastapi import Request
from fastapi.responses import JSONResponse

from exceptions import CityNotFoundException

async def city_not_found_exception_handler(request: Request, exc: CityNotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"message": f"{str(exc)}"},
    )