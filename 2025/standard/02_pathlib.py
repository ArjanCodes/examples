from pathlib import Path


def main() -> None:
    base = Path("my_project")
    config = base / "config" / "settings.toml"

    print("Config path:", config)

    if config.exists():
        print("File size:", config.stat().st_size)
    else:
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text("[settings]\nname = 'Example'")


if __name__ == "__main__":
    main()
