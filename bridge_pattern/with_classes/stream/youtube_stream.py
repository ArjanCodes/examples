import logging
from dataclasses import dataclass

from stream.data import generate_id
from stream.device import StreamingDevice


@dataclass
class YouTubeStreamingService:

    device: StreamingDevice

    def start_stream(self) -> str:
        stream_reference = generate_id()
        logging.info(f"Starting YouTube stream with reference {stream_reference}.")
        return stream_reference

    def fill_buffer(self, stream_reference: str) -> None:
        buffer_data = self.device.get_buffer_data()
        logging.info(
            f"Received buffer data: {buffer_data}. Sending to YouTube stream: {stream_reference}."
        )

    def stop_stream(self, stream_reference: str) -> None:
        logging.info(f"Closing YouTube stream with reference {stream_reference}.")
