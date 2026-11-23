import pytest

from alvo import apnumber


def test_zero_is_spelled_out():
    """The issue: apnumber(0) must return 'zero', not the digit string '0'."""
    assert apnumber(0) == "zero"


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "zero"),
        (1, "one"),
        (2, "two"),
        (3, "three"),
        (4, "four"),
        (5, "five"),
        (6, "six"),
        (7, "seven"),
        (8, "eight"),
        (9, "nine"),
    ],
)
def test_single_digits_are_words(value, expected):
    """Docs promise numbers 0 through 9 are returned as words."""
    assert apnumber(value) == expected


def test_zero_float_is_spelled_out():
    assert apnumber(0.0) == "zero"


@pytest.mark.parametrize("value", [-1, 10, 11, 100])
def test_out_of_range_values_are_digits(value):
    """Values outside 0-9 are still rendered as plain digit strings."""
    assert apnumber(value) == str(value)


def test_non_numeric_values_unchanged():
    assert apnumber("abc") == "abc"
    assert apnumber(None) == "None"
