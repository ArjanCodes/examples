import pandas as pd
from commands.validations import validate_alias_exists, validate_cols_exist
from events import raise_event

from .model import Model

DUPLICATE_SUFFIX = "_duplicate"


def merge(
    model: Model,
    file1: str,
    file2: str,
    left_on: str,
    right_on: str,
    alias: str,
    cols: list[str] = [],
) -> None:
    validate_alias_exists(model, file1)
    validate_alias_exists(model, file2)

    if len(cols) > 0:
        cols.append(right_on)
    else:
        
        cols = model.read(file2).columns.values.tolist()

    validate_cols_exist(model, file1, [left_on])
    validate_cols_exist(model, file2, [right_on, *cols])

    file: pd.DataFrame = pd.merge(
        model.read(file1),
        model.read(file2)[cols],
        how="left",
        left_on=left_on,
        right_on=right_on,
        suffixes=(None, DUPLICATE_SUFFIX),
    )

    drop_cols = [col for col in file.columns if col.endswith(DUPLICATE_SUFFIX)]
    file.drop(columns=drop_cols, inplace=True)
    model.create(alias, file)
    raise_event("merge", file)
