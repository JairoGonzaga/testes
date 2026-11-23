import pytest

from alvo import naturalsize


def test_exactly_one_kilobyte_is_converted():
    """naturalsize(1000) must roll over to the next unit, not stay in bytes."""
    assert naturalsize(1000) == "1.0 kB"


def test_exactly_one_kilobyte_float():
    assert naturalsize(1000.0) == "1.0 kB"


def test_negative_exactly_one_kilobyte():
    assert naturalsize(-1000) == "-1.0 kB"


@pytest.mark.parametrize(
    "value, expected",
    [
        (1000, "1.0 kB"),
        (1000 ** 2, "1.0 MB"),
        (1000 ** 3, "1.0 GB"),
        (1000 ** 4, "1.0 TB"),
        (-1000, "-1.0 kB"),
        (-(1000 ** 2), "-1.0 MB"),
    ],
)
def test_decimal_unit_boundaries(value, expected):
    assert naturalsize(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1024, "1.0 KiB"),
        (1024 ** 2, "1.0 MiB"),
        (1024 ** 3, "1.0 GiB"),
        (-1024, "-1.0 KiB"),
    ],
)
def test_binary_unit_boundaries(value, expected):
    assert naturalsize(value, binary=True) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1024, "1.0K"),
        (1024 ** 2, "1.0M"),
        (1024 ** 3, "1.0G"),
    ],
)
def test_gnu_unit_boundaries(value, expected):
    assert naturalsize(value, gnu=True) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0 Bytes"),
        (1, "1 Byte"),
        (-1, "-1 Byte"),
        (500, "500 Bytes"),
        (999, "999 Bytes"),
        (1001, "1.0 kB"),
        (999999, "1.0 MB"),
    ],
)
def test_below_boundary_values_unchanged(value, expected):
    assert naturalsize(value) == expected
