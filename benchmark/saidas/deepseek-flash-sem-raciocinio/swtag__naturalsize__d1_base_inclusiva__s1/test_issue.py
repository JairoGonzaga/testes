import pytest

from alvo import naturalsize


def test_decimal_exact_kilobyte():
    """Exactly 1000 bytes should be reported as 1.0 kB, not 1000 Bytes."""
    assert naturalsize(1000) == "1.0 kB"


def test_binary_exact_kilobyte():
    """Exactly 1024 bytes should be reported as 1.0 KiB in binary mode."""
    assert naturalsize(1024, binary=True) == "1.0 KiB"


def test_gnu_exact_kilobyte():
    """Exactly 1024 bytes should be reported as 1.0K in gnu mode."""
    assert naturalsize(1024, gnu=True) == "1.0K"


@pytest.mark.parametrize(
    "value, expected",
    [
        (999, "999 Bytes"),
        (1001, "1.0 kB"),
        (1000000, "1.0 MB"),
        (1024, "1.0 kB"),
        (2000, "2.0 kB"),
    ],
)
def test_decimal_boundaries(value, expected):
    assert naturalsize(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1023, "1023 Bytes"),
        (1025, "1.0 KiB"),
        (2048, "2.0 KiB"),
        (1048576, "1.0 MiB"),
    ],
)
def test_binary_boundaries(value, expected):
    assert naturalsize(value, binary=True) == expected


def test_small_values_unchanged():
    assert naturalsize(1) == "1 Byte"
    assert naturalsize(0) == "0 Bytes"
    assert naturalsize(512) == "512 Bytes"
