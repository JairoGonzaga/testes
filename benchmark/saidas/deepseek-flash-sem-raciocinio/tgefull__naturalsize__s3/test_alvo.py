import math

import pytest

from alvo import naturalsize, suffixes


def test_suffixes_dictionary_contents():
    assert suffixes["decimal"] == ("kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "RB", "QB")
    assert suffixes["binary"] == ("KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB", "RiB", "QiB")
    assert suffixes["gnu"] == "KMGTPEZYRQ"


def test_zero_decimal():
    assert naturalsize(0) == "0 Bytes"


def test_zero_binary():
    assert naturalsize(0, binary=True) == "0 Bytes"


def test_zero_gnu():
    assert naturalsize(0, gnu=True) == "0B"


def test_one_byte_decimal():
    assert naturalsize(1) == "1 Byte"


def test_minus_one_byte_decimal():
    assert naturalsize(-1) == "-1 Byte"


def test_one_byte_binary():
    assert naturalsize(1, binary=True) == "1 Byte"


def test_minus_one_byte_binary():
    assert naturalsize(-1, binary=True) == "-1 Byte"


def test_one_byte_gnu():
    # gnu path bypasses the singular "Byte" special-case
    assert naturalsize(1, gnu=True) == "1B"


def test_minus_one_byte_gnu():
    assert naturalsize(-1, gnu=True) == "-1B"


def test_few_bytes_decimal():
    assert naturalsize(999) == "999 Bytes"


def test_few_bytes_negative_decimal():
    assert naturalsize(-500) == "-500 Bytes"


def test_few_bytes_binary():
    assert naturalsize(1000, binary=True) == "1000 Bytes"


def test_few_bytes_negative_binary():
    assert naturalsize(-1023, binary=True) == "-1023 Bytes"


def test_few_bytes_gnu():
    assert naturalsize(1023, gnu=True) == "1023B"


def test_few_bytes_negative_gnu():
    assert naturalsize(-1023, gnu=True) == "-1023B"


def test_kilobyte_decimal():
    assert naturalsize(1000) == "1.0 kB"


def test_kilobyte_binary():
    assert naturalsize(1024, binary=True) == "1.0 KiB"


def test_kilobyte_gnu():
    assert naturalsize(1024, gnu=True) == "1.0K"


def test_negative_kilobyte_decimal():
    assert naturalsize(-1000) == "-1.0 kB"


def test_negative_kilobyte_binary():
    assert naturalsize(-1024, binary=True) == "-1.0 KiB"


def test_megabyte_decimal():
    assert naturalsize(1_500_000) == "1.5 MB"


def test_megabyte_binary():
    assert naturalsize(1024 * 1024) == "1.0 MB"


def test_megabyte_binary_flag():
    assert naturalsize(1024 * 1024, binary=True) == "1.0 MiB"


def test_rounding_pushes_to_next_unit_decimal():
    # 999950 is close enough to 1000 kB that rounding produces 1000.0 -> bump to MB
    assert naturalsize(999_950) == "1.0 MB"


def test_rounding_pushes_to_next_unit_binary():
    assert naturalsize(1024 * 1024 - 50, binary=True) == "1.0 MiB"


def test_no_rounding_within_unit():
    # rounding below base does not increment exponent
    assert naturalsize(999_400) == "999.4 kB"


def test_custom_format():
    assert naturalsize(1500, format="%.2f") == "1.50 kB"


def test_custom_format_integer():
    assert naturalsize(2000, format="%d") == "2 kB"


def test_gnu_no_space():
    res = naturalsize(2048, gnu=True)
    assert " " not in res
    assert res == "2.0K"


def test_binary_space():
    assert naturalsize(2048, binary=True) == "2.0 KiB"


def test_gnu_overrides_binary():
    # gnu takes precedence over binary
    assert naturalsize(1024, binary=True, gnu=True) == "1.0K"


def test_large_values_cap_exponent():
    huge = 1000 ** 12
    res = naturalsize(huge)
    # should use the last decimal suffix QB
    assert res.endswith("QB")


def test_large_binary_values_cap_exponent():
    huge = 1024 ** 12
    res = naturalsize(huge, binary=True)
    assert res.endswith("QiB")


def test_large_gnu_values_cap_exponent():
    huge = 1024 ** 12
    res = naturalsize(huge, gnu=True)
    assert res.endswith("Q")


def test_string_input():
    assert naturalsize("1000") == "1.0 kB"


def test_float_input():
    assert naturalsize(1500.0) == "1.5 kB"


@pytest.mark.parametrize(
    "value,expected",
    [
        (0, "0 Bytes"),
        (1, "1 Byte"),
        (2, "2 Bytes"),
        (999, "999 Bytes"),
        (1000, "1.0 kB"),
        (1000 ** 2, "1.0 MB"),
        (1000 ** 3, "1.0 GB"),
        (1000 ** 4, "1.0 TB"),
    ],
)
def test_decimal_table(value, expected):
    assert naturalsize(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (0, "0 Bytes"),
        (1, "1 Byte"),
        (1023, "1023 Bytes"),
        (1024, "1.0 KiB"),
        (1024 ** 2, "1.0 MiB"),
        (1024 ** 3, "1.0 GiB"),
        (1024 ** 4, "1.0 TiB"),
    ],
)
def test_binary_table(value, expected):
    assert naturalsize(value, binary=True) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (0, "0B"),
        (1, "1B"),
        (1023, "1023B"),
        (1024, "1.0K"),
        (1024 ** 2, "1.0M"),
        (1024 ** 3, "1.0G"),
        (1024 ** 4, "1.0T"),
    ],
)
def test_gnu_table(value, expected):
    assert naturalsize(value, gnu=True) == expected


def test_result_type_is_str():
    assert isinstance(naturalsize(1000), str)
    assert isinstance(naturalsize(1000, binary=True), str)
    assert isinstance(naturalsize(1000, gnu=True), str)
