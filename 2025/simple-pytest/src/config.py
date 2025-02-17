import os
from configparser import ConfigParser
from enum import StrEnum, auto
from pathlib import Path
from typing import Any

import click
from pydantic import BaseModel

from src.constants.ai import POSSIBLE_MODELS
from src.tracing.logger import logger

CONFIG_NAME = "config.ini"
HOME_USER_PATH = Path.home()
BRAGIR_DIRECTORY = HOME_USER_PATH / ".bragir"
CONFIG_FILE_PATH = BRAGIR_DIRECTORY / CONFIG_NAME


BASE_CONFIG = {
    "audio": {
        "min_silence_len": "1000",
        "silence_thresh": "-40",
        "keep_silence": "True",
    },
    "logging": {
        "level": "info",
    },
    "client": {
        "openai_api_key": "YOUR_API_KEY",
        "model": POSSIBLE_MODELS[0],
    },
}


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
    openai_api_key: str
    model: str


class Config(BaseModel):
    audio: AudioConfig
    logging: LoggingConfig
    client: ClientConfig


def create_config_file(file_path: Path = CONFIG_FILE_PATH) -> None:
    logger.info(f"Creating config file at: {file_path}")

    # Ensure bragir directory exists
    os.makedirs(BRAGIR_DIRECTORY, exist_ok=True)

    config_parser = ConfigParser()
    config_parser.read_dict(BASE_CONFIG)

    with open(file_path, "w") as file:
        config_parser.write(file)


def get_config_parser(file_path: Path) -> ConfigParser:
    config_parser = ConfigParser()
    config_parser.read(file_path)
    return config_parser


def find_section(
    key: str,
    config_parser: ConfigParser = get_config_parser(file_path=CONFIG_FILE_PATH),
) -> str | None:
    sections = config_parser.sections()

    for section in sections:
        if config_parser.has_option(section, key):
            return section

    return None


def reset_config_file(
    config_parser: ConfigParser = ConfigParser(), target_path: Path = CONFIG_FILE_PATH
) -> None:
    logger.info(f"Resetting config file at: {target_path}")
    config_parser.read_dict(BASE_CONFIG)

    with open(target_path, "w") as file:
        config_parser.write(file)


def set_config(config: Config, file_path: Path = CONFIG_FILE_PATH) -> None:
    logger.info(f"Setting config file at {file_path}")
    config_parser = get_config_parser(file_path=file_path)

    for section, values in config.model_dump().items():
        if not config_parser.has_section(section):
            config_parser.add_section(section)

        for key, value in values.items():
            config_parser.set(section, key, str(value))

    with open(file_path, "w") as file:
        config_parser.write(file)


def set_config_value(key: str, value: str, file_path: Path = CONFIG_FILE_PATH) -> None:
    config_parser = get_config_parser(file_path=file_path)
    section = find_section(key, config_parser)

    if section is None:
        logger.error(f"Section for key {key} not found {file_path}")
        exit(1)

    config_parser.set(section, key, value)

    with open(file_path, "w") as file:
        config_parser.write(file)


def get_config(file_path: Path = CONFIG_FILE_PATH) -> Config | None:
    config_parser = get_config_parser(file_path=file_path)

    config_dict = {
        section: dict(config_parser[section]) for section in config_parser.sections()
    }

    if config_dict == {}:
        return None

    return Config.model_validate(config_dict)


def read_config(
    file_path: Path = CONFIG_FILE_PATH,
):
    config = get_config(file_path=file_path)

    if config is None:
        logger.error("Config file not found")
        exit(1)

    for section_name, section_value in config.model_dump().items():
        click.echo(click.style(f"[{section_name}]", fg="cyan", bold=True))

        for key, value in section_value.items():
            if key == "openai_api_key":
                click.echo(
                    f"  {click.style(key, fg='yellow')} = {click.style('*************', fg='green')}"
                )
            else:
                click.echo(
                    f"  {click.style(key, fg='yellow')} = {click.style(str(value), fg='green')}"
                )

        click.echo()


def update_dict(config: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    for key in config.keys():
        if isinstance(config[key], dict):
            config[key] = update_dict(config[key], updates)
        else:
            if key in updates:
                config[key] = updates[key]

    return config
