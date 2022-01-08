import logging
from dataclasses import dataclass

from stream.data import Buffer, generate_id


@dataclass
class YouTubeStreamingService:

    buffer: Buffer

    def start_stream(self) -> str:
        stream_reference = generate_id()
        logging.info(f"Starting YouTube stream with reference {stream_reference}.")
        return stream_reference

    def fill_buffer(self, stream_reference: str) -> None:
        buffer_data = self.buffer()
        logging.info(
            f"Received buffer data: {buffer_data}. Sending to YouTube stream: {stream_reference}."
        )

    def stop_stream(self, stream_reference: str) -> None:
        logging.info(f"Closing YouTube stream with reference {stream_reference}.")
