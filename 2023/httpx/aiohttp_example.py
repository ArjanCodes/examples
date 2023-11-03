import aiohttp
import asyncio
import time

BASE_URL = "https://httpbin.org"


async def fetch_get(session: aiohttp.ClientSession) -> dict:
    async with session.get(f"{BASE_URL}/get") as response:
        return await response.json()


async def fetch_post(session: aiohttp.ClientSession) -> dict:
    data_to_post = {"key": "value"}
    async with session.post(f"{BASE_URL}/post", json=data_to_post) as response:
        return await response.json()


async def fetch_put(session: aiohttp.ClientSession) -> dict:
    data_to_put = {"key": "updated_value"}
    async with session.put(f"{BASE_URL}/put", json=data_to_put) as response:
        return await response.json()


async def fetch_delete(session: aiohttp.ClientSession) -> dict:
    async with session.delete(f"{BASE_URL}/delete") as response:
        return await response.json()


async def main() -> None:
    # record the starting time
    start = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        # GET
        print("GET:", await fetch_get(session))

        # POST
        print("POST:", await fetch_post(session))

        # PUT
        print("PUT:", await fetch_put(session))

        # DELETE
        print("DELETE:", await fetch_delete(session))

    # record the ending time
    end = time.perf_counter()
    print(f"Time taken: {end - start:.2f} seconds.")


if __name__ == "__main__":
    asyncio.run(main())
