from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from slowapi import Limiter
from slowapi.util import get_remote_address

app = FastAPI()
limiter = Limiter(
    key_func=get_remote_address,
)


@app.get("/limited")
@limiter.limit("2/second")
async def limited_route(request: Request) -> dict[str, str]:
    return {"message": "This is a limited route"}


def main() -> None:
    client = TestClient(app)

    for _ in range(5):
        response = client.get("/limited")
        print(response.status_code, response.json())


if __name__ == "__main__":
    main()
