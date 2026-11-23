"""Tests reproducing: naturalsize(-1) uses the plural 'Bytes' instead of 'Byte'."""

import pytest

from alvo import naturalsize


def test_positive_one_is_singular():
    # Sanity check: this already works today.
    assert naturalsize(1) == "1 Byte"


def test_negative_one_is_singular():
    # The bug: currently returns '-1 Bytes'.
    assert naturalsize(-1) == "-1 Byte"


def test_negative_one_float_is_singular():
    assert naturalsize(-1.0) == "-1 Byte"


def test_negative_one_binary_is_singular():
    # Consistency with naturalsize(1, binary=True) == '1 Byte'.
    assert naturalsize(1, binary=True) == "1 Byte"
    assert naturalsize(-1, binary=True) == "-1 Byte"


def test_negative_one_gnu_is_unchanged():
    # gnu mode never used the plural forms, so this must keep working.
    assert naturalsize(-1, gnu=True) == "-1B"
    assert naturalsize(1, gnu=True) == "1B"


@pytest.mark.parametrize("value", [-2, -100, -500, -999])
def test_other_negative_values_stay_plural(value):
    assert naturalsize(value) == "%d Bytes" % value


@pytest.mark.parametrize(
    "value,expected",
    [
        (0, "0 Bytes"),
        (1, "1 Byte"),
        (-1, "-1 Byte"),
        (2, "2 Bytes"),
        (-2, "-2 Bytes"),
        (999, "999 Bytes"),
        (1000, "1.0 kB"),
        (-1000, "-1.0 kB"),
    ],
)
def test_table(value, expected):
    assert naturalsize(value) == expected
