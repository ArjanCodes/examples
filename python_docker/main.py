from dataclasses import dataclass, field

from fastapi import FastAPI, Response

app = FastAPI()


@dataclass
class Channel:
    id: str
    name: str
    tags: list[str] = field(default_factory=list)
    description: str | None = None


@app.get("/")
def read_root() -> Response:
    return Response("The server is running.")


@app.get("/channels/{channel_id}", response_model=Channel)
def read_item(channel_id: str) -> Channel:
    return Channel(
        id=channel_id,
        name="ArjanCodes",
        tags=["software design", "python"],
        description="ArjanCodes focuses on helping you become a better software developer.",
    )
