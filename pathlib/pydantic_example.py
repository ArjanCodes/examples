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
    try:
        parsed_yaml = yaml.safe_load(path.read_text())
        settings = PySettings(**parsed_yaml)
        print(settings)
        print(settings.path.parent)
    except yaml.YAMLError as exc:
        print(exc)


if __name__ == "__main__":
    main()
