import pandas as pd

import src


def load_transaction_data() -> pd.DataFrame:
    settings = src.config.load_settings()
    raw_transactions = pd.read_csv(settings.data.path)
    transaction_preprocessing_pipeline = src.transformers.create_preprocessing_pipeline()
    cleaned_transactions = transaction_preprocessing_pipeline.fit_transform(raw_transactions)
    src.schema.TransactionsSchema.validate(cleaned_transactions, inplace=True)
    return cleaned_transactions
