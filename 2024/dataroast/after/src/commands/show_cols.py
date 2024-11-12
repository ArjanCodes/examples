from commands.validations import validate_alias_exists
from events import raise_event

from .model import Model


def show_cols(model: Model, alias: str) -> None:
    validate_alias_exists(model, alias)
    raise_event("cols", model.read(alias).columns.values)
