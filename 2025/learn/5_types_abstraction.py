from typing import Protocol, Callable

class Logger(Protocol):
    def info(self, message: str) -> None: ...
    def error(self, message: str) -> None: ...

def process_order(order_id: int, logger: Logger) -> None:
    logger.info(f"Processing order {order_id}")


ImageExporter = Callable[[bytes], None]

def export_image(data: bytes, exporter: ImageExporter) -> None:
    exporter(data)