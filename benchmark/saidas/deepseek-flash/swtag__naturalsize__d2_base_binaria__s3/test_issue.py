import pytest

from alvo import naturalsize


def test_binary_uses_powers_of_1024():
    # 3000000 / 1024**2 = 2.86... -> "2.9 MiB"
    assert naturalsize(3000000, binary=True) == "2.9 MiB"


def test_binary_exact_powers_of_1024():
    assert naturalsize(1024, binary=True) == "1.0 KiB"
    assert naturalsize(1024 ** 2, binary=True) == "1.0 MiB"
    assert naturalsize(1024 ** 3, binary=True) == "1.0 GiB"
    assert naturalsize(1024 ** 4, binary=True) == "1.0 TiB"
    assert naturalsize(2048, binary=True) == "2.0 KiB"


def test_binary_negative_values():
    assert naturalsize(-3000000, binary=True) == "-2.9 MiB"
    assert naturalsize(-1024 ** 2, binary=True) == "-1.0 MiB"


def test_binary_threshold_between_units():
    # 1023 bytes stays in bytes, 1024 bytes promotes to KiB
    assert naturalsize(1023, binary=True) == "1023 Bytes"
    assert naturalsize(1024 * 1023, binary=True) == "1023.0 KiB"
    # rounding promotion must also use the binary base
    assert naturalsize(1024 * 1023.99, binary=True) == "1.0 MiB"


def test_binary_large_values():
    # 5 * 1024**6 = 5 PiB (not 5.6... PB scaled with 1000)
    assert naturalsize(5 * 1024 ** 5, binary=True) == "5.0 PiB"
    assert naturalsize(1024 ** 8, binary=True) == "1.0 YiB"


@pytest.mark.parametrize(
    "value, expected",
    [
        (3000000, "3.0 MB"),
        (1000, "1.0 kB"),
        (1000 ** 2, "1.0 MB"),
        (1000 ** 3, "1.0 GB"),
        (999, "999 Bytes"),
        (1, "1 Byte"),
    ],
)
def test_decimal_still_uses_powers_of_1000(value, expected):
    assert naturalsize(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (3000000, "2.9M"),
        (1024, "1.0K"),
        (1024 ** 2, "1.0M"),
        (1023, "1023B"),
    ],
)
def test_gnu_still_uses_powers_of_1024(value, expected):
    assert naturalsize(value, gnu=True) == expected
