import pytest

from alvo import naturalsize


@pytest.mark.parametrize(
    "value, expected",
    [
        (999999, "1.0 MB"),
        (999999999, "1.0 GB"),
        (999999999999, "1.0 TB"),
    ],
)
def test_decimal_units_are_promoted_when_rounding_reaches_the_next_unit(value, expected):
    assert naturalsize(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1024**2 - 1, "1.0 MiB"),
        (1024**3 - 1, "1.0 GiB"),
    ],
)
def test_binary_units_are_promoted_when_rounding_reaches_the_next_unit(value, expected):
    assert naturalsize(value, binary=True) == expected


def test_gnu_units_are_promoted_when_rounding_reaches_the_next_unit():
    assert naturalsize(1024**2 - 1, gnu=True) == "1.0M"
