"""Reproduction tests for the naturalsize() unit-boundary bug.

Issue: `naturalsize(1000)` returns ``'1000 Bytes'`` instead of ``'1.0 kB'``.
Exactly one base unit (1000 in decimal mode, 1024 in binary/gnu mode) is not
converted to the next unit, because the "too small for a suffix" shortcut uses
``<=`` instead of ``<``.
"""

import pytest

from alvo import naturalsize


@pytest.mark.parametrize(
    "value, expected",
    [
        (1000, "1.0 kB"),
        (-1000, "-1.0 kB"),
        (1000.0, "1.0 kB"),
    ],
)
def test_exactly_one_kilobyte_is_converted(value, expected):
    """One kilobyte (decimal base) must be shown with the kB suffix."""
    assert naturalsize(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1024, "1.0 KiB"),
        (-1024, "-1.0 KiB"),
    ],
)
def test_exactly_one_kibibyte_is_converted(value, expected):
    """One kibibyte (binary base) must be shown with the KiB suffix."""
    assert naturalsize(value, binary=True) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1024, "1.0K"),
        (-1024, "-1.0K"),
    ],
)
def test_exactly_one_kibibyte_is_converted_gnu(value, expected):
    """GNU mode must also convert exactly one base unit."""
    assert naturalsize(value, gnu=True) == expected


@pytest.mark.parametrize(
    "value, kwargs, expected",
    [
        (999, {}, "999 Bytes"),
        (-999, {}, "-999 Bytes"),
        (0, {}, "0 Bytes"),
        (1, {}, "1 Byte"),
        (1023, {"binary": True}, "1023 Bytes"),
        (1023, {"gnu": True}, "1023B"),
        (1000, {"gnu": True}, "1000B"),
        (500, {}, "500 Bytes"),
    ],
)
def test_values_below_base_keep_bytes_unit(value, kwargs, expected):
    """Values strictly below the base must keep the plain bytes unit."""
    assert naturalsize(value, **kwargs) == expected


@pytest.mark.parametrize(
    "value, kwargs, expected",
    [
        (2000, {}, "2.0 kB"),
        (999999, {}, "1.0 MB"),
        (1000000, {}, "1.0 MB"),
        (2048, {"binary": True}, "2.0 KiB"),
        (1024 * 1024, {"binary": True}, "1.0 MiB"),
        (2048, {"gnu": True}, "2.0K"),
    ],
)
def test_larger_values_still_use_larger_units(value, kwargs, expected):
    """Sanity checks: larger values keep behaving as before."""
    assert naturalsize(value, **kwargs) == expected
