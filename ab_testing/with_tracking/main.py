import json
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from event import post_event
from gui import WorsePad


@dataclass
class Config:
    show_save_button: bool = True


def read_config_file() -> Config:
    config_file = Path.cwd() / "config.json"
    config_dict = json.loads(config_file.read_text())
    return Config(**config_dict)


def main():
    load_dotenv()
    config = read_config_file()
    app = WorsePad(post_event, config.show_save_button)
    app.mainloop()


if __name__ == "__main__":
    main()
