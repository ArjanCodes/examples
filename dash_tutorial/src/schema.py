import enum


@enum.unique
class DataSchema(enum.Enum):
    DATE = "date"
    AMOUNT = "amount"
    CATEGORY = "category"
    YEAR = "year"
    MONTH = "month"
