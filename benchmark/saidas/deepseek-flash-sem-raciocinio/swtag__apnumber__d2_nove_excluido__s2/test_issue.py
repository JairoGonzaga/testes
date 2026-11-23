import math

import pytest

from alvo import apnumber

_WORDS = (
    "zero", "one", "two", "three", "four",
    "five", "six", "seven", "eight", "nine",
)


def test_apnumber_nine_is_spelled_out():
    """The issue: apnumber(9) should return 'nine', not '9'."""
    assert apnumber(9) == "nine"


@pytest.mark.parametrize("value, expected", list(enumerate(_WORDS)))
def test_single_digits_are_spelled_out(value, expected):
    assert apnumber(value) == expected


def test_nine_as_string_digit():
    assert apnumber("9") == "nine"


def test_values_outside_single_digit_range_are_stringified():
    assert apnumber(10) == "10"
    assert apnumber(-1) == "-1"
    assert apnumber(100) == "100"


def test_non_finite_values():
    assert apnumber(float("nan")) == "NaN"
    assert apnumber(float("inf")) == "+Inf"
    assert apnumber(float("-inf")) == "-Inf"


def test_non_numeric_values_are_stringified():
    assert apnumber("abc") == "abc"
    assert apnumber(None) == "None"
