"""Reproduction tests for the issue: naturalsize(-1) uses the plural 'Bytes'.

`naturalsize(1)` returns `'1 Byte'`, so the negative counterpart `-1` should
also use the singular form: `'-1 Byte'`.
"""

import pytest

from alvo import naturalsize


def test_negative_one_is_singular_byte():
    assert naturalsize(-1) == "-1 Byte"


def test_negative_one_float_is_singular_byte():
    assert naturalsize(-1.0) == "-1 Byte"


def test_negative_one_binary_is_singular_byte():
    assert naturalsize(-1, binary=True) == "-1 Byte"


def test_negative_one_gnu_stays_plain_bytes():
    # The gnu format never uses the "Byte(s)" wording.
    assert naturalsize(-1, gnu=True) == "-1B"


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "1 Byte"),
        (1.0, "1 Byte"),
        (1, "1 Byte"),
        (0, "0 Bytes"),
        (-2, "-2 Bytes"),
    ],
)
def test_singular_plural_behaviour_is_preserved(value, expected):
    assert naturalsize(value) == expected


def test_positive_one_binary_is_singular_byte():
    assert naturalsize(1, binary=True) == "1 Byte"
