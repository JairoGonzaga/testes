"""Reproduction tests for the ordinal() suffix bug.

Issue: ordinal(11) returns '11st' but should return '11th'.

The teens (11, 12, 13) must always take the 'th' suffix, even though their
last digit is 1, 2 or 3.  The same applies to any number whose last two
digits are 11, 12 or 13 (111, 112, 113, 1011, ...).
"""

import pytest

from alvo import ordinal


def test_eleven():
    assert ordinal(11) == "11th"


def test_twelve():
    assert ordinal(12) == "12th"


def test_thirteen():
    assert ordinal(13) == "13th"


@pytest.mark.parametrize("value", [111, 112, 113, 211, 212, 213, 1011, 1112, 1113])
def test_teens_beyond_one_hundred(value):
    assert ordinal(value) == f"{value}th"


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (10, "10th"),
        (14, "14th"),
        (20, "20th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (24, "24th"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
        (104, "104th"),
        (100, "100th"),
    ],
)
def test_regular_suffixes_still_work(value, expected):
    assert ordinal(value) == expected
