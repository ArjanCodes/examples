import hashlib
import time
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable

from fastapi import FastAPI, HTTPException, Request

app = FastAPI()


# Mock database of API keys and their respective limits
@dataclass
class RateLimit:
    max_calls: int
    period: int


api_key_limits = {
    "api_key_1": RateLimit(max_calls=5, period=60),
    "api_key_2": RateLimit(max_calls=10, period=60),
}


def rate_limit():
    def decorator(func: Callable[[Request], Any]) -> Callable[[Request], Any]:
        usage: dict[str, list[float]] = {}

        @wraps(func)
        async def wrapper(request: Request) -> Any:
            # get the API key
            api_key = request.headers.get("X-API-KEY")
            if not api_key:
                raise HTTPException(status_code=400, detail="API key missing")

            # check if the API key is valid
            if api_key not in api_key_limits:
                raise HTTPException(status_code=403, detail="Invalid API key")

            # get the rate limits for the API key
            limits = api_key_limits[api_key]

            # get the client's IP address
            if not request.client:
                raise ValueError("Request has no client information")
            ip_address: str = request.client.host

            # create a unique identifier for the client
            unique_id: str = hashlib.sha256((api_key + ip_address).encode()).hexdigest()

            # update the timestamps
            now = time.time()
            if unique_id not in usage:
                usage[unique_id] = []
            timestamps = usage[unique_id]
            timestamps[:] = [t for t in timestamps if now - t < limits.period]

            if len(timestamps) < limits.max_calls:
                timestamps.append(now)
                return await func(request)

            # calculate the time to wait before the next request
            wait = limits.period - (now - timestamps[0])
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Retry after {wait:.2f} seconds",
            )

        return wrapper

    return decorator


@app.get("/")
@rate_limit()
async def read_root(request: Request):
    return {"message": "Hello, World!"}


# Run the server using `uvicorn script_name:app --reload`
