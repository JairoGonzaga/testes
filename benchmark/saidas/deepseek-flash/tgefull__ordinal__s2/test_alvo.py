import math
from decimal import Decimal

import pytest

from alvo import _SUFIXOS, _format_not_finite, ordinal


def test_sufixos_constant():
    assert _SUFIXOS == ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")


@pytest.mark.parametrize(
    "value, expected",
    [
        (float("nan"), "NaN"),
        (-float("nan"), "NaN"),
        (math.nan, "NaN"),
        (float("inf"), "+Inf"),
        (math.inf, "+Inf"),
        (float("-inf"), "-Inf"),
        (-math.inf, "-Inf"),
        (0.0, ""),
        (-0.0, ""),
        (1.5, ""),
        (-1.5, ""),
        (1, ""),
        (-1, ""),
    ],
)
def test_format_not_finite(value, expected):
    assert _format_not_finite(value) == expected


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
        (20, "20th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (24, "24th"),
        (100, "100th"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
        (104, "104th"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (114, "114th"),
        (121, "121st"),
        (122, "122nd"),
        (123, "123rd"),
        (1000, "1000th"),
    ],
)
def test_ordinal_integer_suffixes(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (-1, "-1th"),
        (-2, "-2th"),
        (-3, "-3th"),
        (-7, "-7rd"),
        (-8, "-8nd"),
        (-9, "-9st"),
        (-11, "-11th"),
        (-12, "-12th"),
        (-13, "-13th"),
        (-21, "-21th"),
        (-22, "-22th"),
        (-23, "-23th"),
    ],
)
def test_ordinal_negative_integer_suffixes_follow_python_modulo(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0.1, "0th"),
        (0.9, "0th"),
        (1.1, "1st"),
        (1.9, "1st"),
        (2.1, "2nd"),
        (2.9, "2nd"),
        (3.1, "3rd"),
        (3.9, "3rd"),
        (4.9, "4th"),
        (10.9, "10th"),
        (11.1, "11th"),
        (11.9, "11th"),
        (12.1, "12th"),
        (12.9, "12th"),
        (13.1, "13th"),
        (13.9, "13th"),
        (21.9, "21st"),
        (22.9, "22nd"),
        (23.9, "23rd"),
        (-0.5, "0th"),
        (-1.1, "-1th"),
        (-1.9, "-1th"),
        (-2.1, "-2th"),
        (-3.9, "-3th"),
        (-7.1, "-7rd"),
        (-8.1, "-8nd"),
        (-9.1, "-9st"),
    ],
)
def test_ordinal_truncates_finite_floats_toward_zero(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (float("nan"), "NaN"),
        (float("inf"), "+Inf"),
        (float("-inf"), "-Inf"),
        ("nan", "NaN"),
        ("NaN", "NaN"),
        ("inf", "+Inf"),
        ("+inf", "+Inf"),
        ("Infinity", "+Inf"),
        ("-inf", "-Inf"),
        ("-Infinity", "-Inf"),
        (Decimal("NaN"), "NaN"),
        (Decimal("Infinity"), "+Inf"),
        (Decimal("-Infinity"), "-Inf"),
    ],
)
def test_ordinal_non_finite_values(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("0", "0th"),
        ("1", "1st"),
        ("2", "2nd"),
        ("3", "3rd"),
        ("4", "4th"),
        ("11", "11th"),
        ("12", "12th"),
        ("13", "13th"),
        ("21", "21st"),
        ("22", "22nd"),
        ("23", "23rd"),
        (" 3 ", "3rd"),
        ("+3", "3rd"),
        ("-1", "-1th"),
    ],
)
def test_ordinal_integer_strings(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("abc", "abc"),
        ("3.14", "3.14"),
        ("1e3", "1e3"),
        ("", ""),
        ("  ", "  "),
        ("nanx", "nanx"),
        ("infinityx", "infinityx"),
    ],
)
def test_ordinal_invalid_numeric_strings_return_original_string(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, "None"),
        ([], "[]"),
        ({}, "{}"),
        ((), "()"),
        (set(), "set()"),
        (1 + 2j, "(1+2j)"),
        (b"3", "b'3'"),
    ],
)
def test_ordinal_type_errors_return_str_of_original_value(value, expected):
    assert ordinal(value) == expected


class _FloatRaisesTypeError:
    def __float__(self):
        raise TypeError("cannot convert")

    def __str__(self):
        return "float-type-error"


class _FloatOnly:
    def __float__(self):
        return 3.0

    def __str__(self):
        return "float-only"


class _IntRaisesValue:
    def __float__(self):
        return 2.0

    def __int__(self):
        raise ValueError("cannot convert")

    def __str__(self):
        return "int-value-error"


class _FloatInfinity:
    def __float__(self):
        return float("inf")

    def __str__(self):
        return "should-not-be-used"


def test_ordinal_custom_float_error_returns_str():
    assert ordinal(_FloatRaisesTypeError()) == "float-type-error"


def test_ordinal_custom_float_only_object_fails_at_int_and_returns_str():
    assert ordinal(_FloatOnly()) == "float-only"


def test_ordinal_custom_int_value_error_returns_str():
    assert ordinal(_IntRaisesValue()) == "int-value-error"


def test_ordinal_custom_non_finite_float_uses_format_helper():
    assert ordinal(_FloatInfinity()) == "+Inf"


@pytest.mark.parametrize(
    "args, kwargs, expected",
    [
        ((1,), {}, "1st"),
        ((1, "female"), {}, "1st"),
        ((1,), {"gender": "female"}, "1st"),
        ((2, "male"), {}, "2nd"),
        ((3,), {"gender": "other"}, "3rd"),
        ((11,), {"gender": "female
