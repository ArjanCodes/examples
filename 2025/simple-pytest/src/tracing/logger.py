import logging
import logging.config

from src.tracing.stratergies import LoggerStrategy


def setup_logging(strategy: LoggerStrategy) -> None:
    strategy.setup_logging()


logger = logging.getLogger("root")
