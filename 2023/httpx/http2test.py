import httpx
import asyncio
import time

base_url = (
    "https://httpbin.org/delay/1"  # This endpoint delays the response by 1 second
)


async def fetch(http2=False):
    async with httpx.AsyncClient(http2=http2) as client:
        return await client.get(base_url)


async def fetch_multiple(count, http2=False):
    return await asyncio.gather(*[fetch(http2=http2) for _ in range(count)])


def measure_time(count, http2=False):
    start_time = time.time()
    asyncio.run(fetch_multiple(count, http2=http2))
    return time.time() - start_time


if __name__ == "__main__":
    num_requests = 10

    duration_http1 = measure_time(num_requests, http2=False)
    duration_http2 = measure_time(num_requests, http2=True)

    print(f"Time taken with HTTP/1.1: {duration_http1:.2f} seconds")
    print(f"Time taken with HTTP/2: {duration_http2:.2f} seconds")
