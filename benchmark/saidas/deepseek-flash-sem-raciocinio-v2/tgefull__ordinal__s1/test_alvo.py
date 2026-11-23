import math

import pytest

from alvo import ordinal, _format_not_finite, _SUFIXOS


def test_sufixos_tuple():
    assert _SUFIXOS == ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")


@pytest.mark.parametrize(
    "value, expected",
    [
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
        (0, "0th"),
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (14, "14th"),
        (15, "15th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (24, "24th"),
        (31, "31st"),
        (100, "100th"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (114, "114th"),
        (121, "121st"),
        (122, "122nd"),
        (1000000, "1000000th"),
    ],
)
def test_ordinal_integers(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1.0, "1st"),
        (2.9, "2nd"),
        (3.99, "3rd"),
        (11.7, "11th"),
        (12.1, "12th"),
        (13.5, "13th"),
        (21.4, "21st"),
        (-1.9, "-1th"),
    ],
)
def test_ordinal_floats(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0th"),
        (-1, "-1th"),
        (-2, "-2th"),
        (-3, "-3th"),
        (-4, "-4th"),
        (-11, "-11th"),
        (-12, "-12th"),
        (-13, "-13th"),
        (-21, "-21th"),
    ],
)
def test_ordinal_negative(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("1", "1st"),
        ("2", "2nd"),
        ("3", "3rd"),
        ("4", "4th"),
        ("11", "11th"),
        ("12", "12th"),
        ("13", "13th"),
        ("21", "21st"),
        ("-2", "-2th"),
        (" 7 ", "7th"),
        ("2.9", "2.9"),
    ],
)
def test_ordinal_numeric_strings(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("5x", "5x"),
        ("x", "x"),
        ("", ""),
        ("abc", "abc"),
        ("1.2.3", "1.2.3"),
        (None, "None"),
        ([], "[]"),
        ([1, 2], "[1, 2]"),
        ({"a": 1}, "{'a': 1}"),
        ((1,), "(1,)"),
    ],
)
def test_ordinal_unconvertible_returns_str(value, expected):
    assert ordinal(value) == expected


def test_ordinal_custom_object_uses_str():
    class Thing:
        def __str__(self):
            return "thing!"

    assert ordinal(Thing()) == "thing!"


def test_ordinal_custom_object_with_float_and_int():
    class Num:
        def __float__(self):
            return 3.7

        def __int__(self):
            return 3

    assert ordinal(Num()) == "3rd"


def test_ordinal_bool():
    assert ordinal(True) == "1st"
    assert ordinal(False) == "0th"


@pytest.mark.parametrize(
    "value, expected",
    [
        (float("nan"), "NaN"),
        (float("inf"), "+Inf"),
        (float("-inf"), "-Inf"),
        (math.nan, "NaN"),
        (math.inf, "+Inf"),
        (-math.inf, "-Inf"),
        ("nan", "NaN"),
        ("inf", "+Inf"),
        ("-inf", "-Inf"),
        ("NaN", "NaN"),
        ("Infinity", "+Inf"),
        ("-Infinity", "-Inf"),
    ],
)
def test_ordinal_not_finite(value, expected):
    assert ordinal(value) == expected


def test_format_not_finite():
    assert _format_not_finite(math.nan) == "NaN"
    assert _format_not_finite(math.inf) == "+Inf"
    assert _format_not_finite(-math.inf) == "-Inf"
    assert _format_not_finite(1.0) == ""
    assert _format_not_finite(-1.0) == ""
    assert _format_not_finite(0.0) == ""


def test_gender_argument_is_ignored():
    assert ordinal(1) == ordinal(1, "male") == ordinal(1, "female") == "1st"
    assert ordinal(2, "female") == "2nd"
    assert ordinal(3, gender="female") == "3rd"
    assert ordinal(4, "other") == "4th"
    assert ordinal(11, "female") == "11th"
    assert ordinal(22, gender="male") == "22nd"


def test_gender_keyword_default():
    assert ordinal(value=5) == "5th"
    assert ordinal(value=12, gender="female") == "12th"
