"""Reproduction tests for ISSUE.md: apnumber(None) crashes with TypeError.

Values that cannot be converted to a number are documented to be returned
unchanged (as ``str(value)``), so ``apnumber(None)`` should return ``'None'``
just like ``apnumber('abc')`` returns ``'abc'`` instead of raising.
"""

import math

import pytest

from alvo import apnumber


class Unconvertible:
    """Object whose numeric conversions raise TypeError."""

    def __str__(self):
        return "unconvertible"


def test_apnumber_none_returns_string_none():
    """The exact case from the issue report."""
    assert apnumber(None) == "None"


def test_apnumber_none_does_not_raise():
    """No exception should escape for values that are not numbers."""
    try:
        apnumber(None)
    except TypeError as exc:  # pragma: no cover - this is the bug
        pytest.fail(f"apnumber(None) raised TypeError: {exc}")
    except Exception as exc:  # pragma: no cover - defensive
        pytest.fail(f"apnumber(None) raised {type(exc).__name__}: {exc}")


@pytest.mark.parametrize("value", [None, [1], {"a": 1}, Unconvertible()])
def test_unconvertible_values_return_str(value):
    """Anything that is not a number is returned unchanged as a string."""
    result = apnumber(value)
    assert isinstance(result, str)
    assert result == str(value)


@pytest.mark.parametrize("value", [None, [1], {"a": 1}])
def test_unconvertible_values_are_consistent_with_non_numeric_strings(value):
    """The fallback behaves the same way as for e.g. 'abc'."""
    assert apnumber(value) == str(value)
    assert isinstance(apnumber("abc"), str)
    assert apnumber("abc") == "abc"


def test_none_and_string_fallback_agree():
    """None must be handled like any other non-convertible value."""
    assert apnumber(None) == "None"
    assert apnumber("None") == "None"


# --- Regression tests: documented behaviour must keep working -------------


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "zero"),
        (1, "one"),
        (5, "five"),
        (9, "nine"),
        ("0", "zero"),
        ("7", "seven"),
    ],
)
def test_small_ints_are_spelled_out(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize("value", [10, 11, -1, -100, 1000])
def test_out_of_range_ints_are_stringified(value):
    assert apnumber(value) == str(value)


def test_non_numeric_string_is_returned_unchanged():
    assert apnumber("abc") == "abc"


def test_non_finite_values():
    assert apnumber(float("nan")) == "NaN"
    assert apnumber(float("inf")) == "+Inf"
    assert apnumber(float("-inf")) == "-Inf"
    assert math.isnan(float("nan"))  # sanity check on the input used above
