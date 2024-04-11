import logging
import socket
import time


class Server:
    def __init__(self, host: str = "127.0.0.1", port: int = 3000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self) -> None:
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            logging.info(f"Server started at http://{self.host}:{self.port}")
            self.accept_connections()
        finally:
            self.server_socket.close()

    def accept_connections(self) -> None:
        while True:
            conn, addr = self.server_socket.accept()
            with conn:
                logging.info(f"Connected by {addr}")
                request_handler = RequestHandler(conn)
                request_handler.process_request()


class RequestHandler:
    def __init__(self, conn: socket.socket):
        self.conn = conn

    def process_request(self):
        request = self.conn.recv(1024).decode("utf-8")
        logging.info(f"Request: {request}")
        self.handle_request(request)

    def handle_request(self, request: str):
        path = self.get_path(request)
        response = self.generate_response(path)
        self.conn.sendall(response.encode())

    def get_path(self, request: str):
        try:
            path = request.split(" ")[1]
            if path == "/":
                return "index.html"
            return path
        except IndexError:
            return "index.html"

    def generate_response(self, path: str):
        time.sleep(2)
        try:
            with open(path, "r") as file:
                response_body = file.read()
            response_header = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
        except FileNotFoundError:
            response_body = "<html><body><h1>404 Not Found</h1></body></html>"
            response_header = "HTTP/1.1 404 Not Found\n\n"
        return response_header + response_body


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    server = Server()
    server.start()


if __name__ == "__main__":
    main()
