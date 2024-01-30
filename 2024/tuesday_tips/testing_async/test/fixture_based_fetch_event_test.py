# Create a fixture that returns an event loop.
import asyncio
from unittest.mock import patch
from aiohttp import ClientSession
import pytest

from fetch_event import fetch_event

@pytest.fixture
async def session():
    with patch("aiohttp.ClientSession") as mock:
        yield mock

@pytest.fixture
def event_loop():
    asyncio.get_event_loop_policy().set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

def test_fetch_event(session: ClientSession, event_loop: asyncio.AbstractEventLoop):
    results = event_loop.run_until_complete(fetch_event(session=session, event_id="1"))
    assert len(results) > 0
    

def test_fetch_multiple_events_with_custom_event_loop(
    session: ClientSession, event_loop: asyncio.AbstractEventLoop
):
    tasks = [fetch_event(session=session, event_id=str(i)) for i in range(1, 5)]
    results = event_loop.run_until_complete(asyncio.gather(*tasks))
    assert len(results) == 4

