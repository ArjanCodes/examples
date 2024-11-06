from abc import ABC, abstractmethod

from model.model import Model
from pydantic.dataclasses import dataclass


@dataclass
class CommandArgs:
    model: Model


class Command(ABC):
    @abstractmethod
    def execute(self, args: CommandArgs): ...
