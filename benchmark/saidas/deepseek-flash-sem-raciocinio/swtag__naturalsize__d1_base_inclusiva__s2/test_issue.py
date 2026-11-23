import pytest

from alvo import naturalsize


def test_exactly_one_kilobyte_is_converted():
    # Core case from the issue report.
    assert naturalsize(1000) == "1.0 kB"


@pytest.mark.parametrize(
    "value, expected",
    [
        (1000, "1.0 kB"),
        (1024, "1.0 kB"),
        (-1000, "-1.0 kB"),
        (-1024, "-1.0 kB"),
        (1_000_000, "1.0 MB"),
        (1_000_000_000, "1.0 GB"),
    ],
)
def test_exact_unit_boundaries_decimal(value, expected):
    assert naturalsize(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1024, "1.0 KiB"),
        (-1024, "-1.0 KiB"),
        (1024 ** 2, "1.0 MiB"),
        (1024 ** 3, "1.0 GiB"),
    ],
)
def test_exact_unit_boundaries_binary(value, expected):
    assert naturalsize(value, binary=True) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1024, "1.0K"),
        (-1024, "-1.0K"),
        (1024 ** 2, "1.0M"),
        (1024 ** 3, "1.0G"),
    ],
)
def test_exact_unit_boundaries_gnu(value, expected):
    assert naturalsize(value, gnu=True) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0 Bytes"),
        (1, "1 Byte"),
        (-1, "-1 Byte"),
        (2, "2 Bytes"),
        (999, "999 Bytes"),
        (-999, "-999 Bytes"),
        (1001, "1.0 kB"),
        (1_500, "1.5 kB"),
    ],
)
def test_values_below_one_unit_are_unchanged(value, expected):
    # These already work on the buggy code and must keep working after the fix.
    assert naturalsize(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0B"),
        (1, "1B"),
        (1023, "1023B"),
    ],
)
def test_values_below_one_unit_gnu(value, expected):
    assert naturalsize(value, gnu=True) == expected
