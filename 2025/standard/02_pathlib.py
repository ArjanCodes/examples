from pathlib import Path

base = Path("my_project")
config = base / "config" / "settings.toml"

print("Config path:", config)

if config.exists():
    print("File size:", config.stat().st_size)
else:
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text("[settings]\nname = 'Example'")