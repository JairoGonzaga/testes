import math

import pytest

from alvo import ordinal


def test_ordinal_11_is_11th():
    assert ordinal(11) == "11th"


def test_ordinal_12_is_12th():
    assert ordinal(12) == "12th"


def test_ordinal_13_is_13th():
    assert ordinal(13) == "13th"


@pytest.mark.parametrize(
    "value, expected",
    [
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (1011, "1011th"),
        (1012, "1012th"),
        (1013, "1013th"),
    ],
)
def test_ordinal_teen_suffixes_for_larger_numbers(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (10, "10th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (24, "24th"),
        (0, "0th"),
        (100, "100th"),
    ],
)
def test_ordinal_regular_suffixes_still_work(value, expected):
    assert ordinal(value) == expected


def test_ordinal_gender_argument_accepted():
    assert ordinal(11, gender="female") == "11th"


def test_ordinal_non_finite_and_invalid_values():
    assert ordinal(float("nan")) == "NaN"
    assert ordinal(float("inf")) == "+Inf"
    assert ordinal(float("-inf")) == "-Inf"
    assert ordinal("abc") == "abc"
