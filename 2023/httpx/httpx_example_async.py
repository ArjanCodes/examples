import httpx
import asyncio

base_url = "https://httpbin.org"


async def fetch_get():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/get")
        return ("GET:", response.json())


async def fetch_post():
    data_to_post = {"key": "value"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/post", json=data_to_post)
        return ("POST:", response.json())


async def fetch_put():
    data_to_put = {"key": "updated_value"}
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{base_url}/put", json=data_to_put)
        return ("PUT:", response.json())


async def fetch_delete():
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{base_url}/delete")
        return ("DELETE:", response.json())


async def main():
    tasks = [fetch_get(), fetch_post(), fetch_put(), fetch_delete()]
    results = await asyncio.gather(*tasks)

    for result in results:
        print(result[0], result[1])


# To run the function
if __name__ == "__main__":
    asyncio.run(main())
