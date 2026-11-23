"""Reproduction tests for the issue: ``ordinal(11)`` returns ``'11st'``.

The bug is in the "teens" special case: the module checks ``value % 10``
against ``(11, 12, 13)``, which can never be true.  It should look at the last
two digits (``value % 100``).  Therefore every number whose last two digits are
11, 12 or 13 must get the ``'th'`` suffix.

All assertions below only rely on expected (correct English) ordinal
behaviour, so they fail on the buggy code and pass once the "teens" rule is
fixed.
"""

import pytest

from alvo import ordinal


def test_issue_ordinal_11():
    """The exact case from the issue report."""
    assert ordinal(11) == "11th"


@pytest.mark.parametrize("value", [11, 12, 13])
def test_teens_get_th_suffix(value):
    assert ordinal(value) == f"{value}th"


@pytest.mark.parametrize("value", [111, 112, 113, 211, 212, 213, 1011, 1012, 1013])
def test_teens_ending_gets_th_suffix(value):
    assert ordinal(value) == f"{value}th"


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0th"),
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (5, "5th"),
        (9, "9th"),
        (10, "10th"),
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
        (121, "121st"),
        (122, "122nd"),
        (123, "123rd"),
    ],
)
def test_regular_ordinal_suffixes(value, expected):
    """Regression checks: the non-teens cases must keep working."""
    assert ordinal(value) == expected


def test_no_number_ending_in_11_12_13_uses_st_nd_rd():
    """Sweep: nothing ending in 11/12/13 may get 'st', 'nd' or 'rd'."""
    wrong = {}
    for value in range(0, 500):
        got = ordinal(value)
        if value % 100 in (11, 12, 13) and not got.endswith("th"):
            wrong[value] = got
    assert wrong == {}
