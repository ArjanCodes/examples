from datetime import UTC, datetime
from typing import Any

from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()


class ReceivedWebhook(BaseModel):
    received_at: datetime
    headers: dict[str, str]
    payload: dict[str, Any]


received_webhooks: list[ReceivedWebhook] = []


@app.post("/webhook")
async def receive_webhook(request: Request) -> dict[str, str]:
    payload = await request.json()

    webhook = ReceivedWebhook(
        received_at=datetime.now(UTC),
        headers=dict(request.headers),
        payload=payload,
    )

    received_webhooks.append(webhook)

    print("\nReceived webhook:")
    print(webhook.model_dump_json(indent=2))

    return {"status": "received"}


@app.get("/webhooks")
def list_received_webhooks() -> list[ReceivedWebhook]:
    return received_webhooks
