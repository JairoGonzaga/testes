import math

import pytest

import alvo
from alvo import intword, _format_not_finite, powers, human_powers


# ---------------------------------------------------------------- module data

def test_powers_and_human_powers_content():
    assert powers == [
        10**3, 10**6, 10**9, 10**12, 10**15, 10**18,
        10**21, 10**24, 10**27, 10**30, 10**33, 10**100,
    ]
    assert human_powers == (
        "thousand", "million", "billion", "trillion", "quadrillion",
        "quintillion", "sextillion", "septillion", "octillion", "nonillion",
        "decillion", "googol",
    )
    assert len(powers) == len(human_powers) == 12


# ------------------------------------------------------------ _format_not_finite

def test_format_not_finite_nan():
    assert _format_not_finite(float("nan")) == "NaN"


def test_format_not_finite_negative_inf():
    assert _format_not_finite(float("-inf")) == "-Inf"


def test_format_not_finite_positive_inf():
    assert _format_not_finite(float("inf")) == "+Inf"


def test_format_not_finite_finite_returns_empty():
    assert _format_not_finite(1.5) == ""
    assert _format_not_finite(0.0) == ""
    assert _format_not_finite(-3.0) == ""


# ------------------------------------------------------------- non finite input

def test_intword_nan():
    assert intword(float("nan")) == "NaN"


def test_intword_positive_inf():
    assert intword(float("inf")) == "+Inf"


def test_intword_negative_inf():
    assert intword(float("-inf")) == "-Inf"


def test_intword_nan_string():
    assert intword("nan") == "NaN"


def test_intword_inf_string():
    assert intword("inf") == "+Inf"


def test_intword_negative_inf_string():
    assert intword("-inf") == "-Inf"


# ------------------------------------------------------------- invalid input

def test_intword_invalid_string_returns_str():
    assert intword("abc") == "abc"


def test_intword_float_like_string_returns_str():
    assert intword("1e6") == "1e6"


def test_intword_none_returns_str():
    assert intword(None) == "None"


def test_intword_list_returns_str():
    assert intword([1, 2]) == "[1, 2]"


# ------------------------------------------------------------- small numbers

def test_intword_zero():
    assert intword(0) == "0"


def test_intword_one():
    assert intword(1) == "1"


def test_intword_below_thousand():
    assert intword(999) == "999"


def test_intword_negative_below_thousand():
    assert intword(-999) == "-999"


def test_intword_negative_zero():
    assert intword(-0) == "0"


# ------------------------------------------------------------- thousands

def test_intword_exactly_one_thousand():
    assert intword(1000) == "1.0 thousand"


def test_intword_1234():
    assert intword(1234) == "1.2 thousand"


def test_intword_negative_1234():
    assert intword(-1234) == "-1.2 thousand"


def test_intword_1500():
    assert intword(1500) == "1.5 thousand"


def test_intword_rounded_down_thousand():
    assert intword(1449) == "1.4 thousand"


# ------------------------------------------------------------- millions

def test_intword_one_million():
    assert intword(1000000) == "1.0 million"


def test_intword_1500000():
    assert intword(1500000) == "1.5 million"


def test_intword_negative_million():
    assert intword(-1500000) == "-1.5 million"


def test_intword_half_million():
    assert intword(500000) == "500.0 thousand"


# --------------------------------------------------------------- rollover

def test_intword_999999_rolls_to_million():
    assert intword(999999) == "1.0 million"


def test_intword_999950_rolls_to_million():
    assert intword(999950) == "1.0 million"


def test_intword_999949_no_rollover():
    assert intword(999949) == "999.9 thousand"


def test_intword_999999999_rolls_to_billion():
    assert intword(999999999) == "1.0 billion"


def test_intword_negative_rollover():
    assert intword(-999999) == "-1.0 million"


# ----------------------------------------------------------- larger units

def test_intword_billion():
    assert intword(10**9) == "1.0 billion"


def test_intword_trillion():
    assert intword(10**12) == "1.0 trillion"


def test_intword_quadrillion():
    assert intword(10**15) == "1.0 quadrillion"


def test_intword_quintillion():
    assert intword(10**18) == "1.0 quintillion"


def test_intword_sextillion():
    assert intword(10**21) == "1.0 sextillion"


def test_intword_septillion():
    assert intword(10**24) == "1.0 septillion"


def test_intword_octillion():
    assert intword(10**27) == "1.0 octillion"


def test_intword_nonillion():
    assert intword(10**30) == "1.0 nonillion"


def test_intword_decillion():
    assert intword(10**33) == "1.0 decillion"


def test_intword_quintillion_rollover():
    assert intword(999999999999999999) == "1.0 quintillion"


# ------------------------------------------------------------- largest unit

def test_intword_googol():
    assert intword(10**100) == "1.0 googol"


def test_intword_above_googol():
    assert intword(10**101) == "10.0 googol"


def test_intword_negative_googol():
    assert intword(-10**100) == "-1.0 googol"


def test_intword_just_below_googol_is_decillion():
    # 10**99 lies in the decillion range; the huge value is formatted from
    # the float division, so just check the unit and the shape of the result.
    out = intword(10**99)
    assert out.endswith(" decillion")
    head, _, tail = out.partition(".")
    assert head.isdigit()
    assert len(tail) == len("0 decillion")
    assert tail.endswith("0 decillion")


# ------------------------------------------------------------- custom format

def test_intword_custom_format_whole_thousand():
    assert intword(1234, "%.0f") == "1 thousand"


def test_intword_custom_format_rounds_up():
    assert intword(1500, "%.0f") == "2 thousand"


def test_intword_custom_format_rollover():
    assert intword(999999, "%.0f") == "1 million"


def test_intword_custom_format_million():
    assert intword(1234567, "%.2f") == "1.23 million"


def test_intword_custom_format_small_number_ignores_format():
    assert intword(7, "%.0f") == "7"


def test_intword_custom_format_negative():
    assert intword(-1234, "%.0f") == "-1 thousand"


# ------------------------------------------------------------- misc input types

def test_intword_true():
    assert intword(True) == "1"


def test_intword_float_truncates():
    assert intword(1.9) == "1"


def test_intword_float_truncates_thousand():
    assert intword(1999.9) == "2.0 thousand"


def test_intword_numeric_string():
    assert intword("1500") == "1.5 thousand"


def test_intword_numeric_string_negative():
    assert intword("-1500") == "-1.5 thousand"


@pytest.mark.parametrize("exponent,unit", list(zip(
    [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33], human_powers[:-1])))
def test_intword_all_units(exponent, unit):
    assert intword(10**exponent) == f"1.0 {unit}"
