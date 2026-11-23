"""Tests reproducing the issue: naturalsize(binary=True) must use powers of 1024."""

import pytest

from alvo import naturalsize


def test_binary_true_reported_case():
    # 3000000 / 1024**2 == 2.8610... -> "2.9 MiB" (buggy code returns "3.0 MiB")
    assert naturalsize(3000000, binary=True) == "2.9 MiB"


def test_binary_true_is_not_decimal_result():
    result = naturalsize(3000000, binary=True)
    assert result != naturalsize(3000000)
    assert result != "3.0 MiB"


@pytest.mark.parametrize(
    "value, expected",
    [
        (1024, "1.0 KiB"),
        (1024**2, "1.0 MiB"),
        (1024**3, "1.0 GiB"),
        (1024**4, "1.0 TiB"),
        (1536, "1.5 KiB"),
        (2048, "2.0 KiB"),
        (10**6, "976.6 KiB"),
        (1024**2 + 512 * 1024, "1.5 MiB"),
        (5 * 1024**3, "5.0 GiB"),
    ],
)
def test_binary_uses_powers_of_1024(value, expected):
    assert naturalsize(value, binary=True) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (3000000, "3.0 MB"),
        (1000, "1.0 kB"),
        (1000**2, "1.0 MB"),
        (10**6, "1.0 MB"),
        (1000**3, "1.0 GB"),
    ],
)
def test_decimal_unchanged(value, expected):
    """Decimal (default) behaviour must stay based on powers of 1000."""
    assert naturalsize(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1024, "1.0K"),
        (1024**2, "1.0M"),
        (3000000, "2.9M"),
    ],
)
def test_gnu_unchanged(value, expected):
    """GNU behaviour must stay based on powers of 1024 without a space."""
    assert naturalsize(value, gnu=True) == expected


def test_binary_small_values_unchanged():
    assert naturalsize(1, binary=True) == "1 Byte"
    assert naturalsize(0, binary=True) == "0 Bytes"
    assert naturalsize(1023, binary=True) == "1023 Bytes"


def test_binary_negative_values():
    # Negative values must also use powers of 1024.
    assert naturalsize(-3000000, binary=True) == "-2.9 MiB"
