from pathlib import Path

import pandas as pd


def load_dataset(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)
