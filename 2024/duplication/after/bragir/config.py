from configparser import ConfigParser
from enum import StrEnum, auto
import os
from pathlib import Path

import click
from pydantic import BaseModel, SecretStr, ValidationError

from bragir.tracing.logger import logger

HOMEBREW_PREFIX = "/opt/homebrew"

# Set the configuration directory and file path
CONFIG_DIR = Path(HOMEBREW_PREFIX) / "etc" / "bragir"
CONFIG_FILE_PATH = CONFIG_DIR / "config.ini"

BASE_CONFIG = """# DONT CHANGE STRUCTURE OF THIS FILE
[audio]
min_silence_len=1000
silence_thresh=-40
keep_silence=True

[logging]
level=info

[client]
openai_api_key=YOUR_API_KEY
"""


class LoggingLevel(StrEnum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class AudioConfig(BaseModel):
    min_silence_len: int
    silence_thresh: int
    keep_silence: bool


class LoggingConfig(BaseModel):
    level: LoggingLevel


class ClientConfig(BaseModel):
    openai_api_key: SecretStr


class Config(BaseModel):
    audio: AudioConfig
    logging: LoggingConfig
    client: ClientConfig


def create_config_file(target_path: Path):
    # Ensure the directory exists
    os.makedirs(CONFIG_DIR, exist_ok=True)

    logger.info(f"Creating config file at: {target_path}")
    with open(target_path, "w") as file:
        file.write(BASE_CONFIG)


def read_config(
    file_path: Path = CONFIG_FILE_PATH,
) -> Config:
    logger.info(f"Reading config from {file_path}")
    config_parser = ConfigParser()
    config_parser.read(file_path)

    values = {
        "audio": {
            "min_silence_len": config_parser.getint("audio", "min_silence_len"),
            "silence_thresh": config_parser.getint("audio", "silence_thresh"),
            "keep_silence": config_parser.getboolean("audio", "keep_silence"),
        },
        "logging": {"level": config_parser.get("logging", "level")},
        "client": {"openai_api_key": config_parser.get("client", "openai_api_key")},
    }

    audio_config = AudioConfig(**values["audio"])  # type: ignore
    logging_config = LoggingConfig(**values["logging"])  # type: ignore
    client_config = ClientConfig(**values["client"])  # type: ignore

    return Config(audio=audio_config, logging=logging_config, client=client_config)


try:
    config = read_config(Path(CONFIG_FILE_PATH))
except ValidationError as e:
    click.secho(f"Configuration validation error: {e}", fg="red")
