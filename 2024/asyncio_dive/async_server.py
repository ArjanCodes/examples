import asyncio
import aiofiles

class AsyncServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port

    async def start(self):
        server = await asyncio.start_server(self.accept_connections, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f'Serving on http://{addr[0]}:{addr[1]}')

        async with server:
            await server.serve_forever()

    async def accept_connections(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Connected by {addr}")
        request_handler = AsyncRequestHandler(reader, writer)
        await request_handler.process_request()

class AsyncRequestHandler:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def process_request(self):
        request = await self.reader.read(1024)
        request = request.decode('utf-8')
        print(f"Request: {request}")
        await self.handle_request(request)

    async def handle_request(self, request):
        path = self.get_path(request)
        response = await self.generate_response(path)
        self.writer.write(response.encode())
        await self.writer.drain()
        self.writer.close()

    def get_path(self, request):
        try:
            path = request.split(' ')[1]
            if path == '/':
                return 'index.html'
            return path
        except IndexError:
            return 'index.html'

    async def generate_response(self, path):
        await asyncio.sleep(2)
        try:
            async with aiofiles.open(path, mode = 'r') as f:
                response_body = await f.read()
            response_header = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
        except FileNotFoundError:
            response_body = "<html><body><h1>404 Not Found</h1></body></html>"
            response_header = "HTTP/1.1 404 Not Found\n\n"
        return response_header + response_body

if __name__ == "__main__":
    async def main():
        server = AsyncServer()
        await server.start()

    asyncio.run(main())
