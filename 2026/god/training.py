import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def split_data(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float,
    random_state: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    random_state: int,
) -> RandomForestClassifier:
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=6,
        random_state=random_state,
    )
    model.fit(X_train, y_train)
    return model
