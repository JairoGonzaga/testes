import pytest

from alvo import ordinal


def test_non_numeric_string_returned_as_is():
    assert ordinal("something else") == "something else"


def test_non_numeric_int_like_object_returned_as_str():
    assert ordinal([1, 2]) == "[1, 2]"


def test_none_returned_as_str():
    assert ordinal(None) == "None"


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (21, "21st"),
        (112, "112th"),
        (123, "123rd"),
        ("7", "7th"),
    ],
)
def test_ordinal_still_works_for_numbers(value, expected):
    assert ordinal(value) == expected
