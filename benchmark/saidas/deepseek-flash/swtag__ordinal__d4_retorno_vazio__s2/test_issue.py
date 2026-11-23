"""Tests reproducing the issue: ordinal() returns '' for non-numeric input.

ISSUE.md says values that cannot be converted to int should be returned as
``str(value)``, but the function currently returns an empty string.
"""

import pytest

from alvo import ordinal


@pytest.mark.parametrize(
    "value",
    [
        "something else",
        "hello world",
        "abc",
        "5th",
        "first",
        "  ",
    ],
)
def test_non_numeric_string_is_returned_as_is(value):
    """A non-numeric string must come back as str(value), not ''."""
    assert ordinal(value) == value


def test_issue_example():
    """Exact reproduction of the example from ISSUE.md."""
    assert ordinal("something else") == "something else"


def test_non_numeric_input_is_not_empty():
    """The buggy behaviour was an empty string; make sure it is gone."""
    result = ordinal("something else")
    assert result != ""
    assert isinstance(result, str)


# --- regression checks: the normal behaviour must keep working -----------


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (5, "5th"),
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (101, "101st"),
        (111, "111th"),
        ("7", "7th"),
        ("23", "23rd"),
    ],
)
def test_valid_values_still_get_ordinal_suffix(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (float("nan"), "NaN"),
        (float("inf"), "+Inf"),
        (float("-inf"), "-Inf"),
    ],
)
def test_non_finite_values_are_unchanged(value, expected):
    assert ordinal(value) == expected
