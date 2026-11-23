import math
import pytest

from alvo import (
    intword,
    _format_not_finite,
    powers,
    human_powers,
)


def test_powers_and_human_powers():
    assert powers == [10**x for x in (3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 100)]
    assert human_powers == (
        "thousand", "million", "billion", "trillion", "quadrillion", "quintillion",
        "sextillion", "septillion", "octillion", "nonillion", "decillion", "googol",
    )
    assert len(powers) == len(human_powers)


def test_format_not_finite_nan():
    assert _format_not_finite(float("nan")) == "NaN"


def test_format_not_finite_neg_inf():
    assert _format_not_finite(float("-inf")) == "-Inf"


def test_format_not_finite_pos_inf():
    assert _format_not_finite(float("inf")) == "+Inf"


def test_format_not_finite_regular():
    assert _format_not_finite(123.0) == ""
    assert _format_not_finite(0.0) == ""
    assert _format_not_finite(-5.0) == ""


def test_intword_nan():
    assert intword(float("nan")) == "NaN"


def test_intword_pos_inf():
    assert intword(float("inf")) == "+Inf"


def test_intword_neg_inf():
    assert intword(float("-inf")) == "-Inf"


def test_intword_string_inf():
    assert intword("inf") == "+Inf"
    assert intword("-inf") == "-Inf"
    assert intword("nan") == "NaN"


def test_intword_non_numeric_string():
    assert intword("hello") == "hello"


def test_intword_none():
    assert intword(None) == "None"


def test_intword_zero():
    assert intword(0) == "0"


def test_intword_small_positive():
    assert intword(1) == "1"
    assert intword(999) == "999"


def test_intword_small_negative():
    assert intword(-1) == "-1"
    assert intword(-999) == "-999"


def test_intword_thousand():
    assert intword(1000) == "1.0 thousand"


def test_intword_negative_thousand():
    assert intword(-1000) == "-1.0 thousand"


def test_intword_million():
    assert intword(1_000_000) == "1.0 million"


def test_intword_various_units():
    assert intword(10**6) == "1.0 million"
    assert intword(10**9) == "1.0 billion"
    assert intword(10**12) == "1.0 trillion"
    assert intword(10**15) == "1.0 quadrillion"
    assert intword(10**18) == "1.0 quintillion"
    assert intword(10**21) == "1.0 sextillion"
    assert intword(10**24) == "1.0 septillion"
    assert intword(10**27) == "1.0 octillion"
    assert intword(10**30) == "1.0 nonillion"
    assert intword(10**33) == "1.0 decillion"
    assert intword(10**100) == "1.0 googol"


def test_intword_rounding_up_crosses_unit():
    # 999_950 -> rounds to 1000.0 thousand -> becomes 1.0 million
    assert intword(999_950) == "1.0 million"


def test_intword_rounding_up_crosses_unit_negative():
    assert intword(-999_950) == "-1.0 million"


def test_intword_rounding_no_cross():
    assert intword(1500) == "1.5 thousand"


def test_intword_largest_ordinal_googol():
    assert intword(10**100) == "1.0 googol"
    assert intword(-(10**100)) == "-1.0 googol"


def test_intword_custom_format():
    assert intword(1500, format="%.0f") == "2 thousand"
    assert intword(1234, format="%.2f") == "1.23 thousand"


def test_intword_custom_format_rounding_cross():
    assert intword(999_500, format="%.0f") == "1 million"


def test_intword_float_input_truncated():
    assert intword(1500.9) == "1.5 thousand"
    assert intword(-1500.9) == "-1.5 thousand"


def test_intword_bool_input():
    # bool is int subclass; True -> 1
    assert intword(True) == "1"
    assert intword(False) == "0"


def test_intword_negative_zero_float():
    assert intword(-0.0) == "0"


def test_intword_large_value_above_googol():
    assert intword(10**101) == "10.0 googol" or intword(10**101).endswith("googol")


def test_intword_value_between_units():
    assert intword(1_234_567) == "1.2 million"
    assert intword(2_500_000) == "2.5 million"


def test_intword_exact_boundary_round_up():
    # 999_999 rounds to 1000.0 thousand -> 1.0 million
    assert intword(999_999) == "1.0 million"


def test_intword_type_error_object():
    class Bad:
        def __float__(self):
            raise TypeError("bad")

        def __int__(self):
            raise TypeError("bad")

    assert intword(Bad()) == str(Bad()) or isinstance(intword(Bad()), str)


def test_intword_value_error():
    class Bad:
        def __float__(self):
            raise ValueError("bad")

        def __int__(self):
            raise ValueError("bad")

    result = intword(Bad())
    assert isinstance(result, str)
