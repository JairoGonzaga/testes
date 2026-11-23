"""Tests reproducing the issue: apnumber(None) raises TypeError instead of
returning the string 'None'.

Values that cannot be converted to a number must be returned unchanged as a
string (`str(value)`), exactly like `apnumber('abc')` returns `'abc'`.
"""

import math

import pytest

from alvo import apnumber


def test_apnumber_none_returns_string_none():
    """The core of the issue: apnumber(None) must not raise."""
    assert apnumber(None) == "None"


def test_apnumber_none_does_not_raise_type_error():
    try:
        result = apnumber(None)
    except TypeError as exc:  # pragma: no cover - only on buggy code
        pytest.fail(f"apnumber(None) raised TypeError: {exc}")
    assert isinstance(result, str)


@pytest.mark.parametrize("value", [[], {}, (1, 2), set()])
def test_apnumber_non_numeric_containers_returned_as_string(value):
    """Other non-numeric objects must also be returned as str(value)."""
    assert apnumber(value) == str(value)


def test_apnumber_object_with_str_returned_unchanged():
    class Thing:
        def __str__(self):
            return "thing"

    assert apnumber(Thing()) == "thing"


@pytest.mark.parametrize("value", ["abc", "", "hello world", "b'x'"])
def test_apnumber_non_numeric_strings_returned_unchanged(value):
    assert apnumber(value) == value


def test_apnumber_small_integers_still_spelled_out():
    assert apnumber(0) == "zero"
    assert apnumber(3) == "three"
    assert apnumber(9) == "nine"
    assert apnumber(3.0) == "three"
    assert apnumber("7") == "seven"


def test_apnumber_non_small_integers_returned_as_string():
    assert apnumber(10) == "10"
    assert apnumber(-1) == "-1"


def test_apnumber_non_finite_values():
    assert apnumber(float("nan")) == "NaN"
    assert apnumber(float("inf")) == "+Inf"
    assert apnumber(float("-inf")) == "-Inf"
