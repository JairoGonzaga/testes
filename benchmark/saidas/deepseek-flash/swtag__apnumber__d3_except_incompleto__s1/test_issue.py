"""Tests reproducing the issue: apnumber(None) (and other non-numeric values) crash
with TypeError instead of being returned unchanged as ``str(value)``."""

import math

import pytest

from alvo import apnumber


def test_apnumber_none_returns_string_none():
    # The core bug from the issue report.
    assert apnumber(None) == "None"


def test_apnumber_none_does_not_raise():
    try:
        result = apnumber(None)
    except TypeError as exc:  # pragma: no cover - only on broken code
        pytest.fail(f"apnumber(None) raised TypeError: {exc}")
    assert result == "None"
    assert isinstance(result, str)


def test_apnumber_other_non_convertible_value_returns_str():
    # Same contract as apnumber('abc') -> 'abc': unconvertible values are
    # returned unchanged as a string.
    assert apnumber([1, 2]) == str([1, 2])
    assert apnumber({"a": 1}) == str({"a": 1})


def test_apnumber_unconvertible_object_returns_its_str():
    class Unconvertible:
        def __float__(self):
            raise TypeError("not convertible")

        def __repr__(self):
            return "<unconvertible>"

    assert apnumber(Unconvertible()) == str(Unconvertible())


# Sanity checks: behaviour that already works must keep working.


def test_apnumber_string_unchanged():
    assert apnumber("abc") == "abc"


def test_apnumber_small_integers():
    assert apnumber(0) == "zero"
    assert apnumber(3) == "three"
    assert apnumber(9) == "nine"
    assert apnumber(3.0) == "three"


def test_apnumber_out_of_range():
    assert apnumber(10) == "10"
    assert apnumber(-1) == "-1"
    assert apnumber(123) == "123"


def test_apnumber_not_finite():
    assert apnumber(float("nan")) == "NaN"
    assert apnumber(float("inf")) == "+Inf"
    assert apnumber(float("-inf")) == "-Inf"
    assert apnumber(math.nan) == "NaN"
