"""Reproduction tests for the issue: apnumber(9) returns '9' instead of 'nine'."""

import pytest

from alvo import apnumber


WORDS = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
}


def test_apnumber_nine_returns_word_nine():
    """The exact case reported in the issue."""
    assert apnumber(9) == "nine"


@pytest.mark.parametrize("value,expected", sorted(WORDS.items()))
def test_single_digits_are_spelled_out(value, expected):
    """Every single digit (0 through 9) must be spelled out."""
    assert apnumber(value) == expected


def test_apnumber_nine_from_string_input():
    """A digit given as a string should also be spelled out."""
    assert apnumber("9") == "nine"


def test_apnumber_nine_from_float_input():
    """A float that is exactly 9 should be spelled out too."""
    assert apnumber(9.0) == "nine"


@pytest.mark.parametrize("value", [10, 11, 42, 100, -1, -9])
def test_numbers_outside_single_digits_stay_digits(value):
    """Regression guard: values outside 0..9 must still be returned as digits."""
    assert apnumber(value) == str(value)
