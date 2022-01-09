from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from stream.data import Buffer, BufferData


@dataclass
class StreamingService(ABC):

    devices: list[Buffer] = field(default_factory=list)

    def add_device(self, device: Buffer) -> None:
        self.devices.append(device)

    def retrieve_buffer_data(self) -> list[BufferData]:
        return [device() for device in self.devices]

    @abstractmethod
    def start_stream(self) -> str:
        pass

    @abstractmethod
    def fill_buffer(self, stream_reference: str) -> None:
        pass

    @abstractmethod
    def stop_stream(self, stream_reference: str) -> None:
        pass
