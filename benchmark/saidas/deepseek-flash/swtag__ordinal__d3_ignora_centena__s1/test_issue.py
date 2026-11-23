import math

import pytest

from alvo import ordinal


# ---------------------------------------------------------------------------
# The bug reported in ISSUE.md: numbers ending in 11, 12 or 13 (but bigger
# than 13 itself) must still use the "th" suffix.
# ---------------------------------------------------------------------------

def test_111_is_111th():
    assert ordinal(111) == "111th"


def test_112_is_112th():
    assert ordinal(112) == "112th"


def test_113_is_113th():
    assert ordinal(113) == "113th"


@pytest.mark.parametrize(
    "value, expected",
    [
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (211, "211th"),
        (212, "212th"),
        (213, "213th"),
        (311, "311th"),
        (411, "411th"),
        (512, "512th"),
        (613, "613th"),
        (911, "911th"),
        (1011, "1011th"),
        (1012, "1012th"),
        (1013, "1013th"),
        (1111, "1111th"),
        (11111, "11111th"),
        (1000000 + 11, "1000011th"),
        (1000000 + 12, "1000012th"),
        (1000000 + 13, "1000013th"),
    ],
)
def test_teens_ending_uses_th(value, expected):
    assert ordinal(value) == expected


def test_teens_ending_as_float_uses_th():
    assert ordinal(111.0) == "111th"
    assert ordinal(212.0) == "212th"
    assert ordinal(313.0) == "313th"


def test_teens_ending_as_string_uses_th():
    assert ordinal("111") == "111th"
    assert ordinal("112") == "112th"
    assert ordinal("113") == "113th"


# ---------------------------------------------------------------------------
# Regression guards: the behaviour that already works must keep working.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
        (121, "121st"),
        (122, "122nd"),
        (123, "123rd"),
        (100, "100th"),
        (1000, "1000th"),
    ],
)
def test_regular_ordinals_unchanged(value, expected):
    assert ordinal(value) == expected


def test_not_finite_and_invalid_unchanged():
    assert ordinal(float("nan")) == "NaN"
    assert ordinal(float("inf")) == "+Inf"
    assert ordinal(float("-inf")) == "-Inf"
    assert ordinal("abc") == "abc"
