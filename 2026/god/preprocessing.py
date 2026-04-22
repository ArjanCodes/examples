import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    cleaned = cleaned.drop_duplicates(subset=["customer_id"])
    cleaned = cleaned.dropna(subset=["churn"])

    cleaned["tenure"] = cleaned["tenure"].fillna(cleaned["tenure"].median())
    cleaned["monthly_charges"] = cleaned["monthly_charges"].fillna(
        cleaned["monthly_charges"].median()
    )

    cleaned["support_tickets"] = cleaned["support_tickets"].clip(lower=0, upper=15)

    return cleaned


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    featured = df.copy()

    featured["charges_per_ticket"] = featured["monthly_charges"] / (
        featured["support_tickets"] + 1
    )
    featured["is_senior"] = (featured["age"] >= 65).astype(int)
    featured["is_new_customer"] = (featured["tenure"] < 6).astype(int)

    return featured


def prepare_features_and_target(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    prepared = pd.get_dummies(
        df,
        columns=["contract_type", "internet_service", "payment_method"],
        drop_first=True,
    )

    X = prepared.drop(columns=["customer_id", "churn"])
    y = prepared["churn"]

    return X, y
