from contextlib import asynccontextmanager
from sqlite3 import DataError, IntegrityError
from typing import Callable
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from loguru import logger
from app.api.routes.router import base_router as router
from app.exceptions.exceptions import (
    AuthenticationFailed,
    BaseError,
    EntityDoesNotExistError,
    InvalidOperationError,
    InvalidTokenError,
    ServiceError,
)
from core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from app.database.session import sessionmanager


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager.engine is not None:
        await sessionmanager.close()


app = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
app.include_router(router, prefix=API_PREFIX)


def create_exception_handler(
    status_code: int, detail: str
) -> Callable[[Request, BaseError], JSONResponse]:
    async def exception_handler(_: Request, exc: BaseError) -> JSONResponse:
        nonlocal detail

        if exc.message:
            detail = exc.message

        if exc.name:
            detail = f"{detail} [{exc.name}]"

        logger.error(exc)
        return JSONResponse(status_code=status_code, content={"detail": detail})

    return exception_handler


app.add_exception_handler(
    exc_class_or_status_code=EntityDoesNotExistError,
    handler=create_exception_handler(
        status.HTTP_404_NOT_FOUND, "Entity does not exist."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=InvalidOperationError,
    handler=create_exception_handler(
        status.HTTP_400_BAD_REQUEST, "Can't perform the operation."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=IntegrityError,
    handler=create_exception_handler(
        status.HTTP_400_BAD_REQUEST, "Can't process the request due to integrity error."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=DataError,
    handler=create_exception_handler(
        status.HTTP_400_BAD_REQUEST, "Data can't be processed, check the input."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=AuthenticationFailed,
    handler=create_exception_handler(
        status.HTTP_401_UNAUTHORIZED,
        "Authentication failed due to invalid credentials.",
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=InvalidTokenError,
    handler=create_exception_handler(
        status.HTTP_401_UNAUTHORIZED, "Invalid token, please re-authenticate again."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=ServiceError,
    handler=create_exception_handler(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "A service seems to be down, try again later.",
    ),
)
