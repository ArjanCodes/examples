class Connection:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def connect(self):
        print(f"Connecting to {self.host}:{self.port}")

    def disconnect(self):
        print(f"Disconnecting from {self.host}:{self.port}")

    def send(self, data: str):
        print(f"Sending data to {self.host}:{self.port}")
        print(f"Data: {data}")
