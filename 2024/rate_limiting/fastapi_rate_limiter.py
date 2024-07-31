from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from slowapi import Limiter
from slowapi.util import get_remote_address

RATE_LIMITING_ENABLED = True

app = FastAPI()
limiter = Limiter(
    key_func=get_remote_address,
    strategy="fixed-window",
    storage_uri="memory://",
    enabled=RATE_LIMITING_ENABLED,
)


@app.get("/limited")
@limiter.limit("2/second", per_method=True)
async def limited_route(request: Request) -> dict[str, str]:
    return {"message": "This is a limited route"}


@app.get("/unlimited")
async def unlimited_route(request: Request) -> dict[str, str]:
    return {"message": "This is an unlimited route"}


def main() -> None:
    client = TestClient(app)
    for _ in range(5):
        response = client.get("/unlimited")
        print(response.status_code, response.json())

    for _ in range(5):
        response = client.get("/limited")
        print(response.status_code, response.json())


if __name__ == "__main__":
    main()
