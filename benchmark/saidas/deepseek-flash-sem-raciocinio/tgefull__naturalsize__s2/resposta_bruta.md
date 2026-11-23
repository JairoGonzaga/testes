```python
import math

import pytest

from alvo import naturalsize, suffixes


def test_suffixes_constant():
    assert suffixes["decimal"] == ("kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "RB", "QB")
    assert suffixes["binary"] == ("KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB", "RiB", "QiB")
    assert suffixes["gnu"] == "KMGTPEZYRQ"


def test_single_byte_decimal():
    assert naturalsize(1) == "1 Byte"


def test_single_byte_negative():
    assert naturalsize(-1) == "-1 Byte"


def test_single_byte_float():
    assert naturalsize(1.0) == "1 Byte"


def test_zero_decimal():
    assert naturalsize(0) == "0 Bytes"


def test_small_decimal():
    assert naturalsize(999) == "999 Bytes"


def test_small_decimal_negative():
    assert naturalsize(-999) == "-999 Bytes"


def test_just_below_base():
    assert naturalsize(999.999) == "999 Bytes"


def test_exactly_base():
    assert naturalsize(1000) == "1.0 kB"


def test_kilobyte():
    assert naturalsize(1500) == "1.5 kB"


def test_megabyte():
    assert naturalsize(1000000) == "1.0 MB"


def test_gigabyte():
    assert naturalsize(1000000000) == "1.0 GB"


def test_negative_kilobyte():
    assert naturalsize(-1500) == "-1.5 kB"


def test_binary_single_byte():
    assert naturalsize(1, binary=True) == "1 Byte"


def test_binary_zero():
    assert naturalsize(0, binary=True) == "0 Bytes"


def test_binary_small():
    assert naturalsize(1023, binary=True) == "1023 Bytes"


def test_binary_kib():
    assert naturalsize(1024, binary=True) == "1.0 KiB"


def test_binary_mib():
    assert naturalsize(1024 * 1024, binary=True) == "1.0 MiB"


def test_binary_negative():
    assert naturalsize(-2048, binary=True) == "-2.0 KiB"


def test_gnu_single_byte():
    assert naturalsize(1, gnu=True) == "1B"


def test_gnu_zero():
    assert naturalsize(0, gnu=True) == "0B"


def test_gnu_small():
    assert naturalsize(1023, gnu=True) == "1023B"


def test_gnu_k():
    assert naturalsize(1024, gnu=True) == "1.0K"


def test_gnu_m():
    assert naturalsize(1024 * 1024, gnu=True) == "1.0M"


def test_gnu_negative():
    assert naturalsize(-1024, gnu=True) == "-1.0K"


def test_gnu_no_space():
    result = naturalsize(2048, gnu=True)
    assert " " not in result
    assert result == "2.0K"


def test_custom_format():
    assert naturalsize(1500, format="%.2f") == "1.50 kB"


def test_custom_format_integer():
    assert naturalsize(1500, format="%d") == "1 kB"


def test_large_exponent_yb():
    # 1000**8 is YB
    assert naturalsize(1000 ** 8) == "1.0 YB"


def test_large_exponent_beyond():
    # Way beyond the last suffix should clamp to the last one
    assert naturalsize(1000 ** 15) == "10000000.0 QB"


def test_binary_large_beyond():
    assert naturalsize(1024 ** 15, binary=True) == "1048576.0 QiB"


def test_gnu_large_beyond():
    assert naturalsize(1024 ** 15, gnu=True) == "1048576.0Q"


def test_rounding_bump():
    # 999.95 kB should round up to MB when format is %.1f
    result = naturalsize(999.95 * 1000)
    assert result == "1.0 MB"


def test_rounding_bump_binary():
    result = naturalsize(1023.95 * 1024, binary=True)
    assert result == "1.0 MiB"


def test_rounding_bump_gnu():
    result = naturalsize(1023.95 * 1024, gnu=True)
    assert result == "1.0M"


def test_string_value():
    assert naturalsize("1500") == "1.5 kB"


def test_float_value():
    assert naturalsize(1500.0) == "1.5 kB"


def test_binary_flag_and_gnu_gnu_wins():
    # gnu takes precedence over binary
    assert naturalsize(1024, binary=True, gnu=True) == "1.0K"


def test_format_bump_not_triggered_when_already_last():
    # exponent already at len(suffix), no further bump
    result = naturalsize(1000 ** 20)
    assert result.endswith("QB")


def test_exp_negative_abs():
    # abs value less than base handled early; verify negative small
    assert naturalsize(-1023) == "-1023 Bytes"


def test_all_decimal_suffixes():
    expected = ["kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "RB", "QB"]
    for i, suf in enumerate(expected, start=1):
        val = 1000 ** i
        result = naturalsize(val)
        assert result.endswith(suf)
        assert result.startswith("1.0")


def test_all_binary_suffixes():
    expected = ["KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB", "RiB", "QiB"]
    for i, suf in enumerate(expected, start=1):
        val = 1024 ** i
        result = naturalsize(val, binary=True)
        assert result.endswith(suf)
        assert result.startswith("1.0")


def test_all_gnu_suffixes():
    expected = "KMGTPEZYRQ"
    for i, suf in enumerate(expected, start=1):
        val = 1024 ** i
        result = naturalsize(val, gnu=True)
        assert result.endswith(suf)
        assert result.startswith("1.0")
        assert " " not in result


def test_one_byte_gnu_bool():
    # gnu bypasses the "Byte" singular path
    assert naturalsize(1, gnu=True) == "1B"


def test_float_one_decimal():
    assert naturalsize(1.5) == "1 Bytes"


def test_negative_float_one():
    assert naturalsize(-1.0) == "-1 Byte"
```