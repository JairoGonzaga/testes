import pytest

from alvo import ordinal


def test_non_numeric_string_is_returned_as_is():
    # Reported in ISSUE.md: ordinal('something else') returns '' instead of the input.
    assert ordinal("something else") == "something else"


@pytest.mark.parametrize("value", ["something else", "abc", "1.5", None])
def test_value_that_cannot_become_int_is_returned_as_str(value):
    assert ordinal(value) == str(value)


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
        ("22", "22nd"),
    ],
)
def test_numeric_values_still_get_ordinal_suffix(value, expected):
    assert ordinal(value) == expected
