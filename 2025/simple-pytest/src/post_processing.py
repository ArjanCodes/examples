from functools import reduce
import re


def check_first_is_quote(text: str) -> bool:
    first_letter = text[0]

    return first_letter == '"'


def check_last_is_quote(text: str) -> bool:
    last_letter = text[-1]

    return last_letter == '"'


def remove_quoutes(text: str) -> str:
    if check_first_is_quote(text) and check_last_is_quote(text):
        return text[1:-1]

    if check_first_is_quote(text):
        return text[1:]

    if check_last_is_quote(text):
        return text[:-1]

    return text


def remove_space(text: str, index: int) -> str:
    return text[:index] + text[index + 1 :]


def remove_space_as_first_character(text: str) -> str:
    if text[0] == " ":
        return remove_space(text, 0)
    else:
        return text


def remove_all_newline_before_first_character(text: str) -> str:
    while text[0] == "\n":
        text = remove_space(text, 0)
    return text


def remove_newline_in_the_middle(text: str) -> str:
    first_char = re.search(r"\S", text)
    if first_char is None:
        return text
    first_charachter_index = first_char.start()
    last_charachter_index = len(text) - 1

    in_the_middle_text = text[first_charachter_index:last_charachter_index]

    replaced_text = in_the_middle_text.replace("\n\n", "").replace("\n", " ")

    return text[:first_charachter_index] + replaced_text + text[last_charachter_index]


def process_text(text: str) -> str:
    pipeline = [
        remove_quoutes,
        remove_space_as_first_character,
        remove_all_newline_before_first_character,
        remove_newline_in_the_middle,
    ]

    result = reduce(lambda acc, func: func(acc), pipeline, text)

    return result
