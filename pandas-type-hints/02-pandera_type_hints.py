from datetime import datetime
from pathlib import Path

import pandas as pd
import pandera as pa
from pandera.typing import DataFrame, Series


class OutputSchema(pa.SchemaModel):
    InvoiceNo: Series[pd.StringDtype]
    StockCode: Series[pd.StringDtype] = pa.Field(nullable=True)
    Description: Series[pd.StringDtype] = pa.Field(nullable=True)
    Quantity: Series[int]
    InvoiceDate: Series[datetime]
    UnitPrice: Series[float]
    CustomerID: Series[float] = pa.Field(nullable=True)
    Country: Series[pd.StringDtype]


@pa.check_types
def retrieve_retail_products(path: Path | str) -> DataFrame[OutputSchema]:
    return pd.read_csv(
        path,
        dtype={
            "InvoiceNo": "string",
            "StockCode": "string",
            "Description": "string",
            "Country": "string",
        },
        parse_dates=["InvoiceDate"],
    )


products = retrieve_retail_products("datasets/online_retail.csv")
