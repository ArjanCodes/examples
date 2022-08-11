from dataclasses import dataclass
from pathlib import Path

import pydantic
import yaml


class PySettings(pydantic.BaseModel):
    path: Path
    other: str


@dataclass
class Settings:
    path: Path
    other: str


def main() -> None:
    path = Path().cwd() / "settings.yaml"
    parsed_yaml = yaml.safe_load(path.read_text())
    # settings = Settings(**parsed_yaml) # won't work
    settings = PySettings(**parsed_yaml)
    print(settings)
    print(settings.path.parent)


if __name__ == "__main__":
    main()
