import math
from decimal import Decimal

import pytest

from alvo import _APNUMBER_WORDS, _format_not_finite, apnumber


# ---------------------------------------------------------------------------
# Module constant
# ---------------------------------------------------------------------------

def test_words_tuple_is_exact_and_ordered():
    assert _APNUMBER_WORDS == (
        "zero", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine",
    )
    assert isinstance(_APNUMBER_WORDS, tuple)
    assert len(_APNUMBER_WORDS) == 10


# ---------------------------------------------------------------------------
# _format_not_finite
# ---------------------------------------------------------------------------

def test_format_not_finite_nan():
    assert _format_not_finite(math.nan) == "NaN"


def test_format_not_finite_negative_infinity():
    assert _format_not_finite(-math.inf) == "-Inf"


def test_format_not_finite_positive_infinity():
    assert _format_not_finite(math.inf) == "+Inf"


@pytest.mark.parametrize("value", [0.0, -0.0, 1.0, -1.0, 3.5, 1e308, -1e308])
def test_format_not_finite_returns_empty_string_for_finite_values(value):
    assert _format_not_finite(value) == ""


# ---------------------------------------------------------------------------
# apnumber: integers in the 0..9 range map to words
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("number", "word"),
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
def test_single_digit_integers_become_words(number, word):
    result = apnumber(number)
    assert result == word
    assert isinstance(result, str)


def test_every_word_in_range_is_reached_in_order():
    assert [apnumber(i) for i in range(10)] == list(_APNUMBER_WORDS)


def test_boundary_nine_is_word_and_ten_is_numeric():
    assert apnumber(9) == "nine"
    assert apnumber(10) == "10"


def test_boundary_zero_is_word_and_minus_one_is_numeric():
    assert apnumber(0) == "zero"
    assert apnumber(-1) == "-1"


@pytest.mark.parametrize("number", [10, 11, 12, 42, 100, 999])
def test_integers_at_or_above_ten_stay_numeric(number):
    assert apnumber(number) == str(number)


@pytest.mark.parametrize("number", [-2, -9, -10, -100])
def test_negative_integers_stay_numeric(number):
    assert apnumber(number) == str(number)


def test_large_integer_within_float_range_stays_numeric():
    big = 10 ** 20
    assert apnumber(big) == str(big)
    assert apnumber(big) == "100000000000000000000"


def test_large_float_outside_word_range_returns_integer_text():
    assert apnumber(1e308) == str(int(1e308))


# ---------------------------------------------------------------------------
# apnumber: floats
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("number", "word"),
    [(0.0, "zero"), (1.0, "one"), (5.0, "five"), (9.0, "nine")],
)
def test_integral_floats_in_range_become_words(number, word):
    assert apnumber(number) == word


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (1.5, "one"),
        (9.99, "nine"),
        (0.999, "zero"),
        (-0.5, "zero"),
        (-0.999, "zero"),
        (-1.5, "-1"),
    ],
)
def test_fractional_floats_are_truncated_toward_zero(number, expected):
    assert apnumber(number) == expected


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (10.0, "10"),
        (10.5, "10"),
        (10.999, "10"),
        (12.7, "12"),
        (-2.0, "-2"),
    ],
)
def test_out_of_range_floats_return_truncated_integer_text(number, expected):
    # The original value is replaced by its int() before str() is applied,
    # so the result is the integer text, never the float text.
    assert apnumber(number) == expected


def test_negative_zero_is_zero():
    assert apnumber(-0.0) == "zero"


def test_bool_values_follow_integer_semantics():
    assert apnumber(True) == "one"
    assert apnumber(False) == "zero"


def test_nan_float_is_formatted_as_nan():
    assert apnumber(math.nan) == "NaN"


def test_positive_infinity_float_is_formatted_as_plus_inf():
    assert apnumber(math.inf) == "+Inf"


def test_negative_infinity_float_is_formatted_as_minus_inf():
    assert apnumber(-math.inf) == "-Inf"


# ---------------------------------------------------------------------------
# apnumber: strings
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("text", "word"),
    [
        ("0", "zero"),
        ("3", "three"),
        ("9", "nine"),
        (" 4 ", "four"),
        ("+5", "five"),
        ("-0", "zero"),
    ],
)
def test_numeric_strings_in_range_become_words(text, word):
    assert apnumber(text) == word


@pytest.mark.parametrize(
    ("text", "expected"),
    [("10", "10"), ("42", "42"), ("-3", "-3")],
)
def test_numeric_strings_out_of_range_return_integer_text(text, expected):
    assert apnumber(text) == expected


@pytest.mark.parametrize("text", ["3.5", "2.0", "1e3"])
def test_numeric_strings_rejected_by_int_are_returned_unchanged(text):
    # float() accepts these, but int() does not, so the ValueError path
    # returns the original string.
    assert apnumber(text) == text


@pytest.mark.parametrize("text", ["abc", "", "   ", "0x1", "three", "1,5"])
def test_non_numeric_strings_are_returned_unchanged(text):
    assert apnumber(text) == text


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("nan", "NaN"),
        ("NaN", "NaN"),
        ("inf", "+Inf"),
        ("+inf", "+Inf"),
        ("Infinity", "+Inf"),
        ("-inf", "-Inf"),
        ("-Infinity", "-Inf"),
        ("1e400", "+Inf"),
        ("-1e400", "-Inf"),
    ],
)
def test_non_finite_strings_are_formatted(text, expected):
    assert apnumber(text) == expected


# ---------------------------------------------------------------------------
# apnumber: Decimal and custom numeric protocols
# ---------------------------------------------------------------------------

def test_decimal_in_range_becomes_word():
    assert apnumber(Decimal("7")) == "seven"


def test_decimal_fraction_is_truncated():
    assert apnumber(Decimal("12.5")) == "12"


def test_decimal_nan_and_infinities():
    assert apnumber(Decimal("NaN")) == "NaN"
    assert apnumber(Decimal("Infinity")) == "+Inf"
    assert apnumber(Decimal("-Infinity")) == "-Inf"


class _Numeric:
    """Object exposing both __float__ and __int__, like a numeric type."""

    def __init__(self, number):
        self.number = number

    def __float__(self):
        return float(self.number)

    def __int__(self):
        return int(self.number)

    def __str__(self):
        return f"numeric({self.number})"


def test_custom_numeric_type_uses_float_and_int_protocols():
    assert apnumber(_Numeric(4)) == "four"
    assert apnumber(_Numeric(4.9)) == "four"
    assert apnumber(_Numeric(11)) == "11"


class _FloatOnly:
    """Supports float() but not int(); the int() TypeError is handled."""

    def __float__(self):
        return 3.0

    def __str__(self):
        return "float-only"


def test_object_with_only_float_protocol_falls_back_to_str():
    assert apnumber(_FloatOnly()) == "float-only"


class _Infinite:
    def __float__(self):
        return float("-inf")


def test_custom_float_returning_infinity_is_formatted():
    assert apnumber(_Infinite()) == "-Inf"


class _NoFloat:
    def __str__(self):
        return "no-float"


def test_object_without_float_protocol_returns_its_str():
    assert apnumber(_NoFloat()) == "no-float"


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, "None"),
        ([], "[]"),
        ([1, 2], "[1, 2]"),
        ({}, "{}"),
        ((1,), "(1,)"),
    ],
)
def test_unsupported_container_and_none_return_str_of_value(value, expected):
    assert apnumber(value) == expected


def test_arbitrary_object_returns_its_str():
    sentinel = object()
    assert apnumber(sentinel) == str(sentinel)


# ---------------------------------------------------------------------------
# apnumber: exceptions that are not caught by the handler
# ---------------------------------------------------------------------------

class _Exploding:
    def __float__(self):
        raise RuntimeError("boom")


def test_unexpected_exception_from_float_propagates():
    with pytest.raises(RuntimeError, match="boom"):
        apnumber(_Exploding())


class _FloatOkIntExplodes:
    def __float__(self):
        return 2.0

    def __int__(self):
        raise KeyError("no-int")


def test_unexpected_exception_from_int_propagates():
    with pytest.raises(KeyError):
        apnumber(_FloatOkIntExplodes())


def test_integer_too_large_for_float_propagates_overflow_error():
    # float(10 ** 400) raises OverflowError, which the handler does not catch.
    with pytest.raises(OverflowError):
        apnumber(10 ** 400)
    with pytest.raises(OverflowError):
        apnumber(-(10 ** 400))


# ---------------------------------------------------------------------------
# apnumber: type invariants
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value",
    [0, 9, 10, -1, 2.5, "x", None, math.nan, math.inf, True, Decimal("3")],
)
def test_result_is_always_a_string(value):
    assert isinstance(apnumber(value), str)
