import pandas as pd
from src.schema import TransactionsSchema
from src.transformers import create_preprocessing_pipeline


def load_transaction_data(path: str) -> pd.DataFrame:
    raw_transactions = pd.read_csv(path)
    preprocessing_pipeline = create_preprocessing_pipeline()
    cleaned_transactions = preprocessing_pipeline.fit_transform(raw_transactions)
    TransactionsSchema.validate(cleaned_transactions, inplace=True)
    return cleaned_transactions
