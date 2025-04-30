def write_warnings(log_entries: list[dict[str, str]]) -> None:
    with open("warnings.txt", "w") as f:
        for entry in log_entries:
            timestamped = f"[{entry['timestamp']}] {entry['message']}"
            f.write(timestamped + "\n")
            if "WARNING" in entry["message"]:
                print("WARNING:", timestamped)


def main() -> None:
    log_entries: list[dict[str, str]] = [
        {"timestamp": "2025-04-01 12:00", "message": "INFO: System started"},
        {"timestamp": "2025-04-01 12:05", "message": "WARNING: Low disk space"},
        {"timestamp": "2025-04-01 12:10", "message": "ERROR: Disk failure"},
    ]
    write_warnings(log_entries)


if __name__ == "__main__":
    main()
