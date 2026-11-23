```python
import math

import pytest

from alvo import _APNUMBER_WORDS, _format_not_finite, apnumber


def test_apnumber_words_tuple():
    assert _APNUMBER_WORDS == (
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    )


@pytest.mark.parametrize(
    "value,expected",
    [
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
    ],
)
def test_apnumber_single_digits(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (0.0, "zero"),
        (1.0, "one"),
        (9.0, "nine"),
        (3.9, "three"),
        (9.99, "nine"),
        ("0", "zero"),
        ("7", "seven"),
        ("3.9", "three"),
    ],
)
def test_apnumber_integer_like_and_numeric_strings(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (-1, "-1"),
        (-100, "-100"),
        (10, "10"),
        (11, "11"),
        (1000, "1000"),
        (10.0, "10"),
        (99.5, "99"),
        ("10", "10"),
        ("42", "42"),
    ],
)
def test_apnumber_out_of_range(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (float("nan"), "NaN"),
        (float("-nan"), "NaN"),
        (float("inf"), "+Inf"),
        (float("-inf"), "-Inf"),
    ],
)
def test_apnumber_non_finite_floats(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("nan", "NaN"),
        ("inf", "+Inf"),
        ("-inf", "-Inf"),
        ("NaN", "NaN"),
        ("Infinity", "+Inf"),
        ("-Infinity", "-Inf"),
    ],
)
def test_apnumber_non_finite_strings(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value",
    ["abc", "hello", "", "1abc", None, object()],
)
def test_apnumber_non_numeric_values_fall_back_to_str(value):
    assert apnumber(value) == str(value)


def test_apnumber_none():
    assert apnumber(None) == "None"


def test_apnumber_boolean():
    assert apnumber(True) == "one"
    assert apnumber(False) == "zero"


def test_apnumber_complex_raises_string_conversion():
    value = 1 + 2j
    assert apnumber(value) == str(value)


def test_format_not_finite_nan():
    assert _format_not_finite(float("nan")) == "NaN"


def test_format_not_finite_positive_inf():
    assert _format_not_finite(float("inf")) == "+Inf"


def test_format_not_finite_negative_inf():
    assert _format_not_finite(float("-inf")) == "-Inf"


def test_format_not_finite_finite_returns_empty():
    assert _format_not_finite(0.0) == ""
    assert _format_not_finite(1.5) == ""
    assert _format_not_finite(-42.0) == ""
```