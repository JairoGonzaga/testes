import math

import pytest

from alvo import naturalsize, suffixes


# ---------------------------------------------------------------- module data
def test_suffixes_structure():
    assert suffixes["decimal"] == ("kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "RB", "QB")
    assert suffixes["binary"] == ("KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB", "RiB", "QiB")
    assert suffixes["gnu"] == "KMGTPEZYRQ"
    assert len(suffixes["decimal"]) == 10
    assert len(suffixes["binary"]) == 10
    assert len(suffixes["gnu"]) == 10


# ------------------------------------------------------- decimal (default)
@pytest.mark.parametrize(
    "value,expected",
    [
        (0, "0 Bytes"),
        (1, "1 Byte"),
        (-1, "-1 Byte"),
        (2, "2 Bytes"),
        (-2, "-2 Bytes"),
        (999, "999 Bytes"),
        (-999, "-999 Bytes"),
        (1000, "1.0 kB"),
        (1023, "1.0 kB"),
        (1024, "1.0 kB"),
        (1500, "1.5 kB"),
        (-1500, "-1.5 kB"),
        (-1000, "-1.0 kB"),
        (999499, "999.5 kB"),
        (999949, "999.9 kB"),
        (999950, "1.0 MB"),
        (99999, "100.0 kB"),
        (1000000, "1.0 MB"),
        (999999, "1.0 MB"),
        (1500000, "1.5 MB"),
        (10 ** 9, "1.0 GB"),
        (10 ** 12, "1.0 TB"),
        (10 ** 15, "1.0 PB"),
        (10 ** 18, "1.0 EB"),
        (10 ** 21, "1.0 ZB"),
        (10 ** 24, "1.0 YB"),
        (10 ** 27, "1.0 RB"),
        (10 ** 30, "1.0 QB"),
    ],
)
def test_decimal(value, expected):
    assert naturalsize(value) == expected


def test_decimal_float_input():
    assert naturalsize(1.9) == "1 Bytes"
    assert naturalsize(-1.9) == "-1 Bytes"
    assert naturalsize(0.9) == "0 Bytes"
    assert naturalsize(-0.9) == "0 Bytes"
    assert naturalsize(0.5) == "0 Bytes"
    assert naturalsize(1023.9) == "1.0 kB"


def test_decimal_above_top_suffix_is_clamped():
    # log(1e33, 1000) is 11, min(11, 10) == 10 -> exp clamps, recheck cannot bump
    assert naturalsize(10 ** 33) == "1000.0 QB"


def test_decimal_recheck_bumps_exp():
    assert naturalsize(999950) == "1.0 MB"
    assert naturalsize(999950.0) == "1.0 MB"
    assert naturalsize(999999.9) == "1.0 MB"
    assert naturalsize(999500) == "999.5 kB"


def test_decimal_custom_format():
    assert naturalsize(1000, format="%.3f") == "1.000 kB"
    assert naturalsize(1, format="%.3f") == "1 Byte"
    assert naturalsize(500, format="%.3f") == "500 Bytes"
    assert naturalsize(1234, format="%.0f") == "1 kB"
    assert naturalsize(1999, format="%d") == "1 kB"
    assert naturalsize(1500, format="%d") == "1 kB"
    assert naturalsize(-1500, format="%.2f") == "-1.50 kB"


# --------------------------------------------------------------- binary
@pytest.mark.parametrize(
    "value,expected",
    [
        (0, "0 Bytes"),
        (1, "1 Byte"),
        (-1, "-1 Byte"),
        (1023, "1023 Bytes"),
        (1000, "1000 Bytes"),
        (1024, "1.0 KiB"),
        (1500, "1.5 KiB"),
        (-1500, "-1.5 KiB"),
        (1047552, "1023.0 KiB"),
        (1048064, "1023.5 KiB"),
        (1048575, "1.0 MiB"),
        (1048576, "1.0 MiB"),
        (1000000, "976.6 KiB"),
        (1000000000, "953.7 MiB"),
        (1024 ** 3, "1.0 GiB"),
        (1024 ** 4, "1.0 TiB"),
        (1024 ** 5, "1.0 PiB"),
        (1024 ** 6, "1.0 EiB"),
        (1024 ** 7, "1.0 ZiB"),
        (1024 ** 8, "1.0 YiB"),
        (1024 ** 9, "1.0 RiB"),
        (1024 ** 10, "1.0 QiB"),
        (8 * 1024 ** 10, "8.0 QiB"),
    ],
)
def test_binary(value, expected):
    assert naturalsize(value, binary=True) == expected


def test_binary_recheck_bumps_exp_only_when_not_clamped():
    # log(1024**10, 1024) == 10 == len(suffix) -> recheck branch skipped
    assert naturalsize(1024 ** 10, binary=True) == "1.0 QiB"
    # log(1024**11, 1024) == 11 -> min(11, 10) == 10, recheck skipped as well
    assert naturalsize(1024 ** 11, binary=True) == "1024.0 QiB"


def test_binary_custom_format():
    assert naturalsize(1536, binary=True, format="%d") == "1 KiB"
    assert naturalsize(1999, binary=True, format="%d") == "1 KiB"
    assert naturalsize(1996, binary=True, format="%.2f") == "1.95 KiB"


# ------------------------------------------------------------------- gnu
@pytest.mark.parametrize(
    "value,expected",
    [
        (0, "0B"),
        (1, "1B"),
        (-1, "-1B"),
        (2, "2B"),
        (1023, "1023B"),
        (-1023, "-1023B"),
        (1024, "1.0K"),
        (1500, "1.5K"),
        (-1500, "-1.5K"),
        (1047552, "1023.0K"),
        (1048064, "1023.5K"),
        (1000000, "976.6K"),
        (1048576, "1.0M"),
        (1500000, "1.4M"),
        (1000000000, "953.7M"),
        (1024 ** 3, "1.0G"),
        (1024 ** 4, "1.0T"),
        (1024 ** 5, "1.0P"),
        (1024 ** 6, "1.0E"),
        (1024 ** 7, "1.0Z"),
        (1024 ** 8, "1.0Y"),
        (1024 ** 9, "1.0R"),
        (1024 ** 10, "1.0Q"),
        (8 * 1024 ** 10, "8.0Q"),
    ],
)
def test_gnu(value, expected):
    assert naturalsize(value, gnu=True) == expected


def test_gnu_single_byte_has_no_byte_word():
    # gnu branch skips the "Byte" special case entirely
    assert naturalsize(1, gnu=True) == "1B"
    assert naturalsize(-1, gnu=True) == "-1B"


def test_gnu_top_suffix_clamped():
    assert naturalsize(1024 ** 11, gnu=True) == "1024.0Q"


def test_gnu_custom_format():
    assert naturalsize(1024, gnu=True, format="%d") == "1K"
    assert naturalsize(2047, gnu=True, format="%d") == "1K"
    assert naturalsize(1024, gnu=True, format="%.3f") == "1.000K"
    assert naturalsize(500, gnu=True, format="%.3f") == "500B"


def test_gnu_takes_precedence_over_binary():
    assert naturalsize(1500, binary=True, gnu=True) == "1.5K"
    assert naturalsize(1023, binary=True, gnu=True) == "1023B"


def test_binary_flag_default_is_false():
    assert naturalsize(1500) == naturalsize(1500, binary=False, gnu=False)
    assert naturalsize(1500) != naturalsize(1500, binary=True)


# -------------------------------------------------------------- odd edge cases
def test_negative_recheck_uses_abs_value():
    # rounding -2047/1024 to one decimal gives -2.0, |−2.0| < 1024 -> no bump
    assert naturalsize(-2047, gnu=True) == "-2.0K"


def test_value_is_cast_to_float():
    assert naturalsize(True) == "1 Byte"
    assert naturalsize(False) == "0 Bytes"


def test_results_are_strings():
    for value in (0, 1, 1024, 10 ** 9):
        assert isinstance(naturalsize(value), str)
        assert isinstance(naturalsize(value, binary=True), str)
        assert isinstance(naturalsize(value, gnu=True), str)


def test_base_constants():
    # decimal uses base 1000, binary/gnu use base 1024
    assert naturalsize(1024) == "1.0 kB"
    assert naturalsize(1000, binary=True) == "1000 Bytes"
    assert naturalsize(1024, binary=True) == "1.0 KiB"
    assert naturalsize(1024, gnu=True) == "1.0K"


def test_space_before_suffix():
    assert naturalsize(1500).count(" ") == 1
    assert " " not in naturalsize(1500, gnu=True)
    assert " " not in naturalsize(1500, binary=True, gnu=True)


def test_log_used_as_expected():
    assert int(min(math.log(1500, 1000), 10)) == 1
    assert naturalsize(1500) == "1.5 kB"
