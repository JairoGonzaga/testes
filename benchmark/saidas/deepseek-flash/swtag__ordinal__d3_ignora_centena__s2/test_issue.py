"""Reproduction tests for ISSUE.md: ordinal(111) returns '111st' instead of '111th'.

The suffix must be chosen from the last TWO digits of the number: any number
whose last two digits are 11, 12 or 13 takes the "th" suffix, no matter how
many digits precede them (111, 112, 113, 1011, 2113, ...).
"""

import pytest

from alvo import ordinal


@pytest.mark.parametrize(
    "value, expected",
    [
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
    ],
)
def test_teen_suffix_for_three_digit_numbers(value, expected):
    """The exact case reported in the issue: ordinal(111) must be '111th'."""
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (211, "211th"),
        (212, "212th"),
        (213, "213th"),
        (311, "311th"),
        (1011, "1011th"),
        (1012, "1012th"),
        (1013, "1013th"),
        (2111, "2111th"),
        (2112, "2112th"),
        (2113, "2113th"),
        (999911, "999911th"),
        (999912, "999912th"),
        (999913, "999913th"),
    ],
)
def test_teen_suffix_for_any_number_ending_in_11_12_13(value, expected):
    """Numbers whose last two digits are 11/12/13 always take 'th'."""
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
    ],
)
def test_teen_suffix_for_two_digit_numbers_still_works(value, expected):
    """Regression check: the behaviour that already worked must be preserved."""
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (24, "24th"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
        (104, "104th"),
        (0, "0th"),
        (10, "10th"),
        (20, "20th"),
        (100, "100th"),
        (110, "110th"),
        (120, "120th"),
        (1000, "1000th"),
    ],
)
def test_regular_suffixes_are_unchanged(value, expected):
    """All non-teen endings keep the plain digit-based suffix."""
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (-111, "-111th"),
        (-112, "-112th"),
        (-113, "-113th"),
        (-1011, "-1011th"),
    ],
)
def test_negative_numbers_ending_in_11_12_13(value, expected):
    """Negative numbers ending in 11/12/13 are 'th' too (suffix by magnitude)."""
    assert ordinal(value) == expected
