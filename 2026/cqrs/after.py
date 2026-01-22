from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from db import Database, get_db, oid_str, parse_object_id, shutdown_db
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ----------------------------
# Types / helpers
# ----------------------------

Status = Literal["open", "triaged", "closed"]

PREVIEW_LEN = 80


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def make_preview(message: str) -> str:
    msg = message.strip().replace("\n", " ")
    return msg if len(msg) <= PREVIEW_LEN else msg[: PREVIEW_LEN - 1] + "…"


# ----------------------------
# MongoDB configuration (local + auth)
# ----------------------------


COMMANDS_COLL = "ticket_commands"  # source of truth
READS_COLL = "ticket_reads"  # read projection for list/dashboard

# ----------------------------
# FastAPI app + DB lifecycle
# ----------------------------

app = FastAPI()


@app.on_event("startup")
async def startup() -> None:
    db = get_db()

    # Write-side indexes (source of truth)
    await db[COMMANDS_COLL].create_index("status")
    await db[COMMANDS_COLL].create_index("updated_at")

    # Read-side indexes (optimized for query patterns)
    await db[READS_COLL].create_index("status")
    await db[READS_COLL].create_index("updated_at")
    await db[READS_COLL].create_index("has_note")  # cheap example of a read-only filter


@app.on_event("shutdown")
async def shutdown() -> None:
    await shutdown_db()


# ----------------------------
# Commands (write DTOs)
# ----------------------------


class CreateTicket(BaseModel):
    customer_id: str
    subject: str
    message: str


class UpdateStatus(BaseModel):
    new_status: Status


class AddAgentNote(BaseModel):
    note: str


# ----------------------------
# Queries (read DTOs)
# ----------------------------


class TicketListItem(BaseModel):
    id: str
    subject: str
    status: Status
    updated_at: datetime
    preview: str
    has_note: bool


class TicketDetails(BaseModel):
    id: str
    customer_id: str
    subject: str
    message: str
    status: Status
    agent_note: str | None = None
    created_at: datetime
    updated_at: datetime


# ----------------------------
# Command handlers (write side)
# ----------------------------


async def cmd_create_ticket(db: Database, cmd: CreateTicket) -> str:
    now = utcnow()
    doc: dict[str, Any] = {
        "customer_id": cmd.customer_id,
        "subject": cmd.subject,
        "message": cmd.message,
        "status": "open",
        "agent_note": None,
        "created_at": now,
        "updated_at": now,
    }
    res = await db[COMMANDS_COLL].insert_one(doc)
    return oid_str(res.inserted_id)


async def cmd_update_status(db: Database, ticket_id: str, cmd: UpdateStatus) -> None:
    _id = parse_object_id(ticket_id)

    existing = await db[COMMANDS_COLL].find_one({"_id": _id})
    if existing is None:
        raise ValueError("Ticket not found")

    if existing["status"] == "closed" and cmd.new_status != "closed":
        raise ValueError("Closed tickets cannot be reopened")

    await db[COMMANDS_COLL].update_one(
        {"_id": _id},
        {"$set": {"status": cmd.new_status, "updated_at": utcnow()}},
    )


async def cmd_add_agent_note(db: Database, ticket_id: str, cmd: AddAgentNote) -> None:
    _id = parse_object_id(ticket_id)

    existing = await db[COMMANDS_COLL].find_one({"_id": _id})
    if existing is None:
        raise ValueError("Ticket not found")

    await db[COMMANDS_COLL].update_one(
        {"_id": _id},
        {"$set": {"agent_note": cmd.note, "updated_at": utcnow()}},
    )


# ----------------------------
# Projector (build read model)
# ----------------------------


async def project_ticket(db: Database, ticket_id: str) -> None:
    """
    Read model goal:
    - store exactly what the list/dashboard needs
    - in a shape that is cheap to query
    - derived fields (preview, has_note) are computed once here
    """
    _id = parse_object_id(ticket_id)
    doc = await db[COMMANDS_COLL].find_one({"_id": _id})
    if doc is None:
        return

    note = (doc.get("agent_note") or "").strip()

    read_doc: dict[str, Any] = {
        "_id": doc["_id"],  # same id on read side
        "subject": doc["subject"],
        "status": doc["status"],
        "updated_at": doc["updated_at"],
        "preview": make_preview(doc.get("message", "")),
        "has_note": bool(note),
    }

    await db[READS_COLL].update_one(
        {"_id": doc["_id"]},
        {"$set": read_doc},
        upsert=True,
    )


# ----------------------------
# Command endpoints (write API)
# ----------------------------


@app.post("/tickets")
async def create_ticket(cmd: CreateTicket) -> dict[str, str]:
    db = get_db()
    ticket_id = await cmd_create_ticket(db, cmd)
    await project_ticket(db, ticket_id)  # synchronous for demo
    return {"id": ticket_id}


@app.post("/tickets/{ticket_id}/status")
async def update_status(ticket_id: str, cmd: UpdateStatus) -> dict[str, str]:
    db = get_db()
    try:
        await cmd_update_status(db, ticket_id, cmd)
        await project_ticket(db, ticket_id)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/tickets/{ticket_id}/agent-note")
async def add_agent_note(ticket_id: str, cmd: AddAgentNote) -> dict[str, str]:
    db = get_db()
    try:
        await cmd_add_agent_note(db, ticket_id, cmd)
        await project_ticket(db, ticket_id)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----------------------------
# Query endpoints (read API)
# ----------------------------


@app.get("/tickets", response_model=list[TicketListItem])
async def list_tickets(
    status: Status | None = None,
    has_note: bool | None = None,
    limit: int = 20,
    skip: int = 0,
) -> list[TicketListItem]:
    """
    Now reads are truly read-optimized:
    - no need to pull message/agent_note
    - preview + has_note already exist
    - can index/filter on read-only fields
    """
    db = get_db()

    query: dict[str, Any] = {}
    if status is not None:
        query["status"] = status
    if has_note is not None:
        query["has_note"] = has_note

    cursor = (
        db[READS_COLL]
        .find(
            query,
            projection={
                "subject": 1,
                "status": 1,
                "updated_at": 1,
                "preview": 1,
                "has_note": 1,
            },
        )
        .sort("updated_at", -1)
        .skip(skip)
        .limit(limit)
    )

    out: list[TicketListItem] = []
    async for doc in cursor:
        out.append(
            TicketListItem(
                id=oid_str(doc["_id"]),
                subject=doc["subject"],
                status=doc["status"],
                updated_at=doc["updated_at"],
                preview=doc["preview"],
                has_note=doc["has_note"],
            )
        )
    return out


@app.get("/tickets/{ticket_id}", response_model=TicketDetails)
async def get_ticket(ticket_id: str) -> TicketDetails:
    """
    For details we read from the source of truth.
    (You *could* also build a separate details projection if needed.)
    """
    db = get_db()
    _id = parse_object_id(ticket_id)

    doc = await db[COMMANDS_COLL].find_one({"_id": _id})
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
    """
    Dashboard runs on the read model, not the write model.
    """
    db = get_db()
    pipeline = [{"$group": {"_id": "$status", "count": {"$sum": 1}}}]

    counts: dict[str, int] = {"open": 0, "triaged": 0, "closed": 0}

    cursor = await db[READS_COLL].aggregate(pipeline)
    async for row in cursor:
        counts[str(row["_id"])] = int(row["count"])
    return counts
