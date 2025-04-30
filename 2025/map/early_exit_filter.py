def scan_for_suspicious(events: list[dict[str, str]]) -> None:
    event = next(filter(is_suspicious, events), None)
    if event:
        print(f"Suspicious login detected: {event}")


def is_suspicious(event: dict[str, str]) -> bool:
    return (
        "login" in event.get("type", "").lower()
        and "unusual" in event.get("details", "").lower()
    )


def main() -> None:
    events: list[dict[str, str]] = [
        {"type": "login", "details": "User logged in"},
        {"type": "login", "details": "Unusual login from new device"},
        {"type": "logout", "details": "User logged out"},
    ]
    scan_for_suspicious(events)


if __name__ == "__main__":
    main()
