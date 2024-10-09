import pytest

from main import levenshtein_distance


@pytest.mark.parametrize(
    "str1, str2, expected",
    [
        ("kitten", "sitting", 3),
        ("flaw", "lawn", 2),
        ("gumbo", "gambol", 2),
        ("kitten", "kitten", 0),
        ("kitten", "", 6),
        ("", "sitting", 7),
        ("", "", 0),
        ("a", "b", 1),
        ("ab", "ac", 1),
        ("abc", "ac", 1),
        ("abc", "abc", 0),
        ("abc", "def", 3),
        ("abc", "defg", 4),
    ],
)
def test_levenshtein_distance(str1: str, str2: str, expected: int) -> None:
    assert levenshtein_distance(str1, str2) == expected
