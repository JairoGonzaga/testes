import math

import pytest

from alvo import apnumber

WORDS = (
    "zero", "one", "two", "three", "four",
    "five", "six", "seven", "eight", "nine",
)


def test_nine_is_spelled_out():
    """The reported bug: apnumber(9) must return 'nine', not '9'."""
    assert apnumber(9) == "nine"


@pytest.mark.parametrize("value, expected", list(enumerate(WORDS)))
def test_all_single_digits_are_spelled_out(value, expected):
    """Every single-digit number (0-9 inclusive) is spelled out."""
    assert apnumber(value) == expected


def test_last_spelled_out_digit_is_nine():
    assert apnumber(9) == "nine"
    # The very next number is no longer a single digit and stays numeric.
    assert apnumber(10) == "10"


def test_numbers_above_nine_stay_numeric():
    for value in (10, 11, 42, 1000):
        assert apnumber(value) == str(value)


def test_negative_numbers_stay_numeric():
    for value in (-1, -9, -100):
        assert apnumber(value) == str(value)


def test_non_numeric_values_are_returned_as_text():
    assert apnumber("abc") == "abc"
    assert apnumber(None) == "None"


def test_non_finite_values_are_formatted():
    assert apnumber(float("nan")) == "NaN"
    assert apnumber(float("inf")) == "+Inf"
    assert apnumber(float("-inf")) == "-Inf"
