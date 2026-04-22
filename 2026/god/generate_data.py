from pathlib import Path

import numpy as np
import pandas as pd


def generate_synthetic_churn_data(
    n_samples: int = 1500,
    random_state: int = 42,
) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    age = rng.integers(18, 80, size=n_samples)
    tenure = rng.integers(0, 72, size=n_samples).astype(float)
    monthly_charges = rng.normal(70, 25, size=n_samples).clip(10, 200).astype(float)
    support_tickets = rng.poisson(2.5, size=n_samples)

    contract_type = rng.choice(
        ["monthly", "yearly", "two_year"],
        size=n_samples,
        p=[0.55, 0.30, 0.15],
    )
    internet_service = rng.choice(
        ["fiber", "dsl", "none"],
        size=n_samples,
        p=[0.50, 0.35, 0.15],
    )
    payment_method = rng.choice(
        ["credit_card", "bank_transfer", "paypal"],
        size=n_samples,
        p=[0.45, 0.35, 0.20],
    )

    # Create a somewhat realistic churn signal
    logit = (
        -1.8
        + 0.015 * (monthly_charges - 70)
        + 0.35 * support_tickets
        - 0.03 * tenure
        + 0.9 * (contract_type == "monthly")
        + 0.35 * (internet_service == "fiber")
        - 0.25 * (payment_method == "bank_transfer")
    )

    churn_probability = 1 / (1 + np.exp(-logit))
    churn = rng.binomial(1, churn_probability)

    df = pd.DataFrame(
        {
            "customer_id": [f"CUST-{i:05d}" for i in range(n_samples)],
            "age": age,
            "tenure": tenure,
            "monthly_charges": monthly_charges,
            "support_tickets": support_tickets,
            "contract_type": contract_type,
            "internet_service": internet_service,
            "payment_method": payment_method,
            "churn": churn,
        }
    )

    # Add some missing values to simulate real data
    missing_tenure_idx = rng.choice(n_samples, size=80, replace=False)
    missing_charges_idx = rng.choice(n_samples, size=50, replace=False)

    df.loc[missing_tenure_idx, "tenure"] = np.nan
    df.loc[missing_charges_idx, "monthly_charges"] = np.nan

    return df


def save_dataset(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


if __name__ == "__main__":
    output_path = Path("data/churn.csv")
    df = generate_synthetic_churn_data(n_samples=1500, random_state=42)
    save_dataset(df, output_path)

    print(f"Saved dataset to {output_path.resolve()}")
    print()
    print(df.head())
