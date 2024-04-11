import asyncio
import time

import aiohttp


async def fetch(session: aiohttp.ClientSession, url: str) -> float:
    start_time = time.time()
    async with session.get(url) as response:
        await response.text()
        return time.time() - start_time


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        urls = ["http://127.0.0.1:3000" for _ in range(2)]
        tasks = [fetch(session, url) for url in urls]
        response_times = await asyncio.gather(*tasks)
        for i, response_time in enumerate(response_times, start=1):
            print(f"Request {i}: {response_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
