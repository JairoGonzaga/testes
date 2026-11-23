import pytest

from alvo import ordinal


def test_non_numeric_string_is_returned_as_is():
    # Reported case: ordinal('something else') returns '' instead of the input.
    assert ordinal('something else') == 'something else'


@pytest.mark.parametrize("value", ["abc", "not a number", "primeiro"])
def test_non_numeric_values_return_str_of_value(value):
    assert ordinal(value) == str(value)


def test_none_returns_str_of_none():
    # None cannot be converted to int either, so it should fall back to str(value).
    assert ordinal(None) == 'None'


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
        (111, "111th"),
        (112, "112th"),
        ("3", "3rd"),
    ],
)
def test_numeric_values_still_get_ordinal_suffix(value, expected):
    assert ordinal(value) == expected
