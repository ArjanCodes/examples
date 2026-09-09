"""PEP 810: imports can stay at module scope but load on first use."""

import sys
lazy import json
lazy from pathlib import Path


def main() -> None:
    # Neither module has been executed just because this file started.
    print(f"json loaded at startup? {'json' in sys.modules}")
    print(f"pathlib loaded at startup? {'pathlib' in sys.modules}")

    payload = json.dumps({"feature": "lazy imports"})
    print(f"json loaded after json.dumps()? {'json' in sys.modules}: {payload}")

    print(f"pathlib loaded before use? {'pathlib' in sys.modules}")
    print(f"current folder: {Path.cwd().name}")
    print(f"pathlib loaded after Path.cwd()? {'pathlib' in sys.modules}")


if __name__ == "__main__":
    main()
