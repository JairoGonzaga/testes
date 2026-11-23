"""Tests reproducing the issue: naturalsize does not promote the unit when the
formatted value rounds up to the next unit (e.g. 999999 -> '1000.0 kB' instead
of '1.0 MB')."""

import pytest

from alvo import naturalsize


def _numeric_and_suffix(result):
    """Split '1000.0 kB' / '1.0M' into (1000.0, 'kB' / 'M')."""
    result = result.strip()
    idx = 0
    while idx < len(result) and (result[idx].isdigit() or result[idx] in "+-.eE"):
        idx += 1
    return float(result[:idx]), result[idx:].strip()


def test_issue_example_promotes_to_next_unit():
    # Exact example from the issue report.
    assert naturalsize(999999) == "1.0 MB"


def test_decimal_promotion_several_units():
    assert naturalsize(999_999_999) == "1.0 GB"
    assert naturalsize(999_999_999_999) == "1.0 TB"


def test_decimal_promotion_with_negative_value():
    assert naturalsize(-999999) == "-1.0 MB"


def test_binary_promotion():
    # 1048575 bytes = 1023.999 KiB, which formats to '1024.0 KiB' -> '1.0 MiB'
    assert naturalsize(1024**2 - 1, binary=True) == "1.0 MiB"
    assert naturalsize(1024**3 - 1, binary=True) == "1.0 GiB"


def test_gnu_promotion():
    value, suffix = _numeric_and_suffix(naturalsize(1024**2 - 1, gnu=True))
    assert suffix == "M"
    assert value == pytest.approx(1.0)


def test_custom_format_also_promotes():
    # With no decimals, 999999 -> '1000 kB' -> '1 MB'
    assert naturalsize(999999, format="%.0f") == "1 MB"
    assert naturalsize(987_654_321, format="%.0f") == "988 MB"


def test_values_that_do_not_round_up_are_unchanged():
    assert naturalsize(999499) == "999.5 kB"
    assert naturalsize(999499, format="%.0f") == "999 kB"
    assert naturalsize(1500) == "1.5 kB"
    assert naturalsize(1500, binary=True) == "1.5 KiB"
    assert naturalsize(1500, gnu=True) == "1.5K"
    assert naturalsize(1000) == "1.0 kB"
    assert naturalsize(999) == "999 Bytes"
    assert naturalsize(1) == "1 Byte"
    assert naturalsize(0) == "0 Bytes"
