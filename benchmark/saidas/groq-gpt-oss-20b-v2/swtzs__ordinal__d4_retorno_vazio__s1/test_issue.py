# test_issue.py
import pytest

from alvo import ordinal


def test_numeric_ordinals():
    """Numeric values should return correct ordinal strings."""
    assert ordinal(1) == "1st"
    assert ordinal(2) == "2nd"
    assert ordinal(3) == "3rd"
    assert ordinal(4) == "4th"
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"
    assert ordinal(21) == "21st"
    assert ordinal(22) == "22nd"
    assert ordinal(23) == "23rd"
    assert ordinal(24) == "24th"


def test_non_numeric_returns_string():
    """Non‑numeric input should be returned as the string representation of the value."""
    # The current buggy implementation returns an empty string for this input.
    assert ordinal("something else") == "something else"


def test_non_finite_values():
    """Non‑finite numeric values are delegated to _format_not_finite."""
    assert ordinal(float("nan")) == "NaN"
    assert ordinal(float("inf")) == "+Inf"
    assert ordinal(float("-inf")) == "-Inf"
