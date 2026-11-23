import math

import pytest

from alvo import _APNUMBER_WORDS, _format_not_finite, apnumber


WORDS = ("zero", "one", "two", "three", "four",
         "five", "six", "seven", "eight", "nine")


def test_words_table():
    assert _APNUMBER_WORDS == WORDS


# --- _format_not_finite -------------------------------------------------

def test_format_not_finite_nan():
    assert _format_not_finite(float("nan")) == "NaN"


def test_format_not_finite_neg_inf():
    assert _format_not_finite(float("-inf")) == "-Inf"


def test_format_not_finite_pos_inf():
    assert _format_not_finite(float("inf")) == "+Inf"


def test_format_not_finite_finite():
    assert _format_not_finite(0.0) == ""
    assert _format_not_finite(3.5) == ""
    assert _format_not_finite(-7.0) == ""


# --- apnumber: normal ints ---------------------------------------------

@pytest.mark.parametrize("n,expected", list(enumerate(WORDS)))
def test_apnumber_zero_to_nine(n, expected):
    assert apnumber(n) == expected


# --- apnumber: floats truncate towards zero ----------------------------

@pytest.mark.parametrize("value,expected", [
    (0.0, "zero"),
    (0.9, "zero"),
    (1.0, "one"),
    (2.99, "two"),
    (3.5, "three"),
    (9.999, "nine"),
    (10.0, "10"),
])
def test_apnumber_floats(value, expected):
    assert apnumber(value) == expected


def test_apnumber_negative_float_truncates_toward_zero():
    assert apnumber(-0.5) == "zero"
    assert apnumber(-0.99999) == "zero"


# --- apnumber: negative and large ints ---------------------------------

@pytest.mark.parametrize("n", [-1, -10, -1000])
def test_apnumber_negative_returns_str(n):
    assert apnumber(n) == str(n)


@pytest.mark.parametrize("n", [10, 11, 99, 1000, 10 ** 20])
def test_apnumber_big_returns_str(n):
    assert apnumber(n) == str(n)


# --- apnumber: non-finite -------------------------------------------------

def test_apnumber_nan():
    assert apnumber(float("nan")) == "NaN"


def test_apnumber_pos_inf():
    assert apnumber(float("inf")) == "+Inf"


def test_apnumber_neg_inf():
    assert apnumber(float("-inf")) == "-Inf"


def test_apnumber_huge_float_is_inf():
    assert apnumber(1e400) == "+Inf"
    assert apnumber(-1e400) == "-Inf"


def test_apnumber_nan_string():
    assert apnumber("nan") == "NaN"


def test_apnumber_inf_string():
    assert apnumber("inf") == "+Inf"
    assert apnumber("-inf") == "-Inf"


class _FloatNaN:
    def __float__(self):
        return float("nan")


def test_apnumber_object_float_nan():
    assert apnumber(_FloatNaN()) == "NaN"


# --- apnumber: strings ----------------------------------------------------

@pytest.mark.parametrize("value,expected", [
    ("4", "four"),
    ("0", "zero"),
    ("9", "nine"),
    ("10", "10"),
    ("-1", "-1"),
])
def test_apnumber_numeric_strings(value, expected):
    assert apnumber(value) == expected


def test_apnumber_non_numeric_string():
    assert apnumber("abc") == "abc"
    assert apnumber("") == ""


def test_apnumber_float_string_without_decimal_point():
    # int("3.9") raises ValueError -> the string itself is returned
    assert apnumber("3.9") == "3.9"


def test_apnumber_whitespace_string_padded():
    assert apnumber(" 5 ") == "five"


# --- apnumber: booleans ---------------------------------------------------

def test_apnumber_bools():
    assert apnumber(True) == "one"
    assert apnumber(False) == "zero"


# --- apnumber: unconvertible objects -------------------------------------

def test_apnumber_none():
    assert apnumber(None) == "None"


def test_apnumber_list():
    value = [1, 2]
    assert apnumber(value) == str(value)


def test_apnumber_complex():
    value = complex(1, 2)
    assert apnumber(value) == str(value)


class _NoFloat:
    def __str__(self):
        return "custom-str"


def test_apnumber_unconvertible_object_uses_str():
    assert apnumber(_NoFloat()) == "custom-str"


class _BadFloat:
    def __float__(self):
        raise ValueError("nope")


def test_apnumber_float_raising_value_error():
    assert apnumber(_BadFloat()).startswith("<")


class _TypeErrFloat:
    def __float__(self):
        raise TypeError("nope")


def test_apnumber_float_raising_type_error():
    assert apnumber(_TypeErrFloat()).startswith("<")
