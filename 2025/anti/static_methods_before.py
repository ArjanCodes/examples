import numpy as np
import pandas as pd


class DataPreprocessingUtils:
    @staticmethod
    def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
        """Fill missing numeric values with the median of each column."""
        return df.fillna(df.median(numeric_only=True))

    @staticmethod
    def normalize_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """Min-max normalize specified columns in the DataFrame."""
        df = df.copy()
        for col in columns:
            min_val = df[col].min()
            max_val = df[col].max()
            if min_val == max_val:
                df[col] = 0.0  # avoid division by zero
            else:
                df[col] = (df[col] - min_val) / (max_val - min_val)
        return df

    @staticmethod
    def encode_categorical(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """Convert categorical columns into one-hot encoded columns."""
        return pd.get_dummies(df, columns=columns, drop_first=True)


def main() -> None:
    df = pd.DataFrame(
        {
            "age": [25, 30, np.nan, 22],
            "income": [50000, 60000, 55000, np.nan],
            "gender": ["male", "female", "female", "male"],
        }
    )

    df = DataPreprocessingUtils.fill_missing_values(df)
    df = DataPreprocessingUtils.normalize_columns(df, ["age", "income"])
    df = DataPreprocessingUtils.encode_categorical(df, ["gender"])

    print(df)


if __name__ == "__main__":
    main()
