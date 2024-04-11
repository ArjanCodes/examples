import asyncio
import json
import logging
from typing import Any, Awaitable, Callable, Iterable, Optional

import aiosqlite

logging.basicConfig(level=logging.INFO)


class Router:
    def __init__(self):
        self.routes: dict[str, Callable[..., Awaitable[Any]]] = {}

    def route(
        self, path: str, method: str = "GET"
    ) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
        def decorator(
            func: Callable[..., Awaitable[Any]],
        ) -> Callable[..., Awaitable[Any]]:
            self.routes[f"{method} {path}"] = func
            return func

        return decorator

    async def handle(
        self, method: str, path: str, data: Optional[dict[str, Any]] = None
    ) -> str:
        logging.info(f"Handling {method} {path} {data}")
        handler = self.routes.get(f"{method} {path}")
        if handler:
            if data is not None:
                data = await handler(data)
            else:
                data = await handler()
            response_body = json.dumps(data)
            response_header = "HTTP/1.1 200 OK\nContent-Type: application/json\n\n"
            return response_header + response_body
        else:
            return (
                "HTTP/1.1 404 Not Found\nContent-Type: application/json\n\n"
                + json.dumps({"error": "Not Found"})
            )


class AsyncAPIServer:
    def __init__(
        self, host: str = "127.0.0.1", port: int = 5000, router: Optional[Router] = None
    ):
        self.host = host
        self.port = port
        self.router = router if router is not None else Router()

    async def start(self) -> None:
        server = await asyncio.start_server(
            self.accept_connections, self.host, self.port
        )
        addr = server.sockets[0].getsockname()
        logging.info(f"Serving on http://{addr[0]}:{addr[1]}")

        async with server:
            await server.serve_forever()

    async def accept_connections(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        addr = writer.get_extra_info("peername")
        logging.info(f"Connected by {addr}")
        request_handler = AsyncAPIRequestHandler(reader, writer, self.router)
        await request_handler.process_request()

    def route(
        self, path: str, method: str = "GET"
    ) -> Callable[..., Callable[..., Awaitable[Any]]]:
        return self.router.route(path, method)


class AsyncAPIRequestHandler:
    def __init__(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, router: Router
    ):
        self.reader = reader
        self.writer = writer
        self.router = router

    async def process_request(self) -> None:
        request_line = await self.reader.readline()
        request_line = request_line.decode("utf-8").strip()
        logging.info(f"Request: {request_line}")
        method, path, _ = request_line.split(" ")

        if method in ["POST", "PUT", "DELETE"]:
            content_length = await self.read_headers()
            if content_length:
                body = await self.reader.readexactly(content_length)
                data = json.loads(body.decode("utf-8"))
                response = await self.router.handle(method, path, data=data)
            else:
                response = (
                    "HTTP/1.1 400 Bad Request\nContent-Type: application/json\n\n"
                    + json.dumps({"error": "Bad Request"})
                )
        else:
            response = await self.router.handle(method, path)

        self.writer.write(response.encode())
        await self.writer.drain()
        self.writer.close()

    async def read_headers(self) -> Optional[int]:
        content_length = None
        while True:
            line = await self.reader.readline()
            if line == b"\r\n":  # End of headers
                break
            header = line.decode("utf-8").strip()
            if header.lower().startswith("content-length"):
                content_length = int(header.split(":")[1].strip())
        return content_length


api = AsyncAPIServer()


@api.route("/books")
async def get_books() -> dict[str, Iterable[aiosqlite.Row]]:
    async with aiosqlite.connect("book.db") as conn:
        async with conn.execute("SELECT * FROM books") as cursor:
            books = await cursor.fetchall()
    return {"books": books}


@api.route("/movies")
async def get_movies() -> dict[str, Iterable[aiosqlite.Row]]:
    async with aiosqlite.connect("movie.db") as conn:
        async with conn.execute("SELECT * FROM movies") as cursor:
            movies = await cursor.fetchall()
    return {"movies": movies}


@api.route("/books", "POST")
async def add_book(data: dict[str, Any]) -> dict[str, str]:
    async with aiosqlite.connect("book.db") as conn:
        await conn.execute(
            "INSERT INTO books (title, author) VALUES (?, ?)",
            (data["title"], data["author"]),
        )
        await conn.commit()
    return {"message": "Book added"}


@api.route("/movies", "POST")
async def add_movie(data: dict[str, Any]) -> dict[str, str]:
    async with aiosqlite.connect("movie.db") as conn:
        await conn.execute(
            "INSERT INTO movies (title, director) VALUES (?, ?)",
            (data["title"], data["director"]),
        )
        await conn.commit()
    return {"message": "Movie added"}


@api.route("/books", "DELETE")
async def delete_book(data: dict[str, Any]) -> dict[str, str]:
    async with aiosqlite.connect("book.db") as conn:
        await conn.execute("DELETE FROM books WHERE title = ?", (data["title"],))
        await conn.commit()
    return {"message": "Book deleted"}


@api.route("/movies", "DELETE")
async def delete_movie(data: dict[str, Any]) -> dict[str, str]:
    async with aiosqlite.connect("movie.db") as conn:
        await conn.execute("DELETE FROM movies WHERE title = ?", (data["title"],))
        await conn.commit()
    return {"message": "Movie deleted"}


async def create_table(statement: str, db_path: str) -> None:
    async with aiosqlite.connect(db_path) as db:
        await db.execute(statement)
        await db.commit()


async def main() -> None:
    async with asyncio.TaskGroup() as tasks:
        tasks.create_task(
            create_table(
                "CREATE TABLE IF NOT EXISTS books (title TEXT, author TEXT)", "book.db"
            )
        )
        tasks.create_task(
            create_table(
                "CREATE TABLE IF NOT EXISTS movies (title TEXT, director TEXT)",
                "movie.db",
            )
        )
    await api.start()


if __name__ == "__main__":
    asyncio.run(main())
