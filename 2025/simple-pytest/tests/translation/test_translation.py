from unittest.mock import Mock

from src.translation import (
    split_by_breakpoints,
    translate,
)
from src.translation.translation import Part


def test_empty_list_of_collection():
    assert split_by_breakpoints([], [1]) == []


def test_empty_list_of_breakpoints_with_one_element_collection():
    assert split_by_breakpoints([1], []) == [1]


def test_list_of_different_types():
    collection: list[int | str | float | list[int] | dict[str, int]] = [
        1,
        "two",
        3.0,
        [4],
        {"five": 5},
    ]
    breakpoints = [2, 4]
    expected: list[list[int | str] | list[float | list[int]] | list[dict[str, int]]] = [
        [1, "two"],
        [3.0, [4]],
        [{"five": 5}],
    ]
    assert split_by_breakpoints(collection, breakpoints) == expected


def test_breakpoint_out_of_bounds():
    collection = [1, 2, 3]
    breakpoints = [5]
    expected: list[list[int]] = [
        [1, 2, 3]
    ]  # Might need clarification based on desired behavior
    assert split_by_breakpoints(collection, breakpoints) == expected


def test_breakpoints_higher_than_length():
    collection = [1, 2, 3]
    breakpoints = [4, 5]
    expected: list[list[int]] = [
        [1, 2, 3],
        [],
    ]  # Might need clarification based on desired behavior
    assert split_by_breakpoints(collection, breakpoints) == expected


def test_translate_with_mock_openai(mocker: Mock):
    # Mock the translator object and its method chain
    mock_translator = mocker.Mock()
    mock_parse = mock_translator.beta.chat.completions.parse
    mock_parse.return_value = Mock(
        choices=[Mock(message=Mock(content="translated content"))]
    )

    # Mock the SRTPart object
    mock_part = Mock()
    mock_part.index = 1
    mock_part.content = "This is a test."

    # Define the language
    language = "fr"

    # Call the translate function
    result = translate(mock_translator, mock_part, language)

    # Assertions
    mock_parse.assert_called_once_with(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": """
                You are a translation machine that only translates text to **fr**.

                Translate only into fr without altering any other language.

                Index is the following: 1
            """,
            },
            {"role": "user", "content": "This is a test."},
        ],
        response_format=Part,  # Replace Mock with `Part` if it's a specific type
    )

    assert result == "translated content"
