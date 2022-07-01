import numpy as np
import pandera as pa


class RawTransactionsSchema(pa.SchemaModel):
    date: pa.typing.Series[str]
    amount: pa.typing.Series[float]
    category: pa.typing.Series[str]


class TransactionsSchema(pa.SchemaModel):
    date: pa.typing.Series[np.datetime64]
    amount: pa.typing.Series[float]
    category: pa.typing.Series[str]
    year: pa.typing.Series[str]
    month: pa.typing.Series[str]
