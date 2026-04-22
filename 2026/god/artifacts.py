import json
from pathlib import Path

import joblib
import pandas as pd
from evaluation import EvaluationResult
from sklearn.ensemble import RandomForestClassifier


def save_model(model: RandomForestClassifier, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)


def save_metrics(result: EvaluationResult, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "accuracy": result.accuracy,
        "classification_report": result.classification_report,
    }

    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def compute_feature_importances(
    model: RandomForestClassifier,
    feature_names: list[str],
) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "feature": feature_names,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)


def save_feature_importances(importances: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    importances.to_csv(path, index=False)
