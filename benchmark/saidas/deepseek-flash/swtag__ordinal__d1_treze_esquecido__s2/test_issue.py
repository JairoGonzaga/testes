"""Reproduction tests for the issue: ``ordinal(13)`` returns ``'13rd'``.

The suffix table makes 11, 12 and 13 special cases (they always take "th"),
but the implementation only special-cases 11 and 12:

    digit = 0 if value % 100 in (11, 12) else value % 10

so 13 (and any number whose last two digits are 13, e.g. 113, 1013) gets the
third-entry suffix "rd" instead of "th".
"""

import pytest

from alvo import ordinal


def test_issue_ordinal_13():
    """Exact example from the issue report."""
    assert ordinal(13) == "13th"


def test_issue_ordinal_13_is_not_rd():
    """Sanity check on the buggy value, to make the failure message explicit."""
    assert ordinal(13) != "13rd"


@pytest.mark.parametrize("value", [13, 113, 213, 1013, 1113, 10013])
def test_issue_numbers_ending_in_13(value):
    """Any number whose last two digits are 13 takes the 'th' suffix."""
    assert ordinal(value) == f"{value}th"


@pytest.mark.parametrize(
    "value, expected",
    [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (14, "14th"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (114, "114th"),
    ],
)
def test_issue_teens_and_repeated_teens(value, expected):
    """All three teens (11th, 12th, 13th) and their repeats behave alike."""
    assert ordinal(value) == expected


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
        (22, "22nd"),
        (23, "23rd"),
        (24, "24th"),
        (100, "100th"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
        (104, "104th"),
    ],
)
def test_issue_ordinal_table(value, expected):
    """Regression table: the accepted behaviour for ordinary ordinals."""
    assert ordinal(value) == expected


def test_issue_other_behaviours_still_work():
    """Non-finite handling should be untouched by the fix for 13."""
    assert ordinal(float("nan")) == "NaN"
    assert ordinal(float("inf")) == "+Inf"
    assert ordinal(float("-inf")) == "-Inf"
