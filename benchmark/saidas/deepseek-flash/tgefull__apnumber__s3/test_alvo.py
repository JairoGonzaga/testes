import math
from decimal import Decimal

import pytest

from alvo import _APNUMBER_WORDS, _format_not_finite, apnumber


def test_apnumber_words_constant():
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
    "value, expected",
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
def test_apnumber_single_digit_integers(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value",
    [-100, -10, -2, -1, 10, 11, 100, 10**20],
)
def test_apnumber_integers_outside_single_digit_range(value):
    assert apnumber(value) == str(value)


@pytest.mark.parametrize(
    "value, expected",
    [
        (0.0, "zero"),
        (0.1, "zero"),
        (0.9, "zero"),
        (-0.0, "zero"),
        (-0.1, "zero"),
        (-0.9, "zero"),
        (1.0, "one"),
        (1.1, "one"),
        (1.9, "one"),
        (2.5, "two"),
        (8.5, "eight"),
        (9.0, "nine"),
        (9.9, "nine"),
        (-1.0, "-1"),
        (-1.1, "-1"),
        (-1.9, "-1"),
        (-9.9, "-9"),
        (-10.9, "-10"),
        (10.0, "10"),
        (10.1, "10"),
        (10.9, "10"),
        (100.5, "100"),
    ],
)
def test_apnumber_floats_truncate_toward_zero_then_format_integer(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (math.nan, "NaN"),
        (math.inf, "+Inf"),
        (-math.inf, "-Inf"),
    ],
)
def test_apnumber_non_finite_floats(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("nan", "NaN"),
        ("NaN", "NaN"),
        ("NAN", "NaN"),
        ("inf", "+Inf"),
        ("+inf", "+Inf"),
        ("Infinity", "+Inf"),
        ("+Infinity", "+Inf"),
        ("-inf", "-Inf"),
        ("-Infinity", "-Inf"),
    ],
)
def test_apnumber_non_finite_numeric_strings(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("0", "zero"),
        ("00", "zero"),
        ("+0", "zero"),
        ("-0", "zero"),
        ("1", "one"),
        ("9", "nine"),
        (" 4 ", "four"),
        ("+3", "three"),
        ("10", "10"),
        ("-1", "-1"),
        ("0010", "10"),
        ("-01", "-1"),
    ],
)
def test_apnumber_finite_integer_strings(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("1.0", "1.0"),
        ("3.7", "3.7"),
        ("9.9", "9.9"),
        ("10.0", "10.0"),
        ("-0.0", "-0.0"),
        ("+4.5", "+4.5"),
        ("1e3", "1e3"),
        ("1E3", "1E3"),
        (" 4.5 ", " 4.5 "),
    ],
)
def test_apnumber_finite_strings_that_int_cannot_parse_return_original(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value",
    ["", " ", "abc", "one", "10x", "3.7.1", "1,000"],
)
def test_apnumber_invalid_strings_return_original_string(value):
    assert apnumber(value) == str(value)


@pytest.mark.parametrize(
    "value",
    [
        None,
        [1, 2],
        (1, 2),
        {"a": 1},
        1 + 2j,
        b"not a number",
    ],
)
def test_apnumber_unconvertible_values_return_str(value):
    assert apnumber(value) == str(value)


def test_apnumber_arbitrary_object_returns_str():
    value = object()
    assert apnumber(value) == str(value)


@pytest.mark.parametrize(
    "value, expected",
    [
        (True, "one"),
        (False, "zero"),
    ],
)
def test_apnumber_booleans(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (Decimal("0"), "zero"),
        (Decimal("9"), "nine"),
        (Decimal("9.9"), "nine"),
        (Decimal("-0.1"), "zero"),
        (Decimal("-1.2"), "-1"),
        (Decimal("10"), "10"),
        (Decimal("NaN"), "NaN"),
        (Decimal("Infinity"), "+Inf"),
        (Decimal("-Infinity"), "-Inf"),
    ],
)
def test_apnumber_decimal_values(value, expected):
    assert apnumber(value) == expected


class _FloatOnly:
    def __float__(self):
        return 3.0

    def __str__(self):
        return "float-only"


class _IntDifferentFromFloat:
    def __float__(self):
        return 2.0

    def __int__(self):
        return 7

    def __str__(self):
        return "int-different"


class _NonFiniteObject:
    def __float__(self):
        return float("-inf")

    def __str__(self):
        return "non-finite"


def test_apnumber_float_only_object_raises_type_error_on_int_and_returns_str():
    value = _FloatOnly()
    assert apnumber(value) == "float-only"


def test_apnumber_uses_int_of_original_object_not_int_of_float():
    assert apnumber(_IntDifferentFromFloat()) == "seven"


def test_apnumber_object_whose_float_is_non_finite():
    assert apnumber(_NonFiniteObject()) == "-Inf"


def test_apnumber_huge_integer_float_overflow_propagates():
    with pytest.raises(OverflowError):
        apnumber(10**400)


@pytest.mark.parametrize(
    "value, expected",
    [
        (math.nan, "NaN"),
        (math.inf, "+Inf"),
        (-math.inf, "-Inf"),
    ],
)
def test_format_not_finite(value, expected):
    assert _format_not_finite(value) == expected


@pytest.mark.parametrize(
    "value",
    [0.0, -0.0, 1.0, -1.0, 1e300, -1e300],
)
def test_format_not_finite_returns_empty_string_for_finite_values(value):
    assert _format_not_finite(value) == ""
