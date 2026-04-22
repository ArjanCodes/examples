from artifacts import (
    compute_feature_importances,
    save_feature_importances,
    save_metrics,
    save_model,
)
from config import TrainingConfig
from data_loading import load_dataset
from evaluation import evaluate_model
from preprocessing import clean_data, engineer_features, prepare_features_and_target
from training import split_data, train_model


def run_pipeline(config: TrainingConfig) -> None:
    print("Running churn experiment...\n")

    df = load_dataset(config.data_path)
    print("Raw sample:")
    print(df.head(), "\n")

    cleaned = clean_data(df)
    featured = engineer_features(cleaned)
    X, y = prepare_features_and_target(featured)

    X_train, X_test, y_train, y_test = split_data(
        X,
        y,
        test_size=config.test_size,
        random_state=config.random_state,
    )

    model = train_model(
        X_train,
        y_train,
        random_state=config.random_state,
    )

    result = evaluate_model(model, X_test, y_test)
    importances = compute_feature_importances(model, X.columns.tolist())

    model_path = config.output_dir / "churn_model.joblib"
    metrics_path = config.output_dir / "metrics.json"
    importances_path = config.output_dir / "feature_importances.csv"

    save_model(model, model_path)
    save_metrics(result, metrics_path)
    save_feature_importances(importances, importances_path)

    print("Evaluation results:")
    for line in result.summary_lines():
        print(line)

    print("\nTop 10 feature importances:")
    print(importances.head(10).to_string(index=False), "\n")

    print(f"Artifacts saved in: {config.output_dir.resolve()}")


def main() -> None:
    config = TrainingConfig(
        data_path="data/churn.csv",
        output_dir="artifacts",
        test_size=0.25,
        random_state=42,
    )
    run_pipeline(config)


if __name__ == "__main__":
    main()
