from events import raise_event

from .model import Model


def show_files(model: Model) -> None:
    table_names = model.get_table_names()
    if len(table_names) == 0:
        raise_event("files", "No files currently stored.")
        return

    message = "Files presently stored:"
    for name in table_names:
        message += f"\nAlias: {name}"
    raise_event("files", message)
