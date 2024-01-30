import asyncio
import pytest
from unittest.mock import patch
from aiohttp import ClientSession

from fetch_event import fetch_event


@pytest.fixture
async def session():
    with patch("aiohttp.ClientSession") as mock:
        yield mock


@pytest.mark.asyncio
async def test_fetch_event(session: ClientSession):
    event = await fetch_event(session=session, event_id="1")
    event_2 = await fetch_event(session=session, event_id="20")

    assert event is not None
    assert event_2["error"] == "Event not found."


@pytest.mark.asyncio
async def test_fetch_multiple_events(session: ClientSession):
    event_ids = ["1", "2", "3", "4", "5", "6"]

    tasks = [
        asyncio.create_task(fetch_event(session=session, event_id=event_id))
        for event_id in event_ids
    ]
    results = await asyncio.gather(*tasks)

    assert len(results) == 6
