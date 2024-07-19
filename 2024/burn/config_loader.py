import json
import os
from typing import Any

DEFAULT_CONFIG = {"load_data": True, "data_path": "data/", "data_type": "json"}


def load_config(config_file_path: str) -> dict[str, Any]:
    if not os.path.isfile(config_file_path):
        return DEFAULT_CONFIG
    with open(config_file_path, "r") as f:
        config_data = f.read()
        return json.loads(config_data)
