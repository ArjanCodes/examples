import numpy as np
import pandas as pd
from data_processing import encode_categorical, fill_missing_values, normalize_columns


def main() -> None:
    df = pd.DataFrame(
        {
            "age": [25, 30, np.nan, 22],
            "income": [50000, 60000, 55000, np.nan],
            "gender": ["male", "female", "female", "male"],
        }
    )

    df = fill_missing_values(df)
    df = normalize_columns(df, ["age", "income"])
    df = encode_categorical(df, ["gender"])

    print(df)


if __name__ == "__main__":
    main()
