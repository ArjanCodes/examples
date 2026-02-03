from dataclasses import InitVar, dataclass


@dataclass
class User:
    email: str
    raw_password: InitVar[str]
