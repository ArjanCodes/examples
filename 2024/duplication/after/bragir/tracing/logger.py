import logging
import logging.config

from bragir.tracing.stratergies import LoggerStrategy


def setup_logging(strategy: LoggerStrategy) -> None:
    strategy.setup_logging()


logger = logging.getLogger("root")
