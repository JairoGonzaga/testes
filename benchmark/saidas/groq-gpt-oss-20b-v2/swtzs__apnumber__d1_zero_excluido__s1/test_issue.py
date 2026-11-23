import math

import pytest

from alvo import apnumber


def test_apnumber_zero():
    """Zero should be spelled out, not returned as a digit string."""
    assert apnumber(0) == "zero"


def test_apnumber_single_digits():
    """Other single digits should return their word forms."""
    assert apnumber(5) == "five"
    assert apnumber(9) == "nine"


def test_apnumber_two_digit():
    """Numbers with two or more digits should be returned as strings."""
    assert apnumber(10) == "10"
    assert apnumber(99) == "99"


def test_apnumber_floats():
    """Integers provided as floats should still be spelled out."""
    assert apnumber(5.0) == "five"
    assert apnumber(0.0) == "zero"


def test_apnumber_negative():
    """Negative integers should be returned as strings."""
    assert apnumber(-1) == "-1"
    assert apnumber(-9) == "-9"


def test_apnumber_non_finite():
    """Non‑finite values should be represented specially."""
    assert apnumber(math.nan) == "NaN"
    assert apnumber(math.inf) == "+Inf"
    assert apnumber(-math.inf) == "-Inf"
