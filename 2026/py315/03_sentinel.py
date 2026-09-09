"""PEP 661: make an explicit 'argument was not provided' value."""

import pickle


MISSING = sentinel("MISSING")


def display_name(name: str | MISSING = MISSING) -> str:
    if name is MISSING:
        return "Anonymous developer"
    return name


def main() -> None:
    print(display_name())
    print(display_name("Arjan"))
    print(f"readable repr: {MISSING!r}")
    print(f"pickle keeps identity? {pickle.loads(pickle.dumps(MISSING)) is MISSING}")


if __name__ == "__main__":
    main()
