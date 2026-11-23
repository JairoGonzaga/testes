"""Reproduction tests for the issue: naturalsize(-1) uses the plural 'Bytes'.

naturalsize(1) returns '1 Byte', but the negative counterpart incorrectly
returns '-1 Bytes'.  The singular form must also be used for -1.
"""

import pytest

from alvo import naturalsize


def test_negative_one_is_singular():
    assert naturalsize(-1) == "-1 Byte"


def test_negative_one_float_is_singular():
    assert naturalsize(-1.0) == "-1 Byte"


def test_negative_one_binary_is_singular():
    # binary uses the same "Byte(s)" wording as the decimal variant
    assert naturalsize(-1, binary=True) == "-1 Byte"


@pytest.mark.parametrize("value", [1, 1.0])
def test_positive_one_still_singular(value):
    assert naturalsize(value) == "1 Byte"


@pytest.mark.parametrize("value,expected", [(0, "0 Bytes"), (-2, "-2 Bytes"), (2, "2 Bytes")])
def test_other_small_values_still_plural(value, expected):
    assert naturalsize(value) == expected


def test_gnu_negative_one_unchanged():
    assert naturalsize(-1, gnu=True) == "-1B"
