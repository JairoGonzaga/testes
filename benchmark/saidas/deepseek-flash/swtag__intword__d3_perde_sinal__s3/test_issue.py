import pytest

from alvo import intword


def test_negative_million_keeps_minus_sign():
    assert intword(-1000000) == "-1.0 million"


def test_negative_thousand_keeps_minus_sign():
    assert intword(-1234) == "-1.2 thousand"


def test_negative_several_units_keep_minus_sign():
    assert intword(-1500000000) == "-1.5 billion"
    assert intword(-2000000000000) == "-2.0 trillion"


def test_negative_below_first_power_keeps_minus_sign():
    assert intword(-999) == "-999"
    assert intword(-1) == "-1"


def test_negative_with_custom_format_keeps_minus_sign():
    assert intword(-1234567, "%.2f") == "-1.23 million"


def test_positive_values_unchanged():
    assert intword(1000000) == "1.0 million"
    assert intword(1234) == "1.2 thousand"
    assert intword(999) == "999"


def test_rounding_up_boundary_negative():
    # -999950 rounds up to the next unit; the sign must survive the promotion too
    assert intword(-999950) == "-1.0 million"


def test_non_finite_values_unchanged():
    assert intword(float("-inf")) == "-Inf"
    assert intword(float("inf")) == "+Inf"
    assert intword(float("nan")) == "NaN"
