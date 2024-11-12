from commands.validations import validate_alias_exists
from events import raise_event

from .model import Model


def show_data(model: Model, alias: str, num: int | None = None) -> None:
    if num is None:
        raise ValueError("num must be provided")
    
    validate_alias_exists(model, alias)
    raise_event("data", model.read(alias, num))
