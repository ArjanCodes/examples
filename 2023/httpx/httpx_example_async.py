from typing import Any
import time
import asyncio
import httpx

BASE_URL = "https://httpbin.org"


async def fetch_get() -> Any:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/get")
        return response.json()


async def fetch_post():
    data_to_post = {"key": "value"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/post", json=data_to_post)
        return response.json()


async def fetch_put():
    data_to_put = {"key": "updated_value"}
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{BASE_URL}/put", json=data_to_put)
        return response.json()


async def fetch_delete():
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/delete")
        return response.json()


async def main():
    # record the starting time
    start = time.perf_counter()

    tasks = [fetch_get(), fetch_post(), fetch_put(), fetch_delete()]
    results = await asyncio.gather(*tasks)

    for result in results:
        print(result)

    # record the ending time
    end = time.perf_counter()
    print(f"Time taken: {end - start:.2f} seconds.")


# To run the function
if __name__ == "__main__":
    asyncio.run(main())
