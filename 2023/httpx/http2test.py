import httpx
import asyncio
import time

BASE_URL = (
    "https://httpbin.org/delay/1"  # This endpoint delays the response by 1 second
)


async def fetch(http2: bool = False):
    async with httpx.AsyncClient(http2=http2) as client:
        return await client.get(BASE_URL)


async def fetch_multiple(count: int, http2: bool = False):
    return await asyncio.gather(*[fetch(http2=http2) for _ in range(count)])


def measure_time(count: int, http2: bool = False):
    start_time = time.perf_counter()
    asyncio.run(fetch_multiple(count, http2=http2))
    return time.perf_counter() - start_time


def main() -> None:
    num_requests = 10

    duration_http1 = measure_time(num_requests, http2=False)
    duration_http2 = measure_time(num_requests, http2=True)

    print(f"Time taken with HTTP/1.1: {duration_http1:.2f} seconds")
    print(f"Time taken with HTTP/2: {duration_http2:.2f} seconds")


if __name__ == "__main__":
    main()
