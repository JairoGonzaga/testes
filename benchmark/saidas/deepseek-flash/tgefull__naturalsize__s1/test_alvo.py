import pytest

from alvo import naturalsize, suffixes


def test_suffix_tables():
    assert suffixes["decimal"] == (
        "kB",
        "MB",
        "GB",
        "TB",
        "PB",
        "EB",
        "ZB",
        "YB",
        "RB",
        "QB",
    )
    assert suffixes["binary"] == (
        "KiB",
        "MiB",
        "GiB",
        "TiB",
        "PiB",
        "EiB",
        "ZiB",
        "YiB",
        "RiB",
        "QiB",
    )
    assert suffixes["gnu"] == "KMGTPEZYRQ"


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0 Bytes"),
        (0.5, "0 Bytes"),
        (-0.5, "0 Bytes"),
        (1, "1 Byte"),
        (-1, "-1 Byte"),
        (1.9, "1 Bytes"),
        (-1.9, "-1 Bytes"),
        (999, "999 Bytes"),
        (-999, "-999 Bytes"),
        (999.9, "999 Bytes"),
        (-999.9, "-999 Bytes"),
        (1000, "1.0 kB"),
        (-1000, "-1.0 kB"),
        (1024, "1.0 kB"),
        (1500, "1.5 kB"),
        (50_000, "50.0 kB"),
        (999_999, "1.0 MB"),
        (-999_999, "-1.0 MB"),
    ],
)
def test_decimal_defaults(value, expected):
    assert naturalsize(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0 Bytes"),
        (0.5, "0 Bytes"),
        (-0.5, "0 Bytes"),
        (1, "1 Byte"),
        (-1, "-1 Byte"),
        (1.9, "1 Bytes"),
        (-1.9, "-1 Bytes"),
        (1000, "1000 Bytes"),
        (-1000, "-1000 Bytes"),
        (1023, "1023 Bytes"),
        (1023.9, "1023 Bytes"),
        (1024, "1.0 KiB"),
        (1536, "1.5 KiB"),
        (-1536, "-1.5 KiB"),
        (50_000, "48.8 KiB"),
        (1024 * 1024 - 1, "1.0 MiB"),
        (1024 * 1024, "1.0 MiB"),
    ],
)
def test_binary(value, expected):
    assert naturalsize(value, binary=True) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0B"),
        (0.5, "0B"),
        (-0.5, "0B"),
        (1, "1B"),
        (-1, "-1B"),
        (1.9, "1B"),
        (-1.9, "-1B"),
        (1000, "1000B"),
        (-1000, "-1000B"),
        (1023, "1023B"),
        (1023.9, "1023B"),
        (1024, "1.0K"),
        (1536, "1.5K"),
        (-1536, "-1.5K"),
        (50_000, "48.8K"),
        (1024 * 1024 - 1, "1.0M"),
        (1024 * 1024, "1.0M"),
    ],
)
def test_gnu(value, expected):
    assert naturalsize(value, gnu=True) == expected


@pytest.mark.parametrize(
    "exponent, suffix",
    [
        (1, "kB"),
        (2, "MB"),
        (3, "GB"),
        (4, "TB"),
        (5, "PB"),
        (6, "EB"),
        (7, "ZB"),
        (8, "YB"),
        (9, "RB"),
        (10, "QB"),
    ],
)
def test_all_decimal_suffixes(exponent, suffix):
    assert naturalsize(2 * (1000**exponent)) == f"2.0 {suffix}"


@pytest.mark.parametrize(
    "exponent, suffix",
    [
        (1, "KiB"),
        (2, "MiB
