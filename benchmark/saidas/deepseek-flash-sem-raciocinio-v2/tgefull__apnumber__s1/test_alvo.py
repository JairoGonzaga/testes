import math

import pytest

from alvo import _APNUMBER_WORDS, _format_not_finite, apnumber


WORDS = ["zero", "one", "two", "three", "four",
         "five", "six", "seven", "eight", "nine"]


def test_words_constant():
    assert _APNUMBER_WORDS == tuple(WORDS)


@pytest.mark.parametrize("n,expected", list(enumerate(WORDS)))
def test_ints_in_range(n, expected):
    assert apnumber(n) == expected


@pytest.mark.parametrize("n,expected", list(enumerate(WORDS)))
def test_floats_in_range(n, expected):
    assert apnumber(float(n)) == expected


@pytest.mark.parametrize("n,expected", [(0.0, "zero"), (0.9, "zero"),
                                        (1.9, "one"), (9.999, "nine"),
                                        (-0.5, "zero"),
                                        (2.5, "two")])
def test_float_truncation(n, expected):
    assert apnumber(n) == expected


@pytest.mark.parametrize("n,expected", [(10, "10"), (11, "11"), (100, "100"),
                                        (-1, "-1"), (-10, "-10")])
def test_ints_out_of_range(n, expected):
    assert apnumber(n) == expected


@pytest.mark.parametrize("n,expected", [(10.0, "10"), (10.7, "10"),
                                        (-1.0, "-1"), (-1.9, "-1")])
def test_floats_out_of_range(n, expected):
    assert apnumber(n) == expected


@pytest.mark.parametrize("n,expected", [("0", "zero"), ("3", "three"),
                                        ("9", "nine"), (" 3 ", "three"),
                                        ("5", "five")])
def test_numeric_strings(n, expected):
    assert apnumber(n) == expected


@pytest.mark.parametrize("n,expected", [("10", "10"), ("-2", "-2"),
                                        ("15", "15")])
def test_numeric_strings_out_of_range(n, expected):
    assert apnumber(n) == expected


@pytest.mark.parametrize("value,expected", [("5.0", "5.0"), ("3.9", "3.9"),
                                            ("abc", "abc"), ("", ""),
                                            (None, "None")])
def test_unconvertible_values_return_str(value, expected):
    assert apnumber(value) == expected


def test_list_returns_str():
    assert apnumber([]) == "[]"


def test_object_returns_str():
    obj = object()
    assert apnumber(obj) == str(obj)


def test_bad_float_value_error():
    class Bad:
        def __float__(self):
            raise ValueError("boom")

        def __str__(self):
            return "bad"

    assert apnumber(Bad()) == "bad"


def test_only_str_object():
    class OnlyStr:
        def __str__(self):
            return "onlystr"

    assert apnumber(OnlyStr()) == "onlystr"


def test_bool_values():
    assert apnumber(True) == "one"
    assert apnumber(False) == "zero"


def test_bytes_value():
    assert apnumber(b"5") == "five"


def test_nan():
    assert apnumber(float("nan")) == "NaN"


def test_positive_inf():
    assert apnumber(float("inf")) == "+Inf"


def test_negative_inf():
    assert apnumber(float("-inf")) == "-Inf"


def test_string_inf():
    assert apnumber("inf") == "+Inf"
    assert apnumber("-inf") == "-Inf"
    assert apnumber("nan") == "NaN"


def test_overflow_to_inf():
    assert apnumber(1e400) == "+Inf"
    assert apnumber(-1e400) == "-Inf"


def test_format_not_finite_isnan():
    assert _format_not_finite(float("nan")) == "NaN"
    assert _format_not_finite(math.nan) == "NaN"


def test_format_not_finite_neg_inf():
    assert _format_not_finite(float("-inf")) == "-Inf"


def test_format_not_finite_pos_inf():
    assert _format_not_finite(float("inf")) == "+Inf"


def test_format_not_finite_finite():
    assert _format_not_finite(0.0) == ""
    assert _format_not_finite(5.0) == ""
    assert _format_not_finite(-3.5) == ""
