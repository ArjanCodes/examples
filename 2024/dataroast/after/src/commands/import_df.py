import pandas as pd
from commands.validations import validate_path_exists
from events import raise_event

from .model import Model


def import_df(model: Model, alias: str, path: str) -> None:
    validate_path_exists(path)

    df = pd.read_csv(path)
    model.create(alias, df)
    raise_event("import", "Imported!")
