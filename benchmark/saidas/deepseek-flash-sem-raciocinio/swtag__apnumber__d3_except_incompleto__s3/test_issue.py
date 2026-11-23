import math

import pytest

from alvo import apnumber


def test_apnumber_none_returns_string():
    # Main issue: None cannot be converted, so it must be returned as str(value)
    assert apnumber(None) == "None"


@pytest.mark.parametrize("value", [None, "abc", "None", "hello"])
def test_apnumber_unconvertible_values_return_str(value):
    assert apnumber(value) == str(value)


def test_apnumber_none_does_not_raise():
    # Should not raise TypeError anymore
    try:
        result = apnumber(None)
    except TypeError as exc:  # pragma: no cover - failure path
        pytest.fail(f"apnumber(None) raised TypeError: {exc}")
    assert isinstance(result, str)


def test_unrelated_behaviour_still_ok():
    # Sanity checks that should hold both before and after the fix
    assert apnumber(0) == "zero"
    assert apnumber(3) == "three"
    assert apnumber(9) == "nine"
    assert apnumber(10) == "10"
    assert apnumber("5") == "five"
    assert apnumber("3.5") == "3.5"
    assert apnumber(float("nan")) == "NaN"
    assert apnumber(float("inf")) == "+Inf"
    assert apnumber(float("-inf")) == "-Inf"


def test_nan_detection_untouched():
    assert math.isnan(float("nan"))
