from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from bson import ObjectId
from db import get_db, shutdown_db
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

Status = Literal["open", "triaged", "closed"]

PREVIEW_LEN = 80


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def oid_str(oid: ObjectId) -> str:
    return str(oid)


def parse_object_id(ticket_id: str) -> ObjectId:
    try:
        return ObjectId(ticket_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid ticket id") from e


def make_preview(message: str) -> str:
    msg = message.strip().replace("\n", " ")
    return msg if len(msg) <= PREVIEW_LEN else msg[: PREVIEW_LEN - 1] + "…"


app = FastAPI()


@app.on_event("startup")
async def startup() -> None:
    db = get_db()

    # Practical indexes for common queries (still one collection)
    await db[TICKETS_COLL].create_index("status")
    await db[TICKETS_COLL].create_index("updated_at")


@app.on_event("shutdown")
async def shutdown() -> None:
    shutdown_db()


# ---- Pydantic models ----


class TicketIn(BaseModel):
    customer_id: str
    subject: str
    message: str


class TicketPatch(BaseModel):
    status: Status | None = None
    agent_note: str | None = None


class TicketDetails(BaseModel):
    id: str
    customer_id: str
    subject: str
    message: str
    status: Status
    agent_note: str | None = None
    created_at: datetime
    updated_at: datetime


class TicketListItem(BaseModel):
    id: str
    subject: str
    status: Status
    updated_at: datetime
    preview: str
    has_note: bool


# ---- Endpoints (no CQRS yet) ----


@app.post("/tickets", response_model=TicketDetails)
async def create_ticket(payload: TicketIn) -> TicketDetails:
    db = get_db()
    now = utcnow()

    doc: dict[str, Any] = {
        "customer_id": payload.customer_id,
        "subject": payload.subject,
        "message": payload.message,
        "status": "open",
        "agent_note": None,
        "created_at": now,
        "updated_at": now,
    }

    res = await db[TICKETS_COLL].insert_one(doc)
    return TicketDetails(id=oid_str(res.inserted_id), **doc)


@app.patch("/tickets/{ticket_id}", response_model=TicketDetails)
async def update_ticket(ticket_id: str, patch: TicketPatch) -> TicketDetails:
    db = get_db()

    existing = await db[TICKETS_COLL].find_one({"_id": ticket_id})
    if existing is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Business rule mixed with patching and persistence
    if patch.status is not None:
        if existing["status"] == "closed" and patch.status != "closed":
            raise HTTPException(
                status_code=400, detail="Closed tickets cannot be reopened"
            )

    update: dict[str, Any] = {"updated_at": utcnow()}
    if patch.status is not None:
        update["status"] = patch.status
    if patch.agent_note is not None:
        update["agent_note"] = patch.agent_note

    await db[TICKETS_COLL].update_one({"_id": _id}, {"$set": update})

    updated = {**existing, **update}
    return TicketDetails(
        id=ticket_id,
        customer_id=updated["customer_id"],
        subject=updated["subject"],
        message=updated["message"],
        status=updated["status"],
        agent_note=updated.get("agent_note"),
        created_at=updated["created_at"],
        updated_at=updated["updated_at"],
    )


@app.get("/tickets", response_model=list[TicketListItem])
async def list_tickets(
    status: Status | None = None, limit: int = 20, skip: int = 0
) -> list[TicketListItem]:
    """
    Pain point in the BEFORE version:
    - The list view wants preview + has_note (read concerns).
    - We compute them on every request.
    - If this gets more complex (scores, denormalized fields, analytics),
      this endpoint becomes a hotspot.
    """
    db = get_db()

    query: dict[str, Any] = {}
    if status is not None:
        query["status"] = status

    # We still need message + agent_note to compute preview/has_note.
    cursor = (
        db[TICKETS_COLL]
        .find(
            query,
            projection={
                "subject": 1,
                "status": 1,
                "updated_at": 1,
                "message": 1,
                "agent_note": 1,
            },
        )
        .sort("updated_at", -1)
        .skip(skip)
        .limit(limit)
    )

    out: list[TicketListItem] = []
    async for doc in cursor:
        note = (doc.get("agent_note") or "").strip()
        out.append(
            TicketListItem(
                id=oid_str(doc["_id"]),
                subject=doc["subject"],
                status=doc["status"],
                updated_at=doc["updated_at"],
                preview=make_preview(doc.get("message", "")),
                has_note=bool(note),
            )
        )
    return out


@app.get("/tickets/{ticket_id}", response_model=TicketDetails)
async def get_ticket(ticket_id: str) -> TicketDetails:
    db = get_db()

    doc = await db[TICKETS_COLL].find_one({"_id": ticket_id})
    if doc is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return TicketDetails(
        id=ticket_id,
        customer_id=doc["customer_id"],
        subject=doc["subject"],
        message=doc["message"],
        status=doc["status"],
        agent_note=doc.get("agent_note"),
        created_at=doc["created_at"],
        updated_at=doc["updated_at"],
    )


@app.get("/dashboard")
async def dashboard() -> dict[str, int]:
    db = get_db()
    pipeline = [{"$group": {"_id": "$status", "count": {"$sum": 1}}}]

    counts: dict[str, int] = {"open": 0, "triaged": 0, "closed": 0}
    async for row in db[TICKETS_COLL].aggregate(pipeline):
        counts[str(row["_id"])] = int(row["count"])
    return counts
