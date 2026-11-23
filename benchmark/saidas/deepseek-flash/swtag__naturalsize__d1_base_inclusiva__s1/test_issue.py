"""Tests reproducing the issue: naturalsize(1000) returns '1000 Bytes'.

Expected behaviour: a value that is *exactly* one unit (1000 for decimal,
1024 for binary/gnu) must be converted to the next unit, e.g. 1000 -> '1.0 kB'.
Only values strictly smaller than the base stay in plain bytes.
"""

import pytest

from alvo import naturalsize


# ---------------------------------------------------------------------------
# The exact case reported in the issue
# ---------------------------------------------------------------------------
def test_one_kilobyte_is_converted():
    assert naturalsize(1000) == "1.0 kB"


@pytest.mark.parametrize("value", [1000, 1000.0, -1000, -1000.0])
def test_exact_base_is_converted_decimal(value):
    expected = "1.0 kB" if value > 0 else "-1.0 kB"
    assert naturalsize(value) == expected


@pytest.mark.parametrize("value", [1024, 1024.0, -1024, -1024.0])
def test_exact_base_is_converted_binary(value):
    expected = "1.0 KiB" if value > 0 else "-1.0 KiB"
    assert naturalsize(value, binary=True) == expected


@pytest.mark.parametrize("value", [1024, 1024.0, -1024, -1024.0])
def test_exact_base_is_converted_gnu(value):
    expected = "1.0K" if value > 0 else "-1.0K"
    assert naturalsize(value, gnu=True) == expected


# ---------------------------------------------------------------------------
# Values just below the base must still be rendered as plain bytes
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("value", [0, 1, 2, 5, 999, -5, -999])
def test_below_base_stays_bytes(value):
    if value == 1:
        expected = "1 Byte"
    elif value == -1:
        expected = "-1 Byte"
    else:
        expected = "%d Bytes" % value
    assert naturalsize(value) == expected


@pytest.mark.parametrize("value", [999, 1000, -1000, -1023])
def test_below_base_stays_bytes_binary(value):
    assert naturalsize(value, binary=True) == "%d Bytes" % value


@pytest.mark.parametrize("value", [0, 1, 999, 1000, -1, -1000])
def test_below_base_stays_bytes_gnu(value):
    assert naturalsize(value, gnu=True) == "%dB" % value


# ---------------------------------------------------------------------------
# Sanity checks: larger values and formatting still behave
# ---------------------------------------------------------------------------
def test_larger_values_decimal():
    assert naturalsize(1_000_000) == "1.0 MB"
    assert naturalsize(1_000_000_000) == "1.0 GB"


def test_larger_values_binary():
    assert naturalsize(1024 * 1024, binary=True) == "1.0 MiB"
    assert naturalsize(1024 ** 3, binary=True) == "1.0 GiB"


def test_larger_values_gnu():
    assert naturalsize(1024 * 1024, gnu=True) == "1.0M"


def test_exact_base_with_custom_format():
    assert naturalsize(1000, format="%.0f") == "1 kB"
    assert naturalsize(1000, format="%.2f") == "1.00 kB"


def test_gnu_has_no_space_and_decimal_has_one():
    # The unit separator must not change with the fix.
    assert naturalsize(1000).endswith(" kB")
    assert naturalsize(1024, gnu=True).endswith("K")
    assert " " not in naturalsize(1024, gnu=True)
