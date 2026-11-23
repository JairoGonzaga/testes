"""Reproduction tests for: ordinal() returns '' for non-numeric input.

The issue states that values which cannot be converted to int should be
returned as ``str(value)`` instead of an empty string.
"""

import pytest

from alvo import ordinal


def test_non_numeric_string_is_returned_as_str():
    # The exact example from the issue report.
    assert ordinal("something else") == "something else"


@pytest.mark.parametrize(
    "value",
    [
        "something else",
        "abc",
        "abc123",
        None,
        [1, 2],
        {"a": 1},
    ],
)
def test_unconvertible_values_are_returned_as_str(value):
    assert ordinal(value) == str(value)


def test_unconvertible_object_instance_is_returned_as_str():
    class Unconvertible:
        def __str__(self):
            return "unconvertible"

        def __float__(self):
            raise TypeError("not a number")

        def __int__(self):
            raise ValueError("not a number")

    obj = Unconvertible()
    assert ordinal(obj) == "unconvertible"


def test_valid_inputs_still_work():
    # Guard against a "fix" that breaks the normal behaviour.
    assert ordinal(1) == "1st"
    assert ordinal(2) == "2nd"
    assert ordinal(3) == "3rd"
    assert ordinal(4) == "4th"
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"
    assert ordinal(21) == "21st"
    assert ordinal(42) == "42nd"
    assert ordinal(112) == "112th"
    assert ordinal("42") == "42nd"
    assert ordinal(2.7) == "2nd"


def test_non_finite_values_unchanged():
    assert ordinal(float("nan")) == "NaN"
    assert ordinal(float("inf")) == "+Inf"
    assert ordinal(float("-inf")) == "-Inf"
