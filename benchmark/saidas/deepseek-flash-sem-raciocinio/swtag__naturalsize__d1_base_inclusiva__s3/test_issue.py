import pytest

from alvo import naturalsize


def test_exactly_one_kilobyte_decimal():
    # 1000 bytes is exactly 1 kB and must be converted to the next unit
    assert naturalsize(1000) == "1.0 kB"


def test_exactly_one_kilobyte_float():
    assert naturalsize(1000.0) == "1.0 kB"


def test_exactly_one_kilobyte_negative():
    assert naturalsize(-1000) == "-1.0 kB"


def test_exactly_one_kibibyte_binary():
    assert naturalsize(1024, binary=True) == "1.0 KiB"


def test_exactly_one_kibibyte_gnu():
    assert naturalsize(1024, gnu=True) == "1.0K"


@pytest.mark.parametrize(
    "value, expected",
    [
        (999, "999 Bytes"),
        (1001, "1.0 kB"),
        (1000**2, "1.0 MB"),
        (1024**3, "1.1 GB"),
        (0, "0 Bytes"),
        (1, "1 Byte"),
    ],
)
def test_other_boundaries_unchanged(value, expected):
    assert naturalsize(value) == expected
