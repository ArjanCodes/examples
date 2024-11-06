from src.model.model import Model

from os.path import exists


def values_are_strings(*args:str) -> bool:
    for value in args:
        if not isinstance(value, str):
            return False
    return True


def value_exists_in_dataframes(model:Model,arg: str) -> bool:
    return arg in model.get_table_names()


def cols_exists_in_dataframe(model:Model, *args:str) -> bool:
    cols = model.read(str(args[0])).columns.values.tolist()
    for arg in args[1:]:
        if arg not in cols:
            return False
    return True


def values_are_numereic(*args) -> bool:
    for value in args:
        if not value.isnumeric():
            return False
    return True

def path_exists(path:str) -> bool:
    return exists(path)
