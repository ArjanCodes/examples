from datetime import UTC, datetime
from uuid import UUID, uuid4

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

app = FastAPI()

links: dict[str, "ShortLink"] = {}
webhooks: dict[UUID, "Webhook"] = {}


class ShortLinkCreate(BaseModel):
    target_url: HttpUrl


class ShortLink(BaseModel):
    id: UUID
    short_code: str
    target_url: HttpUrl
    clicks: int = 0


class WebhookCreate(BaseModel):
    url: HttpUrl


class Webhook(BaseModel):
    id: UUID
    url: HttpUrl


@app.post("/links")
def create_short_link(data: ShortLinkCreate) -> ShortLink:
    short_code = uuid4().hex[:6]

    link = ShortLink(
        id=uuid4(),
        short_code=short_code,
        target_url=data.target_url,
    )

    links[short_code] = link
    return link


@app.get("/links")
def list_short_links() -> list[ShortLink]:
    return list(links.values())


@app.post("/webhooks")
def create_webhook(data: WebhookCreate) -> Webhook:
    webhook = Webhook(
        id=uuid4(),
        url=data.url,
    )

    webhooks[webhook.id] = webhook
    return webhook


@app.get("/webhooks")
def list_webhooks() -> list[Webhook]:
    return list(webhooks.values())


@app.get("/{short_code}")
def redirect_to_target(short_code: str) -> RedirectResponse:
    link = links.get(short_code)

    if link is None:
        raise HTTPException(status_code=404, detail="Short link not found")

    link.clicks += 1

    payload = {
        "type": "link.clicked",
        "link_id": str(link.id),
        "short_code": link.short_code,
        "target_url": str(link.target_url),
        "clicks": link.clicks,
        "clicked_at": datetime.now(UTC).isoformat(),
    }

    for webhook in webhooks.values():
        httpx.post(
            str(webhook.url),
            json=payload,
            timeout=5,
        )

    return RedirectResponse(str(link.target_url))
