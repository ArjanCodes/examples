import pandas as pd

from src.schema import TransactionsSchema
from src.transformers import preprocessing_pipeline


def load_transaction_data(path: str) -> pd.DataFrame:
    raw_transactions = pd.read_csv(path)
    cleaned_transactions = preprocessing_pipeline(raw_transactions)
    TransactionsSchema.validate(cleaned_transactions, inplace=True)
    return cleaned_transactions
