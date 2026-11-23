"""Reproduction tests for the issue: `ordinal()` returns an empty string for
non-numeric input instead of `str(value)`.

The bug lives in the `except (TypeError, ValueError)` branch of
`alvo.ordinal`, which returns `''` rather than the string form of the value.
"""

import pytest

from alvo import ordinal


def test_ordinal_returns_string_form_of_unparseable_text():
    # The exact example from the issue report.
    assert ordinal("something else") == "something else"


def test_ordinal_returns_string_form_of_arbitrary_text():
    assert ordinal("abc") == "abc"
    assert ordinal("") == ""
    assert ordinal("12th") == "12th"


def test_ordinal_returns_string_form_of_none():
    assert ordinal(None) == "None"


def test_ordinal_returns_string_form_of_containers():
    assert ordinal([]) == "[]"
    assert ordinal([1, 2]) == "[1, 2]"
    assert ordinal({}) == "{}"
    assert ordinal({"a": 1}) == "{'a': 1}"


def test_ordinal_returns_string_form_of_arbitrary_object():
    class NotANumber:
        def __str__(self):
            return "not a number"

        def __int__(self):
            raise TypeError("cannot convert")

        def __float__(self):
            raise TypeError("cannot convert")

    value = NotANumber()
    assert ordinal(value) == "not a number"
    assert ordinal(value) == str(value)


@pytest.mark.parametrize("gender", ["male", "female"])
def test_ordinal_non_numeric_input_with_gender(gender):
    assert ordinal("something else", gender=gender) == "something else"
    assert ordinal(None, gender=gender) == "None"


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0th"),
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
        (112, "112th"),
        (101, "101st"),
        ("12", "12th"),
    ],
)
def test_ordinal_still_formats_numbers_correctly(value, expected):
    """Regression guard: numeric behaviour must not change with the fix."""
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (float("nan"), "NaN"),
        (float("inf"), "+Inf"),
        (float("-inf"), "-Inf"),
    ],
)
def test_ordinal_non_finite_values_unchanged(value, expected):
    """Regression guard: non-finite handling must not change with the fix."""
    assert ordinal(value) == expected
