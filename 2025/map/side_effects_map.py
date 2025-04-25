def write_warnings(log_entries: list[dict[str, str]]) -> None:
    def process(entry: dict[str, str]) -> None:
        timestamped = f"[{entry['timestamp']}] {entry['message']}"
        with open("warnings.txt", "a") as f:
            f.write(timestamped + "\n")
        if "WARNING" in entry["message"]:
            print("WARNING:", timestamped)

    list(map(process, log_entries))


def main() -> None:
    log_entries: list[dict[str, str]] = [
        {"timestamp": "2025-04-01 12:00", "message": "INFO: System started"},
        {"timestamp": "2025-04-01 12:05", "message": "WARNING: Low disk space"},
        {"timestamp": "2025-04-01 12:10", "message": "ERROR: Disk failure"},
    ]
    write_warnings(log_entries)


if __name__ == "__main__":
    main()
