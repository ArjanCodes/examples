from dataclasses import dataclass

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


@dataclass(frozen=True)
class EvaluationResult:
    accuracy: float
    classification_report: dict[str, object]

    def summary_lines(self) -> list[str]:
        report = self.classification_report
        return [
            f"Accuracy: {self.accuracy:.3f}",
            (
                f"Class 0 -> precision={report['0']['precision']:.3f}, "
                f"recall={report['0']['recall']:.3f}, "
                f"f1={report['0']['f1-score']:.3f}"
            ),
            (
                f"Class 1 -> precision={report['1']['precision']:.3f}, "
                f"recall={report['1']['recall']:.3f}, "
                f"f1={report['1']['f1-score']:.3f}"
            ),
        ]


def evaluate_model(
    model: RandomForestClassifier,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> EvaluationResult:
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions, output_dict=True)

    return EvaluationResult(
        accuracy=accuracy,
        classification_report=report,
    )
