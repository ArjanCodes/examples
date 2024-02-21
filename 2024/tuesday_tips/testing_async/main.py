import aiohttp
import asyncio

from fetch_event import fetch_event


# Example usage
async def main() -> None:
    event_id = "1"
    async with aiohttp.ClientSession() as session:
        event_info = await fetch_event(session=session, event_id=event_id)

        print(f"Title: {event_info['title']}")
        print(f"Description: {event_info['description']}")
        print(f"Location: {event_info['location']}")


if __name__ == "__main__":
    asyncio.run(main())

