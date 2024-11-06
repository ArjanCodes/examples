from dataclasses import field
from sys import maxsize

from model.model import Model
from pandas import DataFrame
from pydantic.dataclasses import dataclass


@dataclass
class DataDictionary(Model):
    dataframes: dict = field(default_factory=dict)

    def create(self, alias: str, df: DataFrame) -> None:
        self.dataframes[alias] = df

    def read(self, alias: str, head: int = maxsize) -> DataFrame:
        if alias not in self.dataframes:
            raise Exception(f"Dataframe {alias} not found!")
        return self.dataframes[alias].head(head)

    def update(self, alias: str, df: DataFrame) -> None:
        if alias not in self.dataframes:
            raise Exception(f"Dataframe {alias} not found!")
        self.dataframes[alias] = df

    def delete(self, alias: str) -> None:
        if alias not in self.dataframes:
            raise Exception(f"Dataframe {alias} not found!")
        del self.dataframes[alias]

    def get_table_names(self) -> list[str]:
        return [df for df in self.dataframes.keys()]
