from typing import Protocol


class StreamingService(Protocol):
    def start_stream(self) -> str:
        ...

    def fill_buffer(self, stream_reference: str) -> None:
        ...

    def stop_stream(self, stream_reference: str) -> None:
        ...
