import math
import pytest

from alvo import _format_not_finite, apnumber

# Tests for _format_not_finite

def test_format_not_finite_nan():
    assert _format_not_finite(float('nan')) == "NaN"

def test_format_not_finite_negative_inf():
    assert _format_not_finite(-math.inf) == "-Inf"

def test_format_not_finite_positive_inf():
    assert _format_not_finite(math.inf) == "+Inf"

def test_format_not_finite_finite_number_returns_empty():
    for val in [0, 1.23, -5.6, 42]:
        assert _format_not_finite(val) == ""

# Tests for apnumber

@pytest.mark.parametrize(
    "input_value,expected",
    [
        (0, "zero"),
        (1, "one"),
        (5, "five"),
        (9, "nine"),
        (3.7, "three"),  # float truncated to int
        (8.9, "eight"),
        (0.0, "zero"),
        (-1, "-1"),
        (-2.3, "-2"),
        (10, "10"),
        (123, "123"),
        (True, "one"),  # bool is subclass of int
        (False, "zero"),
    ],
)
def test_apnumber_basic(input_value, expected):
    assert apnumber(input_value) == expected

def test_apnumber_non_finite_nan():
    assert apnumber(float('nan')) == "NaN"
    # also string representations that become NaN via float conversion
    assert apnumber("nan") == "NaN"

def test_apnumber_non_finite_infinities():
    assert apnumber(math.inf) == "+Inf"
    assert apnumber(-math.inf) == "-Inf"
    assert apnumber("inf") == "+Inf"
    assert apnumber("-inf") == "-Inf"

def test_apnumber_invalid_conversion_returns_str():
    # value that cannot be converted to float raises TypeError/ValueError
    class Bad:
        def __float__(self):
            raise ValueError("bad float")
    bad_instance = Bad()
    assert apnumber(bad_instance) == str(bad_instance)

    # string that is not a number
    assert apnumber("not-a-number") == "not-a-number"

    # bytes that cannot be converted to float
    assert apnumber(b"abc") == "b'abc'"

def test_apnumber_string_numeric_not_int_convertible():
    # "3.5" becomes float 3.5 (finite) then int conversion fails, returns original string
    assert apnumber("3.5") == "3.5"
    # "-7.9" similarly
    assert apnumber("-7.9") == "-7.9"

def test_apnumber_custom_float_object():
    class Foo:
        def __float__(self):
            return 4.2
        def __int__(self):
            return 4
        def __repr__(self):
            return "Foo()"
        def __str__(self):
            return "Foo()"
    # float conversion succeeds, int conversion yields 4, maps to word "four"
    assert apnumber(Foo()) == "four"

def test_apnumber_zero_and_boundary():
    # Zero as different types
    assert apnumber(0) == "zero"
    assert apnumber("0") == "zero"
    # Boundary just below 10
    assert apnumber(9) == "nine"
    # Boundary just at 10 returns numeric string
    assert apnumber(10) == "10"
