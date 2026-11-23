import math

import pytest

import alvo
from alvo import ordinal, _SUFIXOS, _format_not_finite


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (5, "5th"),
        (9, "9th"),
        (0, "0th"),
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
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (211, "211th"),
        (212, "212th"),
        (213, "213th"),
        (121, "121st"),
        (122, "122nd"),
        (123, "123rd"),
        (1000, "1000th"),
        (1001, "1001st"),
        (-1, "-1th"),
        (-2, "-2th"),
        (-3, "-3th"),
        (-11, "-11th"),
    ],
)
def test_ordinal_integers(value, expected):
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
        (" 5 ", "5th"),
        ("-1", "-1th"),
    ],
)
def test_ordinal_string_numbers(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (3.9, "3rd"),
        (0.5, "0th"),
        (11.9, "11th"),
        (22.7, "22nd"),
        (1.0, "1st"),
    ],
)
def test_ordinal_floats_truncate(value, expected):
    assert ordinal(value) == expected


def test_ordinal_bool():
    assert ordinal(True) == "1st"
    assert ordinal(False) == "0th"


@pytest.mark.parametrize(
    "value, expected",
    [
        ("abc", "abc"),
        ("3.9", "3.9"),
        (None, "None"),
        ([], "[]"),
        ([1], "[1]"),
        ({}, "{}"),
        ((1, 2), "(1, 2)"),
    ],
)
def test_ordinal_unconvertible_returns_str(value, expected):
    assert ordinal(value) == expected


def test_ordinal_nan():
    assert ordinal(float("nan")) == "NaN"
    assert ordinal(math.nan) == "NaN"
    assert ordinal("nan") == "NaN"


def test_ordinal_infinities():
    assert ordinal(float("inf")) == "+Inf"
    assert ordinal(float("-inf")) == "-Inf"
    assert ordinal(math.inf) == "+Inf"
    assert ordinal(-math.inf) == "-Inf"
    assert ordinal("inf") == "+Inf"
    assert ordinal("-inf") == "-Inf"


def test_gender_parameter_ignored():
    assert ordinal(1) == ordinal(1, "female") == ordinal(1, gender="male") == "1st"
    assert ordinal(1, "female") == "1st"


def test_format_not_finite():
    assert _format_not_finite(float("nan")) == "NaN"
    assert _format_not_finite(float("inf")) == "+Inf"
    assert _format_not_finite(float("-inf")) == "-Inf"
    assert _format_not_finite(0.0) == ""
    assert _format_not_finite(1.5) == ""


def test_sufixos_constant():
    assert _SUFIXOS == ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")
    assert alvo._SUFIXOS[1] == "st"
    assert alvo._SUFIXOS[2] == "nd"
    assert alvo._SUFIXOS[3] == "rd"
    assert alvo._SUFIXOS[0] == "th"
    assert alvo._SUFIXOS[9] == "th"
