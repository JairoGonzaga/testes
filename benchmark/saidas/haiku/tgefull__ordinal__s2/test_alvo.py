"""Pytest suite for alvo.ordinal and its helper _format_not_finite."""
import inspect
import math

import pytest

from alvo import _SUFIXOS, _format_not_finite, ordinal


class _FloatOnly:
    """Converts to a finite float but not to an int (no __int__ or __index__)."""

    def __float__(self):
        return 5.0

    def __str__(self):
        return "float-only"


class _FloatAndInt:
    """int() uses __int__, so the final integer is 7 even though float() gives 5.0."""

    def __float__(self):
        return 5.0

    def __int__(self):
        return 7

    def __str__(self):
        return "float-and-int"


def _reference_suffix(n):
    """Independent oracle for non-negative integers."""
    if n % 100 in (11, 12, 13):
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


# ---------------------------------------------------------------------------
# Module constants
# ---------------------------------------------------------------------------

def test_suffix_table_contents():
    assert _SUFIXOS == ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")
    assert len(_SUFIXOS) == 10


# ---------------------------------------------------------------------------
# _format_not_finite
# ---------------------------------------------------------------------------

def test_format_not_finite_nan():
    assert _format_not_finite(math.nan) == "NaN"


def test_format_not_finite_positive_infinity():
    assert _format_not_finite(math.inf) == "+Inf"


def test_format_not_finite_negative_infinity():
    assert _format_not_finite(-math.inf) == "-Inf"


@pytest.mark.parametrize("value", [0.0, -0.0, 1.5, -2.5, 1e308, 0, 7, -7])
def test_format_not_finite_returns_empty_string_for_finite(value):
    assert _format_not_finite(value) == ""


def test_format_not_finite_rejects_strings():
    with pytest.raises(TypeError):
        _format_not_finite("inf")


# ---------------------------------------------------------------------------
# ordinal: positive integers
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0th"),
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (5, "5th"),
        (6, "6th"),
        (7, "7th"),
        (8, "8th"),
        (9, "9th"),
        (10, "10th"),
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (14, "14th"),
        (15, "15th"),
        (19, "19th"),
        (20, "20th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (24, "24th"),
        (31, "31st"),
        (42, "42nd"),
        (53, "53rd"),
        (99, "99th"),
        (100, "100th"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
        (104, "104th"),
        (110, "110th"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (114, "114th"),
        (121, "121st"),
        (122, "122nd"),
        (123, "123rd"),
        (201, "201st"),
        (1001, "1001st"),
        (1002, "1002nd"),
        (1003, "1003rd"),
        (1011, "1011th"),
        (1012, "1012th"),
        (1013, "1013th"),
        (1021, "1021st"),
        (1111, "1111th"),
    ],
)
def test_ordinal_positive_integers(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize("hundreds", range(10))
@pytest.mark.parametrize("teen", [11, 12, 13])
def test_teens_use_th_whatever_the_hundreds(hundreds, teen):
    value = hundreds * 100 + teen
    assert ordinal(value) == f"{value}th"


def test_ordinal_matches_reference_rule_over_range():
    for n in range(0, 2000):
        assert ordinal(n) == f"{n}{_reference_suffix(n)}", n


def test_large_ints_are_formatted_exactly():
    assert ordinal(10**300) == f"{10**300}th"
    # 2**53 + 1 is not representable as a float; the int must be kept exact.
    assert ordinal(2**53 + 1) == f"{2**53 + 1}rd"


def test_int_too_large_for_float_propagates_overflow_error():
    # float() runs before int(), and OverflowError is not in the caught tuple.
    with pytest.raises(OverflowError):
        ordinal(10**400)


# ---------------------------------------------------------------------------
# ordinal: negative integers
# The code uses Python's floored modulo, so these outputs are the current
# behaviour and are pinned here to catch mutations of the arithmetic.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (-1, "-1th"),
        (-2, "-2th"),
        (-3, "-3th"),
        (-7, "-7rd"),
        (-8, "-8nd"),
        (-9, "-9st"),
        (-10, "-10th"),
        (-11, "-11th"),
        (-13, "-13th"),
        (-88, "-88th"),
        (-89, "-89th"),
    ],
)
def test_ordinal_negative_integers_use_floored_modulo(value, expected):
    assert ordinal(value) == expected


# ---------------------------------------------------------------------------
# ordinal: floats, bools and objects with numeric protocols
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (1.0, "1st"),
        (2.0, "2nd"),
        (3.0, "3rd"),
        (11.0, "11th"),
        (12.9, "12th"),
        (2.7, "2nd"),
        (-0.0, "0th"),
        (-0.5, "0th"),
        (-2.7, "-2th"),
        (1e20, f"{10**20}th"),
    ],
)
def test_ordinal_finite_floats_truncate_toward_zero(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize("value, expected", [(True, "1st"), (False, "0th")])
def test_ordinal_bools_behave_as_ints(value, expected):
    assert ordinal(value) == expected


def test_final_conversion_uses_int_not_float():
    assert ordinal(_FloatAndInt()) == "7th"


# ---------------------------------------------------------------------------
# ordinal: strings
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        ("1", "1st"),
        ("2", "2nd"),
        ("42", "42nd"),
        ("111", "111th"),
        ("  7  ", "7th"),
        ("+5", "5th"),
        ("-0", "0th"),
        ("-9", "-9st"),
    ],
)
def test_ordinal_integer_strings_are_converted(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize("value", ["3.0", " 1.5 ", "1e3", "2.5e1"])
def test_non_integer_numeric_strings_are_returned_unchanged(value):
    assert ordinal(value) == value


@pytest.mark.parametrize(
    "value, expected",
    [
        (math.nan, "NaN"),
        (float("nan"), "NaN"),
        (math.inf, "+Inf"),
        (-math.inf, "-Inf"),
        ("nan", "NaN"),
        ("inf", "+Inf"),
        ("+inf", "+Inf"),
        ("-inf", "-Inf"),
        ("Infinity", "+Inf"),
        ("-INF", "-Inf"),
    ],
)
def test_non_finite_values_are_named_not_converted(value, expected):
    # Non-finite checks must run before int(), otherwise "nan"/"inf" would
    # hit the ValueError fallback and come back lowercase.
    assert ordinal(value) == expected


# ---------------------------------------------------------------------------
# ordinal: non-numeric input falls back to str(value)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (None, "None"),
        ("abc", "abc"),
        ("", ""),
        (" ", " "),
        ([1, 2], "[1, 2]"),
        ({}, "{}"),
        ((), "()"),
        (1j, "1j"),
        (_FloatOnly(), "float-only"),
    ],
)
def test_non_numeric_values_fall_back_to_str(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize("value", [1, 1.5, "x", None, math.nan, math.inf])
def test_always_returns_a_str(value):
    assert isinstance(ordinal(value), str)


# ---------------------------------------------------------------------------
# ordinal: gender parameter
# ---------------------------------------------------------------------------

def test_gender_default_is_male():
    assert inspect.signature(ordinal).parameters["gender"].default == "male"


@pytest.mark.parametrize("gender", ["male", "female", "neuter", "", None])
def test_gender_does_not_change_output(gender):
    assert ordinal(2, gender=gender) == "2nd"
    assert ordinal(11, gender) == "11th"
