from pathlib import Path


def find_project_root(marker: str = ".git") -> Path:
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if (parent / marker).exists():
            return parent
    raise FileNotFoundError(f"Project root with marker '{marker}' not found")
