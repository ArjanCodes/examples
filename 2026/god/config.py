from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TrainingConfig:
    data_path: Path
    output_dir: Path
    test_size: float = 0.25
    random_state: int = 42

    def __post_init__(self) -> None:
        if not self.data_path.exists():
            raise FileNotFoundError(f"Dataset not found: {self.data_path}")
        if self.data_path.suffix != ".csv":
            raise ValueError("data_path must point to a CSV file")
        if not 0 < self.test_size < 1:
            raise ValueError("test_size must be between 0 and 1")
