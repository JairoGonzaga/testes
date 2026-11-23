import math
from decimal import Decimal
from fractions import Fraction

import pytest

from alvo import _APNUMBER_WORDS, _format_not_finite, apnumber

WORDS = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")


class _Both:
    """Converts with both float() and int(), like a numeric type would."""

    def __float__(self):
        return 4.0

    def __int__(self):
        return 4


class _NanLike:
    def __float__(self):
        return math.nan


class _Unconvertible:
    def __str__(self):
        return "unconvertible"


class _FloatRaises:
    def __float__(self):
        raise ValueError("no float here")

    def __str__(self):
        return "float-raises"


# ---------------------------------------------------------------------------
# Word table
# ---------------------------------------------------------------------------

def test_words_table_holds_the_ten_digit_names_in_order():
    assert isinstance(_APNUMBER_WORDS, tuple)
    assert _APNUMBER_WORDS == WORDS


# ---------------------------------------------------------------------------
# In-range and out-of-range integers
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("digit", range(10))
def test_each_single_digit_int_is_spelled_out(digit):
    assert apnumber(digit) == WORDS[digit]


def test_zero_is_the_lower_bound_of_the_word_range():
    assert apnumber(0) == "zero"


def test_nine_is_the_upper_bound_of_the_word_range():
    assert apnumber(9) == "nine"


@pytest.mark.parametrize("value", [10, 11, 12, 19, 99, 100, 1000])
def test_ints_from_ten_upwards_are_returned_as_digits(value):
    result = apnumber(value)
    assert isinstance(result, str)
    assert result == str(value)


@pytest.mark.parametrize("value", [-1, -2, -9, -10, -100])
def test_negative_ints_are_returned_as_digits(value):
    result = apnumber(value)
    assert isinstance(result, str)
    assert result == str(value)


def test_large_int_is_returned_exactly():
    assert apnumber(10 ** 20 + 7) == str(10 ** 20 + 7)
    assert apnumber(2 ** 53 + 1) == "9007199254740993"


def test_bools_behave_as_their_integer_values():
    assert apnumber(True) == "one"
    assert apnumber(False) == "zero"


# ---------------------------------------------------------------------------
# Floats: finite values are truncated toward zero before the range check
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (0.0, "zero"),
        (-0.0, "zero"),
        (3.0, "three"),
        (3.7, "three"),
        (9.0, "nine"),
        (9.999, "nine"),
        (0.5, "zero"),
        (-0.5, "zero"),
        (10.0, "10"),
        (10.5, "10"),
        (-1.5, "-1"),
        (-9.5, "-9"),
    ],
)
def test_floats_are_truncated_toward_zero_before_lookup(value, expected):
    assert apnumber(value) == expected


def test_large_finite_float_is_returned_as_full_integer_digits():
    assert apnumber(1e16) == "10000000000000000"
    assert apnumber(1e300) == str(int(1e300))


# ---------------------------------------------------------------------------
# Non-finite floats
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (math.nan, "NaN"),
        (float("nan"), "NaN"),
        (math.inf, "+Inf"),
        (float("inf"), "+Inf"),
        (-math.inf, "-Inf"),
        (float("-inf"), "-Inf"),
    ],
)
def test_non_finite_floats_are_reported_not_spelled(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (Decimal("NaN"), "NaN"),
        (Decimal("Infinity"), "+Inf"),
        (Decimal("-Infinity"), "-Inf"),
    ],
)
def test_decimal_non_finite_values_are_reported(value, expected):
    assert apnumber(value) == expected


def test_nan_like_object_reports_nan():
    assert apnumber(_NanLike()) == "NaN"


# ---------------------------------------------------------------------------
# Other numeric types
# ---------------------------------------------------------------------------

def test_decimal_and_fraction_inputs_are_converted_like_numbers():
    assert apnumber(Decimal("3")) == "three"
    assert apnumber(Decimal("12")) == "12"
    assert apnumber(Decimal("-2")) == "-2"
    assert apnumber(Fraction(19, 2)) == "nine"
    assert apnumber(Fraction(21, 2)) == "10"


def test_object_providing_float_and_int_is_spelled_out():
    assert apnumber(_Both()) == "four"


# ---------------------------------------------------------------------------
# Huge integers overflow float() and the error is not caught
# ---------------------------------------------------------------------------

def test_huge_int_that_overflows_float_propagates_overflow_error():
    with pytest.raises(OverflowError):
        apnumber(10 ** 400)
    with pytest.raises(OverflowError):
        apnumber(-(10 ** 400))


# ---------------------------------------------------------------------------
# Strings
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "text, expected",
    [
        ("0", "zero"),
        ("-0", "zero"),
        ("+0", "zero"),
        ("1", "one"),
        ("9", "nine"),
        ("03", "three"),
        (" 7 ", "seven"),
        ("+5", "five"),
    ],
)
def test_integer_strings_in_range_are_spelled_out(text, expected):
    assert apnumber(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("10", "10"),
        ("010", "10"),
        ("-3", "-3"),
        ("-03", "-3"),
        ("12345678901234567890", "12345678901234567890"),
    ],
)
def test_integer_strings_out_of_range_are_returned_as_normalised_digits(text, expected):
    assert apnumber(text) == expected


@pytest.mark.parametrize("text", ["3.5", "3.0", "1e1", "0.0", "-2.5", "10.0"])
def test_decimal_notation_strings_are_returned_unchanged(text):
    assert apnumber(text) == text


@pytest.mark.parametrize(
    "text, expected",
    [
        ("nan", "NaN"),
        ("NaN", "NaN"),
        ("+nan", "NaN"),
        ("inf", "+Inf"),
        ("+inf", "+Inf"),
        ("Infinity", "+Inf"),
        ("-inf", "-Inf"),
        ("-INFINITY", "-Inf"),
        (" -inf ", "-Inf"),
        ("1e400", "+Inf"),
        ("-1e400", "-Inf"),
    ],
)
def test_strings_that_parse_to_non_finite_floats_are_reported(text, expected):
    assert apnumber(text) == expected


@pytest.mark.parametrize(
    "text", ["", " ", "abc", "three", "0x3", "1,5", "12abc", "--3"]
)
def test_non_numeric_strings_are_returned_unchanged(text):
    assert apnumber(text) == text


# ---------------------------------------------------------------------------
# Non-numeric values fall back to str()
# ---------------------------------------------------------------------------

def test_none_falls_back_to_str():
    result = apnumber(None)
    assert isinstance(result, str)
    assert result == "None"


@pytest.mark.parametrize(
    "value, expected",
    [
        ([], "[]"),
        ([1, 2], "[1, 2]"),
        ({}, "{}"),
        ((1,), "(1,)"),
    ],
)
def test_containers_fall_back_to_str(value, expected):
    assert apnumber(value) == expected


def test_unconvertible_object_falls_back_to_its_str():
    assert apnumber(_Unconvertible()) == "unconvertible"


def test_object_whose_float_raises_value_error_falls_back_to_str():
    assert apnumber(_FloatRaises()) == "float-raises"


# ---------------------------------------------------------------------------
# _format_not_finite helper
# ---------------------------------------------------------------------------

def test_format_not_finite_reports_nan():
    assert _format_not_finite(math.nan) == "NaN"


def test_format_not_finite_reports_negative_infinity():
    assert _format_not_finite(-math.inf) == "-Inf"


def test_format_not_finite_reports_positive_infinity():
    assert _format_not_finite(math.inf) == "+Inf"


@pytest.mark.parametrize("value", [0.0, -0.0, 1.0, -1.5, 1e308, -1e-308, 5e-324])
def test_format_not_finite_returns_empty_string_for_finite_values(value):
    assert _format_not_finite(value) == ""
