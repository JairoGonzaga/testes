"""Reproduction tests for the issue in ISSUE.md.

`naturalsize()` must promote the unit when formatting rounds the value up to
the size of the next unit (e.g. 999999 bytes is "1000.0 kB" after rounding,
which should be reported as "1.0 MB").
"""

import pytest

from alvo import naturalsize


def test_issue_example():
    """The exact example from the issue report."""
    assert naturalsize(999999) == "1.0 MB"


@pytest.mark.parametrize(
    "value, expected",
    [
        # values whose formatted result rounds up to the next unit boundary
        (999999, "1.0 MB"),
        (999999999, "1.0 GB"),
        (999999999999, "1.0 TB"),
        # the same thing for negative numbers
        (-999999, "-1.0 MB"),
        (-999999999, "-1.0 GB"),
    ],
)
def test_decimal_rounding_promotes_unit(value, expected):
    assert naturalsize(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        # 1023.999 KiB rounds up to the KiB limit, so it must become 1.0 MiB
        (1024 * 1024 - 1, "1.0 MiB"),
        (1024 * 1024 * 1024 - 1, "1.0 GiB"),
    ],
)
def test_binary_rounding_promotes_unit(value, expected):
    assert naturalsize(value, binary=True) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0 Bytes"),
        (1, "1 Byte"),
        (-1, "-1 Byte"),
        (2, "2 Bytes"),
        (500, "500 Bytes"),
        (999, "999 Bytes"),
        (1000, "1.0 kB"),
        (1500, "1.5 kB"),
        (999899, "999.9 kB"),
        (1000000, "1.0 MB"),
        (2500000, "2.5 MB"),
        (1000000000, "1.0 GB"),
    ],
)
def test_regular_values_unchanged(value, expected):
    """Normal (non-boundary) formatting must keep working as before."""
    assert naturalsize(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0B"),
        (512, "512B"),
        (1024, "1.0K"),
        (1024 * 1024, "1.0M"),
    ],
)
def test_gnu_values_unchanged(value, expected):
    """GNU style output for ordinary values must keep working."""
    assert naturalsize(value, gnu=True) == expected
