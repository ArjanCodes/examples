import json
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from event import post_event
from feature import read_config
from gui import WorsePad


def main():
    load_dotenv()
    config = read_config()
    print(config)
    app = WorsePad(post_event, config.show_save_button)
    app.mainloop()


if __name__ == "__main__":
    main()
