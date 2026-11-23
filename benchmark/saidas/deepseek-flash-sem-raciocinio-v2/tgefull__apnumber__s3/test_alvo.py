import math
import pytest

from alvo import apnumber, _format_not_finite, _APNUMBER_WORDS


def test_word_table():
    assert _APNUMBER_WORDS == (
        "zero", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine",
    )


@pytest.mark.parametrize("value, expected", [
    (0, "zero"),
    (1, "one"),
    (2, "two"),
    (3, "three"),
    (4, "four"),
    (5, "five"),
    (6, "six"),
    (7, "seven"),
    (8, "eight"),
    (9, "nine"),
])
def test_single_digits(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize("value, expected", [
    (10, "10"),
    (11, "11"),
    (-1, "-1"),
    (100, "100"),
    (10 ** 30, "1000000000000000000000000000000"),
])
def test_out_of_range_integers_return_str(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize("value, expected", [
    (3.7, "three"),
    (9.99, "nine"),
    (0.5, "zero"),
    (2.0, "two"),
    (-0.0, "zero"),
    (10.0, "10"),
    (-2.5, "-2"),
    (9.5, "nine"),
])
def test_floats_are_truncated(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize("value, expected", [
    ("5", "five"),
    ("0", "zero"),
    ("10", "10"),
    ("-3", "-3"),
    ("3.9", "3.9"),
    ("abc", "abc"),
    ("", ""),
])
def test_strings(value, expected):
    assert apnumber(value) == expected


def test_bool_values():
    assert apnumber(True) == "one"
    assert apnumber(False) == "zero"


@pytest.mark.parametrize("value, expected", [
    (float("nan"), "NaN"),
    (float("inf"), "+Inf"),
    (float("-inf"), "-Inf"),
    ("nan", "NaN"),
    ("inf", "+Inf"),
    ("-inf", "-Inf"),
    (float("1e400"), "+Inf"),
])
def test_non_finite_values(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize("value, expected", [
    (None, "None"),
    (complex(1, 2), "(1+2j)"),
    ([1, 2], "[1, 2]"),
    ((2,), "(2,)"),
    ({"a": 1}, "{'a': 1}"),
])
def test_unconvertible_values_return_str(value, expected):
    assert apnumber(value) == expected


def test_bytes_value():
    assert apnumber(b"3") == "three"


def test_format_not_finite_nan():
    assert _format_not_finite(float("nan")) == "NaN"


def test_format_not_finite_negative_inf():
    assert _format_not_finite(float("-inf")) == "-Inf"


def test_format_not_finite_positive_inf():
    assert _format_not_finite(float("inf")) == "+Inf"


def test_format_not_finite_finite_falls_through():
    assert _format_not_finite(0.0) == ""
    assert _format_not_finite(1.5) == ""
    assert _format_not_finite(-3.0) == ""
