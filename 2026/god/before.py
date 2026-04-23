import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


class ChurnExperiment:
    def __init__(
        self,
        data_path: str = "data/churn.csv",
        output_dir: str = "artifacts",
        test_size: float = 0.2,
        random_state: int = 42,
    ) -> None:
        self.data_path = Path(data_path)
        self.output_dir = Path(output_dir)
        self.test_size = test_size
        self.random_state = random_state
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=6,
            random_state=random_state,
        )

    def run(self) -> None:
        print("Running churn experiment...\n")

        if not self.data_path.exists():
            raise FileNotFoundError(f"Dataset not found: {self.data_path}")
        if self.data_path.suffix != ".csv":
            raise ValueError("data_path must point to a CSV file")
        if not self.output_dir.parent.exists():
            raise FileNotFoundError(
                f"Parent directory for output_dir does not exist: {self.output_dir.parent}"
            )
        if not 0 < self.test_size < 1:
            raise ValueError("test_size must be between 0 and 1")
        if self.random_state < 0:
            raise ValueError("random_state must be >= 0")

        self.output_dir.mkdir(parents=True, exist_ok=True)

        df = self._load_data()
        X, y = self._prepare_features(df)
        X_train, X_test, y_train, y_test = self._split_data(X, y)

        self._train_model(X_train, y_train)
        metrics = self._evaluate_model(X_test, y_test)
        self._save_artifacts(metrics, X.columns.tolist())
        self._print_summary(metrics, X.columns.tolist())

    def _load_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.data_path)
        print("Raw sample:")
        print(df.head(), "\n")

        cleaned = df.copy()

        cleaned = cleaned.drop_duplicates(subset=["customer_id"])
        cleaned = cleaned.dropna(subset=["churn"])

        cleaned["tenure"] = cleaned["tenure"].fillna(cleaned["tenure"].median())
        cleaned["monthly_charges"] = cleaned["monthly_charges"].fillna(
            cleaned["monthly_charges"].median()
        )
        cleaned["support_tickets"] = cleaned["support_tickets"].clip(lower=0, upper=15)

        return cleaned

    def _prepare_features(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        prepared = df.copy()

        prepared["charges_per_ticket"] = prepared["monthly_charges"] / (
            prepared["support_tickets"] + 1
        )
        prepared["is_senior"] = (prepared["age"] >= 65).astype(int)
        prepared["is_new_customer"] = (prepared["tenure"] < 6).astype(int)

        prepared = pd.get_dummies(
            prepared,
            columns=["contract_type", "internet_service", "payment_method"],
            drop_first=True,
        )

        X = prepared.drop(columns=["customer_id", "churn"])
        y = prepared["churn"]

        return X, y

    def _split_data(
        self, X: pd.DataFrame, y: pd.Series
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        return train_test_split(
            X,
            y,
            test_size=self.test_size,
            random_state=self.random_state,
            stratify=y,
        )

    def _train_model(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        self.model.fit(X_train, y_train)

    def _evaluate_model(
        self, X_test: pd.DataFrame, y_test: pd.Series
    ) -> dict[str, object]:
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions, output_dict=True)

        return {
            "accuracy": accuracy,
            "classification_report": report,
        }

    def _save_artifacts(
        self, metrics: dict[str, object], feature_names: list[str]
    ) -> None:
        model_path = self.output_dir / "churn_model.joblib"
        metrics_path = self.output_dir / "metrics.json"
        importances_path = self.output_dir / "feature_importances.csv"

        joblib.dump(self.model, model_path)

        with metrics_path.open("w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)

        importances = pd.DataFrame(
            {
                "feature": feature_names,
                "importance": self.model.feature_importances_,
            }
        ).sort_values("importance", ascending=False)

        importances.to_csv(importances_path, index=False)

    def _print_summary(
        self, metrics: dict[str, object], feature_names: list[str]
    ) -> None:
        print("Evaluation results:")
        print(f"Accuracy: {metrics['accuracy']:.3f}\n")

        report = metrics["classification_report"]
        print("Precision / Recall / F1:")
        print(
            f"Class 0 -> precision={report['0']['precision']:.3f}, "
            f"recall={report['0']['recall']:.3f}, "
            f"f1={report['0']['f1-score']:.3f}"
        )
        print(
            f"Class 1 -> precision={report['1']['precision']:.3f}, "
            f"recall={report['1']['recall']:.3f}, "
            f"f1={report['1']['f1-score']:.3f}\n"
        )

        importances = pd.DataFrame(
            {
                "feature": feature_names,
                "importance": self.model.feature_importances_,
            }
        ).sort_values("importance", ascending=False)

        print("Top 10 feature importances:")
        print(importances.head(10).to_string(index=False), "\n")

        print(f"Artifacts saved in: {self.output_dir.resolve()}")


def main() -> None:
    experiment = ChurnExperiment(
        data_path="data/churn.csv",
        output_dir="artifacts",
        test_size=0.25,
        random_state=42,
    )
    experiment.run()


if __name__ == "__main__":
    main()
