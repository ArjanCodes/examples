import json
import random
from time import sleep

from aiohttp import ClientSession


async def read_data(
    path: str = "./data/fictional_events.json",
) -> dict[str, dict[str, str]]:
    sleep(random.choice([0.125, 0.5, 0.75, 0.1]))
    with open(path) as file:
        data = json.load(file)
    return data


async def fetch_event(event_id: str, session: ClientSession = None) -> dict[str, str]:
    json_data = await read_data()

    try:
        event = json_data[event_id]
        return event
    except KeyError:
        return {"error": "Event not found."}
