import abc
import enum


class Connection:
    def __init__(self):
        self.name = None
        self.ip = None
        self.port = None

    @property
    def status(self):
        return (
            ConnectionStatus.CONNECTED
            if all([self.name, self.ip, self.port])
            else ConnectionStatus.DISCONNECTED
        )

    def connect(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port

    def disconnect(self):
        self.name = None
        self.ip = None
        self.port = None

    def send(self, message):
        print(f"Sent {message} to {self.name} at {self.ip}:{self.port}")

    def receive(self):
        return f"Received message from {self.name} at {self.ip}:{self.port}"


class IOTDevice(abc.ABC):
    @abc.abstractmethod
    def connect(self, name, ip, port):
        pass

    @abc.abstractmethod
    def disconnect(self):
        pass

    @abc.abstractmethod
    def send(self, message):
        pass

    @abc.abstractmethod
    def receive(self):
        pass


class Light(IOTDevice):
    def __init__(self, connection):
        self.connection = connection

    def connect(self, name, ip, port):
        self.connection.connect(name, ip, port)

    def disconnect(self):
        self.connection.disconnect()

    def send(self, message):
        self.connection.send(message)

    def receive(self):
        return self.connection.receive()


class ConnectionStatus(enum.Enum):
    CONNECTED = 1
    DISCONNECTED = 2


if __name__ == "__main__":
    connection = Connection()
    print(connection.status)
    connection.connect("Arjan", "localhost", 8080)
    print(connection.status)
    connection.disconnect()
    print(connection.status)
