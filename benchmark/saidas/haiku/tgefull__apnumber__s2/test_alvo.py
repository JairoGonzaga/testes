import math
from decimal import Decimal

import pytest

from alvo import _APNUMBER_WORDS, _format_not_finite, apnumber

WORDS = ("zero", "one", "two", "three", "four",
         "five", "six", "seven", "eight", "nine")


class _Labelled:
    """Object that float() and int() both reject, so apnumber falls back to str()."""

    def __str__(self):
        return "custom label"


def reference(value):
    """Expected apnumber result for a finite value, from its truncated integer."""
    n = math.trunc(value)
    return _APNUMBER_WORDS[n] if 0 <= n <= 9 else str(n)


# ---------------------------------------------------------------------------
# Word table
# ---------------------------------------------------------------------------

def test_word_table_is_the_exact_tuple_of_zero_to_nine():
    assert isinstance(_APNUMBER_WORDS, tuple)
    assert _APNUMBER_WORDS == WORDS


# ---------------------------------------------------------------------------
# _format_not_finite
# ---------------------------------------------------------------------------

def test_format_not_finite_nan():
    assert _format_not_finite(math.nan) == "NaN"


def test_format_not_finite_negative_infinity():
    assert _format_not_finite(-math.inf) == "-Inf"


def test_format_not_finite_positive_infinity():
    assert _format_not_finite(math.inf) == "+Inf"


@pytest.mark.parametrize("value", [0.0, -0.0, 1.5, -3.0, 1e308, -1e-308])
def test_format_not_finite_returns_empty_string_for_finite_values(value):
    assert _format_not_finite(value) == ""


# ---------------------------------------------------------------------------
# Digits 0-9 become words
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("digit, word", list(enumerate(WORDS)))
def test_each_digit_from_zero_to_nine_maps_to_its_word(digit, word):
    assert apnumber(digit) == word


def test_zero_and_nine_are_the_inclusive_bounds():
    assert apnumber(0) == "zero"
    assert apnumber(9) == "nine"


# ---------------------------------------------------------------------------
# Integers outside 0..9 are returned as decimal strings
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("value, expected", [
    (10, "10"),
    (11, "11"),
    (99, "99"),
    (100, "100"),
    (-1, "-1"),
    (-10, "-10"),
    (-123, "-123"),
])
def test_integers_outside_zero_to_nine_are_returned_as_decimal_strings(value, expected):
    assert apnumber(value) == expected


def test_ten_is_the_exclusive_upper_bound():
    assert apnumber(10) == "10"


def test_minus_one_is_below_the_lower_bound():
    assert apnumber(-1) == "-1"


def test_large_int_is_returned_in_full():
    assert apnumber(10 ** 30) == str(10 ** 30)
    assert apnumber(-(10 ** 30)) == str(-(10 ** 30))


def test_large_power_of_two_float_converts_exactly_to_int_string():
    assert apnumber(2.0 ** 64) == str(2 ** 64)


def test_int_beyond_float_range_propagates_overflow_error():
    # float() runs before int(), and OverflowError is not in the except tuple.
    with pytest.raises(OverflowError):
        apnumber(10 ** 400)
    with pytest.raises(OverflowError):
        apnumber(-(10 ** 400))


# ---------------------------------------------------------------------------
# Floats are truncated toward zero, not rounded
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("value, expected", [
    (0.0, "zero"),
    (-0.0, "zero"),
    (0.5, "zero"),
    (-0.9, "zero"),
    (1e-300, "zero"),
    (3.2, "three"),
    (3.7, "three"),
    (7.0, "seven"),
    (9.5, "nine"),
    (9.999, "nine"),
    (-1.5, "-1"),
])
def test_finite_floats_are_truncated_toward_zero_before_lookup(value, expected):
    assert apnumber(value) == expected


def test_float_is_truncated_not_rounded():
    assert apnumber(3.7) == "three"
    assert apnumber(3.7) != "four"


def test_float_at_or_above_ten_returns_int_form_without_decimal_point():
    assert apnumber(10.0) == "10"
    assert apnumber(10.5) == "10"
    assert apnumber(12.9) == "12"


def test_negative_whole_float_returns_int_form():
    assert apnumber(-3.0) == "-3"


# ---------------------------------------------------------------------------
# Booleans (int subclass)
# ---------------------------------------------------------------------------

def test_bool_values_follow_their_integer_value():
    assert apnumber(True) == "one"
    assert apnumber(False) == "zero"


# ---------------------------------------------------------------------------
# Decimal
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("value, expected", [
    (Decimal("7"), "seven"),
    (Decimal("3.9"), "three"),
    (Decimal("-2.5"), "-2"),
    (Decimal("12"), "12"),
])
def test_decimal_values_are_converted_like_floats(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize("value, expected", [
    (Decimal("NaN"), "NaN"),
    (Decimal("Infinity"), "+Inf"),
    (Decimal("-Infinity"), "-Inf"),
    (Decimal("1e400"), "+Inf"),
])
def test_decimal_non_finite_values_are_reported_like_floats(value, expected):
    assert apnumber(value) == expected


def test_decimal_signaling_nan_cannot_become_float_and_is_returned_as_str():
    assert apnumber(Decimal("sNaN")) == "sNaN"


# ---------------------------------------------------------------------------
# Strings
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("value, expected", [
    ("0", "zero"),
    ("5", "five"),
    ("9", "nine"),
    ("+4", "four"),
    ("  7  ", "seven"),
    ("10", "10"),
    ("-2", "-2"),
])
def test_integer_strings_are_converted_like_ints(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize("value", ["3.7", "1e3", "2.0", "-0.5"])
def test_numeric_strings_that_are_not_ints_are_returned_unchanged(value):
    assert apnumber(value) == value


@pytest.mark.parametrize("value", ["abc", "", "five", "1,5", "3 4"])
def test_non_numeric_strings_are_returned_unchanged(value):
    assert apnumber(value) == value


@pytest.mark.parametrize("text, expected", [
    ("nan", "NaN"),
    ("NaN", "NaN"),
    ("inf", "+Inf"),
    ("+inf", "+Inf"),
    ("-inf", "-Inf"),
    ("Infinity", "+Inf"),
    ("-Infinity", "-Inf"),
])
def test_non_finite_strings_are_reported_like_non_finite_floats(text, expected):
    assert apnumber(text) == expected


# ---------------------------------------------------------------------------
# Non-finite floats
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("value, expected", [
    (math.nan, "NaN"),
    (float("nan"), "NaN"),
    (math.inf, "+Inf"),
    (-math.inf, "-Inf"),
    (1e308 * 10, "+Inf"),
    (-1e308 * 10, "-Inf"),
])
def test_non_finite_floats_are_reported(value, expected):
    assert apnumber(value) == expected


# ---------------------------------------------------------------------------
# Objects rejected by float() fall back to str()
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("value, expected", [
    (None, "None"),
    ([], "[]"),
    ([1, 2], "[1, 2]"),
    ({}, "{}"),
    ((1,), "(1,)"),
])
def test_objects_rejected_by_float_are_returned_via_str(value, expected):
    assert apnumber(value) == expected


def test_custom_object_rejected_by_float_uses_its_str_form():
    assert apnumber(_Labelled()) == "custom label"


# ---------------------------------------------------------------------------
# Result type and sweeps
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("value", [
    0, 5, 10, -4, 2.5, "8", "x", None, math.nan, math.inf, Decimal("4"),
])
def test_result_is_always_a_str(value):
    assert isinstance(apnumber(value), str)


def test_sweep_of_integers_matches_reference():
    for n in range(-25, 30):
        expected = WORDS[n] if 0 <= n <= 9 else str(n)
        assert apnumber(n) == expected


def test_sweep_of_fractional_floats_matches_truncated_reference():
    for n in range(0, 15):
        for frac in (0.0, 0.25, 0.75, 0.999):
            assert apnumber(n + frac) == reference(n + frac)
            assert apnumber(-(n + frac)) == reference(-(n + frac))
