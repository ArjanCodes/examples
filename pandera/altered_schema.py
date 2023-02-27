from pandera import Check, Column, DataFrameSchema

schema = DataFrameSchema(
    columns={
        "InvoiceNo": Column(
            dtype="str",  # Changed
            checks=None,
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "StockCode": Column(
            dtype="str",  # Changed
            checks=None,
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "Description": Column(
            dtype="str",  # Changed
            checks=None,
            nullable=True,  # Changed
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "Quantity": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(min_value=1),
                # Removed this Check
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "InvoiceDate": Column(
            dtype="datetime",  # Changed
            checks=None,
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "UnitPrice": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(min_value=0.01),
                # Removed this Check
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "CustomerID": Column(
            dtype="float64",
            # Removed all Checks (makes no sense)
            checks=None,
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "Country": Column(
            dtype="str",  # Changed
            checks=None,
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
    },
    checks=None,
    # Removed Index checks (makes no sense)
    dtype=None,
    coerce=True,
    strict=False,
    name=None,
    ordered=False,
    unique=None,
    report_duplicates="all",
    unique_column_names=False,
    title=None,
    description=None,
)
