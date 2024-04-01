import asyncio
import aiofiles
import logging

logging.basicConfig(level=logging.INFO)
class AsyncServer:
    def __init__(self, host: str = '127.0.0.1', port: int = 5000):
        self.host = host
        self.port = port

    async def start(self) -> None:
        server = await asyncio.start_server(self.accept_connections, self.host, self.port)
        addr = server.sockets[0].getsockname()
        logging.info(f"Server started at http://{addr[0]}:{addr[1]}")

        async with server:
            await server.serve_forever()

    async def accept_connections(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        addr = writer.get_extra_info('peername')
        logging.info(f"Connected by {addr}")
        request_handler = AsyncRequestHandler(reader, writer)
        await request_handler.process_request()

class AsyncRequestHandler:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer

    async def process_request(self) -> None:
        request = await self.reader.read(1024)
        request = request.decode('utf-8')
        logging.info(f"Request: {request}")
        await self.handle_request(request)

    async def handle_request(self, request: str) -> None:
        path = self.get_path(request)
        response = await self.generate_response(path)
        self.writer.write(response.encode())
        await self.writer.drain()
        self.writer.close()

    def get_path(self, request: str) -> str:
        try:
            path = request.split(' ')[1]
            if path == '/':
                return 'index.html'
            return path
        except IndexError:
            return 'index.html'

    async def generate_response(self, path: str) -> str:
        await asyncio.sleep(2)
        try:
            async with aiofiles.open(path, mode = 'r') as f:
                response_body = await f.read()
            response_header = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
        except FileNotFoundError:
            response_body = "<html><body><h1>404 Not Found</h1></body></html>"
            response_header = "HTTP/1.1 404 Not Found\n\n"
        return response_header + response_body


async def main() -> None:
    server = AsyncServer()
    await server.start()

if __name__ == "__main__":
    asyncio.run(main())
