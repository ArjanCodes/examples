import asyncio
import json
import logging

import aiohttp

logging.basicConfig(level=logging.INFO)


async def fetch_books(session: aiohttp.ClientSession) -> str:
    async with session.get("http://127.0.0.1:5000/books") as response:
        return await response.text()


async def add_book(session: aiohttp.ClientSession, title: str, author: str) -> str:
    async with session.post(
        "http://127.0.0.1:5000/books",
        data=json.dumps({"title": title, "author": author}),
    ) as response:
        return await response.text()


async def delete_book(session: aiohttp.ClientSession, title: str) -> str:
    async with session.delete(
        f"http://127.0.0.1:5000/books", data=json.dumps({"title": title})
    ) as response:
        return await response.text()


async def add_movie(session: aiohttp.ClientSession, title: str, director: str) -> str:
    async with session.post(
        "http://127.0.0.1:5000/movies",
        data=json.dumps({"title": title, "director": director}),
    ) as response:
        return await response.text()


async def delete_movie(session: aiohttp.ClientSession, title: str) -> str:
    async with session.delete(
        f"http://127.0.0.1:5000/movies", data=json.dumps({"title": title})
    ) as response:
        return await response.text()


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        batch = [
            fetch_books(session),
            add_book(session, "The Catcher in the Rye", "J.D. Salinger"),
            add_book(session, "1984", "George Orwell"),
            add_movie(session, "The Godfather", "Francis Ford Coppola"),
            delete_book(session, "1984"),
            delete_movie(session, "The Godfather"),
        ]
        results = await asyncio.gather(*batch)
        for result in results:
            logging.info(result)


if __name__ == "__main__":
    asyncio.run(main())
