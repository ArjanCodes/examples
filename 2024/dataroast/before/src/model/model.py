from sys import maxsize
from pandas import DataFrame
from pydantic.dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Model(ABC):
    @abstractmethod
    def create(self, alias: str, df: DataFrame): ...

    @abstractmethod
    def read(self, alias: str, head: int = maxsize) -> DataFrame: ...

    @abstractmethod
    def update(self, alias: str, df: DataFrame): ...

    @abstractmethod
    def delete(self, alias: str): ...

    @abstractmethod
    def get_table_names(self) -> list[str]: ...
