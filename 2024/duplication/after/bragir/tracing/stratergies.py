from importlib import resources
import json
import logging.config
from abc import ABC, abstractmethod


class LoggerStrategy(ABC):
    @abstractmethod
    def setup_logging(self):
        pass


class InfoLoggerStrategy(LoggerStrategy):
    def setup_logging(self):
        with resources.open_text("bragir.logging_configs", "info.json") as f:
            logging_config = json.load(f)
        logging.config.dictConfig(config=logging_config)


class DebugLoggerStrategy(LoggerStrategy):
    def setup_logging(self):
        with resources.open_text("bragir.logging_configs", "debug.json") as f:
            logging_config = json.load(f)
        logging.config.dictConfig(config=logging_config)
