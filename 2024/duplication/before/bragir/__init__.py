import os
from pathlib import Path

from bragir.config import CONFIG_FILE_PATH, create_config_file, read_config
from bragir.tracing.logger import logger

path = Path(CONFIG_FILE_PATH).expanduser()

if not os.path.isfile(path):
    logger.info(f"Config file not found at: {CONFIG_FILE_PATH}")
    logger.info(f"Creating config file at: {CONFIG_FILE_PATH}")
    create_config_file(path)
    logger.info(f"Created config file at: {CONFIG_FILE_PATH}")


config = read_config(path)
