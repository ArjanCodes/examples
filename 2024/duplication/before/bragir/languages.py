from enum import StrEnum, auto
from typing import Any, Type


class Languages(StrEnum):
    PORTUGUESE = auto()
    SPANISH = auto()
    FRENCH = auto()
    POLISH = auto()
    GERMAN = auto()
    ITALIAN = auto()
    DUTCH = auto()
    SWEDISH = auto()
    DANISH = auto()
    NORWEGIAN = auto()
    FINNISH = auto()
    TURKISH = auto()


def to_output(enum_class: Type[StrEnum]) -> str:
    formatted_enum = " ".join([f"{enum.value}" for enum in enum_class])
    return formatted_enum


def parse_languages(input_languages: Any):
    valid_languages: list[Languages] = []
    valid_string_languages = [language.value.lower() for language in Languages]

    for target_language in input_languages:
        if target_language.lower() in valid_string_languages:
            valid_languages.append(Languages[target_language.upper()])

    return valid_languages
