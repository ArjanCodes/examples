import asyncio
import time

import requests


async def counter() -> None:
    now = time.time()
    print("Started counter")
    for i in range(0, 10):
        last = now
        await asyncio.sleep(0.001)
        now = time.time()
        print(f"{i}: Was asleep for {now - last}s")


async def main() -> None:
    task = asyncio.create_task(counter())

    print("Sending HTTP request")
    response = requests.get("https://www.arjancodes.com")
    print(f"Got HTTP response with status {response.status_code}")

    await task


asyncio.run(main())
