import aiohttp

# A few handy JSON types
JSON = int | str | float | bool | None | dict[str, "JSON"] | list["JSON"]
JSONObject = dict[str, JSON]
JSONList = list[JSON]


async def http_get(url: str) -> JSONObject:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
