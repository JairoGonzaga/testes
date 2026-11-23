import math
import pytest
from alvo import apnumber

def test_apnumber_none_returns_string():
    """apnumber should return the string 'None' for a None input."""
    assert apnumber(None) == "None"

def test_apnumber_non_numeric_string():
    """Non‑numeric strings are returned unchanged."""
    assert apnumber("abc") == "abc"

def test_apnumber_small_integer():
    """Integers 0‑9 are converted to their word form."""
    assert apnumber(5) == "five"
    assert apnumber(0) == "zero"

def test_apnumber_out_of_range_integer():
    """Integers outside 0‑9 are returned as strings."""
    assert apnumber(10) == "10"
    assert apnumber(-3) == "-3"

def test_apnumber_non_finite_values():
    """Non‑finite floats are formatted specially."""
    assert apnumber(float("nan")) == "NaN"
    assert apnumber(float("inf")) == "+Inf"
    assert apnumber(float("-inf")) == "-Inf"
